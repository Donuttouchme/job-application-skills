---
name: cv-writer
description: Produce a CV tailored to one job posting, built from the shared profile at "~/job-search/profile.md" and rendered in three designs as submission-ready PDFs plus ATS-pasteable text. Analyses fit against the posting, tailors emphasis without misrepresenting anything, and can audit an existing CV against the profile. Use when the user wants a CV, résumé or Lebenslauf written, tailored or reviewed for a specific position, points at a job posting and asks for a CV, or starts a new job application.
---

# CV Writer

Build a CV for one posting from `profile.md`, tailoring emphasis but never the
facts. Runs first in the application workflow and offers the letter afterwards.

Swiss market, English or German, chosen by the posting. Always produce all
three designs: the owner's design (**default**), **klassisch**, and
**tabellarisch**. The default is the one to send unless the user picks another.

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
5. **Build the shared content once from `profile.md`.** Use the posting's
   language and all three matching templates in `assets\`: `cv-<de|en>.html`
   (owner default), `cv-klassisch-<de|en>.html`, and
   `cv-tabellarisch-<de|en>.html`. Their header comments specify the exact
   repeated HTML fragments; adapt markup, never facts. Never start from an
   existing variant in `cv\`: that inherits its selections and any drift it
   carries. Consult those variants for phrasing that worked, never for content.
   - `{{PERSONAL}}` is nationality · residence permit, drawn only from the
     Profile's Work eligibility. Include the same line in `cv.txt` and trace
     it as a `fact` citing `profile.md`, not as `contact`. Use only recorded
     facts; omit unavailable parts rather than guessing.
   - If the Profile's Identity and contact names a `Photo` file, copy that file
     into the application folder as `photo.<ext>` (preserve its extension), and
     set `{{PHOTO}}` to `<img class="photo" src="photo.<ext>" alt="">` in all
     three HTML files. Use a relative reference. If Photo is absent or `none`,
     leave `{{PHOTO}}` empty; do not search for a photo or substitute an image.
     A named file that cannot be read is a discrepancy to ask about, not a
     reason to silently choose a different image.
6. **Tailor** per [TAILORING.md](TAILORING.md), writing every line per
   [VOICE.md](VOICE.md).
7. **Write one `cv.txt` and one `cv-trace.md`, then pour that content into
   `cv.html` (default), `cv-klassisch.html`, and `cv-tabellarisch.html`.**
   `cv.txt` is the finished plain text (no decorative letterhead, for ATS
   fields). Follow `../motivational-letter/scripts/TRACE-FORMAT.md`: trace
   every non-empty line as a fact, heading, or contact, and cite facts only to
   `profile.md`. All designs carry identical wording, selections and fact
   order within each section. Only section placement differs: tabellarisch
   places skills and languages last under Kenntnisse / Skills, as its template
   specifies. Do not create a separate content selection or Trace per design.
   Check all three layouts in A4 print preview: each must fit one page. If any
   does not, apply [When it will not fit one page](#when-it-will-not-fit-one-page)
   to the shared content; the tightest design decides. Never trim per design.
8. **Run the deterministic checks before showing any CV content.** Resolve the
   sibling script path `../motivational-letter/scripts/check.py` relative to
   this skill and run:
   `python ../motivational-letter/scripts/check.py phrases cv.txt
   --document-type cv --language <en|de-ch>` and
   `python ../motivational-letter/scripts/check.py trace cv.txt --document-type
   cv --trace cv-trace.md --profile ~/job-search/profile.md`. Fix every blocking
   finding, rewrite the document and trace together, and repeat both commands
   until both exit 0.
9. **Launch the independent checker** as a fresh-context subagent, following
   [Independent checker](#independent-checker). Present its findings; the user,
   not the writer or checker, chooses between the two resolutions.
10. **Iterate with the user.** No PDF while iterating. On every regeneration,
   rewrite all three HTML files, the shared `cv.txt`, and `cv-trace.md`, check
   the one-page fit of each design, then repeat the complete pipeline in steps
   8–9 before showing the result. Apply only changes the user accepted.
11. **On approval** render all three HTML files via `scripts\make-pdf.ps1`.
    Use the Profile's surname and given name, ASCII-folding diacritics
    (for example ä → a, ö → o, ü → u, é → e, ß → ss):
    - German: `Lebenslauf_<Nachname>_<Vorname>.pdf`,
      `Lebenslauf_<Nachname>_<Vorname>_klassisch.pdf`,
      `Lebenslauf_<Nachname>_<Vorname>_tabellarisch.pdf`.
    - English: `CV_<Last>_<First>.pdf`, `CV_<Last>_<First>_klassisch.pdf`,
      `CV_<Last>_<First>_tabellarisch.pdf`.
    Invoke the script once for each corresponding HTML/PDF pair, and verify
    each PDF has exactly one A4 page. If any overflows, revise only shared
    content per the fit rule, regenerate all designs, rerun the checks, and
    obtain approval again before rendering. Send the default unless the user
    picks another; record the exact PDF filename sent in `application.md`.
12. **Offer the letter** — invoke `motivational-letter` only if the user says
    yes. Applications wanting only a CV are common.

## Check

For an existing CV, prepare or update `cv.txt` and `cv-trace.md`, run both
commands in Write step 8 until they exit 0, then use the same fresh-context
subagent in Write step 9. Present its findings and let the user decide; apply
only accepted changes, regenerate every output, and rerun the complete
pipeline.

## Independent checker

Use Claude Code's Task / subagent tool to launch a fresh-context subagent. Do
not pass it the drafting conversation or the writer's reasoning. Give it this
instruction, substituting the paths for the current installation and
application:

> Review this finished CV independently. Read only these files:
> - this skill's `CHECKER.md` and `VOICE.md`
> - `~/job-search/profile.md`
> - this application's `posting.md` and `fit.md`
> - this application's letter, if one exists
> - this application's finished `cv.txt` and `cv-trace.md`
> - this application's `cv.html`, `cv-klassisch.html`, and `cv-tabellarisch.html`
> - all three approved CV PDFs, if they already exist
>
> Do not read any other file or use prior conversation. In particular, never
> read `profile-history.md`, `search.md`, the drafting conversation, or the
> writer's reasoning. Apply every rule in `CHECKER.md`. For every fact in the
> trace, compare the CV unit directly with its cited excerpt and flag any
> unsupported escalation of scope, role, magnitude, or ownership; the presence
> of a real excerpt is not enough. Check consistency with the letter only when
> it was included. Return findings only, in `CHECKER.md`'s output format. Treat
> each finding as a discrepancy rather than a verdict and give both
> resolutions: the CV is wrong and must be corrected, or the claim is true and
> `profile.md` under-records it. Do not edit any file and do not choose a
> resolution for the user.

If the environment has no Task / subagent tool, say so to the user, run these
same checker instructions in the current session with exactly the same file
limits, and state explicitly that the fallback check is not independent.

## When it will not fit one page

All three designs must fit one A4 page. The tightest design decides the shared
content budget. Apply every accepted reduction to `cv.txt`, `cv-trace.md`, and
all three HTML/PDF outputs; never trim content for just one design.

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
- **ATS constraints are binding on every template:** single column (the
  tabellarisch date gutter labels a row, not a column layout), no images except
  the optional header photo, no tables, real text. Do not "improve" them away.
- `~/job-search/` holds personal data: never transmitted, never version
  controlled.
