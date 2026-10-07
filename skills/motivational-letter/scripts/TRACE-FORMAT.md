# Trace format

`check.py trace` reads a line-based Markdown file. For CVs, make one entry for
each non-empty line text in `cv.txt`. For letters, make one entry for each
sentence in the body of `letter.txt`; a paragraph without sentence-ending
punctuation, such as a salutation or closing, is one unit. Preserve the unit
text exactly. Letter sentences are not split at `z. B.`, `z. H.`, `d. h.`,
`u. a.`, `ca.`, `Dr.`, `Nr.`, `e.g.`, `i.e.`, or `etc.`.
The optional document heading is `# Trace`. Each value is a JSON string on one
line; JSON quoting makes punctuation, quotes and leading spaces unambiguous and
is parsed with the Python standard library.

```markdown
# Trace

## Entry
- Unit: "Skills"
- Category: "heading"

## Entry
- Unit: "Built a release tool for one team."
- Category: "fact"
- Source: "profile.md"
- Excerpt: "Built a release tool for one team."
- Source: "profile.md"
- Excerpt: "Outcome: reduced manual release work."

## Entry
- Unit: "candidate@example.test"
- Category: "contact"
```

Fields are case-sensitive and have this order:

1. `## Entry`
2. one `- Unit: <JSON string>` containing the exact CV line or letter unit
3. one `- Category: <JSON string>`: `fact`, `heading`, or `contact`; letters
   also allow `salutation`, `motivation`, and `closing`
4. for a fact, one or more adjacent `Source` / `Excerpt` pairs

`Source` is a logical source name, not a path. For a CV the only allowed name
is `profile.md`. A letter allows `profile.md`, `company.md`, `motivation.md`,
and `search.md`; `profile-history.md` is never allowed. The corresponding CLI
option supplies each source's path. A cited source that cannot be read is an
input error. An excerpt is copied verbatim from the source, but spaces, tabs,
and line breaks are treated as equivalent when it is matched. The forbidden
`Never claim`, `Voice profile`, and `[NEEDED]` regions apply to `profile.md`.
Non-fact entries do not need excerpts.

Run both checks whenever the CV is generated or regenerated:

```text
python check.py phrases cv.txt --document-type cv --language en
python check.py trace cv.txt --document-type cv --trace cv-trace.md --profile profile.md
```

For a letter, pass all four permitted source paths so any source named by its
trace can be checked:

```text
python check.py phrases letter.txt --document-type letter --language en
python check.py trace letter.txt --document-type letter --trace letter-trace.md --profile profile.md --company company.md --motivation motivation.md --search search.md
```

Use `--language de-ch` for German Swiss documents. Exit code 0 is clean, 1
means blocking findings, and 2 means an input or installation error. The trace
check verifies that a citation exists in an allowed, non-forbidden source
region. It does not verify that the document unit is an accurate interpretation
of the excerpt.
