#!/usr/bin/env python3
"""Mirror checked static pages for GitHub Pages' main/root publishing option."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'
for page in SITE.glob('*.html'):
 shutil.copy2(page,ROOT/page.name)
for name in ['.nojekyll','robots.txt','sitemap.xml']:
 shutil.copy2(SITE/name,ROOT/name)
for folder in ['guides','originals']:
 source=SITE/'documents'/folder
 if source.exists():shutil.copytree(source,ROOT/'documents'/folder,dirs_exist_ok=True)
shutil.copy2(SITE/'documents/manifest.json',ROOT/'documents/manifest.json')
print('Mirrored generated HTML, discovery files and document library into the repository root. Source code, README and About remain unchanged.')
