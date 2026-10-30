"""Build the IPP case-study review pages: a hub and six project pages, plus a fact-check list in docs/.

Sources: the IPP corporate overview deck (Presentation2.pdf, slides 7-13) and the live
https://internationalprocessplants.com/case-studies/ page. Every figure below appears in one
of the two; where they differ, the pages use the deck's wording. Open questions go to
docs/case-studies-fact-check.md, which is not deployed.
"""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'case-studies'
LIVE = 'https://internationalprocessplants.com'
CHEM_SRC = (ROOT / 'src' / 'chemical-page.html').read_text(encoding='utf-8')
HEADER = re.search(r'<header class="site-header">.*?</header>', CHEM_SRC, re.S).group(0)
FOOTER = re.search(r'<footer class="site-footer">.*?</footer>', CHEM_SRC, re.S).group(0)

CTA = {
    'sell_plant': ('Have an idle plant?',
                   'IPP buys closed and idle plants, including the real estate, buildings and production systems, '
                   'and can take on the environmental liabilities that come with the site.',
                   ('Sell your plant to IPP', f'{LIVE}/sell-plants/'), ('Contact IPP', f'{LIVE}/contact/')),
    'buy_plant': ('Looking for a complete plant or process unit?',
                  'IPP offers complete process plants and process lines for relocation, with IPP handling '
                  'dismantling and shipping.',
                  ('Browse IPP plants', f'{LIVE}/plants/'), ('Contact IPP', f'{LIVE}/contact/')),
    'clear_site': ('Need to clear a shut-down unit from your site?',
                   'IPP buys shut-down process units and complete plants, and offers them for relocation.',
                   ('Sell your plant to IPP', f'{LIVE}/sell-plants/'), ('Contact IPP', f'{LIVE}/contact/')),
}

CASES = [
    {
        'slug': 'pet-plant-darlington-sc',
        'card': 'PET plant',
        'h1': 'PET Plant Repurposing, Darlington, SC',
        'title': 'PET Plant Repurposing Case Study, Darlington, SC | IPP',
        'desc': 'IPP bought a 760-acre PET plant in Darlington, SC, took over $300,000+ monthly carrying costs and environmental obligations, and announced a 2016 restart.',
        'standfirst': 'A polyester fiber and PET resin site that cost its owner more than $300,000 a month to '
                      'hold was set for a restart after IPP bought it.',
        'img': 'pet-plant-darlington-sc.jpg',
        'alt': 'PET resin and polyester fiber plant in Darlington, South Carolina',
        'cta': 'sell_plant',
        'stats': [('$300,000+', 'Monthly carrying cost taken over'), ('760 acres', 'Site area'),
                  ('2016', 'Restart announced'), ('250+', 'Jobs expected')],
        'summary': [('Industry', 'Polyester fiber and PET resin'),
                    ('Location', 'Darlington, South Carolina, USA'),
                    ('Capacity', '550 million lb PET bottle resin; 250 million lb amorphous PET resin'),
                    ('IPP’s role', 'Bought the site, took over its carrying costs and environmental obligations'),
                    ('Result', 'Restart announced in 2016, expected to create at least 250 jobs')],
        'challenge': [
            'The Darlington site combined polyester fiber production with two resin lines: 550 million pounds '
            'of capacity for PET bottle resin and 250 million pounds for amorphous PET resin. The property covers '
            '760 acres, with 1.1 million square feet of covered manufacturing space and 100 acres inside the fence.',
            'Holding the site cost the owner more than $300,000 every month, and the land carried environmental '
            'obligations on top of that cost.',
        ],
        'solution': [
            'IPP purchased the property and took over the carrying costs from the owner. The purchase moved the '
            'site’s environmental obligations to IPP as well, so the seller exited both the monthly expense '
            'and the cleanup exposure.',
            'The restart plan built on the existing site infrastructure, local skilled labor and modernizations '
            'to improve efficiency.',
        ],
        'results': [
            'In 2016, IPP announced that the plant would restart as a fiber manufacturing facility to serve '
            'specialty industrial and healthcare demand for high-quality polyester fiber. The project was '
            'expected to create at least 250 jobs and bring a new, low-cost domestic supplier of polyester '
            'fiber to the market.',
        ],
        'units': None,
        'takeaway': 'An idle site keeps costing money every month. Selling the complete property to IPP, '
                    'environmental obligations included, ended those costs for the owner and set the plant up for '
                    'a restart.',
    },
    {
        'slug': 'mibk-solvent-plant-deer-park-tx',
        'card': 'MIBK solvent plant',
        'h1': 'MIBK Solvent Plant Relocation, Deer Park, TX to India',
        'title': 'MIBK Plant Relocation Case Study: Texas to India | IPP',
        'desc': 'IPP removed a 208 million lb/yr solvents complex from an operating Texas refinery and managed its dismantling and shipping for reinstallation in India.',
        'standfirst': 'A four-unit solvents complex left an operating refinery in Texas and now runs in '
                      'southeastern India.',
        'img': 'mibk-solvent-plant-deer-park-tx.jpg',
        'alt': 'MIBK solvent plant distillation columns in Deer Park, Texas',
        'cta': 'buy_plant',
        'stats': [('208M lb/yr', 'Complex capacity'), ('4', 'Production units'),
                  ('Texas to India', 'Relocation route')],
        'summary': [('Industry', 'Industrial solvents'),
                    ('Location', 'Deer Park, Texas, USA; reinstalled in southeastern India'),
                    ('Capacity', '208 million lb/yr M&H plant complex'),
                    ('IPP’s role', 'Bought and removed the facility, sold it, managed dismantling and shipping'),
                    ('Result', 'Reinstalled in southeastern India, now the only MIBK plant operating in the country')],
        'challenge': [
            'IPP agreed to purchase and remove a solvents facility from a refinery complex in Deer Park, Texas. '
            'The facility was a 208 million lb/yr M&H plant complex built from four units.',
            'Its equipment was intertwined with several units that stayed in operation, so the dismantling had to '
            'happen inside a working refinery.',
        ],
        'solution': [
            'After several months of evaluation and feasibility studies, IPP sold the M&H plant to an IPP '
            'customer for relocation to India and took responsibility for dismantling and shipping.',
            'IPP and its contractors worked under the refinery’s Environmental Health and Safety policies, '
            'which were stricter because of the live units around the equipment. The dismantling was surgical, '
            'to protect those operating units.',
        ],
        'results': [
            'The plant has been reinstalled in southeastern India. IPP reports that it is now the only MIBK plant '
            'in operation in the country.',
        ],
        'units': ('Units in the M&H plant complex', [
            'Methyl isobutyl carbinol (MIBC): 78 million lb/yr',
            'Methyl isobutyl ketone (MIBK): 78 million lb/yr',
            'Di-acetone alcohol (DAA): 34 million lb/yr',
            'Hexylene glycol (HG): 18 million lb/yr']),
        'takeaway': 'A process unit can leave an operating site without shutting down the units around it. '
                    'The MIBK project moved a complete complex out of a live refinery and into production on '
                    'another continent.',
    },
    {
        'slug': 'synthetic-chemical-site-kirkby-uk',
        'card': 'Synthetic chemical complex',
        'h1': 'Synthetic Chemical Site Repurposing, Kirkby, UK',
        'title': 'Synthetic Chemical Site Case Study: Kirkby, UK | IPP',
        'desc': 'IPP bought a 400,000 sq ft synthetic chemicals complex in Kirkby, UK, took on its environmental liability and turned the site into Knowsley Industrial Park.',
        'standfirst': 'A photographic chemicals complex closed in a bankruptcy restructuring became a '
                      'multi-tenant industrial park.',
        'img': 'synthetic-chemical-site-kirkby-uk.jpg',
        'alt': 'Aerial view of the synthetic chemical site at Knowsley Industrial Park, Kirkby, UK',
        'cta': 'sell_plant',
        'stats': [('400,000 sq ft', 'Chemicals and engineering complex'), ('1st', 'Environmental liability transfer in UK history'),
                  ('~250', 'People employed on site')],
        'summary': [('Industry', 'Synthetic photographic chemicals'),
                    ('Location', 'Kirkby, Knowsley, UK'),
                    ('Site', '400,000 sq ft chemicals and engineering complex'),
                    ('IPP’s role', 'Bought the complex and took on its environmental liability'),
                    ('Result', 'Knowsley Industrial Park, employing approximately 250 people')],
        'challenge': [
            'A bankruptcy restructuring required the owner of a 400,000 sq ft synthetic photographic chemicals '
            'and engineering complex to close and sell it quickly. The complex had employed nearly 500 people, '
            'and 100 remained at the time of shutdown.',
            'Digital photography had also changed the synthetic photographic chemicals business dramatically.',
        ],
        'solution': [
            'IPP purchased the complex and took on its environmental liability. IPP reports this as the first '
            'environmental liability transfer in the history of the United Kingdom, and it absolved the '
            'restructuring company of further responsibility for environmental cleanup.',
            'The site’s flexible unit operations were then put to new use, and IPP created an active '
            'industrial business park on the site.',
        ],
        'results': [
            'The site now operates as Knowsley Industrial Park. Tenants run new and existing units there, and the '
            'park employs approximately 250 people. Growth plans at the time pointed to approximately 200 '
            'additional jobs.',
        ],
        'units': ('Units operated by park tenants', [
            'Solvent recovery plant', 'Silver recovery plant', 'Pilot plant']),
        'takeaway': 'A restructuring seller needs a clean exit fast. Taking on the environmental liability let the '
                    'seller walk away, and the site’s unit operations found new tenants instead of standing idle.',
    },
    {
        'slug': 'methanol-plant-brazil-to-west-virginia',
        'card': 'Methanol plant',
        'h1': 'Methanol Plant Relocation, Brazil to West Virginia',
        'title': 'Methanol Plant Relocation Case Study: Brazil to US | IPP',
        'desc': 'IPP bought a 750 ton/day methanol plant idled by gas costs in Brazil and relocated it for re-erection in West Virginia to supply a major methanol consumer.',
        'standfirst': 'A methanol plant idled by high gas costs in Brazil was dismantled and relocated for '
                      're-erection in West Virginia.',
        'img': 'methanol-plant-brazil.jpg',
        'alt': 'Methanol plant distillation columns in Brazil before relocation',
        'cta': 'buy_plant',
        'stats': [('750 tons/day', 'Methanol capacity'), ('Brazil to USA', 'Relocation route'),
                  ('Over-the-fence', 'Planned supply to a major consumer')],
        'summary': [('Industry', 'Methanol'),
                    ('Location', 'Brazil; relocated to West Virginia, USA'),
                    ('Capacity', '750 tons/day'),
                    ('IPP’s role', 'Bought the idle plant, marketed it to US buyers, dismantled and relocated it'),
                    ('Result', 'Being re-erected in West Virginia to supply methanol over-the-fence to a major consumer')],
        'challenge': [
            'A methanol plant in Brazil had just completed a turnaround that raised its maximum capacity to '
            '750 tons/day. High natural gas costs in Brazil then forced the plant to shut down, leaving the '
            'recently upgraded unit idle.',
        ],
        'solution': [
            'IPP purchased the plant. Knowing that the US natural gas market was attractive for methanol '
            'production, IPP marketed it to companies and investors in the United States.',
            'The plant was then dismantled in Brazil and relocated to West Virginia for re-erection.',
        ],
        'results': [
            'The plant is being re-erected in West Virginia, where it will provide methanol over-the-fence to a '
            'major consumer. The arrangement lets the company produce methanol locally with low-cost gas and '
            'avoid expensive freight charges.',
        ],
        'units': None,
        'takeaway': 'A plant that cannot compete on feedstock cost in one country can compete in another. '
                    'IPP marketed this unit in the United States, where natural gas was attractive for methanol '
                    'production.',
    },
    {
        'slug': 'nitric-acid-plant-pasadena-tx',
        'card': 'Nitric acid plant',
        'h1': 'Nitric Acid Plant Relocation, Pasadena, TX to India',
        'title': 'Nitric Acid Plant Relocation Case Study, Pasadena | IPP',
        'desc': 'IPP bought a 500 ton/day nitric acid plant in Pasadena, TX to free space for new installations and sold it to a manufacturer for relocation to India.',
        'standfirst': 'A shut-down nitric acid plant made room for new installations in Texas and was sold to be '
                      'relocated to India.',
        'img': 'nitric-acid-plant-pasadena-tx.jpg',
        'alt': 'Nitric acid plant piping and process structure in Pasadena, Texas',
        'cta': 'clear_site',
        'stats': [('500 tons/day', 'Rated capacity'), ('65%', 'Nitric acid concentration'),
                  ('300 tons/day', 'Turn-down capability')],
        'summary': [('Industry', 'Industrial chemicals (nitric acid)'),
                    ('Location', 'Pasadena, Texas, USA; sold for relocation to India'),
                    ('Capacity', '500 tons/day of 65% nitric acid, turn-down to 300 tons/day'),
                    ('IPP’s role', 'Bought the shut-down plant to clear the site, then resold it'),
                    ('Result', 'Sold to a major global nitric acid manufacturer for relocation to India')],
        'challenge': [
            'The previous owner of a nitric acid plant in Pasadena, Texas, exited the nitric acid business and '
            'shut the plant down. The site needed the space for new installations.',
            'The plant was rated for 500 tons/day of 65% concentrated nitric acid, with turn-down capability as '
            'low as 300 tons/day.',
        ],
        'solution': [
            'IPP purchased the plant to make room for the new installations at the site. The plant was then offered as a '
            'complete unit for relocation.',
        ],
        'results': [
            'IPP sold the plant to a major global nitric acid manufacturer, to be relocated to India.',
        ],
        'units': None,
        'takeaway': 'A shut-down unit can leave a site as a complete plant. Selling it for relocation freed '
                    'the space for new installations and placed the plant with a nitric acid manufacturer.',
    },
    {
        'slug': 'oleochemical-plant-bromborough-uk',
        'card': 'Oleochemical plant',
        'h1': 'Oleochemical Plant Relocation, Bromborough, UK',
        'title': 'Oleochemical Plant Relocation Case Study, Bromborough | IPP',
        'desc': 'IPP bought a 30-acre oleochemical site in Bromborough, UK, moved its units to Germany and the USA and turned the land into a mixed-use waterfront development.',
        'standfirst': 'One site, two exits: the process units moved to Germany and the USA, and the land became a '
                      'waterfront development.',
        'img': 'oleochemical-plant-bromborough-uk.jpg',
        'alt': 'Oleochemical plant distillation columns in Bromborough, UK',
        'cta': 'sell_plant',
        'stats': [('30 acres', 'Fatty acids facility'), ('2 countries', 'Germany and the USA'),
                  ('2016', 'Planning & Placemaking Awards winner')],
        'summary': [('Industry', 'Oleochemicals'),
                    ('Location', 'Bromborough, UK'),
                    ('Site', '30-acre fatty acids facility'),
                    ('IPP’s role', 'Bought the site, took on carry costs and environmental liabilities, relocated the units'),
                    ('Result', 'Units relocated to Germany and the USA; site converted into an award-winning waterfront development')],
        'challenge': [
            'A 30-acre fatty acids facility in Bromborough held esters, sorbitan, triacetin and glycerin '
            'purification plants. Feedstock for the oleochemicals industry comes mostly from Southeast Asia, so '
            'the plant was no longer viable to operate in the UK.',
        ],
        'solution': [
            'IPP purchased the facility and took over all carry costs and environmental liabilities. The process units '
            'were relocated to Germany and the USA.',
            'With the units gone, IPP converted the site into a mixed-use commercial and residential waterfront '
            'development.',
        ],
        'results': [
            'The redevelopment won at The Planning & Placemaking Awards 2016. Combining existing, repurposed '
            'structures with new improvements, the site is becoming a place to live and work, with offices, '
            'homes and public riverfront space.',
        ],
        'units': ('Plants on the original site', [
            'Esters plant', 'Sorbitan plant', 'Triacetin plant', 'Glycerin purification plant']),
        'takeaway': 'When a plant cannot run where it stands, its units and its land can each find a new use. '
                    'IPP moved the equipment to where it could operate and redeveloped the site it left behind.',
    },
]

# Review-only notes: where each fact comes from and what IPP still has to confirm.
REVIEW = {
    'pet-plant-darlington-sc': {
        'sources': 'Deck slide 7; live /case-studies/ PET tab.',
        'open': [
            'Restart: the deck says IPP "announced" a restart in 2016 and the jobs were "expected"; the live page says the plant '
            'was restarted in 2016 and "created at least 250 jobs". The page follows the deck. If IPP confirms the restart, '
            'switch the page, hub and meta to past tense.',
            'Carrying cost: deck "over $300,000 per month", live "$300,000/month". Page uses "more than $300,000".',
            'Capacity basis: neither source gives a time unit for 550M lb / 250M lb. Pounds per year?',
            'The live page says "low-cost cosmetic supplier"; the deck says "domestic". Page uses "domestic".',
            'Year IPP bought the site, and who operates it now: not stated.',
        ],
    },
    'mibk-solvent-plant-deer-park-tx': {
        'sources': 'Deck slide 12; live /case-studies/ MIBK tab.',
        'open': [
            '"Only MIBK plant in operation in India": published by IPP on both. Confirm it is still true.',
            'Project year and timeline from agreement to reinstallation: not stated.',
            'Refinery and buyer names: not stated, left out.',
            'Deck phrase "World Class Texas Refinery Complex" dropped as hype.',
        ],
    },
    'synthetic-chemical-site-kirkby-uk': {
        'sources': 'Deck slide 8; live /case-studies/ Synthetic Chemical tab.',
        'open': [
            'Seller: the deck names Kodak; the live page does not. Page leaves the seller unnamed until IPP confirms.',
            'Location: the deck title says Liverpool, the text says Kirkby and Knowsley Industrial Park. Page uses Kirkby, Knowsley.',
            'Employees: deck "nearly 500", live "500". Park jobs: deck "approx. 250", live "250+". Page follows the deck: '
            '"nearly 500" and "approximately 250".',
            '"First environmental liability transfer in UK history": published by IPP on both, written as an IPP report. Source?',
            'The 200 additional jobs come from growth plans at the time; the page says so. Did they happen? Year of purchase?',
        ],
    },
    'methanol-plant-brazil-to-west-virginia': {
        'sources': 'Deck slide 11; live /case-studies/ Methanol tab.',
        'open': [
            'Outcome: the deck says "currently being re-erected"; the live page says it was re-erected and "continues to provide '
            'methanol". The page follows the deck ("is being re-erected", "will provide"). If IPP confirms it is running, '
            'switch to past tense.',
            'City: the deck heading says Rio de Janeiro; both texts say only Brazil. Page uses Brazil.',
            'Year, buyer and consumer names: not stated.',
        ],
    },
    'nitric-acid-plant-pasadena-tx': {
        'sources': 'Deck slide 13 only (not on the live case-studies page).',
        'open': [
            'Was the plant reinstalled in India, and is it running? The page says only "sold, to be relocated to India".',
            'The CTA no longer says sellers avoid demolition costs; add it back only if IPP approves that line.',
            'Whose "new installations" needed the space: the seller’s own expansion?',
            'Year, seller and buyer names: not stated.',
            'Thin source: about 90 words on the slide, so the page stays short.',
        ],
    },
    'oleochemical-plant-bromborough-uk': {
        'sources': 'Deck slide 9 only (not on the live case-studies page).',
        'open': [
            'Award: the slide shows a "Planning & Placemaking Awards 2016 Winner" badge. Which category, and who received it?',
            'Which units went to Germany and which to the USA?',
            'Status of the waterfront development today ("is becoming" in the deck).',
            'Year, seller and capacities: not stated.',
        ],
    },
}

GLOBAL_OPEN = [
    'Where these pages will live on internationalprocessplants.com (the live /case-studies/ page is one tabbed page with 4 of these projects).',
    'Equipment links: the deck names no equipment for PET, Methanol or Nitric acid, so no equipment or listing links were added. '
    'Each page links to IPP’s plants or sell pages and to the other case studies.',
    'Photos are cropped from the corporate deck slides. Ask IPP for the original files and confirm they can be published.',
    'This list is internal: it is not deployed to Vercel and must not be migrated to WordPress.',
    'Savings figures were left out: the deck says 60% in one place and 30-50% / 50-60% in another, and the live page says 50%.',
]


def schema(c):
    url = f'{LIVE}/case-studies/{c["slug"]}/'
    return json.dumps({'@context': 'https://schema.org', '@graph': [
        {'@type': 'Article', 'headline': c['h1'], 'description': c['desc'], 'url': url,
         'image': f'{LIVE}/assets/case-studies/{c["img"]}',
         'author': {'@type': 'Organization', 'name': 'International Process Plants'},
         'publisher': {'@type': 'Organization', 'name': 'International Process Plants', 'url': LIVE}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': f'{LIVE}/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Case studies', 'item': f'{LIVE}/case-studies/'},
            {'@type': 'ListItem', 'position': 3, 'name': c['h1'], 'item': url}]}]}, ensure_ascii=False)


def page(title, desc, canonical, body, extra_head=''):
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}">
  <meta name="robots" content="noindex, nofollow">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="International Process Plants">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(desc)}">
  <link rel="stylesheet" href="/assets/chemical/fonts.css">
  <link rel="stylesheet" href="/assets/chemical/page.css">
  <link rel="stylesheet" href="/assets/case-studies/case.css">
  {extra_head}
  <script>document.documentElement.classList.add('js')</script>
</head>
<body class="cs-page">
<a class="skip-link" href="#main">Skip to content</a>
{HEADER}
<main id="main">
{body}
</main>
{FOOTER}
<script>
(function(){{var b=document.getElementById('menu-toggle'),n=document.getElementById('main-nav');if(!b||!n)return;b.hidden=false;
b.addEventListener('click',function(){{var o=n.classList.toggle('is-open');b.setAttribute('aria-expanded',o)}})}})();
</script>
</body>
</html>
'''


def crumbs(*items):
    parts = [f'<a href="{LIVE}/">Home</a>']
    for label, href in items:
        parts.append('<span aria-hidden="true">/</span>')
        parts.append(f'<a href="{href}">{escape(label)}</a>' if href else f'<span aria-current="page">{escape(label)}</span>')
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>'


def paras(items):
    return ''.join(f'<p>{escape(p)}</p>' for p in items)


def case_page(c):
    stats = ''.join(f'<li><strong>{escape(v)}</strong><span>{escape(k)}</span></li>' for v, k in c['stats'])
    summary = ''.join(f'<div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>' for k, v in c['summary'])
    units = ''
    if c['units']:
        head, items = c['units']
        units = (f'<section class="cs-block"><h2>{escape(head)}</h2><ul class="cs-units">'
                 + ''.join(f'<li>{escape(i)}</li>' for i in items) + '</ul></section>')
    h2, text, primary, secondary = CTA[c['cta']]
    related = ''.join(
        f'<a class="cs-related-card" href="/case-studies/{o["slug"]}/"><span>{escape(o["card"])}</span>'
        f'<strong>{escape(o["summary"][-1][1])}</strong></a>'
        for o in CASES if o is not c)
    body = f'''<section class="cs-hero">
  <div class="container">
    {crumbs(('Case studies', '/case-studies/'), (c['card'], None))}
    <div class="cs-hero-grid">
      <div>
        <h1>{escape(c['h1'])}</h1>
        <p class="cs-standfirst">{escape(c['standfirst'])}</p>
      </div>
      <figure class="cs-hero-photo"><img src="/assets/case-studies/{c['img']}" alt="{escape(c['alt'])}" width="640" height="440"></figure>
    </div>
    <ul class="cs-stats" aria-label="Project results">{stats}</ul>
  </div>
</section>
<div class="container cs-layout">
  <article class="cs-body">
    <section class="cs-block"><h2>The challenge</h2>{paras(c['challenge'])}</section>
    <section class="cs-block"><h2>IPP’s solution</h2>{paras(c['solution'])}</section>
    <section class="cs-block"><h2>The results</h2>{paras(c['results'])}</section>
    {units}
    <section class="cs-block cs-takeaway"><h2>What this means for plant owners</h2><p>{escape(c['takeaway'])}</p></section>
  </article>
  <aside class="cs-summary" aria-label="Project summary">
    <h2>Project summary</h2>
    <dl>{summary}</dl>
  </aside>
</div>
<section class="cs-cta">
  <div class="container cs-cta-inner">
    <div><h2>{escape(h2)}</h2><p>{escape(text)}</p></div>
    <div class="cs-cta-buttons"><a class="cs-button" href="{primary[1]}">{escape(primary[0])} <span aria-hidden="true">→</span></a><a class="cs-button cs-button-outline" href="{secondary[1]}">{escape(secondary[0])}</a></div>
  </div>
</section>
<section class="cs-related">
  <div class="container"><h2>More IPP case studies</h2><div class="cs-related-grid">{related}</div></div>
</section>'''
    return page(c['title'], c['desc'], f'{LIVE}/case-studies/{c["slug"]}/', body,
                f'<script type="application/ld+json">{schema(c)}</script>')


def hub_page():
    cards = ''.join(f'''<a class="cs-card" href="/case-studies/{c['slug']}/">
  <img src="/assets/case-studies/{c['img']}" alt="{escape(c['alt'])}" loading="lazy" width="400" height="260">
  <div><span class="cs-card-label">{escape(c['card'])} · {escape(c['summary'][1][1])}</span>
  <h2>{escape(c['h1'])}</h2><p>{escape(c['summary'][-1][1])}</p>
  <ul>{''.join(f'<li><strong>{escape(v)}</strong> {escape(k)}</li>' for v, k in c['stats'][:2])}</ul></div></a>''' for c in CASES)
    body = f'''<section class="cs-hero cs-hero-hub">
  <div class="container">
    {crumbs(('Case studies', None))}
    <h1>IPP Case Studies</h1>
    <p class="cs-standfirst">Six projects where International Process Plants bought an idle plant, a process unit or a complete site, and found it a new use: a planned restart, a relocation or a new industrial park.</p>
  </div>
</section>
<section class="cs-hub"><div class="container cs-card-grid">{cards}</div></section>
<section class="cs-cta">
  <div class="container cs-cta-inner">
    <div><h2>{escape(CTA['sell_plant'][0])}</h2><p>{escape(CTA['sell_plant'][1])}</p></div>
    <div class="cs-cta-buttons"><a class="cs-button" href="{LIVE}/sell-plants/">Sell your plant to IPP <span aria-hidden="true">→</span></a><a class="cs-button cs-button-outline" href="{LIVE}/plants/">Browse IPP plants</a></div>
  </div>
</section>'''
    return page('IPP Case Studies: Plant Repurposing and Relocation | IPP',
                'Six IPP case studies: idle plants bought, repurposed or relocated, from a PET plant in South Carolina '
                'to a methanol plant moved from Brazil to West Virginia.',
                f'{LIVE}/case-studies/', body)


def fact_check_md():
    lines = ['# IPP case studies: fact check', '',
             'Internal list, not for publishing. The drafts use figures from the IPP corporate deck and the live '
             'case-studies page; where they differ, the pages follow the deck. IPP should confirm these points '
             'before the pages go live.', '', '## All pages', '']
    lines += [f'- {i}' for i in GLOBAL_OPEN]
    for c in CASES:
        lines += ['', f'## {c["h1"]}', '', f'Page: /case-studies/{c["slug"]}/', '',
                  f'Sources: {REVIEW[c["slug"]]["sources"]}', '']
        lines += [f'- {i}' for i in REVIEW[c['slug']]['open']]
    return '\n'.join(lines) + '\n'


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / 'index.html').write_text(hub_page(), encoding='utf-8')
    (ROOT / 'docs' / 'case-studies-fact-check.md').write_text(fact_check_md(), encoding='utf-8')
    for c in CASES:
        d = OUT / c['slug']
        d.mkdir(exist_ok=True)
        (d / 'index.html').write_text(case_page(c), encoding='utf-8')
        words = sum(len(t.split()) for k in ('challenge', 'solution', 'results') for t in c[k]) + len(c['takeaway'].split())
        print(f'{c["slug"]}: title {len(c["title"])}, desc {len(c["desc"])}, body words {words}')


if __name__ == '__main__':
    main()
