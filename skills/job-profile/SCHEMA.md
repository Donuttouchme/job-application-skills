# Profile Schema

The format of `~/job-search/profile.md`. `cv-writer` and
`motivational-letter` read this structure, so section headings are a contract —
rename one and the readers stop finding it.

## The `[NEEDED]` convention

Anything not yet answered is written as **`[NEEDED]`** with a short note saying
what would fill it and why it matters.

`[NEEDED]` is not a placeholder to be tidied away — it is the mechanism that
keeps unknowns visible. A reader skill must treat a `[NEEDED]` field as absent
and refuse to use it, never as an invitation to guess.

Fill one only with an answer from the user.

## Sections, in order

### Identity and contact

Table: name, email, phone, city, **street address**, plus optional GitHub,
LinkedIn, website. The street address exists for the letterhead; a Swiss
Anschreiben is malformed without it.

### Work eligibility

Citizenship, permit type, notice period, earliest start date, relocation or
commute radius. On the Swiss market a B permit stated plainly ("no sponsorship
required") removes a real objection, so it belongs here.

### Salary expectation

Annual gross in **CHF**, a figure or a range. Required whenever a posting asks
for `Gehaltsvorstellung` / `Lohnvorstellung`; without it those letters are
blocked.

### Languages

Table of language and CEFR level, with the evidence where one exists (a passed
exam and its date). Readers cap letter complexity at these levels, so an
optimistic entry here produces a letter the user cannot defend at interview.

### Career narrative

What the user does now, what is wanted next, and **why they are moving**. The
"why" recurs in every letter, so it is written once here rather than improvised
each time.

### Positions

Newest first, grouped by employer:

```markdown
### <Employer>

**<Title>** — <start> – <end>
- **[core]** the responsibility that defines what the role actually was
- **[core]** another one the role cannot be understood without
- additional detail
```

Facts only. Achievements with outcomes belong in Stories.

### `[core]` — load-bearing responsibilities

`cv-writer` must carry **every** `[core]` bullet into every CV, and may select
among the rest according to the posting.

A bullet is `[core]` when **its absence would give a different picture of the
role**, not merely a less complete one. If a coordination-and-compliance job
reads as a pure engineering job once a bullet is gone, that bullet is `[core]`.

Two or three per position is usually right. Marking everything `[core]` defeats
the purpose — every CV then carries every position in full and cannot be focused.

The judgement is made **here, once, by the user** — deliberately not during CV
generation, where a model is simultaneously trying to fit one page and will
quietly resolve the tension in favour of length.

### Education

Degree, institution, years. Thesis topic where it is still relevant evidence.

### Stories

The highest-value section. Five to eight, each in this shape:

```markdown
### <n>. <short name>
<What the situation was and what the user did — two or three sentences.>
**Outcome:** <the measurable or concretely observable result>
**Evidences:** <which skills or requirements this can be used to support>
```

An unfinished story keeps **`Outcome: [NEEDED]`** and a note on what to probe
for. Readers classify a story without an outcome as *weak*, never *strong*, so
an unfinished story silently weakens every letter that uses it.

### Skills → evidence

A table mapping each claimed skill to the story or position that proves it, with
a class:

Two independent axes. Conflating them is the mistake this schema exists to
prevent.

**Evidence — how much proof exists:**

| Class | Condition |
|---|---|
| **strong** | a named story or position demonstrates it, with an outcome |
| **weak** | related but distant — different technology, smaller scale, older than ~4 years, **or a skill with no story behind it** |
| **missing** | claimed nowhere |

**Command — what could be defended in an interview:**

| Level | Meaning |
|---|---|
| **defend** | could whiteboard it, explain the trade-offs, debug it live |
| **discuss** | has used it and understands what it does, but would need to look things up |
| **exposure** | has touched it; would not claim it |

The axes move independently, and a skill can be **strong / discuss** — a
technology genuinely used in a shipped project that is still being learned. That
combination is extremely common for anyone mid-transition, and having no way to
record it forces a false choice between overclaiming and deleting real work.

**The mechanical consequence:** a `discuss` skill may be listed on a CV, but a
letter must not build a **lead argument** on it, and neither document may imply
depth. Nothing is hidden; the claim is simply sized to what an interview would
bear.

`motivational-letter` applies these same three classes when scoring a posting's
requirements. The definitions are deliberately repeated in both skills; keep
them identical if either changes.

Classing a personal project as `weak` is not pessimism. It is real work, and a
letter may lead with it — it just must not be presented as professional track
record.

### Dossier documents

What is in `documents\`, what each item is, and what it proves. Feeds the
submission checklist: which Arbeitszeugnisse, which diplomas, which permit.

### Voice profile

**Observations, not raw text.** Typical sentence length, register, how the user
hedges, characteristic constructions, whether humour appears, how directly
claims get made. Note which samples the observations came from.

Never derived from `archive\letters\`.

### Do not mention

Employers, technologies, or claims that must never appear. Readers treat this as
absolute.

## Appending during use

When another skill hits a gap mid-task and the user answers on the spot, the
answer is appended here in the section it belongs to, in the format above. This
is how the profile grows into the shape of the jobs actually applied for,
instead of the shape an upfront questionnaire imagined.

Two rules for an append: it never overwrites an existing entry without
confirmation, and a partial answer stays partial — an outcome that was not given
remains `[NEEDED]` rather than being rounded up into a claim.
