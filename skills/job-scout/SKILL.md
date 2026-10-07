---
name: job-scout
description: Find Swiss job postings worth applying to, judged against the user's profile, direction and filter, and return a short ranked shortlist that never repeats a posting already reviewed. Use when the user asks to find, search or scout jobs or roles, or asks what to apply to next.
---

# Job Scout

A **shortlist**, never a list: at most five postings, each with the reason it is
worth an application. Volume is the usual failure mode of a job search (hundreds
of applications, a handful of interviews); the scout exists to pick, not to
collect.

## Paths

| What | Where |
|---|---|
| Profile: evidence, languages, direction | `~/job-search/profile.md` |
| Search constraints: commute, working hours, licence, health parameters | `~/job-search/search.md` |
| Profile history — never read | `~/job-search/profile-history.md` |
| Applications already sent | `~/job-search/applications-log.md` |
| Seen-ledger: every posting ever reviewed | `~/job-search/scout-seen.json` |
| Company watchlist: career pages searched every run | `~/job-search/scout-companies.json` |
| Search settings: home, radius, queries, exclusions | `~/job-search/scout-config.json` (start from `scout-config.example.json`) |
| Fetcher | `scripts/scout.py` |

The folder can be moved: set `JOB_SEARCH_DIR` and the script follows it.

## The filter

A posting makes the shortlist only when all four hold:

1. **Evidence covers at least half the must-haves.** Count against what
   `profile.md` can prove, at its recorded strength: `strong` counts 1,
   `transferable` ½, `weak` ½, and `missing` 0.
2. **Daily contact with the direction.** The work itself touches the direction
   recorded in `profile.md` → *Career narrative → What is wanted now*, so every
   working day builds toward it. A support role qualifies when the systems it
   supports do.
3. **Language within reach.** The posting's language requirement is at or below
   the user's CEFR level in `profile.md`, or the team works in English. The
   jobs.ch `language_skills` level is a hint (observed 1–4); read the posting
   text before deciding.
4. **Reachable and in scope:** within the commute and working-hour limits in
   `search.md`, outside any lane the profile has closed, at a seniority the
   profile can back.

Salary is reported, never filtered on, unless the profile sets a hard floor.

## Run

1. **Fetch**: `python scripts/scout.py fetch` (options `--max-km 70`,
   `--days 30`). It queries jobs.ch, swissdevjobs.ch, LinkedIn's public
   listing and the machine-readable career pages in the company watchlist,
   folds one posting listed on several boards into one, and drops postings
   already in the ledger, out of radius, in an excluded place, or with an
   excluded title (both set in `scout-config.json`). A LinkedIn hit is discovery
   only: the application goes through the company's own channel, never Easy
   Apply.
2. **Widen** with one pass over what the fetcher cannot reach:
   - every watchlist company of type `manual`: read its career page (WebFetch;
     a browser tool when the list renders only in JavaScript) and take the
     postings that fit the title scope;
   - **job-room.ch**, the RAV portal, if the user is registered there: it needs
     their login, so remind them to check it; postings under the
     *Stellenmeldepflicht* are visible there to registered job seekers for five
     working days before anywhere else.
   Drop any whose company and title already appear in the ledger.
3. **Triage by title and preview.** Keep the ones that could pass the filter;
   every other candidate gets verdict `rejected` with a few-word reason.
4. **Read each kept posting in full** (WebFetch) and apply the filter line by
   line. A posting that fails any line is `rejected`, reason named.
5. **Check `applications-log.md`**: a company already applied to is shown only
   with that fact stated.
6. **Rank the survivors** by filter line 1; at equal score, transferable
   evidence outranks weak. Then use line 2. Take the top five.
7. **Record every reviewed posting**, shown and rejected alike, in a JSON file
   of `{id, source, company, title, url, verdict, reason}` and run
   `python scripts/scout.py mark <file>`. The run is complete when the ledger
   holds every candidate from steps 1–2; a posting left out will come back next
   run.

## First run

No `scout-config.json` yet → copy `scout-config.example.json` from this skill
into the job-search folder and fill it with the user: home coordinates (a town
centre is enough), the LinkedIn location and radius, search queries for their
direction, title words to skip, places to skip. Derive commute and working-hour
defaults from `search.md`, derive the direction from `profile.md`, and confirm
them rather than asking from zero.

## Company watchlist

`~/job-search/scout-companies.json` lists employers whose own career pages are
searched every run. Three types:

| Type | When | Fields |
|---|---|---|
| `workday` | the careers link points at `*.myworkdayjobs.com` | `endpoint` (`https://<tenant>.wd<n>.myworkdayjobs.com/wday/cxs/<tenant>/<site>`), `site`, `location_filter` regex |
| `links` | jobs are plain links in the page HTML (prospective.ch and similar) | `url`, `pattern` regex with groups (title slug, id), `url_template`, optional `title_filter` |
| `manual` | anything else, including JavaScript-only lists | `url`; read by the agent in step 2 |

Add a company whenever a run, the user or market research names an employer in
range that hires for the direction. Probe its careers page first: a Workday or
link-pattern match saves a manual read on every future run.

## Output

Per shortlisted posting:

```markdown
### <n>. <Title> — <Company>, <Place> (<km> km, published <date>)
<url>
**Why this:** <one or two sentences: which evidence carries it and what the
work builds toward>
**Must-haves covered:** <x of y>. **Gap:** <the one thing to defend or learn>
**Language:** <what the posting asks>. **Salary:** <if stated>
```

Close with one line of counts (fetched, triaged out, read in full, shortlisted)
and an offer to start the application with `cv-writer` for any of them.
