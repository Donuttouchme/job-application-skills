"""Check staged files for personal data without echoing matched values."""

import re
import subprocess
import sys
from pathlib import Path

HOME_PATH = re.compile(
    r"(?:\b[A-Z]:[\\/]Users[\\/]|/home/|/Users/)"
    r"[^\s/\\<>\"'`$%{}()|]+",
    re.IGNORECASE,
)
EMAIL = re.compile(
    r"[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Z0-9](?:[A-Z0-9.-]*[A-Z0-9])?\.[A-Z]{2,}",
    re.IGNORECASE,
)
PHONE = re.compile(r"(?<![\w+])\+[1-9]\d{0,2}(?: *\d){8,}(?!\w)")
PHONE_PLACEHOLDERS = {"+41 79 123 45 67"}
AHV = re.compile(r"(?<!\d)756\.\d{4}\.\d{4}\.\d{2}(?!\d)")
TOKEN = re.compile(
    r"\b(?:ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|"
    r"github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|"
    r"AKIA[A-Z0-9]{16})(?![A-Za-z0-9_])"
)


def blocked_path(filename):
    path = filename.replace("\\", "/").casefold()
    while path.startswith("./"):
        path = path[2:]
    return path.startswith(("docs/personal_data/", ".scratch/"))


def allowed_email(address):
    domain = address.rsplit("@", 1)[1].casefold()
    return (
        domain in {"example.com", "example.org", "example.net"}
        or domain.endswith((".users.noreply.github.com",
                            ".example.com", ".example.org", ".example.net",
                            ".example", ".test", ".invalid"))
    )


def local_patterns():
    """Resolve Git's private info directory, including in linked worktrees."""
    result = subprocess.run(
        ["git", "rev-parse", "--git-path", "info/personal-patterns"],
        check=True, capture_output=True,
    )
    path = Path(result.stdout.decode("utf-8").strip())
    if not path.exists():
        return []
    return [
        re.compile(re.escape(line.strip()), re.IGNORECASE)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def findings(filename, content, patterns=()):
    """Return line numbers and generic reasons; never retain matched values."""
    if blocked_path(filename):
        return [(1, "private directory")]
    found = []
    for line_number, line in enumerate(content.splitlines(), 1):
        for regex, reason in (
            (HOME_PATH, "personal home path"),
            (AHV, "Swiss AHV number"),
            (TOKEN, "access token"),
        ):
            if regex.search(line):
                found.append((line_number, reason))
        if any(not allowed_email(match.group()) for match in EMAIL.finditer(line)):
            found.append((line_number, "email address"))
        if any(match.group().strip() not in PHONE_PLACEHOLDERS
               for match in PHONE.finditer(line)):
            found.append((line_number, "international phone number"))
        if any(pattern.search(line) for pattern in patterns):
            found.append((line_number, "local personal pattern"))
    return found


def staged_contents(filenames):
    """Read index blobs in one batch, not unstaged working-tree contents."""
    index = subprocess.run(
        ["git", "ls-files", "--stage", "-z", "--", *filenames],
        check=True, capture_output=True,
    )
    entries = []
    for record in index.stdout.split(b"\0"):
        if not record:
            continue
        metadata, filename = record.split(b"\t", 1)
        _, object_id, stage = metadata.split()
        if stage != b"0":
            raise ValueError("unmerged index entry")
        entries.append((filename.decode("utf-8", "surrogateescape"), object_id))
    blobs = subprocess.run(
        ["git", "cat-file", "--batch"],
        input=b"".join(object_id + b"\n" for _, object_id in entries),
        check=True, capture_output=True,
    ).stdout
    offset = 0
    for filename, _ in entries:
        end = blobs.index(b"\n", offset)
        _, kind, size = blobs[offset:end].split()
        if kind != b"blob":
            raise ValueError("index entry is not a file")
        offset = end + 1
        size = int(size)
        yield filename, blobs[offset:offset + size].decode("utf-8", "replace")
        offset += size + 1


def main(filenames=None):
    filenames = sys.argv[1:] if filenames is None else filenames
    if not filenames:
        return 0
    failed = False
    try:
        patterns = local_patterns()
        for filename, content in staged_contents(filenames):
            for line_number, reason in findings(filename, content, patterns):
                print(f"{filename}:{line_number}: {reason} [redacted]", file=sys.stderr)
                failed = True
    except (OSError, subprocess.CalledProcessError, ValueError):
        print("personal-data-guard: unable to check staged files [redacted]",
              file=sys.stderr)
        return 1
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
