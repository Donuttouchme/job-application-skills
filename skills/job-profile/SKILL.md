---
name: job-profile
description: Build and maintain the Profile at "~/job-search/profile.md", Profile history at "~/job-search/profile-history.md", and Search constraints at "~/job-search/search.md". Seeds from existing CVs, interviews for measurable outcomes and for the user's own writing voice, and fills targeted gaps on request. Use when these files are missing or incomplete, when another job-application skill needs a fact that is not on file, or when the user wants to record or update their background, achievements, salary expectation, availability, language levels, or practical job-search limits.
---

# Job Profile

Owns the Profile, Profile history and Search constraints under
`~/job-search/`. The Profile holds current truth, the history records what it
replaced, and Search constraints hold practical limits.

`cv-writer` reads only the Profile. `motivational-letter` reads the Profile and
Search constraints. Neither reads Profile history or runs its own interview —
they invoke this skill instead.

## Paths

| What | Where |
|---|---|
| Profile — current truth | `~/job-search/profile.md` |
| Profile history — never read by writers | `~/job-search/profile-history.md` |
| Search constraints | `~/job-search/search.md` |
| CV variants to seed from | `~/job-search/cv/` (prefer `.html` — readable as text) |
| Certificates, diplomas | `~/job-search/documents/` |
| Previous letters | `~/job-search/archive/letters/` — **never** a voice source |

## Modes

**Bootstrap** — one of the three files is missing, or the Profile has not
reached the ready gate. Seed from the CVs, then interview to the gate. See
[INTERVIEW.md](INTERVIEW.md).

**Extend** — another skill hit a gap, or a `[NEEDED]` marker needs filling. Ask
only about that, update the right file, stop. This is the common case and it
should take two minutes, not twenty.

**Review** — the user wants to update. Show the current Profile and Search
constraints, ask what changed, and do not re-ask what is already answered.
Consult Profile history only when the user asks about an earlier correction.

On entering any mode, compare the modification time of `profile.md`,
`profile-history.md` and `search.md` against `cv\`. If a CV is newer than any
of them, say which of the three files is older, name the CV, and offer to
reconcile from it. A stale source file is the one failure mode nothing
downstream can detect: every reader trusts its allowed sources completely.

## The ready gate

A profile is ready when all of these exist and none is marked `[NEEDED]`:

- [ ] name, email, phone, **street address** and city
- [ ] work eligibility and earliest start date
- [ ] salary expectation, annual gross in **CHF**
- [ ] language levels in CEFR
- [ ] career narrative: what is wanted now, and why moving
- [ ] positions with dates
- [ ] **at least two stories with a measurable outcome**
- [ ] voice profile, based on observations from at least one genuine sample

Below the gate, say which items are missing and that letters are blocked until
they exist. Do not let a caller proceed on a profile that is not ready — a
letter written from an empty profile is generic filler, which is worse than no
letter.

Missing hand-written English or German samples remain `[NEEDED]` warnings.
They never block the gate when the voice profile already has observations from
another genuine sample.

## Bootstrap

1. **Seed from the CVs.** List `cv\`, ask which variant is current, read it.
   Extract contact details, positions, dates, education, skills and languages.
   Present what was extracted and let the user correct it. Never guess which CV
   is current when several exist.

   **If PDFs cannot be read in this environment**, see [INTERVIEW.md](INTERVIEW.md)
   for what to do instead. Never infer a CV's contents from its filename.
2. **Interview only for what a CV cannot hold** — measurable outcomes, the why,
   salary, practical constraints, voice. Follow
   [INTERVIEW.md](INTERVIEW.md), block by block.
3. **Write after every block**, not at the end. An interrupted session must
   lose at most one block.
4. **Inventory `documents\`** — Arbeitszeugnisse, Empfehlungsschreiben,
   diplomas, permits. Ask what anything unrecognised is. This feeds the dossier
   checklist.
5. **Stop at the gate.** Do not keep going for completeness. The Profile and
   Search constraints grow through use, and an interview that is not finished
   is worth nothing.

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
- **Correct in place only with explicit confirmation.** In the same step,
  replace the old text and write a dated Profile history entry containing the
  replaced text, new text and reason. Every permanent correction also leaves a
  scoped one-line Never-claim rule in the Profile that bans only the replaced
  claim. Never round a partial answer up; keep the missing part `[NEEDED]`.
  Extend mode follows the same rule.
- **Temporary limitations are current facts**, recorded in the relevant
  Profile or Search constraints section, not Never-claim rules.
- **Writers never read Profile history.** Its superseded text must not return
  to an outgoing document.
- Personal data — address, salary, permit status. It stays local, is never
  transmitted, and `~/job-search/` never goes under version control.

## Structure of the file

See [SCHEMA.md](SCHEMA.md) for the three document formats, the `[NEEDED]`
convention, and the evidence classes that `cv-writer` and
`motivational-letter` depend on.
