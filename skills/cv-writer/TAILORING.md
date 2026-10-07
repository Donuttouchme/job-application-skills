# Tailoring

Tailoring changes **what is emphasised**, never what is true. The rules below
make that mechanical rather than a judgement call made under page pressure.

## What may change, by section

| Section | May change | Must not change |
|---|---|---|
| Role line under the name | rewritten toward the posting's vocabulary | a seniority marker the profile does not support; a domain with no visible evidence |
| Profile / Kurzprofil | rewritten per position; chooses which career thread leads | new facts; anything absent from `profile.md`; implying professional use of a `weak` skill |
| Technical Skills | order of rows, order within a row | adding a skill not in the profile; listing one whose evidence is not visible in this CV |
| Professional Experience | bullet **wording** and order; selection among non-`[core]` bullets | dropping a **`[core]`** bullet; dates, titles, employers; what happened |
| Projects | which 2–3 appear, and their order | describing a personal project so it reads as professional work |
| Education | order only | anything |
| Languages | nothing | must match the profile's CEFR values exactly |

Positions and projects are treated differently on purpose. Positions describe
the professional record, so the `[core]` bullets — the ones without which the
role reads as a different job — always travel. Projects are a portfolio, where
selection is normal and everyone does it.

## The six rules

**1. Emphasis and vocabulary may change; scope and role may not.**

> "Built internal automation tools in C#"
> → *"Developed C# tooling that removed manual steps from the engineering
> workflow"* — same fact, the posting's language. **Fine.**
> → *"Led the automation strategy"* — promotes the role. **Not fine.**

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

**5. The role line: no seniority inflation, evidence must be visible.** The line
under the name is positioning, not a title claim — `Software Engineer – Backend`
where the held title was `Feature Owner` is normal and read as such by everyone.
What it may not carry: `Senior` / `Lead` / `Principal` / `Head of` unsupported
by the profile, or a domain whose evidence is not visible in this CV.

**6. The interviewer test.** *Can this line be asked about, and answered with a
source?* Identical to the letter's rule, deliberately.

## Where the profile is the thing to fix

A profile assembled from CV bullets inherits their silences: nobody lists their
own daily toolchain as an achievement. So a skill can look unevidenced while
being three years of solid experience.

When tailoring hits a skill that seems unsupported, the question to ask the user
is *"is this under-recorded in the profile?"* — not *"should we remove it?"*.
Where the answer is yes, hand it to `job-profile` in extend mode.
