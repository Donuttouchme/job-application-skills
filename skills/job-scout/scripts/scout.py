"""Candidate fetcher and seen-ledger for the job-scout skill.

  python scout.py fetch [--max-km 70] [--days 30]   -> JSON candidates on stdout
  python scout.py mark <json-file>                   -> append reviewed postings to the ledger
  python scout.py seen                               -> print the ledger

Sources queried here: jobs.ch (public search API), swissdevjobs.ch (public JSON
feed) and LinkedIn's public guest listing. Sources the script cannot reach are
searched by the agent and recorded with `mark` like any other.
"""
import json
from html import unescape
import math
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

try:  # Windows certificate store; Python's bundled one rejects some Workday chains
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

import os

# Everything personal lives in the job-search folder, never in this script.
BASE = Path(os.environ.get("JOB_SEARCH_DIR", Path.home() / "job-search")).expanduser()
LEDGER = BASE / "scout-seen.json"
COMPANIES = BASE / "scout-companies.json"
CONFIG = BASE / "scout-config.json"
if not CONFIG.exists():
    sys.exit(f"No {CONFIG}. Copy scout-config.example.json from the job-scout skill there and fill it in.")
CFG = json.loads(CONFIG.read_text(encoding="utf-8"))

HOME = tuple(CFG["home"])  # (lat, lon) the distance filter measures from
QUERIES = CFG["queries"]
LINKEDIN_QUERIES = CFG.get("linkedin_queries", QUERIES)
WORKDAY_QUERIES = CFG.get("workday_queries", QUERIES)
# Titles out of reach or out of scope before any reading, and places out of range.
SKIP_TITLE = re.compile(CFG.get("skip_title") or r"(?!x)x", re.I)
SKIP_PLACE = re.compile(CFG.get("skip_place") or r"(?!x)x", re.I)
JOBS_CH = "https://www.jobs.ch/api/v1/public/search?query={q}&rows=20&page={p}"  # rows > 20 is rejected
SWISSDEVJOBS = "https://swissdevjobs.ch/api/jobsLight"
# LinkedIn's distance is in miles and is measured from its own location string.
LINKEDIN = ("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
            "?keywords={q}&location=" + urllib.parse.quote(CFG["linkedin_location"])
            + "&distance=" + str(CFG.get("linkedin_distance_miles", 40))
            + "&f_TPR=r2592000&start={s}")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = re.sub(r"\(.*?\)|\d+\s*-?\s*\d*\s*%|m/w/d|w/m/d|all genders", "", s.lower())
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def key(company: str, title: str) -> str:
    return f"{norm(company)}|{norm(title)}"


def km(a, b) -> float:
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def load_ledger() -> list:
    return json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else []


def get(url: str, as_json: bool = True):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r) if as_json else r.read().decode("utf-8", "replace")


# Every source yields records of one shape; `km` is None where the source gives
# no coordinates (LinkedIn), which is then bounded by its own location query.

def from_jobs_ch():
    for q in QUERIES:
        for page in (1, 2, 3, 4):
            try:
                data = get(JOBS_CH.format(q=urllib.parse.quote(q), p=page))
            except Exception as e:  # one failing query must not sink the run
                print(f"warn: jobs.ch {q} p{page}: {e}", file=sys.stderr)
                break
            for d in data.get("documents", []):
                c = d.get("coordinates") or {}
                yield {
                    "id": f"jobs.ch:{d['job_id']}", "source": "jobs.ch",
                    "title": d.get("title"), "company": d.get("company_name"),
                    "place": d.get("place"),
                    "km": round(km(HOME, (c["lat"], c["lon"]))) if c else None,
                    "published": d["publication_date"][:10],
                    "languages": d.get("language_skills"),
                    "url": d["_links"]["detail_en"]["href"],
                    "preview": d.get("preview"),
                }
            if page >= data.get("num_pages", 1):
                break
            time.sleep(0.5)


def from_swissdevjobs():
    # One JSON list of every live IT posting, with level, salary and language.
    try:
        jobs = get(SWISSDEVJOBS)
    except Exception as e:
        print(f"warn: swissdevjobs: {e}", file=sys.stderr)
        return
    for d in jobs:
        if d.get("isPaused") or d.get("expLevel") in ("Senior", "Lead", "Principal"):
            continue
        has_geo = d.get("latitude") is not None
        sal = d.get("annualSalaryFrom")
        yield {
            "id": f"swissdevjobs:{d['_id']}", "source": "swissdevjobs.ch",
            "title": d.get("name"), "company": d.get("company"),
            "place": d.get("actualCity"),
            "km": round(km(HOME, (d["latitude"], d["longitude"]))) if has_geo else None,
            "published": (d.get("activeFrom") or "")[:10],
            "languages": d.get("language"),
            "url": f"https://swissdevjobs.ch/jobs/{d['jobUrl']}",
            "preview": f"{d.get('expLevel')} · {d.get('techCategory')} · "
                       f"{', '.join(d.get('technologies', [])[:8])}"
                       + (f" · CHF {sal}–{d.get('annualSalaryTo')}" if sal else ""),
        }


def from_linkedin():
    # Public guest listing, no login. Read-only discovery: applications still go
    # through the company's own channel, never Easy Apply.
    card = re.compile(
        r'jobPosting:(\d+).*?base-search-card__title">\s*(.*?)\s*</h3>.*?'
        r'base-search-card__subtitle">.*?>\s*(.*?)\s*</.*?'
        r'job-search-card__location">\s*(.*?)\s*</span>.*?datetime="([\d-]+)"',
        re.S,
    )
    for q in LINKEDIN_QUERIES:
        for start in (0, 25):
            url = LINKEDIN.format(q=urllib.parse.quote(q), s=start)
            try:
                html = get(url, as_json=False)
            except Exception as e:
                print(f"warn: linkedin {q} {start}: {e}", file=sys.stderr)
                break
            found = card.findall(html)
            for jid, title, company, place, date in found:
                yield {
                    "id": f"linkedin:{jid}", "source": "linkedin",
                    "title": unescape(title), "company": unescape(company),
                    "place": unescape(place), "km": None, "published": date,
                    "languages": None,
                    "url": f"https://www.linkedin.com/jobs/view/{jid}/",
                    "preview": None,
                }
            if len(found) < 25:
                break
            time.sleep(2)


def load_companies() -> list:
    return json.loads(COMPANIES.read_text(encoding="utf-8")) if COMPANIES.exists() else []


def from_workday(c):
    # Workday's own career-site API: POST a search, get titles and paths back.
    for q in WORKDAY_QUERIES:
        body = json.dumps({"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": q}).encode()
        req = urllib.request.Request(
            c["endpoint"] + "/jobs", data=body,
            headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                posts = json.load(r).get("jobPostings", [])
        except Exception as e:
            print(f"warn: {c['name']} {q}: {e}", file=sys.stderr)
            continue
        for p in posts:
            loc = p.get("locationsText", "")
            if c.get("location_filter") and not re.search(c["location_filter"], loc + p["externalPath"], re.I):
                continue
            yield {
                "id": f"workday:{c['name']}:{p['externalPath']}", "source": f"career page ({c['name']})",
                "title": p["title"], "company": c["name"], "place": loc, "km": c.get("km"),
                "published": None, "languages": None,
                "url": c["site"] + p["externalPath"], "preview": p.get("postedOn"),
            }
        time.sleep(0.5)


def from_links(c):
    # Server-rendered list (prospective.ch and similar): job URLs matched by a
    # per-company pattern whose first group is the title slug.
    try:
        html = get(c["url"], as_json=False)
    except Exception as e:
        print(f"warn: {c['name']}: {e}", file=sys.stderr)
        return
    keep = re.compile(c.get("title_filter", "."), re.I)
    for m in dict.fromkeys(re.findall(c["pattern"], html)):
        if not keep.search(m[0]):
            continue
        url = c["url_template"].format(*m)
        yield {
            "id": f"links:{c['name']}:{m[1]}", "source": f"career page ({c['name']})",
            "title": m[0].replace("-", " "), "company": c["name"], "place": c.get("place"),
            "km": c.get("km"), "published": None, "languages": None, "url": url, "preview": None,
        }


def from_career_pages():
    for c in load_companies():
        if c["type"] == "workday":
            yield from from_workday(c)
        elif c["type"] == "links":
            yield from from_links(c)
        # type "manual": the agent reads the page itself (see SKILL.md)


SOURCES = {
    "jobs.ch": from_jobs_ch, "swissdevjobs": from_swissdevjobs,
    "linkedin": from_linkedin, "career pages": from_career_pages,
}


def fetch(max_km: float, days: int) -> None:
    ledger = load_ledger()
    seen_ids = {e["id"] for e in ledger}
    seen_keys = {key(e["company"], e["title"]) for e in ledger}
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    out, taken, counts = [], set(), {}
    for name, source in SOURCES.items():
        n = 0
        for r in source():
            k = key(r["company"], r["title"])
            if r["id"] in seen_ids or k in seen_keys or k in taken:
                continue  # the key also folds one posting listed on several boards
            if SKIP_TITLE.search(r["title"] or "") or SKIP_PLACE.search(r["place"] or ""):
                continue
            if (r["km"] is not None and r["km"] > max_km) or (r["published"] and r["published"] < cutoff):
                continue
            taken.add(k)
            out.append(r)
            n += 1
        counts[name] = n
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    print(f"\n{len(out)} new candidates {counts}", file=sys.stderr)


def mark(path: str) -> None:
    """Each entry needs id, source, company, title, url, verdict (shown|rejected) and reason."""
    new = json.loads(Path(path).read_text(encoding="utf-8"))
    ledger = load_ledger()
    ids = {e["id"] for e in ledger}
    today = datetime.now().strftime("%Y-%m-%d")
    for e in new:
        if e["id"] not in ids:
            e.setdefault("date", today)
            ledger.append(e)
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ledger: {len(ledger)} entries")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if not args or args[0] not in ("fetch", "mark", "seen"):
        sys.exit(__doc__)
    if args[0] == "fetch":
        opts = dict(zip(args[1::2], args[2::2]))
        fetch(float(opts.get("--max-km", 70)), int(opts.get("--days", 30)))
    elif args[0] == "mark":
        mark(args[1])
    else:
        print(json.dumps(load_ledger(), ensure_ascii=False, indent=1))
