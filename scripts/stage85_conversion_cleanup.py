#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

MAIN_RE = re.compile(r"<main\b[^>]*>.*?</main>", re.I | re.S)
S64_RE = re.compile(
    r"\s*<section\b[^>]*class=[\"'][^\"']*\bs64-conversion\b[^\"']*[\"'][^>]*>.*?</section>\s*",
    re.I | re.S,
)
NATIVE_RE = re.compile(
    r"\s*<section\b[^>]*class=[\"'][^\"']*\b(?:contact|cta-box)\b[^\"']*[\"'][^>]*>.*?</section>\s*",
    re.I | re.S,
)
DIRECT_CONTACT_RE = re.compile(r"https://t\.me/Alexuys|mailto:alexgtup@gmail\.com", re.I)
SECTION_START_RE = re.compile(r"<section\b[^>]*>", re.I | re.S)


def final_section_has_contact(main: str) -> bool:
    sections = list(SECTION_START_RE.finditer(main))
    if not sections:
        return False
    return bool(DIRECT_CONTACT_RE.search(main[sections[-1].start():]))


def target_files() -> list[Path]:
    out: list[Path] = []
    for base in (root / "cases", root / "guides", root / "en" / "cases", root / "en" / "guides"):
        if base.is_dir():
            out.extend(sorted(base.glob("*/index.html")))
    for p in (
        root / "cases" / "index.html",
        root / "guides" / "index.html",
        root / "services" / "index.html",
        root / "about" / "index.html",
        root / "en" / "cases" / "index.html",
        root / "en" / "guides" / "index.html",
        root / "en" / "services" / "index.html",
        root / "en" / "about" / "index.html",
    ):
        if p.is_file():
            out.append(p)
    # preserve order while removing duplicates
    seen: set[Path] = set()
    unique: list[Path] = []
    for p in out:
        key = p.resolve()
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


changed: list[str] = []
removed_s64 = 0
moved_native = 0
deduped_s64 = 0

for path in target_files():
    text = path.read_text(encoding="utf-8")
    mm = MAIN_RE.search(text)
    if not mm:
        raise SystemExit(f"stage85: missing <main>: {path.relative_to(root)}")
    main = mm.group(0)
    original = main

    s64_blocks = list(S64_RE.finditer(main))
    native_blocks = [m for m in NATIVE_RE.finditer(main) if DIRECT_CONTACT_RE.search(m.group(0))]

    if native_blocks and s64_blocks:
        # Prefer the page-specific conversion surface. It usually contains context
        # tailored to the case/guide and is less repetitive than the generic Stage64 CTA.
        native_html = native_blocks[-1].group(0).strip()
        main = S64_RE.sub("\n", main)
        removed_s64 += len(s64_blocks)

        # Move the native CTA to the real page ending so recommendation/demo blocks
        # can stay above it without forcing another generic CTA after them.
        main = main.replace(native_blocks[-1].group(0), "\n", 1)
        main = main[:-7].rstrip() + "\n\n" + native_html + "\n</main>"
        moved_native += 1

    elif len(s64_blocks) > 1:
        # Hubs such as /about/ and /services/ can receive Stage64 twice because a
        # later growth block is appended between the two Stage64 passes. Keep one.
        keep_html = s64_blocks[-1].group(0).strip()
        main = S64_RE.sub("\n", main)
        main = main[:-7].rstrip() + "\n\n" + keep_html + "\n</main>"
        removed_s64 += len(s64_blocks) - 1
        deduped_s64 += 1

    if main != original:
        text = text[: mm.start()] + main + text[mm.end():]
        path.write_text(text, encoding="utf-8")
        changed.append(path.relative_to(root).as_posix())

# Final invariant: no target page may end with multiple generic conversion blocks,
# and every touched target must still finish with a direct contact action.
problems: list[str] = []
for path in target_files():
    text = path.read_text(encoding="utf-8")
    mm = MAIN_RE.search(text)
    if not mm:
        continue
    main = mm.group(0)
    s64_count = len(S64_RE.findall(main))
    native_count = sum(1 for m in NATIVE_RE.finditer(main) if DIRECT_CONTACT_RE.search(m.group(0)))
    if s64_count > 1:
        problems.append(f"{path.relative_to(root)}: s64={s64_count}")
    if s64_count and native_count:
        problems.append(f"{path.relative_to(root)}: generic+native conversion duplicate")
    if path.relative_to(root).as_posix() in changed and not final_section_has_contact(main):
        problems.append(f"{path.relative_to(root)}: final section lost direct contact")

if problems:
    raise SystemExit("stage85 conversion cleanup invariant failed: " + "; ".join(problems))

print(
    f"stage85 conversion cleanup: changed={len(changed)}; removed generic CTA={removed_s64}; "
    f"native CTA moved to ending={moved_native}; duplicate Stage64 hubs={deduped_s64}"
)
if changed:
    print("stage85 cleaned pages: " + ", ".join(changed))
