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
SECTION_RE = re.compile(r"\s*<section\b[^>]*>.*?</section>\s*", re.I | re.S)
DIRECT_CONTACT_RE = re.compile(r"https://t\.me/Alexuys|mailto:alexgtup@gmail\.com", re.I)
SECTION_START_RE = re.compile(r"<section\b[^>]*>", re.I | re.S)


def final_section_has_contact(main: str) -> bool:
    sections = list(SECTION_START_RE.finditer(main))
    if not sections:
        return False
    return bool(DIRECT_CONTACT_RE.search(main[sections[-1].start():]))


def is_case_detail(rel: str) -> bool:
    parts = Path(rel).parts
    return len(parts) >= 3 and parts[0] == "cases" and parts[-1] == "index.html"


def is_page_specific_conversion(block: str, rel: str) -> bool:
    """Identify a genuine page-ending conversion surface, not any section with a link.

    Case detail pages are allowed to use their bespoke demo/contact sections. Hubs
    stay conservative: only explicit contact/cta classes can replace Stage64.
    This prevents a hero or product recommendation from being moved to the end.
    """
    if not DIRECT_CONTACT_RE.search(block):
        return False
    opening = block[: block.find(">") + 1].lower()
    excluded = (
        "s64-conversion",
        "growth-section",
        "s51-hero",
        "s48-hero",
        "s50-hero",
        "s44-services-hero",
        "s68-entry",
        "s66-tool-link",
        "case-study-hero",
        'class="hero',
        "class='hero",
    )
    if any(marker in opening for marker in excluded):
        return False

    # Product/case pages may intentionally use a plain `.section` that combines
    # live demo + Telegram. That is strong, specific and should beat generic copy.
    if is_case_detail(rel):
        return True

    # Hubs/guides are stricter: only semantically explicit CTA containers qualify.
    explicit = ("contact", "cta-box", "s50-cta")
    return any(marker in opening for marker in explicit)


def native_blocks(main: str, rel: str) -> list[re.Match[str]]:
    return [m for m in SECTION_RE.finditer(main) if is_page_specific_conversion(m.group(0), rel)]


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
    rel = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8")
    mm = MAIN_RE.search(text)
    if not mm:
        raise SystemExit(f"stage85: missing <main>: {rel}")
    main = mm.group(0)
    original = main

    s64_blocks = list(S64_RE.finditer(main))
    natives = native_blocks(main, rel)

    if natives and s64_blocks:
        native_match = natives[-1]
        native_html = native_match.group(0).strip()
        main = S64_RE.sub("\n", main)
        removed_s64 += len(s64_blocks)

        main = main.replace(native_match.group(0), "\n", 1)
        main = main[:-7].rstrip() + "\n\n" + native_html + "\n</main>"
        moved_native += 1

    elif len(s64_blocks) > 1:
        keep_html = s64_blocks[-1].group(0).strip()
        main = S64_RE.sub("\n", main)
        main = main[:-7].rstrip() + "\n\n" + keep_html + "\n</main>"
        removed_s64 += len(s64_blocks) - 1
        deduped_s64 += 1

    if main != original:
        text = text[: mm.start()] + main + text[mm.end():]
        path.write_text(text, encoding="utf-8")
        changed.append(rel)

problems: list[str] = []
for path in target_files():
    rel = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8")
    mm = MAIN_RE.search(text)
    if not mm:
        continue
    main = mm.group(0)
    s64_count = len(S64_RE.findall(main))
    native_count = len(native_blocks(main, rel))
    if s64_count > 1:
        problems.append(f"{rel}: s64={s64_count}")
    if s64_count and native_count:
        problems.append(f"{rel}: generic+native conversion duplicate")
    if rel in changed and not final_section_has_contact(main):
        problems.append(f"{rel}: final section lost direct contact")

# Structural regression guards for the two primary hubs that were previously
# vulnerable to accidental hero/product relocation.
for rel, expected_first in (("about/index.html", "s50-hero"), ("services/index.html", "s44-services-hero")):
    path = root / rel
    if not path.is_file():
        continue
    main = MAIN_RE.search(path.read_text(encoding="utf-8"))
    if not main:
        continue
    first = SECTION_START_RE.search(main.group(0))
    if not first or expected_first not in first.group(0):
        problems.append(f"{rel}: first section must remain {expected_first}")

if problems:
    raise SystemExit("stage85 conversion cleanup invariant failed: " + "; ".join(problems))

print(
    f"stage85 conversion cleanup: changed={len(changed)}; removed generic CTA={removed_s64}; "
    f"native CTA moved to ending={moved_native}; duplicate Stage64 hubs={deduped_s64}"
)
if changed:
    print("stage85 cleaned pages: " + ", ".join(changed))
