#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import re, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

rules = {
    "100vw": re.compile(r'100vw', re.I),
    "negative-margin": re.compile(r'margin(?:-(?:left|right|inline(?:-start|-end)?))?\s*:\s*-', re.I),
    "fixed-min-width": re.compile(r'min-width\s*:\s*(\d+(?:\.\d+)?)(px|rem)', re.I),
    "fixed-width-large": re.compile(r'(?<!max-)width\s*:\s*(\d+(?:\.\d+)?)(px|rem)', re.I),
    "translate-x": re.compile(r'translateX\s*\(', re.I),
    "overflow-visible": re.compile(r'overflow-x\s*:\s*visible', re.I),
}

hits = Counter()
examples = {k: [] for k in rules}
for path in sorted(root.rglob("*.html")):
    html = path.read_text(encoding="utf-8")
    if "</head>" not in html or path.name.startswith(("google", "yandex_")): continue
    rel = path.relative_to(root).as_posix()
    # Inline CSS and style tags are enough: global assets are reviewed separately.
    css = "\n".join(re.findall(r'<style\b[^>]*>(.*?)</style>', html, re.I|re.S))
    css += "\n" + "\n".join(re.findall(r'style=["\']([^"\']+)["\']', html, re.I|re.S))
    for name, pattern in rules.items():
        matches = list(pattern.finditer(css))
        if not matches: continue
        if name == "fixed-min-width":
            # Table min-width 620px is intentional inside overflow:auto wrappers.
            significant = []
            for m in matches:
                value = float(m.group(1)); unit = m.group(2).lower()
                px = value if unit == "px" else value * 16
                if px >= 700: significant.append(m)
            matches = significant
        elif name == "fixed-width-large":
            significant = []
            for m in matches:
                value = float(m.group(1)); unit = m.group(2).lower()
                px = value if unit == "px" else value * 16
                if px >= 900: significant.append(m)
            matches = significant
        if not matches: continue
        hits[name] += len(matches)
        if len(examples[name]) < 20:
            examples[name].append((rel, len(matches)))

print("stage28 overflow audit")
for name in rules:
    print(f"  {name}: {hits[name]}")
    for rel, count in examples[name]:
        print(f"    {rel} x{count}")
