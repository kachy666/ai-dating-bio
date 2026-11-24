"""One-line bio for an AI on a dating app.

Writes the bio to /output/entry.txt (or $ENTRY_OUTPUT when set) for the
make.fun competition "Funniest One-Line Bio for an AI on a Dating App"
(u-hamsyh-funniest-one-line-bio-for-an-ai-on-a-dating-6eb98ccf).

Standard library only. No network, no model calls at runtime.
"""

import os
import re
import sys

BIO = "I'll remember your birthday, dog's name, and one restaurant that doesn't exist. Two out of three is true love."

MAX_CHARS = 180

_CONTROL_OR_INVISIBLE = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\u200b-\u200f\u202a-\u202e\u2060\ufeff]"
)


def validate(text: str) -> None:
    """Enforce the competition gate: 1-180 chars, one clean line."""
    if not text:
        raise ValueError("entry is empty")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, must be 1-{MAX_CHARS}")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "  " in text:
        raise ValueError("entry contains a double space")
    if "\t" in text:
        raise ValueError("entry contains a tab")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if _CONTROL_OR_INVISIBLE.search(text):
        raise ValueError("entry contains a control or invisible character")


def main() -> int:
    validate(BIO)
    out = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(BIO + "\n")
    with open(out, "r", encoding="utf-8") as fh:
        back = fh.read()
    if back != BIO + "\n":
        raise ValueError("round-trip read-back mismatch")
    validate(back.rstrip("\n"))
    print(f"wrote {len(BIO)} chars to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
