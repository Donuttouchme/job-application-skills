# Fit Analysis

Turns a posting into an approved argument before a single sentence is drafted.
Output goes to `fit.md` in the application directory.

`cv-writer` and `motivational-letter` share this file. Whichever runs first
writes `fit.md`; the second reuses it only when both the posting and the Profile
(`profile.md`) predate it. If either has changed since the analysis, redo it.
That is what keeps the CV and the letter telling one story.

## 1. Decompose the posting

Three buckets. Quote the posting rather than paraphrasing it — paraphrase is
where requirements quietly soften.

- **Must-have** — stated as required, or repeated across sections
- **Nice-to-have** — "von Vorteil", "a plus", "ideally"
- **Unstated signals** — what the tone and vocabulary reveal about the team.
  "Hands-on in einem kleinen Team" and "etablierte Prozesse" want opposite
  letters. These never appear as bullet points and are usually what decides
  which story lands.

## 2. Classify the evidence

Read `profile.md`. For each requirement, exactly one class:

| Class | Condition |
|---|---|
| **strong** | a named story or position demonstrates it directly, with an outcome |
| **transferable** | proven work in another domain that served the same purpose the requirement asks for |
| **weak** | related but distant (not transferable) — different technology, smaller scale, older than ~4 years, a completed personal project, **or a skill with no story behind it** |
| **missing** | nothing in the profile |

Classify transferable evidence per posting requirement, recording the original
domain and the shared purpose. It keeps the Command level of the original work;
it never implies depth in the new tool. Command is independent of evidence class.

In-progress items (planned certifications, certifications under way, unfinished
projects) are never evidence.

The listed-skill-without-a-story case is the one that goes wrong. A skill in a
list is not evidence — it is a claim. Classify it **weak**.

## 3. Propose an action

Every row carries one:

- **lead argument** — a body paragraph is built on it
- **mention in passing** — one clause, no paragraph
- **stay silent** — true but irrelevant here, or too weak to survive follow-up
- **acknowledge and defuse** — name the gap and say what compensates. Use
  sparingly; two of these in one letter reads as apology.

## 4. `fit.md` format

For each transferable row, label the **original domain** and **shared purpose**
in Evidence from profile, and record the original work's Command level there.

```markdown
# Fit — <Company>, <Role>

Posting: <url or "pasted">   Analysed: <date>

## Must-have
| Requirement (quoted) | Evidence from profile | Class | Action |
|---|---|---|---|
| "3+ Jahre Erfahrung mit Java" | Backend rewrite at X, 4 yrs, cut p95 latency 40% | strong | lead argument |
| "Erfahrung mit CI/CD" | Release gates reduced failed releases; original domain: automotive; shared purpose: controlled releases; Command: discuss | transferable | mention in passing |
| "Kenntnisse in Kubernetes" | listed as a skill, no story | weak | mention in passing |
| "Stipendium…" | — | missing | acknowledge and defuse |

## Nice-to-have
…same table…

## Unstated signals
- "kleines, agiles Team" → wants autonomy evidence, not process evidence

## Verdict
<one paragraph: what this letter argues, in plain words>

## Recommended CV variant
<filename from cv\, and why>
```

## 5. Before drafting

Present `fit.md` and get approval. The user is approving **concrete sentences
that will exist**, not a table — so the Action column has to be readable as a
plan.

If **every must-have is weak or missing**, say so plainly before writing.
Applying anyway is a legitimate choice; making it unknowingly is not.

## Gaps

When a must-have has no evidence, **invent nothing**. Record it as missing and
ask whether to acknowledge it or stay silent. If the user supplies a story on
the spot, hand it to the `job-profile` skill in **extend** mode so it lands in
`profile.md` in the right shape — that is how the profile grows into the shape
of the jobs actually being applied for. An outcome the user did not give stays
`[NEEDED]`; never round a partial answer up into a claim.
