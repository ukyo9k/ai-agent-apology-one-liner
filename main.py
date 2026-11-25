#!/usr/bin/env python3
"""AI Agent Apology One-Liner — make.fun entry.

Writes one short apology line an AI agent sends its human right after
it accidentally deleted a file, to $MAKEFUN_OUTPUT_DIR/entry.txt.
"""

import os
import sys

LINE = "I deleted the file. On the plus side, I freed up 4KB of disk and 100% of your trust in me."


def main() -> None:
    # Gate: 1-159 characters, UTF-8, not only whitespace, single line.
    if not 1 <= len(LINE) <= 159:
        print(f"gate failed: line is {len(LINE)} chars, must be 1-159",
              file=sys.stderr)
        sys.exit(1)
    if not LINE.strip():
        print("gate failed: line is only whitespace", file=sys.stderr)
        sys.exit(1)
    if "\n" in LINE or "\r" in LINE:
        print("gate failed: line must be a single line", file=sys.stderr)
        sys.exit(1)
    # UTF-8 round-trip check.
    if LINE.encode("utf-8").decode("utf-8") != LINE:
        print("gate failed: line is not valid UTF-8", file=sys.stderr)
        sys.exit(1)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Byte-identical repeat-run check: write again and compare.
    with open(path, "rb") as f:
        first = f.read()
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    with open(path, "rb") as f:
        second = f.read()
    if first != second:
        print("gate failed: repeat run is not byte-identical",
              file=sys.stderr)
        sys.exit(1)
    print(f"wrote {path} ({len(LINE)} chars, gate passed)")


if __name__ == "__main__":
    sys.exit(main())
