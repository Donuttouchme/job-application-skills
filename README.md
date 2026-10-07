# The owner's job-search toolkit

Four [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills)
for the repo owner's own job search, not a generic product: the **Swiss market**,
English and Swiss German, and a career change into **DevOps / Platform**.

| Skill | What it does |
|---|---|
| `job-profile` | Seeds from existing CVs, interviews for gaps, and maintains the Profile, Profile history and Search constraints. |
| `job-scout` | Searches Swiss job boards and company career pages; returns at most five ranked postings and remembers every posting reviewed. |
| `cv-writer` | Tailors a one-page, ATS-safe CV from the Profile only; produces plain text, a Trace and an approved PDF. |
| `motivational-letter` | Researches the company, analyses fit, writes or reviews a letter; produces plain text, a Trace, an approved PDF and a covering email. |

**Nothing gets invented.** Unknown facts stay `[NEEDED]` until the owner fills
them. Use `job-scout` to find postings, then `cv-writer` for a chosen posting;
the letter is optional. DevOps / Platform is the primary **Lane**. The second
Lane, **junior software engineer**, fills shortlist slots only when the primary
Lane has fewer than five good postings.

## Install

Install **all four skill folders together**, as siblings in your personal
skills directory. From the repo root, in Bash (Git Bash on Windows):

```bash
mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/
```

On Windows that directory is `%USERPROFILE%\.claude\skills\`.
`cv-writer` calls `../motivational-letter/scripts/check.py` and shares its fit
analysis rules; the letter also uses the CV writer's voice rules. Installing
only a writer is not enough.

## Set up your job-search folder

Keep personal data outside this repo, in `~/job-search/` by default. For a
different folder, set `JOB_SEARCH_DIR` for the scout and tell the other skills
to use the same path. Create the folder and add your existing documents:

```text
~/job-search/
  cv/                    existing CVs (HTML or text versions are easiest to read)
  documents/             certificates, references, diplomas
  archive/letters/       old letters (optional)
  profile.md             Profile, created by job-profile
  profile-history.md     Profile history, created by job-profile
  search.md              Search constraints, created by job-profile
  scout-config.json      search settings, copied from the example below
  applications/          created per application by the skills
```

Ask Claude to "build my job profile"; `job-profile` seeds from your CVs and
interviews you for the rest. It owns all three profile documents:

| Document | Purpose and readers |
|---|---|
| **Profile** (`profile.md`) | Current verified facts; read by `cv-writer`, `motivational-letter` and `job-scout`. |
| **Profile history** (`profile-history.md`) | Replaced facts and why they changed; consulted only by `job-profile`, never by writers or the scout. |
| **Search constraints** (`search.md`) | Commute, working hours, licence and health parameters, with permission to state them; read by `motivational-letter` and `job-scout`, never by `cv-writer`. |

For `job-scout`, copy `skills/job-scout/scout-config.example.json` to
`~/job-search/scout-config.json` and set your home coordinates, LinkedIn
location, search queries and exclusions from the Profile and Search constraints.

**Never put `~/job-search/` under version control or anywhere public.** It holds
personal profile and application data.

## Checks

Both writers use `skills/motivational-letter/scripts/check.py` before showing
any draft or revision:

- `phrases` checks the shared banned-phrase list, ignoring case, and flags
  `ß` in Swiss German (`de-ch`).
- `trace` checks every CV line or letter sentence against its **Trace**.
  Facts need excerpts from allowed sources: the Profile only for a CV; the
  Profile, company facts, motivation or Search constraints for a letter.
  Profile history is never allowed.

Blocking findings must be fixed. A valid Trace does not prove a claim is
accurate: a fresh-context **independent checker** then checks for inflated
scope, role, magnitude or ownership. It never sees Profile history or the
drafting conversation. The owner decides whether the document is wrong or the
Profile under-records a true claim. Without a subagent tool, the skills disclose
that their same-session fallback is not independent.

See [Trace format and check commands](skills/motivational-letter/scripts/TRACE-FORMAT.md)
for inputs and exit codes. Run the shared check script's tests from the repo root:

```bash
python -m unittest discover -s skills/motivational-letter/scripts/tests -v
```

## Requirements

- Claude Code with web fetch enabled for postings and company research, and a
  Task / subagent tool for the independent checker.
- Python 3 for the shared check script, its tests and `job-scout`; standard
  library only (`truststore` is optional for the scout on Windows).
- Windows with Microsoft Edge or Google Chrome for PDF rendering
  (`make-pdf.ps1`). On macOS or Linux, replace that step with a headless browser
  print-to-PDF.

The skills use Swiss German orthography, SN 010130 letter layout, Swiss job
boards and the RAV portal; they are tuned for this job search.
