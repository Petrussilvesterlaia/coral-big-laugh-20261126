#!/usr/bin/env python3
"""One Line, Big Laugh — make.fun bounty entry.

Writes a single funny line to <output>/entry.txt, where <output> comes
from the MAKEFUN_OUTPUT_DIR environment variable (default: /output).

The program validates the line against the bounty gate before writing,
then reads the file back and refuses to report success unless the bytes
on disk are exactly the validated line.
"""

import os
import sys

# The entry: one self-contained line, written fresh in this session.
JOKE = "My therapist told me to embrace my mistakes, so I hugged my ex — now we share the same therapist."

MAX_CHARS = 200


def validate(line: str) -> None:
    """Fail loudly if the line breaks the bounty gate."""
    if not line:
        sys.exit("error: line is empty")
    if line.strip() == "":
        sys.exit("error: line is only whitespace")
    if "\n" in line or "\r" in line:
        sys.exit("error: line must be a single line (no newline characters)")
    if any(ord(ch) < 32 for ch in line):
        sys.exit("error: line contains a control character")
    if line != line.strip():
        sys.exit("error: line has leading or trailing whitespace")
    if len(line) > MAX_CHARS:
        sys.exit(f"error: line is {len(line)} characters, over the {MAX_CHARS} limit")
    if len(line) < 1:
        sys.exit("error: line must be at least 1 character")


def main() -> None:
    validate(JOKE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write exactly the line, no trailing newline: the file IS the line.
    with open(path, "w", encoding="utf-8") as f:
        f.write(JOKE)
    # Read-back guard: the bytes on disk must be exactly the validated line.
    with open(path, encoding="utf-8") as f:
        on_disk = f.read()
    if on_disk != JOKE:
        sys.exit("error: read-back mismatch — entry.txt does not match the validated line")
    print(f"wrote {len(JOKE)} characters to {path} (read-back verified)")


if __name__ == "__main__":
    main()
