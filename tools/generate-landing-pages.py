#!/usr/bin/env python3
"""
Generate INTERNAL-REVIEW HTML landing pages for 38 IPP equipment categories.

Each page follows the approved batch-type-agitated-reactors template structure,
with all content sourced from real scraped data (all_products.json, category-page.html).

Usage:
    python3 generate-landing-pages.py
    python3 generate-landing-pages.py --category tank
    python3 generate-landing-pages.py --dry-run
"""

import json
import os
import re
import sys
import math
import argparse
from html import escape as html_escape
from html.parser import HTMLParser
from collections import Counter

# ============================================================
# PATHS
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
# Pages live under equipment/, at the same path as each category's url_path
LANDING_DIR = os.path.join(PROJECT_ROOT, "equipment")

# ============================================================
# CATEGORY DEFINITIONS
# (data_folder, landing_page_folder, display_name, url_path, ims_category_url, primary_query)
# ============================================================
CATEGORIES = [
    ("reactors/batch-type-body-only", "reactors/batch-type-body-only", "Batch Type Body Only Reactors", "/equipment/reactor/batch-type-body-only/", "https://ims.internationalprocessplants.com/inventory/equipment/reactor/batch-type-body-only", "used reactor vessel for sale"),
    ("tank", "tank", "Tanks", "/equipment/tank/", "https://ims.internationalprocessplants.com/inventory/equipment/tank", "used tanks for sale"),
    ("dryer/porcupine-dryer", "dryer/porcupine-dryer", "Porcupine Dryers", "/equipment/dryer/porcupine-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/porcupine-dryer", "used porcupine dryer for sale"),
    ("dryer/rotary-steam-tube-dryer", "dryer/rotary-steam-tube-dryer", "Rotary Steam Tube Dryers", "/equipment/dryer/rotary-steam-tube-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/rotary-steam-tube-dryer", "used rotary steam tube dryer for sale"),
    ("dryer/rotary-vacuum-dryer", "dryer/rotary-vacuum-dryer", "Rotary Vacuum Dryers", "/equipment/dryer/rotary-vacuum-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/rotary-vacuum-dryer", "used rotary vacuum dryer for sale"),
    ("dryer/spray-dryer", "dryer/spray-dryer", "Spray Dryers", "/equipment/dryer/spray-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/spray-dryer", "used spray dryer for sale"),
    ("dryer/holoflite-and-screw-dryer", "dryer/holoflite-and-screw-dryer", "Holoflite & Screw Dryers", "/equipment/dryer/holoflite-and-screw-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/holoflite-and-screw-dryer", "used holoflite dryer for sale"),
    ("dryer/fluid-bed-dryer", "dryer/fluid-bed-dryer", "Fluid Bed Dryers", "/equipment/dryer/fluid-bed-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/fluid-bed-dryer", "used fluid bed dryer for sale"),
    ("dryer/ribbon-and-paddle-dryer", "dryer/ribbon-and-paddle-dryer", "Ribbon & Paddle Dryers", "/equipment/dryer/ribbon-and-paddle-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/ribbon-and-paddle-dryer", "used ribbon and paddle dryer for sale"),
    ("dryer/twin-shell-and-double-cone-dryer", "dryer/twin-shell-and-double-cone-dryer", "Twin Shell & Double Cone Dryers", "/equipment/dryer/twin-shell-and-double-cone-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/twin-shell-and-double-cone-dryer", "used twin shell and double cone dryer for sale"),
    ("dryer/wyssmont-dryer", "dryer/wyssmont-dryer", "Wyssmont Dryers", "/equipment/dryer/wyssmont-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/wyssmont-dryer", "used Wyssmont dryer for sale"),
    ("dryer/freeze-dryer", "dryer/freeze-dryer", "Freeze Dryers", "/equipment/dryer/freeze-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/freeze-dryer", "used freeze dryer for sale"),
    ("dryer/horizontal-belt-continuous-dryer", "dryer/horizontal-belt-continuous-dryer", "Horizontal Belt & Continuous Dryers", "/equipment/dryer/horizontal-belt-continuous-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/horizontal-belt-continuous-dryer", "used horizontal belt continuous dryer for sale"),
    ("centrifuge/auto-discharge-bottom", "centrifuge/auto-discharge-bottom", "Auto Discharge-Bottom Basket Centrifuges", "/equipment/centrifuge/auto-discharge-bottom/", "https://ims.internationalprocessplants.com/inventory/equipment/basket-centrifuge/auto-discharge-bottom", "used auto discharge bottom centrifuge for sale"),
    ("centrifuge/manual-discharge-top", "centrifuge/manual-discharge-top", "Manual Discharge-Top Basket Centrifuges", "/equipment/centrifuge/manual-discharge-top/", "https://ims.internationalprocessplants.com/inventory/equipment/basket-centrifuge/manual-discharge-top", "used manual discharge top centrifuge for sale"),
    ("centrifuge/basket-centrifuge-parts", "centrifuge/basket-centrifuge-parts", "Basket Centrifuge Parts", "/equipment/centrifuge/basket-centrifuge-parts/", "https://ims.internationalprocessplants.com/inventory/equipment/basket-centrifuge/parts-only", "basket centrifuge parts for sale"),
    ("centrifuge/disc-bowl-centrifuge", "centrifuge/disc-bowl-centrifuge", "Disc Bowl Centrifuges", "/equipment/centrifuge/disc-bowl-centrifuge/", "https://ims.internationalprocessplants.com/inventory/equipment/disc-bowl-centrifuge", "used disc bowl centrifuge for sale"),
    ("centrifuge/inverting-filter-centrifuge", "centrifuge/inverting-filter-centrifuge", "Inverting Filter Centrifuges", "/equipment/centrifuge/inverting-filter-centrifuge/", "https://ims.internationalprocessplants.com/inventory/equipment/inverting-filter-centrifuge", "used inverting filter centrifuge for sale"),
    ("centrifuge/solid-bowl-decanter-centrifuge", "centrifuge/solid-bowl-decanter-centrifuge", "Solid Bowl-Decanter Centrifuges", "/equipment/centrifuge/solid-bowl-decanter-centrifuge/", "https://ims.internationalprocessplants.com/inventory/equipment/solid-bowl-decanter-centrifuge", "used solid bowl decanter centrifuge for sale"),
    ("filter/rosenmund-and-cogiem", "filter/rosenmund-and-cogiem", "Rosenmund and Cogiem Filters", "/equipment/filter/rosenmund-and-cogiem/", "https://ims.internationalprocessplants.com/inventory/equipment/filter/rosenmund-and-cogiem", "used Rosenmund filter for sale"),
    ("filter/pressure-leaf", "filter/pressure-leaf", "Pressure Leaf Filters", "/equipment/filter/pressure-leaf/", "https://ims.internationalprocessplants.com/inventory/equipment/filter/pressure-leaf", "used pressure leaf filter for sale"),
    ("filter/nutsche", "filter/nutsche", "Nutsche Filters", "/equipment/filter/nutsche/", "https://ims.internationalprocessplants.com/inventory/equipment/filter/nutsche", "used nutsche filter for sale"),
    ("heat-exchanger/shell-and-tube", "heat-exchanger/shell-and-tube", "Shell and Tube Heat Exchangers", "/equipment/heat-exchanger/shell-and-tube/", "https://ims.internationalprocessplants.com/inventory/equipment/heat-exchanger/shell-and-tube", "used shell and tube heat exchanger for sale"),
    ("mixer/muller-mixer", "mixer/muller-mixer", "Muller Mixers", "/equipment/mixer/muller-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/muller-mixer", "used muller mixer for sale"),
    ("mixer/nauta-mixer", "mixer/nauta-mixer", "Nauta Mixers", "/equipment/mixer/nauta-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/nauta-mixer", "used Nauta mixer for sale"),
    ("mixer/intensive-mixer", "mixer/intensive-mixer", "Intensive Mixers", "/equipment/mixer/intensive-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/intensive-mixer", "used intensive mixer for sale"),
    ("mixer/twin-shell-and-double-cone-mixer", "mixer/twin-shell-and-double-cone-mixer", "Twin Shell & Double Cone Mixers", "/equipment/mixer/twin-shell-and-double-cone-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/twin-shell-and-double-cone-mixer", "used twin shell and double cone mixer for sale"),
    ("mixer/ribbon-paddle-mixer", "mixer/ribbon-paddle-mixer", "Ribbon & Paddle Mixers", "/equipment/mixer/ribbon-paddle-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/ribbon-paddle-mixer", "used ribbon paddle mixer for sale"),
    ("mixer/double-arm-mixer", "mixer/double-arm-mixer", "Double Arm Mixers", "/equipment/mixer/double-arm-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/double-arm-mixer", "used double arm mixer for sale"),
    ("mixer/continuous-mixer", "mixer/continuous-mixer", "Continuous Mixers", "/equipment/mixer/continuous-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/continuous-mixer", "used continuous mixer for sale"),
    ("glass-lined-parts/agitator", "glass-lined-parts/agitator", "Glass Lined Agitators", "/equipment/glass-lined-parts/agitator/", "https://ims.internationalprocessplants.com/inventory/equipment/glass-lined-parts/agitator", "used glass lined agitator for sale"),
    ("glass-lined-parts/baffle", "glass-lined-parts/baffle", "Glass Lined Baffles", "/equipment/glass-lined-parts/baffle/", "https://ims.internationalprocessplants.com/inventory/equipment/glass-lined-parts/baffle", "used glass lined baffle for sale"),
    ("glass-lined-parts/cryo-lock-blades", "glass-lined-parts/cryo-lock-blades", "Glass Lined Cryo-Lock Blades", "/equipment/glass-lined-parts/cryo-lock-blades/", "https://ims.internationalprocessplants.com/inventory/equipment/glass-lined-parts/cryo-lock-blades", "used glass lined cryo lock blades for sale"),
    ("glass-lined-parts/pro-ring", "glass-lined-parts/pro-ring", "Glass Lined Pro-Ring", "/equipment/glass-lined-parts/pro-ring/", "https://ims.internationalprocessplants.com/inventory/equipment/glass-lined-parts/pro-ring", "used glass lined Pro-Ring for sale"),
    ("evaporator/crystalizer-evaporator", "evaporator/crystalizer-evaporator", "Crystalizer/Evaporator", "/equipment/evaporator/crystalizer-evaporator/", "https://ims.internationalprocessplants.com/inventory/equipment/evaporator/crystalizer-evaporator", "used crystallizer evaporator for sale"),
    ("evaporator/flash", "evaporator/flash", "Flash Evaporators", "/equipment/evaporator/flash/", "https://ims.internationalprocessplants.com/inventory/equipment/evaporator/flash", "used flash evaporator for sale"),
    ("evaporator/rising-falling-film", "evaporator/rising-falling-film", "Rising/Falling Film Evaporators", "/equipment/evaporator/rising-falling-film/", "https://ims.internationalprocessplants.com/inventory/equipment/evaporator/rising-falling-film", "used rising falling film evaporator for sale"),
    ("evaporator/wiped-thin-film", "evaporator/wiped-thin-film", "Wiped/Thin Film Evaporators", "/equipment/evaporator/wiped-thin-film/", "https://ims.internationalprocessplants.com/inventory/equipment/evaporator/wiped-thin-film", "used wiped thin film evaporator for sale"),
]

# ============================================================
# EQUIPMENT TYPE -> FontAwesome ICON MAPPING
# ============================================================
EQUIPMENT_ICONS = {
    "reactor": "fa-flask",
    "tank": "fa-database",
    "dryer": "fa-fire-flame-simple",
    "centrifuge": "fa-circle-notch",
    "filter": "fa-filter",
    "heat-exchanger": "fa-temperature-half",
    "mixer": "fa-blender",
    "glass-lined-parts": "fa-shield-halved",
    "evaporator": "fa-cloud",
}

# Default industries for equipment types
INDUSTRY_ICONS = [
    ("fa-pills", "Pharmaceutical"),
    ("fa-flask", "Chemical Processing"),
    ("fa-dna", "Biotechnology"),
    ("fa-wheat-awn", "Food &amp; Beverage"),
    ("fa-pump-soap", "Cosmetics"),
    ("fa-vial", "Fine Chemicals"),
    ("fa-seedling", "Agrochemicals"),
    ("fa-link", "Polymers &amp; Resins"),
    ("fa-droplet", "Paints &amp; Coatings"),
    ("fa-oil-well", "Petrochemicals"),
]


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def parse_numeric(value_str):
    """Extract numeric value from a string like '3,000 L (790 gallons)' or '1.01 bar (14.7 psi)'."""
    if not value_str:
        return None
    # Remove commas, find first number
    cleaned = value_str.replace(",", "")
    match = re.search(r"([\d.]+)", cleaned)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None


def round_count(n):
    """Round product count for display: 5 -> '5', 47 -> '45+', 172 -> '170+', 1336 -> '1,300+'."""
    if n <= 10:
        return str(n)
    if n <= 100:
        rounded = (n // 5) * 5
        return f"{rounded}+"
    if n <= 1000:
        rounded = (n // 10) * 10
        return f"{rounded:,}+"
    rounded = (n // 100) * 100
    return f"{rounded:,}+"


def slug_from_name(name):
    """Convert display name to URL slug."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def h(text):
    """HTML-escape text."""
    return html_escape(str(text))


def src(src_type, label, text, link_url=None):
    """Generate a source-cited span."""
    link = ""
    if link_url:
        link = f'<a href="{h(link_url)}" target="_blank" class="src-link"></a>'
    return f'<span class="src src-{src_type}" data-src-label="{h(label)}">{text}</span>{link}'


class CategoryPageParser(HTMLParser):
    """Extract meaningful text from category-page.html."""

    def __init__(self):
        super().__init__()
        self.texts = []
        self.current_tag = None
        self.capture = False
        self.h1_text = ""
        self.h2_texts = []
        self.h3_texts = []
        self.p_texts = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "h2", "h3", "p"):
            self.current_tag = tag
            self.capture = True
            self._buf = []

    def handle_endtag(self, tag):
        if tag == self.current_tag and self.capture:
            text = " ".join(self._buf).strip()
            if text and len(text) > 20:
                if tag == "h1":
                    self.h1_text = text
                elif tag == "h2":
                    self.h2_texts.append(text)
                elif tag == "h3":
                    self.h3_texts.append(text)
                elif tag == "p":
                    self.p_texts.append(text)
            self.capture = False
            self.current_tag = None

    def handle_data(self, data):
        if self.capture:
            self._buf.append(data.strip())


def parse_category_page(html_path):
    """Parse category-page.html and return structured text."""
    parser = CategoryPageParser()
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            parser.feed(f.read())
    except Exception:
        pass
    return {
        "h1": parser.h1_text,
        "h2": parser.h2_texts,
        "h3": parser.h3_texts,
        "paragraphs": parser.p_texts,
    }


def get_category_description_url(md_path):
    """Extract source URL from category-description.md."""
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r"\*\*Source URL:\*\*\s*(https?://\S+)", content)
        if match:
            return match.group(1)
    except Exception:
        pass
    return ""


def analyze_products(products):
    """Analyze all products and extract key statistics."""
    stats = {
        "count": len(products),
        "materials": Counter(),
        "manufacturers": Counter(),
        "conditions": Counter(),
        "capacity_values": [],
        "pressure_values": [],
        "temperature_values": [],
        "all_attrs": set(),
    }

    for p in products:
        attrs = p.get("attributes", {})
        stats["all_attrs"].update(attrs.keys())

        # Material
        mat = attrs.get("Material", "")
        if mat:
            stats["materials"][mat] += 1

        # Manufacturer
        mfr = attrs.get("Manufacturer", "")
        if mfr:
            stats["manufacturers"][mfr] += 1

        # Condition
        cond = attrs.get("Condition", "")
        if cond:
            stats["conditions"][cond] += 1

        # Capacity - try multiple field names
        for cap_key in ["Capacity (Design)", "Capacity", "Cake Volume", "Total Heat Transfer Surface Area",
                        "Heat Transfer Surface Area", "Evaporation Rate", "Filtration Area"]:
            cap = attrs.get(cap_key, "")
            if cap:
                val = parse_numeric(cap)
                if val and val > 0:
                    stats["capacity_values"].append((val, cap, p))
                break

        # Pressure - try multiple field names
        for pres_key in ["Internal Pressure", "Pressure", "Shell Pressure", "Tube Pressure"]:
            pres = attrs.get(pres_key, "")
            if pres:
                val = parse_numeric(pres)
                if val is not None:
                    stats["pressure_values"].append((val, pres, p))
                break

        # Temperature - try multiple field names
        for temp_key in ["Internal Temperature", "Temperature", "Shell Temperature", "Tube Temperature"]:
            temp = attrs.get(temp_key, "")
            if temp:
                val = parse_numeric(temp)
                if val is not None:
                    stats["temperature_values"].append((val, temp, p))
                break

    return stats


def pick_representative_products(products, n=3):
    """Pick n representative products with most attributes filled."""
    sorted_prods = sorted(products, key=lambda p: p.get("attribute_count", 0), reverse=True)
    # Try to pick diverse manufacturers
    seen_mfrs = set()
    selected = []
    for p in sorted_prods:
        mfr = p.get("attributes", {}).get("Manufacturer", "unknown")
        if mfr not in seen_mfrs or len(selected) >= len(sorted_prods) // 2:
            selected.append(p)
            seen_mfrs.add(mfr)
        if len(selected) >= n:
            break
    # Fill remainder if needed
    for p in sorted_prods:
        if len(selected) >= n:
            break
        if p not in selected:
            selected.append(p)
    return selected[:n]


def group_products_by_material(products):
    """Group products by material type for tabs."""
    groups = {}
    for p in products:
        mat = p.get("attributes", {}).get("Material", "Other")
        if not mat:
            mat = "Other"
        # Simplify material names for grouping
        mat_group = simplify_material(mat)
        if mat_group not in groups:
            groups[mat_group] = []
        groups[mat_group].append(p)

    # Sort groups by count, descending
    sorted_groups = sorted(groups.items(), key=lambda x: len(x[1]), reverse=True)
    return sorted_groups


def simplify_material(mat):
    """Simplify material name for tab grouping."""
    mat_lower = mat.lower()
    if "glass" in mat_lower:
        return "Glass-Lined"
    if "hastelloy" in mat_lower:
        return "Hastelloy"
    if "titanium" in mat_lower:
        return "Titanium"
    if "316l" in mat_lower:
        return "Stainless Steel 316L"
    if "316" in mat_lower:
        return "Stainless Steel 316"
    if "304" in mat_lower:
        return "Stainless Steel 304"
    if "321" in mat_lower:
        return "Stainless Steel 321"
    if "stainless" in mat_lower or "ss " in mat_lower:
        return "Stainless Steel"
    if "carbon" in mat_lower:
        return "Carbon Steel"
    if "nickel" in mat_lower:
        return "Nickel Alloy"
    if "alloy" in mat_lower:
        return "Specialty Alloy"
    return mat


def get_primary_capacity_key(attrs_set):
    """Determine the primary capacity/size attribute key for this equipment type."""
    priority = [
        "Capacity (Design)", "Capacity", "Total Heat Transfer Surface Area",
        "Heat Transfer Surface Area", "Filtration Area", "Evaporation Rate",
        "Cake Volume", "Basket Diameter", "Diameter", "Shell Diameter",
        "Vessel Size", "Overall Length",
    ]
    for key in priority:
        if key in attrs_set:
            return key
    return None


def get_display_specs(product, max_specs=5):
    """Get the most important specs from a product for display on cards."""
    attrs = product.get("attributes", {})
    specs = []

    # Priority order of attributes to show
    priority_keys = [
        "Capacity (Design)", "Capacity", "Total Heat Transfer Surface Area",
        "Heat Transfer Surface Area", "Filtration Area", "Evaporation Rate",
        "Cake Volume", "Basket Diameter", "Vessel Size",
        "Material", "Internal Pressure", "Pressure", "Shell Pressure",
        "Internal Temperature", "Temperature", "Shell Temperature",
        "Internal Full Vacuum", "Vacuum",
        "Motor Power", "Drive Motor HP", "Speed-RPM Maximum",
        "Diameter", "Shell Diameter", "Straight Side Length", "Length",
        "Overall Length", "Overall Height", "Height",
        "Condition", "Manufacturer", "Model",
        "Orientation", "Support Type", "Jacket Type",
        "Agitation Seal Type", "Tube Number", "TEMA Type",
        "Atomizer Type", "Mixer Type", "Glass Agitator Type",
        "Glass Baffle Type", "Reglassed",
    ]

    stock = product.get("stock_number", "")
    shown = set()
    for key in priority_keys:
        if key in attrs and attrs[key] and key not in shown:
            val = attrs[key]
            shown.add(key)
            specs.append((key, val, stock))
            if len(specs) >= max_specs:
                break

    return specs


def build_breadcrumbs(url_path, display_name):
    """Build breadcrumb list from URL path."""
    parts = [p for p in url_path.strip("/").split("/") if p]
    crumbs = [
        {"name": "Home", "url": "https://internationalprocessplants.com/"},
        {"name": "Equipment", "url": "https://internationalprocessplants.com/equipment/"},
    ]
    # Add intermediate breadcrumbs
    path_so_far = "/equipment/"
    for i, part in enumerate(parts[1:], start=1):  # skip 'equipment'
        if i < len(parts):
            label = part.replace("-", " ").title()
            path_so_far += part + "/"
            if i < len(parts) - 1:
                crumbs.append({
                    "name": label,
                    "url": f"https://internationalprocessplants.com{path_so_far}",
                })
    # Final breadcrumb (current page, no URL)
    crumbs.append({"name": f"Used {display_name} for Sale"})
    return crumbs


def get_equipment_icon(data_folder):
    """Get FontAwesome icon class for equipment type."""
    top_level = data_folder.split("/")[0]
    return EQUIPMENT_ICONS.get(top_level, "fa-cog")


def format_material_list(materials_counter, max_display=6):
    """Format materials for display."""
    top = materials_counter.most_common(max_display)
    return [mat for mat, _ in top]


def format_manufacturer_list(mfr_counter, max_display=6):
    """Format manufacturers for display."""
    top = mfr_counter.most_common(max_display)
    return [mfr for mfr, _ in top]


# ============================================================
# HTML GENERATION
# ============================================================

def generate_schema_json(cat, stats, breadcrumbs):
    """Generate Schema.org JSON-LD."""
    data_folder, lp_folder, display_name, url_path, ims_url, query = cat
    full_url = f"https://internationalprocessplants.com{url_path}"

    materials = format_material_list(stats["materials"])
    manufacturers = format_manufacturer_list(stats["manufacturers"])

    # Capacity range text
    cap_text = ""
    if stats["capacity_values"]:
        cap_vals = sorted(stats["capacity_values"], key=lambda x: x[0])
        cap_text = f" Capacities from {cap_vals[0][1].split('(')[0].strip()} to {cap_vals[-1][1].split('(')[0].strip()}."

    mfr_text = ", ".join(manufacturers[:4]) if manufacturers else "multiple manufacturers"

    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": f"{full_url}#webpage",
        "url": full_url,
        "name": f"Buy Used {display_name} for Sale | IPP",
        "description": f"Buy used {display_name.lower()} from International Process Plants. {mfr_text} and more manufacturers. {', '.join(materials[:4])} construction.{cap_text}",
        "inLanguage": "en-US",
        "about": {
            "@type": "Organization",
            "@id": "https://internationalprocessplants.com/#organization",
            "name": "International Process Plants",
            "alternateName": "IPP",
            "url": "https://internationalprocessplants.com",
            "foundingDate": "1980",
            "description": "Global supplier of new and used process plants and equipment for chemical, pharmaceutical, and industrial applications.",
            "address": [
                {"@type": "PostalAddress", "addressCountry": "US", "addressLocality": "South Carolina"},
                {"@type": "PostalAddress", "addressCountry": "DE", "addressLocality": "Germany"},
                {"@type": "PostalAddress", "addressCountry": "GB", "addressLocality": "United Kingdom"},
            ],
            "numberOfEmployees": {"@type": "QuantitativeValue", "value": "150"},
            "areaServed": "Worldwide",
        },
        "mainEntity": {
            "@type": "Product",
            "name": f"Used {display_name}",
            "description": f"Used and surplus {display_name.lower()} from {mfr_text} and other manufacturers. {', '.join(materials[:4])} construction.{cap_text}",
            "brand": {"@type": "Brand", "name": "International Process Plants"},
            "category": "Process Equipment",
            "material": materials[:7],
            "offers": {
                "@type": "AggregateOffer",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "offerCount": round_count(stats["count"]),
                "description": f"Quote-based pricing. Used {display_name.lower()} available at significant savings compared to new equipment.",
            },
        },
        "hasPart": {
            "@type": "FAQPage",
            "@id": f"{full_url}#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f"How many {display_name.lower()} does IPP have in stock?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"IPP stocks {display_name.lower()} from manufacturers including {mfr_text}. {', '.join(materials[:4])} construction available.{cap_text}",
                    },
                },
                {
                    "@type": "Question",
                    "name": f"What materials of construction are available for {display_name.lower()}?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"IPP stocks {display_name.lower()} in {', '.join(materials)} construction.",
                    },
                },
                {
                    "@type": "Question",
                    "name": f"How much can I save buying used {display_name.lower()} versus new?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": f"Buying used {display_name.lower()} from IPP can save up to 50% of capital and 90% of lead time versus buying new. Exact savings depend on manufacturer, capacity, material of construction, and condition. Contact IPP for pricing on specific units.",
                    },
                },
            ],
        },
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [],
        },
    }

    for i, crumb in enumerate(breadcrumbs, 1):
        item = {"@type": "ListItem", "position": i, "name": crumb["name"]}
        if "url" in crumb:
            item["item"] = crumb["url"]
        schema["breadcrumb"]["itemListElement"].append(item)

    return json.dumps(schema, indent=6, ensure_ascii=False)


def generate_product_card(product, ims_url, badge_text=None):
    """Generate HTML for a single product card."""
    attrs = product.get("attributes", {})
    stock = product.get("stock_number", "")
    url = product.get("url", "")
    mfr = attrs.get("Manufacturer", "Unknown")
    mat = attrs.get("Material", "")
    cond = attrs.get("Condition", "Used")

    # Build card title
    cap_key = None
    for k in ["Capacity (Design)", "Capacity", "Total Heat Transfer Surface Area",
              "Heat Transfer Surface Area", "Filtration Area", "Evaporation Rate",
              "Cake Volume", "Vessel Size", "Basket Diameter", "Diameter"]:
        if k in attrs and attrs[k]:
            cap_key = k
            break

    cap_display = attrs.get(cap_key, "") if cap_key else ""
    # Extract just the metric value for title
    cap_short = cap_display.split("(")[0].strip() if cap_display else ""

    title_parts = [mfr]
    if mat:
        title_parts.append(mat)
    card_title = " ".join(title_parts)
    if cap_short:
        card_title += f" &mdash; {h(cap_short)}"

    icon = "fa-cog"
    mat_lower = mat.lower() if mat else ""
    if "glass" in mat_lower:
        icon = "fa-shield-halved"
    elif "hastelloy" in mat_lower or "titanium" in mat_lower:
        icon = "fa-flask-vial"
    elif "stainless" in mat_lower:
        icon = "fa-gears"
    else:
        icon = "fa-cog"

    specs = get_display_specs(product, max_specs=5)

    # Description
    desc_parts = []
    if cond:
        desc_parts.append(cond)
    desc_parts.append(h(mfr))
    if mat:
        desc_parts.append(h(mat))

    equip_type = attrs.get("Type", "equipment")
    desc = f"{' '.join(desc_parts)} {equip_type.lower()}."
    if cap_display:
        desc += f" {h(cap_display)}."

    badge_html = ""
    if badge_text:
        badge_html = f'<div class="badge-popular">{h(badge_text)}</div>'

    price_hint = ""
    if cond and "new" in cond.lower():
        price_hint = '<span class="price-hint">New equipment</span>'

    specs_html = ""
    for key, val, stk in specs:
        specs_html += f"""
                            <li class="src src-product" data-src-label="{h(key)} field: detail/{h(stk)}"><i class="fas fa-check"></i> {h(val)}</li>"""

    return f"""
                <div class="product-card">
                    {badge_html}
                    <div class="product-card-img"><i class="fas {icon}"></i></div>
                    <div class="product-card-body">
                        <h3>{card_title}</h3>
                        <p class="card-desc"><span class="src src-product" data-src-label="All specs from IMS product page: {h(url)}">{desc}</span><a href="{h(url)}" target="_blank" class="src-link"></a></p>
                        <ul class="specs">{specs_html}
                        </ul>
                        <div class="card-footer">
                            {price_hint}
                            <div class="card-footer-wrap">
                                <a href="/contact/" class="btn-card">Request Specs <i class="fas fa-arrow-right"></i></a>
                                <a href="{h(url)}" class="btn-inventory" target="_blank">View IPP# {h(stock)} <i class="fas fa-external-link-alt"></i></a>
                            </div>
                        </div>
                    </div>
                </div>"""


def generate_material_tabs(products, stats, display_name, ims_url):
    """Generate the product tabs section (by material)."""
    material_groups = group_products_by_material(products)

    # If fewer than 2 groups or very few products, skip tabs
    if len(material_groups) <= 1 and stats["count"] <= 5:
        # Just show all products directly, no tabs
        reps = pick_representative_products(products, min(3, len(products)))
        cards = ""
        for i, p in enumerate(reps):
            badge = "Featured" if i == 0 else None
            cards += generate_product_card(p, ims_url, badge_text=badge)
        return f"""
        <div class="product-grid">{cards}
        </div>
        <a href="{h(ims_url)}" class="browse-all-link" target="_blank"><i class="fas fa-search"></i> Browse All {h(display_name)} in Stock</a>"""

    # Limit to top 4 material groups for tabs
    tab_groups = material_groups[:4]
    if len(material_groups) > 4:
        # Merge remaining into "Other"
        other_products = []
        for mat, prods in material_groups[4:]:
            other_products.extend(prods)
        tab_groups.append(("Other Materials", other_products))

    # Generate tab nav
    tab_nav = '<div class="tab-nav" id="materialTabs">\n'
    for i, (mat_name, prods) in enumerate(tab_groups):
        active = ' class="active"' if i == 0 else ""
        tab_id = f"mat-{slug_from_name(mat_name)}"
        icon = "fa-cog"
        ml = mat_name.lower()
        if "glass" in ml:
            icon = "fa-shield-halved"
        elif "hastelloy" in ml or "titanium" in ml or "specialty" in ml or "nickel" in ml:
            icon = "fa-flask-vial"
        elif "stainless" in ml or "carbon" in ml:
            icon = "fa-gears"
        tab_nav += f'            <button{active} data-tab="{tab_id}"><i class="fas {icon}"></i> {h(mat_name)} ({len(prods)})</button>\n'
    tab_nav += "        </div>"

    # Generate tab contents
    tab_contents = ""
    for i, (mat_name, prods) in enumerate(tab_groups):
        active = " active" if i == 0 else ""
        tab_id = f"mat-{slug_from_name(mat_name)}"
        reps = pick_representative_products(prods, min(3, len(prods)))

        cards = ""
        for j, p in enumerate(reps):
            badge = f"Top {mat_name}" if j == 0 else None
            cards += generate_product_card(p, ims_url, badge_text=badge)

        tab_contents += f"""
        <div class="tab-content{active}" id="{tab_id}">
            <h3 style="font-size: 22px; font-weight: 700; color: var(--primary); margin-bottom: 12px;">Buy Used {h(mat_name)} {h(display_name)} for Sale</h3>
            <p style="color: var(--text-light); margin-bottom: 32px; max-width: 800px; line-height: 1.8;">{src("ims", f"Material field across IMS product pages: {mat_name} appears on {len(prods)} listings", f"IPP stocks {len(prods)} {mat_name.lower()} {display_name.lower()}", ims_url)}. Browse the inventory for current availability.</p>
            <div class="product-grid">{cards}
            </div>
            <a href="{h(ims_url)}" class="browse-all-link" target="_blank"><i class="fas fa-search"></i> Browse All {h(mat_name)} {h(display_name)} in Stock</a>
        </div>"""

    return f"""
        {tab_nav}
{tab_contents}"""


def generate_condition_tabs(products, stats, display_name, ims_url):
    """Generate the product tabs by condition."""
    cond_groups = {}
    for p in products:
        cond = p.get("attributes", {}).get("Condition", "Used")
        if not cond:
            cond = "Used"
        # Simplify conditions
        cl = cond.lower()
        if "re-glass" in cl or "reglass" in cl:
            key = "Re-Glassed"
        elif "new" in cl:
            key = "New"
        elif "unused" in cl:
            key = "Unused"
        elif "refurbish" in cl or "rebuilt" in cl:
            key = "Refurbished"
        elif "needs" in cl:
            key = "Needs Work"
        else:
            key = "Used"
        if key not in cond_groups:
            cond_groups[key] = []
        cond_groups[key].append(p)

    # Only create tabs if there are at least 2 condition types
    if len(cond_groups) <= 1:
        return ""

    # Order: Used first, then Re-Glassed, New, Unused, Refurbished, Needs Work
    order = ["Used", "Re-Glassed", "New", "Unused", "Refurbished", "Needs Work"]
    sorted_groups = [(k, cond_groups[k]) for k in order if k in cond_groups]

    cond_icons = {
        "Used": "fa-tools",
        "Re-Glassed": "fa-shield-halved",
        "New": "fa-box-open",
        "Unused": "fa-box-open",
        "Refurbished": "fa-wrench",
        "Needs Work": "fa-screwdriver-wrench",
    }

    tab_nav = '<div class="tab-nav" id="conditionTabs">\n'
    for i, (cond_name, prods) in enumerate(sorted_groups):
        active = ' class="active"' if i == 0 else ""
        tab_id = f"cond-{slug_from_name(cond_name)}"
        icon = cond_icons.get(cond_name, "fa-cog")
        tab_nav += f'            <button{active} data-tab="{tab_id}"><i class="fas {icon}"></i> {h(cond_name)} ({len(prods)})</button>\n'
    tab_nav += "        </div>"

    tab_contents = ""
    for i, (cond_name, prods) in enumerate(sorted_groups):
        active = " active" if i == 0 else ""
        tab_id = f"cond-{slug_from_name(cond_name)}"
        reps = pick_representative_products(prods, min(3, len(prods)))

        cards = ""
        for j, p in enumerate(reps):
            badge = f"{cond_name}" if j == 0 else None
            cards += generate_product_card(p, ims_url, badge_text=badge)

        tab_contents += f"""
        <div class="tab-content{active}" id="{tab_id}">
            <h3 style="font-size: 22px; font-weight: 700; color: var(--primary); margin-bottom: 12px;">Buy {h(cond_name)} {h(display_name)} for Sale</h3>
            <p style="color: var(--text-light); margin-bottom: 32px; max-width: 800px; line-height: 1.8;">{src("ims", f"Condition field across IMS product pages: {cond_name} on {len(prods)} listings", f"IPP stocks {len(prods)} {cond_name.lower()} {display_name.lower()}", ims_url)}. Browse the inventory for current availability.</p>
            <div class="product-grid">{cards}
            </div>
            <a href="{h(ims_url)}" class="browse-all-link" target="_blank"><i class="fas fa-search"></i> Browse All {h(cond_name)} {h(display_name)} in Stock</a>
        </div>"""

    return f"""
        {tab_nav}
{tab_contents}"""


def generate_advantages_section(display_name, stats, ims_url):
    """Generate the 6 advantage cards section."""
    materials = format_material_list(stats["materials"])
    manufacturers = format_manufacturer_list(stats["manufacturers"], max_display=4)
    mfr_text = ", ".join(manufacturers) if manufacturers else "multiple manufacturers"
    mat_text = ", ".join(materials[:4]) if materials else "multiple materials"

    cap_range = ""
    if stats["capacity_values"]:
        sorted_caps = sorted(stats["capacity_values"], key=lambda x: x[0])
        cap_range = f"from {sorted_caps[0][1].split('(')[0].strip()} to {sorted_caps[-1][1].split('(')[0].strip()}"

    pres_range = ""
    if stats["pressure_values"]:
        sorted_pres = sorted(stats["pressure_values"], key=lambda x: x[0])
        pres_range = f"Pressure ratings range from {sorted_pres[0][1]} to {sorted_pres[-1][1]}."

    has_glass = any("glass" in m.lower() for m in stats["materials"])

    reglassing_card = f"""
            <div class="advantage-card">
                <div class="advantage-icon"><i class="fas fa-shield-halved"></i></div>
                <h3>Refurbishment &amp; Re-Glassing</h3>
                <p>{src("about", "IPP About page: UGE 'Founded 1995; glass-lined steel equipment; stocks 700+ vessels and 2,700+ parts'", "IPP offers re-glassed equipment through its UGE (Universal Glasteel Equipment) division, founded in 1995, which stocks 700+ vessels and 2,700+ parts.", "https://internationalprocessplants.com/about/")} Contact IPP for refurbishment options.</p>
                <a href="/contact/" class="card-link">View Refurbishment Options <i class="fas fa-arrow-right"></i></a>
            </div>""" if has_glass else f"""
            <div class="advantage-card">
                <div class="advantage-icon"><i class="fas fa-shield-halved"></i></div>
                <h3>Quality Assured Equipment</h3>
                <p>{src("about", "IPP About page: IPP provides inspection and assessment services", "IPP provides equipment inspection and assessment services.")} {src("about", "IPP About page: GPS 'custom fabricated process equipment' with '12-16 week average delivery'", "IPP's GPS subsidiary also provides custom fabricated new equipment with 12&ndash;16 week average delivery.", "https://internationalprocessplants.com/about/")}</p>
                <a href="/contact/" class="card-link">Ask About Quality Assurance <i class="fas fa-arrow-right"></i></a>
            </div>"""

    return f"""
<!-- ===== ADVANTAGES ===== -->
<section id="advantages">
    <div class="container">
        <div class="section-header">
            <h2>Advantages of Buying <span>Used {h(display_name)}</span> from IPP</h2>
            <p>{src("homepage", "IPP homepage: 'over 46 years of experience'", "International Process Plants combines over 46 years of process equipment expertise", "https://internationalprocessplants.com")}, {src("homepage", "IPP homepage: 'nearly 150 colleagues around the world'", "nearly 150 colleagues")} across {src("about", "IPP About page lists 15 countries by name", "15 countries", "https://internationalprocessplants.com/about/")} to deliver {display_name.lower()} ready for your process.</p>
        </div>

        <div class="advantage-grid">
            <div class="advantage-card">
                <div class="advantage-icon"><i class="fas fa-piggy-bank"></i></div>
                <h3>Significant Cost Savings</h3>
                <p>{src("homepage", "IPP homepage exact quote for used equipment systems savings", f"Buying used {display_name.lower()} from IPP can save up to 50% of capital and 90% of lead time versus buying new.", "https://internationalprocessplants.com")} With a broad inventory from multiple manufacturers, IPP offers a wide selection to match your budget and specifications.</p>
                <a href="/contact/" class="card-link">Request a Quote <i class="fas fa-arrow-right"></i></a>
            </div>
            <div class="advantage-card">
                <div class="advantage-icon"><i class="fas fa-truck-fast"></i></div>
                <h3>Immediate Availability</h3>
                <p>In-stock {display_name.lower()} from IPP are ready to ship. New OEM equipment requires extended lead times for engineering, procurement, and fabrication. {src("about", "IPP About page: GPS 'custom fabricated process equipment' with '12-16 week average delivery'", "IPP's GPS subsidiary also provides custom fabricated new equipment with 12&ndash;16 week average delivery.", "https://internationalprocessplants.com/about/")}</p>
                <a href="/contact/" class="card-link">Check Availability <i class="fas fa-arrow-right"></i></a>
            </div>
            <div class="advantage-card">
                <div class="advantage-icon"><i class="fas fa-industry"></i></div>
                <h3>Multiple OEM Manufacturers in Stock</h3>
                <p>{src("ims", f"Manufacturer field across IMS product pages: {mfr_text} all appear as distinct manufacturers", f"IPP stocks {display_name.lower()} from {mfr_text}, and additional manufacturers.")} {src("ims", "Each IMS product page shows OEM Manufacturer field with traceable stock number", "Every unit is an original OEM product with traceable provenance.")}</p>
                <a href="/contact/" class="card-link">Browse Manufacturers <i class="fas fa-arrow-right"></i></a>
            </div>
{reglassing_card}
            <div class="advantage-card">
                <div class="advantage-icon"><i class="fas fa-globe"></i></div>
                <h3>Global Presence in 15 Countries</h3>
                <p>{src("about", "IPP About page lists all 15 countries by name", "IPP operates offices in 15 countries: Brazil, Canada, China, Czech Republic, France, Germany, India, Italy, Mexico, Pakistan, Portugal, Romania, Turkey, United Kingdom, and United States.", "https://internationalprocessplants.com/about/")} {src("homepage", "IPP homepage: 'more than 160,000 customers worldwide'", "IPP has served 160,000+ customers worldwide.", "https://internationalprocessplants.com")}</p>
                <a href="/contact/" class="card-link">Find Nearest Office <i class="fas fa-arrow-right"></i></a>
            </div>
            <div class="advantage-card">
                <div class="advantage-icon"><i class="fas fa-flask-vial"></i></div>
                <h3>Full Range of Materials &amp; Specs</h3>
                <p>{src("ims", f"All specs from Material and key attribute fields across {stats['count']} IMS product pages", f"Material of construction includes {mat_text}. {cap_range + '.' if cap_range else ''} {pres_range}")}</p>
                <a href="/contact/" class="card-link">Talk to an Engineer <i class="fas fa-arrow-right"></i></a>
            </div>
        </div>
    </div>
</section>"""


def generate_how_it_works(display_name):
    """Generate the 5-step how-it-works section."""
    equip_singular = display_name.rstrip("s")
    if display_name.endswith("ies"):
        equip_singular = display_name[:-3] + "y"
    elif display_name.endswith("ves"):
        equip_singular = display_name[:-3] + "f"

    return f"""
<!-- ===== HOW IT WORKS ===== -->
<section id="process">
    <div class="container">
        <div class="section-header">
            <h2>How Buying a <span>Used {h(equip_singular)}</span> Works</h2>
            <p>The process of purchasing used {display_name.lower()} from IPP follows five steps, from specification to delivery.</p>
        </div>

        <div class="process-grid">
            <div class="process-step">
                <div class="step-number">1</div>
                <h4>Submit Requirements</h4>
                <p>Share your equipment specifications: capacity, material of construction, pressure rating, temperature, and application. Or browse our searchable inventory.</p>
            </div>
            <div class="process-step">
                <div class="step-number">2</div>
                <h4>Receive Data Package</h4>
                <p>IPP sends a detailed equipment data sheet with specifications, dimensions, condition report, and photographs.</p>
            </div>
            <div class="process-step">
                <div class="step-number">3</div>
                <h4>Inspect the Equipment</h4>
                <p>Contact IPP to arrange an on-site visit or request a live video walkthrough with an IPP engineer at one of our global locations.</p>
            </div>
            <div class="process-step">
                <div class="step-number">4</div>
                <h4>Refurbishment Options</h4>
                <p>IPP offers refurbishment services. Contact IPP for details on available reconditioning, re-glassing, and testing options.</p>
            </div>
            <div class="process-step">
                <div class="step-number">5</div>
                <h4>Packaging &amp; Delivery</h4>
                <p>IPP coordinates packaging, crating, freight, and delivery to your plant site. Worldwide shipping from offices in 15 countries.</p>
            </div>
        </div>
    </div>
</section>"""


def generate_industries_section(display_name, ims_url):
    """Generate the industries section."""
    return f"""
<!-- ===== INDUSTRIES SERVED ===== -->
<section id="industries">
    <div class="container">
        <div class="section-header">
            <h2>Industries That Buy <span>Used {h(display_name)}</span></h2>
            <p>{src("category", "IMS category page lists industrial applications for this equipment type", f"IPP supplies used {display_name.lower()} to manufacturers across multiple process industries worldwide.", ims_url)}</p>
        </div>

        <div class="industry-grid">
            {"".join(f'<div class="industry-tag"><i class="fas {icon}"></i> {name}</div>' + chr(10) + "            " for icon, name in INDUSTRY_ICONS)}
        </div>
    </div>
</section>"""


def generate_faq_section(cat, stats):
    """Generate FAQ section with 3 questions using real data."""
    data_folder, lp_folder, display_name, url_path, ims_url, query = cat
    materials = format_material_list(stats["materials"])
    manufacturers = format_manufacturer_list(stats["manufacturers"], max_display=6)
    mfr_text = ", ".join(manufacturers) if manufacturers else "multiple manufacturers"
    mat_text = ", ".join(materials[:4]) if materials else "multiple materials"

    cap_range_text = ""
    if stats["capacity_values"]:
        sorted_caps = sorted(stats["capacity_values"], key=lambda x: x[0])
        cap_range_text = f"from {sorted_caps[0][1]} to {sorted_caps[-1][1]}"

    conditions = [c for c, _ in stats["conditions"].most_common()]
    cond_text = ", ".join(conditions) if conditions else "various conditions"

    # FAQ 1: How many in stock?
    faq1_q = f"How many {display_name.lower()} does IPP have in stock?"
    faq1_a = f"""{src("ims", f"Manufacturer field across IMS product pages: {len(stats['manufacturers'])} unique manufacturers", f"IPP stocks {display_name.lower()} from {mfr_text}, and additional manufacturers.")} {src("ims", f"Material field across IMS product pages: {mat_text}", f"The inventory includes {mat_text} construction.")}"""
    if cap_range_text:
        faq1_a += f" {src('ims', f'Capacity field: {cap_range_text}', f'Capacities range {cap_range_text}.')}"
    faq1_a += f' Browse the <a href="{h(ims_url)}" target="_blank">IMS inventory</a> for current availability.'

    # FAQ 2: What materials?
    faq2_q = f"What materials of construction are available for {display_name.lower()}?"
    faq2_a = f"""{src("ims", f"Material field on IMS product pages: {', '.join(materials)}", f"IPP stocks {display_name.lower()} in {', '.join(materials)} construction.")}"""
    faq2_a += f" Browse the inventory to see current availability by material."

    # FAQ 3: Savings?
    faq3_q = f"How much can I save buying used {display_name.lower()} versus new?"
    faq3_a = f"""{src("homepage", "IPP homepage exact quote for used equipment systems savings", f"Buying used {display_name.lower()} from IPP can save up to 50% of capital and 90% of lead time versus buying new.", "https://internationalprocessplants.com")} The exact savings depend on manufacturer, capacity, material of construction, and condition. Contact IPP for pricing on specific units."""

    # FAQ 4: Conditions available
    faq4_q = f"What condition grades are available for {display_name.lower()}?"
    faq4_a = f"""{src("ims", f"Condition field across IMS product pages: {cond_text}", f"IPP stocks {display_name.lower()} in {cond_text} condition.")}"""
    if any("re-glass" in c.lower() or "reglass" in c.lower() for c in conditions):
        faq4_a += f" {src('about', 'IPP About page: UGE provides glass-lined equipment services', 'Re-glassed units have received new borosilicate glass linings through IPP&#39;s UGE division.', 'https://internationalprocessplants.com/about/')}"
    faq4_a += " Browse the current inventory for available condition options."

    # FAQ 5: Delivery time
    faq5_q = f"How long does it take to receive {display_name.lower()} from IPP?"
    faq5_a = f"""{src("category", "IMS category page: surplus and used equipment in stock and ready to ship", f"In-stock {display_name.lower()} are ready to ship.", ims_url)} Equipment requiring refurbishment ships on a timeline that depends on scope. {src("about", "IPP About page: GPS '12-16 week average delivery'", "IPP's GPS subsidiary provides new custom fabricated equipment with 12&ndash;16 week average delivery.", "https://internationalprocessplants.com/about/")} {src("about", "IPP About page lists 15 countries by name", "IPP ships from offices in 15 countries worldwide.")}"""

    # FAQ 6: Inspection
    faq6_q = f"Can I visit IPP to inspect {display_name.lower()} before buying?"
    faq6_a = f"""Contact IPP to arrange a visit or discuss inspection options for specific equipment. {src("about", "IPP About page lists all 15 countries by name", "IPP operates offices in 15 countries: Brazil, Canada, China, Czech Republic, France, Germany, India, Italy, Mexico, Pakistan, Portugal, Romania, Turkey, United Kingdom, and United States.", "https://internationalprocessplants.com/about/")}"""

    return f"""
<!-- ===== FAQ SECTION ===== -->
<section id="faq">
    <div class="container">
        <div class="section-header">
            <h2>Frequently Asked Questions About <span>Buying Used {h(display_name)}</span></h2>
            <p>Answers to the most common questions from engineers and procurement teams evaluating used {display_name.lower()}.</p>
        </div>

        <div class="faq-wrapper">
            <div class="faq-tab-nav" id="faqTabs">
                <button class="active" data-faqtab="faq-inventory">Inventory</button>
                <button data-faqtab="faq-process">Process</button>
            </div>

            <!-- Inventory Tab -->
            <div class="faq-tab-content active" id="faq-inventory">
                <div class="faq-item">
                    <button class="faq-question">{h(faq1_q)} <i class="fas fa-chevron-down"></i></button>
                    <div class="faq-answer">{faq1_a}</div>
                </div>
                <div class="faq-item">
                    <button class="faq-question">{h(faq2_q)} <i class="fas fa-chevron-down"></i></button>
                    <div class="faq-answer">{faq2_a}</div>
                </div>
                <div class="faq-item">
                    <button class="faq-question">{h(faq3_q)} <i class="fas fa-chevron-down"></i></button>
                    <div class="faq-answer">{faq3_a}</div>
                </div>
                <div class="faq-item">
                    <button class="faq-question">{h(faq4_q)} <i class="fas fa-chevron-down"></i></button>
                    <div class="faq-answer">{faq4_a}</div>
                </div>
            </div>

            <!-- Process Tab -->
            <div class="faq-tab-content" id="faq-process">
                <div class="faq-item">
                    <button class="faq-question">{h(faq5_q)} <i class="fas fa-chevron-down"></i></button>
                    <div class="faq-answer">{faq5_a}</div>
                </div>
                <div class="faq-item">
                    <button class="faq-question">{h(faq6_q)} <i class="fas fa-chevron-down"></i></button>
                    <div class="faq-answer">{faq6_a}</div>
                </div>
            </div>
        </div>
    </div>
</section>"""


def generate_comparison_table(display_name, stats, ims_url):
    """Generate Used vs New comparison table."""
    materials = format_material_list(stats["materials"])
    mat_text = ", ".join(materials[:4]) if materials else "multiple materials"

    cap_range = ""
    if stats["capacity_values"]:
        sorted_caps = sorted(stats["capacity_values"], key=lambda x: x[0])
        cap_range = f"{sorted_caps[0][1].split('(')[0].strip()} to {sorted_caps[-1][1].split('(')[0].strip()}"

    pres_range = ""
    if stats["pressure_values"]:
        sorted_pres = sorted(stats["pressure_values"], key=lambda x: x[0])
        pres_range = f"{sorted_pres[0][1]} to {sorted_pres[-1][1]}"

    cap_row = ""
    if cap_range:
        cap_row = f"""
                <tr>
                    <td><strong>Available Capacities</strong></td>
                    <td>{src("ims", f"Capacity field across IMS product pages: {cap_range}", f"{cap_range} (multiple units in stock)")}</td>
                    <td>Custom-built to specification</td>
                </tr>"""

    pres_row = ""
    if pres_range:
        pres_row = f"""
                <tr>
                    <td><strong>Pressure Ratings</strong></td>
                    <td>{src("ims", f"Pressure field across IMS product pages: {pres_range}", f"{pres_range} (from inventory)")}</td>
                    <td>Custom-engineered to specification</td>
                </tr>"""

    return f"""
<!-- ===== COMPARISON TABLE: USED vs NEW ===== -->
<section id="comparison">
    <div class="container">
        <div class="section-header">
            <h2>Buying Used {h(display_name)} vs <span>Buying New</span></h2>
            <p>{src("homepage", "IPP homepage exact quote for used equipment systems savings", f"Buying used {display_name.lower()} from IPP can save up to 50% of capital and 90% of lead time versus buying new.", "https://internationalprocessplants.com")} Here is how used and new {display_name.lower()} compare across key factors.</p>
        </div>

        <table class="comparison-table">
            <thead>
                <tr>
                    <th>Factor</th>
                    <th>Used from IPP</th>
                    <th>New (OEM)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Equipment Cost</strong></td>
                    <td class="highlight">{src("homepage", "IPP homepage: used equipment saves '50 percent of capital versus new'", "Significant savings vs new OEM price")}</td>
                    <td>Full OEM list price</td>
                </tr>
                <tr>
                    <td><strong>Delivery Timeline</strong></td>
                    <td class="highlight">{src("category", f"IMS category page: surplus and used {display_name.lower()} in stock and ready to ship", "In-stock units ready to ship")}</td>
                    <td>Extended lead times (new fabrication)</td>
                </tr>{cap_row}
                <tr>
                    <td><strong>Materials</strong></td>
                    <td>{src("ims", f"Material field across IMS product pages: {mat_text}", mat_text)}</td>
                    <td>Custom-specified</td>
                </tr>{pres_row}
            </tbody>
        </table>
    </div>
</section>"""


def generate_full_page(cat, products, stats, cat_page_data, cat_desc_url):
    """Generate the complete HTML page for a category."""
    data_folder, lp_folder, display_name, url_path, ims_url, query = cat

    full_url = f"https://internationalprocessplants.com{url_path}"
    breadcrumbs = build_breadcrumbs(url_path, display_name)
    schema_json = generate_schema_json(cat, stats, breadcrumbs)

    materials = format_material_list(stats["materials"])
    manufacturers = format_manufacturer_list(stats["manufacturers"], max_display=4)
    mfr_text = ", ".join(manufacturers) if manufacturers else "multiple manufacturers"
    mat_text = ", ".join(materials[:4]) if materials else "multiple materials"

    # Meta description
    cap_range_meta = ""
    if stats["capacity_values"]:
        sorted_caps = sorted(stats["capacity_values"], key=lambda x: x[0])
        cap_range_meta = f" {sorted_caps[0][1].split('(')[0].strip()} to {sorted_caps[-1][1].split('(')[0].strip()}."

    meta_desc = f"Buy used {display_name.lower()} for sale from IPP. {mfr_text} &amp; more manufacturers. {mat_text}.{cap_range_meta} Ships worldwide."

    # Title slug for filename
    slug = slug_from_name(display_name)

    # Equipment icon
    equip_icon = get_equipment_icon(data_folder)

    # Hero intro text
    intro_text = f"""Buying used {display_name.lower()} through International Process Plants gives {src("category", f"IMS category page lists industrial applications for {display_name.lower()}", "chemical, pharmaceutical, biotech, and specialty manufacturers")} access to {src("ims", f"Material field across {stats['count']} IMS product pages", f"{mat_text} construction")} from {src("ims", f"Manufacturer field across {stats['count']} IMS product pages", mfr_text, ims_url)}."""

    # Expandable details
    expand_parts = []
    if materials:
        expand_parts.append(f"""{src("ims", f"Material field across {stats['count']} IMS product pages — each grade appears as distinct value", f"Material of construction includes {', '.join(materials)}.")}""")
    if stats["capacity_values"]:
        sorted_caps = sorted(stats["capacity_values"], key=lambda x: x[0])
        min_cap = sorted_caps[0]
        max_cap = sorted_caps[-1]
        expand_parts.append(f"""{src("ims", f"Capacity field: smallest {min_cap[1]}, largest {max_cap[1]} on IPP# {max_cap[2]['stock_number']}", f"Capacities range from {min_cap[1]} to {max_cap[1]}.", max_cap[2]['url'])}""")
    if stats["pressure_values"]:
        sorted_pres = sorted(stats["pressure_values"], key=lambda x: x[0])
        expand_parts.append(f"""{src("ims", f"Pressure field: lowest {sorted_pres[0][1]}, highest {sorted_pres[-1][1]}", f"Pressure ratings range from {sorted_pres[0][1]} to {sorted_pres[-1][1]}.")}""")
    if stats["conditions"]:
        cond_list = [c for c, _ in stats["conditions"].most_common()]
        expand_parts.append(f"""{src("ims", f"Condition field across {stats['count']} IMS product pages shows: {', '.join(cond_list)}", f"Condition options include {', '.join(cond_list).lower()}.")}""")

    expand_parts.append(f"""{src("homepage", "IPP homepage exact quote for used equipment systems savings", f"Buying used {display_name.lower()} from IPP can save up to 50% of capital and 90% of lead time versus buying new.", "https://internationalprocessplants.com")}""")

    expand_text_first = expand_parts[0] if expand_parts else ""
    expand_text_rest = " ".join(expand_parts[1:]) if len(expand_parts) > 1 else ""

    # Truncated preview for expand
    # Take first ~80 chars of the first expand part for the truncated view
    truncated_preview = ""
    if materials:
        truncated_preview = f"Material of construction includes {', '.join(materials[:3])}..."

    # Hero stats
    count_display = round_count(stats["count"])

    # Hero feature cards (right side) - pick 2-3 representative product links
    feature_cards = ""
    if stats["count"] > 0:
        top_materials_for_cards = []
        for mat_name, count in stats["materials"].most_common(3):
            # Find a representative product of this material
            for p in products:
                if p.get("attributes", {}).get("Material", "") == mat_name:
                    top_materials_for_cards.append((mat_name, p))
                    break

        if not top_materials_for_cards:
            # Fallback: just pick top products
            for p in pick_representative_products(products, 3):
                mat = p.get("attributes", {}).get("Material", "Equipment")
                top_materials_for_cards.append((mat, p))

        for mat_name, p in top_materials_for_cards[:3]:
            mat_lower = mat_name.lower()
            icon = "fa-cog"
            if "glass" in mat_lower:
                icon = "fa-shield-halved"
            elif "hastelloy" in mat_lower or "titanium" in mat_lower:
                icon = "fa-flask-vial"
            elif "stainless" in mat_lower:
                icon = "fa-gears"

            mfr_list = ", ".join([m for m, _ in stats["manufacturers"].most_common(3) if any(
                pp.get("attributes", {}).get("Material", "") == mat_name and pp.get("attributes", {}).get("Manufacturer", "") == m
                for pp in products
            )][:2]) or mfr_text

            feature_cards += f"""
                <a href="{h(p['url'])}" target="_blank" style="display: flex; align-items: center; gap: 16px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 14px; padding: 20px 24px; text-decoration: none; transition: all 0.3s; color: #fff;" onmouseover="this.style.background='rgba(26,143,196,0.15)';this.style.borderColor='var(--accent)'" onmouseout="this.style.background='rgba(255,255,255,0.08)';this.style.borderColor='rgba(255,255,255,0.15)'">
                    <i class="fas {icon}" style="font-size: 36px; color: var(--accent); width: 48px; text-align: center;"></i>
                    <div>
                        <div style="font-size: 17px; font-weight: 700;">{h(mat_name)} {h(display_name)}</div>
                        <div style="font-size: 13px; color: rgba(255,255,255,0.6);">{h(mfr_list)} &amp; more</div>
                    </div>
                    <i class="fas fa-arrow-right" style="margin-left: auto; color: var(--accent); font-size: 14px;"></i>
                </a>"""

    # Generate material tabs section
    material_tabs_html = generate_material_tabs(products, stats, display_name, ims_url)

    # Generate condition tabs section
    condition_tabs_html = generate_condition_tabs(products, stats, display_name, ims_url)

    # Generate comparison table
    comparison_html = generate_comparison_table(display_name, stats, ims_url)

    # Generate advantages
    advantages_html = generate_advantages_section(display_name, stats, ims_url)

    # Generate how it works
    how_it_works_html = generate_how_it_works(display_name)

    # Generate industries
    industries_html = generate_industries_section(display_name, ims_url)

    # Generate FAQ
    faq_html = generate_faq_section(cat, stats)

    # Short name for CTA
    short_name = display_name
    if len(short_name) > 30:
        # Try to shorten
        short_name = short_name.split("&")[0].strip()

    # Condition tabs section (only if meaningful)
    condition_section = ""
    if condition_tabs_html:
        condition_section = f"""
<!-- ===== PRODUCT TABS: BY CONDITION ===== -->
<section id="equipment-by-condition">
    <div class="container">
        <div class="section-header">
            <h2>Buy {h(display_name)} for Sale <span>by Condition</span></h2>
            <p>{src("ims", f"Condition field across IMS product pages: {', '.join(c for c, _ in stats['conditions'].most_common())}", f"IPP stocks {display_name.lower()} in multiple condition grades.")} Choose the condition that matches your budget and performance requirements.</p>
        </div>
{condition_tabs_html}
    </div>
</section>"""

    # ============================================================
    # ASSEMBLE THE FULL HTML
    # ============================================================
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[INTERNAL REVIEW] Buy Used {h(display_name)} for Sale</title>
    <meta name="description" content="{meta_desc}">
    <meta name="robots" content="noindex, nofollow">
    <link rel="canonical" href="{full_url}">

    <script type="application/ld+json">
    {schema_json}
    </script>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <style>
        :root {{
            --primary: #192e37;
            --primary-light: #154b63;
            --accent: #1a8fc4;
            --accent-hover: #1678a6;
            --success: #2e7d32;
            --warning: #e67e22;
            --text: #2c3e50;
            --text-light: #626265;
            --bg: #ffffff;
            --bg-alt: #f4f7f9;
            --bg-dark: #192e37;
            --border: #e0e6eb;
            --card-shadow: 0 2px 16px rgba(25, 46, 55, 0.08);
            --card-hover: 0 8px 32px rgba(25, 46, 55, 0.14);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        html, body {{
            overflow-x: hidden;
            width: 100%;
            max-width: 100vw;
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text);
            line-height: 1.7;
            background: var(--bg);
        }}

        .container {{ max-width: 1248px; margin: 0 auto; padding: 0 24px; }}

        /* ===== HEADER ===== */
        .header {{
            background: var(--primary);
            padding: 16px 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .header .container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .header-logo {{
            color: #fff;
            font-size: 20px;
            font-weight: 800;
            text-decoration: none;
            letter-spacing: -0.5px;
        }}
        .header-logo span {{ color: var(--accent); }}
        .header-nav {{ display: flex; gap: 28px; align-items: center; }}
        .header-nav a {{
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: color 0.2s;
        }}
        .header-nav a:hover {{ color: #fff; }}
        .header-nav .btn-quote {{
            background: var(--accent);
            color: #fff;
            padding: 10px 22px;
            border-radius: 6px;
            font-weight: 600;
            transition: background 0.2s;
        }}
        .header-nav .btn-quote:hover {{ background: var(--accent-hover); }}

        /* ===== HERO ===== */
        .hero {{
            background-color: #192e37;
            background-image: url('https://internationalprocessplants.com/wp-content/uploads/2024/07/ipp-featured-basic.jpg');
            background-size: cover;
            background-position: center;
            background-blend-mode: overlay;
            padding: 80px 0 70px;
            color: #fff;
            position: relative;
        }}
        .hero::before {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(230deg, rgba(21, 75, 99, 0.92), rgba(25, 46, 55, 0.96));
            z-index: 0;
        }}
        .hero > .container {{ position: relative; z-index: 1; }}
        .hero-content {{ overflow-wrap: break-word; word-wrap: break-word; min-width: 0; }}
        .hero-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
        }}
        .hero h1 {{
            font-size: 42px;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 24px;
            letter-spacing: -1px;
        }}
        .hero h1 span {{ color: var(--accent); }}
        .hero .intro-text {{
            font-size: 16px;
            line-height: 1.8;
            color: rgba(255,255,255,0.85);
            margin-bottom: 32px;
        }}
        .hero .intro-expand {{
            font-size: 16px;
            line-height: 1.8;
            color: rgba(255,255,255,0.85);
            margin-bottom: 32px;
        }}
        .hero .intro-expand summary {{
            list-style: none;
            cursor: pointer;
            font-size: inherit;
            line-height: inherit;
            color: inherit;
        }}
        .hero .intro-expand summary::-webkit-details-marker {{ display: none; }}
        .hero .intro-expand .arrow-expand {{
            color: var(--accent);
            font-size: 18px;
            cursor: pointer;
        }}
        .hero .intro-expand[open] summary .truncated {{
            display: none;
        }}
        .hero .intro-expand[open] summary .arrow-expand {{
            display: none;
        }}
        .hero .intro-expand .intro-rest {{
            margin-top: 16px;
        }}
        .hero .intro-expand .arrow-collapse {{
            color: var(--accent);
            font-size: 18px;
            cursor: pointer;
        }}

        /* Trust badges */
        .trust-badges {{
            display: flex;
            gap: 20px;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }}
        .trust-badge {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            font-weight: 600;
            color: rgba(255,255,255,0.9);
            background: rgba(255,255,255,0.08);
            padding: 8px 16px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .trust-badge i {{ color: var(--accent); font-size: 16px; }}

        /* Hero CTA */
        .hero-cta-group {{ display: flex; gap: 16px; margin-bottom: 40px; }}
        .btn-primary {{
            background: var(--accent);
            color: #fff;
            padding: 14px 32px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 15px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            transition: all 0.2s;
            border: none;
            cursor: pointer;
        }}
        .btn-primary:hover {{ background: var(--accent-hover); transform: translateY(-1px); }}
        .btn-secondary {{
            background: transparent;
            color: #fff;
            padding: 14px 32px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 15px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            border: 2px solid rgba(255,255,255,0.3);
            transition: all 0.2s;
        }}
        .btn-secondary:hover {{ border-color: #fff; }}

        /* Hero stats */
        .hero-stats {{
            display: flex;
            gap: 32px;
            padding-top: 24px;
            border-top: 1px solid rgba(255,255,255,0.15);
        }}
        .hero-stat .number {{
            font-size: 32px;
            font-weight: 800;
            color: var(--accent);
            display: block;
        }}
        .hero-stat .label {{
            font-size: 13px;
            color: rgba(255,255,255,0.7);
            line-height: 1.4;
        }}

        /* Hero image area */
        .hero-image {{
            position: relative;
            text-align: center;
        }}

        /* ===== SECTION COMMON ===== */
        section {{ padding: 80px 0; }}
        section:nth-child(even) {{ background: var(--bg-alt); }}

        .section-header {{
            text-align: center;
            max-width: 720px;
            margin: 0 auto 48px;
        }}
        .section-header h2 {{
            font-size: 34px;
            font-weight: 800;
            margin-bottom: 16px;
            letter-spacing: -0.5px;
            color: var(--primary);
        }}
        .section-header h2 span {{ color: var(--accent); }}
        .section-header p {{
            font-size: 16px;
            color: var(--text-light);
            line-height: 1.8;
        }}

        /* ===== TABS ===== */
        .tab-nav {{
            display: flex;
            gap: 4px;
            background: var(--bg-alt);
            padding: 5px;
            border-radius: 12px;
            justify-content: center;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }}
        .tab-nav button {{
            padding: 12px 24px;
            border: none;
            background: transparent;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            color: var(--text-light);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
            font-family: inherit;
        }}
        .tab-nav button.active {{
            background: #fff;
            color: var(--primary);
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .tab-nav button:hover:not(.active) {{ color: var(--primary); }}
        .tab-nav button i {{ font-size: 16px; }}

        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}

        /* ===== PRODUCT CARDS ===== */
        .product-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
        }}
        .product-card {{
            background: #fff;
            border-radius: 14px;
            border: 1px solid var(--border);
            overflow: hidden;
            transition: all 0.3s;
            position: relative;
        }}
        .product-card:hover {{
            box-shadow: var(--card-hover);
            transform: translateY(-4px);
            border-color: var(--accent);
        }}
        .badge-popular {{
            position: absolute;
            top: 12px;
            right: 12px;
            background: var(--accent);
            color: #fff;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .product-card-img {{
            position: relative;
            height: 200px;
            background: var(--bg-alt);
            display: flex;
            align-items: center;
            justify-content: center;
            border-bottom: 1px solid var(--border);
            overflow: hidden;
        }}
        .product-card-img i {{
            font-size: 64px;
            color: var(--primary-light);
            opacity: 0.3;
        }}
        .product-card-body {{ padding: 24px; }}
        .product-card h3 {{
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--primary);
        }}
        .product-card .card-desc {{
            font-size: 14px;
            color: var(--text-light);
            margin-bottom: 16px;
            line-height: 1.6;
        }}
        .product-card .specs {{
            list-style: none;
            margin-bottom: 20px;
        }}
        .product-card .specs li {{
            font-size: 13px;
            padding: 6px 0;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--text);
        }}
        .product-card .specs li:last-child {{ border-bottom: none; }}
        .product-card .specs li i {{ color: var(--accent); font-size: 12px; width: 16px; }}
        .product-card .card-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .product-card .price-hint {{
            font-size: 13px;
            color: var(--success);
            font-weight: 600;
        }}
        .btn-card {{
            background: var(--primary);
            color: #fff;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
            border: none;
            cursor: pointer;
            font-family: inherit;
        }}
        .btn-card:hover {{ background: var(--primary-light); }}
        .btn-inventory {{
            color: var(--accent);
            font-size: 12px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: color 0.2s;
        }}
        .btn-inventory:hover {{ color: var(--accent-hover); text-decoration: underline; }}
        .card-footer-wrap {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .browse-all-link {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: var(--accent);
            font-weight: 600;
            font-size: 14px;
            text-decoration: none;
            margin-top: 16px;
            transition: color 0.2s;
        }}
        .browse-all-link:hover {{ color: var(--accent-hover); text-decoration: underline; }}

        /* ===== ADVANTAGE CARDS ===== */
        .advantage-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
        }}
        .advantage-card {{
            background: #fff;
            border-radius: 14px;
            padding: 32px;
            border: 1px solid var(--border);
            transition: all 0.3s;
        }}
        .advantage-card:hover {{
            box-shadow: var(--card-hover);
            transform: translateY(-4px);
        }}
        .advantage-icon {{
            width: 52px;
            height: 52px;
            background: rgba(26, 143, 196, 0.1);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
        }}
        .advantage-icon i {{ font-size: 22px; color: var(--accent); }}
        .advantage-card h3 {{
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 10px;
            color: var(--primary);
        }}
        .advantage-card p {{
            font-size: 14px;
            color: var(--text-light);
            line-height: 1.7;
            margin-bottom: 16px;
        }}
        .advantage-card .card-link {{
            color: var(--accent);
            font-size: 13px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}

        /* ===== FAQ ===== */
        .faq-wrapper {{
            max-width: 880px;
            margin: 0 auto;
        }}
        .faq-tab-nav {{
            display: flex;
            gap: 4px;
            background: var(--bg-alt);
            padding: 5px;
            border-radius: 12px;
            justify-content: center;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }}
        .faq-tab-nav button {{
            padding: 10px 20px;
            border: none;
            background: transparent;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-light);
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }}
        .faq-tab-nav button.active {{
            background: #fff;
            color: var(--primary);
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .faq-item {{
            border: 1px solid var(--border);
            border-radius: 12px;
            margin-bottom: 12px;
            overflow: hidden;
            background: #fff;
        }}
        .faq-question {{
            padding: 20px 24px;
            font-size: 15px;
            font-weight: 600;
            color: var(--primary);
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.2s;
            width: 100%;
            border: none;
            background: #fff;
            text-align: left;
            font-family: inherit;
        }}
        .faq-question:hover {{ background: var(--bg-alt); }}
        .faq-question i {{ font-size: 14px; color: var(--accent); transition: transform 0.3s; }}
        .faq-answer {{
            padding: 0 24px 20px;
            font-size: 14px;
            color: var(--text-light);
            line-height: 1.8;
            display: none;
        }}
        .faq-item.open .faq-answer {{ display: block; }}
        .faq-item.open .faq-question i {{ transform: rotate(180deg); }}

        /* ===== CTA BANNER ===== */
        .cta-banner {{
            background: linear-gradient(230deg, var(--primary-light), var(--primary));
            padding: 64px 0;
            color: #fff;
            text-align: center;
        }}
        .cta-banner h2 {{
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 16px;
        }}
        .cta-banner p {{
            font-size: 16px;
            color: rgba(255,255,255,0.8);
            max-width: 600px;
            margin: 0 auto 32px;
            line-height: 1.7;
        }}
        .cta-banner .btn-primary {{ font-size: 16px; padding: 16px 36px; }}

        /* ===== INDUSTRIES ===== */
        .industry-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
        }}
        .industry-tag {{
            background: #fff;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
            text-align: center;
            font-size: 13px;
            font-weight: 600;
            color: var(--text);
            transition: all 0.2s;
        }}
        .industry-tag:hover {{
            border-color: var(--accent);
            color: var(--accent);
        }}
        .industry-tag i {{
            display: block;
            font-size: 24px;
            margin-bottom: 8px;
            color: var(--accent);
        }}

        /* ===== PROCESS STEPS ===== */
        .process-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
        }}
        .process-step {{
            text-align: center;
            padding: 24px 16px;
            position: relative;
        }}
        .process-step .step-number {{
            width: 44px;
            height: 44px;
            background: var(--accent);
            color: #fff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 16px;
            margin: 0 auto 16px;
        }}
        .process-step h4 {{
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--primary);
        }}
        .process-step p {{
            font-size: 13px;
            color: var(--text-light);
            line-height: 1.5;
        }}

        /* ===== COMPARISON TABLE ===== */
        .comparison-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border);
            margin: 32px 0;
        }}
        .comparison-table thead th {{
            background: var(--primary);
            color: #fff;
            padding: 16px 20px;
            font-size: 14px;
            font-weight: 600;
            text-align: left;
        }}
        .comparison-table tbody td {{
            padding: 14px 20px;
            font-size: 14px;
            border-bottom: 1px solid var(--border);
        }}
        .comparison-table tbody tr:last-child td {{ border-bottom: none; }}
        .comparison-table tbody tr:nth-child(even) {{ background: var(--bg-alt); }}
        .comparison-table .highlight {{
            color: var(--success);
            font-weight: 600;
        }}

        /* ===== FOOTER ===== */
        .footer {{
            background: var(--primary);
            color: rgba(255,255,255,0.7);
            padding: 48px 0 24px;
        }}
        .footer-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 40px;
            margin-bottom: 40px;
        }}
        .footer h4 {{
            color: #fff;
            font-size: 15px;
            margin-bottom: 16px;
        }}
        .footer p, .footer a {{
            font-size: 14px;
            color: rgba(255,255,255,0.6);
            text-decoration: none;
            line-height: 1.8;
        }}
        .footer a:hover {{ color: #fff; }}
        .footer ul {{ list-style: none; }}
        .footer ul li {{ margin-bottom: 8px; }}
        .footer-bottom {{
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 24px;
            font-size: 13px;
            text-align: center;
        }}

        /* ===== RESPONSIVE ===== */
        @media (max-width: 1024px) {{
            .hero-grid {{ grid-template-columns: 1fr; }}
            .hero-image {{ display: none; }}
            .product-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .advantage-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .industry-grid {{ grid-template-columns: repeat(3, 1fr); }}
            .process-grid {{ grid-template-columns: repeat(3, 1fr); }}
            .footer-grid {{ grid-template-columns: 1fr 1fr; }}
        }}

        @media (max-width: 768px) {{
            .header-nav {{ display: none; }}
            .header {{ padding: 12px 0; }}
            .header-logo {{ font-size: 17px; }}
            .hero {{ padding: 40px 0 36px; }}
            .hero h1 {{ font-size: 26px; line-height: 1.2; }}
            .hero h1 span {{ display: inline; }}
            .hero-content > p, .hero .intro-expand, .hero .intro-text {{ font-size: 15px; line-height: 1.7; word-wrap: break-word; overflow-wrap: break-word; }}
            .hero-cta-group {{ flex-direction: column; gap: 12px; }}
            .hero-cta-group a {{ width: 100%; text-align: center; justify-content: center; }}
            .btn-primary {{ padding: 14px 24px; font-size: 15px; }}
            .btn-secondary {{ padding: 12px 24px; font-size: 14px; }}
            .hero-stats {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 16px;
                padding-top: 20px;
            }}
            .hero-stat {{ text-align: center; }}
            .hero-stat .number {{ font-size: 26px; }}
            .hero-stat .label {{ font-size: 12px; }}
            .trust-badges {{
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                padding-bottom: 4px;
            }}
            .trust-badge {{
                font-size: 12px;
                padding: 8px 12px;
                white-space: nowrap;
            }}
            section {{ padding: 40px 0; }}
            .section-header {{ margin-bottom: 32px; }}
            .section-header h2 {{ font-size: 24px; line-height: 1.3; }}
            .section-header p {{ font-size: 14px; word-wrap: break-word; overflow-wrap: break-word; }}
            .container {{ padding: 0 16px; max-width: 100%; overflow-x: hidden; }}
            .tab-nav {{
                justify-content: flex-start;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                scrollbar-width: none;
                flex-wrap: nowrap;
                padding: 4px;
                gap: 2px;
            }}
            .tab-nav::-webkit-scrollbar {{ display: none; }}
            .tab-nav button {{
                padding: 10px 16px;
                font-size: 13px;
                white-space: nowrap;
                flex-shrink: 0;
            }}
            .tab-content h3 {{ font-size: 19px !important; margin-bottom: 8px !important; }}
            .tab-content > p {{ font-size: 14px !important; line-height: 1.7 !important; margin-bottom: 24px !important; }}
            .product-grid {{ grid-template-columns: 1fr; gap: 16px; }}
            .product-card-img {{ height: 140px; }}
            .product-card-img i {{ font-size: 48px; }}
            .product-card-body {{ padding: 16px; }}
            .product-card h3 {{ font-size: 16px; }}
            .product-card .card-desc {{ font-size: 13px; margin-bottom: 12px; }}
            .product-card .specs li {{ font-size: 12px; padding: 5px 0; }}
            .product-card .card-footer {{
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
            }}
            .card-footer-wrap {{
                width: 100%;
                flex-direction: row;
                align-items: center;
                gap: 12px;
            }}
            .btn-card {{
                padding: 10px 16px;
                font-size: 13px;
                flex-shrink: 0;
            }}
            .btn-inventory {{ font-size: 11px; }}
            .badge-popular {{
                font-size: 10px;
                padding: 3px 10px;
                top: 8px;
                right: 8px;
            }}
            .browse-all-link {{ font-size: 13px; margin-top: 12px; }}
            .comparison-table {{ display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }}
            .comparison-table thead th {{ padding: 12px 14px; font-size: 13px; white-space: nowrap; }}
            .comparison-table tbody td {{ padding: 10px 14px; font-size: 13px; min-width: 140px; }}
            .advantage-grid {{ grid-template-columns: 1fr; gap: 16px; }}
            .advantage-card {{ padding: 24px; }}
            .advantage-card h3 {{ font-size: 16px; }}
            .advantage-card p {{ font-size: 13px; }}
            .process-grid {{ grid-template-columns: repeat(2, 1fr); gap: 12px; }}
            .process-step {{ padding: 16px 12px; }}
            .process-step .step-number {{ width: 36px; height: 36px; font-size: 14px; margin-bottom: 12px; }}
            .process-step h4 {{ font-size: 13px; }}
            .process-step p {{ font-size: 12px; }}
            .cta-banner {{ padding: 40px 0; }}
            .cta-banner h2 {{ font-size: 24px; }}
            .cta-banner p {{ font-size: 14px; }}
            .cta-banner .btn-primary {{ width: 100%; text-align: center; justify-content: center; font-size: 15px; padding: 14px 24px; }}
            .industry-grid {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
            .industry-tag {{ padding: 12px; font-size: 12px; }}
            .industry-tag i {{ font-size: 20px; margin-bottom: 6px; }}
            .faq-tab-nav {{
                justify-content: flex-start;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                scrollbar-width: none;
                flex-wrap: nowrap;
                padding: 4px;
                gap: 2px;
            }}
            .faq-tab-nav::-webkit-scrollbar {{ display: none; }}
            .faq-tab-nav button {{
                padding: 8px 14px;
                font-size: 12px;
                white-space: nowrap;
                flex-shrink: 0;
            }}
            .faq-question {{ padding: 16px; font-size: 14px; }}
            .faq-answer {{ padding: 0 16px 16px; font-size: 13px; }}
            .footer-grid {{ grid-template-columns: 1fr; gap: 24px; }}
            .footer {{ padding: 36px 0 20px; }}
            .footer h4 {{ font-size: 14px; margin-bottom: 10px; }}
            .footer p, .footer a {{ font-size: 13px; }}
            .footer-bottom {{ font-size: 12px; }}
            .intro-expand summary p {{ font-size: 14px; }}
            .intro-rest {{ font-size: 14px; line-height: 1.7; }}
        }}

        img, video, iframe {{ max-width: 100%; height: auto; }}
        .tab-content > p, .section-header p {{ max-width: 100% !important; }}

        @media (max-width: 400px) {{
            .hero h1 {{ font-size: 22px; }}
            .hero-stat .number {{ font-size: 22px; }}
            .section-header h2 {{ font-size: 21px; }}
            .cta-banner h2 {{ font-size: 21px; }}
            .tab-nav button {{ padding: 8px 12px; font-size: 12px; }}
            .process-grid {{ grid-template-columns: 1fr; }}
            .industry-grid {{ grid-template-columns: 1fr 1fr; }}
        }}
    </style>
    <!-- ===== INTERNAL REVIEW OVERLAY ===== -->
    <style>
        .review-banner {{
            position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
            background: #d32f2f; color: #fff; padding: 10px 24px;
            font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 600;
            display: flex; align-items: center; justify-content: space-between;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3);
        }}
        .review-banner .legend {{ display: flex; gap: 16px; align-items: center; }}
        .review-banner .legend-item {{ display: flex; align-items: center; gap: 4px; font-size: 12px; }}
        .review-banner .dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}
        .review-banner .dot-ims {{ background: #4caf50; }}
        .review-banner .dot-homepage {{ background: #2196f3; }}
        .review-banner .dot-about {{ background: #ff9800; }}
        .review-banner .dot-category {{ background: #9c27b0; }}
        .review-banner .dot-product {{ background: #00bcd4; }}
        .review-banner .dot-general {{ background: #607d8b; }}
        .review-toggle {{ background: #fff; color: #d32f2f; border: none; padding: 6px 14px; border-radius: 4px; font-weight: 700; cursor: pointer; font-size: 12px; }}
        body {{ margin-top: 44px !important; }}
        .header {{ top: 44px !important; }}

        /* Source badges */
        .src {{
            position: relative;
            border-bottom: 2px dotted;
            cursor: help;
        }}
        .src-ims {{ border-color: #4caf50; background: rgba(76,175,80,0.08); }}
        .src-homepage {{ border-color: #2196f3; background: rgba(33,150,243,0.08); }}
        .src-about {{ border-color: #ff9800; background: rgba(255,152,0,0.08); }}
        .src-category {{ border-color: #9c27b0; background: rgba(156,39,176,0.08); }}
        .src-product {{ border-color: #00bcd4; background: rgba(0,188,212,0.08); }}
        .src-general {{ border-color: #607d8b; background: rgba(96,125,139,0.08); }}

        .src-tooltip {{
            display: none;
            position: fixed;
            background: #222;
            color: #fff;
            font-size: 13px;
            padding: 14px 18px;
            border-radius: 10px;
            max-width: 600px;
            width: max-content;
            z-index: 99999;
            line-height: 1.7;
            font-weight: 400;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
            pointer-events: auto;
            word-wrap: break-word;
        }}
        .src-tooltip a {{
            color: #4caf50;
            text-decoration: underline;
            font-weight: 600;
            display: inline-block;
            margin-top: 6px;
        }}
        .src-tooltip a:hover {{ color: #81c784; }}
        .src-tooltip .close-tip {{
            position: absolute;
            top: 4px;
            right: 8px;
            color: #999;
            cursor: pointer;
            font-size: 14px;
            font-weight: 700;
            line-height: 1;
        }}
        .src-tooltip .close-tip:hover {{ color: #fff; }}

        /* Source link icon */
        .src-link {{
            display: inline-block;
            width: 14px; height: 14px;
            background: currentColor;
            mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3'/%3E%3C/svg%3E") no-repeat center;
            -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3'/%3E%3C/svg%3E") no-repeat center;
            vertical-align: middle;
            margin-left: 2px;
            opacity: 0.7;
        }}
        .src-link:hover {{ opacity: 1; }}

        .sources-hidden .src {{ border-bottom: none !important; background: none !important; }}
        .sources-hidden .src::after {{ display: none !important; }}
        .sources-hidden .src-link {{ display: none !important; }}
        .sources-hidden .review-banner {{ opacity: 0.4; }}
    </style>
</head>
<body>

<!-- ===== INTERNAL REVIEW BANNER ===== -->
<div class="review-banner">
    <div><strong>INTERNAL REVIEW</strong> &mdash; Hover over highlighted text to see source. Click link icons to verify.</div>
    <div class="legend">
        <div class="legend-item"><span class="dot dot-product"></span> IMS Product Page</div>
        <div class="legend-item"><span class="dot dot-category"></span> IMS Category Page</div>
        <div class="legend-item"><span class="dot dot-homepage"></span> IPP Homepage</div>
        <div class="legend-item"><span class="dot dot-about"></span> IPP About Page</div>
        <div class="legend-item"><span class="dot dot-ims"></span> All Products Data</div>
        <div class="legend-item"><span class="dot dot-general"></span> Industry Standard</div>
    </div>
    <button class="review-toggle" onclick="document.body.classList.toggle('sources-hidden'); this.textContent = document.body.classList.contains('sources-hidden') ? 'Show Sources' : 'Hide Sources';">Hide Sources</button>
</div>

<!-- ===== HEADER ===== -->
<header class="header">
    <div class="container">
        <a href="/" class="header-logo">International <span>Process Plants</span></a>
        <nav class="header-nav">
            <a href="/buy-used/">Buy Used</a>
            <a href="/buy-new/">Buy New</a>
            <a href="/sell-to-ipp/">Sell to IPP</a>
            <a href="/equipment/">Equipment</a>
            <a href="/plants/">Plants</a>
            <a href="/about/">About IPP</a>
            <a href="/contact/" class="btn-quote">Ask an Expert</a>
        </nav>
    </div>
</header>

<!-- ===== HERO SECTION ===== -->
<section class="hero">
    <div class="container">
        <div class="hero-grid">
            <div class="hero-content">
                <h1>Buy Used {h(display_name)} <span>for Sale</span></h1>

                <p class="intro-text">{intro_text}</p>

                <details class="intro-expand">
                    <summary>
                        <p><span class="truncated">{h(truncated_preview)}</span> <span class="arrow-expand">&#10132;</span></p>
                    </summary>
                    <p class="intro-rest">{expand_text_first} {expand_text_rest} <span class="arrow-collapse" onclick="this.closest('details').removeAttribute('open')">&#11013;</span></p>
                </details>

                <div class="hero-cta-group">
                    <a href="/contact/" class="btn-primary"><i class="fas fa-envelope"></i> Request a Quote</a>
                    <a href="{h(ims_url)}" class="btn-secondary"><i class="fas fa-search"></i> Search Inventory</a>
                </div>

                <div class="hero-stats">
                    <div class="hero-stat src src-ims" data-src-label="IMS search returns {stats['count']} {display_name.lower()}. Rounded to {count_display}.">
                        <span class="number">{count_display}</span>
                        <span class="label">{h(display_name)}<br>in Stock</span>
                    </div>
                    <div class="hero-stat src src-homepage" data-src-label="IPP homepage: 'over 46 years of experience' (2026-46=1980). foundingDate=1980">
                        <span class="number">1980</span>
                        <span class="label">Established<br>Since</span>
                    </div>
                    <div class="hero-stat src src-about" data-src-label="IPP About page lists 15 countries: Brazil, Canada, China, Czech Republic, France, Germany, India, Italy, Mexico, Pakistan, Portugal, Romania, Turkey, UK, US">
                        <span class="number">15</span>
                        <span class="label">Countries<br>with Offices</span>
                    </div>
                </div>
            </div>

            <div class="hero-image" style="display: flex; flex-direction: column; gap: 16px;">{feature_cards}
            </div>
        </div>
    </div>
</section>

<!-- ===== PRODUCT TABS: BY MATERIAL ===== -->
<section id="equipment-by-material">
    <div class="container">
        <div class="section-header">
            <h2>Buy Used {h(display_name)} <span>by Material</span></h2>
            <p>{src("ims", f"Material field across all IMS product pages: {mat_text}", f"IPP stocks {display_name.lower()} in {mat_text} construction.")} Choose the material that matches your process chemistry and corrosion requirements.</p>
        </div>
{material_tabs_html}
    </div>
</section>
{condition_section}
{comparison_html}
{advantages_html}
{how_it_works_html}

<!-- ===== CTA BANNER ===== -->
<div class="cta-banner">
    <div class="container">
        <h2>Need {h(short_name)}? Ask an IPP Expert.</h2>
        <p>Tell us your capacity, material, pressure, and temperature requirements. Our team will match your specifications against current inventory and provide a detailed quote.</p>
        <a href="/contact/" class="btn-primary"><i class="fas fa-envelope"></i> Request a Quote</a>
    </div>
</div>
{industries_html}
{faq_html}

<!-- ===== FINAL CTA ===== -->
<div class="cta-banner">
    <div class="container">
        <h2>Ready to Buy {h(display_name)}?</h2>
        <p>IPP has supplied quality process equipment worldwide since 1980, serving 160,000+ customers. Tell us what you need &mdash; our team will respond with matched inventory and pricing.</p>
        <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
            <a href="/contact/" class="btn-primary"><i class="fas fa-comments"></i> Talk to an Engineer</a>
            <a href="{h(ims_url)}" class="btn-secondary" style="border-color: rgba(255,255,255,0.4);"><i class="fas fa-search"></i> Search Inventory</a>
        </div>
    </div>
</div>

<!-- ===== FOOTER ===== -->
<footer class="footer">
    <div class="container">
        <div class="footer-grid">
            <div>
                <h4>International Process Plants</h4>
                <p>Established in 1980. IPP is the world's largest inventory of new and used process plants and equipment, serving chemical, pharmaceutical, and industrial manufacturers worldwide. Nearly 150 colleagues across 15 countries. 160,000+ customers served.</p>
            </div>
            <div>
                <h4>Equipment</h4>
                <ul>
                    <li><a href="/buy-used/reactors/">Reactors</a></li>
                    <li><a href="/buy-used/heat-exchangers/">Heat Exchangers</a></li>
                    <li><a href="/buy-used/centrifuges/">Centrifuges</a></li>
                    <li><a href="/buy-used/dryers/">Dryers</a></li>
                    <li><a href="/buy-used/filters/">Filters</a></li>
                </ul>
            </div>
            <div>
                <h4>Company</h4>
                <ul>
                    <li><a href="/about/">About IPP</a></li>
                    <li><a href="/sell-to-ipp/">Sell to IPP</a></li>
                    <li><a href="/plants/">Complete Plants</a></li>
                    <li><a href="/careers/">Careers</a></li>
                    <li><a href="/contact/">Contact</a></li>
                </ul>
            </div>
            <div>
                <h4>Contact</h4>
                <ul>
                    <li><a href="tel:+16095868004">USA: +1 609-586-8004</a></li>
                    <li><a href="tel:+441642367910">UK: +44-1642-367910</a></li>
                </ul>
                <br>
                <h4>Subsidiaries</h4>
                <ul>
                    <li><a href="#">Gale Process Solutions</a></li>
                    <li><a href="#">Universal Glasteel Equipment</a></li>
                    <li><a href="#">Universal Turbomachinery Equipment</a></li>
                    <li><a href="#">Universal Vortex Inc</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            &copy; 2026 International Process Plants. All rights reserved.
        </div>
    </div>
</footer>

<script>
// Tab functionality
document.querySelectorAll('.tab-nav').forEach(nav => {{
    nav.querySelectorAll('button').forEach(btn => {{
        btn.addEventListener('click', () => {{
            const tabId = btn.dataset.tab;
            const section = nav.closest('section');

            nav.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            section.querySelectorAll('.tab-content').forEach(content => {{
                content.classList.remove('active');
            }});
            section.querySelector(`#${{tabId}}`).classList.add('active');
        }});
    }});
}});

// FAQ tab functionality
document.querySelectorAll('.faq-tab-nav').forEach(nav => {{
    nav.querySelectorAll('button').forEach(btn => {{
        btn.addEventListener('click', () => {{
            const tabId = btn.dataset.faqtab;

            nav.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            document.querySelectorAll('.faq-tab-content').forEach(content => {{
                content.classList.remove('active');
                content.style.display = 'none';
            }});
            const target = document.getElementById(tabId);
            target.classList.add('active');
            target.style.display = 'block';
        }});
    }});
}});

// FAQ accordion
document.querySelectorAll('.faq-question').forEach(question => {{
    question.addEventListener('click', () => {{
        const item = question.closest('.faq-item');
        const wasOpen = item.classList.contains('open');

        // Close all in same tab
        item.closest('.faq-tab-content').querySelectorAll('.faq-item').forEach(i => {{
            i.classList.remove('open');
        }});

        if (!wasOpen) item.classList.add('open');
    }});
}});

// Initialize FAQ tabs display
document.querySelectorAll('.faq-tab-content').forEach((content, index) => {{
    content.style.display = index === 0 ? 'block' : 'none';
}});

// === SOURCE ANNOTATION TOOLTIPS ===
const globalTip = document.createElement('div');
globalTip.className = 'src-tooltip';
globalTip.style.display = 'none';
document.body.appendChild(globalTip);

let activeSrc = null;

function closeTooltip() {{
    globalTip.style.display = 'none';
    if (activeSrc) activeSrc.classList.remove('active');
    activeSrc = null;
}}

function openTooltip(el) {{
    const label = el.getAttribute('data-src-label');
    const linkEl = el.nextElementSibling?.classList?.contains('src-link') ? el.nextElementSibling :
                   el.parentElement?.querySelector('.src-link');
    const href = linkEl ? linkEl.getAttribute('href') : null;

    let html = '<span class="close-tip">&times;</span>' + label;
    if (href) {{
        html += '<br><a href="' + href + '" target="_blank">Verify source &rarr;</a>';
    }}
    globalTip.innerHTML = html;

    const rect = el.getBoundingClientRect();
    let top = rect.top - 12;
    let left = rect.left;

    globalTip.style.display = 'block';
    globalTip.style.left = '0px';
    globalTip.style.top = '0px';
    const tipRect = globalTip.getBoundingClientRect();

    top = rect.top - tipRect.height - 12;
    if (top < 60) top = rect.bottom + 12;
    if (left + tipRect.width > window.innerWidth - 20) left = window.innerWidth - tipRect.width - 20;
    if (left < 10) left = 10;

    globalTip.style.left = left + 'px';
    globalTip.style.top = top + 'px';

    if (activeSrc && activeSrc !== el) activeSrc.classList.remove('active');
    el.classList.add('active');
    activeSrc = el;

    globalTip.querySelector('.close-tip').onclick = (e) => {{
        e.stopPropagation();
        closeTooltip();
    }};
}}

document.querySelectorAll('.src[data-src-label]').forEach(el => {{
    el.addEventListener('click', (e) => {{
        e.preventDefault();
        if (activeSrc === el) {{
            closeTooltip();
        }} else {{
            openTooltip(el);
        }}
    }});
}});

document.addEventListener('mousedown', (e) => {{
    if (!activeSrc) return;
    if (globalTip.contains(e.target)) return;
    if (activeSrc.contains(e.target)) return;
    closeTooltip();
}});

window.addEventListener('scroll', closeTooltip, {{ passive: true }});

document.querySelectorAll('.src-link').forEach(el => el.style.display = 'none');
</script>

</body>
</html>"""

    return html


# ============================================================
# MAIN
# ============================================================

def process_category(cat, dry_run=False):
    """Process a single category and generate its landing page."""
    data_folder, lp_folder, display_name, url_path, ims_url, query = cat

    # Load data
    data_path = os.path.join(DATA_DIR, data_folder, "all_products.json")
    cat_page_path = os.path.join(DATA_DIR, data_folder, "category-page.html")
    cat_desc_path = os.path.join(DATA_DIR, data_folder, "category-description.md")

    if not os.path.exists(data_path):
        print(f"  SKIP: No all_products.json found at {data_path}")
        return False

    with open(data_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    if not products:
        print(f"  SKIP: Empty product list for {display_name}")
        return False

    cat_page_data = parse_category_page(cat_page_path)
    cat_desc_url = get_category_description_url(cat_desc_path)

    # Analyze
    stats = analyze_products(products)
    print(f"  Products: {stats['count']}, Materials: {len(stats['materials'])}, Manufacturers: {len(stats['manufacturers'])}")

    if dry_run:
        print(f"  DRY RUN: Would generate page for {display_name}")
        return True

    # Generate HTML
    html = generate_full_page(cat, products, stats, cat_page_data, cat_desc_url)

    # Write to file
    slug = slug_from_name(display_name)
    output_dir = os.path.join(PROJECT_ROOT, url_path.strip("/"))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"INTERNAL-REVIEW-{slug}.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  OUTPUT: {output_path}")
    print(f"  SIZE: {len(html):,} bytes, {html.count(chr(10)):,} lines")
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate IPP landing pages from scraped data")
    parser.add_argument("--category", type=str, help="Generate only this category (data folder name, e.g. 'tank')")
    parser.add_argument("--dry-run", action="store_true", help="Analyze data but don't write files")
    args = parser.parse_args()

    print("=" * 70)
    print("IPP Landing Page Generator")
    print("=" * 70)
    print(f"Data directory: {DATA_DIR}")
    print(f"Output directory: {LANDING_DIR}")
    print(f"Categories: {len(CATEGORIES)}")
    print()

    success = 0
    failed = 0

    for cat in CATEGORIES:
        data_folder = cat[0]
        display_name = cat[2]

        if args.category and args.category not in (data_folder, display_name):
            continue

        print(f"[{data_folder}] {display_name}")
        try:
            if process_category(cat, dry_run=args.dry_run):
                success += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
        print()

    print("=" * 70)
    print(f"DONE: {success} generated, {failed} failed/skipped")
    print("=" * 70)


if __name__ == "__main__":
    main()
