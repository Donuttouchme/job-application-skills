"""Shared checks for finished plain-text CVs and letters (standard library only).

  python check.py phrases <document.txt> --document-type cv|letter --language en|de-ch

This command checks literal banned phrases and Swiss orthography only, not traces.
Phrase matches ignore case and whitespace; line references mark the match's start.
Exit codes: 0 clean, 1 blocking findings, 2 input or installation error.
"""
import argparse
import re
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    phrases = commands.add_parser("phrases", help="check banned phrases and Swiss orthography")
    phrases.add_argument("document", type=Path, help="finished UTF-8 plain-text document")
    phrases.add_argument("--document-type", choices=("cv", "letter"), required=True)
    phrases.add_argument("--language", choices=("en", "de-ch"), required=True)
    args = parser.parse_args()

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


if __name__ == "__main__":
    raise SystemExit(main())
