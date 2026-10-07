---
name: motivational-letter
description: Write or review a cover letter (EN) or Motivationsschreiben (DE-CH) for a job application on the Swiss market. Researches the company, analyses fit against the posting, drafts within a word budget, and renders a submission-ready PDF plus an ATS-pasteable text and a covering email. Use when the user wants a motivational letter, cover letter, Bewerbung, Anschreiben or Motivationsschreiben written or checked, points at a job posting URL, or pastes a posting and asks what to write.
---

# Motivational Letter

Turn a job posting into a submission-ready letter, or review one that exists.
Swiss market: **Motivationsschreiben** (DE-CH) or **cover letter** (EN).

## Paths

| What | Where |
|---|---|
| Profile | `~/job-search/profile.md` |
| Search constraints | `~/job-search/search.md` |
| Profile history — never read | `~/job-search/profile-history.md` |
| CV variants | `~/job-search/cv/` |
| Certificates, diplomas | `~/job-search/documents/` |
| Previous letters | `~/job-search/archive/letters/` |
| This application | `~/job-search/applications/YYYY-MM-DD-<company>-<role>/` |

## Routing

1. **No `profile.md` or `search.md`, or a Profile below the ready gate** →
   invoke the `job-profile` skill. A profile that merely exists is not enough:
   check its ready gate — a street address, a CHF salary expectation, CEFR
   levels, the narrative, and at least two stories carrying a measurable
   outcome, none of them marked `[NEEDED]`. Never write a letter from a Profile
   below the gate; the result is generic filler that reads worse than no
   letter.
2. **Posting supplied** (URL or pasted), no letter in play → **Write**.
3. **Existing letter supplied** → **Check**.

Ambiguous — for example an application directory that already holds
`letter.md` — means **ask**, never guess.

## Write

Create a todo per step and work through them in order.

1. **Get the posting.** URL → WebFetch. Login wall, thin response, or clearly
   not a posting → stop and ask for it pasted. Never reconstruct a posting.
2. **Create the application directory.** Save `posting.md` (raw text, URL,
   date) and `application.md` (date, company, position, channel, contact,
   status — the fields an RAV job-search log asks for).
3. **Research the company → `company.md`.** About / Products / News, plus the
   **Impressum** for the legal name and postal address. 3–5 concrete facts,
   **each with its source URL**. Also capture the contact person and any
   `Referenznummer`. Nothing found → say so and write no company praise.
4. **Pick the language** from the posting; load `STYLE-DE-CH.md` or
   `STYLE-EN.md`. Swiss company with an English posting → ask.
5. **Fit analysis → `fit.md`**, per [FIT-ANALYSIS.md](FIT-ANALYSIS.md). Reuse an
   existing `fit.md` for this posting only when both the posting and the
   Profile (`profile.md`) predate it; otherwise redo the analysis. Present it
   and get approval before drafting. All must-haves weak or missing → say so
   plainly first.
6. **Recommend a CV variant** from `cv\`, read it, and write to **complement**
   it — never contradicting, never restating.
7. **Ask the user for the reason → `motivation.md`.** Two or three short
   questions, in the user's language: *Why this job? What about the work do you
   want to do every day? Is there anything about this company that actually
   pulled you, or is it the role?* Offer what is already known (earlier answers,
   memory) for confirmation rather than asking from zero. Record the answers in
   the user's own words. **The letter's motivation comes only from here.** No
   answer, no motivation sentence: a letter without a stated reason is better
   than one with an invented reason.
8. **Check phrasing against `archive\letters\`.** Report reused openings,
   closings, and paragraph skeletons. Reusing a *story* is fine and expected.
   Same company already in the archive → warn explicitly.
9. **Draft and trace.** Draft from the Profile, Search constraints and approved
   motivation, within the word budget and in the user's voice per
   [`..\cv-writer\VOICE.md`](../cv-writer/VOICE.md): the reason from
   `motivation.md`, the evidence from `fit.md`. Write `letter.md`, `letter.txt`
   (the plain-text body, with no letterhead), and `letter-trace.md` per
   [scripts/TRACE-FORMAT.md](scripts/TRACE-FORMAT.md). Trace every sentence;
   facts may cite only `profile.md`, `company.md`, `motivation.md`, or
   `search.md`.
10. **Run the deterministic checks before showing any draft.** Resolve
    `scripts/check.py` relative to this skill and run
    `python scripts/check.py phrases letter.txt --document-type
    letter --language <en|de-ch>` and `python scripts/check.py trace letter.txt
    --document-type letter --trace letter-trace.md --profile
    ~/job-search/profile.md --company company.md --motivation motivation.md
    --search ~/job-search/search.md`. Fix every blocking finding before showing
    any letter content; rewrite the document and trace together and repeat both
    commands until both exit 0.
11. **Launch the independent checker** as a fresh-context subagent, following
    [Independent checker](#independent-checker). Present its findings; the user,
    not the writer or checker, chooses between the two resolutions.
12. **Iterate** in `letter.md`. Regenerate `letter.txt` and `letter-trace.md`
    and rerun the complete pipeline in steps 10–11 after every change before
    showing the revision. Apply only changes the user accepted. **Generate no
    PDF while iterating.**
13. **On approval**, produce `letter.pdf` (`scripts/make-pdf.ps1`), `email.md`
    (subject plus 3–4 sentences), and the dossier checklist: CV variant,
    Arbeitszeugnisse, diplomas. Regenerate the plain text and trace and rerun
    the complete pipeline with the final outputs.

## Check

Prepare or update `letter.txt` and `letter-trace.md`, run both commands in Write
step 10 until they exit 0, then use the same fresh-context subagent in Write
step 11. Inside an application directory, give it `posting.md`, `company.md`,
`fit.md`, and the CV being submitted if it exists. With no posting, say that fit
cannot be assessed and never present the review as complete.

Report findings, let the user choose which to accept, apply **only those**. Copy
`letter.md` to `letter.prev.md` first, then regenerate every output so they
never diverge from the source, and rerun the complete pipeline.

## Independent checker

Use Claude Code's Task / subagent tool to launch a fresh-context subagent. Do
not pass it the drafting conversation or the writer's reasoning. Give it this
instruction, substituting the paths for the current installation and
application and the style selected for the posting's language:

> Review this finished letter independently. Read only these files:
> - this skill's `CHECKER.md` and selected `STYLE-EN.md` or `STYLE-DE-CH.md`
> - the sibling `cv-writer/VOICE.md`
> - `~/job-search/profile.md` and `~/job-search/search.md`
> - this application's `company.md`, `motivation.md`, `posting.md`, and `fit.md`
> - this application's CV being submitted, if one exists
> - this application's finished `letter.txt` and `letter-trace.md`
>
> Do not read any other file or use prior conversation. In particular, never
> read `profile-history.md`, archive letters, the drafting conversation, or the
> writer's reasoning. Apply every rule in `CHECKER.md` and the supplied voice
> and style files. For every fact in the trace, compare the letter unit directly
> with its cited excerpt and flag any unsupported escalation of scope, role,
> magnitude, or ownership; the presence of a real excerpt is not enough. Check
> consistency with the CV only when it was included. Return findings only, in
> `CHECKER.md`'s output format. Treat each finding as a discrepancy rather than
> a verdict and give both resolutions: the letter is wrong and must be
> corrected, or the claim is true and `profile.md` under-records it. Do not edit
> any file and do not choose a resolution for the user.

If the environment has no Task / subagent tool, say so to the user, run these
same checker instructions in the current session with exactly the same file
limits, and state explicitly that the fallback check is not independent.

## Hard rules

- **Verifiable claims** — numbers, employers, technologies, durations,
  outcomes, company facts and practical limits — come only from `profile.md`,
  `search.md` and `company.md`. Motivation comes from `motivation.md`; framing
  is free. Never read `profile-history.md`. The test: *if an interviewer asks
  about this sentence, is there a source that supports it?*
- **Never invent** a company fact, an address, a contact name, or a figure.
  Ask instead.
- **Swiss German has no `ß`** — `Grüsse`, `Strasse`, `gemäss`. One `ß` marks the
  letter as written from a German template.
- **Never exceed the word budget.** One page is not negotiable on this market.
- **Never show unchecked output.** `letter.txt` and `letter-trace.md` are
  regenerated together, and both the phrase and letter trace checks pass
  before the first draft and every revision is shown.
- `~/job-search/` holds personal data. It is never transmitted anywhere and
  never goes under version control.
