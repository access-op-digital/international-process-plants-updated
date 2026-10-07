"""Normalize layout wrappers into semantic content so the skill's Word writer keeps headings/tables."""
from pathlib import Path
from lxml import html,etree
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.build-deps'))
WORK=ROOT/'docs/chemical-build/content'
SKILL=Path.home()/'.agents/skills/anup-commercial-content/scripts'
doc=html.document_fromstring((WORK/'content.html').read_text(encoding='utf-8'))
# Final-copy cleanup: drop screen-only chrome and separate fields the page lays out side by side.
def link(href,text):
 a=html.Element('a',href=href);a.text=text;return a
for card in doc.xpath('//article[contains(@class,"stock-card")]'):
 specs=card.xpath('.//a[contains(@aria-label,"View Specs")]/@href');h=card.xpath('.//h3')[0]
 if specs:
  t=h.text_content().strip()
  for c in list(h):h.remove(c)
  h.text=None;h.append(link(specs[0],t))
for n in doc.xpath('//nav[contains(@class,"breadcrumbs")]|//*[@aria-hidden="true"]|//*[contains(@class,"card-actions")]|//a[contains(@class,"video-thumb")]/img'):
 if n.getparent() is not None:n.drop_tree()
for el in doc.iter():
 for attr in ('text','tail'):
  v=getattr(el,attr)
  if v and any(c in v for c in '↗↓▶'):setattr(el,attr,v.replace(' ↗','').replace('↗','').replace(' ↓','').replace('↓','').replace('▶',''))
for a in doc.xpath('//a'):
 if len(a)==0 and a.text:a.text=a.text.strip()
for a in doc.xpath('//a[h2 or h3 or h4 or p or div]'):
 href=a.get('href','')
 for s in a.xpath('.//span[contains(@class,"text-link")]'):s.drop_tree()
 heads=a.xpath('.//h2|.//h3|.//h4')
 if heads and href and not href.startswith('#'):
  h=heads[0];t=h.text_content().strip()
  for c in list(h):h.remove(c)
  h.text=None;h.append(link(href,t))
 a.drop_tag()
for row in doc.xpath('//div[contains(@class,"button-row") or contains(@class,"closing-actions") or contains(@class,"inventory-bottom-links") or contains(@class,"category-links")]'):
 links=[(a.get('href',''),a.text_content().strip()) for a in row.xpath('.//a')]
 p=html.Element('p')
 if all(h.startswith('#') for h,_ in links):p.text='Buttons: '+' · '.join(t for _,t in links)
 else:
  for i,(h,t) in enumerate(links):
   a=link(h,t);a.tail=' · ' if i<len(links)-1 else None;p.append(a)
 row.getparent().replace(row,p)
for li in doc.xpath('//ul[@class="hero-stats"]/li'):
 num=li.xpath('./strong')[0].text_content().strip();label=li.xpath('./span')[0].text_content().strip()
 label=label[0].lower()+label[1:]
 for c in list(li):li.remove(c)
 li.text=f'{num}, {label}' if num.startswith('Since') else f'{num} {label}'
for logos in doc.xpath('//div[contains(@class,"client-logos")]'):
 p=html.Element('p');p.text=', '.join(i.get('alt') for i in logos.xpath('.//img'));logos.getparent().replace(logos,p)
for li in doc.xpath('//ul[contains(@class,"maker-list")]/li'):
 a=li.xpath('./a')[0];a.tail=': '+(a.tail or '')
for strong in doc.xpath('//ul[contains(@class,"recognition-badges")]//strong'):
 strong.tail=': '+(strong.tail or '')
for li in doc.xpath('//li[contains(@class,"video-card")]'):
 thumb=li.xpath('.//a[contains(@class,"video-thumb")]')[0];href=thumb.get('href')
 quote=(li.xpath('.//blockquote') or [None])[0];quote=quote.text_content().strip() if quote is not None else thumb.get('data-title')
 who=li.xpath('.//p[contains(@class,"video-who")]')[0];name=who.xpath('./strong')[0].text_content().strip()
 role=who.text_content().strip()[len(name):].strip()
 for c in list(li):li.remove(c)
 li.text=None;a=link(href,quote);a.tail=f' {name}, {role} (video)';li.append(a)
for h in doc.xpath('//ol[contains(@class,"buying-steps")]/li/h3'):
 h.tag='strong';h.tail=': '+(h.tail or '')
for pid,label in (('why-buyers','For buyers'),('why-sellers','For sellers')):
 for panel in doc.xpath(f'//*[@id="{pid}"]'):
  p=html.Element('p');s=html.Element('strong');s.text=label;p.append(s);panel.addprevious(p)
for node in doc.xpath('//input|//select|//button|//svg|//*[@class="results-header"]|//*[@class="stock-image"]'):
 node.getparent().remove(node)
for node in doc.xpath('//img'):
 node.drop_tag()
for node in doc.xpath('//summary'):node.tag='h3'
for dl in doc.xpath('//dl'):
 table=html.Element('table')
 for row in dl.xpath('./div'):
  tr=html.Element('tr')
  for child in row.xpath('./dt|./dd'):
   cell=html.Element('td');cell.text=child.text_content();tr.append(cell)
  table.append(tr)
 dl.getparent().replace(dl,table)
for a in doc.xpath('//a[h2 or h3 or p or div]'):
 href=a.get('href');a.tag='div';a.attrib.clear()
 p=html.Element('p');link=html.Element('a',href=href);link.text='Source / details';p.append(link);a.append(p)
for node in doc.xpath('//*[@class="manufacturer-links"]'):
 node.tag='ul'
 for a in list(node):
  node.remove(a);li=html.Element('li');li.append(a);node.append(li)
etree.strip_tags(doc,'section','div','article','aside','details','nav')
body=doc.xpath('//body')[0]
clean='\n'.join(html.tostring(n,encoding='unicode') for n in body)
clean='\n'.join(line.rstrip() for line in clean.splitlines()).strip()+'\n'
(WORK/'content.html').write_text(clean,encoding='utf-8')
sys.path.insert(0,str(SKILL))
from build_outputs import build_job
from engine import output_writer
from docx.shared import RGBColor
output_writer.FONT_NAME='Roboto'
job=build_job(str(WORK))
out=ROOT/'docs/chemical-build/deliverables/used-chemical-process-plants-for-sale-content.docx'
word=output_writer._build_docx(job,clean)
for style in word.styles:
 if style.name.startswith('Heading'):
  style.font.name='Montserrat';style.font.color.rgb=RGBColor.from_string('183947')
 elif style.name in ['Normal','List Bullet','List Number']:
  style.font.name='Roboto'
for paragraph in word.paragraphs:
 if paragraph.style.name.startswith('Heading'):
  for run in paragraph.runs:run.font.name='Montserrat'
word.save(out)
print('Semantic Word copy exported:',out.name)
