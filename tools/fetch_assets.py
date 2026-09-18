#!/usr/bin/env python3
"""Fetch only the authorised raster illustrations referenced in content/assets.json."""
from pathlib import Path
import json,hashlib,urllib.request,time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/images';OUT.mkdir(parents=True,exist_ok=True)
items=json.loads((ROOT/'content/assets.json').read_text())
items['favicon']=['gajra-earth-claude-build','assets/aura-heart-192.png','GAJRA Earth source-project raster favicon']
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
(ROOT/'assets/asset-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
