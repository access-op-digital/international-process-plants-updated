#!/usr/bin/env python3
"""
Convert IPP equipment landing page HTML files into clean, readable
markdown files for client review.

Output: docs/client-review/*.md
No external dependencies - uses only Python standard library.

v3 — Sequential DOM walk: processes HTML top-to-bottom between </header>
     and <footer, converting every visible element to markdown.
     No pattern-specific extractors — nothing gets dropped.
"""

import os
import re
import html as html_module
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EQUIPMENT_DIR = BASE_DIR / "equipment"
OUTPUT_DIR = BASE_DIR / "docs" / "client-review"


# ---------------------------------------------------------------------------
# Utility: decode HTML entities
# ---------------------------------------------------------------------------
def decode_entities(text: str) -> str:
    """Decode all HTML entities including named, decimal, and hex."""
    text = html_module.unescape(text)
    # Catch any remaining numeric refs
    text = re.sub(r"&#x([0-9a-fA-F]+);", lambda m: chr(int(m.group(1), 16)), text)
    text = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), text)
    return text


def clean_whitespace(text: str) -> str:
    """Collapse runs of whitespace into single spaces and strip."""
    return re.sub(r"\s+", " ", text).strip()


def strip_tags(text: str) -> str:
    """Remove all HTML tags but preserve text content."""
    text = re.sub(r"<br\s*/?>", " ", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text


# ---------------------------------------------------------------------------
# Main conversion: sequential HTML-to-markdown
# ---------------------------------------------------------------------------
def html_to_markdown(html_content: str) -> str:
    """Convert full HTML page to markdown by sequential DOM walk."""

    # ── Step 1: Extract body content between </header> and <footer ──
    header_end = re.search(r"</header>", html_content)
    if header_end:
        body = html_content[header_end.end():]
    else:
        body = html_content

    # Cut at <footer
    footer_start = re.search(r"<footer[\s>]", body)
    if footer_start:
        body = body[:footer_start.start()]

    # ── Step 1b: Pre-extract hero featured products before HTML gets processed ──
    _hero_featured = []
    hero_img_m = re.search(r'<div\s+class="hero-image"[^>]*>(.*?)(?=</div>\s*</div>\s*</div>\s*</section>)', body, re.DOTALL)
    if not hero_img_m:
        hero_img_m = re.search(r'<div\s+class="hero-image"[^>]*>(.*)', body, re.DOTALL)
    if hero_img_m:
        img_block = hero_img_m.group(1)
        for card_m in re.finditer(
            r'<a\s+href="([^"]*)"[^>]*>.*?'
            r'font-size:\s*17px[^"]*"[^>]*>([^<]*)</div>\s*'
            r'<div\s+style="font-size:\s*13px[^"]*">([^<]*)</div>',
            img_block, re.DOTALL
        ):
            url = card_m.group(1).strip()
            name = decode_entities(card_m.group(2).strip())
            condition = decode_entities(card_m.group(3).strip())
            if name:
                _hero_featured.append((name, condition, url))

    # ── Step 2: Remove blocks we want to skip entirely ──

    # Remove <style>...</style>
    body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.DOTALL)

    # Remove <script>...</script> (including JSON-LD)
    body = re.sub(r"<script[^>]*>.*?</script>", "", body, flags=re.DOTALL)

    # Remove <nav>...</nav>
    body = re.sub(r"<nav[^>]*>.*?</nav>", "", body, flags=re.DOTALL)

    # Remove <meta ... /> and <link ... />
    body = re.sub(r"<meta[^>]*/?>", "", body)
    body = re.sub(r"<link[^>]*/?>", "", body)

    # Remove internal review bar
    body = re.sub(r'<div\s+class="internal-review-bar"[^>]*>.*?</div>', "", body, flags=re.DOTALL)

    # Remove source-toggle
    body = re.sub(r'<div\s+class="source-toggle"[^>]*>.*?</div>', "", body, flags=re.DOTALL)

    # ── Step 3: Strip source annotations ──

    # <span class="src src-*" data-src-label="...">TEXT</span> → TEXT
    body = re.sub(
        r'<span\s+class="src\s+src-[^"]*"[^>]*>(.*?)</span>',
        r"\1", body, flags=re.DOTALL
    )

    # <li class="src src-*" data-src-label="...">TEXT</li> → <li>TEXT</li>
    body = re.sub(
        r'<li\s+class="src\s+src-[^"]*"[^>]*>(.*?)</li>',
        r"<li>\1</li>", body, flags=re.DOTALL
    )

    # <div class="hero-stat src src-*" ...> → <div class="hero-stat">
    body = re.sub(
        r'<div\s+class="hero-stat\s+src\s+src-[^"]*"[^>]*>',
        '<div class="hero-stat">', body
    )

    # Remove <a class="src-link">...</a>
    body = re.sub(r'<a\s+[^>]*class="src-link"[^>]*>.*?</a>', "", body, flags=re.DOTALL)

    # ── Step 4: Strip Font Awesome icons ──
    body = re.sub(r'<i\s+class="fa[sbrl]?\s+fa-[^"]*"[^>]*>\s*</i>', "", body)

    # ── Step 5: Convert <br> to space ──
    body = re.sub(r"<br\s*/?>", " ", body)

    # ── Step 6: Strip arrow/collapse elements ──
    body = re.sub(r'<span\s+class="arrow-expand"[^>]*>.*?</span>', "", body, flags=re.DOTALL)
    body = re.sub(r'<span\s+class="arrow-collapse"[^>]*>.*?</span>', "", body, flags=re.DOTALL)
    body = re.sub(r'<span\s+class="truncated"[^>]*>.*?</span>', "", body, flags=re.DOTALL)

    # ── Step 7: Convert links <a href="URL">TEXT</a> → [TEXT](URL) ──
    # But skip tab-nav buttons and non-content links
    def convert_link(m):
        full_tag = m.group(0)
        href = m.group(1)
        inner_html = m.group(2)
        # Strip tags from inner to get visible text
        text = clean_whitespace(strip_tags(decode_entities(inner_html)))
        if not text:
            return ""
        return f"[{text}]({href})"

    body = re.sub(
        r'<a\s+[^>]*href="([^"]*)"[^>]*>(.*?)</a>',
        convert_link, body, flags=re.DOTALL
    )

    # ── Step 8: Process the body sequentially ──
    lines = []

    # Split into logical blocks at section boundaries, cta-banner divs, etc.
    # We'll process the HTML in chunks, recognizing structural elements.

    # Process sections, cta-banners, and other top-level blocks
    # Split at <section or <div class="cta-banner" or generic styled divs at section level
    # Strategy: find all structural elements and process them in order

    _process_body(body, lines)

    # ── Step 8b: Inject pre-extracted hero featured products after the first --- ──
    if _hero_featured:
        featured_block = ["", "**Featured Equipment:**"]
        for name, condition, url in _hero_featured:
            featured_block.append(f"- [{name} -- {condition}]({url})")
        featured_block.append("")
        # Insert after the Quick Stats line or after the first ---
        insert_idx = None
        for i, line in enumerate(lines):
            if line.startswith("**Quick Stats:**"):
                insert_idx = i + 1
                break
        if insert_idx is None:
            for i, line in enumerate(lines):
                if line.strip() == "---":
                    insert_idx = i
                    break
        if insert_idx is not None:
            for j, fline in enumerate(featured_block):
                lines.insert(insert_idx + j, fline)

    # ── Step 9: Clean up the output ──
    result = "\n".join(lines)

    # Decode any remaining entities
    result = decode_entities(result)

    # Clean up excessive blank lines (max 2 consecutive)
    result = re.sub(r"\n{4,}", "\n\n\n", result)

    # Clean up whitespace at line ends
    result = re.sub(r"[ \t]+\n", "\n", result)

    # Remove trailing whitespace
    result = result.strip() + "\n"

    return result


def _process_body(body: str, lines: list):
    """Process the body HTML sequentially, appending markdown lines."""

    # Tokenize: find structural elements in order
    # We look for: <section...>...</section>, <div class="cta-banner">...</div>,
    # top-level <div style="..."> blocks (cross-sell), etc.

    # Pattern to find top-level structural blocks
    # We iterate through looking for opening tags of interest
    pos = 0

    while pos < len(body):
        # Find the next structural element
        next_section = _find_next(body, pos, r'<section[\s>]')
        next_cta = _find_next(body, pos, r'<div\s+class="cta-banner"')
        next_styled_div = _find_next(body, pos, r'<div\s+style="[^"]*background[^"]*padding')

        # Find minimum
        candidates = []
        if next_section is not None:
            candidates.append(('section', next_section))
        if next_cta is not None:
            candidates.append(('cta', next_cta))
        if next_styled_div is not None:
            candidates.append(('styled_div', next_styled_div))

        if not candidates:
            break

        block_type, block_start = min(candidates, key=lambda x: x[1])

        # Any text between pos and block_start is "gap" content — check for meaningful text
        gap = body[pos:block_start]
        gap_text = clean_whitespace(strip_tags(gap))
        if gap_text and len(gap_text) > 5:
            # There might be headings or content in the gap
            _process_inline_html(gap, lines)

        if block_type == 'section':
            # Find closing </section>
            section_end = _find_closing_tag(body, block_start, 'section')
            if section_end is None:
                section_end = len(body)
            section_html = body[block_start:section_end]
            _process_section(section_html, lines)
            pos = section_end

        elif block_type == 'cta':
            # Find the end of this cta-banner div (nested div handling)
            cta_end = _find_closing_tag(body, block_start, 'div')
            if cta_end is None:
                cta_end = len(body)
            cta_html = body[block_start:cta_end]
            _process_cta_banner(cta_html, lines)
            pos = cta_end

        elif block_type == 'styled_div':
            div_end = _find_closing_tag(body, block_start, 'div')
            if div_end is None:
                div_end = len(body)
            div_html = body[block_start:div_end]
            _process_styled_div(div_html, lines)
            pos = div_end


def _find_next(body: str, pos: int, pattern: str):
    """Find next occurrence of pattern after pos, return start index or None."""
    m = re.search(pattern, body[pos:])
    if m:
        return pos + m.start()
    return None


def _find_closing_tag(body: str, start: int, tag: str) -> int:
    """Find the closing tag, handling nesting. Returns position after closing tag."""
    # Find the end of the opening tag first
    open_tag_end = body.find('>', start)
    if open_tag_end < 0:
        return None

    depth = 1
    pos = open_tag_end + 1
    open_re = re.compile(rf'<{tag}[\s>]')
    close_re = re.compile(rf'</{tag}\s*>')

    while depth > 0 and pos < len(body):
        next_open = open_re.search(body[pos:])
        next_close = close_re.search(body[pos:])

        if next_close is None:
            return None

        open_pos = pos + next_open.start() if next_open else len(body)
        close_pos = pos + next_close.start()

        if open_pos < close_pos:
            depth += 1
            pos = open_pos + 1
        else:
            depth -= 1
            if depth == 0:
                return pos + next_close.end()
            pos = close_pos + 1

    return None


def _process_section(section_html: str, lines: list):
    """Process a <section> block into markdown."""
    lines.append("")
    lines.append("---")
    lines.append("")

    # Check for section ID to detect type
    id_m = re.search(r'<section[^>]*id="([^"]*)"', section_html)
    section_id = id_m.group(1) if id_m else ""

    # Extract section header (h2 + intro p)
    _extract_section_header(section_html, lines)

    # Detect section type and process accordingly
    has_tabs = bool(re.search(r'class="tab-content', section_html))
    has_product_cards = bool(re.search(r'class="product-card"', section_html))
    has_faq = bool(re.search(r'class="faq-question"', section_html))
    has_comparison_table = bool(re.search(r'class="comparison-table"', section_html))
    has_advantage_cards = bool(re.search(r'class="advantage-card"', section_html))
    has_process_steps = bool(re.search(r'class="process-step"', section_html))
    has_industry_tags = bool(re.search(r'class="industry-tag"', section_html))

    if has_faq or "faq" in section_id:
        _process_faq_section(section_html, lines)
    elif has_comparison_table or "comparison" in section_id or "used-vs-new" in section_id:
        _process_comparison_section(section_html, lines)
    elif has_advantage_cards or "advantages" in section_id or "why-ipp" in section_id:
        _process_advantages_section(section_html, lines)
    elif has_process_steps or "process" in section_id:
        _process_process_section(section_html, lines)
    elif has_industry_tags or "industries" in section_id:
        _process_industries_section(section_html, lines)
    elif has_tabs or has_product_cards:
        _process_product_tabs_section(section_html, lines)
    elif "hero" in section_html[:200]:
        _process_hero_section(section_html, lines)
    else:
        # Generic section: extract all content
        _process_generic_section(section_html, lines)


def _extract_section_header(section_html: str, lines: list):
    """Extract H2 heading and section-header intro paragraph."""
    # H2
    h2_m = re.search(r"<h2[^>]*>(.*?)</h2>", section_html, re.DOTALL)
    if h2_m:
        h2_text = clean_whitespace(strip_tags(decode_entities(h2_m.group(1))))
        lines.append(f"## {h2_text}")
        lines.append("")

    # Section header intro paragraph
    header_m = re.search(r'<div\s+class="section-header">(.*?)</div>', section_html, re.DOTALL)
    if header_m:
        for p_m in re.finditer(r"<p[^>]*>(.*?)</p>", header_m.group(1), re.DOTALL):
            text = clean_whitespace(strip_tags(decode_entities(p_m.group(1))))
            if text:
                lines.append(text)
                lines.append("")


def _process_hero_section(section_html: str, lines: list):
    """Process the hero section: H1, intro, stats, featured products, CTAs."""

    # H1
    h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", section_html, re.DOTALL)
    if h1_m:
        h1_text = clean_whitespace(strip_tags(decode_entities(h1_m.group(1))))
        # Replace the --- ## line we already added with # title
        # Remove the last few lines (the empty section header)
        while lines and (lines[-1] == "" or lines[-1] == "---"):
            lines.pop()
        lines.append(f"# {h1_text}")
        lines.append("")

    # Intro text paragraph
    intro_m = re.search(r'<p\s+class="intro-text">(.*?)</p>', section_html, re.DOTALL)
    if intro_m:
        text = clean_whitespace(strip_tags(decode_entities(intro_m.group(1))))
        if text:
            lines.append(text)
            lines.append("")

    # Details/expand content
    details_m = re.search(r'<details\s+class="intro-expand">(.*?)</details>', section_html, re.DOTALL)
    if details_m:
        details_html = details_m.group(1)
        for p_m in re.finditer(r'<p\s+class="intro-rest">(.*?)</p>', details_html, re.DOTALL):
            text = clean_whitespace(strip_tags(decode_entities(p_m.group(1))))
            if text:
                lines.append(text)
                lines.append("")

    # Hero CTA buttons
    cta_group = re.search(r'<div\s+class="hero-cta-group">(.*?)</div>', section_html, re.DOTALL)
    if cta_group:
        btns = _extract_md_links(cta_group.group(1))
        if btns:
            lines.append(" | ".join(btns))
            lines.append("")

    # Hero stats
    stats = []
    for stat_m in re.finditer(r'<div\s+class="hero-stat[^"]*"[^>]*>(.*?)</div>', section_html, re.DOTALL):
        stat_html = stat_m.group(1)
        num_m = re.search(r'<span\s+class="number">(.*?)</span>', stat_html, re.DOTALL)
        lab_m = re.search(r'<span\s+class="label">(.*?)</span>', stat_html, re.DOTALL)
        if num_m and lab_m:
            number = clean_whitespace(strip_tags(decode_entities(num_m.group(1))))
            label = clean_whitespace(strip_tags(decode_entities(lab_m.group(1))))
            stats.append(f"{number} {label}")
    if stats:
        lines.append(f"**Quick Stats:** {' | '.join(stats)}")
        lines.append("")

    # Hero featured products are now extracted pre-processing and injected by the caller


def _process_product_tabs_section(section_html: str, lines: list):
    """Process product tab sections (by-material, by-manufacturer, by-condition)."""

    # Tab nav buttons are already skipped (they're UI chrome)
    # Skip <button> elements in tab-nav
    # Process each tab-content div

    tab_contents = list(re.finditer(
        r'<div\s+class="tab-content[^"]*"[^>]*id="([^"]*)"[^>]*>(.*?)(?=<div\s+class="tab-content|$)',
        section_html, re.DOTALL
    ))

    # Also try faq-tab-content pattern
    if not tab_contents:
        tab_contents = list(re.finditer(
            r'<div\s+class="faq-tab-content[^"]*"[^>]*id="([^"]*)"[^>]*>(.*?)(?=<div\s+class="faq-tab-content|$)',
            section_html, re.DOTALL
        ))

    for tc_m in tab_contents:
        tab_id = tc_m.group(1)
        tab_html = tc_m.group(2)

        # Tab heading H3
        h3_m = re.search(r'<h3[^>]*style="[^"]*font-size:\s*22px[^"]*"[^>]*>(.*?)</h3>', tab_html, re.DOTALL)
        if h3_m:
            h3_text = clean_whitespace(strip_tags(decode_entities(h3_m.group(1))))
            lines.append(f"### {h3_text}")
            lines.append("")

        # Tab intro paragraph
        p_m = re.search(r'<p\s+style="[^"]*(?:color|margin)[^"]*"[^>]*>(.*?)</p>', tab_html, re.DOTALL)
        if p_m:
            text = clean_whitespace(strip_tags(decode_entities(p_m.group(1))))
            if text:
                lines.append(text)
                lines.append("")

        # Product cards
        _process_product_cards(tab_html, lines)

        # Browse all link (already converted to markdown link format)
        browse_m = re.search(r'\[([^\]]*[Bb]rowse\s+[Aa]ll[^\]]*)\]\(([^)]+)\)', tab_html)
        if browse_m:
            lines.append(f"[{browse_m.group(1)}]({browse_m.group(2)})")
            lines.append("")

    # If no tab contents found, check for direct product cards (no tabs)
    if not tab_contents:
        # Check if there are product cards directly in the section
        if '<div class="product-card">' in section_html or "product-card" in section_html:
            _process_product_cards(section_html, lines)
            # Browse all link
            browse_m = re.search(r'\[([^\]]*[Bb]rowse\s+[Aa]ll[^\]]*)\]\(([^)]+)\)', section_html)
            if browse_m:
                lines.append(f"[{browse_m.group(1)}]({browse_m.group(2)})")
                lines.append("")
        else:
            _process_generic_section(section_html, lines)


def _process_product_cards(tab_html: str, lines: list):
    """Extract product cards from a tab content block."""
    card_splits = re.split(r'<div\s+class="product-card(?:\s[^-][^"]*)?"', tab_html)

    for i, card_html in enumerate(card_splits):
        if i == 0:
            continue

        # Badge
        badge_m = re.search(r'<div\s+class="badge[^"]*"[^>]*>(.*?)</div>', card_html, re.DOTALL)
        badge_text = ""
        if badge_m:
            badge_text = clean_whitespace(strip_tags(decode_entities(badge_m.group(1))))

        # Card title (h3 inside card body)
        h3_m = re.search(r"<h3[^>]*>(.*?)</h3>", card_html, re.DOTALL)
        title = ""
        if h3_m:
            title = clean_whitespace(strip_tags(decode_entities(h3_m.group(1))))

        # IPP# link
        ipp_link_m = re.search(
            r'\[View IPP#\s*(\d+)\]\((https?://[^)]+)\)',
            card_html
        )
        if not ipp_link_m:
            ipp_link_m = re.search(
                r'\[([^\]]*IPP#\s*(\d+)[^\]]*)\]\(([^)]+)\)',
                card_html
            )

        ipp_num = ""
        ipp_url = ""
        if ipp_link_m:
            groups = ipp_link_m.groups()
            if len(groups) == 2:
                ipp_num = groups[0]  # The number from "View IPP# NNN"
                ipp_url = groups[1]
            elif len(groups) == 3:
                ipp_num = groups[1]
                ipp_url = groups[2]

        # Card heading
        if title:
            heading = f"#### {title}"
            if badge_text:
                heading = f"#### [{badge_text}] {title}"
            if ipp_num and ipp_url:
                heading += f" ([IPP# {ipp_num}]({ipp_url}))"
            lines.append(heading)
            lines.append("")

        # Card description
        desc_m = re.search(r'<p\s+class="card-desc">(.*?)</p>', card_html, re.DOTALL)
        if desc_m:
            desc = clean_whitespace(strip_tags(decode_entities(desc_m.group(1))))
            if desc:
                lines.append(desc)
                lines.append("")

        # Specs list items
        for li_m in re.finditer(r"<li[^>]*>(.*?)</li>", card_html, re.DOTALL):
            li_text = clean_whitespace(strip_tags(decode_entities(li_m.group(1))))
            if li_text:
                lines.append(f"- {li_text}")

        # Card footer links (Request Specs, View IPP#)
        footer_links = []
        for link_m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', card_html):
            text = link_m.group(1)
            url = link_m.group(2)
            # Skip if it's the browse-all link or already handled
            if "Browse All" in text:
                continue
            footer_links.append(f"[{text}]({url})")

        if footer_links:
            lines.append("")
            lines.append(" | ".join(footer_links))

        lines.append("")


def _process_faq_section(section_html: str, lines: list):
    """Process FAQ section: extract all Q&A pairs from all tab groups."""

    # Find all questions
    questions = list(re.finditer(
        r'<button\s+class="faq-question"[^>]*>(.*?)</button>',
        section_html, re.DOTALL
    ))

    # Find all answers
    answers = list(re.finditer(
        r'<div\s+class="faq-answer"[^>]*>(.*?)</div>\s*(?:</div>|$)',
        section_html, re.DOTALL
    ))

    for i, q_m in enumerate(questions):
        q_text = clean_whitespace(strip_tags(decode_entities(q_m.group(1))))
        lines.append(f"**Q: {q_text}**")

        if i < len(answers):
            a_text = clean_whitespace(strip_tags(decode_entities(answers[i].group(1))))
            lines.append(f"A: {a_text}")
        lines.append("")


def _process_comparison_section(section_html: str, lines: list):
    """Process comparison table section."""

    # Table
    table_m = re.search(r"<table[^>]*>(.*?)</table>", section_html, re.DOTALL)
    if not table_m:
        _process_generic_section(section_html, lines)
        return

    table_html = table_m.group(1)
    rows = []

    # Headers
    thead_m = re.search(r"<thead>(.*?)</thead>", table_html, re.DOTALL)
    if thead_m:
        ths = re.findall(r"<th[^>]*>(.*?)</th>", thead_m.group(1), re.DOTALL)
        headers = [clean_whitespace(strip_tags(decode_entities(th))) for th in ths]
        rows.append("| " + " | ".join(headers) + " |")
        rows.append("|" + "|".join(["-----" for _ in headers]) + "|")

    # Body rows
    tbody_m = re.search(r"<tbody>(.*?)</tbody>", table_html, re.DOTALL)
    if tbody_m:
        for tr_m in re.finditer(r"<tr>(.*?)</tr>", tbody_m.group(1), re.DOTALL):
            cells = re.findall(r"<td[^>]*>(.*?)</td>", tr_m.group(1), re.DOTALL)
            cell_texts = [clean_whitespace(strip_tags(decode_entities(c))) for c in cells]
            if any(cell_texts):
                rows.append("| " + " | ".join(cell_texts) + " |")

    if rows:
        lines.extend(rows)
        lines.append("")

    # Also check for content after the table (additional comparison grids)
    after_table = section_html[table_m.end():]
    _extract_remaining_content(after_table, lines)


def _process_advantages_section(section_html: str, lines: list):
    """Process advantages/why-ipp section with advantage cards."""

    # Advantage cards
    card_splits = re.split(r'<div\s+class="advantage-card[^"]*"[^>]*>', section_html)
    for i, card in enumerate(card_splits):
        if i == 0:
            continue
        h3_m = re.search(r"<h3[^>]*>(.*?)</h3>", card, re.DOTALL)
        p_m = re.search(r"<p[^>]*>(.*?)</p>", card, re.DOTALL)

        if h3_m:
            title = clean_whitespace(strip_tags(decode_entities(h3_m.group(1))))
            lines.append(f"### {title}")
        if p_m:
            text = clean_whitespace(strip_tags(decode_entities(p_m.group(1))))
            if text:
                lines.append(text)
        lines.append("")

    # If no advantage-card divs found, try generic extraction
    if len(card_splits) <= 1:
        _process_generic_section(section_html, lines)


def _process_process_section(section_html: str, lines: list):
    """Process how-it-works / process steps section."""

    step_splits = re.split(r'<div\s+class="process-step[^"]*"[^>]*>', section_html)
    step_num = 0
    for i, step in enumerate(step_splits):
        if i == 0:
            continue
        step_num += 1
        h4_m = re.search(r"<h4[^>]*>(.*?)</h4>", step, re.DOTALL)
        p_m = re.search(r"<p[^>]*>(.*?)</p>", step, re.DOTALL)

        title = clean_whitespace(strip_tags(decode_entities(h4_m.group(1)))) if h4_m else f"Step {step_num}"
        desc = clean_whitespace(strip_tags(decode_entities(p_m.group(1)))) if p_m else ""

        lines.append(f"{step_num}. **{title}** -- {desc}")

    if step_num > 0:
        lines.append("")

    # If no process-step divs found, try generic
    if len(step_splits) <= 1:
        _process_generic_section(section_html, lines)


def _process_industries_section(section_html: str, lines: list):
    """Process industries section with industry tags."""

    for im in re.finditer(r'<div\s+class="industry-tag[^"]*"[^>]*>(.*?)</div>', section_html, re.DOTALL):
        tag_text = clean_whitespace(strip_tags(decode_entities(im.group(1))))
        if tag_text:
            lines.append(f"- {tag_text}")

    lines.append("")


def _process_cta_banner(cta_html: str, lines: list):
    """Process a CTA banner div into markdown blockquote."""
    lines.append("")
    lines.append("---")
    lines.append("")

    h2_m = re.search(r"<h2[^>]*>(.*?)</h2>", cta_html, re.DOTALL)
    if h2_m:
        heading = clean_whitespace(strip_tags(decode_entities(h2_m.group(1))))
        lines.append(f"## {heading}")
        lines.append("")

    for p_m in re.finditer(r"<p[^>]*>(.*?)</p>", cta_html, re.DOTALL):
        text = clean_whitespace(strip_tags(decode_entities(p_m.group(1))))
        if text:
            lines.append(text)
            lines.append("")

    # CTA buttons (already converted to markdown links)
    btns = _extract_md_links(cta_html)
    if btns:
        lines.append(" | ".join(btns))
        lines.append("")


def _process_styled_div(div_html: str, lines: list):
    """Process a styled div (like cross-sell sections) into markdown."""
    lines.append("")
    lines.append("---")
    lines.append("")

    # H3
    h3_m = re.search(r"<h3[^>]*>(.*?)</h3>", div_html, re.DOTALL)
    if h3_m:
        h3_text = clean_whitespace(strip_tags(decode_entities(h3_m.group(1))))
        lines.append(f"### {h3_text}")
        lines.append("")

    # Paragraphs
    for p_m in re.finditer(r"<p[^>]*>(.*?)</p>", div_html, re.DOTALL):
        text = clean_whitespace(strip_tags(decode_entities(p_m.group(1))))
        if text:
            lines.append(text)
            lines.append("")

    # Links
    btns = _extract_md_links(div_html)
    if btns:
        lines.append(" | ".join(btns))
        lines.append("")


def _process_generic_section(section_html: str, lines: list):
    """Generic section processor: extract all headings, paragraphs, lists, links, cards."""

    # Skip the section-header (already extracted by _extract_section_header)
    # Process remaining content

    # Subtype cards (for parent/index pages)
    subtype_cards = list(re.finditer(
        r'<a\s+[^>]*class="[^"]*subtype-card[^"]*"[^>]*>',
        section_html, re.DOTALL
    ))

    # Type cards / equipment cards (related equipment links)
    type_cards = list(re.finditer(
        r'\[([^\]]+)\]\(([^)]+)\)',
        section_html
    ))

    # H3 headings (not in section-header)
    for h3_m in re.finditer(r'<h3[^>]*>(.*?)</h3>', section_html, re.DOTALL):
        h3_text = clean_whitespace(strip_tags(decode_entities(h3_m.group(1))))
        if h3_text:
            lines.append(f"### {h3_text}")
            lines.append("")

    # H4 headings
    for h4_m in re.finditer(r'<h4[^>]*>(.*?)</h4>', section_html, re.DOTALL):
        h4_text = clean_whitespace(strip_tags(decode_entities(h4_m.group(1))))
        if h4_text:
            lines.append(f"#### {h4_text}")
            lines.append("")

    # Paragraphs not in section-header
    section_header_end = 0
    header_m = re.search(r'</div>\s*(?=\s*<div|<table|<ul|<ol|<a\s)', section_html)
    if header_m:
        section_header_end = header_m.end()

    # List items
    for li_m in re.finditer(r"<li[^>]*>(.*?)</li>", section_html, re.DOTALL):
        li_text = clean_whitespace(strip_tags(decode_entities(li_m.group(1))))
        if li_text:
            lines.append(f"- {li_text}")

    # Links in cards (type-card, equipment-card, reactor-type-card, etc.)
    for card_m in re.finditer(
        r'\[([^\]]+)\]\((/equipment/[^)]+)\)',
        section_html
    ):
        text = card_m.group(1)
        url = card_m.group(2)
        if text and not any(text == l.lstrip("- ").split("](")[0].lstrip("[") for l in lines if l.startswith("- [")):
            lines.append(f"- [{text}]({url})")

    # Standalone paragraphs
    for p_m in re.finditer(r'<p[^>]*>(.*?)</p>', section_html, re.DOTALL):
        text = clean_whitespace(strip_tags(decode_entities(p_m.group(1))))
        if text and len(text) > 10:
            # Check it's not already in lines
            if text not in [l.strip() for l in lines]:
                lines.append(text)
                lines.append("")

    # Tables in generic sections
    for table_m in re.finditer(r"<table[^>]*>(.*?)</table>", section_html, re.DOTALL):
        _process_table(table_m.group(1), lines)

    lines.append("")


def _process_table(table_html: str, lines: list):
    """Convert an HTML table to markdown table."""
    rows = []

    thead_m = re.search(r"<thead>(.*?)</thead>", table_html, re.DOTALL)
    if thead_m:
        ths = re.findall(r"<th[^>]*>(.*?)</th>", thead_m.group(1), re.DOTALL)
        headers = [clean_whitespace(strip_tags(decode_entities(th))) for th in ths]
        rows.append("| " + " | ".join(headers) + " |")
        rows.append("|" + "|".join(["-----" for _ in headers]) + "|")

    tbody_m = re.search(r"<tbody>(.*?)</tbody>", table_html, re.DOTALL)
    if tbody_m:
        for tr_m in re.finditer(r"<tr>(.*?)</tr>", tbody_m.group(1), re.DOTALL):
            cells = re.findall(r"<td[^>]*>(.*?)</td>", tr_m.group(1), re.DOTALL)
            cell_texts = [clean_whitespace(strip_tags(decode_entities(c))) for c in cells]
            if any(cell_texts):
                rows.append("| " + " | ".join(cell_texts) + " |")

    if rows:
        lines.extend(rows)
        lines.append("")


def _process_inline_html(html_block: str, lines: list):
    """Process any inline HTML content that appears between structural blocks."""
    # H1
    for m in re.finditer(r"<h1[^>]*>(.*?)</h1>", html_block, re.DOTALL):
        text = clean_whitespace(strip_tags(decode_entities(m.group(1))))
        if text:
            lines.append(f"# {text}")
            lines.append("")

    # H2
    for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html_block, re.DOTALL):
        text = clean_whitespace(strip_tags(decode_entities(m.group(1))))
        if text:
            lines.append(f"## {text}")
            lines.append("")

    # H3
    for m in re.finditer(r"<h3[^>]*>(.*?)</h3>", html_block, re.DOTALL):
        text = clean_whitespace(strip_tags(decode_entities(m.group(1))))
        if text:
            lines.append(f"### {text}")
            lines.append("")

    # Paragraphs
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", html_block, re.DOTALL):
        text = clean_whitespace(strip_tags(decode_entities(m.group(1))))
        if text:
            lines.append(text)
            lines.append("")


def _extract_md_links(html_block: str) -> list:
    """Extract markdown links [TEXT](URL) from already-converted HTML."""
    links = []
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', html_block):
        links.append(f"[{m.group(1)}]({m.group(2)})")
    return links


def _extract_remaining_content(html_block: str, lines: list):
    """Extract any remaining meaningful content from an HTML block."""
    text = clean_whitespace(strip_tags(decode_entities(html_block)))
    if text and len(text) > 10:
        lines.append(text)
        lines.append("")


# ---------------------------------------------------------------------------
# Title and filename utilities
# ---------------------------------------------------------------------------
def extract_title(html_text: str) -> str:
    """Extract the H1 title."""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html_text, re.DOTALL)
    if m:
        return clean_whitespace(strip_tags(decode_entities(m.group(1))))
    m = re.search(r"<title[^>]*>(.*?)</title>", html_text, re.DOTALL)
    if m:
        title = strip_tags(decode_entities(m.group(1)))
        title = re.sub(r"\s*\|.*$", "", title)
        title = re.sub(r"^\[INTERNAL REVIEW\]\s*", "", title)
        return clean_whitespace(title)
    return "Equipment Page"


def get_output_filename(html_path: Path) -> str:
    """Derive output markdown filename from HTML path."""
    rel = html_path.relative_to(EQUIPMENT_DIR)
    parts = list(rel.parts)

    if parts[-1] == "index.html":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1].replace(".html", "")

    if len(parts) == 0:
        return "equipment-index.md"
    elif len(parts) == 1:
        return f"{parts[0]}-index.md"
    else:
        return "-".join(parts) + ".md"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    html_files = sorted(EQUIPMENT_DIR.rglob("*.html"))

    # Skip the top-level equipment/index.html
    html_files = [f for f in html_files if not (f.parent == EQUIPMENT_DIR and f.name == "index.html")]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    generated = []
    for html_path in html_files:
        out_name = get_output_filename(html_path)
        out_path = OUTPUT_DIR / out_name

        print(f"  Converting: {html_path.relative_to(BASE_DIR)} -> {out_name}")

        html_text = html_path.read_text(encoding="utf-8")
        md_content = html_to_markdown(html_text)

        out_path.write_text(md_content, encoding="utf-8")
        generated.append((out_name, extract_title(html_text)))

    # Create _INDEX.md
    index_lines = [
        "# IPP Equipment Landing Pages - Client Review\n",
        f"**Total pages:** {len(generated)}\n",
        "## Pages\n",
        "| # | File | Page Title |",
        "|---|------|------------|",
    ]
    for i, (fname, title) in enumerate(generated, 1):
        index_lines.append(f"| {i} | [{fname}]({fname}) | {title} |")

    (OUTPUT_DIR / "_INDEX.md").write_text("\n".join(index_lines), encoding="utf-8")

    print(f"\n  Done! Generated {len(generated)} markdown files + _INDEX.md")
    print(f"  Output directory: {OUTPUT_DIR}")
    return len(generated)


if __name__ == "__main__":
    main()
