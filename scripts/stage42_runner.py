#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

# Stage 42 was intentionally authored as a standalone build patch, but its first
# implementation looked for one literal opening tag order. Production pages use
# equivalent hero markup with different attribute/class order. Patch that helper at
# runtime so the commercial layer remains independent of source formatting while
# keeping the Stage 42 content itself auditable in one file.
target = Path(__file__).with_name("stage42_competitor_gap.py")
if not target.is_file():
    raise SystemExit("stage42-runner: stage42_competitor_gap.py missing")

source = target.read_text(encoding="utf-8")
pattern = re.compile(
    r'def insert_after_hero\(text: str, block: str, route: str\) -> str:\n.*?\n\n\ndef insert_before_trust',
    re.S,
)
replacement = r'''def insert_after_hero(text: str, block: str, route: str) -> str:
    if 'data-stage42-market="true"' in text:
        return text
    # Match a SECTION whose class list contains the standalone token `hero`,
    # regardless of attribute order or extra classes such as `hero container`.
    hero_re = re.compile(
        r'<section\b(?=[^>]*\bclass="[^"]*(?:^|\s)hero(?:\s|$)[^"]*")[^>]*>',
        re.I,
    )
    match = hero_re.search(text)
    if not match:
        # Fallback for compact/generated markup where class token boundaries are
        # still valid HTML but whitespace can be unusual.
        hero_re = re.compile(r'<section\b[^>]*\bclass="[^"]*hero[^"]*"[^>]*>', re.I)
        match = hero_re.search(text)
    if not match:
        raise SystemExit(f"stage42: hero not found: {route}")
    start = match.start()
    end = text.find('</section>', match.end())
    if end < 0:
        raise SystemExit(f"stage42: hero end not found: {route}")
    end += len('</section>')
    return text[:end] + "\n" + block + text[end:]


def insert_before_trust'''

# Use a callable replacement so backslashes in the injected Python source are
# treated literally rather than as re.sub replacement escapes.
source, count = pattern.subn(lambda _m: replacement, source, count=1)
if count != 1:
    raise SystemExit("stage42-runner: could not replace insert_after_hero helper")

namespace = {
    "__name__": "__main__",
    "__file__": str(target),
    "__package__": None,
}
exec(compile(source, str(target), "exec"), namespace, namespace)
