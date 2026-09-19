#!/usr/bin/env python3
"""Validate the actual publish artifact after every content transformation."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys
import xml.etree.ElementTree as ET

BASE = 'https://alexgtup.github.io'


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.canonicals, self.robots, self.links = [], [], []
        self.h1 = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'h1':
            self.h1 += 1
        if tag == 'a':
            self.links.append(a.get('href') or '')
        if tag == 'link' and 'canonical' in (a.get('rel') or '').lower().split():
            self.canonicals.append(a.get('href'))
        if tag == 'meta' and (a.get('name') or '').lower() == 'robots':
            self.robots.append(a.get('content') or '')


def validate(root):
    errors, docs = [], {}
    for path in root.rglob('*.html'):
        text = path.read_text(encoding='utf-8')
        docs[path.resolve()] = Document(text)
        for match in re.finditer(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, re.I | re.S):
            try:
                json.loads(match[1])
            except ValueError:
                errors.append(f'invalid JSON-LD: {path}')

    def local_path(url):
        path = root / unquote(urlsplit(url).path).lstrip('/')
        return (path / 'index.html' if path.is_dir() else path).resolve()

    primary = None
    for name in ('sitemap.xml', 'sitemap-google.xml'):
        urls = [(node.text or '').strip() for node in ET.parse(root / name).findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        if not urls:
            errors.append(f'empty sitemap: {name}')
        if len(urls) != len(set(urls)):
            errors.append(f'duplicate URLs: {name}')
        if primary is None:
            primary = set(urls)
        elif set(urls) != primary:
            errors.append('XML sitemaps disagree')
        for url in urls:
            parsed = urlsplit(url)
            if parsed.scheme != 'https' or parsed.netloc != urlsplit(BASE).netloc or parsed.query or parsed.fragment:
                errors.append(f'invalid sitemap URL: {url}')
                continue
            doc = docs.get(local_path(url))
            if doc is None:
                errors.append(f'missing sitemap page: {url}')
                continue
            if doc.canonicals != [url]:
                errors.append(f'canonical mismatch: {url}')
            if len(doc.robots) != 1:
                errors.append(f'expected one robots meta: {url}')
            directives = {v.strip().lower() for s in doc.robots for v in s.split(',')}
            if directives & {'none', 'noindex'}:
                errors.append(f'noindex in sitemap: {url}')
            if doc.h1 != 1:
                errors.append(f'expected one H1: {url}')
    if set((root / 'sitemap.txt').read_text().splitlines()) != primary:
        errors.append('text and XML sitemaps disagree')
    for source, doc in docs.items():
        for href in doc.links:
            parsed = urlsplit(href)
            if parsed.scheme not in ('', 'http', 'https') or (parsed.netloc and parsed.netloc != urlsplit(BASE).netloc):
                continue
            if parsed.path.startswith('/') or parsed.netloc:
                target = local_path(href)
            else:
                target = (source.parent / unquote(parsed.path)) if parsed.path else source
                if target.is_dir():
                    target /= 'index.html'
            if not target.exists():
                errors.append(f'broken link: {source.relative_to(root.resolve())} -> {href}')
    if errors:
        raise SystemExit('Final indexability failed:\n' + '\n'.join(sorted(set(errors))))
    print(f'Final indexability OK: {len(primary)} sitemap URLs, {len(docs)} HTML files; canonical, robots, H1, JSON-LD and internal links checked')


if __name__ == '__main__':
    validate(Path(sys.argv[1] if len(sys.argv) > 1 else '_site'))
