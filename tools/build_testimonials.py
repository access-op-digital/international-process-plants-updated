"""Build testimonials/index.html: the proposed International Process Plants
reviews and testimonials page, on the same plan as the Modern House Numbers
testimonials page (hero with Google score pills, testimonials, Google reviews
word for word, closing band).

Run from the repo root:  python tools/build_testimonials.py

Inputs:
  data/testimonials/gbp-reviews-princeton-junction-nj.json
  data/testimonials/gbp-reviews-eastover-sc.json
      The two Google Business Profiles Google Maps lists for International
      Process Plants, pulled through DataForSEO business_data/google/reviews.
  case-studies/index.html
      Header, language tab and footer are lifted from it, so every review-site
      page carries the same live-site chrome.
  VIDEOS below
      The four customer interviews in the "Customer Testimonials" YouTube
      playlist that the live homepage embeds (PLRlhdb05DXKSO3XMiN2gd5-DduvcVPWHx).
      Wording, names and roles match the video cards already on the chemical
      page; the fifth playlist video is a company promo, not a testimonial.

Rules:
  - Review text is Google's, untouched (HTML-escaped only). Star-only reviews
    count in Google's rating but are not shown, as Google itself does.
  - Score pills show the rating and count Google reports, not a computed one.
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

PROFILES = [
    ("gbp-reviews-princeton-junction-nj.json", "Princeton Junction, NJ"),
    ("gbp-reviews-eastover-sc.json", "Eastover, SC"),
]

TITLE = "International Process Plants Reviews and Testimonials"
DESC = ("Read International Process Plants reviews: chemical manufacturers on video at SOCMA 2024, "
        "plus Google reviews of our New Jersey and South Carolina locations.")

# (video id, quote or title, is a direct quote, name, role, thumbnail alt)
VIDEOS = [
    ("1Qhma3r0Cas", "The International Process Plants team is outstanding! They understand my business", True,
     "Chuck Castley", "Commercial vice president, Chemicals Incorporated, Baytown, Texas",
     "Chuck Castley of Chemicals Incorporated in a video interview at IPP’s SOCMA 2024 booth"),
    ("WlsjZMptSZg", "If somebody asked me to rate IPP 1-10, I’d give them a 10 every time!", True,
     "Joel Salzman", "VP of Operations, ChemDesign Products, Inc., Marinette, Wisconsin",
     "Joel Salzman of ChemDesign Products in a video interview at IPP’s SOCMA 2024 booth"),
    ("BWWcZNOchrY", "The power of partnership: A testimonial to International Process Plants’ customer commitment", False,
     "Clay Pace", "President of Commercial & Technology, Seatex, LLC, Houston",
     "Clay Pace of Seatex in a video interview at IPP’s SOCMA 2024 booth"),
    ("Kz6N9uacqkY", "Communication and quick customer response are what sets IPP apart", False,
     "Anna Nguyen", "Commercial Sales & Operations Manager, Hoyer Global",
     "Anna Nguyen of Hoyer Global in a video interview with IPP’s Keith West at SOCMA 2024"),
]

STAR = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 '
        '4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="{c}"/></svg>')


def esc(s):
    return html.escape(s, quote=True)


def stars(n, size, label=True):
    n = max(0, min(5, int(round(n))))
    body = "".join(STAR.format(s=size, c="#f5a623" if i < n else "#cfdbe1") for i in range(5))
    if not label:
        return '<span class="tm-stars" aria-hidden="true">%s</span>' % body
    return '<span class="tm-stars" role="img" aria-label="%d out of 5 stars">%s</span>' % (n, body)


def short_name(full):
    """First name plus last initial, as on the MHN page. Handles and single
    names stay as Google shows them."""
    name = re.sub(r"\s*\([^)]*\)", "", full or "").strip()
    if not name:
        return "Google user"
    parts = name.split()
    if len(parts) == 1:
        return parts[0]
    last = parts[-1].strip(".")
    if len(last) == 1:
        return "%s %s." % (parts[0], last.upper())
    return "%s %s." % (parts[0], last[0].upper())


def load_profiles():
    profiles, shown = [], []
    for fname, place in PROFILES:
        raw = json.loads((DATA / fname).read_text(encoding="utf-8"))
        res = raw["tasks"][0]["result"][0]
        items = [i for i in (res.get("items") or []) if i.get("type") == "google_reviews_search"]
        profiles.append({"place": place, "rating": res["rating"]["value"], "votes": res["rating"]["votes_count"],
                         "cid": res["cid"], "fetched": len(items), "pulled": (res.get("datetime") or "")[:10]})
        for it in items:
            text = (it.get("review_text") or "").strip()
            if text:
                shown.append({"place": place, "cid": res["cid"], "name": short_name(it.get("profile_name")),
                              "rating": (it.get("rating") or {}).get("value") or 5,
                              "translated": bool(it.get("original_review_text")),
                              "paras": [p.strip() for p in re.split(r"\n+", text) if p.strip()]})
    return profiles, shown


def maps(cid):
    return "https://www.google.com/maps?cid=%s" % cid


def video_card(v):
    vid, text, is_quote, name, role, alt = v
    words = ('<blockquote>“%s”</blockquote>' % esc(text)) if is_quote else ('<p class="video-title">%s</p>' % esc(text))
    return ('<li class="video-card"><a class="video-thumb" href="https://www.youtube.com/watch?v=%s" data-video="%s" '
            'data-title="%s" target="_blank" rel="noopener noreferrer" aria-label="Play the video: %s">'
            '<img src="/assets/chemical/reviews/%s.webp" alt="%s" width="480" height="270" loading="lazy" decoding="async">'
            '<span class="play-icon" aria-hidden="true">▶</span></a>%s'
            '<p class="video-who"><strong>%s</strong>%s</p></li>'
            % (vid, vid, esc(text), esc(text), vid, esc(alt), words, esc(name), esc(role)))


FEATURE_ID = "WlsjZMptSZg"


def feature(v):
    vid, text, is_quote, name, role, alt = v
    return ('      <figure class="tm-feature"><a class="video-thumb" href="https://www.youtube.com/watch?v=%s" data-video="%s" '
            'data-title="%s" target="_blank" rel="noopener noreferrer" aria-label="Play the video: %s">'
            '<img src="/assets/testimonials/%s.webp" alt="%s" width="960" height="540" decoding="async">'
            '<span class="play-icon" aria-hidden="true">▶</span></a>'
            '<figcaption><blockquote>“%s”</blockquote><p class="video-who"><strong>%s</strong>%s</p></figcaption></figure>'
            % (vid, vid, esc(text), esc(text), vid, esc(alt), esc(text), esc(name), esc(role)))


def stats(profiles):
    # 160,000+ customers: live homepage ("a portfolio of more than 160,000 customers around the world").
    rows = [("160,000+", "Customers worldwide"), ("%d" % len(VIDEOS), "Customer video interviews, SOCMA 2024")]
    for p in profiles:
        rows.append(("%.1f" % p["rating"], '<a href="%s" target="_blank" rel="noopener">Google rating, %s</a> (%d reviews)'
                     % (maps(p["cid"]), esc(p["place"]), p["votes"])))
    return "\n".join('      <li><strong>%s</strong><span>%s</span></li>' % r for r in rows)


def review_card(r):
    src = "Google review · %s" % r["place"]
    if r["translated"]:
        src += " · translated by Google"
    return ('<li><figure class="tm-review"><div class="tm-review-top">%s<span class="tm-review-src">%s</span></div>'
            '<blockquote>%s</blockquote><figcaption>%s</figcaption></figure></li>'
            % (stars(r["rating"], 16), esc(src), "".join("<p>%s</p>" % esc(p) for p in r["paras"]), esc(r["name"])))


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

    profiles, shown = load_profiles()
    page = TEMPLATE
    for key, val in {
        "@@TITLE@@": esc(TITLE), "@@DESC@@": esc(DESC),
        "@@HEADER@@": header, "@@LANG@@": lang, "@@FOOTER@@": footer, "@@BURGER@@": burger,
        "@@PULLED@@": ", ".join("%s %s" % (p["place"], p["pulled"]) for p in profiles),
        "@@FEATURE@@": feature(next(v for v in VIDEOS if v[0] == FEATURE_ID)),
        "@@STATS@@": stats(profiles),
        "@@VIDEOS@@": "\n".join(video_card(v) for v in VIDEOS if v[0] != FEATURE_ID),
        "@@REVIEWS@@": "\n".join(review_card(r) for r in shown),
        "@@PLAYLIST@@": PLAYLIST,
        "@@MAPS_NJ@@": maps(profiles[0]["cid"]), "@@MAPS_SC@@": maps(profiles[1]["cid"]),
    }.items():
        page = page.replace(key, val)
    leftover = re.findall(r"@@[A-Z_]+@@", page)
    assert not leftover, leftover
    assert "—" not in page.split("</header>")[1].split("<footer")[0], "em dash in page copy"

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(page, encoding="utf-8", newline="\n")
    print("wrote", OUT.relative_to(ROOT), len(page.encode("utf-8")), "bytes")
    for p in profiles:
        print("  %s: Google %.1f from %d reviews, fetched %d" % (p["place"], p["rating"], p["votes"], p["fetched"]))
    print("  reviews with text shown: %d; videos: %d" % (len(shown), len(VIDEOS)))


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
  .tm-feature .video-thumb{border-radius:0}
  .tm-feature figcaption{padding:18px 22px 20px}
  .tm-feature blockquote{margin:0 0 10px;font:600 18px/1.45 var(--heading);color:var(--ink)}
  .tm-feature .video-who{margin:0}
  .cs-stats a{color:#fff;text-decoration:underline;text-decoration-color:#7aafc5;text-underline-offset:3px}
  .cs-stats a:hover{color:#fff;text-decoration-color:#fff}
  /* section heading: the chemical page's split intro (H2 left, intro right) */
  .tm-split{display:grid;grid-template-columns:.9fr 1.1fr;gap:68px;align-items:start;margin-bottom:36px}
  .tm-split h2{margin:0;font-size:30px}
  .tm-split p{margin:0 0 14px;font-size:16px;line-height:1.75}
  .tm-split p:last-child{margin-bottom:0}
  .tm-videos{grid-template-columns:repeat(3,minmax(0,1fr))}
  /* Google review wall */
  .tm-wall{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;margin:0;padding:0;list-style:none}
  .tm-review{display:flex;flex-direction:column;gap:14px;height:100%;margin:0;padding:24px;background:#fff;border:1px solid var(--line);border-radius:10px}
  .tm-review-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px 12px}
  .tm-review-src{font:600 12px/1.4 var(--heading);text-transform:uppercase;letter-spacing:.6px;color:var(--link)}
  .tm-review blockquote{flex-grow:1;margin:0;color:var(--ink);font:500 17px/1.55 var(--heading)}
  .tm-review blockquote p{margin:0}
  .tm-review figcaption{padding-top:12px;border-top:1px solid var(--line);font-size:14px;font-weight:600;color:var(--deep)}
  @media(max-width:860px){.tm-split{grid-template-columns:1fr;gap:14px;margin-bottom:28px}.tm-split h2{font-size:26px}
    .cs-cta-inner{flex-direction:column;align-items:flex-start}}
  @media(max-width:700px){.tm-videos,.tm-wall{grid-template-columns:1fr}}
  @media(max-width:560px){.tm-split h2{font-size:24px}.tm-split p{font-size:15px}.tm-feature blockquote{font-size:16px}
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
        <p>International Process Plants asked customers to rate us on a scale of 1 to 10. Four customers answered on camera at SOCMA 2024 in Nashville: Joel Salzman of ChemDesign Products, featured above, and customers from Chemicals Incorporated, Seatex and Hoyer Global, who speak about our customer commitment, communication and long-term business relationships.</p>
        <p><a class="text-link" href="@@PLAYLIST@@" target="_blank" rel="noopener noreferrer">Watch the Customer Testimonials playlist ↗</a></p>
      </div>
    </div>
    <ul class="video-reviews tm-videos">
@@VIDEOS@@
    </ul>
  </div>
</section>

<section class="section reviews-section">
  <div class="container">
    <div class="tm-split">
      <h2>Google Reviews of International Process Plants</h2>
      <div>
        <p>Google lists two International Process Plants profiles: our headquarters in Princeton Junction, New Jersey, and our location in Eastover, South Carolina. Reviews with written comments appear word for word, and star-only reviews count toward each profile’s rating on Google.</p>
        <p>Read every review on Google: <a class="text-link" href="@@MAPS_NJ@@" target="_blank" rel="noopener">Princeton Junction, NJ ↗</a> and <a class="text-link" href="@@MAPS_SC@@" target="_blank" rel="noopener">Eastover, SC ↗</a></p>
      </div>
    </div>
    <ul class="tm-wall">
@@REVIEWS@@
    </ul>
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
// Testimonial videos play inline on click; the YouTube link stays as the no-script fallback.
document.querySelectorAll('.video-thumb[data-video]').forEach(function(link){
  link.addEventListener('click',function(e){
    if(e.metaKey||e.ctrlKey||e.shiftKey||e.button!==0)return;
    e.preventDefault();
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+link.dataset.video+'?autoplay=1&rel=0';
    f.title=link.dataset.title||'Customer testimonial video';
    f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    f.allowFullscreen=true;
    var box=document.createElement('div');box.className='video-frame';box.appendChild(f);link.replaceWith(box);
  });
});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
