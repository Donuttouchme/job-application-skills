# Tailoring

Tailoring changes **what is emphasised**, never what is true. The rules below
make that mechanical rather than a judgement call made under page pressure.

## What may change, by section

| Section | May change | Must not change |
|---|---|---|
| Role line under the name | nothing until the owner changes it | fixed to `Software Engineer`; no tailoring to the posting |
| Profile / Kurzprofil | rewritten per position; chooses which career thread leads | new facts; anything absent from `profile.md`; implying professional use of a `weak` skill |
| Technical Skills | order of rows, order within a row | adding a skill not in the profile; listing one whose evidence is not visible in this CV |
| Professional Experience | bullet **wording** and order; selection among non-`[core]` bullets | dropping a **`[core]`** bullet; dates, titles, employers; what happened |
| Projects | which 2–3 appear, and their order | describing a personal project so it reads as professional work |
| Education | order only | anything |
| Interests | optional one-line section; order of confirmed items | adding an interest the owner has not confirmed may appear on the CV |
| Languages | nothing | must match the profile's CEFR values exactly |

Positions and projects are treated differently on purpose. Positions describe
the professional record, so the `[core]` bullets — the ones without which the
role reads as a different job — always travel. Projects are a portfolio, where
selection is normal and everyone does it.

## Document language

Write everything in the document's language except proper names, product names
and official titles. Translate Profile wording, including explanatory notes
such as a company's former-name parenthetical; the company names inside the
note remain proper names. Translation changes language, never meaning.

## Content density

Use the one A4 page to make the relevant evidence and the person behind it
clear. Do not optimise for the fewest possible words: keep connected Profile
prose, useful context, and a short recorded consequence in a bullet when they
fit. If the shared content does not fit every design, apply the skill's *When it
will not fit one page* rules in their stated order.

## The six rules

**1. Emphasis and vocabulary may change; scope and role may not.**

These generalised pairs come from real corrections. Inflation consistently
runs toward ownership, so that is the first direction to check.

| Bad | Good |
|---|---|
| "Designed a security function" when there was no hands-on work on it | Omit it. |
| `"Led the migration to <tool>"` when among the first in the team to switch | `"Among the first in the team to switch to <tool>"`, only where it earns its space. |
| "Programs" for what were projects — scope inflation outside automotive | "Projects". |
| "Resolved complex production defects" | "Fixed defects from ordinary tickets raised by the internal test team, including on already-released software". |
| "Built internal automation tools to streamline workflows" | Small scripts that saved one person about an hour a week, no longer in use; not a tooling-impact claim. At most, evidence that the language was used professionally. |

**2. Mirror the posting's vocabulary only between genuine synonyms.** If the
posting says `CI/CD pipelines` and the work was release scripting, do not
relabel it. Matching vocabulary is smart between synonyms and dishonest between
a thing and its promotion.

**3. The qualifier is structural, not inline.** Writing
`Java 21 (personal projects) · Spring Boot (personal projects)` is defensive and
makes a worse CV. Instead: **every listed skill must have visible evidence
somewhere in the CV.** Where that evidence is a personal project, the Projects
section already says so. The Profile paragraph carries the matching obligation:
it may not imply professional use of a skill the profile classes `weak`.

**4. Understatement is a defect too, a lesser one.** Told never to overstate,
the safe direction is to hedge — and a hedged CV is a weak CV. Where the profile
records ownership (`owned`, `responsible for`, `led`) and the CV says
`supported`, `assisted with`, `was involved in`, `contributed to`, `helped to`,
that is 🟡: visible, never blocking. The asymmetry is deliberate. Overstating
misleads the employer and collapses at interview; understating only costs the
user, who may have chosen it.

**5. The role line is fixed to `Software Engineer` until the owner changes it.**
The line under the name is positioning, not a title claim; do not tailor it
to the posting. The no-seniority-inflation rule still applies: `Senior` /
`Lead` / `Principal` / `Head of` unsupported by the profile promotes the role.
A domain whose evidence is not visible in this CV is likewise unsupported.

**6. The interviewer test.** *Can this line be asked about, and answered with a
source?* Identical to the letter's rule, deliberately.

## In-progress items

A planned certification or unfinished project is never evidence. It may appear
only with its date and status, for example `exam planned January 2027`. Never
write `certified` before the result, or `completed` before completion is
verified. A project may appear only once it is public and labelled as personal.

## Where the profile is the thing to fix

A profile assembled from CV bullets inherits their silences: nobody lists their
own daily toolchain as an achievement. So a skill can look unevidenced while
being three years of solid experience.

When tailoring hits a skill that seems unsupported, the question to ask the user
is *"is this under-recorded in the profile?"* — not *"should we remove it?"*.
Where the answer is yes, hand it to `job-profile` in extend mode.
