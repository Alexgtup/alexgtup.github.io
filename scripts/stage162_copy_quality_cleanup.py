#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
path = ROOT / "telegram-bots" / "index.html"
if not path.exists():
    raise SystemExit("stage162: telegram-bots page missing")

text = path.read_text(encoding="utf-8")
old = "Что важно в разработке Telegram-бота до запуска."
new = "Что важно при разработке Telegram-бота до запуска."

if old not in text and new not in text:
    raise SystemExit("stage162: target heading missing")
text = text.replace(old, new)
path.write_text(text, encoding="utf-8")

final = path.read_text(encoding="utf-8")
if old in final or new not in final:
    raise SystemExit("stage162: cleanup guard failed")

print("stage162 copy quality cleanup: /telegram-bots/")
