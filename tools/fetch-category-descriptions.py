#!/usr/bin/env python3
"""
Fetch IMS category description pages for all 39 equipment types.
Extracts description text, materials, industries, applications from each page.
Saves as category-description.md in each data folder.
"""

import requests
from html.parser import HTMLParser
import os
import re
import time

BASE = "https://ims.internationalprocessplants.com/inventory/equipment"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Mapping: (data folder, IMS category page URL path, display name)
CATEGORIES = [
    ("reactors/batch-type-agitated",        "reactor/batch-type-agitated",              "Batch-Type Agitated Reactors"),
    ("reactors/batch-type-body-only",        "reactor/batch-type-body-only",             "Batch Type Body Only Reactors"),
    ("tank",                                 "tank",                                      "Tanks"),
    ("dryer/porcupine-dryer",               "porcupine-dryer",                           "Porcupine Dryers"),
    ("dryer/rotary-steam-tube-dryer",       "rotary-steam-tube-dryer",                   "Rotary Steam Tube Dryers"),
    ("dryer/rotary-vacuum-dryer",           "rotary-vacuum-dryer",                       "Rotary Vacuum Dryers"),
    ("dryer/spray-dryer",                   "spray-dryer",                               "Spray Dryers"),
    ("dryer/holoflite-and-screw-dryer",     "holoflite-and-screw-dryer",                "Holoflite & Screw Dryers"),
    ("dryer/fluid-bed-dryer",              "fluid-bed-dryer",                            "Fluid Bed Dryers"),
    ("dryer/ribbon-and-paddle-dryer",       "ribbon-and-paddle-dryer",                   "Ribbon & Paddle Dryers"),
    ("dryer/twin-shell-and-double-cone-dryer", "twin-shell-and-double-cone-dryer",       "Twin Shell & Double Cone Dryers"),
    ("dryer/wyssmont-dryer",               "wyssmont-dryer",                             "Wyssmont Dryers"),
    ("dryer/freeze-dryer",                 "freeze-dryer",                               "Freeze Dryers"),
    ("dryer/horizontal-belt-continuous-dryer","horizontal-belt-and-continuous-dryer",     "Horizontal Belt & Continuous Dryers"),
    ("centrifuge/auto-discharge-bottom",    "basket-centrifuge/auto-discharge-bottom",   "Auto Discharge-Bottom Basket Centrifuges"),
    ("centrifuge/manual-discharge-top",     "basket-centrifuge/manual-discharge-top",    "Manual Discharge-Top Basket Centrifuges"),
    ("centrifuge/basket-centrifuge-parts",  "basket-centrifuge/parts-only",              "Basket Centrifuge Parts"),
    ("centrifuge/disc-bowl-centrifuge",     "disc-bowl-centrifuge",                      "Disc Bowl Centrifuges"),
    ("centrifuge/inverting-filter-centrifuge","inverting-filter-centrifuge",              "Inverting Filter Centrifuges"),
    ("centrifuge/solid-bowl-decanter-centrifuge","solid-bowl-decanter-centrifuge",       "Solid Bowl-Decanter Centrifuges"),
    ("filter/rosenmund-and-cogiem",         "filter/rosenmund-and-cogiem",               "Rosenmund and Cogiem Filters"),
    ("filter/pressure-leaf",               "filter/pressure-leaf",                       "Pressure Leaf Filters"),
    ("filter/nutsche",                     "filter/nutsche",                              "Nutsche Filters"),
    ("heat-exchanger/shell-and-tube",      "heat-exchanger/shell-and-tube",              "Shell and Tube Heat Exchangers"),
    ("mixer/muller-mixer",                 "muller-mixer",                                "Muller Mixers"),
    ("mixer/nauta-mixer",                  "nauta-mixer",                                 "Nauta Mixers"),
    ("mixer/intensive-mixer",              "intensive-mixer",                              "Intensive Mixers"),
    ("mixer/twin-shell-and-double-cone-mixer","twin-shell-and-double-cone-mixer",        "Twin Shell & Double Cone Mixers"),
    ("mixer/ribbon-paddle-mixer",          "ribbon-and-paddle-mixer",                     "Ribbon & Paddle Mixers"),
    ("mixer/double-arm-mixer",             "double-arm-mixer",                            "Double Arm Mixers"),
    ("mixer/continuous-mixer",             "continuous-mixer",                             "Continuous Mixers"),
    ("glass-lined-parts/agitator",         "glass-lined-parts/agitator",                 "Glass Lined Agitators"),
    ("glass-lined-parts/baffle",           "glass-lined-parts/baffle",                   "Glass Lined Baffles"),
    ("glass-lined-parts/cryo-lock-blades", "glass-lined-parts/cryo-lock-blades",         "Glass Lined Cryo-Lock Blades"),
    ("glass-lined-parts/pro-ring",         "glass-lined-parts/pro-ring",                 "Glass Lined Pro-Ring"),
    ("evaporator/crystalizer-evaporator",  "evaporator/crystalizer-evaporator",          "Crystalizer/Evaporator"),
    ("evaporator/flash",                   "evaporator/flash",                            "Flash Evaporators"),
    ("evaporator/rising-falling-film",     "evaporator/rising-falling-film",             "Rising/Falling Film Evaporators"),
    ("evaporator/wiped-thin-film",         "evaporator/wiped-thin-film",                 "Wiped/Thin Film Evaporators"),
]


class TextExtractor(HTMLParser):
    """Extract visible text from HTML, skipping scripts/styles."""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
        self.skip_tags = {'script', 'style', 'noscript'}

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip = True

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip = False

    def handle_data(self, data):
        if not self.skip:
            stripped = data.strip()
            if stripped:
                self.text.append(stripped)

    def get_text(self):
        return '\n'.join(self.text)


def extract_description_sections(html):
    """Extract description content from IMS category page HTML."""
    # Look for description sections in the HTML
    sections = {}

    # Extract text content
    parser = TextExtractor()
    parser.feed(html)
    full_text = parser.get_text()

    # Look for common section patterns
    # Materials of Construction
    mat_match = re.search(r'Materials?\s+(?:of\s+)?Construction(.*?)(?=Industries|Applications|Key\s+Features|Materials\s+Processed|$)',
                          full_text, re.DOTALL | re.IGNORECASE)
    if mat_match:
        sections['materials'] = mat_match.group(1).strip()[:2000]

    # Industries
    ind_match = re.search(r'Industries?\s+(?:&\s+)?(?:Applications?)?(.*?)(?=Materials?\s+(?:of|Processed)|Key\s+Features|Applications|$)',
                          full_text, re.DOTALL | re.IGNORECASE)
    if ind_match:
        sections['industries'] = ind_match.group(1).strip()[:2000]

    return full_text, sections


def fetch_and_save(folder, url_path, name):
    """Fetch an IMS category page and save description content."""
    url = f"{BASE}/{url_path}"
    output_dir = os.path.join(DATA_DIR, folder)
    output_file = os.path.join(output_dir, "category-description.md")

    try:
        resp = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

        if resp.status_code != 200:
            print(f"  [{resp.status_code}] {name} — {url}")
            # Try alternate URL patterns
            return False

        html = resp.text

        # Check for error pages
        if "not found" in html.lower() and len(html) < 5000:
            print(f"  [NOT FOUND] {name} — {url}")
            return False

        full_text, sections = extract_description_sections(html)

        # Save the raw HTML for later processing
        html_file = os.path.join(output_dir, "category-page.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)

        # Save extracted text as markdown
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {name} — IMS Category Page\n\n")
            f.write(f"**Source URL:** {url}\n\n")
            f.write(f"---\n\n")
            f.write(f"## Full Page Text\n\n")
            f.write(full_text[:10000])
            f.write("\n")

        print(f"  [OK] {name} — {url}")
        return True

    except Exception as e:
        print(f"  [ERROR] {name} — {e}")
        return False


if __name__ == "__main__":
    print("Fetching IMS category description pages...")
    print("=" * 60)

    success = 0
    failed = 0
    failed_list = []

    for folder, url_path, name in CATEGORIES:
        result = fetch_and_save(folder, url_path, name)
        if result:
            success += 1
        else:
            failed += 1
            failed_list.append((folder, url_path, name))
        time.sleep(0.5)  # Be polite

    print(f"\n{'=' * 60}")
    print(f"DONE: {success} succeeded, {failed} failed")

    if failed_list:
        print(f"\nFailed pages:")
        for folder, url_path, name in failed_list:
            print(f"  {name} — {BASE}/{url_path}")
