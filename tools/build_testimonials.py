"""Build testimonials/index.html: the proposed International Process Plants
reviews and testimonials page, on the plan of the Modern House Numbers
testimonials page, laid out with the review site's own patterns (case-study
hero with stats strip, the chemical page's split section headings).

Run from the repo root:  python tools/build_testimonials.py

Inputs:
  data/testimonials/gbp-reviews-princeton-junction-nj.json
  data/testimonials/gbp-reviews-eastover-sc.json
      The two Google Business Profiles Google Maps lists for International
      Process Plants, pulled through DataForSEO business_data/google/reviews.
  case-studies/index.html
      Header, language tab and footer are lifted from it.
  CUSTOMER_VIDEOS / TEAM_VIDEOS below
      Customer interviews: the four in the "Customer Testimonials" playlist the
      live homepage embeds (PLRlhdb05DXKSO3XMiN2gd5-DduvcVPWHx); wording, names
      and roles as on the chemical page. Team videos: the company's own YouTube
      channel (@internationalprocessplants2946); captions paraphrase each video's
      YouTube description. Thumbnails: assets/chemical/reviews/ (customer) and
      assets/testimonials/ (YouTube's full-size frames, 960x540 webp).

Rules:
  - Review text and owner replies are Google's, untouched (HTML-escaped only).
  - Every review is shown, written or rating-only, so the cards match the counts
    Google reports for each profile (user review, 2026-11-20).
  - No Review or AggregateRating markup (self-serving reviews).
  - Copy: full brand name, then we/our; no "you"; no em dash.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "testimonials"
OUT = ROOT / "testimonials" / "index.html"
PLAYLIST = "https://www.youtube.com/playlist?list=PLRlhdb05DXKSO3XMiN2gd5-DduvcVPWHx"
CHANNEL = "https://www.youtube.com/@internationalprocessplants2946"
MIN_RATING_ONLY = 1  # show every review, so the cards match Google's counts

PROFILES = [
    ("gbp-reviews-princeton-junction-nj.json", "Princeton Junction, NJ"),
    ("gbp-reviews-eastover-sc.json", "Eastover, SC"),
]

TITLE = "International Process Plants Reviews and Testimonials"
DESC = ("Read International Process Plants reviews: chemical manufacturers on video at SOCMA 2024, "
        "plus Google reviews of our New Jersey and South Carolina locations.")

# (video id, quote or title, is a direct quote, name, role, thumbnail alt)
CUSTOMER_VIDEOS = [
    ("WlsjZMptSZg", "If somebody asked me to rate IPP 1-10, I’d give them a 10 every time!", True,
     "Joel Salzman", "VP of Operations, ChemDesign Products, Inc., Marinette, Wisconsin",
     "Joel Salzman of ChemDesign Products in a video interview at IPP’s SOCMA 2024 booth"),
    ("1Qhma3r0Cas", "The International Process Plants team is outstanding! They understand my business", True,
     "Chuck Castley", "Commercial vice president, Chemicals Incorporated, Baytown, Texas",
     "Chuck Castley of Chemicals Incorporated in a video interview at IPP’s SOCMA 2024 booth"),
    ("BWWcZNOchrY", "The power of partnership: A testimonial to International Process Plants’ customer commitment", False,
     "Clay Pace", "President of Commercial & Technology, Seatex, LLC, Houston",
     "Clay Pace of Seatex in a video interview at IPP’s SOCMA 2024 booth"),
    ("Kz6N9uacqkY", "Communication and quick customer response are what sets IPP apart", False,
     "Anna Nguyen", "Commercial Sales & Operations Manager, Hoyer Global",
     "Anna Nguyen of Hoyer Global in a video interview with IPP’s Keith West at SOCMA 2024"),
]
FEATURE_ID = "WlsjZMptSZg"

# (video id, card title, speaker or label, caption, thumbnail alt)
TEAM_VIDEOS = [
    ("j3ZA5moOMH8", "International Process Plants company overview", "International Process Plants",
     "Nearly half a century of process plants, process units and equipment for more than 160,000 customers worldwide.",
     "International Process Plants company overview video"),
    ("-Z7G91gTLZs", "Relocate, don’t build new: a hydrogen peroxide plant moved from Mexico to Türkiye", "Plant relocation",
     "A 10,000-ton/year plant on track to start up in about 18 months instead of four years, with more than 70% CAPEX "
     "savings on engineering and equipment.",
     "Hydrogen peroxide plant relocation from Mexico to Türkiye"),
    ("3BKFldn1FuY", "Why quality used process equipment delivers faster, smarter growth", "Ross Gale, Vice President, IPP Group",
     "How proven, in-stock process equipment lets manufacturers expand capacity quickly and cost-effectively.",
     "Ross Gale of International Process Plants on used process equipment"),
    ("I_msf-Bjsag", "Why used process equipment can be the smarter choice", "Ross Gale, Vice President, IPP Group",
     "Faster lead times and major capital savings from proven used process equipment.",
     "Ross Gale of International Process Plants explaining used versus new equipment"),
    ("eJ0BJhUpiIQ", "A thank-you from SOCMA 2024", "Keith West, Global Director of Equipment Sales",
     "A thank-you to the Society of Chemical Manufacturers & Affiliates after the 2024 SOCMA Show in Nashville.",
     "Keith West of International Process Plants at SOCMA 2024"),
]

STAR = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 '
        '4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="{c}"/></svg>')


def esc(s):
    return html.escape(s, quote=True)


def stars(n, size):
    n = max(0, min(5, int(round(n))))
    body = "".join(STAR.format(s=size, c="#f5a623" if i < n else "#cfdbe1") for i in range(5))
    return '<span class="tm-stars" role="img" aria-label="%d out of 5 stars">%s</span>' % (n, body)


def short_name(full):
    """First name plus last initial, as on the MHN page. Single names stay as Google shows them."""
    name = re.sub(r"\s*\([^)]*\)", "", full or "").strip()
    if not name:
        return "Google user"
    parts = name.split()
    if len(parts) == 1:
        return parts[0]
    last = parts[-1].strip(".")
    return "%s %s." % (parts[0], last[0].upper())


def paras(text):
    return [p.strip() for p in re.split(r"\n+", text or "") if p.strip()]


def load_profiles():
    profiles, written, rating_only, hidden = [], [], [], 0
    for fname, place in PROFILES:
        raw = json.loads((DATA / fname).read_text(encoding="utf-8"))
        res = raw["tasks"][0]["result"][0]
        items = [i for i in (res.get("items") or []) if i.get("type") == "google_reviews_search"]
        profiles.append({"place": place, "rating": res["rating"]["value"], "votes": res["rating"]["votes_count"],
                         "cid": res["cid"], "fetched": len(items), "pulled": (res.get("datetime") or "")[:10]})
        for it in items:
            rating = (it.get("rating") or {}).get("value") or 0
            owner = it.get("owner_answer") or ""
            r = {"place": place, "name": short_name(it.get("profile_name")), "rating": rating,
                 "translated": bool(it.get("original_review_text")), "paras": paras(it.get("review_text")),
                 "reply": paras(owner), "ts": it.get("timestamp") or ""}
            if r["paras"]:
                written.append(r)
            elif rating >= MIN_RATING_ONLY:
                rating_only.append(r)
            else:
                hidden += 1
    # Headquarters first, then newest first within each profile.
    order = {place: i for i, (_, place) in enumerate(PROFILES)}
    key = lambda r: (order[r["place"]], "".join(chr(0x10FFFF - ord(c)) for c in r["ts"]))
    return profiles, sorted(written, key=key) + sorted(rating_only, key=key), hidden


def maps(cid):
    return "https://www.google.com/maps?cid=%s" % cid


def thumb(vid, src, alt, w, h, lazy=True):
    return ('<a class="video-thumb" href="https://www.youtube.com/watch?v=%s" data-video="%s" target="_blank" '
            'rel="noopener noreferrer" aria-label="Play the video">'
            '<img src="%s" alt="%s" width="%d" height="%d"%s decoding="async">'
            '<span class="play-icon" aria-hidden="true">▶</span></a>'
            % (vid, vid, src, esc(alt), w, h, ' loading="lazy"' if lazy else ""))


def customer_card(v):
    vid, text, is_quote, name, role, alt = v
    words = ('<blockquote>“%s”</blockquote>' % esc(text)) if is_quote else ('<p class="video-title">%s</p>' % esc(text))
    return ('<li class="video-card">%s%s<p class="video-who"><strong>%s</strong>%s</p></li>'
            % (thumb(vid, "/assets/chemical/reviews/%s.webp" % vid, alt, 480, 270).replace(
                'aria-label="Play the video"', 'data-title="%s" aria-label="Play the video: %s"' % (esc(text), esc(text))),
               words, esc(name), esc(role)))


def team_card(v):
    vid, title, who, caption, alt = v
    return ('<li class="video-card">%s<p class="video-title">%s</p><p class="video-who"><strong>%s</strong>%s</p></li>'
            % (thumb(vid, "/assets/testimonials/%s.webp" % vid, alt, 960, 540).replace(
                'aria-label="Play the video"', 'data-title="%s" aria-label="Play the video: %s"' % (esc(title), esc(title))),
               esc(title), esc(who), esc(caption)))


def feature(v):
    vid, text, is_quote, name, role, alt = v
    t = thumb(vid, "/assets/testimonials/%s.webp" % vid, alt, 960, 540, lazy=False).replace(
        'aria-label="Play the video"', 'data-title="%s" aria-label="Play the video: %s"' % (esc(text), esc(text)))
    return ('      <figure class="tm-feature">%s<figcaption><blockquote>“%s”</blockquote>'
            '<p class="video-who"><strong>%s</strong>%s</p></figcaption></figure>' % (t, esc(text), esc(name), esc(role)))


def stats(profiles):
    # 160,000+ customers: live homepage ("a portfolio of more than 160,000 customers around the world").
    rows = [("160,000+", "Customers worldwide"), ("%d" % len(CUSTOMER_VIDEOS), "Customer video interviews, SOCMA 2024")]
    for p in profiles:
        rows.append(("%.1f" % p["rating"], '<a href="%s" target="_blank" rel="noopener">Google rating, %s</a> (%d reviews)'
                     % (maps(p["cid"]), esc(p["place"]), p["votes"])))
    return "\n".join('      <li><strong>%s</strong><span>%s</span></li>' % r for r in rows)


def review_card(r):
    src = "Google review · %s" % r["place"]
    if r["translated"]:
        src += " · translated by Google"
    if r["paras"]:
        body = '<blockquote>%s</blockquote>' % "".join("<p>%s</p>" % esc(p) for p in r["paras"])
    else:
        body = '<p class="tm-review-none">%d-star rating on Google, no written comment</p>' % int(round(r["rating"]))
    reply = ""
    if r["reply"]:
        reply = ('<div class="tm-reply"><span>Response from International Process Plants</span>%s</div>'
                 % "".join("<p>%s</p>" % esc(p) for p in r["reply"]))
    return ('<li><figure class="tm-review"><div class="tm-review-top">%s<span class="tm-review-src">%s</span></div>'
            '%s%s<figcaption>%s</figcaption></figure></li>'
            % (stars(r["rating"], 16), esc(src), body, reply, esc(r["name"])))


def slider(label, items_html, extra_class=""):
    return ('<div class="tm-slider" data-slider>\n'
            '      <ul class="tm-track%s" tabindex="0" aria-label="%s">\n%s\n      </ul>\n'
            '      <div class="tm-slider-nav" hidden><button type="button" class="tm-prev" aria-label="Previous">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button>'
            '<button type="button" class="tm-next" aria-label="Next"><svg viewBox="0 0 24 24" aria-hidden="true">'
            '<path d="M9 6l6 6-6 6"/></svg></button></div>\n    </div>'
            % (extra_class, esc(label), items_html))


def lift(src, start, end):
    i = src.index(start)
    j = src.index(end, i) + len(end)
    return src[i:j]


def main():
    hub = (ROOT / "case-studies" / "index.html").read_text(encoding="utf-8")
    header = lift(hub, '<header class="ipp-header">', '</header>')
    lang = lift(hub, '<div class="ipp-lang"', 'EN</div>')
    footer = lift(hub, '<footer class="ipp-footer">', '</footer>')
    burger = lift(hub, '<script>(function(){var h=document.querySelector(".ipp-header")', '</script>')

    profiles, reviews, hidden = load_profiles()
    page = TEMPLATE
    for key, val in {
        "@@TITLE@@": esc(TITLE), "@@DESC@@": esc(DESC),
        "@@HEADER@@": header, "@@LANG@@": lang, "@@FOOTER@@": footer, "@@BURGER@@": burger,
        "@@PULLED@@": ", ".join("%s %s" % (p["place"], p["pulled"]) for p in profiles),
        "@@FEATURE@@": feature(next(v for v in CUSTOMER_VIDEOS if v[0] == FEATURE_ID)),
        "@@STATS@@": stats(profiles),
        "@@CUSTOMER_SLIDER@@": slider("Customer video interviews", "\n".join(customer_card(v) for v in CUSTOMER_VIDEOS), " tm-videos"),
        "@@REVIEW_SLIDER@@": slider("Google reviews", "\n".join(review_card(r) for r in reviews), " tm-reviews"),
        "@@TEAM_SLIDER@@": slider("International Process Plants videos", "\n".join(team_card(v) for v in TEAM_VIDEOS), " tm-videos"),
        "@@PLAYLIST@@": PLAYLIST, "@@CHANNEL@@": CHANNEL,
        "@@MAPS_NJ@@": maps(profiles[0]["cid"]), "@@MAPS_SC@@": maps(profiles[1]["cid"]),
    }.items():
        page = page.replace(key, val)
    leftover = re.findall(r"@@[A-Z_]+@@", page)
    assert not leftover, leftover
    body = page.split("</header>")[1].split("<footer")[0]
    assert "—" not in body, "em dash in page copy"

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page, encoding="utf-8", newline="\n")
    print("wrote", OUT.relative_to(ROOT), len(page.encode("utf-8")), "bytes")
    for p in profiles:
        print("  %s: Google %.1f from %d reviews, fetched %d" % (p["place"], p["rating"], p["votes"], p["fetched"]))
    print("  review cards: %d (rating-only below %d stars not shown: %d)" % (len(reviews), MIN_RATING_ONLY, hidden))
    print("  customer videos: %d; team videos: %d" % (len(CUSTOMER_VIDEOS), len(TEAM_VIDEOS)))


TEMPLATE = """<!doctype html>
<!--
  REVIEWS AND TESTIMONIALS, International Process Plants
  Proposed new page: there is no /testimonials/ on the live site yet.
  GENERATED by tools/build_testimonials.py from data/testimonials/*.json.
  Do not edit by hand; change the script or the data and re-run it.
  Google reviews pulled: @@PULLED@@. Text untouched.
  No Review or AggregateRating markup, on purpose.
-->
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>@@TITLE@@</title>
  <meta name="description" content="@@DESC@@">
  <meta name="robots" content="noindex, nofollow">
  <link rel="canonical" href="https://internationalprocessplants.com/testimonials/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="International Process Plants">
  <meta property="og:title" content="@@TITLE@@">
  <meta property="og:description" content="@@DESC@@">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="@@TITLE@@">
  <meta name="twitter:description" content="@@DESC@@">
  <link rel="stylesheet" href="/assets/chemical/fonts.css">
  <link rel="stylesheet" href="/assets/chemical/page.css">
  <link rel="stylesheet" href="/assets/case-studies/case.css">
  <link rel="stylesheet" href="/assets/case-studies/site.css">
  <style>
  .visually-hidden{position:absolute!important;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
  .tm-stars{display:inline-flex;gap:2px;flex:none}
  .tm-stars svg{display:block;flex:none;width:16px;height:16px;max-width:none;stroke:none}
  /* hero: case-study layout (text left, featured interview right, stats strip below) */
  .tm-feature{margin:0;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.18)}
  .tm-feature figcaption{padding:18px 22px 20px}
  .tm-feature blockquote{margin:0 0 10px;font:600 18px/1.45 var(--heading);color:var(--ink)}
  .tm-feature .video-who{margin:0}
  .cs-stats a{color:#fff;text-decoration:underline;text-decoration-color:#7aafc5;text-underline-offset:3px}
  .cs-stats a:hover{color:#fff;text-decoration-color:#fff}
  /* section heading: the chemical page's split intro (H2 left, intro right) */
  .tm-split{display:grid;grid-template-columns:.9fr 1.1fr;gap:68px;align-items:start;margin-bottom:36px}
  .tm-split h2{margin:0;font-size:30px}
  .tm-split p{margin:0 0 14px;font-size:16px;line-height:1.75}
  .tm-split p:last-child,.tm-split .button-row{margin-bottom:0}
  .tm-split .button-row{margin-top:20px}
  .tm-split .button svg{width:15px;height:15px;flex:none}
  /* sliders: scroll-snap track, three cards across on desktop, arrows below */
  .tm-track{display:grid;grid-auto-flow:column;grid-auto-columns:calc((100% - 44px)/3);gap:22px;margin:0;padding:2px 2px 6px;
    list-style:none;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;overscroll-behavior-x:contain;scrollbar-width:none}
  .tm-track::-webkit-scrollbar{display:none}
  .tm-track>li{scroll-snap-align:start;min-width:0}
  .tm-track:focus-visible{outline:2px solid var(--blue);outline-offset:4px}
  .tm-track .video-card{height:100%}
  .tm-slider-nav{display:flex;justify-content:flex-end;gap:10px;margin-top:22px}
  .tm-slider-nav[hidden]{display:none}
  .tm-slider-nav button{display:grid;place-items:center;width:46px;height:46px;padding:0;border:1px solid #c6d8e0;border-radius:50%;
    background:#fff;color:var(--deep);cursor:pointer;transition:background .15s,color .15s,border-color .15s}
  .tm-slider-nav button:hover:not(:disabled){background:var(--navy);border-color:var(--navy);color:#fff}
  .tm-slider-nav button:disabled{opacity:.35;cursor:default}
  .tm-slider-nav svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2.2}
  /* Google review cards */
  .tm-review{display:flex;flex-direction:column;gap:14px;height:100%;margin:0;padding:24px;background:#fff;border:1px solid var(--line);border-radius:10px}
  .tm-review-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px 12px}
  .tm-review-src{font:600 12px/1.4 var(--heading);text-transform:uppercase;letter-spacing:.6px;color:var(--link)}
  .tm-review blockquote{margin:0;color:var(--ink);font:500 17px/1.55 var(--heading)}
  .tm-review blockquote p,.tm-reply p{margin:0}
  .tm-review-none{margin:0;color:var(--body);font-size:15px;font-style:italic}
  .tm-reply{padding:12px 14px;background:#f3f8fa;border-left:3px solid var(--blue);border-radius:0 6px 6px 0;font-size:14px;line-height:1.6;color:var(--body)}
  .tm-reply span{display:block;margin-bottom:4px;font:600 11px/1.4 var(--heading);text-transform:uppercase;letter-spacing:.6px;color:var(--deep)}
  .tm-review figcaption{margin-top:auto;padding-top:12px;border-top:1px solid var(--line);font-size:14px;font-weight:600;color:var(--deep)}
  @media(max-width:1100px){.tm-track{grid-auto-columns:calc((100% - 22px)/2)}}
  @media(max-width:860px){.tm-split{grid-template-columns:1fr;gap:14px;margin-bottom:28px}.tm-split h2{font-size:26px}
    .cs-cta-inner{flex-direction:column;align-items:flex-start}}
  @media(max-width:620px){.tm-track{grid-auto-columns:86%;gap:16px}.tm-slider-nav{justify-content:center}}
  @media(max-width:560px){.tm-split h2{font-size:24px}.tm-split p{font-size:15px}.tm-feature blockquote{font-size:16px}
    .tm-split .button-row .button{flex:1 1 100%}
    .cs-cta-buttons,.cs-cta-buttons .cs-button{width:100%;text-align:center}}
  </style>
  <script>document.documentElement.classList.add('js')</script>
</head>
<body class="cs-page">
<a class="skip-link" href="#main">Skip to content</a>
@@HEADER@@@@LANG@@
<main id="main">
<section class="cs-hero">
  <div class="container">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="https://internationalprocessplants.com/">Home</a><span aria-hidden="true">/</span><a href="https://internationalprocessplants.com/about-us/">About Us</a><span aria-hidden="true">/</span><span aria-current="page">Reviews and testimonials</span></nav>
    <div class="cs-hero-grid">
      <div>
        <h1>International Process Plants Reviews and Testimonials</h1>
        <p class="cs-standfirst">Chemical manufacturers describe working with International Process Plants in their own words: in video interviews recorded at the SOCMA 2024 show in Nashville, and in Google reviews of our New Jersey headquarters and South Carolina location.</p>
      </div>
@@FEATURE@@
    </div>
    <ul class="cs-stats" aria-label="Reviews at a glance">
@@STATS@@
    </ul>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="tm-split">
      <h2>What Do Chemical Manufacturers Say About International Process Plants?</h2>
      <div>
        <p>International Process Plants asked customers to rate us on a scale of 1 to 10. Four customers answered on camera at SOCMA 2024 in Nashville, from ChemDesign Products, Chemicals Incorporated, Seatex and Hoyer Global, speaking about our customer commitment, communication and long-term business relationships.</p>
        <p><a class="text-link" href="@@PLAYLIST@@" target="_blank" rel="noopener noreferrer">Watch the Customer Testimonials playlist ↗</a></p>
      </div>
    </div>
    @@CUSTOMER_SLIDER@@
  </div>
</section>

<section class="section reviews-section">
  <div class="container">
    <div class="tm-split">
      <h2>Google Reviews of International Process Plants</h2>
      <div>
        <p>Google lists two International Process Plants profiles: our headquarters in Princeton Junction, New Jersey, and our location in Eastover, South Carolina. Written reviews appear word for word, together with our replies, and each profile’s full rating and review count is on Google.</p>
        <div class="button-row">
          <a class="button" href="@@MAPS_NJ@@" target="_blank" rel="noopener">Princeton Junction, NJ reviews <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg></a>
          <a class="button" href="@@MAPS_SC@@" target="_blank" rel="noopener">Eastover, SC reviews <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg></a>
        </div>
      </div>
    </div>
    @@REVIEW_SLIDER@@
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="tm-split">
      <h2>International Process Plants on Video</h2>
      <div>
        <p>The International Process Plants team explains how relocated plants and used process equipment save manufacturers time and capital, from a company overview to a hydrogen peroxide plant moved from Mexico to Türkiye.</p>
        <p><a class="text-link" href="@@CHANNEL@@" target="_blank" rel="noopener noreferrer">Visit our YouTube channel ↗</a></p>
      </div>
    </div>
    @@TEAM_SLIDER@@
  </div>
</section>

<section class="cs-cta">
  <div class="container cs-cta-inner">
    <div><h2>Buying or selling a process plant?</h2><p>International Process Plants buys and sells used process plants and equipment worldwide. Our case studies show how idle plants found new owners and new uses.</p></div>
    <div class="cs-cta-buttons"><a class="cs-button" href="https://internationalprocessplants.com/contact/">Contact International Process Plants <span aria-hidden="true">→</span></a><a class="cs-button cs-button-outline" href="/case-studies/">Read our case studies</a></div>
  </div>
</section>
</main>
@@FOOTER@@
@@BURGER@@
<script>
// Videos play inline on click; the YouTube link stays as the no-script fallback.
document.querySelectorAll('.video-thumb[data-video]').forEach(function(link){
  link.addEventListener('click',function(e){
    if(e.metaKey||e.ctrlKey||e.shiftKey||e.button!==0)return;
    e.preventDefault();
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+link.dataset.video+'?autoplay=1&rel=0';
    f.title=link.dataset.title||'International Process Plants video';
    f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    f.allowFullscreen=true;
    var box=document.createElement('div');box.className='video-frame';box.appendChild(f);link.replaceWith(box);
  });
});
// Sliders: arrows scroll one card; arrows hide when every card already fits.
document.querySelectorAll('[data-slider]').forEach(function(s){
  var track=s.querySelector('.tm-track'),nav=s.querySelector('.tm-slider-nav'),
      prev=s.querySelector('.tm-prev'),next=s.querySelector('.tm-next');
  function step(){var li=track.querySelector('li');var gap=parseFloat(getComputedStyle(track).columnGap)||0;return li?li.getBoundingClientRect().width+gap:track.clientWidth;}
  function update(){
    var max=track.scrollWidth-track.clientWidth;
    nav.hidden=max<=2;
    prev.disabled=track.scrollLeft<=2;
    next.disabled=track.scrollLeft>=max-2;
  }
  prev.addEventListener('click',function(){track.scrollBy({left:-step()});});
  next.addEventListener('click',function(){track.scrollBy({left:step()});});
  track.addEventListener('scroll',function(){window.requestAnimationFrame(update);},{passive:true});
  window.addEventListener('resize',update);
  update();
});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
