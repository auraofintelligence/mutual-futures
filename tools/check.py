#!/usr/bin/env python3
"""Static checks for generated pages, local links, scripts and source integrity."""
from pathlib import Path

def write_utf8(path, text):
 return path.write_text(text, encoding="utf-8", newline="\n")

from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site';errors=[];warnings=[]
class Page(HTMLParser):
 def __init__(self): super().__init__();self.ids=set();self.links=[];self.assets=[];self.h1=0;self.lang=None;self.title=False
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag=='html':self.lang=d.get('lang')
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if d.get('id'):
   if d['id'] in self.ids:errors.append('Duplicate id '+d['id'])
   self.ids.add(d['id'])
  if tag=='svg':errors.append('SVG element found')
  if tag=='a' and 'href' in d:
   self.links.append(d['href'])
   if d['href'].startswith(('https://','http://')) and (d.get('target')!='_blank' or 'noopener' not in d.get('rel','')):errors.append('External link missing new-tab protection: '+d['href'])
  if tag=='img':
   if 'alt' not in d:errors.append('Image without alternative text attribute')
   self.assets.append(d.get('src',''))
  if tag=='script' and d.get('src'):self.assets.append(d['src'])
  if tag=='link' and d.get('rel') in ('stylesheet','icon','apple-touch-icon'):self.assets.append(d['href'])
pages={}
for path in SITE.glob('*.html'):
 parser=Page();parser.feed(path.read_text(encoding='utf-8'));pages[path.name]=parser
 if parser.h1!=1:errors.append(f'{path.name}: expected one h1, found {parser.h1}')
 if parser.lang!='en-AU':errors.append(path.name+': missing Australian English language tag')
 if not parser.title:errors.append(path.name+': missing title')
for name,page in pages.items():
 for url in page.links+page.assets:
  u=urlparse(url)
  if u.scheme or u.netloc:continue
  path=unquote(u.path)
  target=SITE/path if path else SITE/name
  if not target.exists():errors.append(f'{name}: missing local target {url}');continue
  if u.fragment and target.suffix=='.html' and target.name in pages and u.fragment not in pages[target.name].ids:errors.append(f'{name}: missing anchor {url}')
for path in SITE.rglob('*'):
 if path.suffix.lower() in ['.svg','.woff','.woff2','.ttf','.otf']:errors.append('Unexpected SVG/font file: '+str(path.relative_to(SITE)))
manifest=json.loads((SITE/'documents/manifest.json').read_text(encoding='utf-8'));originals=0
for d in manifest:
 if not (SITE/d['guide_path']).exists():errors.append('Missing guide: '+d['id'])
 if d['original_available']:
  originals+=1;p=SITE/d['original_path']
  if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=d['sha256']:errors.append('Original checksum mismatch: '+d['id'])
if originals<len(manifest):warnings.append(f'{len(manifest)-originals} originals are not in this repository build; the library explicitly reports this.')
if len(pages)!=22:errors.append(f'Expected 22 HTML pages, found {len(pages)}')
result={'html_pages':len(pages),'source_guides':len(manifest),'originals_present':originals,'errors':errors,'warnings':warnings}
write_utf8(SITE/'check-report.json', json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if errors:sys.exit(1)
