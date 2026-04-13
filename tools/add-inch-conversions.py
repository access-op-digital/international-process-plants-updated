#!/usr/bin/env python3
"""
Add inch conversions to mm dimension values across IPP equipment landing pages.

Finds patterns like "2,750 mm" that are NOT already followed by "(N in)" and
inserts the inch equivalent. Excludes CSS contexts, data-src-label attributes,
meta descriptions, and JSON-LD structured data.

Usage: python3 tools/add-inch-conversions.py
"""

import re
import os
import glob

EQUIPMENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "equipment")

# Pattern to match mm values: handles "2,750 mm", "600 mm", "355.6 mm"
# Captures the numeric part (with optional commas and decimals)
MM_PATTERN = re.compile(
    r'(\d[\d,]*\.?\d*)\s+mm'           # e.g. "2,750 mm" or "355.6 mm"
    r'(?!\s*\(\d[\d.]*\s*in\))'         # negative lookahead: NOT already followed by "(N in)"
)

# Contexts to SKIP (CSS properties, data attributes, meta, JSON-LD)
CSS_PROPS = re.compile(
    r'(?:margin|padding|font-size|border-radius|gap|width|height|max-width|'
    r'min-width|min-height|max-height|top|left|right|bottom)\s*:\s*[^;]*$',
    re.IGNORECASE
)

def parse_mm_value(s):
    """Parse a mm string like '2,750' or '355.6' into a float."""
    return float(s.replace(',', ''))

def mm_to_inches(mm_val):
    """Convert mm to inches, rounded to 1 decimal. Drop .0 if whole number."""
    inches = mm_val / 25.4
    rounded = round(inches, 1)
    if rounded == int(rounded):
        return str(int(rounded))
    return f"{rounded:.1f}"

def is_inside_style_attr(text, pos):
    """Check if position is inside a style='...' attribute."""
    # Look backwards for style=" or style='
    before = text[max(0, pos - 500):pos]
    # Find last style= opening
    style_start = max(before.rfind('style="'), before.rfind("style='"))
    if style_start == -1:
        return False
    # Determine which quote
    actual_pos = max(0, pos - 500) + style_start
    quote_char = text[actual_pos + 6]  # character after style=
    # Find the closing quote after style_start
    close = text.find(quote_char, actual_pos + 7)
    return close == -1 or close > pos

def is_inside_data_src_label(text, pos):
    """Check if position is inside a data-src-label='...' attribute."""
    before = text[max(0, pos - 500):pos]
    attr_start = max(before.rfind('data-src-label="'), before.rfind("data-src-label='"))
    if attr_start == -1:
        return False
    actual_pos = max(0, pos - 500) + attr_start
    quote_char = text[actual_pos + 15]  # character after data-src-label=
    close = text.find(quote_char, actual_pos + 16)
    return close == -1 or close > pos

def is_inside_style_block(text, pos):
    """Check if position is inside a <style>...</style> block."""
    before = text[:pos]
    last_style_open = before.rfind('<style')
    if last_style_open == -1:
        return False
    last_style_close = before.rfind('</style>')
    return last_style_close < last_style_open

def is_inside_meta_or_jsonld(text, pos):
    """Check if position is inside a meta tag or JSON-LD script block."""
    before = text[max(0, pos - 1000):pos]
    # Meta description
    meta_start = before.rfind('<meta')
    if meta_start != -1:
        actual_pos = max(0, pos - 1000) + meta_start
        meta_close = text.find('>', actual_pos)
        if meta_close == -1 or meta_close > pos:
            return True
    # JSON-LD
    jsonld_start = before.rfind('application/ld+json')
    if jsonld_start != -1:
        actual_pos = max(0, pos - 1000) + jsonld_start
        script_close = text.find('</script>', actual_pos)
        if script_close == -1 or script_close > pos:
            return True
    return False

def is_css_line_context(text, pos):
    """Check if the mm value is part of a CSS property value on the same line."""
    # Get the line containing the position
    line_start = text.rfind('\n', 0, pos) + 1
    line_end = text.find('\n', pos)
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:pos]
    return bool(CSS_PROPS.search(line))

def process_file(filepath):
    """Process a single HTML file, adding inch conversions. Returns count of changes."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    count = 0

    def replacer(match):
        nonlocal count
        pos = match.start()

        # Skip if in excluded contexts
        if is_inside_style_attr(content, pos):
            return match.group(0)
        if is_inside_data_src_label(content, pos):
            return match.group(0)
        if is_inside_style_block(content, pos):
            return match.group(0)
        if is_inside_meta_or_jsonld(content, pos):
            return match.group(0)
        if is_css_line_context(content, pos):
            return match.group(0)

        mm_str = match.group(1)
        mm_val = parse_mm_value(mm_str)
        inches = mm_to_inches(mm_val)

        count += 1
        return f"{mm_str} mm ({inches} in)"

    new_content = MM_PATTERN.sub(replacer, content)

    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return count


def main():
    html_files = glob.glob(os.path.join(EQUIPMENT_DIR, '**', '*.html'), recursive=True)
    html_files.sort()

    total_conversions = 0
    files_modified = 0

    print(f"Scanning {len(html_files)} HTML files in {EQUIPMENT_DIR}\n")

    for filepath in html_files:
        rel = os.path.relpath(filepath, os.path.dirname(EQUIPMENT_DIR))
        count = process_file(filepath)
        if count > 0:
            print(f"  {rel}: {count} conversions added")
            total_conversions += count
            files_modified += 1

    print(f"\nDone. {total_conversions} conversions added across {files_modified} files.")


if __name__ == '__main__':
    main()
