---
name: cv-writer
description: Produce a CV tailored to one job posting, built from the shared profile at "~/job-search/profile.md" and rendered as a submission-ready PDF plus ATS-pasteable text. Analyses fit against the posting, tailors emphasis without misrepresenting anything, and can audit an existing CV against the profile. Use when the user wants a CV, résumé or Lebenslauf written, tailored or reviewed for a specific position, points at a job posting and asks for a CV, or starts a new job application.
---

# CV Writer

Build a CV for one posting from `profile.md`, tailoring emphasis but never the
facts. Runs first in the application workflow and offers the letter afterwards.

Swiss market, English or German, chosen by the posting.

## Paths

| What | Where |
|---|---|
| Profile — the only content source | `~/job-search/profile.md` |
| Profile history — never read | `~/job-search/profile-history.md` |
| Search constraints — never read | `~/job-search/search.md` |
| Templates for reference wording | `~/job-search/cv/` |
| This application | `~/job-search/applications/YYYY-MM-DD-<company>-<role>/` |

## Routing

1. **Profile missing or below its ready gate** → invoke `job-profile`. A CV built
   from an incomplete profile inherits the gaps silently.
2. **Posting supplied**, no CV in play → **Write**.
3. **Existing CV supplied** → **Check**, per [CHECKER.md](CHECKER.md).

## Write

Create a todo per step.

1. **Get the posting.** URL → WebFetch. Login wall, thin response, or clearly not
   a posting → stop and ask for it pasted. Never reconstruct one.
2. **Create the application directory**; write `posting.md` (raw text, URL, date)
   and `application.md` (date, company, position, channel, contact, status).
3. **Pick the language** from the posting.
4. **Fit analysis → `fit.md`**, following
   `..\motivational-letter\FIT-ANALYSIS.md` — one shared method, deliberately
   not reimplemented here. Reuse an existing `fit.md` for this posting only
   when both the posting and the Profile (`profile.md`) predate it; otherwise
   redo the analysis.
5. **Build content from `profile.md`, layout from `assets\cv-en.html` or
   `assets\cv-de.html`.** Never start from an existing variant in `cv\`: that
   inherits its selections and any drift it carries. Consult those variants for
   phrasing that worked, never for content.
6. **Tailor** per [TAILORING.md](TAILORING.md), writing every line per
   [VOICE.md](VOICE.md).
7. **Write `cv.html`, `cv.txt`, and `cv-trace.md`.** `cv.txt` is the finished
   plain text (no letterhead, for ATS fields). Follow
   `../motivational-letter/scripts/TRACE-FORMAT.md`: trace every non-empty line
   as a fact, heading, or contact, and cite facts only to `profile.md`.
8. **Check before showing any CV content.** Self-check per
   [CHECKER.md](CHECKER.md), then resolve the sibling script path
   `../motivational-letter/scripts/check.py` relative to this skill and run:
   `python ../motivational-letter/scripts/check.py phrases cv.txt
   --document-type cv --language <en|de-ch>` and
   `python ../motivational-letter/scripts/check.py trace cv.txt --document-type
   cv --trace cv-trace.md --profile ~/job-search/profile.md`. Fix every blocking
   finding first.
9. **Iterate with the user.** No PDF while iterating. On every regeneration,
   rewrite `cv.html`, `cv.txt`, and `cv-trace.md`, then repeat both checks in
   step 8 before showing the result.
10. **On approval** render `cv.pdf` via `scripts\make-pdf.ps1` and record in
    `application.md` which CV was sent.
11. **Offer the letter** — invoke `motivational-letter` only if the user says
    yes. Applications wanting only a CV are common.

## When it will not fit one page

Give way in this order, and never silently:

1. tighten wording — same fact, fewer words
2. drop a non-`[core]` position bullet — least relevant by `fit.md`
3. drop a project — weakest by `fit.md`, unless it is the only visible evidence
   for a listed skill, in which case the skill goes with it
4. stop and ask

## Hard rules

- **Content comes only from `profile.md`.** The posting supplies vocabulary and
  priorities, never facts.
- **The shared checks are a display gate.** Never show a new or regenerated CV
  until both `phrases` and `trace` exit 0 against the current `cv.txt` and
  `cv-trace.md`. If `../motivational-letter/scripts/` is missing, stop and say:
  "The motivational-letter skill is not installed beside cv-writer; install it
  to run the required CV checks." Never skip or recreate the sibling checker.
- **Every `[core]` bullet appears in every CV.** Non-`[core]` bullets may be
  selected among; `[core]` ones may not.
- **Every listed skill must have visible evidence in the CV.** Where the
  evidence is a personal project, the Projects section labels it as one — that
  is qualification enough. Drop the project and the skill loses its standing.
- **A finding is a discrepancy, not a verdict.** When the CV and the profile
  disagree, the profile is wrong at least as often as the CV. Offer both
  resolutions; never auto-remove a claim.
- **ATS constraints are binding on the template:** single column, no images, no
  tables, real text. All four already hold — do not "improve" them away.
- `~/job-search/` holds personal data: never transmitted, never version
  controlled.
