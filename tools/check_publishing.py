#!/usr/bin/env python3
"""Prevent the repository-root publisher from replacing the designed website."""
from pathlib import Path
from hashlib import sha256
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
errors = []
files = list(SITE.glob('*.html')) + [SITE / n for n in ('.nojekyll', 'robots.txt', 'sitemap.xml')]
files += [p for folder in ('assets', 'documents') for p in (SITE / folder).rglob('*') if p.is_file()]
for source in files:
    relative = source.relative_to(SITE)
    published = ROOT / relative
    if not published.is_file():
        errors.append(f'Missing root-publishing file: {relative}')
    elif sha256(source.read_bytes()).digest() != sha256(published.read_bytes()).digest():
        errors.append(f'Root and Actions artifact differ: {relative}')
for root in (ROOT, SITE):
    homepage = (root / 'index.html').read_text(encoding='utf-8')
    if 'class="hero home"' not in homepage or 'id="site-index"' not in homepage:
        errors.append(f'{root.name}: homepage is not the designed Mutual Futures page')
print(json.dumps({'checked_files': len(files), 'errors': errors}, indent=2))
if errors:
    raise SystemExit(1)
