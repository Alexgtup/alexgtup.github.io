#!/usr/bin/env python3
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import datetime as dt
import os
import sys
import xml.etree.ElementTree as ET

BASE = "https://alexgtup.github.io"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def norm_bytes(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").rstrip()


def read_sitemap(path: Path) -> list[tuple[str, str]]:
    root = ET.parse(path).getroot()
    rows = []
    for node in root.findall("s:url", NS):
        loc = node.find("s:loc", NS)
        lastmod = node.find("s:lastmod", NS)
        if loc is not None and (loc.text or "").strip():
            rows.append(((loc.text or "").strip(), (lastmod.text or "").strip() if lastmod is not None else ""))
    return rows


def local_path(root: Path, url: str) -> Path | None:
    p = urlparse(url).path
    if p == "/":
        return root / "index.html"
    if p.endswith("/"):
        return root / p.lstrip("/") / "index.html"
    candidate = root / p.lstrip("/")
    return candidate if candidate.exists() else None


def fetch(url: str, cache_bust: str = "") -> bytes:
    suffix = ("&" if "?" in url else "?") + "indexnow_delta=" + cache_bust if cache_bust else ""
    req = Request(
        url + suffix,
        headers={
            "User-Agent": "Alexuys-IndexNow-Delta/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urlopen(req, timeout=12) as r:
        if getattr(r, "status", 200) != 200:
            raise HTTPError(url, getattr(r, "status", 500), "non-200", r.headers, None)
        return r.read()


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "/tmp/indexnow-urls.txt")
    sitemap = root / "sitemap.xml"
    if not sitemap.exists():
        raise SystemExit("final sitemap.xml missing")

    rows = read_sitemap(sitemap)
    new_urls = {u for u, _ in rows}
    sha = os.environ.get("GITHUB_SHA", "")[:12] or "compare"

    try:
        old_xml = fetch(BASE + "/sitemap.xml", sha)
        old_root = ET.fromstring(old_xml)
        old_urls = {
            (n.text or "").strip()
            for n in old_root.findall(".//s:loc", NS)
            if (n.text or "").strip()
        }
        baseline_ok = True
    except Exception as e:
        print(f"IndexNow delta: live sitemap unavailable ({type(e).__name__}: {e})")
        old_urls = set()
        baseline_ok = False

    changed: set[str] = set()

    if baseline_ok:
        removed = old_urls - new_urls
        changed.update(removed)

        def compare(url: str) -> tuple[str, bool, str]:
            lp = local_path(root, url)
            if lp is None or not lp.exists():
                return url, True, "local-missing"
            try:
                remote = fetch(url, sha)
            except (HTTPError, URLError, TimeoutError, OSError) as e:
                return url, True, type(e).__name__
            same = norm_bytes(remote) == norm_bytes(lp.read_bytes())
            return url, not same, "changed" if not same else "same"

        with ThreadPoolExecutor(max_workers=12) as ex:
            futs = [ex.submit(compare, u) for u in sorted(new_urls)]
            reasons = {}
            for fut in as_completed(futs):
                url, is_changed, reason = fut.result()
                if is_changed:
                    changed.add(url)
                    reasons[url] = reason

        print(
            f"IndexNow delta: new sitemap={len(new_urls)}, live sitemap={len(old_urls)}, "
            f"changed/new/removed={len(changed)}"
        )
        for url in sorted(changed):
            marker = "removed" if url not in new_urls else reasons.get(url, "changed")
            print(f"  {marker}: {url}")
    else:
        today = dt.datetime.now(dt.timezone.utc).date().isoformat()
        fallback = {u for u, lm in rows if lm == today}
        changed.update(fallback)
        print(f"IndexNow delta fallback: {len(changed)} URLs with lastmod={today}")

    out.write_text("\n".join(sorted(changed)) + ("\n" if changed else ""), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
