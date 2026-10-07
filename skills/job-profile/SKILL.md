---
name: job-profile
description: Build and maintain the shared job-application profile at "~/job-search/profile.md" — the single source of truth for every factual claim that appears in a CV or a cover letter. Seeds from existing CVs, interviews for measurable outcomes and for the user's own writing voice, and fills targeted gaps on request. Use when the profile is missing or incomplete, when another job-application skill needs a fact that is not on file, or when the user wants to record or update their background, achievements, salary expectation, availability, or language levels.
---

# Job Profile

Owns `~/job-search/profile.md`. Every factual claim in a CV or a letter traces
back to this file, so it is the one place worth getting right.

`motivational-letter` and `cv-writer` read it. Neither runs its own interview —
they invoke this skill instead.

## Paths

| What | Where |
|---|---|
| The profile | `~/job-search/profile.md` |
| CV variants to seed from | `~/job-search/cv/` (prefer `.html` — readable as text) |
| Certificates, diplomas | `~/job-search/documents/` |
| Previous letters | `~/job-search/archive/letters/` — **never** a voice source |

## Modes

**Bootstrap** — no `profile.md`, or one that has not reached the ready gate.
Seed from the CVs, then interview to the gate. See [INTERVIEW.md](INTERVIEW.md).

**Extend** — another skill hit a gap, or a `[NEEDED]` marker needs filling. Ask
only about that, append, stop. This is the common case and it should take two
minutes, not twenty.

**Review** — the user wants to update. Show what is on file, ask what changed,
do not re-ask what is already answered.

On entering any mode, compare the profile's modification time against `cv\`. A
CV newer than the profile means facts were changed somewhere else and the
profile has silently fallen behind — say so, name the file, and offer to
re-seed from it. A stale profile is the one failure mode nothing downstream can
detect: every reader trusts it completely.

## The ready gate

A profile is ready when all of these exist and none is marked `[NEEDED]`:

- [ ] name, email, phone, **street address** and city
- [ ] work eligibility and earliest start date
- [ ] salary expectation, annual gross in **CHF**
- [ ] language levels in CEFR
- [ ] career narrative: what is wanted now, and why moving
- [ ] positions with dates
- [ ] **at least two stories with a measurable outcome**
- [ ] voice profile

Below the gate, say which items are missing and that letters are blocked until
they exist. Do not let a caller proceed on a profile that is not ready — a
letter written from an empty profile is generic filler, which is worse than no
letter.

## Bootstrap

1. **Seed from the CVs.** List `cv\`, ask which variant is current, read it.
   Extract contact details, positions, dates, education, skills and languages.
   Present what was extracted and let the user correct it. Never guess which CV
   is current when several exist.

   **If PDFs cannot be read in this environment**, see [INTERVIEW.md](INTERVIEW.md)
   for what to do instead. Never infer a CV's contents from its filename.
2. **Interview only for what a CV cannot hold** — measurable outcomes, the why,
   salary, voice. Follow [INTERVIEW.md](INTERVIEW.md), block by block.
3. **Write after every block**, not at the end. An interrupted session must
   lose at most one block.
4. **Inventory `documents\`** — Arbeitszeugnisse, Empfehlungsschreiben,
   diplomas, permits. Ask what anything unrecognised is. This feeds the dossier
   checklist.
5. **Stop at the gate.** Do not keep going for completeness. The profile grows
   through use, and an interview that is not finished is worth nothing.

## Hard rules

- **Never invent, never infer to fill a blank.** An unanswered question stays
  `[NEEDED]`. A profile that quietly guesses is worse than an empty one,
  because everything downstream trusts it.
- **A story without a measurable outcome is not finished.** Probe as
  [INTERVIEW.md](INTERVIEW.md) describes. If nothing quantifiable exists,
  record a concretely observable outcome and mark it as such — never
  "improved efficiency".
- **The voice profile comes only from text the user actually wrote.**
  `archive\letters\` is excluded: letters there are assumed AI-assisted, and
  using them would teach the skill to imitate its own output.
- **Never overwrite.** Existing content is corrected only with the user's
  confirmation; new material is appended.
- Personal data — address, salary, permit status. It stays local, is never
  transmitted, and `~/job-search/` never goes under version control.

## Structure of the file

See [SCHEMA.md](SCHEMA.md) for the section-by-section format, the `[NEEDED]`
convention, and the evidence classes that `cv-writer` and
`motivational-letter` depend on.
