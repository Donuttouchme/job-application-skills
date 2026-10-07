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
   existing `fit.md` if `cv-writer` already wrote one for this posting. Present
   it and get approval before drafting. All must-haves weak or missing → say so
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
9. **Draft** from the Profile, Search constraints and approved motivation,
   within the word budget and in the user's voice per
   [`..\cv-writer\VOICE.md`](../cv-writer/VOICE.md): the reason from
   `motivation.md`, the evidence from `fit.md`.
10. **Self-check** against [CHECKER.md](CHECKER.md) and fix before showing.
11. **Write `letter.md`** immediately so it can be edited in an editor, then
    iterate. **Generate no PDF while iterating.**
12. **On approval**, produce `letter.pdf` (`scripts/make-pdf.ps1`),
    `letter.txt` (no letterhead, for ATS fields), `email.md` (subject plus 3–4
    sentences), and the dossier checklist: CV variant, Arbeitszeugnisse,
    diplomas.

## Check

Follow [CHECKER.md](CHECKER.md). Inside an application directory, pick up
`posting.md`, `company.md`, `fit.md`, and the CV variant automatically. With no
posting, say that fit cannot be assessed and run the other three dimensions —
never present a partial review as complete.

Report findings, let the user choose which to accept, apply **only those**. Copy
`letter.md` to `letter.prev.md` first, then regenerate every output so they
never diverge from the source.

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
- `~/job-search/` holds personal data. It is never transmitted anywhere and
  never goes under version control.
