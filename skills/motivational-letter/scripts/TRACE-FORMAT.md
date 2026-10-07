# Trace format

`check.py trace` reads a line-based Markdown file. For CVs, make one entry for
each non-empty line text in `cv.txt`, preserving the text exactly.
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
2. one `- Unit: <JSON string>` containing the exact CV line
3. one `- Category: <JSON string>`: `fact`, `heading`, or `contact`
4. for a fact, one or more adjacent `Source` / `Excerpt` pairs

`Source` is a logical source name, not a path. For a CV the only allowed name
is `profile.md`; `--profile` supplies the path from which that source is read.
An excerpt is copied verbatim from the source, but spaces, tabs, and line breaks
are treated as equivalent when it is matched. `heading` and `contact` entries
do not need excerpts.

Run both checks whenever the CV is generated or regenerated:

```text
python check.py phrases cv.txt --document-type cv --language en
python check.py trace cv.txt --document-type cv --trace cv-trace.md --profile profile.md
```

Use `--language de-ch` for a German Swiss CV. Exit code 0 is clean, 1 means
blocking findings, and 2 means an input or installation error. The trace check
verifies that a citation exists in an allowed, non-forbidden source region. It
does not verify that the CV line is an accurate interpretation of the excerpt.
