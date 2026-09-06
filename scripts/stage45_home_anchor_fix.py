#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
path = root / "index.html"
if not path.is_file():
    raise SystemExit("stage45: homepage missing")
text = path.read_text(encoding="utf-8")
replacements = {
    '<a class="button" href="#projects">Смотреть реальные проекты ↓</a>': '<a class="button" href="#work">Смотреть реальные проекты ↓</a>',
    '<section class="s44-section" aria-labelledby="choose-title">': '<section class="s44-section" id="services" aria-labelledby="choose-title">',
    '<section class="s44-section s44-projects" id="projects" aria-labelledby="projects-title">': '<section class="s44-section s44-projects" id="work" aria-labelledby="projects-title">',
    '<section class="s44-section" aria-labelledby="difference-title">': '<section class="s44-section" id="about" aria-labelledby="difference-title">',
    '<section class="s44-section" aria-labelledby="process-title">': '<section class="s44-section" id="process" aria-labelledby="process-title">',
}
changed = 0
for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new, 1)
        changed += 1
    elif new not in text:
        raise SystemExit(f"stage45: expected homepage marker missing: {old[:80]}")
path.write_text(text, encoding="utf-8")
print(f"stage45 homepage anchors restored: {changed} changes")
