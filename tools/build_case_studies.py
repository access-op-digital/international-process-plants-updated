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
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'case-studies'
LIVE = 'https://internationalprocessplants.com'
REVIEW_SITE = 'https://international-process-plants-update-one.vercel.app'
sys.path.insert(0, str(ROOT / 'tools'))
from live_site_chrome import header_html, footer_html, MENU_SCRIPT  # noqa: E402  (the live site's header and footer)
HEADER = header_html()
FOOTER = footer_html()

CTA = {
    'sell_plant': ('Have an idle plant?',
                   'IPP buys closed and idle plants, including the real estate, buildings and production systems, '
                   'and can take on the environmental liabilities that come with the site.',
                   ('Sell your plant to IPP', f'{LIVE}/sell-plants/'), ('Contact IPP', f'{LIVE}/contact/')),
    'buy_plant': ('Looking for a complete plant or process unit?',
                  'IPP offers complete process plants and process lines for relocation, and handles the '
                  'dismantling and shipping.',
                  ('Browse available plants', f'{LIVE}/plants/'), ('Contact IPP', f'{LIVE}/contact/')),
    'clear_site': ('Need to clear a shut-down unit from your site?',
                   'IPP buys shut-down process units and complete plants, and offers them for relocation.',
                   ('Sell your plant to IPP', f'{LIVE}/sell-plants/'), ('Contact IPP', f'{LIVE}/contact/')),
}

CASES = [
    {
        'slug': 'pet-plant-darlington-sc',
        'card': 'PET plant',
        'h1': 'How International Process Plants Saved a PET Plant Owner $300,000 a Month in Darlington, SC',
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
                    ('Result', 'Restart announced in 2016; it was expected to create at least 250 jobs')],
        'challenge': [
            'The Darlington site combined polyester fiber production with two resin lines: 550 million lb '
            'of capacity for PET bottle resin and 250 million lb for amorphous PET resin. The property covers '
            '760 acres, with 1.1 million sq ft of covered manufacturing space and 100 acres inside the fence.',
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
        'h1': 'How International Process Plants Relocated a Texas Refinery’s MIBK Solvent Plant to India',
        'title': 'MIBK Plant Relocation Case Study: Texas to India | IPP',
        'desc': 'IPP removed a 208 million lb/yr solvents complex from an operating Texas refinery and managed its dismantling and shipping for reinstallation in India.',
        'standfirst': 'A four-unit solvents complex left an operating refinery in Texas and now runs in '
                      'southeastern India.',
        'img': 'mibk-solvent-plant-deer-park-tx.jpg',
        'alt': 'MIBK solvent plant distillation columns in Deer Park, Texas',
        'cta': 'buy_plant',
        'stats': [('208 million lb/yr', 'Complex capacity'), ('4', 'Production units'),
                  ('Texas to India', 'Relocation route')],
        'summary': [('Industry', 'Industrial solvents'),
                    ('Location', 'Deer Park, Texas, USA; reinstalled in southeastern India'),
                    ('Capacity', '208 million lb/yr M&H Plant complex'),
                    ('IPP’s role', 'Bought and removed the facility, sold it, managed dismantling and shipping'),
                    ('Result', 'Reinstalled in southeastern India, now the only MIBK plant operating in the country')],
        'challenge': [
            'IPP agreed to purchase and remove a solvents facility from a world-class refinery complex in Deer Park, Texas. '
            'The facility was a 208 million lb/yr M&H Plant complex built from four units.',
            'Its equipment was intertwined with several units that stayed in operation, so the dismantling had to '
            'happen inside a working refinery.',
        ],
        'solution': [
            'After several months of evaluation and feasibility studies, IPP sold the M&H Plant to one of its '
            'customers for relocation to India and took responsibility for dismantling and shipping.',
            'IPP and its contractors worked under the refinery’s Environmental Health and Safety policies, '
            'which were stricter because of the live units around the equipment. The dismantling was surgical, '
            'to protect those operating units.',
        ],
        'results': [
            'The plant has been reinstalled in southeastern India. IPP reports that it is now the only MIBK plant '
            'in operation in the country.',
        ],
        'units': ('Units in the M&H Plant complex', [
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
        'h1': 'How International Process Plants Turned Kodak’s Kirkby Chemical Site into an Industrial Park',
        'title': 'Synthetic Chemical Site Case Study: Kirkby, UK | IPP',
        'desc': 'IPP bought Kodak’s 400,000 sq ft synthetic chemicals complex in Kirkby, UK, took on its environmental liability and turned it into Knowsley Industrial Park.',
        'standfirst': 'Kodak’s synthetic photographic chemicals complex, closed in a bankruptcy restructuring, '
                      'became a multi-tenant industrial park.',
        'img': 'synthetic-chemical-site-kirkby-uk.jpg',
        'alt': 'Aerial view of the former Kodak synthetic chemicals site, now Knowsley Industrial Park, Kirkby, UK',
        'cta': 'sell_plant',
        'stats': [('400,000 sq ft', 'Chemicals and engineering complex'), ('1st', 'Environmental liability transfer in UK history'),
                  ('~250', 'People employed on site')],
        'summary': [('Industry', 'Synthetic photographic chemicals'),
                    ('Location', 'Kirkby, near Liverpool, UK'),
                    ('Seller', 'Kodak, as part of its bankruptcy restructuring'),
                    ('Site', '400,000 sq ft chemicals and engineering complex'),
                    ('IPP’s role', 'Bought the complex and took on its environmental liability'),
                    ('Result', 'Knowsley Industrial Park, employing approximately 250 people')],
        'challenge': [
            'As part of its bankruptcy restructuring, Kodak needed to close and sell its 400,000 sq ft synthetic '
            'photographic chemicals and engineering complex in Kirkby, near Liverpool, quickly. The complex had '
            'employed nearly 500 people, and 100 remained at the time of shutdown.',
            'Digital photography had also changed the synthetic photographic chemicals business dramatically.',
        ],
        'solution': [
            'IPP purchased the complex and took on its environmental liability. IPP reports this as the first '
            'environmental liability transfer in the history of the United Kingdom, and it absolved Kodak of '
            'further responsibility for environmental cleanup.',
            'The site’s flexible and profitable unit operations were then put to new use, and IPP created an active '
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
        'h1': 'How International Process Plants Moved an Idled Methanol Plant from Brazil to West Virginia',
        'title': 'Methanol Plant Relocation Case Study: Brazil to US | IPP',
        'desc': 'IPP bought a 750 tons/day methanol plant idled by gas costs in Brazil and relocated it for re-erection in West Virginia to supply a major methanol consumer.',
        'standfirst': 'A methanol plant idled by high gas costs in Brazil was dismantled and relocated for '
                      're-erection in West Virginia.',
        'img': 'methanol-plant-brazil.jpg',
        'alt': 'Methanol plant distillation columns in Brazil before relocation',
        'cta': 'buy_plant',
        'stats': [('750 tons/day', 'Methanol capacity'), ('Brazil to USA', 'Relocation route'),
                  ('Over-the-fence', 'Planned supply to a major consumer')],
        'summary': [('Industry', 'Methanol'),
                    ('Location', 'Rio de Janeiro, Brazil; relocated to West Virginia, USA'),
                    ('Capacity', '750 tons/day'),
                    ('IPP’s role', 'Bought the idle plant, marketed it to US buyers, dismantled and relocated it'),
                    ('Result', 'Relocated for re-erection in West Virginia to supply methanol over-the-fence to a major consumer')],
        'challenge': [
            'A methanol plant in Rio de Janeiro, Brazil, had just completed a turnaround that raised its maximum capacity to '
            '750 tons/day. High natural gas costs in Brazil then forced the plant to shut down, leaving the '
            'recently upgraded unit idle.',
        ],
        'solution': [
            'IPP purchased the plant. Knowing that the US natural gas market was attractive for methanol '
            'production, IPP marketed it to companies and investors in the United States.',
            'The plant was then dismantled in Brazil and relocated to West Virginia for re-erection.',
        ],
        'results': [
            'The plant was being re-erected in West Virginia to provide methanol over-the-fence to a major '
            'consumer. The arrangement was set up to let the company produce methanol locally with low-cost gas '
            'and avoid expensive freight charges.',
        ],
        'units': None,
        'takeaway': 'A plant that cannot compete on feedstock cost in one country can compete in another. '
                    'IPP marketed this unit in the United States, where natural gas was attractive for methanol '
                    'production.',
    },
    {
        'slug': 'nitric-acid-plant-pasadena-tx',
        'card': 'Nitric acid plant',
        'h1': 'How International Process Plants Cleared a Texas Site by Relocating Its Nitric Acid Plant to India',
        'title': 'Nitric Acid Plant Relocation Case Study, Pasadena | IPP',
        'desc': 'IPP bought a 500 tons/day nitric acid plant in Pasadena, TX to free space for new installations and sold it to a manufacturer for relocation to India.',
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
            'IPP purchased the plant, clearing space for the site’s new installations. The plant was then offered as a '
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
        'h1': 'How International Process Plants Turned a UK Oleochemical Site into an Award-Winning Waterfront Development',
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
                    ('IPP’s role', 'Bought the site, took on carrying costs and environmental liabilities, relocated the units'),
                    ('Result', 'Units relocated to Germany and the USA; site converted into an award-winning waterfront development')],
        'challenge': [
            'A 30-acre fatty acids facility in Bromborough held esters, sorbitan, triacetin and glycerin '
            'purification plants. Feedstock for the oleochemicals industry comes mostly from Southeast Asia, so '
            'the plant was no longer viable to operate in the UK.',
        ],
        'solution': [
            'IPP purchased the facility and took over all carrying costs and environmental liabilities. The process units '
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
            'Capacity basis: neither source gives a time unit for 550 million lb / 250 million lb. Pounds per year?',
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
            'The deck’s "World Class Texas Refinery Complex" is now on the page as "world-class refinery complex" (all deck facts used, 2026-10-30).',
        ],
    },
    'synthetic-chemical-site-kirkby-uk': {
        'sources': 'Deck slide 8; live /case-studies/ Synthetic Chemical tab.',
        'open': [
            'Seller: the deck names Kodak and the page now does too (decided 2026-10-30: the deck is client data). '
            'IPP’s live case-studies page does not name Kodak, so confirm IPP is happy to publish it.',
            'Location: the deck title says Liverpool, the text says Kirkby and Knowsley Industrial Park. Page uses '
            '"Kirkby, near Liverpool".',
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
            'methanol". The page keeps the deck’s meaning in past tense ("was being re-erected"). If IPP confirms it '
            'is running, say so.',
            'City: the deck heading says Rio de Janeiro; the page now uses it. Both texts say only Brazil.',
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
    'Savings (hub page): the deck gives "as much as 60%" on equipment (slide 15) and an average of 30-50% on used '
    'equipment and 50-60% on complete plants (slide 21); both are on the hub as client statements. The live site '
    'says 50% of capital cost and an 85% shorter lead time, which the hub does not use.',
    'Company facts on the hub come from deck slides 2-6, 10, 14-21. The slogans are on the hub too (added '
    '2026-10-30 at the user’s request): "world’s leading source", "world’s most trusted name in idled '
    'manufacturing plants" (the deck heading drops "in"; it was added) and the tagline. Slide 2’s mission line '
    'is still left out because its title is missing a word. '
    'The deck’s website, www.ippe.com, does not redirect to the current site, so the pages link to '
    'internationalprocessplants.com instead.',
    'Offices: slide 2 says 15 offices and slide 3 lists 15 countries; slide 17 names the HQ and 8 regional facilities. The hub says "offices in 15 countries" everywhere (QC round 2). '
    'The hub shows both lists as given.',
    'Equipment photos (slide 16) carry no captions in the deck; the alt text describes what each photo shows.',
]

# IPP business lines (deck slides 4, 6, 10, 14, 15). Each case study links to its line.
SERVICES = {
    'plants': {
        'name': 'Complete process plants',
        'img': 'service-complete-process-plants.jpg',
        'alt': 'Aerial view of a complete process plant site with buildings, process units and ponds',
        'text': [
            'IPP buys and sells complete idled process plants, including the real estate, complete production '
            'systems, buildings and intellectual property, for operation in place or for relocation.',
            'By reusing the existing site infrastructure, IPP revitalizes dormant facilities so a new owner can get '
            'its product to market with less CAPEX and in significantly less time. IPP purchases closed or idle '
            'manufacturing facilities, including the real estate, buildings, complete production systems and '
            'available intellectual assets, and may assume the environmental liabilities to remove the risk of '
            'additional cleanup costs for the seller.',
        ],
    },
    'units': {
        'name': 'Process units and systems',
        'img': 'service-process-units.jpg',
        'alt': 'Process units and distillation columns at a coastal refinery site',
        'text': [
            'IPP buys and sells individual process lines when only part of a plant becomes available for sale, or '
            'when the real estate is not available, and offers the line as a complete unit for relocation.',
            'When a process unit shuts down, the owner often wants it removed to reduce carrying costs and make room '
            'for future expansion. Instead of demolition, the most costly option, IPP resells the unit as a usable '
            'second-hand system and weighs the value of the process equipment against the cost of demolition. IPP has '
            'saved individual clients millions of dollars by taking responsibility for site dismantling and clean-up, '
            'equipment removal and complete plant relocation.',
            'IPP has purchased and relocated process units from virtually every major process manufacturing company '
            'and hundreds of medium-sized enterprises, from units inside active plant sites to complete plant '
            'closures. Most demolition projects cost the owner money; selling the plant for reuse yields a '
            'bottom-line profit, at a significantly higher value than scrap.',
        ],
    },
    'equipment': {
        'name': 'Process equipment',
        'img': 'service-process-equipment.jpg',
        'alt': 'Stainless steel reactor, piping and columns inside a process plant',
        'text': [
            'IPP buys individual pieces of process equipment from customers worldwide, either surplus to ongoing '
            'operations or from the liquidation of its complete plants, and offers them at significant '
            'savings versus new, with immediate delivery.',
            'The inventory covers second-hand, unused (from canceled projects), rebuilt and re-glassed equipment, '
            'much of it in exotic alloy, stainless steel and glass-lined construction. More than 15,000 pieces built '
            'by hundreds of OEMs are available from IPP’s yards in the US, UK, Germany and Romania and from '
            'plant sites around the globe, including ASME coded, TÜV certified and National Board stamped '
            'equipment.',
            'IPP often ships equipment directly from its original plant site, so buyers can also relocate the '
            'ancillary equipment, such as valves, controls, piping and instrumentation, to further increase the value.',
        ],
    },
}
SERVICE_OF = {
    'pet-plant-darlington-sc': 'plants', 'synthetic-chemical-site-kirkby-uk': 'plants',
    'oleochemical-plant-bromborough-uk': 'plants', 'mibk-solvent-plant-deer-park-tx': 'units',
    'methanol-plant-brazil-to-west-virginia': 'units', 'nitric-acid-plant-pasadena-tx': 'units',
}

# Company facts for the hub (deck slides 2, 3, 5, 15-22).
ABOUT = [
    'International Process Plants (IPP) buys and sells second-hand industrial process plants, process systems '
    'and individual process equipment. Its portfolio holds more than 100 complete process plants, 15 complete '
    'industrial sites including the real estate, manufacturing assets and intellectual property, and more than '
    '15,000 individual pieces of ready-to-ship process equipment. This inventory has made IPP the world’s '
    'leading source of good quality, second-hand industrial process plants, process systems and individual '
    'process equipment.',
    'IPP is headquartered in Princeton Junction, New Jersey, between New York City and Philadelphia, and works '
    'through offices in 15 countries. Over the past 40 years its customer base has grown to 160,000 '
    'relationships, including all of the Fortune 100 members within the process industries and tens of thousands '
    'of small and midsize manufacturers.',
    'IPP’s tagline sums up the offer: Your Partner for Complete Plant Solutions.',
]
ABOUT_STATS = [('100+', 'Complete process plants'), ('15', 'Complete industrial sites'),
               ('15,000+', 'Pieces of process equipment'), ('15', 'Countries with offices'),
               ('160,000', 'Customer relationships'), ('40 years', 'In the process industries')]
APPROACH = [
    'Primarily a buyer, not a broker, of plants and equipment worldwide.',
    'A relationship company rather than a transactional one, working with plant owners and buyers on their '
    'overall strategy over decades, not just one plant.',
    'A 40+ year reputation for honesty, integrity and fairness.',
    'Sales professionals with more than 275 combined years of experience in the process plant and equipment business.',
    'An extensive, diverse portfolio of plants, systems and equipment; if IPP does not have what a buyer needs, it '
    'finds out what is available on the market.',
    'Turnkey relocation and dismantling/demolition projects worldwide, inside active plants and during complete '
    'plant closures.',
    'Experience assuming environmental remediation responsibilities in certain plant real estate transactions.',
]
INDUSTRIES = ['Petrochemical', 'Industrial chemical', 'Agrichemical and fertilizer', 'Oil refining',
              'Fine and specialty chemical', 'Polymers', 'Artificial fiber', 'Power generation',
              'Oil and gas processing', 'Pharmaceutical', 'Food processing', 'Paper',
              'Metals processing and refining', 'Alternative fuels']
EQUIPMENT_CATEGORIES = ['Agitators', 'Bins and silos', 'Blowers', 'Boilers', 'Briquetters and Chilsonators',
                        'Calciners and kilns', 'Centrifuges', 'Chillers and ice systems', 'Columns', 'Compressors',
                        'Conveyors', 'Cooling towers', 'Cutters', 'Dryers', 'Dust collectors',
                        'Electrical generators', 'Evaporators', 'Extruders', 'Fermenters and bioreactors',
                        'Filters', 'Glass parts', 'Heat exchangers', 'Incinerators', 'Mills', 'Mixers',
                        'Packaging equipment', 'Plastics equipment', 'Pulp and paper equipment', 'Pulverizers',
                        'Pumps', 'Reactors', 'Screens and separators', 'Scrubbers', 'Tanks']
EQUIPMENT_PHOTOS = [('equipment-centrifuge.jpg', 'Blue industrial centrifuge on a skid'),
                    ('equipment-vessel.jpg', 'Blue horizontal process vessel with nozzles'),
                    ('equipment-dryer.jpg', 'Stainless steel fluid bed unit'),
                    ('equipment-compressor.jpg', 'Machinery package with insulated piping'),
                    ('equipment-heat-exchanger.jpg', 'Shell and tube heat exchanger'),
                    ('equipment-turbine-generator.jpg', 'Turbine generator set in a plant hall')]
SAVINGS = [
    'Clients tell IPP they save as much as 60% when they buy its equipment instead of new from the OEM.',
    'On average, clients report savings of 30 to 50% on used equipment and 50 to 60% on complete plants, '
    'compared with buying new from the OEM.',
    'For many clients in mature, global industries, buying an existing plant was the only economically viable '
    'way to meet their expansion plans.',
]
SELLER_INTRO = ('IPP manages and executes the entire process of selling process plants and equipment to end '
                'users, so the previous owner can focus on its business instead of selling parts and pieces and '
                'managing their removal. Removal is planned to minimize the impact on the seller’s ongoing '
                'operations on site.')
SELLER_AVOIDS = ['Demolition', 'Real estate taxes', 'Removing idle assets from the site',
                 'Trying to sell redundant assets', 'Managing demolition projects',
                 'Hours of personnel time spent managing closure activities instead of the core business']
SELLER_SIMPLER = ['One buyer and one contact, not 50 buyers', 'IPP manages the dismantling project',
                  'IPP manages the clean-up project']
REUSE = ('When plants or equipment fall out of use at one manufacturer, they are traditionally scrapped, usually '
         'while they still have useful life left. IPP’s mission is to reduce the need for new equipment by '
         'reusing existing equipment elsewhere in the world. That lowers the environmental impact and gets '
         'customers into production faster and at a lower cost.')
ONE_STOP = ('From selling and purchasing to demolishing, dismantling and shipping, IPP covers every step in one '
            'place, so owners can focus on their plant or process.')
FAQ = [
    ('A used plant comes without a performance warranty. How do I know it will work?',
     'IPP buys and offers plants with documentation of their performance and operating condition before '
     'shutdown. Once the plant is dismantled, packed, shipped, reconditioned as required and reinstalled with '
     'consideration for climate differences, it will produce the same quantity and quality of product from the '
     'same inputs. IPP considers this better than the 10% performance guarantee offered with a new plant.'),
    ('Do second-hand plants and equipment have a limited useful life?',
     'Most of IPP’s equipment was operated by companies with aggressive maintenance programs, so even rotating '
     'equipment and equipment in heavy service was properly maintained. As long as the new owner continues the '
     'manufacturer’s required maintenance, the plants and equipment can have their useful lives extended.'),
]
HQ = ('IPP World Headquarters', '410 Princeton Hightstown Road, Princeton Junction, NJ 08550, USA', '+1 609-586-8004')
FACILITIES = [('IPP U.K.', 'Storage facility and sales office'), ('IPP India & Far East', 'Sales office'),
              ('IPP Czech Republic', 'Sales office'), ('IPP China', 'Representative office'),
              ('IPP Germany', 'Storage facility and workshop'), ('UPE Romania', 'Reglass facility and workshop'),
              ('IPP Egypt', 'Representative office'), ('IPP Windsor, NJ, USA', 'Storage facility and workshop')]
OFFICE_COUNTRIES = ['Argentina', 'China', 'Czech Republic', 'Egypt', 'France', 'Germany', 'India', 'Italy', 'Poland',
                    'Portugal', 'Romania', 'Russia', 'Turkey', 'United Kingdom', 'United States']


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


BRAND = 'International Process Plants'


def brand(text):
    """The client wants the full brand name on these pages, never the IPP abbreviation (2026-11-03).

    The copy above still says IPP for brevity; this swaps it in titles, meta, body, alt text and schema.
    The shared site header and footer are left as the live site has them."""
    text = text.replace(f'{BRAND} (IPP)', BRAND)
    text = re.sub(r"\bIPP(’|')s\b", BRAND + '’', text)
    return re.sub(r'\bIPP\b', BRAND, text)


def page(title, desc, canonical, body, og_slug, og_alt, extra_head=''):
    title, desc, body, og_alt, extra_head = map(brand, (title, desc, body, og_alt, extra_head))
    # Preview images are served from the review site, so link previews work before the pages move to WordPress.
    og_img = f'{REVIEW_SITE}/assets/case-studies/og/{og_slug}.jpg'
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
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{escape(og_alt)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(desc)}">
  <meta name="twitter:image" content="{og_img}">
  <link rel="stylesheet" href="/assets/chemical/fonts.css">
  <link rel="stylesheet" href="/assets/chemical/page.css">
  <link rel="stylesheet" href="/assets/case-studies/case.css">
  <link rel="stylesheet" href="/assets/case-studies/site.css">
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
{MENU_SCRIPT}
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
    service = SERVICES[SERVICE_OF[c['slug']]]
    rows = c['summary'][:-1] + [('IPP service', service['name'])] + c['summary'][-1:]
    summary = ''.join(f'<div><dt>{escape(k)}</dt><dd>{escape(v)}</dd></div>' for k, v in rows)
    service_block = (f'<section class="cs-block cs-service"><h2>IPP service: {escape(service["name"])}</h2>'
                     f'{paras(service["text"])}<p><a href="/case-studies/#ipp-services">How IPP works across '
                     f'plants, units and equipment <span aria-hidden="true">→</span></a></p></section>')
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
    {service_block}
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
    return page(c['title'], c['desc'], f'{LIVE}/case-studies/{c["slug"]}/', body, c['slug'], c['alt'],
                f'<script type="application/ld+json">{schema(c)}</script>')


def bullets(items, cls=''):
    return f'<ul class="{cls}">' + ''.join(f'<li>{escape(i)}</li>' for i in items) + '</ul>'


def company_sections():
    stats = ''.join(f'<li><strong>{escape(v)}</strong><span>{escape(k)}</span></li>' for v, k in ABOUT_STATS)
    services = ''
    for key, s in SERVICES.items():
        cases = [c for c in CASES if SERVICE_OF[c['slug']] == key]
        links = (('<p class="cs-service-cases"><strong>Case studies:</strong> '
                  + ', '.join(f'<a href="/case-studies/{c["slug"]}/">{escape(c["card"])}</a>' for c in cases)
                  + '</p>') if cases else '')
        services += (f'<article class="cs-service-card"><img src="/assets/case-studies/{s["img"]}" '
                     f'alt="{escape(s["alt"])}" loading="lazy" width="500" height="300"><div>'
                     f'<h3>{escape(s["name"])}</h3>{paras(s["text"])}{links}</div></article>')
    photos = ''.join(f'<figure><img src="/assets/case-studies/{f}" alt="{escape(a)}" loading="lazy" width="360" '
                     f'height="260"></figure>' for f, a in EQUIPMENT_PHOTOS)
    faq = ''.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in FAQ)
    facilities = ''.join(f'<li><strong>{escape(n)}</strong><span>{escape(r)}</span></li>' for n, r in FACILITIES)
    return f'''<section class="cs-section" id="about-ipp">
  <div class="container">
    <h2>About International Process Plants</h2>
    <div class="cs-two-col"><div>{paras(ABOUT)}</div>
    <div><h3>How IPP works with plant owners and buyers</h3>{bullets(APPROACH, 'cs-checks')}</div></div>
    <ul class="cs-about-stats">{stats}</ul>
  </div>
</section>
<section class="cs-section cs-section-alt" id="ipp-services">
  <div class="container">
    <h2>IPP’s three business areas</h2>
    <div class="cs-service-grid">{services}</div>
  </div>
</section>
<section class="cs-section" id="equipment">
  <div class="container">
    <h2>Process equipment inventory categories</h2>
    <p>IPP’s process equipment inventory is organized into these categories:</p>
    {bullets(EQUIPMENT_CATEGORIES, 'cs-chips')}
    <div class="cs-photo-grid">{photos}</div>
  </div>
</section>
<section class="cs-section cs-section-alt" id="industries">
  <div class="container">
    <h2>Industries IPP focuses on</h2>
    {bullets(INDUSTRIES, 'cs-chips')}
  </div>
</section>
<section class="cs-section" id="savings">
  <div class="container cs-two-col">
    <div><h2>What clients report saving</h2>{bullets(SAVINGS, 'cs-checks')}</div>
    <div><h2>Reduce, reuse, recycle</h2><p>{escape(REUSE)}</p><h3>One stop shop</h3><p>{escape(ONE_STOP)}</p></div>
  </div>
</section>
<section class="cs-section cs-section-alt" id="sellers">
  <div class="container">
    <h2>Why plant owners sell to IPP</h2>
    <p>{escape(SELLER_INTRO)}</p>
    <div class="cs-two-col"><div><h3>Costs a seller avoids</h3>{bullets(SELLER_AVOIDS, 'cs-checks')}</div>
    <div><h3>Simpler, quicker and more cost-effective than selling alone</h3>{bullets(SELLER_SIMPLER, 'cs-checks')}</div></div>
  </div>
</section>
<section class="cs-section" id="questions">
  <div class="container cs-faq">
    <h2>Common questions about used plants and equipment</h2>
    {faq}
  </div>
</section>
<section class="cs-section cs-section-alt" id="offices">
  <div class="container">
    <h2>IPP headquarters and regional offices</h2>
    <p>The world’s most trusted name in idled manufacturing plants, IPP works through offices in 15 countries.</p>
    <div class="cs-two-col"><div><h3>{escape(HQ[0])}</h3><p>{escape(HQ[1])}<br><a href="tel:+16095868004">{escape(HQ[2])}</a></p>
    <h3>Countries with IPP offices</h3>{bullets(OFFICE_COUNTRIES, 'cs-chips')}</div>
    <div><h3>Regional facilities</h3><ul class="cs-facilities">{facilities}</ul></div></div>
  </div>
</section>'''


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
{company_sections()}
<section class="cs-cta">
  <div class="container cs-cta-inner">
    <div><h2>{escape(CTA['sell_plant'][0])}</h2><p>{escape(CTA['sell_plant'][1])}</p></div>
    <div class="cs-cta-buttons"><a class="cs-button" href="{LIVE}/sell-plants/">Sell your plant to IPP <span aria-hidden="true">→</span></a><a class="cs-button cs-button-outline" href="{LIVE}/plants/">Browse available plants</a></div>
  </div>
</section>'''
    return page('Case Studies: Plant Repurposing and Relocation | IPP',
                'Six IPP case studies: idle plants bought, repurposed or relocated, from a PET plant in South Carolina '
                'to a methanol plant moved from Brazil to West Virginia.',
                f'{LIVE}/case-studies/', body, 'case-studies',
                'IPP case study plants: a PET plant, an MIBK solvent plant and a methanol plant')


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
