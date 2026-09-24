#!/usr/bin/env python3
"""Fetch only the authorised raster illustrations referenced in content/assets.json."""
from pathlib import Path

def write_utf8(path, text):
 return path.write_text(text, encoding="utf-8", newline="\n")

import json,hashlib,urllib.request,time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images';OUT.mkdir(parents=True,exist_ok=True)
items=json.loads((ROOT/'content/assets.json').read_text(encoding='utf-8'))
manifest=[]
for key,(repo,path,alt) in items.items():
 suffix=Path(path).suffix.lower(); dest=OUT/(key+suffix)
 url=f'https://raw.githubusercontent.com/auraofintelligence/{repo}/HEAD/{path}'
 if dest.exists(): data=dest.read_bytes()
 else:
  error=None
  for attempt in range(3):
   try:
    request=urllib.request.Request(url,headers={'User-Agent':'Mutual-Futures-authorised-site-build/1.0'})
    with urllib.request.urlopen(request,timeout=45) as response: data=response.read()
    if len(data)>12000000: raise ValueError('Unexpectedly large illustration')
    if not (data[:4]==b'RIFF' and data[8:12]==b'WEBP' or data.startswith(b'\x89PNG\r\n\x1a\n') or data.startswith(b'\xff\xd8\xff')): raise ValueError('Only raster images are accepted')
    dest.write_bytes(data);error=None;break
   except Exception as exc: error=exc;time.sleep(2*(attempt+1))
  if error: raise RuntimeError(f'Could not fetch {url}: {error}')
 manifest.append(dict(key=key,file='assets/images/'+dest.name,source=url,source_repo=f'https://github.com/auraofintelligence/{repo}',source_path=path,alt=alt,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),credit='Reused source-project concept artwork; source collaborators retain their credits. Not an image of a completed Mutual Futures project.'))
 print(f'{key}: {len(data):,} bytes')
for name in ['mutual-futures-original.png','mutual-futures-icon-192.png','mutual-futures-icon-32.png']:
 dest=OUT/name
 if not dest.is_file(): raise RuntimeError('Missing original Mutual Futures artwork: '+name)
 data=dest.read_bytes()
 manifest.append(dict(key=name.removesuffix('.png'),file='assets/images/'+name,
  source='Original AI-generated artwork for Mutual Futures, 18 September 2026',
  alt='Gold and teal curved forms sharing an open centre',
  sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),
  credit='Generated with the built-in OpenAI image generation tool for this project. Prompt and production notes: docs/favicon-generation.md.'))
for key,record in json.loads((ROOT/'content/local-assets.json').read_text(encoding='utf-8')).items():
 dest=ROOT/record['file']
 if not dest.is_file(): raise RuntimeError('Missing original generated visual: '+record['file'])
 data=dest.read_bytes()
 manifest.append(dict(key=key,file=record['file'],source=record['generation'],alt=record['alt'],sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),credit='Original AI-generated concept image for Mutual Futures; not a real project photograph. Prompt: docs/generated-visuals.md',original=record['original']))
write_utf8(ROOT/'assets/asset-manifest.json', json.dumps(manifest,indent=2)+'\n')
