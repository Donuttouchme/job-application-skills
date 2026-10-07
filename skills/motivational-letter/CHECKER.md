# Checker

Four dimensions. Every finding quotes the letter, names the problem, carries a
severity, and proposes a rewrite. Used both by check mode and by write step 9
(self-check before showing a draft).

## Severity

| Level | Meaning |
|---|---|
| 🔴 **blocking** | do not send |
| 🟡 **weakening** | send-able, but the letter is worse for it |
| ⚪ **cosmetic** | rhythm, repetition, polish |

Blocking, exhaustively: a claim with no source; a misread requirement; a `ß` in
a Swiss letter; a missing `Gehaltsvorstellung` or `Eintrittstermin` the posting
asked for; a missing recipient block in a DE-CH letter; over the word budget.

## 1. Fit to the posting

Needs `posting.md`. Without it, say the dimension cannot be assessed and run the
other three — **never present a partial review as complete**.

- Every must-have from `fit.md` marked *lead argument*: is it actually in the
  letter?
- Anything the letter argues that the posting never asked for — dead weight
- Requirements answered with the wrong evidence (adjacent technology presented
  as the requested one) → 🔴, this is a misread, not a stretch
- DE-CH: posting asks for salary or start date and the letter is silent → 🔴

## 2. Language and style

- Grammar, typos, agreement
- Sentences over ~25 words, stacked subordinate clauses, passive where an actor
  exists
- Nominal style — `zur Durchführung der Optimierung` instead of a verb
- **Sentence complexity above the user's CEFR level in `profile.md`** → 🟡. A
  letter that outruns its writer produces an interview that contradicts it.
- DE-CH: any `ß` → 🔴. Also check `Strasse`, `Grüsse`, `gemäss`, and `CHF` with
  an apostrophe thousands separator (`CHF 95'000`).

## 3. Cliché and AI tells

Load the banned list from the active style file, and check every rule in
`..\cv-writer\VOICE.md` (staging, sentence openings, paragraph shape, the
read-aloud test). Beyond that, the structural tells:

- tricolons — "planned, built, and delivered" three times in one letter
- "not only … but also" / "nicht nur … sondern auch"
- em-dash pile-ups; "It's not just X, it's Y"
- an opening that describes the act of applying rather than saying something
- a closing sentence that could be pasted into any other letter
- uniform paragraph lengths — real writing is uneven

If the archive letters were AI-assisted, they are the calibration set: if this
dimension finds nothing in them, it is too lenient.

### Authenticity

- No sentence carries the user's own reason (traceable to `motivation.md`) → 🔴
- A sentence paraphrasing the posting or the company's news back to the reader → 🟡
- A paragraph that restates CV bullets in prose → 🟡
- Any phrase from the register's *Amtsdeutsch* list, or a sentence the user
  would not say on the phone → 🟡

## 4. Concreteness and evidence

The operative test, applied sentence by sentence:

> *If an interviewer asks about this sentence, is there a source that supports
> it?*

- Verifiable claim — number, employer, technology, duration, outcome, company
  fact — not traceable to `profile.md` or `company.md` → 🔴
- Adjective with no evidence behind it ("umfassende Erfahrung") → 🟡
- **Inference** from profile evidence ("Kubernetes → comfortable with
  containerised deployments") → 🟡, always flagged so the user decides. Allowed,
  never silent.
- Motivation, interest, and framing need no source. Do not flag them.

### A finding is a discrepancy, not a verdict

An unsourced claim has **two** possible resolutions, and the wrong one is easy
to reach for:

1. **the claim is inflated** — soften it or remove it
2. **the claim is true and `profile.md` under-records it** — correct the profile

The second is common, because a profile built from CV bullets inherits their
silences: nobody lists their own daily toolchain as an achievement. Offer both,
never auto-remove, and never phrase a finding as an accusation. Where the user
confirms the second, hand it to `job-profile` in extend mode.

### Cross-document consistency

A claim can be sourced and still be wrong, because it contradicts something
already sent. Check the letter against the CV variant being submitted and
against `archive\letters\`:

- the letter names a technology the CV names differently (`C++` where every CV
  says `C#`) → 🔴
- a count differs between letter and CV ("fünf parallele Projekte" where the
  CV lists three) → 🔴
- a self-assessment differs from an earlier letter — language level, years of
  experience → 🟡, and say which letters differ and on what dates. Improvement
  over time is legitimate; the user decides. Never silently "correct" it.

## Output

```markdown
## <n> findings — <x> blocking, <y> weakening, <z> cosmetic

### 🔴 Unsupported claim
> "in einem Team von über 30 Entwicklern"
Not in profile.md, which records teams of 6–8. An interviewer will ask.
**Suggested:** "in einem Team von acht Entwicklern"
```

Then let the user pick. Apply **only** what was accepted. Copy `letter.md` to
`letter.prev.md` before overwriting, and regenerate `letter.pdf`, `letter.txt`
and `email.md` so nothing diverges from the source.
