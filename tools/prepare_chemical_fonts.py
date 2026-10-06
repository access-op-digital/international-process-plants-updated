"""Fetch the brand's Latin WOFF2 variable fonts from Google's public font service."""
from pathlib import Path
from urllib.request import Request,urlopen
import json,re
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/chemical'
ua='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
def get(url):
 with urlopen(Request(url,headers={'User-Agent':ua}),timeout=40) as r:return r.read()
url='https://fonts.googleapis.com/css2?family=Montserrat:wght@400..700&family=Roboto:wght@400..700&family=Inter:wght@400..700&display=swap'
css=get(url).decode()
blocks=re.findall(r'/\* latin \*/\s*(@font-face\s*\{[^}]+\})',css)
assert len(blocks)==3, 'Expected three Latin variable font blocks'
manifest=[];out=[]
for block in blocks:
 family=re.search(r"font-family:\s*'([^']+)'",block).group(1)
 remote=re.search(r'url\(([^)]+)\)',block).group(1)
 assert 'woff2' in block
 name=family.lower()+'-latin.woff2'; data=get(remote);(OUT/name).write_bytes(data)
 out.append(block.replace(remote,'/assets/chemical/'+name))
 manifest.append({'family':family,'file':name,'bytes':len(data),'source':remote})
(OUT/'fonts.css').write_text('\n'.join(out),encoding='utf-8')
(ROOT/'docs/chemical-build/font-sources.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Three variable WOFF2 fonts,',sum(x['bytes'] for x in manifest),'bytes total.')
