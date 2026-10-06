"""Build the review-site homepage from existing equipment pages and Vercel routes."""
from pathlib import Path
from html import escape
from lxml import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CHEMICAL = '/chemical-process-plant-equipment-used-systems-for-sale/'
GROUPS = {
    'chemical-plants': ('Chemical process plants', 'Complete plants, process lines and individual chemical equipment.', 'plant'),
    'reactor': ('Reactors', 'Batch-type, fixed bed, fluid bed, hydrogenation and more.', 'vessel'),
    'heat-exchanger': ('Heat exchangers', 'Shell and tube, plate and frame, air cooled and other designs.', 'heat'),
    'centrifuge': ('Centrifuges', 'Basket, disc bowl, decanter and specialty centrifuge pages.', 'cycle'),
    'dryer': ('Dryers', 'Spray, rotary, vacuum, fluid bed and other dryer types.', 'heat'),
    'filter': ('Filters', 'Nutsche, pressure leaf, Rosenmund and Cogeim filters.', 'vessel'),
    'mixer': ('Mixers', 'Ribbon, paddle, planetary, Nauta and other mixer types.', 'cycle'),
    'agitators': ('Agitators', 'Drive agitators, glass-lined drive agitators, shafts and mixers.', 'cycle'),
    'evaporator': ('Evaporators', 'Flash, film and crystallizer evaporator pages.', 'vessel'),
    'mill': ('Mills', 'Ball, colloid, pebble, roll, bead and sand mills, plus pelletizers.', 'cycle'),
    'tank': ('Tanks', 'Explore the tank equipment overview.', 'vessel'),
    'glass-lined-parts': ('Glass-lined parts', 'Agitators, baffles, Cryo-Lock blades and Pro-Ring accessories.', 'vessel'),
    'boiler': ('Boilers', 'Explore the boiler equipment overview.', 'heat'),
    'chiller': ('Chillers', 'Explore the chiller equipment overview.', 'heat'),
    'fermenter': ('Fermenters', 'Explore the fermenter equipment overview.', 'vessel'),
    'homogenizer': ('Homogenizers', 'Explore the industrial homogenizer page.', 'cycle'),
    'incinerator': ('Incinerators', 'Incinerators and thermal oxidizers.', 'heat'),
    'kettle': ('Kettles', 'Steam-jacketed kettle equipment.', 'vessel'),
    'kiln': ('Kilns', 'Explore the rotary kiln page.', 'heat'),
    'pulverizer': ('Pulverizers', 'Explore the pulverizer equipment overview.', 'cycle'),
}
ICONS = {
    'plant': '<path d="M5 36V20l12-7v9l12-7v21M29 36V5h7l3 31M4 36h38M10 28h3m8 0h3m10-14h3m-3 7h4"/>',
    'vessel': '<path d="M12 12c0-7 22-7 22 0v21c0 7-22 7-22 0zM12 12c0 7 22 7 22 0M23 3v29m-6-5h12M15 37v6m16-6v6M5 19h7m22 9h7"/>',
    'heat': '<rect x="6" y="10" width="34" height="26" rx="3"/><path d="M13 10v26m7-26v26m7-26v26m7-26v26M1 18h5m34 10h5M14 4v6m18 26v6"/>',
    'cycle': '<circle cx="23" cy="23" r="16"/><path d="M23 7v10m0 12v10M7 23h10m12 0h10M12 12l7 7m9 9 6 6M12 34l7-7m9-9 6-6"/><circle cx="23" cy="23" r="6"/>',
}

config = json.loads((ROOT / 'vercel.json').read_text(encoding='utf-8'))
rewrites = {item['destination']: item['source'] for item in config.get('rewrites', []) if ':' not in item['source']}
catalog = {key: [] for key in GROUPS}
catalog['chemical-plants'].append({'title': 'Chemical process plants', 'url': CHEMICAL,
    'file': CHEMICAL.strip('/') + '/index.html', 'overview': True})

for page in sorted((ROOT / 'equipment').rglob('*.html')):
    relative = page.relative_to(ROOT).as_posix()
    parts = page.relative_to(ROOT / 'equipment').parts
    if len(parts) < 2:
        continue  # The equipment overview is linked separately.
    group = parts[0]
    if group not in catalog:
        raise ValueError(f'Add a display name for the new equipment family: {group}')
    # The explicitly routed review edition is the current entry for this subtype.
    if relative == 'equipment/reactor/batch-type-agitated/index.html':
        continue
    document = html.fromstring(page.read_bytes())
    title = ' '.join(' '.join(document.xpath('//h1//text()')).split())
    title = re.sub(r'^Buy Used\s+', '', title)
    title = re.sub(r'\s+(for Sale|Sourced to Specification)$', '', title)
    title = title.replace('Glass Lined', 'Glass-Lined')
    route = rewrites.get('/' + relative)
    if not route:
        route = '/' + relative[:-10] if page.name == 'index.html' else '/' + relative
    catalog[group].append({'title': title, 'url': route, 'file': relative,
        'overview': len(parts) == 2 and (group != 'agitators' or page.name == 'buy-used-agitators.html')})

cards = []
manifest = []
options = []
for key, (name, description, icon) in GROUPS.items():
    pages = catalog[key]
    overview = next(page for page in pages if page['overview'])
    types = sorted((page for page in pages if not page['overview']), key=lambda page: page['title'])
    options.append(f'<option value="{key}">{escape(name)}</option>')
    rows = ''.join(f'<li data-page-title="{escape(page["title"].lower(), quote=True)}"><a href="{escape(page["url"], quote=True)}">{escape(page["title"])}<span aria-hidden="true">↗</span></a></li>' for page in types)
    details = f'<details><summary>Browse {len(types)} equipment types<span class="disclosure" aria-hidden="true">+</span></summary><ul>{rows}</ul></details>' if types else '<p class="single-page">Category overview</p>'
    noun = 'page' if len(pages) == 1 else 'pages'
    cards.append(f'''<article class="family" data-category="{key}" data-family-name="{escape(name.lower(), quote=True)}">
      <div class="family-meta"><svg viewBox="0 0 46 46" aria-hidden="true">{ICONS[icon]}</svg><span>{len(pages)} {noun}</span></div>
      <h3><a href="{escape(overview['url'], quote=True)}">{escape(name)}<span aria-hidden="true">↗</span></a></h3>
      <p class="family-description">{escape(description)}</p>{details}
    </article>''')
    manifest.extend({'category': key, **page} for page in pages)

page_count = len(manifest)
values = {'CARDS': '\n'.join(cards), 'OPTIONS': '\n'.join(options), 'PAGE_COUNT': str(page_count),
          'FAMILY_COUNT': str(len(GROUPS)), 'EQUIPMENT_FAMILIES': str(len(GROUPS) - 1)}
template = (ROOT / 'src/hub-page.html').read_text(encoding='utf-8')
for key, value in values.items():
    template = template.replace('{{' + key + '}}', value)
if re.search(r'\{\{[A-Z_]+\}\}', template):
    raise ValueError('Unfilled hub template placeholder')
(ROOT / 'index.html').write_text(template, encoding='utf-8')
out = ROOT / 'docs/hub'
out.mkdir(parents=True, exist_ok=True)
(out / 'route-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(f'Built the homepage hub: {page_count} page entries in {len(GROUPS)} categories.')
