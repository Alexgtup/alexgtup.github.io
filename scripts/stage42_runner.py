#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

target = Path(__file__).with_name("stage42_competitor_gap.py")
if not target.is_file():
    raise SystemExit("stage42-runner: stage42_competitor_gap.py missing")

source = target.read_text(encoding="utf-8")
# Public profile metrics change over time. Keep the commercial blocks aligned with
# facts currently visible on Freelance.ru instead of repeating an unverified review count.
source = source.replace("20+ отзывов на Freelance.ru", "19 выполненных заданий · оценки 9/9")
source = source.replace("20+ отзывов на Freelance.ru.", "проверяемый профиль Freelance.ru.")
source = source.replace("20+ отзывов", "19 выполненных заданий")

pattern = re.compile(
    r'def insert_after_hero\(text: str, block: str, route: str\) -> str:\n.*?\n\n\ndef insert_before_trust',
    re.S,
)
replacement = r'''def insert_after_hero(text: str, block: str, route: str) -> str:
    if 'data-stage42-market="true"' in text:
        return text
    hero_re = re.compile(
        r'<section\b(?=[^>]*\bclass="[^"]*(?:^|\s)hero(?:\s|$)[^"]*")[^>]*>',
        re.I,
    )
    match = hero_re.search(text)
    if not match:
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

source, count = pattern.subn(lambda _m: replacement, source, count=1)
if count != 1:
    raise SystemExit("stage42-runner: could not replace insert_after_hero helper")

namespace = {"__name__":"__main__","__file__":str(target),"__package__":None}
exec(compile(source, str(target), "exec"), namespace, namespace)
