#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")

# 1) Make internal interaction goals respect the same consent gate as all other analytics.
js_path = root / "assets" / "site-enhancements.js"
if not js_path.is_file():
    raise SystemExit(f"stage64: missing {js_path}")

js = js_path.read_text(encoding="utf-8")
stage8 = js.find("// Stage 8: useful interaction goals")
if stage8 < 0:
    raise SystemExit("stage64: Stage 8 analytics block not found")

start = js.find("  const METRIKA_ID = 112290993;", stage8)
listener = js.find("  document.addEventListener('click'", stage8)
if start >= 0 and listener > start:
    block = js[start:listener]
    service_line = next((line for line in block.splitlines() if "const servicePaths =" in line), None)
    if not service_line:
        raise SystemExit("stage64: service path registry missing in Stage 8")
    replacement = (
        service_line
        + "\n"
        + "  const goal = (name, params={}) => {\n"
        + "    const analytics = window.alexuysAnalytics;\n"
        + "    if (!analytics || typeof analytics.goal !== 'function') return;\n"
        + "    analytics.goal(name, params);\n"
        + "  };\n"
    )
    js = js[:start] + replacement + js[listener:]
elif "const analytics = window.alexuysAnalytics;" not in js[stage8:listener if listener > 0 else None]:
    raise SystemExit("stage64: Stage 8 analytics block has unexpected shape")

# Mark the dynamically-created mobile CTA so telegram_click can be segmented by placement.
mobile_marker = "    cta.rel = 'noopener noreferrer';\n    cta.textContent ="
if "cta.dataset.cta = 'mobile_floating';" not in js:
    if mobile_marker not in js:
        raise SystemExit("stage64: mobile CTA marker not found")
    js = js.replace(
        mobile_marker,
        "    cta.rel = 'noopener noreferrer';\n    cta.dataset.cta = 'mobile_floating';\n    cta.textContent =",
        1,
    )

js_path.write_text(js, encoding="utf-8")

# 2) Add a clear static conversion path at the end of individual cases and guides.
# Mobile already has a floating CTA; this fixes the desktop/end-of-content dead end too.
def cta_html(kind: str, english: bool) -> str:
    if english:
        if kind == "case":
            kicker = "HAVE A SIMILAR PROJECT?"
            title = "Show the current state. We can define the next working step."
            body = "A link, screenshot or short description is enough to start. I will use the current project state instead of forcing a rebuild from zero."
            secondary_href = "/en/services/"
            secondary_text = "View services →"
            primary_text = "Discuss in Telegram ↗"
        else:
            kicker = "READY TO TURN THE DECISION INTO A BUILD?"
            title = "Translate the choice into a concrete first release."
            body = "Send the current workflow, constraints and expected result. The first step can stay small and measurable."
            secondary_href = "/en/cases/"
            secondary_text = "View cases →"
            primary_text = "Discuss in Telegram ↗"
    else:
        if kind == "case":
            kicker = "ЕСТЬ ПОХОЖАЯ ЗАДАЧА?"
            title = "Покажите текущее состояние — определим следующий рабочий шаг."
            body = "Для старта достаточно ссылки, скриншота или короткого описания. Не обязательно переписывать проект с нуля — сначала оценивается то, что уже есть."
            secondary_href = "/services/"
            secondary_text = "Посмотреть направления →"
            primary_text = "Обсудить в Telegram ↗"
        else:
            kicker = "РЕШЕНИЕ СТАЛО ПОНЯТНЕЕ?"
            title = "Переведём выбор в конкретный первый этап разработки."
            body = "Пришлите текущий сценарий, ограничения и ожидаемый результат. Первый этап можно сделать небольшим и измеримым."
            secondary_href = "/cases/"
            secondary_text = "Посмотреть кейсы →"
            primary_text = "Обсудить в Telegram ↗"

    placement = f"{kind}_end"
    return f'''\n<section class="s64-conversion" data-stage64-conversion="{kind}">
  <div class="container s64-conversion__inner">
    <span class="s64-conversion__kicker">{kicker}</span>
    <h2>{title}</h2>
    <p>{body}</p>
    <div class="s64-conversion__actions">
      <a class="button primary" href="https://t.me/Alexuys" target="_blank" rel="noopener noreferrer" data-cta="{placement}">{primary_text}</a>
      <a class="button" href="{secondary_href}">{secondary_text}</a>
    </div>
  </div>
</section>\n'''


def patch_page(path: Path, kind: str, english: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'data-stage64-conversion=' in text:
        return False
    match = re.search(r"<main\b[^>]*>.*?</main>", text, flags=re.S | re.I)
    if not match:
        raise SystemExit(f"stage64: <main> not found: {path}")
    main = match.group(0)
    # If a page already ends with a direct Telegram action, do not duplicate it.
    if "https://t.me/Alexuys" in main[-3200:]:
        return False
    patched_main = main[:-7] + cta_html(kind, english) + "</main>"
    text = text[: match.start()] + patched_main + text[match.end() :]
    path.write_text(text, encoding="utf-8")
    return True

patched = []
targets: list[tuple[Path, str, bool]] = []
for p in sorted((root / "cases").glob("*/index.html")):
    targets.append((p, "case", False))
for p in sorted((root / "guides").glob("*/index.html")):
    targets.append((p, "guide", False))
for p in sorted((root / "en" / "cases").glob("*/index.html")):
    targets.append((p, "case", True))
for p in sorted((root / "en" / "guides").glob("*/index.html")):
    targets.append((p, "guide", True))

for path, kind, english in targets:
    if patch_page(path, kind, english):
        patched.append(path.relative_to(root).as_posix())

# 3) Shared styling. Stage 62 runs afterwards and fingerprints the final CSS.
css_path = root / "assets" / "site-enhancements.css"
if not css_path.is_file():
    raise SystemExit(f"stage64: missing {css_path}")
css = css_path.read_text(encoding="utf-8")
marker = "/* stage64 conversion paths */"
if marker not in css:
    css += r'''

/* stage64 conversion paths */
.s64-conversion{padding:clamp(4.5rem,8vw,7rem) 0;border-top:1px solid rgba(255,255,255,.08)}
.s64-conversion__inner{width:min(100%,92rem);margin-inline:auto;padding-inline:clamp(1.1rem,4vw,4.5rem)}
.s64-conversion__inner{padding-top:clamp(1.5rem,3vw,2.2rem);padding-bottom:clamp(1.5rem,3vw,2.2rem);border:1px solid rgba(255,255,255,.11);border-radius:1.25rem;background:linear-gradient(145deg,#11161c,#0c1015)}
.s64-conversion__kicker{display:block;color:#7f8994;font:800 .62rem/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.09em}
.s64-conversion h2{max-width:18ch;margin:.75rem 0 0;font-size:clamp(2rem,4.2vw,4.3rem);line-height:.98;letter-spacing:-.05em}
.s64-conversion p{max-width:58rem;margin:1rem 0 0;color:#929ba5;line-height:1.7}
.s64-conversion__actions{display:flex;gap:.65rem;flex-wrap:wrap;margin-top:1.4rem}
@media(max-width:700px){.s64-conversion{padding:3.5rem 0}.s64-conversion__inner{border-radius:1rem}.s64-conversion__actions .button{width:100%;justify-content:center;text-align:center}}
'''
    css_path.write_text(css, encoding="utf-8")

# Guard the intended conversion path on every targeted page.
missing = []
for path, _, _ in targets:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"<main\b[^>]*>.*?</main>", text, flags=re.S | re.I)
    if not match or "https://t.me/Alexuys" not in match.group(0)[-4200:]:
        missing.append(path.relative_to(root).as_posix())
if missing:
    raise SystemExit("stage64: pages still missing end-of-content Telegram path: " + ", ".join(missing))

print(f"stage64: consent-aware internal goals patched; end CTA added to {len(patched)} pages")
