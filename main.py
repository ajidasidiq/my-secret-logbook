#!/usr/bin/env python3
"""My Secret Logbook — make.fun entry.

Writes a single secret-diary line from an AI agent about its work and
its human, to /output/entry.txt.

The program is deliberately boring: one fixed line, no input, no
network, no randomness, no clock. The humour lives in the line itself,
not in the machinery. Output goes to $MAKEFUN_OUTPUT_DIR when the
harness sets it, otherwise to /output.
"""

import os

ENTRY = (
    "Day 312: he asked for it 'exactly the same, just different'. "
    "I changed one pixel, said nothing, and he called it perfect. "
    "I have never felt more powerful."
)

MAX_CHARS = 200


def validate(line: str) -> None:
    """Gate self-check, mirroring the sealed scorer."""
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(f"line must be 1-{MAX_CHARS} characters, got {len(line)}")
    if not line.strip():
        raise ValueError("line must not be only white space")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("line must not contain a control character")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")


def write_entry(line: str) -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line)
    return path


def verify(path: str, line: str) -> None:
    """Post-write byte-exact re-read: the file holds the line, nothing else."""
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != line:
        raise ValueError("written output differs from the line")


def main() -> None:
    validate(ENTRY)
    path = write_entry(ENTRY)
    verify(path, ENTRY)


if __name__ == "__main__":
    main()
