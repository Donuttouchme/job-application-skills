# Job application skills for Claude Code

Four [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills) that
work together on a job search for the **Swiss market** (English or Swiss German):

| Skill | What it does |
|---|---|
| `job-profile` | Interviews you once and builds `profile.md`, the single source of truth for every claim in a CV or letter: positions, stories with measurable outcomes, skills with an honest evidence level, your writing voice. |
| `job-scout` | Searches jobs.ch, swissdevjobs.ch, LinkedIn's public listing and company career pages, and returns a ranked shortlist of at most five postings that fit your profile. Remembers every posting it has shown you. |
| `cv-writer` | Tailors a one-page, ATS-safe CV to one posting, from the profile only, and renders it to PDF. |
| `motivational-letter` | Writes or reviews a cover letter / Motivationsschreiben: researches the company, analyses fit, drafts within a word budget, checks for clichés and AI tells, renders a PDF plus a covering email. |

The core rule across all four: **nothing gets invented.** Every fact comes from
your profile; a gap stays marked `[NEEDED]` until you fill it.

## Install

Copy the folders under `skills/` into your personal skills directory:

```bash
cp -r skills/* ~/.claude/skills/
```

On Windows that directory is `%USERPROFILE%\.claude\skills\`.

## Set up your job-search folder

The skills keep all your personal data in one folder, `~/job-search/` by default
(set `JOB_SEARCH_DIR` to move it). Create it with:

```
~/job-search/
  cv/                    existing CVs (HTML or text versions are easiest to read)
  documents/             certificates, references, diplomas
  archive/letters/       old letters (optional)
  applications/          created per application by the skills
```

Then ask Claude to build your profile ("build my job profile"); `job-profile`
seeds it from your CVs and interviews you for the rest. For `job-scout`, copy
`skills/job-scout/scout-config.example.json` to `~/job-search/scout-config.json`
and set your home coordinates, LinkedIn location, search queries and
exclusions.

**Never put `~/job-search/` under version control or anywhere public.** It holds
your address, salary expectation and work permit details.

## Requirements

- Claude Code with web fetch enabled (postings and company research)
- Python 3 for `job-scout` (standard library only; `truststore` optional on Windows)
- Windows with Microsoft Edge or Google Chrome for the PDF rendering
  (`make-pdf.ps1`). On macOS or Linux, replace that step with any headless
  browser print-to-PDF.

## Adapting

The skills assume Switzerland: CHF salaries, Swiss German orthography (no `ß`),
SN 010130 letter layout, jobs.ch and the RAV portal. For another market, change
`STYLE-*.md` in `motivational-letter` and the sources in `job-scout/scripts/scout.py`.
