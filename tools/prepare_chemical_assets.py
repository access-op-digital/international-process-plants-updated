"""Fetch public IPP source records and original assets; never changes live content."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from lxml import html
import json, re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/chemical-build/sources'
ASSETS = ROOT / 'assets/chemical'
ASSETS.mkdir(parents=True, exist_ok=True)
UA = 'Mozilla/5.0'
def get(url):
    with urlopen(Request(url, headers={'User-Agent': UA}), timeout=60) as r:
        return r.read(), r.headers.get('Content-Type', ''), r.geturl()

selected = {
    '603031': ('plants', 'Formaldehyde production plant', 'Chemical & specialty'),
    '603016': ('plants', 'Sodium metabisulfite plant', 'Chemical & specialty'),
    '603039': ('plants', 'Nitric acid plant', 'Fertilizer'),
    '603040': ('plants', 'Ammonium nitrate plant', 'Fertilizer'),
    '601610': ('plants', 'Methanol production plant', 'Petrochemical'),
    '601813': ('plants', 'API manufacturing site', 'Pharmaceutical'),
    '242492': ('equipment', 'Sinclair stainless steel reactor', 'Reactors'),
    '232498': ('equipment', 'Gale Process Solutions new reactor', 'Reactors'),
    '242533': ('equipment', 'Graham Hart shell-and-tube heat exchanger', 'Heat exchangers'),
    '235730': ('equipment', 'Krauss Maffei peeler centrifuge', 'Centrifuges'),
    '238212': ('equipment', 'APV Anhydro spray dryer', 'Dryers'),
    '225365': ('equipment', 'Perrin filter press', 'Filters'),
    '211545': ('equipment', 'Estrella glass-lined packed column', 'Distillation columns'),
    '242886': ('equipment', 'Cookson & Zinn stainless steel tank', 'Tanks'),
}
records = {}
for file in SOURCE.glob('inventory-*.json'):
    for row in json.loads(file.read_text(encoding='utf-8')):
        key = row['url'].rstrip('/').split('/')[-1]
        if key in selected:
            records[key] = row
# The current reactor reference includes an additional verified IMS detail URL.
ref = html.fromstring((SOURCE/'reactor-reference.html').read_text(encoding='utf-8'))
for key in selected.keys() - records.keys():
    links = ref.xpath('//a[contains(@href,"'+key+'")]')
    if links:
        records[key] = {'url': links[0].get('href'), 'attributes': {}, 'source': 'https://internationalprocessplants.com/process-equipment/reactor/'}

def detail(item):
    key, row = item
    data, _, final = get(row['url'])
    (SOURCE/('detail-'+key+'.html')).write_bytes(data)
    doc = html.fromstring(data)
    for node in doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," attributeText ")]'):
        labels = node.xpath('.//*[contains(@class,"attributeLabel")]')
        values = node.xpath('.//*[contains(@class,"attributeValue")]')
        if labels and values:
            row['attributes'][' '.join(labels[0].text_content().split()).rstrip(':')] = ' '.join(values[0].text_content().split())
    row['detail_text'] = ' '.join(doc.text_content().split())
    row.update(dict(zip(['group','display_title','category'], selected[key])))
    row['id'] = key
    row['checked'] = '2026-10-07'
    row['url'] = final
    if not row.get('image'):
        imgs = doc.xpath('//img[contains(@src,"/productimage/")]')
        if imgs: row['image'] = urljoin(final, imgs[0].get('src'))
    if row.get('image'):
        img, typ, _ = get(row['image'])
        ext = '.png' if 'png' in typ else '.webp' if 'webp' in typ else '.jpg'
        rawpath = SOURCE/('image-'+key+ext)
        rawpath.write_bytes(img)
        row['original_asset'] = str(rawpath.relative_to(ROOT)).replace('\\','/')
        row['local_image'] = '/assets/chemical/'+key+'.webp'
    return row

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(detail, records.items()))
(ROOT/'docs/chemical-build/inventory-detail.json').write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
print('Inventory details fetched:', len(results))
for r in results: print(r['id'], r['attributes'])

home = html.fromstring((SOURCE/'home.html').read_text(encoding='utf-8'))
asset_names = {'shell.png':'Shell','sanofi.png':'Sanofi','lilly.png':'Lilly','DOW.png':'Dow','lonza.png':'Lonza','air-products.png':'Air Products','IPP-LOGO_DARKBLUE-FINAL-300x118.png':'International Process Plants'}
manifest = []
for name, alt in asset_names.items():
    imgs = home.xpath('//img[contains(@src,"'+name+'")]')
    if not imgs: continue
    url = imgs[0].get('src')
    raw, typ, _ = get(url)
    (ASSETS/name).write_bytes(raw)
    manifest.append({'file':name,'alt':alt,'source':url,'bytes':len(raw)})
(ROOT/'docs/chemical-build/asset-sources.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Brand assets:', len(manifest))
