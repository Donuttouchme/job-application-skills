"""Shared checks for finished plain-text CVs and letters (standard library only).

  python check.py phrases <document.txt> --document-type cv|letter --language en|de-ch
  python check.py trace <document.txt> --document-type cv --trace <trace.md> --profile <profile.md>

Exit codes: 0 clean, 1 blocking findings, 2 input or installation error.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def check_phrases(args):
    list_path = Path(__file__).resolve().parent / "banned-phrases.txt"
    try:
        banned = list_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        print(f"error: cannot read banned phrase list {list_path}: {exc}", file=sys.stderr)
        return 2
    try:
        document = args.document.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"error: cannot read document {args.document}: {exc}", file=sys.stderr)
        return 2
    findings = []
    folded_document = document.casefold()
    for phrase in banned:
        phrase = phrase.strip()
        if not phrase:
            continue
        pattern = r"\s+".join(re.escape(word) for word in phrase.casefold().split())
        for match in re.finditer(pattern, folded_document):
            number = folded_document.count("\n", 0, match.start()) + 1
            findings.append((number, phrase))
    orthography = []
    for number, line in enumerate(document.splitlines(), 1):
        if args.language == "de-ch" and "ß" in line.lower():
            orthography.append(f'  line {number}: "ß" is forbidden in de-ch')
    if findings:
        print("Banned phrases:")
        for number, phrase in sorted(findings):
            print(f'  line {number}: "{phrase}"')
    if orthography:
        print("Swiss orthography:")
        print("\n".join(orthography))
    if findings or orthography:
        return 1
    print("Clean: no banned phrases or Swiss orthography findings.")
    return 0


def parse_trace(text):
    entries = []
    current = None
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line in {"# Trace", "# CV trace"}:
            continue
        if line == "## Entry":
            if current is not None and "pending_source" in current:
                raise ValueError(
                    f"line {current['pending_source_line']}: Source needs a following Excerpt"
                )
            current = {"line": number, "citations": []}
            entries.append(current)
            continue
        if current is None:
            raise ValueError(f"line {number}: expected '## Entry'")
        match = re.fullmatch(r"- (Unit|Category|Source|Excerpt): (.+)", line)
        if not match:
            raise ValueError(f"line {number}: invalid trace field")
        field, encoded = match.groups()
        try:
            value = json.loads(encoded)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {number}: invalid JSON string: {exc.msg}") from exc
        if not isinstance(value, str):
            raise ValueError(f"line {number}: trace values must be JSON strings")
        key = field.casefold()
        if key in {"unit", "category"}:
            if key in current:
                raise ValueError(f"line {number}: duplicate {field} field")
            if "pending_source" in current:
                raise ValueError(
                    f"line {current['pending_source_line']}: Source needs a following Excerpt"
                )
            current[key] = value
            current[f"{key}_line"] = number
        elif key == "source":
            if "pending_source" in current:
                raise ValueError(
                    f"line {current['pending_source_line']}: Source needs a following Excerpt"
                )
            current["pending_source"] = value
            current["pending_source_line"] = number
        else:
            if "pending_source" not in current:
                raise ValueError(f"line {number}: Excerpt needs a preceding Source")
            current["citations"].append({
                "source": current.pop("pending_source"),
                "source_line": current.pop("pending_source_line"),
                "excerpt": value,
                "excerpt_line": number,
            })
    if current is not None and "pending_source" in current:
        raise ValueError(
            f"line {current['pending_source_line']}: Source needs a following Excerpt"
        )
    return entries


def normalise_whitespace(text):
    return " ".join(text.split())


def normalised_text_with_offsets(text):
    """Return whitespace-normalised text and each output character's source offset."""
    output = []
    offsets = []
    pending_space = None
    for offset, character in enumerate(text):
        if character.isspace():
            if output and pending_space is None:
                pending_space = offset
            continue
        if pending_space is not None:
            output.append(" ")
            offsets.append(pending_space)
            pending_space = None
        output.append(character)
        offsets.append(offset)
    return "".join(output), offsets


def forbidden_profile_ranges(profile):
    ranges = {"voice": [], "never": [], "needed": []}
    active = None
    active_level = None
    offset = 0
    for line_with_ending in profile.splitlines(keepends=True):
        line = line_with_ending.rstrip("\r\n")
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading:
            level = len(heading.group(1))
            if active is not None and level <= active_level:
                active = None
                active_level = None
            name = heading.group(2).strip().casefold()
            if name == "voice profile":
                active, active_level = "voice", level
            elif name == "never claim":
                active, active_level = "never", level
        line_range = (offset, offset + len(line_with_ending))
        if active is not None:
            ranges[active].append(line_range)
        if "[NEEDED]" in line:
            ranges["needed"].append(line_range)
        offset += len(line_with_ending)
    return ranges


def range_overlaps(start, end, ranges):
    return any(start < range_end and end > range_start for range_start, range_end in ranges)


def citation_profile_status(excerpt, profile, ranges):
    """Return missing, allowed, or forbidden region names for a profile excerpt."""
    needle = normalise_whitespace(excerpt)
    normalised, offsets = normalised_text_with_offsets(profile)
    if not needle:
        return "missing", set()
    starts = [match.start() for match in re.finditer(re.escape(needle), normalised)]
    if not starts:
        return "missing", set()
    forbidden = set()
    for start in starts:
        source_start = offsets[start]
        source_end = offsets[start + len(needle) - 1] + 1
        occurrence_regions = {
            name for name, region_ranges in ranges.items()
            if range_overlaps(source_start, source_end, region_ranges)
        }
        if not occurrence_regions:
            return "allowed", set()
        forbidden.update(occurrence_regions)
    return "forbidden", forbidden


def check_trace(args):
    try:
        document = args.document.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"error: cannot read document {args.document}: {exc}", file=sys.stderr)
        return 2
    try:
        trace_text = args.trace.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"error: cannot read trace {args.trace}: {exc}", file=sys.stderr)
        return 2
    try:
        profile = args.profile.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"error: cannot read source profile.md at {args.profile}: {exc}", file=sys.stderr)
        return 2
    try:
        entries = parse_trace(trace_text)
    except ValueError as exc:
        print(f"error: cannot parse trace {args.trace}: {exc}", file=sys.stderr)
        return 2

    for item in entries:
        if "unit" not in item or "category" not in item:
            print(
                f"error: cannot parse trace {args.trace}: entry at line {item['line']} "
                "needs Unit and Category fields",
                file=sys.stderr,
            )
            return 2
        if item["category"] not in {"fact", "heading", "contact"}:
            print(
                f"error: cannot parse trace {args.trace}: entry at line {item['line']} has "
                f"unsupported CV category {item['category']!r}",
                file=sys.stderr,
            )
            return 2

    document_units = [
        (number, line) for number, line in enumerate(document.splitlines(), 1)
        if line.strip()
    ]
    document_unit_text = {line for _, line in document_units}
    traced = {item.get("unit") for item in entries}
    untraced = [item for item in document_units if item[1] not in traced]
    seen_units = set()
    duplicate_entries = []
    for item in entries:
        if item["unit"] in seen_units:
            duplicate_entries.append(item)
        seen_units.add(item["unit"])
    stale_entries = [item for item in entries if item["unit"] not in document_unit_text]
    missing_excerpts = [
        item for item in entries
        if item["category"] == "fact"
        and not any(normalise_whitespace(citation["excerpt"])
                    for citation in item["citations"])
    ]
    excerpts_not_found = []
    forbidden_excerpts = {"voice": [], "never": [], "needed": []}
    history_citations = []
    disallowed_sources = []
    profile_ranges = forbidden_profile_ranges(profile)
    for item in entries:
        for citation in item["citations"]:
            if not normalise_whitespace(citation["excerpt"]):
                continue
            source_basename = citation["source"].replace("\\", "/").rsplit("/", 1)[-1]
            if source_basename.casefold() == "profile-history.md":
                history_citations.append(citation)
                continue
            if citation["source"] != "profile.md":
                disallowed_sources.append(citation)
                continue
            status, regions = citation_profile_status(
                citation["excerpt"], profile, profile_ranges,
            )
            if status == "missing":
                excerpts_not_found.append(citation)
            elif status == "forbidden":
                for region in regions:
                    forbidden_excerpts[region].append(citation)
    if untraced:
        print("Untraced units:")
        for number, unit in untraced:
            print(f"  document line {number}: {json.dumps(unit, ensure_ascii=False)}")
    if missing_excerpts:
        print("Facts with no excerpts:")
        for item in missing_excerpts:
            print(
                f"  trace line {item['unit_line']}: "
                f"{json.dumps(item['unit'], ensure_ascii=False)}"
            )
    if excerpts_not_found:
        print("Excerpts not found:")
        for citation in excerpts_not_found:
            print(
                f"  trace line {citation['excerpt_line']}: "
                f"{json.dumps(citation['excerpt'], ensure_ascii=False)}"
            )
    forbidden_headings = {
        "voice": "Excerpts from Voice profile:",
        "never": "Excerpts from Never claim:",
        "needed": "Excerpts from [NEEDED] lines:",
    }
    for region in ("voice", "never", "needed"):
        if forbidden_excerpts[region]:
            print(forbidden_headings[region])
            for citation in forbidden_excerpts[region]:
                print(
                    f"  trace line {citation['excerpt_line']}: "
                    f"{json.dumps(citation['excerpt'], ensure_ascii=False)}"
                )
    if history_citations:
        print("Profile history citations:")
        for citation in history_citations:
            print(
                f"  trace line {citation['source_line']}: "
                f"{json.dumps(citation['source'], ensure_ascii=False)}"
            )
    if disallowed_sources:
        print(f"Sources not allowed for {args.document_type}:")
        for citation in disallowed_sources:
            print(
                f"  trace line {citation['source_line']}: "
                f"{json.dumps(citation['source'], ensure_ascii=False)}"
            )
    if duplicate_entries:
        print("Duplicate entries:")
        for item in duplicate_entries:
            print(
                f"  trace line {item['unit_line']}: "
                f"{json.dumps(item['unit'], ensure_ascii=False)}"
            )
    if stale_entries:
        print("Stale entries:")
        for item in stale_entries:
            print(
                f"  trace line {item['unit_line']}: "
                f"{json.dumps(item['unit'], ensure_ascii=False)}"
            )
    if (untraced or missing_excerpts or excerpts_not_found
            or any(forbidden_excerpts.values()) or history_citations
            or disallowed_sources or duplicate_entries or stale_entries):
        return 1
    print("Clean: every CV unit has a valid trace citation.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    phrases = commands.add_parser(
        "phrases",
        help="check banned phrases and Swiss orthography",
        description=("Check literal banned phrases and Swiss orthography. Phrase matches "
                     "ignore case and whitespace; line references mark the match's start."),
    )
    phrases.add_argument("document", type=Path, help="finished UTF-8 plain-text document")
    phrases.add_argument("--document-type", choices=("cv", "letter"), required=True)
    phrases.add_argument("--language", choices=("en", "de-ch"), required=True)
    phrases.set_defaults(run=check_phrases)

    trace = commands.add_parser(
        "trace",
        help="check that finished document units have allowed citations",
        description=("Check that citations exist for finished document units. This verifies "
                     "that a citation exists, not that the document line is accurate."),
    )
    trace.add_argument("document", type=Path, help="finished UTF-8 plain-text document")
    trace.add_argument("--document-type", choices=("cv",), required=True)
    trace.add_argument("--trace", type=Path, required=True, help="UTF-8 Markdown trace")
    trace.add_argument("--profile", type=Path, required=True, help="profile.md source file")
    trace.set_defaults(run=check_trace)
    args = parser.parse_args()
    return args.run(args)


if __name__ == "__main__":
    raise SystemExit(main())
