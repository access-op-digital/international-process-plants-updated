"""The live internationalprocessplants.com header and footer, rebuilt for the case-study review pages.

Measured in Chrome on 2026-11-03: a sticky white header bar with a 4 px #134a62 top line, 1248 px content, the 226 px
dark-blue logo, the eight-item Montserrat menu with its dropdowns and the EN language tab; the grey gradient footer
with Buying & Selling, About (+ IPP\u2019s Group of Companies), Contact, the 11 global offices and the copyright bar.
Icons and the US flag come from IPP-work/_pipeline/live_design.py (the 40-page build). Styles: assets/case-studies/site.css.
"""
from html import escape as _e

US_FLAG = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAMCAIAAADgcHrrAAAAK3RFWHRDcmVhdGlvbiBUaW1lAHphIDMxIGRlYyAyMDA1IDE3OjEzOjE3ICswMTAwcgTDIgAAAAd0SU1FB9UMHxAUEGyS6bUAAAAJcEhZcwAACxIAAAsSAdLdfvwAAAAEZ0FNQQAAsY8L/GEFAAABTklEQVR42o2SzUrDQBSFZ0pCGq1N2iAUrC6kFFy57gvYvSs37vsohb6Jj6DgQhcFV4JrhYg0pO1kMpO/SWaScVp3GmkPZ3GZc74LAxeORo8QFqvVKopIr2fpekMIefc5G+g++KuqCqUMqkpLkmg4tGzbphR2OmYc55TmJ89P4KJdg5WljVAzCDTPW3a7ZRy7RVFxrkURU57f3ly2UlCnNedI9fp907KgGiAs223TMDTD0I8nE2do12LEdTVCVBsglChnWVFVUgVClOThPn0F9RjGlDFNSuk4rUbjKE254xwmSa4WmeeDgzOjFmv6fjOOten0Ossi3/9ST3CjTXbK3wCo/9uPtKv5DOR5Sumv4D+IYcwYg9LzQByDxQLspw/XXRMC5XhcChEKsSf2QmnAOZSMAUIKjNcY72QQxigMlwjBd8ehUuLt1ezEwm1T+RuJ/sc7wy28LQAAAABJRU5ErkJggg=='
CARET = '<svg class="ipp-caret" viewBox="0 0 320 512" aria-hidden="true"><path fill="currentColor" d="M143 352.3L7 216.3c-9.4-9.4-9.4-24.6 0-33.9l22.6-22.6c9.4-9.4 24.6-9.4 33.9 0l96.4 96.4 96.4-96.4c9.4-9.4 24.6-9.4 33.9 0l22.6 22.6c9.4 9.4 9.4 24.6 0 33.9l-136 136c-9.2 9.4-24.4 9.4-33.8 0z"/></svg>'
BARS = '<svg viewBox="0 0 448 512" aria-hidden="true"><path fill="currentColor" d="M16 132h416c8.837 0 16-7.163 16-16V76c0-8.837-7.163-16-16-16H16C7.163 60 0 67.163 0 76v40c0 8.837 7.163 16 16 16zm0 160h416c8.837 0 16-7.163 16-16v-40c0-8.837-7.163-16-16-16H16c-8.837 0-16 7.163-16 16v40c0 8.837 7.163 16 16 16zm0 160h416c8.837 0 16-7.163 16-16v-40c0-8.837-7.163-16-16-16H16c-8.837 0-16 7.163-16 16v40c0 8.837 7.163 16 16 16z"/></svg>'


LIVE = 'https://internationalprocessplants.com'
LOGO = LIVE + '/wp-content/uploads/2023/12/IPP-LOGO_DARKBLUE-FINAL-300x118.png'
IMS = 'https://ims.internationalprocessplants.com'
NAV = [
    ('Our Plants', LIVE + '/plants/', [('Search Plants', IMS + '/search?asset=Plant')]),
    ('Our Equipment', LIVE + '/process-equipment/', [('Search Equipment', IMS + '/search?asset=Equipment')]),
    ('Buy Used', LIVE + '/buy-used/', []),
    ('Buy New', LIVE + '/buy-new/', []),
    ('Sell to IPP', LIVE + '/sell-to-ipp/',
     [('Sell Us Your Equipment', LIVE + '/sell-equipment/'), ('Sell Us Your Plants', LIVE + '/sell-plants/')]),
    ('About Us', LIVE + '/about-us/', []),
    ('FAQ & More', LIVE + '/more/', [('White Papers', LIVE + '/white-papers/')]),
    ('Contact', LIVE + '/contact/', []),
]
FOOT_BUY = [('Buy Used', LIVE + '/buy-used/'), ('Buy New', LIVE + '/buy-new/'), ('Sell to IPP', LIVE + '/sell-to-ipp/'),
            ('Plants', LIVE + '/plants/'), ('Search Plants', IMS + '/search?asset=Plant'),
            ('Equipment', LIVE + '/process-equipment/'), ('Search Equipment', IMS + '/search?asset=Equipment')]
FOOT_ABOUT = [('About IPP', LIVE + '/about-us/'), ('FAQ', LIVE + '/more/#ipp_faq'), ('Events', LIVE + '/more/#ipp_events'),
              ('Careers', LIVE + '/more/#ipp_careers'), ('Articles', LIVE + '/articles/')]
GROUP = [('Gale Process Solutions', 'https://galeprocesssolutions.com/'),
         ('Universal Glasteel Equipment', 'https://uge-inc.com/')]
SOCIAL = [
    ('Facebook', 'https://www.facebook.com/InternationalProcess',
     'M9.2 21v-8H6.5V9.9h2.7V7.6c0-2.7 1.6-4.1 4-4.1 1.1 0 2.1.1 2.4.1v2.8h-1.7c-1.3 0-1.5.6-1.5 1.5v2h3.1l-.4 3.1h-2.7v8z'),
    ('X', 'https://twitter.com/processplants',
     'M17.8 3h3l-6.6 7.6L22 21h-6.1l-4.8-6.3L5.6 21h-3l7.1-8.1L2.3 3h6.2l4.3 5.7zm-1.1 16.2h1.7L7.4 4.7H5.6z'),
    ('LinkedIn', 'https://www.linkedin.com/company/internationalprocessplants',
     'M6.9 21H3.3V9.4h3.6zM5.1 7.8a2.1 2.1 0 1 1 0-4.2 2.1 2.1 0 0 1 0 4.2zM21 21h-3.6v-5.6c0-1.3 0-3.1-1.9-3.1s-2.2 1.5-2.2 3V21H9.7V9.4h3.4V11h.1c.5-.9 1.6-1.9 3.4-1.9 3.6 0 4.3 2.4 4.3 5.5z'),
]
# Office list as shown under "View all 11 global offices" on the live footer (read 2026-11-03).
OFFICES = [
    ('Headquarters — USA', 'IPP World HQ', '410 Princeton Hightstown Road, Princeton Junction, NJ 08550, USA', '+1 609-586-8004', ''),
    ('UK', 'IPP Europe Ltd', 'The Grange Business Centre, Belasis Ave, Billingham, TS23 1LG, UK', '+44 1642 367 910', ''),
    ('Germany', 'IPPE Germany GmbH', 'Zorbiger Straße 56, 06749 Bitterfeld-Wolfen, Germany', '+49 3493 515848-0', ''),
    ('Czech Republic', 'IPPE Eastern Europe', 'Hajecka 14, 618 00 Brno, Czech Republic', '+420 548 216 680', ''),
    ('India & Far East', 'IPPE India Office', '83/A Tagor Nagar Society, Old Padra Rd, Baroda, Gujarat 390015, India',
     '+91 265 234 1057', ''),
    ('China', 'IPPE China / Lucky Star Chem', "A1809, Times Int'l Center, 101 Shaoyaoju Bei Li, Chaoyang, Beijing 100029, China",
     '010-8435 1598', 'info@luckystarchem.com'),
    ('Romania', 'UGE – UPE Romania', 'Str. Negoiu nr. 1, Fagaras, 505200 Jud. Brasov, Romania', '+40 268 217 579',
     'fagaras@upe.ro'),
    ('Poland', 'Universal Turbomachinery Equipment', 'ul. Aleksandrowska 67/93, 91-205 Łódź, Poland',
     '+48 42 611 06 07', 'ute@ute.com.pl'),
    ('Mexico', 'IPP Mexico', 'Ciudad de México, 11370, Mexico', '+1 609 249 2190', 'Arturog@ippe.com'),
    ('Egypt', 'IPP Egypt', '27 Hegaz Street, Heliopolis, Cairo, Egypt', '+2 (02) 2454-9350', 'EgyptRep@ippe.com'),
    ('Portugal', 'IPP Portugal', 'Rua João Luís de Moura, N 4-A, 1 Esq, 2750-387 Cascais, Portugal', '',
     'PortugalRep@ippe.com'),
]
PIN = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" '
       'd="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5" fill="none" '
       'stroke="currentColor" stroke-width="2"/></svg>')
CHEVRON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.5" '
           'd="M6 9l6 6 6-6"/></svg>')
ARROW = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="3" '
         'd="M9 6l6 6-6 6"/></svg>')
ENVELOPE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M2 5h20v14H2zm2 2v.3l8 5.3 '
            '8-5.3V7zm16 2.7l-8 5.3-8-5.3V17h16z"/></svg>')


def _a(label, href, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="{_e(href)}">{_e(label)}</a>'


def header_html():
    items = []
    for label, href, subs in NAV:
        if subs:
            sub = ''.join(f'<li>{_a(t, h)}</li>' for t, h in subs)
            items.append(f'<li class="has-sub"><a href="{_e(href)}">{_e(label)}{CARET}</a><ul class="ipp-sub">{sub}</ul></li>')
        else:
            items.append(f'<li>{_a(label, href)}</li>')
    return (f'<header class="ipp-header"><div class="ipp-header-inner">'
            f'<a href="{LIVE}/" class="ipp-logo"><img src="{LOGO}" width="226" height="89" alt="International Process Plants (IPP)"></a>'
            f'<button class="ipp-burger" type="button" aria-label="Menu" aria-expanded="false">{BARS}</button>'
            f'<nav class="ipp-nav" aria-label="Main menu"><ul>{"".join(items)}</ul></nav>'
            f'</div></header>'
            f'<div class="ipp-lang" title="English"><img src="{US_FLAG}" width="18" height="12" alt="en_US">EN</div>')


def footer_html(year=2026):
    buy = ''.join(f'<li>{_a(t, h)}</li>' for t, h in FOOT_BUY)
    about = ''.join(f'<li>{_a(t, h)}</li>' for t, h in FOOT_ABOUT)
    group = ''.join(f'<li><a href="{_e(h)}">{ARROW}<span>{_e(t)}</span></a></li>' for t, h in GROUP)
    social = ''.join(f'<a href="{_e(h)}" aria-label="{_e(n)}"><svg viewBox="0 0 24 24" aria-hidden="true">'
                     f'<path fill="currentColor" d="{p}"/></svg></a>' for n, h, p in SOCIAL)
    offices = ''
    for label, name, addr, phone, mail in OFFICES:
        tel = ''.join(ch for ch in phone if ch.isdigit() or ch == '+')
        offices += (f'<div class="ipp-office"><span class="ipp-office-label">{_e(label)}</span><strong>{_e(name)}</strong>'
                    f'<em>{_e(addr)}</em>'
                    + (f'<a href="tel:{tel}">{_e(phone)}</a>' if phone else '')
                    + (f'<a href="mailto:{_e(mail)}">{_e(mail)}</a>' if mail else '') + '</div>')
    return f'''<footer class="ipp-footer">
  <div class="ipp-footer-main"><div class="ipp-footer-inner ipp-footer-grid">
    <a class="ipp-footer-logo" href="{LIVE}/"><img src="{LOGO}" width="226" height="89" alt="International Process Plants (IPP)" loading="lazy"></a>
    <div><h2>Buying &amp; Selling</h2><ul class="ipp-footer-links">{buy}</ul></div>
    <div><h2>About</h2><ul class="ipp-footer-links">{about}</ul>
      <div class="ipp-group"><h3>IPP’s Group of Companies</h3><ul>{group}</ul></div></div>
    <div><h2>Contact</h2>
      <a class="ipp-connect" href="{LIVE}/contact/">{ENVELOPE}<span>Connect</span></a>
      <p class="ipp-phones"><strong>USA</strong> <a href="tel:+16095868004">+1 609-586-8004</a><br>
      <strong>UK</strong> <a href="tel:+441642367910">+44-1642-367910</a><br>
      <a href="mailto:sales@internationalprocessplants.com">sales@internationalprocessplants.com</a></p>
      <div class="ipp-social">{social}</div></div>
  </div></div>
  <div class="ipp-footer-offices"><div class="ipp-footer-inner">
    <p class="ipp-office-links"><a href="{LIVE}/contact/">{PIN}Office Locations</a><a href="{LIVE}/contact/">{PIN}View on Map</a></p>
    <details class="ipp-offices"><summary>View all 11 Global Offices {CHEVRON}</summary><div class="ipp-office-grid">{offices}</div></details>
  </div></div>
  <div class="ipp-copyright">Copyright © {year} IPP - International Process Plants | All Rights Reserved | <a href="{LIVE}/privacy-policy/">Privacy Statement</a></div>
</footer>'''


MENU_SCRIPT = ('<script>(function(){var h=document.querySelector(".ipp-header"),b=h&&h.querySelector(".ipp-burger");'
               'if(!b)return;b.addEventListener("click",function(){b.setAttribute("aria-expanded",h.classList.toggle("open"))})})();</script>')
