#!/usr/bin/env python3
from pathlib import Path
import re
import sys

source_file = Path(__file__).with_name("stage50_hub_experience.py")
source = source_file.read_text(encoding="utf-8")

pattern = re.compile(
    r'def replace_main\(route: str, main: str\) -> None:\n.*?\n\ntelegram =',
    re.S,
)
replacement = r'''def replace_main(route: str, main: str) -> None:
    path = p(route)
    if not path.is_file():
        raise SystemExit(f"stage50 missing {route}")
    text = path.read_text(encoding="utf-8")
    preferred = re.compile(r'<main\b[^>]*id="main-content"[^>]*>.*?</main>', re.S | re.I)
    text, n = preferred.subn(lambda _m: main, text, count=1)
    if n != 1:
        legacy = re.compile(r'<main\b[^>]*>.*?</main>', re.S | re.I)
        text, n = legacy.subn(lambda _m: main, text, count=1)
    if n != 1:
        raise SystemExit(f"stage50 main replace failed {route}")
    path.write_text(text, encoding="utf-8")

telegram ='''
source, n = pattern.subn(lambda _m: replacement, source, count=1)
if n != 1:
    raise SystemExit("stage50-runner: helper patch failed")

namespace = {"__name__": "__main__", "__file__": str(source_file), "__package__": None}
exec(compile(source, str(source_file), "exec"), namespace, namespace)
