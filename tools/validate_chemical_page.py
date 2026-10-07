"""Validate preservation, crawlable content, metadata, assets and meaningful link contracts."""
from pathlib import Path
from lxml import html
import json,re
ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'chemical-process-plant-equipment-used-systems-for-sale/index.html'
raw=PAGE.read_text(encoding='utf-8');doc=html.fromstring(raw)
main=doc.xpath('//main')[0]
visible=' '.join(main.text_content().split())
checks=[]
def check(name,result):
 checks.append({'check':name,'pass':bool(result)})
 if not result:raise AssertionError(name)
check('One H1 with the approved broader plant topic',doc.xpath('//h1/text()')==['Used Chemical Process Plants for Sale'])
canonical='https://internationalprocessplants.com/chemical-process-plant-equipment-used-systems-for-sale/'
check('Existing canonical preserved',doc.xpath('//link[@rel="canonical"]/@href')==[canonical])
check('Draft remains noindex',doc.xpath('//meta[@name="robots"]/@content')==['noindex, nofollow'])
check('Website social type',doc.xpath('//meta[@property="og:type"]/@content')==['website'])
check('No article metadata',not doc.xpath('//meta[starts-with(@property,"article:")]'))
schema=json.loads(doc.xpath('//script[@type="application/ld+json"]/text()')[0]);types=[n['@type'] for n in schema['@graph']]
check('CollectionPage schema without Article/Person', 'CollectionPage' in types and 'Article' not in types and 'Person' not in types)
check('No unconfirmed reviewer claim','reviewedBy' not in raw and 'Reviewed by' not in raw)
check('No fabricated ratings or offers',all(x not in raw for x in ['aggregateRating','priceCurrency','ratingValue']))
categories=doc.xpath('//*[contains(@class,"category-heading")]/h3/text()')
check('Seven original categories in original order',categories==['Reactors','Heat exchangers','Centrifuges','Dryers','Filters','Distillation columns','Tanks'])
original=[
 'Precision-controlled systems for chemical synthesis, available in glass-lined, stainless and specialty alloys.',
 'Shell-and-tube and plate exchangers for thermal control and energy recovery.',
 'Used for purification, separation and crystallization. Basket, inverting and peeler models available.',
 'Moisture removal solutions including rotary, vacuum and disc dryers.',
 'Pressure and vacuum systems to remove particulates or recover solids.',
 'For purification, solvent recovery and fractional separation.',
 'For storage, blending and transfer. Jacketed and non-jacketed tanks available.',
 'Yes. In addition to individual equipment, we sell complete chemical process plants, including teardown and relocation services.',
 'Yes. IPP offers on-site and video inspections for most equipment. Contact us to schedule one.',
 'From multinational chemical producers, toll manufacturers and decommissioned or restructured facilities worldwide.'
]
for text in original:check('Preserved: '+text[:60],text in visible)
cards=doc.xpath('//*[contains(concat(" ",@class," ")," stock-card ")]')
check('14 crawlable inventory cards',len(cards)==14)
check('Six plants and eight equipment cards',len([c for c in cards if c.get('data-group')=='plants'])==6 and len([c for c in cards if c.get('data-group')=='equipment'])==8)
for c in cards:
 a=c.xpath('.//a[contains(@aria-label,"View Specs")]')[0]
 check('Direct secure IMS specs link: '+c.get('id'),a.get('href').startswith('https://ims.internationalprocessplants.com/inventory/') and '/detail/' in a.get('href') and a.get('target')=='_blank' and 'noopener' in a.get('rel',''))
check('Fourteen visible FAQ answers with matching schema',len(doc.xpath('//details'))==14 and len(schema['@graph'][-1]['mainEntity'])==14)
for detail,q in zip(doc.xpath('//details'),schema['@graph'][-1]['mainEntity']):
 check('FAQ schema matches: '+q['name'],' '.join(detail.xpath('./p')[0].text_content().split())==' '.join(q['acceptedAnswer']['text'].split()))
check('No em dashes or CMS author debris','—' not in visible and 'access@op.digital' not in raw and 'Latest Posts' not in raw)
check('No old contact-us links','/contact-us' not in raw)
check('No location filter',not doc.xpath('//select[contains(@id,"location")]'))
check('No inert forms',not doc.xpath('//form'))
ids=doc.xpath('//*[@id]/@id');check('Unique HTML ids',len(ids)==len(set(ids)))
for href in doc.xpath('//a[starts-with(@href,"#")]/@href'):check('Anchor exists '+href,href[1:] in ids)
for img in doc.xpath('//img'):
 check('Meaningful image alt '+img.get('src'),bool(img.get('alt','').strip()))
check('Self-hosted assets exist',all((ROOT/u.lstrip('/')).is_file() for u in doc.xpath('//img/@src|//script[@src]/@src|//link[@rel="stylesheet"]/@href')))
tabs=doc.xpath('//*[@role="tablist"]//*[@role="tab"]')
check('Resources tabs are About Us, FAQs and Blog only',[' '.join(t.text_content().split()) for t in tabs]==['About Us','FAQs','Blog'])
for t in tabs:
 panel=doc.xpath(f'//*[@id="{t.get("aria-controls")}"]')
 check('Tab panel exists: '+t.get('aria-controls'),len(panel)==1 and panel[0].get('role')=='tabpanel' and panel[0].get('aria-labelledby')==t.get('id'))
check('All FAQs sit in the FAQs tab panel',len(doc.xpath('//*[@id="faqs"]//details'))==14)
faq_q=[' '.join(s.text_content().split()) for s in doc.xpath('//*[@id="faqs"]//summary')]
check('Nine buyer FAQs, then five seller FAQs',faq_q[8]=='Does IPP sell new chemical process equipment?' and faq_q[9]=='Does IPP buy shutdown chemical plants and surplus equipment?' and len(faq_q)==14)
check('Hero states both sides',any(p.text_content().startswith('Buying used chemical process plants') for p in doc.xpath('//section[@data-section="0"]//p')) and any(p.text_content().startswith('Selling shutdown chemical plants') for p in doc.xpath('//section[@data-section="0"]//p')))
check('Hero stat strip carries four dated company figures',[' '.join(x.strip() for x in li.itertext() if x.strip()) for li in doc.xpath('//ul[@class="hero-stats"]/li')]==['15,000+ Pieces of inventory','20 Complete plant sites','15 Countries with offices','Since 1980 Supplying process equipment'])
check('Seller path has four steps',doc.xpath('//ol[contains(@class,"seller-steps")]/li/h3/text()')==['Send your asset information','IPP values the assets','Agree the sale structure','Decommissioning, dismantling and removal'])
check('Seller section follows the buying steps',[s.get('id') for s in doc.xpath('//section[@id="buying" or @id="sell"]')]==['buying','sell'])
makers=doc.xpath('//ul[@class="maker-list"]/li/a')
check('Seven leading makers link to type-scoped IMS searches',len(makers)==7 and all('/inventory/search/equipment/' in a.get('href') and 'manufacturer=' in a.get('href') for a in makers))
check('Size ranges on the five types IMS publishes them for',len(doc.xpath('//div[contains(@class,"category-card")][.//p[@class="range-note"]]'))==5)
check('Closing CTA serves buyers and sellers',doc.xpath('//section[contains(@class,"closing-cta")]//h2/text()')==['Ready to buy or sell chemical plants and equipment?'] and all(doc.xpath(f'//section[contains(@class,"closing-cta")]//a[@href="{u}"]') for u in ['https://internationalprocessplants.com/contact/','https://internationalprocessplants.com/sell-plants/','https://internationalprocessplants.com/sell-equipment/','mailto:sales@internationalprocessplants.com','tel:+16095868004']))
check('No phrasal take-on predicate','take on' not in visible.lower())
intro=[' '.join(p.text_content().split()) for p in doc.xpath('//section[@data-section="2"]//p')]
check('Company intro opens with what IPP sells, to whom',intro and intro[0].startswith('International Process Plants (IPP) sells used chemical process plants and equipment to chemical, petrochemical'))
check('Company intro covers selling to IPP',any(x.startswith('IPP buys shutdown chemical plants') for x in intro) and doc.xpath('//section[@data-section="2"]//a[@href="https://internationalprocessplants.com/sell-plants/"]'))
intro_photo=ROOT/'assets/chemical/intro/reactor-removal.webp'
check('Company intro photo fills the heading column, under 200 KB',doc.xpath('//section[@data-section="2"]//figure[@class="intro-photo"]/img[@src="/assets/chemical/intro/reactor-removal.webp"]') and intro_photo.is_file() and intro_photo.stat().st_size<200000)
check('Each equipment type opens with IPP context and lists its subtypes',all(c.xpath('.//ul[@class="type-list"]/li') and 'IPP supplies used' in c.text_content() for c in doc.xpath('//div[contains(@class,"category-card")]')) and len(doc.xpath('//div[contains(@class,"category-card")]'))==7)
check('Recognition shown as four badges',len(doc.xpath('//ul[@class="recognition-badges"]/li/a'))==4 and not doc.xpath('//*[contains(@class,"evidence-links")]'))
check('Global inventory section removed',not doc.xpath('//section[contains(@class,"locations-section")]'))
vids=doc.xpath('//ul[@class="video-reviews"]/li/a[@data-video]')
check('Four customer testimonial videos from IPP playlist with self-hosted thumbnails',[x.get('data-video') for x in vids]==['1Qhma3r0Cas','WlsjZMptSZg','BWWcZNOchrY','Kz6N9uacqkY'] and all(x.get('href')=='https://www.youtube.com/watch?v='+x.get('data-video') for x in vids))
check('VideoObject markup for each testimonial, no rating markup',len([n for n in schema['@graph'] if n['@type']=='VideoObject'])==4)
check('No eyebrow labels or note lines',not doc.xpath('//*[contains(@class,"eyebrow") or contains(@class,"source-note") or contains(@class,"hero-note")]'))
check('Blog tab lists six articles',len(doc.xpath('//*[@id="blog"]//a[contains(@class,"blog-card")]'))==6)
check('Reviews heading follows the outline',doc.xpath('//section[contains(@class,"reviews-section")]//h2/text()')==['What do chemical manufacturers say about IPP?'])
check('Buying process unchanged',doc.xpath('//ol[@class="buying-steps"]/li/h3/text()')==['Share your requirements','Review specifications and inspect','Agree the purchase scope','Plan dismantling and relocation','Arrange shipping and start-up support'])
about=ROOT/'assets/chemical/about/ipp-team.webp'
check('About photo under 200 KB',about.is_file() and about.stat().st_size<200000)
photos=list((ROOT/'assets/chemical').glob('*.webp'))
check('All equipment photographs under 200 KB',len(photos)==13 and all(p.stat().st_size<200000 for p in photos))
report={'page':str(PAGE.relative_to(ROOT)),'checks':checks,'passed':len(checks),'photograph_total_bytes':sum(p.stat().st_size for p in photos),'max_photograph_bytes':max(p.stat().st_size for p in photos)}
(ROOT/'docs/chemical-build/validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(len(checks),'preservation, schema, content and asset checks passed.')
