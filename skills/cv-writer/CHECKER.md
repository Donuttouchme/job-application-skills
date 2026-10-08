# CV Checker

Runs automatically at the end of generation, and can be invoked on demand
against an existing CV.

## Dimensions

| Dimension | Checks | Severity |
|---|---|---|
| Traceability | every line derives from `profile.md` | 🔴 |
| `[core]` completeness | no `[core]` position bullet dropped | 🔴 |
| Escalation | no rephrase raises scope, role or magnitude | 🔴 |
| Evidence visibility | every listed skill, and every domain in the role line, has visible evidence in this CV; the Profile paragraph implies no professional use of a `weak` skill | 🔴 |
| Seniority | no `Senior` / `Lead` / `Principal` / `Head of` the profile does not support | 🔴 |
| In-progress items | date and status required; never evidence; no `certified` before the result or `completed` before verified completion; projects public and labelled personal | 🔴 |
| Consistency | against the letter in the same directory, and against the profile's CEFR levels | 🔴 |
| Format | one A4 page per design (default, klassisch, tabellarisch); single column (the tabellarisch date gutter is a row label, not a column layout); no images except the optional header photo; no tables; real text | 🔴 |
| Understatement | hedging verbs where the profile records ownership | 🟡 |
| Voice | every line passes [VOICE.md](VOICE.md): connected first-person Profile with a sourced hook, concrete objects and stakes, plain verbs, varied rhythm, no unsupported self-praise, uneven bullet shape, nothing from the word lists; everything except proper names, product names and official titles is in the document language; skill-row category labels are bold where the template provides them | 🟡 per line; 🟡 for a skill row missing its provided bold category label; 🟡 when the hook paraphrases the user's recorded self-description more weakly than their own words, recorded stakes are left out, the Profile paragraph names a technology-level gap, or it closes on a gap; 🔴 when the Profile paragraph is an adjective stack or stacks unrelated facts without a hook and connections, every bullet shares one template, or any text that should be translated remains in another language |

## Trace semantics

For every fact in `cv-trace.md`, compare the whole CV unit with the cited
excerpt, not merely the source file. A real, verbatim excerpt does not make an
inflated line accurate. The excerpt must support the unit without escalating
its scope, the user's role, or the magnitude of the work or outcome. In
particular, do not upgrade participation to leadership, contribution to
ownership, individual use to team-wide impact, or a project to a programme.
Report any such mismatch as a discrepancy under the rules below, not as proof
that either the CV or the profile is false.

## A finding is a discrepancy, not a verdict

The checker can tell that the CV and `profile.md` disagree. It cannot tell which
one is wrong, and **must not assume it is the CV**.

Every finding carries both resolutions:

1. **the CV is wrong** — make the evidence visible, or drop the claim
2. **the profile is wrong** — the claim is true and the profile under-records it

The second is common, because a profile assembled from CV bullets inherits their
silences. A typical case: `Terraform` and `Ansible` appear in a skills list with
nothing in the CV body evidencing them, yet they were the daily working
environment of three years of platform work — never written down as
achievements, because nobody lists their own toolchain. Read as
"unsupported claim", the fix would have deleted a true and relevant skill. The
correct fix was to the profile.

**Never phrase a finding as an accusation, and never auto-remove a claim.** Show
the discrepancy, offer both directions, let the user decide. Where the profile is
the thing to correct, hand it to `job-profile` in extend mode.

This is also the answer to "how does the skill know what counts as a lie": it
does not, and it is not asked to. It knows what counts as a *disagreement*, which
is checkable, and the person who did the work adjudicates.

## Output

```markdown
## <n> findings — <x> blocking, <y> weakening

### 🔴 Evidence not visible
> Technical Skills: "Terraform · Ansible"
Neither appears in the positions or projects shown in this CV, and profile.md
records no story for them.
**Either:** add the evidence to a position bullet, or drop the skills.
**Or:** these are genuinely used and the profile under-records them — say so and
they get added properly.
```

Then let the user pick. Apply only what was accepted, and re-render every output
so `cv.html`, `cv-klassisch.html`, `cv-tabellarisch.html`, their three named
PDFs and the shared `cv.txt` never diverge in content. Fact order within each
section stays identical; tabellarisch alone moves skills, interests and
languages to the end. Check every design's one-page fit, and apply any content
reduction to all outputs, never to just the overflowing design.

## Calibration

Any existing CVs in `~/job-search/cv/` written before these rules make a
natural fixture, provided they are readable (HTML or text). Running the checker against them
should produce evidence-visibility findings — and should propose *both*
resolutions for each. Findings that only ever propose deletion mean the rule
above is not implemented.

PDF-only variants are out of scope for calibration when the environment
cannot read PDFs.
