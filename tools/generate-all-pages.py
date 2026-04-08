#!/usr/bin/env python3
"""
Generate INTERNAL-REVIEW HTML landing pages for all 37 IPP equipment categories.

For each category:
1. Reads all_products.json to analyze data and make semantic SEO tab decisions
2. Reads category-description.md for IMS category description content
3. Generates a complete HTML landing page with proper source citations

Usage: python3 generate-all-pages.py
"""

import json
import os
import re
import html as html_module
from collections import Counter
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LANDING_DIR = BASE_DIR / "landing-pages"

CATEGORIES = [
    # (data_folder, landing_folder, display_name, url_path, ims_category_url, primary_query, equipment_type_short)
    ("tank", "tank", "Tanks", "/equipment/tank/", "https://ims.internationalprocessplants.com/inventory/equipment/tank", "used tanks for sale", "tank"),
    ("dryer/porcupine-dryer", "dryer/porcupine-dryer", "Porcupine Dryers", "/equipment/dryer/porcupine-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/porcupine-dryer", "used porcupine dryer for sale", "porcupine dryer"),
    ("dryer/rotary-steam-tube-dryer", "dryer/rotary-steam-tube-dryer", "Rotary Steam Tube Dryers", "/equipment/dryer/rotary-steam-tube-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/rotary-steam-tube-dryer", "used rotary steam tube dryer for sale", "rotary steam tube dryer"),
    ("dryer/rotary-vacuum-dryer", "dryer/rotary-vacuum-dryer", "Rotary Vacuum Dryers", "/equipment/dryer/rotary-vacuum-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/rotary-vacuum-dryer", "used rotary vacuum dryer for sale", "rotary vacuum dryer"),
    ("dryer/spray-dryer", "dryer/spray-dryer", "Spray Dryers", "/equipment/dryer/spray-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/spray-dryer", "used spray dryer for sale", "spray dryer"),
    ("dryer/holoflite-and-screw-dryer", "dryer/holoflite-and-screw-dryer", "Holoflite &amp; Screw Dryers", "/equipment/dryer/holoflite-and-screw-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/holoflite-and-screw-dryer", "used holoflite dryer for sale", "holoflite and screw dryer"),
    ("dryer/fluid-bed-dryer", "dryer/fluid-bed-dryer", "Fluid Bed Dryers", "/equipment/dryer/fluid-bed-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/fluid-bed-dryer", "used fluid bed dryer for sale", "fluid bed dryer"),
    ("dryer/ribbon-and-paddle-dryer", "dryer/ribbon-and-paddle-dryer", "Ribbon &amp; Paddle Dryers", "/equipment/dryer/ribbon-and-paddle-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/ribbon-and-paddle-dryer", "used ribbon and paddle dryer for sale", "ribbon and paddle dryer"),
    ("dryer/twin-shell-and-double-cone-dryer", "dryer/twin-shell-and-double-cone-dryer", "Twin Shell &amp; Double Cone Dryers", "/equipment/dryer/twin-shell-and-double-cone-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/twin-shell-and-double-cone-dryer", "used twin shell and double cone dryer for sale", "twin shell and double cone dryer"),
    ("dryer/wyssmont-dryer", "dryer/wyssmont-dryer", "Wyssmont Dryers", "/equipment/dryer/wyssmont-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/wyssmont-dryer", "used Wyssmont dryer for sale", "Wyssmont dryer"),
    ("dryer/freeze-dryer", "dryer/freeze-dryer", "Freeze Dryers", "/equipment/dryer/freeze-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/freeze-dryer", "used freeze dryer for sale", "freeze dryer"),
    ("dryer/horizontal-belt-continuous-dryer", "dryer/horizontal-belt-continuous-dryer", "Horizontal Belt &amp; Continuous Dryers", "/equipment/dryer/horizontal-belt-continuous-dryer/", "https://ims.internationalprocessplants.com/inventory/equipment/horizontal-belt-continuous-dryer", "used horizontal belt continuous dryer for sale", "horizontal belt and continuous dryer"),
    ("centrifuge/auto-discharge-bottom", "centrifuge/auto-discharge-bottom", "Auto Discharge-Bottom Basket Centrifuges", "/equipment/centrifuge/auto-discharge-bottom/", "https://ims.internationalprocessplants.com/inventory/equipment/basket-centrifuge/auto-discharge-bottom", "used auto discharge bottom centrifuge for sale", "auto discharge bottom basket centrifuge"),
    ("centrifuge/manual-discharge-top", "centrifuge/manual-discharge-top", "Manual Discharge-Top Basket Centrifuges", "/equipment/centrifuge/manual-discharge-top/", "https://ims.internationalprocessplants.com/inventory/equipment/basket-centrifuge/manual-discharge-top", "used manual discharge top centrifuge for sale", "manual discharge top basket centrifuge"),
    ("centrifuge/basket-centrifuge-parts", "centrifuge/basket-centrifuge-parts", "Basket Centrifuge Parts", "/equipment/centrifuge/basket-centrifuge-parts/", "https://ims.internationalprocessplants.com/inventory/equipment/basket-centrifuge/parts-only", "basket centrifuge parts for sale", "basket centrifuge parts"),
    ("centrifuge/disc-bowl-centrifuge", "centrifuge/disc-bowl-centrifuge", "Disc Bowl Centrifuges", "/equipment/centrifuge/disc-bowl-centrifuge/", "https://ims.internationalprocessplants.com/inventory/equipment/disc-bowl-centrifuge", "used disc bowl centrifuge for sale", "disc bowl centrifuge"),
    ("centrifuge/inverting-filter-centrifuge", "centrifuge/inverting-filter-centrifuge", "Inverting Filter Centrifuges", "/equipment/centrifuge/inverting-filter-centrifuge/", "https://ims.internationalprocessplants.com/inventory/equipment/inverting-filter-centrifuge", "used inverting filter centrifuge for sale", "inverting filter centrifuge"),
    ("centrifuge/solid-bowl-decanter-centrifuge", "centrifuge/solid-bowl-decanter-centrifuge", "Solid Bowl-Decanter Centrifuges", "/equipment/centrifuge/solid-bowl-decanter-centrifuge/", "https://ims.internationalprocessplants.com/inventory/equipment/solid-bowl-decanter-centrifuge", "used solid bowl decanter centrifuge for sale", "solid bowl decanter centrifuge"),
    ("filter/rosenmund-and-cogiem", "filter/rosenmund-and-cogiem", "Rosenmund and Cogiem Filters", "/equipment/filter/rosenmund-and-cogiem/", "https://ims.internationalprocessplants.com/inventory/equipment/filter/rosenmund-and-cogiem", "used Rosenmund filter for sale", "Rosenmund and Cogiem filter"),
    ("filter/pressure-leaf", "filter/pressure-leaf", "Pressure Leaf Filters", "/equipment/filter/pressure-leaf/", "https://ims.internationalprocessplants.com/inventory/equipment/filter/pressure-leaf", "used pressure leaf filter for sale", "pressure leaf filter"),
    ("filter/nutsche", "filter/nutsche", "Nutsche Filters", "/equipment/filter/nutsche/", "https://ims.internationalprocessplants.com/inventory/equipment/filter/nutsche", "used nutsche filter for sale", "nutsche filter"),
    ("heat-exchanger/shell-and-tube", "heat-exchanger/shell-and-tube", "Shell and Tube Heat Exchangers", "/equipment/heat-exchanger/shell-and-tube/", "https://ims.internationalprocessplants.com/inventory/equipment/heat-exchanger/shell-and-tube", "used shell and tube heat exchanger for sale", "shell and tube heat exchanger"),
    ("mixer/muller-mixer", "mixer/muller-mixer", "Muller Mixers", "/equipment/mixer/muller-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/muller-mixer", "used muller mixer for sale", "muller mixer"),
    ("mixer/nauta-mixer", "mixer/nauta-mixer", "Nauta Mixers", "/equipment/mixer/nauta-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/nauta-mixer", "used Nauta mixer for sale", "Nauta mixer"),
    ("mixer/intensive-mixer", "mixer/intensive-mixer", "Intensive Mixers", "/equipment/mixer/intensive-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/intensive-mixer", "used intensive mixer for sale", "intensive mixer"),
    ("mixer/twin-shell-and-double-cone-mixer", "mixer/twin-shell-and-double-cone-mixer", "Twin Shell &amp; Double Cone Mixers", "/equipment/mixer/twin-shell-and-double-cone-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/twin-shell-and-double-cone-mixer", "used twin shell and double cone mixer for sale", "twin shell and double cone mixer"),
    ("mixer/ribbon-paddle-mixer", "mixer/ribbon-paddle-mixer", "Ribbon &amp; Paddle Mixers", "/equipment/mixer/ribbon-paddle-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/ribbon-paddle-mixer", "used ribbon paddle mixer for sale", "ribbon and paddle mixer"),
    ("mixer/double-arm-mixer", "mixer/double-arm-mixer", "Double Arm Mixers", "/equipment/mixer/double-arm-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/double-arm-mixer", "used double arm mixer for sale", "double arm mixer"),
    ("mixer/continuous-mixer", "mixer/continuous-mixer", "Continuous Mixers", "/equipment/mixer/continuous-mixer/", "https://ims.internationalprocessplants.com/inventory/equipment/continuous-mixer", "used continuous mixer for sale", "continuous mixer"),
    ("glass-lined-parts/agitator", "glass-lined-parts/agitator", "Glass Lined Agitators", "/equipment/glass-lined-parts/agitator/", "https://ims.internationalprocessplants.com/inventory/equipment/glass-lined-parts/agitator", "used glass lined agitator for sale", "glass lined agitator"),
    ("glass-lined-parts/baffle", "glass-lined-parts/baffle", "Glass Lined Baffles", "/equipment/glass-lined-parts/baffle/", "https://ims.internationalprocessplants.com/inventory/equipment/glass-lined-parts/baffle", "used glass lined baffle for sale", "glass lined baffle"),
    ("glass-lined-parts/cryo-lock-blades", "glass-lined-parts/cryo-lock-blades", "Glass Lined Cryo-Lock Blades", "/equipment/glass-lined-parts/cryo-lock-blades/", "https://ims.internationalprocessplants.com/inventory/equipment/glass-lined-parts/cryo-lock-blades", "used glass lined cryo lock blades for sale", "glass lined cryo-lock blade"),
    ("glass-lined-parts/pro-ring", "glass-lined-parts/pro-ring", "Glass Lined Pro-Ring", "/equipment/glass-lined-parts/pro-ring/", "https://ims.internationalprocessplants.com/inventory/equipment/glass-lined-parts/pro-ring", "used glass lined Pro-Ring for sale", "glass lined Pro-Ring"),
    ("evaporator/crystalizer-evaporator", "evaporator/crystalizer-evaporator", "Crystalizer/Evaporator", "/equipment/evaporator/crystalizer-evaporator/", "https://ims.internationalprocessplants.com/inventory/equipment/evaporator/crystalizer-evaporator", "used crystallizer evaporator for sale", "crystalizer evaporator"),
    ("evaporator/flash", "evaporator/flash", "Flash Evaporators", "/equipment/evaporator/flash/", "https://ims.internationalprocessplants.com/inventory/equipment/evaporator/flash", "used flash evaporator for sale", "flash evaporator"),
    ("evaporator/rising-falling-film", "evaporator/rising-falling-film", "Rising/Falling Film Evaporators", "/equipment/evaporator/rising-falling-film/", "https://ims.internationalprocessplants.com/inventory/equipment/evaporator/rising-falling-film", "used rising falling film evaporator for sale", "rising falling film evaporator"),
    ("evaporator/wiped-thin-film", "evaporator/wiped-thin-film", "Wiped/Thin Film Evaporators", "/equipment/evaporator/wiped-thin-film/", "https://ims.internationalprocessplants.com/inventory/equipment/evaporator/wiped-thin-film", "used wiped thin film evaporator for sale", "wiped thin film evaporator"),
]

# Cross-sell mapping: equipment type -> related types
CROSS_SELL_MAP = {
    "tank": [("Reactors", "/equipment/reactor/", "fas fa-flask"), ("Heat Exchangers", "/equipment/heat-exchanger/shell-and-tube/", "fas fa-temperature-half"), ("Mixers", "/equipment/mixer/", "fas fa-blender")],
    "dryer": [("Filters", "/equipment/filter/", "fas fa-filter"), ("Centrifuges", "/equipment/centrifuge/", "fas fa-circle-notch"), ("Heat Exchangers", "/equipment/heat-exchanger/shell-and-tube/", "fas fa-temperature-half")],
    "centrifuge": [("Filters", "/equipment/filter/", "fas fa-filter"), ("Dryers", "/equipment/dryer/", "fas fa-fan"), ("Reactors", "/equipment/reactor/", "fas fa-flask")],
    "filter": [("Centrifuges", "/equipment/centrifuge/", "fas fa-circle-notch"), ("Dryers", "/equipment/dryer/", "fas fa-fan"), ("Reactors", "/equipment/reactor/", "fas fa-flask")],
    "heat-exchanger": [("Reactors", "/equipment/reactor/", "fas fa-flask"), ("Evaporators", "/equipment/evaporator/", "fas fa-droplet"), ("Tanks", "/equipment/tank/", "fas fa-database")],
    "mixer": [("Reactors", "/equipment/reactor/", "fas fa-flask"), ("Tanks", "/equipment/tank/", "fas fa-database"), ("Dryers", "/equipment/dryer/", "fas fa-fan")],
    "glass-lined-parts": [("Reactors", "/equipment/reactor/", "fas fa-flask"), ("Glass Lined Agitators", "/equipment/glass-lined-parts/agitator/", "fas fa-gears"), ("Glass Lined Baffles", "/equipment/glass-lined-parts/baffle/", "fas fa-grip-lines")],
    "evaporator": [("Heat Exchangers", "/equipment/heat-exchanger/shell-and-tube/", "fas fa-temperature-half"), ("Reactors", "/equipment/reactor/", "fas fa-flask"), ("Tanks", "/equipment/tank/", "fas fa-database")],
}

# Industry icons map
INDUSTRY_ICONS = {
    "Pharmaceutical": "fas fa-pills",
    "Chemical Processing": "fas fa-flask",
    "Biotechnology": "fas fa-dna",
    "Food & Beverage": "fas fa-wheat-awn",
    "Cosmetics": "fas fa-pump-soap",
    "Fine Chemicals": "fas fa-vial",
    "Agrochemicals": "fas fa-seedling",
    "Polymers & Resins": "fas fa-link",
    "Paints & Coatings": "fas fa-droplet",
    "Petrochemicals": "fas fa-oil-well",
    "Mining & Minerals": "fas fa-mountain",
    "Water Treatment": "fas fa-water",
    "Dairy": "fas fa-cow",
    "Power Generation": "fas fa-bolt",
    "Pulp & Paper": "fas fa-scroll",
    "Environmental": "fas fa-leaf",
    "Oil & Gas": "fas fa-gas-pump",
    "Wastewater": "fas fa-faucet-drip",
}

# Default industries by equipment type
DEFAULT_INDUSTRIES = {
    "tank": ["Pharmaceutical", "Chemical Processing", "Food & Beverage", "Biotechnology", "Petrochemicals", "Water Treatment", "Cosmetics", "Paints & Coatings"],
    "dryer": ["Pharmaceutical", "Chemical Processing", "Food & Beverage", "Biotechnology", "Agrochemicals", "Fine Chemicals", "Mining & Minerals", "Cosmetics"],
    "centrifuge": ["Pharmaceutical", "Chemical Processing", "Biotechnology", "Food & Beverage", "Environmental", "Oil & Gas", "Wastewater", "Fine Chemicals"],
    "filter": ["Pharmaceutical", "Chemical Processing", "Biotechnology", "Food & Beverage", "Fine Chemicals", "Cosmetics", "Petrochemicals", "Environmental"],
    "heat-exchanger": ["Chemical Processing", "Petrochemicals", "Pharmaceutical", "Food & Beverage", "Power Generation", "Oil & Gas", "Biotechnology", "Pulp & Paper"],
    "mixer": ["Pharmaceutical", "Chemical Processing", "Food & Beverage", "Cosmetics", "Paints & Coatings", "Polymers & Resins", "Biotechnology", "Agrochemicals"],
    "glass-lined-parts": ["Pharmaceutical", "Chemical Processing", "Fine Chemicals", "Biotechnology", "Agrochemicals", "Cosmetics"],
    "evaporator": ["Chemical Processing", "Pharmaceutical", "Food & Beverage", "Dairy", "Petrochemicals", "Environmental", "Biotechnology", "Pulp & Paper"],
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def esc(text):
    """HTML-escape text."""
    return html_module.escape(str(text))

def get_equipment_type(data_folder):
    """Get the top-level equipment type from folder path."""
    return data_folder.split("/")[0]

def is_glass_lined_part(data_folder):
    """Check if this is a glass-lined parts category."""
    return data_folder.startswith("glass-lined-parts/")

def get_slug(landing_folder):
    """Derive file slug from landing folder."""
    parts = landing_folder.split("/")
    return parts[-1]

def load_products(data_folder):
    """Load all_products.json for a category."""
    path = DATA_DIR / data_folder / "all_products.json"
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return []

def load_category_description(data_folder):
    """Load category-description.md and extract meaningful text."""
    path = DATA_DIR / data_folder / "category-description.md"
    try:
        with open(path) as f:
            text = f.read()
    except Exception:
        return ""

    # Extract text after the navigation junk
    # Look for the meaningful description paragraphs
    lines = text.split("\n")
    useful_lines = []
    skip_patterns = ["BUY USED", "BUY NEW", "SELL TO IPP", "SEARCH PLANTS", "SEARCH EQUIPMENT",
                     "ABOUT US", "FAQ & MORE", "CONTACT", "Quote", "clear all", "Cancel", "Request Quote",
                     "Other Equipment", "Search for more", "---", "**Source URL:**", "## Full Page Text",
                     "Featured", "New Glasslined", "Type:", "Subtype:", "Manufacturer:", "Model:",
                     "Condition:", "Material:", "Capacity (Design):", "Internal Pressure:", "Quote Cart",
                     "cancel", "IPP#", "Stock Number:", "Request a Quote", "Call Us"]

    in_content = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Skip nav/header/product listing junk
        skip = False
        for pat in skip_patterns:
            if stripped.startswith(pat) or stripped == pat:
                skip = True
                break
        if skip:
            continue
        # Look for descriptive sentences (more than 40 chars, contains common words)
        if len(stripped) > 40 and any(w in stripped.lower() for w in ["used", "surplus", "inventory", "equipment", "industrial", "process", "ipP", "ipp", "application", "manufactur", "pharma", "chemical", "available"]):
            useful_lines.append(stripped)

    return " ".join(useful_lines[:5])  # First 5 useful sentences


def parse_numeric(value_str):
    """Extract numeric value from a string like '3,000 L (790 gallons)' or '1.01 bar (14.7 psi)'."""
    if not value_str:
        return None
    # Remove commas and get first number
    cleaned = value_str.replace(",", "")
    match = re.search(r'([\d.]+)', cleaned)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None


def analyze_products(products):
    """Analyze products to determine tab strategy and extract key data."""
    if not products:
        return {
            "count": 0,
            "tab_strategy": "none",
            "tab_groups": {},
            "materials": Counter(),
            "conditions": Counter(),
            "manufacturers": Counter(),
            "capacity_range": None,
            "pressure_range": None,
            "temp_range": None,
            "representative_products": [],
        }

    materials = Counter()
    conditions = Counter()
    manufacturers = Counter()
    capacities = []
    pressures = []
    temps = []

    for p in products:
        attrs = p.get("attributes", {})
        mat = attrs.get("Material", "")
        cond = attrs.get("Condition", "")
        mfr = attrs.get("Manufacturer", "")

        if mat:
            materials[mat] += 1
        if cond:
            conditions[cond] += 1
        if mfr:
            manufacturers[mfr] += 1

        # Parse capacity
        cap_str = attrs.get("Capacity (Design)", "") or attrs.get("Volume", "") or attrs.get("Bowl Volume", "")
        cap_val = parse_numeric(cap_str)
        if cap_val is not None and cap_val > 0:
            capacities.append((cap_val, cap_str, p))

        # Parse pressure
        press_str = attrs.get("Internal Pressure", "") or attrs.get("Pressure", "")
        press_val = parse_numeric(press_str)
        if press_val is not None and press_val > 0:
            pressures.append((press_val, press_str, p))

        # Parse temperature
        temp_str = attrs.get("Internal Temperature", "") or attrs.get("Temperature", "")
        temp_val = parse_numeric(temp_str)
        if temp_val is not None:
            temps.append((temp_val, temp_str, p))

    count = len(products)

    # Determine tab strategy
    total_with_material = sum(materials.values())
    dominant_material_pct = (materials.most_common(1)[0][1] / total_with_material * 100) if total_with_material > 0 and materials else 0

    if count < 5:
        tab_strategy = "none"
        tab_groups = {}
    elif dominant_material_pct > 80:
        # Use CONDITION tabs
        tab_strategy = "condition"
        tab_groups = {}
        for p in products:
            cond = p.get("attributes", {}).get("Condition", "Unknown")
            # Normalize condition
            cond_key = normalize_condition(cond)
            if cond_key not in tab_groups:
                tab_groups[cond_key] = []
            tab_groups[cond_key].append(p)
    else:
        # Use MATERIAL tabs
        tab_strategy = "material"
        tab_groups = {}
        for p in products:
            mat = p.get("attributes", {}).get("Material", "Other")
            mat_key = normalize_material(mat)
            if mat_key not in tab_groups:
                tab_groups[mat_key] = []
            tab_groups[mat_key].append(p)

    # Sort and limit tab groups - keep top 3-4 groups
    if tab_groups:
        sorted_groups = sorted(tab_groups.items(), key=lambda x: -len(x[1]))
        # If many small groups, merge into "Other"
        if len(sorted_groups) > 4:
            main_groups = dict(sorted_groups[:3])
            other = []
            for _, prods in sorted_groups[3:]:
                other.extend(prods)
            if other:
                main_groups["Other"] = other
            tab_groups = main_groups
        else:
            tab_groups = dict(sorted_groups)

    # Build result
    result = {
        "count": count,
        "tab_strategy": tab_strategy,
        "tab_groups": tab_groups,
        "materials": materials,
        "conditions": conditions,
        "manufacturers": manufacturers,
        "capacity_range": (min(capacities, key=lambda x: x[0]), max(capacities, key=lambda x: x[0])) if capacities else None,
        "pressure_range": (min(pressures, key=lambda x: x[0]), max(pressures, key=lambda x: x[0])) if pressures else None,
        "temp_range": (min(temps, key=lambda x: x[0]), max(temps, key=lambda x: x[0])) if temps else None,
    }

    # Select representative products (highest attribute_count, diverse manufacturers)
    sorted_by_attrs = sorted(products, key=lambda x: -x.get("attribute_count", 0))
    seen_mfrs = set()
    reps = []
    for p in sorted_by_attrs:
        mfr = p.get("attributes", {}).get("Manufacturer", "")
        if mfr not in seen_mfrs or len(reps) < 2:
            reps.append(p)
            seen_mfrs.add(mfr)
            if len(reps) >= 3:
                break
    result["representative_products"] = reps

    return result


def normalize_condition(cond):
    """Normalize condition strings into tab-friendly groups."""
    cond_lower = cond.lower().strip()
    if "re-glass" in cond_lower or "reglass" in cond_lower:
        if "needs" in cond_lower:
            return "Needs Reglass"
        return "Re-Glassed"
    elif "new" in cond_lower:
        return "New"
    elif "unused" in cond_lower:
        return "Unused"
    elif "refurbished" in cond_lower or "rebuilt" in cond_lower:
        return "Refurbished"
    elif "used" in cond_lower:
        return "Used"
    else:
        return cond if cond else "Other"


def normalize_material(mat):
    """Normalize material strings into tab-friendly groups."""
    mat_lower = mat.lower().strip()
    if "glass" in mat_lower:
        return "Glass-Lined"
    elif "hastelloy" in mat_lower:
        return "Hastelloy"
    elif "titanium" in mat_lower:
        return "Titanium"
    elif "stainless" in mat_lower or mat_lower.startswith("ss "):
        return "Stainless Steel"
    elif "carbon" in mat_lower:
        return "Carbon Steel"
    elif "alloy" in mat_lower or "nickel" in mat_lower or "inconel" in mat_lower or "monel" in mat_lower:
        return "Specialty Alloys"
    else:
        return mat if mat else "Other"


def select_tab_products(products, n=2):
    """Select n representative products from a tab group, favoring high attribute count and diverse manufacturers."""
    if not products:
        return []
    sorted_prods = sorted(products, key=lambda x: -x.get("attribute_count", 0))
    seen_mfrs = set()
    selected = []
    for p in sorted_prods:
        mfr = p.get("attributes", {}).get("Manufacturer", "")
        if mfr not in seen_mfrs or len(selected) < 1:
            selected.append(p)
            seen_mfrs.add(mfr)
            if len(selected) >= n:
                break
    # Fill remaining if needed
    if len(selected) < n:
        for p in sorted_prods:
            if p not in selected:
                selected.append(p)
                if len(selected) >= n:
                    break
    return selected


def format_product_count(count):
    """Format product count for display (e.g., 700+ for 714)."""
    if count >= 1000:
        return f"{(count // 100) * 100}+"
    elif count >= 100:
        return f"{(count // 10) * 10}+"
    elif count >= 10:
        return f"{count}"
    else:
        return str(count)


def get_top_manufacturers(manufacturers, n=5):
    """Get top n manufacturers."""
    return [m for m, _ in manufacturers.most_common(n)]


def build_product_specs(product):
    """Build a list of spec strings for a product card."""
    attrs = product.get("attributes", {})
    stock = product.get("stock_number", "")
    specs = []

    # Capacity
    cap = attrs.get("Capacity (Design)", "") or attrs.get("Volume", "") or attrs.get("Bowl Volume", "")
    if cap:
        specs.append(("Capacity (Design)", f"{cap}", stock))

    # Pressure/temp
    pressure = attrs.get("Internal Pressure", "") or attrs.get("Pressure", "")
    temp = attrs.get("Internal Temperature", "") or attrs.get("Temperature", "")
    if pressure and temp:
        specs.append(("Internal Pressure + Internal Temperature", f"{pressure}, {temp}", stock))
    elif pressure:
        specs.append(("Internal Pressure", f"{pressure}", stock))
    elif temp:
        specs.append(("Internal Temperature", f"{temp}", stock))

    # Material
    mat = attrs.get("Material", "")
    if mat:
        specs.append(("Material", f"{mat}", stock))

    # Condition
    cond = attrs.get("Condition", "")
    if cond:
        specs.append(("Condition", f"{cond} condition", stock))

    # Manufacturer / Model
    mfr = attrs.get("Manufacturer", "")
    model = attrs.get("Model", "")
    if mfr and model:
        specs.append(("Manufacturer + Model", f"{mfr} {model}", stock))

    # Dimensions or other notable specs
    diameter = attrs.get("Diameter", "")
    length = attrs.get("Straight-side Length", "") or attrs.get("Length", "") or attrs.get("Height", "")
    if diameter and length:
        specs.append(("Diameter + Length", f"{diameter} x {length}", stock))
    elif diameter:
        specs.append(("Diameter", f"{diameter}", stock))

    # Motor
    motor = attrs.get("Motor Power", "") or attrs.get("Motor Horsepower", "")
    if motor:
        specs.append(("Motor Power", f"{motor}", stock))

    return specs[:5]  # Max 5 specs per card


def get_breadcrumb_parent(data_folder, display_name):
    """Get breadcrumb parent category."""
    eq_type = get_equipment_type(data_folder)
    type_names = {
        "tank": "Tanks",
        "dryer": "Dryers",
        "centrifuge": "Centrifuges",
        "filter": "Filters",
        "heat-exchanger": "Heat Exchangers",
        "mixer": "Mixers",
        "glass-lined-parts": "Glass Lined Parts",
        "evaporator": "Evaporators",
    }
    return type_names.get(eq_type, eq_type.replace("-", " ").title())


def get_tab_icon(tab_name):
    """Get Font Awesome icon for a tab."""
    name_lower = tab_name.lower()
    if "glass" in name_lower:
        return "fas fa-shield-halved"
    elif "stainless" in name_lower:
        return "fas fa-gears"
    elif "hastelloy" in name_lower or "alloy" in name_lower or "titanium" in name_lower:
        return "fas fa-flask-vial"
    elif "carbon" in name_lower:
        return "fas fa-cube"
    elif "used" in name_lower:
        return "fas fa-tools"
    elif "re-glass" in name_lower or "reglass" in name_lower:
        return "fas fa-shield-halved"
    elif "new" in name_lower:
        return "fas fa-box-open"
    elif "unused" in name_lower:
        return "fas fa-box"
    elif "refurbish" in name_lower:
        return "fas fa-wrench"
    elif "needs" in name_lower:
        return "fas fa-exclamation-triangle"
    else:
        return "fas fa-industry"


def make_safe_id(text):
    """Make a safe HTML id from text."""
    return re.sub(r'[^a-z0-9-]', '-', text.lower().strip()).strip('-')


# ============================================================
# HTML GENERATION
# ============================================================

def generate_page(cat_tuple):
    """Generate the full HTML page for one category."""
    data_folder, landing_folder, display_name, url_path, ims_url, primary_query, eq_short = cat_tuple

    # Unescape display_name for plain text usage
    display_name_plain = display_name.replace("&amp;", "&")

    products = load_products(data_folder)
    analysis = analyze_products(products)
    cat_desc = load_category_description(data_folder)

    eq_type = get_equipment_type(data_folder)
    is_parts = is_glass_lined_part(data_folder)
    item_word = "parts" if is_parts else "equipment"
    slug = get_slug(landing_folder)

    # Determine what noun to use
    noun_singular = eq_short
    noun_plural = display_name_plain

    # Top manufacturers
    top_mfrs = get_top_manufacturers(analysis["manufacturers"], 5)
    top_mfrs_str = ", ".join(top_mfrs[:3]) if top_mfrs else "various manufacturers"
    all_mfrs_str = ", ".join(top_mfrs) if top_mfrs else "various manufacturers"

    # Materials list
    top_materials = [m for m, _ in analysis["materials"].most_common(5)]
    materials_str = ", ".join(top_materials[:4]) if top_materials else ""

    # Conditions list
    top_conditions = [c for c, _ in analysis["conditions"].most_common(5)]
    conditions_str = ", ".join(top_conditions[:4]) if top_conditions else ""

    # Capacity range
    cap_range_str = ""
    if analysis["capacity_range"]:
        cap_min = analysis["capacity_range"][0][1]
        cap_max = analysis["capacity_range"][1][1]
        cap_range_str = f"{cap_min} to {cap_max}"

    # Pressure range
    press_range_str = ""
    if analysis["pressure_range"]:
        press_min = analysis["pressure_range"][0][1]
        press_max = analysis["pressure_range"][1][1]
        press_range_str = f"{press_min} to {press_max}"

    # Product count display
    count_display = format_product_count(analysis["count"])

    # Breadcrumb parent
    bc_parent = get_breadcrumb_parent(data_folder, display_name_plain)

    # Industries
    industries = DEFAULT_INDUSTRIES.get(eq_type, DEFAULT_INDUSTRIES["tank"])[:10]

    # Cross-sell
    cross_sell = CROSS_SELL_MAP.get(eq_type, CROSS_SELL_MAP["tank"])

    # Base URL
    base_url = f"https://internationalprocessplants.com{url_path}"

    # ---- BUILD HTML ----
    html_parts = []

    # HEAD
    meta_desc = f"Buy used {display_name_plain.lower()} for sale from IPP."
    if top_mfrs:
        meta_desc += f" {top_mfrs_str} & more manufacturers."
    if materials_str:
        meta_desc += f" {materials_str}."
    if cap_range_str:
        meta_desc += f" {cap_range_str}."
    meta_desc += " Ships worldwide."
    # Truncate meta desc to ~160 chars
    if len(meta_desc) > 165:
        meta_desc = meta_desc[:162] + "..."

    html_parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[INTERNAL REVIEW] Buy Used {esc(display_name_plain)} for Sale</title>
    <meta name="description" content="{esc(meta_desc)}">
    <meta name="robots" content="noindex, nofollow">
    <link rel="canonical" href="{esc(base_url)}">

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebPage",
      "@id": "{esc(base_url)}#webpage",
      "url": "{esc(base_url)}",
      "name": "Buy Used {esc(display_name_plain)} for Sale | IPP",
      "description": "{esc(meta_desc)}",
      "inLanguage": "en-US",
      "about": {{
        "@type": "Organization",
        "@id": "https://internationalprocessplants.com/#organization",
        "name": "International Process Plants",
        "alternateName": "IPP",
        "url": "https://internationalprocessplants.com",
        "foundingDate": "1980",
        "description": "Global supplier of new and used process plants and equipment for chemical, pharmaceutical, and industrial applications.",
        "address": [
          {{ "@type": "PostalAddress", "addressCountry": "US", "addressLocality": "South Carolina" }},
          {{ "@type": "PostalAddress", "addressCountry": "DE", "addressLocality": "Germany" }},
          {{ "@type": "PostalAddress", "addressCountry": "GB", "addressLocality": "United Kingdom" }}
        ],
        "numberOfEmployees": {{ "@type": "QuantitativeValue", "value": "150" }},
        "areaServed": "Worldwide"
      }},
      "mainEntity": {{
        "@type": "Product",
        "name": "Used {esc(display_name_plain)}",
        "description": "Used {esc(display_name_plain.lower())} from {esc(all_mfrs_str)} and other manufacturers.{(' ' + esc(materials_str) + ' construction.') if materials_str else ''}{(' Capacities from ' + esc(cap_range_str) + '.') if cap_range_str else ''}",
        "brand": {{ "@type": "Brand", "name": "International Process Plants" }},
        "category": "Process Equipment",
        {('"material": [' + ", ".join('"' + esc(m) + '"' for m in top_materials[:5]) + '],') if top_materials else ''}
        "offers": {{
          "@type": "AggregateOffer",
          "priceCurrency": "USD",
          "availability": "https://schema.org/InStock",
          "offerCount": "{analysis['count']}",
          "description": "Quote-based pricing. Used {esc(display_name_plain.lower())} available at significant savings compared to new equipment."
        }}
      }},
      "hasPart": {{
        "@type": "FAQPage",
        "@id": "{esc(base_url)}#faq",
        "mainEntity": [
          {{
            "@type": "Question",
            "name": "How many {esc(display_name_plain.lower())} does IPP have in stock?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "IPP stocks {esc(display_name_plain.lower())} from {esc(all_mfrs_str)} and other manufacturers.{(' Capacities range from ' + esc(cap_range_str) + '.') if cap_range_str else ''}{(' Available in ' + esc(materials_str) + ' construction.') if materials_str else ''}"
            }}
          }},
          {{
            "@type": "Question",
            "name": "How much can I save buying used {esc(display_name_plain.lower())} versus new?",
            "acceptedAnswer": {{
              "@type": "Answer",
              "text": "Buying used {esc(display_name_plain.lower())} from IPP can save up to 50% of capital and 90% of lead time versus buying new. Exact savings depend on manufacturer, capacity, and condition. Contact IPP for pricing on specific units."
            }}
          }}
        ]
      }},
      "breadcrumb": {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://internationalprocessplants.com/" }},
          {{ "@type": "ListItem", "position": 2, "name": "Equipment", "item": "https://internationalprocessplants.com/equipment/" }},
          {{ "@type": "ListItem", "position": 3, "name": "{esc(bc_parent)}", "item": "https://internationalprocessplants.com/equipment/{eq_type}/" }},
          {{ "@type": "ListItem", "position": 4, "name": "Used {esc(display_name_plain)} for Sale" }}
        ]
      }}
    }}
    </script>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
""")

    # CSS - exact copy from template
    html_parts.append(get_css_block())

    # Close head, open body
    html_parts.append("""</head>
<body>
""")

    # REVIEW BANNER
    html_parts.append(get_review_banner())

    # HEADER
    html_parts.append(get_header())

    # ---- HERO SECTION ----
    html_parts.append(generate_hero(cat_tuple, analysis, cat_desc))

    # ---- MAIN CONTENT ----
    if analysis["count"] == 0:
        # Zero products - coming soon
        html_parts.append(generate_coming_soon(cat_tuple, cat_desc))
    elif analysis["count"] < 5:
        # Few products - no tabs, show all
        html_parts.append(generate_all_products_section(cat_tuple, analysis, products))
    else:
        # Product tabs
        html_parts.append(generate_product_tabs(cat_tuple, analysis))

    # CTA BANNER (mid-page)
    html_parts.append(f"""
<!-- ===== CTA BANNER ===== -->
<div class="cta-banner">
    <div class="container">
        <h2>Ready to Buy a Used {esc(display_name_plain.rstrip('s'))}?</h2>
        <p>Tell us your specifications and requirements. Our team will match your needs against current {esc(display_name_plain.lower())} inventory and provide a detailed quote.</p>
        <a href="/contact/" class="btn-primary"><i class="fas fa-envelope"></i> Request a Quote</a>
    </div>
</div>
""")

    # COMPARISON TABLE (only if we have products)
    if analysis["count"] > 0:
        html_parts.append(generate_comparison_table(cat_tuple, analysis))

    # ADVANTAGES
    html_parts.append(generate_advantages(cat_tuple, analysis, is_parts))

    # HOW IT WORKS (skip for parts)
    if not is_parts:
        html_parts.append(generate_how_it_works(cat_tuple))

    # INDUSTRIES
    html_parts.append(generate_industries(cat_tuple, industries))

    # FAQ
    html_parts.append(generate_faq(cat_tuple, analysis))

    # CROSS-SELL
    html_parts.append(generate_cross_sell(cat_tuple, cross_sell))

    # FINAL CTA
    html_parts.append(f"""
<!-- ===== FINAL CTA ===== -->
<div class="cta-banner">
    <div class="container">
        <h2>Ready to Buy {esc(display_name_plain)}?</h2>
        <p>IPP has supplied quality process equipment worldwide since 1980, serving 160,000+ customers. Tell us what you need &mdash; our team will respond with matched inventory and pricing.</p>
        <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
            <a href="/contact/" class="btn-primary"><i class="fas fa-comments"></i> Talk to an Engineer</a>
            <a href="{esc(ims_url)}" class="btn-secondary" style="border-color: rgba(255,255,255,0.4);"><i class="fas fa-search"></i> Search Inventory</a>
        </div>
    </div>
</div>
""")

    # FOOTER
    html_parts.append(get_footer())

    # JAVASCRIPT
    html_parts.append(get_js_block())

    html_parts.append("""
</body>
</html>""")

    return "".join(html_parts)


def generate_hero(cat_tuple, analysis, cat_desc):
    """Generate the hero section."""
    data_folder, landing_folder, display_name, url_path, ims_url, primary_query, eq_short = cat_tuple
    display_name_plain = display_name.replace("&amp;", "&")

    top_mfrs = get_top_manufacturers(analysis["manufacturers"], 5)
    top_mfrs_str = ", ".join(top_mfrs[:3]) if top_mfrs else "leading manufacturers"

    top_materials = [m for m, _ in analysis["materials"].most_common(5)]
    materials_str = ", ".join(top_materials[:4]) if top_materials else ""

    cap_range_str = ""
    if analysis["capacity_range"]:
        cap_range_str = f"{analysis['capacity_range'][0][1]} to {analysis['capacity_range'][1][1]}"

    press_range_str = ""
    if analysis["pressure_range"]:
        press_range_str = f"{analysis['pressure_range'][0][1]} to {analysis['pressure_range'][1][1]}"

    count_display = format_product_count(analysis["count"])

    # Intro text using category description
    intro_text = f'Buying used {display_name_plain.lower()} through International Process Plants gives '
    intro_text += f'<span class="src src-category" data-src-label="IMS category page for {esc(display_name_plain)}">'
    intro_text += f'chemical, pharmaceutical, and industrial manufacturers</span> access to '
    if top_mfrs:
        intro_text += f'<span class="src src-ims" data-src-label="Manufacturer field across {analysis["count"]} IMS product pages">{esc(top_mfrs_str)} and other OEM manufacturers</span>'
    else:
        intro_text += f'OEM manufacturers'
    intro_text += f'<a href="{esc(ims_url)}" target="_blank" class="src-link"></a>.'

    # Expandable details
    expand_parts = []
    if materials_str:
        expand_parts.append(f'<span class="src src-ims" data-src-label="Material field across {analysis["count"]} IMS product pages">Materials of construction include {esc(materials_str)}.</span>')
    if cap_range_str:
        expand_parts.append(f'<span class="src src-ims" data-src-label="Capacity field across IMS product pages">Capacities range from {esc(cap_range_str)}.</span>')
    if press_range_str:
        expand_parts.append(f'<span class="src src-ims" data-src-label="Internal Pressure field across IMS product pages">Pressure ratings range from {esc(press_range_str)}.</span>')

    conditions = [c for c, _ in analysis["conditions"].most_common(5)]
    if conditions:
        expand_parts.append(f'<span class="src src-ims" data-src-label="Condition field across IMS product pages">Available in {esc(", ".join(conditions))} conditions.</span>')

    expand_parts.append(f'<span class="src src-homepage" data-src-label="IPP homepage exact quote for used equipment systems savings">Buying used {esc(display_name_plain.lower())} from IPP can save up to 50% of capital and 90% of lead time versus buying new.</span><a href="https://internationalprocessplants.com" target="_blank" class="src-link"></a>')

    expand_text = " ".join(expand_parts)

    # Truncated preview
    truncated = expand_parts[0] if expand_parts else ""
    # Strip src spans for truncated display
    trunc_plain = re.sub(r'<[^>]+>', '', truncated)
    if len(trunc_plain) > 80:
        trunc_plain = trunc_plain[:80] + "..."

    # Hero feature cards (link to representative products)
    feature_cards = ""
    reps = analysis["representative_products"]
    if reps:
        cards = []
        for i, p in enumerate(reps[:3]):
            attrs = p.get("attributes", {})
            mfr = attrs.get("Manufacturer", "Unknown")
            mat = attrs.get("Material", "")
            url = p.get("url", ims_url)
            label = f"{mfr} {mat}" if mat else mfr
            sublabel = attrs.get("Condition", "")
            icon = "fas fa-industry"
            if "glass" in mat.lower():
                icon = "fas fa-shield-halved"
            elif "stainless" in mat.lower():
                icon = "fas fa-gears"
            elif "hastelloy" in mat.lower():
                icon = "fas fa-flask-vial"
            cards.append(f"""
                <a href="{esc(url)}" target="_blank" style="display: flex; align-items: center; gap: 16px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 14px; padding: 20px 24px; text-decoration: none; transition: all 0.3s; color: #fff;" onmouseover="this.style.background='rgba(26,143,196,0.15)';this.style.borderColor='var(--accent)'" onmouseout="this.style.background='rgba(255,255,255,0.08)';this.style.borderColor='rgba(255,255,255,0.15)'">
                    <i class="{icon}" style="font-size: 36px; color: var(--accent); width: 48px; text-align: center;"></i>
                    <div>
                        <div style="font-size: 17px; font-weight: 700;">{esc(label)}</div>
                        <div style="font-size: 13px; color: rgba(255,255,255,0.6);">{esc(sublabel)}</div>
                    </div>
                    <i class="fas fa-arrow-right" style="margin-left: auto; color: var(--accent); font-size: 14px;"></i>
                </a>""")
        feature_cards = "\n".join(cards)
    else:
        # No products - show category link
        feature_cards = f"""
                <a href="{esc(ims_url)}" target="_blank" style="display: flex; align-items: center; gap: 16px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 14px; padding: 20px 24px; text-decoration: none; transition: all 0.3s; color: #fff;" onmouseover="this.style.background='rgba(26,143,196,0.15)';this.style.borderColor='var(--accent)'" onmouseout="this.style.background='rgba(255,255,255,0.08)';this.style.borderColor='rgba(255,255,255,0.15)'">
                    <i class="fas fa-search" style="font-size: 36px; color: var(--accent); width: 48px; text-align: center;"></i>
                    <div>
                        <div style="font-size: 17px; font-weight: 700;">Browse {esc(display_name_plain)} Inventory</div>
                        <div style="font-size: 13px; color: rgba(255,255,255,0.6);">View all available units on IMS</div>
                    </div>
                    <i class="fas fa-arrow-right" style="margin-left: auto; color: var(--accent); font-size: 14px;"></i>
                </a>"""

    noun_label = "Parts" if is_glass_lined_part(data_folder) else display_name_plain.split()[-1]

    return f"""
<!-- ===== HERO SECTION ===== -->
<section class="hero">
    <div class="container">
        <div class="hero-grid">
            <div class="hero-content">
                <h1>Buy Used {display_name} <span>for Sale</span></h1>

                <p class="intro-text">{intro_text}</p>

                <details class="intro-expand">
                    <summary>
                        <p><span class="truncated">{esc(trunc_plain)}</span> <span class="arrow-expand">&#10132;</span></p>
                    </summary>
                    <p class="intro-rest">{expand_text} <span class="arrow-collapse" onclick="this.closest('details').removeAttribute('open')">&#11013;</span></p>
                </details>

                <div class="hero-cta-group">
                    <a href="/contact/" class="btn-primary"><i class="fas fa-envelope"></i> Request a Quote</a>
                    <a href="{esc(ims_url)}" class="btn-secondary"><i class="fas fa-search"></i> Search Inventory</a>
                </div>

                <div class="hero-stats">
                    <div class="hero-stat src src-ims" data-src-label="IMS search returns {analysis['count']} {esc(display_name_plain.lower())}">
                        <span class="number">{count_display}</span>
                        <span class="label">{esc(noun_label)}<br>in Stock</span>
                    </div>
                    <div class="hero-stat src src-homepage" data-src-label="IPP homepage: foundingDate=1980">
                        <span class="number">1980</span>
                        <span class="label">Established<br>Since</span>
                    </div>
                    <div class="hero-stat src src-about" data-src-label="IPP About page lists 15 countries">
                        <span class="number">15</span>
                        <span class="label">Countries<br>with Offices</span>
                    </div>
                </div>
            </div>

            <div class="hero-image" style="display: flex; flex-direction: column; gap: 16px;">
{feature_cards}
            </div>
        </div>
    </div>
</section>
"""


def generate_product_tabs(cat_tuple, analysis):
    """Generate product tabs section based on tab strategy."""
    data_folder, landing_folder, display_name, url_path, ims_url, primary_query, eq_short = cat_tuple
    display_name_plain = display_name.replace("&amp;", "&")

    tab_strategy = analysis["tab_strategy"]
    tab_groups = analysis["tab_groups"]

    if not tab_groups:
        return ""

    section_id = f"{get_slug(landing_folder)}-by-{tab_strategy}"
    section_label = "Material" if tab_strategy == "material" else "Condition"

    html = f"""
<!-- ===== PRODUCT TABS: BY {section_label.upper()} ===== -->
<section id="{make_safe_id(section_id)}">
    <div class="container">
        <div class="section-header">
            <h2>Buy Used {display_name} <span>by {esc(section_label)}</span></h2>
            <p><span class="src src-ims" data-src-label="{esc(section_label)} field across {analysis['count']} IMS product pages">IPP stocks {esc(display_name_plain.lower())} across multiple {esc(section_label.lower())} options.</span> Choose the {esc(section_label.lower())} that matches your process requirements.</p>
        </div>

        <div class="tab-nav" id="{make_safe_id(section_label)}Tabs">
"""

    first = True
    for tab_name, tab_products in tab_groups.items():
        active = ' class="active"' if first else ''
        tab_id = make_safe_id(f"tab-{tab_name}")
        icon = get_tab_icon(tab_name)
        count = len(tab_products)
        html += f'            <button{active} data-tab="{tab_id}"><i class="{icon}"></i> {esc(tab_name)} ({count})</button>\n'
        first = False

    html += '        </div>\n\n'

    # Tab contents
    first = True
    for tab_name, tab_products in tab_groups.items():
        active_class = ' active' if first else ''
        tab_id = make_safe_id(f"tab-{tab_name}")
        selected = select_tab_products(tab_products, 2)

        html += f"""        <!-- {esc(tab_name)} Tab -->
        <div class="tab-content{active_class}" id="{tab_id}">
            <h3 style="font-size: 22px; font-weight: 700; color: var(--primary); margin-bottom: 12px;">Buy Used {esc(tab_name)} {esc(display_name_plain)} for Sale</h3>
            <p style="color: var(--text-light); margin-bottom: 32px; max-width: 800px; line-height: 1.8;"><span class="src src-ims" data-src-label="{esc(section_label)} field on IMS products">IPP stocks {len(tab_products)} {esc(tab_name.lower())} {esc(display_name_plain.lower())}.</span> Available from {esc(", ".join(get_top_manufacturers(Counter(p.get('attributes', dict()).get('Manufacturer', '') for p in tab_products), 3)))} and other manufacturers.</p>

            <div class="product-grid">
"""
        for i, p in enumerate(selected):
            html += generate_product_card(p, i == 0, tab_name)

        html += f"""            </div>
            <a href="{esc(ims_url)}" class="browse-all-link" target="_blank"><i class="fas fa-search"></i> Browse All {esc(tab_name)} {esc(display_name_plain)} in Stock</a>
        </div>

"""
        first = False

    html += """    </div>
</section>
"""
    return html


def generate_product_card(product, featured=False, badge_text=""):
    """Generate HTML for a single product card."""
    attrs = product.get("attributes", {})
    stock = product.get("stock_number", "")
    url = product.get("url", "")

    mfr = attrs.get("Manufacturer", "Unknown")
    mat = attrs.get("Material", "")
    cap = attrs.get("Capacity (Design)", "") or attrs.get("Volume", "") or attrs.get("Bowl Volume", "")
    cond = attrs.get("Condition", "")

    # Card title
    title_parts = [mfr]
    if mat:
        title_parts.append(mat)
    if cap:
        # Get just the metric part
        cap_short = cap.split("(")[0].strip() if "(" in cap else cap
        title_parts.append(f"&mdash; {cap_short}")
    title = " ".join(title_parts)
    if len(title) > 60:
        title = f"{mfr} {mat}" if mat else mfr
        if cap:
            cap_short = cap.split("(")[0].strip() if "(" in cap else cap
            title += f" &mdash; {cap_short}"

    # Description
    desc = f'{cond} {mfr} {mat} {attrs.get("Type", "").lower()}'.strip()
    if cap:
        desc += f'. {cap} capacity'
    desc += '.'

    # Icon
    icon = "fas fa-industry"
    if mat:
        mat_lower = mat.lower()
        if "glass" in mat_lower:
            icon = "fas fa-shield-halved"
        elif "stainless" in mat_lower:
            icon = "fas fa-gears"
        elif "hastelloy" in mat_lower:
            icon = "fas fa-flask-vial"

    # Specs
    specs = build_product_specs(product)

    badge_html = ""
    if featured and badge_text:
        badge_html = f'                    <div class="badge-popular">{esc(badge_text)}</div>\n'

    specs_html = ""
    for spec_label, spec_val, spec_stock in specs:
        specs_html += f'                            <li class="src src-product" data-src-label="{esc(spec_label)} field: detail/{esc(spec_stock)}"><i class="fas fa-check"></i> {esc(spec_val)}</li>\n'

    return f"""                <div class="product-card">
{badge_html}                    <div class="product-card-img"><i class="{icon}"></i></div>
                    <div class="product-card-body">
                        <h3>{title}</h3>
                        <p class="card-desc"><span class="src src-product" data-src-label="All specs from IMS product page: {esc(url)}">{esc(desc)}</span><a href="{esc(url)}" target="_blank" class="src-link"></a></p>
                        <ul class="specs">
{specs_html}                        </ul>
                        <div class="card-footer">
                            <div class="card-footer-wrap">
                                <a href="/contact/" class="btn-card">Request Specs <i class="fas fa-arrow-right"></i></a>
                                <a href="{esc(url)}" class="btn-inventory" target="_blank">View IPP# {esc(stock)} <i class="fas fa-external-link-alt"></i></a>
                            </div>
                        </div>
                    </div>
                </div>

"""


def generate_all_products_section(cat_tuple, analysis, products):
    """Generate a section showing all products (for small inventories < 5)."""
    data_folder, landing_folder, display_name, url_path, ims_url, primary_query, eq_short = cat_tuple
    display_name_plain = display_name.replace("&amp;", "&")

    html = f"""
<!-- ===== ALL PRODUCTS ===== -->
<section id="all-products">
    <div class="container">
        <div class="section-header">
            <h2>Available <span>{display_name}</span> in Stock</h2>
            <p><span class="src src-ims" data-src-label="IMS product pages for {esc(display_name_plain)}">IPP currently stocks {analysis['count']} {esc(display_name_plain.lower())}.</span></p>
        </div>

        <div class="product-grid">
"""
    for i, p in enumerate(products):
        html += generate_product_card(p, i == 0, "In Stock")

    html += f"""        </div>
        <a href="{esc(ims_url)}" class="browse-all-link" target="_blank"><i class="fas fa-search"></i> Browse All {esc(display_name_plain)} on IMS</a>
    </div>
</section>
"""
    return html


def generate_coming_soon(cat_tuple, cat_desc):
    """Generate a minimal page for categories with 0 products."""
    data_folder, landing_folder, display_name, url_path, ims_url, primary_query, eq_short = cat_tuple
    display_name_plain = display_name.replace("&amp;", "&")

    desc_html = ""
    if cat_desc:
        desc_html = f'<p style="color: var(--text-light); line-height: 1.8; margin-bottom: 24px;"><span class="src src-category" data-src-label="IMS category page for {esc(display_name_plain)}">{esc(cat_desc)}</span><a href="{esc(ims_url)}" target="_blank" class="src-link"></a></p>'

    return f"""
<!-- ===== COMING SOON ===== -->
<section>
    <div class="container">
        <div class="section-header">
            <h2>{display_name} <span>Coming Soon</span></h2>
            <p>IPP is building inventory for this equipment category. Contact us to discuss your requirements &mdash; we may have units available that are not yet listed.</p>
        </div>
        {desc_html}
        <div style="text-align: center; padding: 40px; background: var(--bg-alt); border-radius: 14px; border: 1px solid var(--border);">
            <i class="fas fa-clock" style="font-size: 48px; color: var(--accent); margin-bottom: 16px; display: block;"></i>
            <h3 style="font-size: 20px; font-weight: 700; margin-bottom: 12px; color: var(--primary);">No {esc(display_name_plain)} Currently Listed</h3>
            <p style="color: var(--text-light); max-width: 500px; margin: 0 auto 24px;">IPP acquires new inventory regularly. Contact our team to discuss your {esc(display_name_plain.lower())} requirements and we will source equipment to match your specifications.</p>
            <a href="/contact/" class="btn-primary"><i class="fas fa-envelope"></i> Contact IPP About {esc(display_name_plain)}</a>
        </div>
    </div>
</section>
"""


def generate_comparison_table(cat_tuple, analysis):
    """Generate the comparison table section."""
    data_folder, landing_folder, display_name, url_path, ims_url, primary_query, eq_short = cat_tuple
    display_name_plain = display_name.replace("&amp;", "&")

    cap_range_str = ""
    if analysis["capacity_range"]:
        cap_range_str = f'{analysis["capacity_range"][0][1]} to {analysis["capacity_range"][1][1]}'

    press_range_str = ""
    if analysis["pressure_range"]:
        press_range_str = f'{analysis["pressure_range"][0][1]} to {analysis["pressure_range"][1][1]}'

    top_materials = [m for m, _ in analysis["materials"].most_common(4)]
    materials_str = ", ".join(top_materials) if top_materials else "Various"

    return f"""
<!-- ===== COMPARISON TABLE: USED vs NEW ===== -->
<section id="comparison">
    <div class="container">
        <div class="section-header">
            <h2>Buying Used {display_name} vs <span>Buying New</span></h2>
            <p><span class="src src-homepage" data-src-label="IPP homepage exact quote for used equipment systems savings">Buying used {esc(display_name_plain.lower())} from IPP can save up to 50% of capital and 90% of lead time versus buying new.</span><a href="https://internationalprocessplants.com" target="_blank" class="src-link"></a> Here is how used and new {esc(display_name_plain.lower())} compare across key factors.</p>
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
                    <td class="highlight"><span class="src src-homepage" data-src-label="IPP homepage: used equipment saves '50 percent of capital versus new'">Significant savings vs new OEM price</span></td>
                    <td>Full OEM list price</td>
                </tr>
                <tr>
                    <td><strong>Delivery Timeline</strong></td>
                    <td class="highlight"><span class="src src-category" data-src-label="IMS category page: used {esc(display_name_plain.lower())} in stock and ready to ship">In-stock units ready to ship</span></td>
                    <td>Extended lead times (new fabrication)</td>
                </tr>
                {f'''<tr>
                    <td><strong>Available Capacities</strong></td>
                    <td><span class="src src-ims" data-src-label="Capacity field across IMS product pages">{esc(cap_range_str)} (multiple units in stock)</span></td>
                    <td>Custom-built to specification</td>
                </tr>''' if cap_range_str else ''}
                {f'''<tr>
                    <td><strong>Materials</strong></td>
                    <td><span class="src src-ims" data-src-label="Material field across IMS product pages">{esc(materials_str)}</span></td>
                    <td>Custom-specified</td>
                </tr>''' if top_materials else ''}
                {f'''<tr>
                    <td><strong>Pressure Ratings</strong></td>
                    <td><span class="src src-ims" data-src-label="Internal Pressure field across IMS product pages">{esc(press_range_str)}</span></td>
                    <td>Custom-engineered to specification</td>
                </tr>''' if press_range_str else ''}
                <tr>
                    <td><strong>Manufacturers</strong></td>
                    <td><span class="src src-ims" data-src-label="Manufacturer field across IMS product pages">{esc(", ".join(get_top_manufacturers(analysis["manufacturers"], 3)))} and others</span></td>
                    <td>Single OEM</td>
                </tr>
                <tr>
                    <td><strong>Environmental Impact</strong></td>
                    <td class="highlight"><span class="src src-general" data-src-label="Industry standard knowledge about equipment reuse">Extends equipment lifecycle, reduces waste</span></td>
                    <td>New raw material consumption</td>
                </tr>
            </tbody>
        </table>
    </div>
</section>
"""


def generate_advantages(cat_tuple, analysis, is_parts=False):
    """Generate the advantages section."""
    data_folder, landing_folder, display_name, url_path, ims_url, primary_query, eq_short = cat_tuple
    display_name_plain = display_name.replace("&amp;", "&")

    top_mfrs = get_top_manufacturers(analysis["manufacturers"], 4)
    top_mfrs_str = ", ".join(top_mfrs) if top_mfrs else "leading manufacturers"

    top_materials = [m for m, _ in analysis["materials"].most_common(4)]
    materials_str = ", ".join(top_materials) if top_materials else ""

    cap_range_str = ""
    if analysis["capacity_range"]:
        cap_range_str = f'{analysis["capacity_range"][0][1]} to {analysis["capacity_range"][1][1]}'

    # Adjust language for parts vs equipment
    if is_parts:
        card6_title = "Full Range of Parts"
        card6_text = f'<span class="src src-ims" data-src-label="Attribute fields across IMS product pages">{esc(display_name_plain)} are available in multiple sizes, configurations, and conditions from IPP inventory.</span>'
        card4_title = "Quality Assured"
        card4_text = f'<span class="src src-about" data-src-label="IPP About page: UGE glass-lined equipment subsidiary">IPP offers {esc(display_name_plain.lower())} through its UGE (Universal Glasteel Equipment) division, which stocks 700+ vessels and 2,700+ parts.</span><a href="https://internationalprocessplants.com/about/" target="_blank" class="src-link"></a>'
    else:
        card6_title = "Full Range of Materials &amp; Specs"
        if materials_str and cap_range_str:
            card6_text = f'<span class="src src-ims" data-src-label="All specs from attribute fields across {analysis["count"]} IMS product pages">Materials include {esc(materials_str)}. Capacities from {esc(cap_range_str)}.</span>'
        else:
            card6_text = f'<span class="src src-ims" data-src-label="Attribute fields across IMS product pages">IPP stocks {esc(display_name_plain.lower())} across a wide range of specifications to match your process requirements.</span>'
        card4_title = "Quality &amp; Refurbishment"
        card4_text = f'<span class="src src-about" data-src-label="IPP About page: UGE glass-lined equipment subsidiary">IPP offers refurbishment services through its UGE (Universal Glasteel Equipment) division, founded in 1995, which stocks 700+ vessels and 2,700+ parts.</span><a href="https://internationalprocessplants.com/about/" target="_blank" class="src-link"></a>'

    return f"""
<!-- ===== ADVANTAGES ===== -->
<section id="advantages">
    <div class="container">
        <div class="section-header">
            <h2>Advantages of Buying <span>Used {display_name}</span> from IPP</h2>
            <p><span class="src src-homepage" data-src-label="IPP homepage: 'over 46 years of experience'">International Process Plants combines over 46 years of process equipment expertise</span>, <span class="src src-homepage" data-src-label="IPP homepage: 'nearly 150 colleagues around the world'">nearly 150 colleagues</span> across <span class="src src-about" data-src-label="IPP About page lists 15 countries by name">15 countries</span>, and an inventory of <span class="src src-homepage" data-src-label="IPP homepage: '15,000 process systems and major equipment pieces'">15,000 process systems and major equipment pieces</span> to deliver {esc(display_name_plain.lower())} ready for your process.</p>
        </div>

        <div class="advantage-grid">
            <div class="advantage-card">
                <div class="advantage-icon"><i class="fas fa-piggy-bank"></i></div>
                <h3>Significant Cost Savings</h3>
                <p><span class="src src-homepage" data-src-label="IPP homepage exact quote for used equipment systems">Buying used {esc(display_name_plain.lower())} from IPP can save up to 50% of capital and 90% of lead time versus buying new.</span><a href="https://internationalprocessplants.com" target="_blank" class="src-link"></a></p>
                <a href="/contact/" class="card-link">Request a Quote <i class="fas fa-arrow-right"></i></a>
            </div>
            <div class="advantage-card">
                <div class="advantage-icon"><i class="fas fa-truck-fast"></i></div>
                <h3>Immediate Availability</h3>
                <p>In-stock {esc(display_name_plain.lower())} from IPP are ready to ship. <span class="src src-about" data-src-label="IPP About page: GPS '12-16 week average delivery'">IPP's GPS subsidiary also provides custom fabricated new equipment with 12&ndash;16 week average delivery.</span><a href="https://internationalprocessplants.com/about/" target="_blank" class="src-link"></a></p>
                <a href="/contact/" class="card-link">Check Availability <i class="fas fa-arrow-right"></i></a>
            </div>
            <div class="advantage-card">
                <div class="advantage-icon"><i class="fas fa-industry"></i></div>
                <h3>Multiple OEM Manufacturers</h3>
                <p><span class="src src-ims" data-src-label="Manufacturer field across IMS product pages">IPP stocks {esc(display_name_plain.lower())} from {esc(top_mfrs_str)} and other manufacturers.</span> Every unit is an original OEM product with traceable provenance.</p>
                <a href="/contact/" class="card-link">Browse Manufacturers <i class="fas fa-arrow-right"></i></a>
            </div>
            <div class="advantage-card">
                <div class="advantage-icon"><i class="fas fa-shield-halved"></i></div>
                <h3>{card4_title}</h3>
                <p>{card4_text}</p>
                <a href="/contact/" class="card-link">Learn More <i class="fas fa-arrow-right"></i></a>
            </div>
            <div class="advantage-card">
                <div class="advantage-icon"><i class="fas fa-globe"></i></div>
                <h3>Global Presence in 15 Countries</h3>
                <p><span class="src src-about" data-src-label="IPP About page lists all 15 countries by name">IPP operates offices in 15 countries: Brazil, Canada, China, Czech Republic, France, Germany, India, Italy, Mexico, Pakistan, Portugal, Romania, Turkey, United Kingdom, and United States.</span><a href="https://internationalprocessplants.com/about/" target="_blank" class="src-link"></a> <span class="src src-homepage" data-src-label="IPP homepage: 'more than 160,000 customers worldwide'">IPP has served 160,000+ customers worldwide.</span><a href="https://internationalprocessplants.com" target="_blank" class="src-link"></a></p>
                <a href="/contact/" class="card-link">Find Nearest Office <i class="fas fa-arrow-right"></i></a>
            </div>
            <div class="advantage-card">
                <div class="advantage-icon"><i class="fas fa-flask-vial"></i></div>
                <h3>{card6_title}</h3>
                <p>{card6_text}</p>
                <a href="/contact/" class="card-link">Talk to an Engineer <i class="fas fa-arrow-right"></i></a>
            </div>
        </div>
    </div>
</section>
"""


def generate_how_it_works(cat_tuple):
    """Generate the How It Works section."""
    data_folder, landing_folder, display_name, url_path, ims_url, primary_query, eq_short = cat_tuple
    display_name_plain = display_name.replace("&amp;", "&")
    noun = display_name_plain.rstrip("s").lower() if not display_name_plain.endswith("ss") else display_name_plain.lower()

    return f"""
<!-- ===== HOW IT WORKS ===== -->
<section id="process">
    <div class="container">
        <div class="section-header">
            <h2>How Buying a <span>Used {esc(noun.title())}</span> Works</h2>
            <p>The process of purchasing used {esc(display_name_plain.lower())} from IPP follows five steps, from specification to delivery.</p>
        </div>

        <div class="process-grid">
            <div class="process-step">
                <div class="step-number">1</div>
                <h4>Submit Requirements</h4>
                <p>Share your specifications: capacity, material of construction, pressure rating, temperature, and application. Or browse our searchable inventory.</p>
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
                <p>IPP offers refurbishment services through its UGE division (700+ vessels, 2,700+ parts in stock). Contact IPP for details on additional services.</p>
            </div>
            <div class="process-step">
                <div class="step-number">5</div>
                <h4>Packaging &amp; Delivery</h4>
                <p>IPP coordinates packaging, crating, freight, and delivery to your plant site. Worldwide shipping from offices in 15 countries.</p>
            </div>
        </div>
    </div>
</section>
"""


def generate_industries(cat_tuple, industries):
    """Generate the Industries section."""
    data_folder, landing_folder, display_name, url_path, ims_url, primary_query, eq_short = cat_tuple
    display_name_plain = display_name.replace("&amp;", "&")

    industry_tags = ""
    for ind in industries:
        icon = INDUSTRY_ICONS.get(ind, "fas fa-industry")
        industry_tags += f'            <div class="industry-tag"><i class="{icon}"></i> {esc(ind)}</div>\n'

    return f"""
<!-- ===== INDUSTRIES SERVED ===== -->
<section id="industries">
    <div class="container">
        <div class="section-header">
            <h2>Industries That Buy <span>Used {display_name}</span></h2>
            <p><span class="src src-category" data-src-label="IMS category page lists application industries">IPP supplies used {esc(display_name_plain.lower())} to manufacturers across multiple process industries worldwide.</span><a href="{esc(ims_url)}" target="_blank" class="src-link"></a></p>
        </div>

        <div class="industry-grid">
{industry_tags}        </div>
    </div>
</section>
"""


def generate_faq(cat_tuple, analysis):
    """Generate the FAQ section."""
    data_folder, landing_folder, display_name, url_path, ims_url, primary_query, eq_short = cat_tuple
    display_name_plain = display_name.replace("&amp;", "&")

    top_mfrs = get_top_manufacturers(analysis["manufacturers"], 5)
    top_mfrs_str = ", ".join(top_mfrs) if top_mfrs else "various manufacturers"

    top_materials = [m for m, _ in analysis["materials"].most_common(4)]
    materials_str = ", ".join(top_materials) if top_materials else ""

    cap_range_str = ""
    if analysis["capacity_range"]:
        cap_range_str = f'{analysis["capacity_range"][0][1]} to {analysis["capacity_range"][1][1]}'

    conditions = [c for c, _ in analysis["conditions"].most_common(5)]
    conditions_str = ", ".join(conditions) if conditions else ""

    # Build FAQ tabs and questions
    faq_tabs = []

    # Inventory tab
    inv_questions = []
    inv_questions.append({
        "q": f"How many {display_name_plain.lower()} does IPP have in stock?",
        "a": f'<span class="src src-ims" data-src-label="Manufacturer field across {analysis["count"]} IMS product pages">IPP stocks {display_name_plain.lower()} from {esc(top_mfrs_str)} and other manufacturers.</span>{(" Capacities range from " + esc(cap_range_str) + ".") if cap_range_str else ""}{(" Available in " + esc(materials_str) + " construction.") if materials_str else ""} Browse the IMS inventory for current availability.'
    })
    if conditions_str:
        inv_questions.append({
            "q": f"What condition grades are available for used {display_name_plain.lower()}?",
            "a": f'<span class="src src-ims" data-src-label="Condition field across IMS product pages">IPP stocks {display_name_plain.lower()} in multiple conditions: {esc(conditions_str)}.</span> Browse the current inventory for available condition options.'
        })
    inv_questions.append({
        "q": f"Does IPP sell new {display_name_plain.lower()} as well as used?",
        "a": f'Yes. <span class="src src-about" data-src-label="IPP About page: GPS provides custom fabricated equipment">IPP stocks new {display_name_plain.lower()} through its Gale Process Solutions (GPS) subsidiary, which provides custom fabricated equipment with 12&ndash;16 week average delivery.</span><a href="https://internationalprocessplants.com/about/" target="_blank" class="src-link"></a> Contact IPP for details on new inventory.'
    })
    faq_tabs.append(("Inventory", inv_questions))

    # Specifications tab
    spec_questions = []
    if cap_range_str:
        spec_questions.append({
            "q": f"What capacity range is available for {display_name_plain.lower()}?",
            "a": f'<span class="src src-ims" data-src-label="Capacity field across IMS product pages">IPP stocks {display_name_plain.lower()} with capacities from {esc(cap_range_str)}.</span> Contact IPP with your capacity requirements for specific recommendations.'
        })
    if materials_str:
        spec_questions.append({
            "q": f"What materials of construction are available?",
            "a": f'<span class="src src-ims" data-src-label="Material field across IMS product pages">IPP stocks {display_name_plain.lower()} in {esc(materials_str)} construction.</span> Contact IPP to discuss material requirements for your application.'
        })
    spec_questions.append({
        "q": f"What manufacturers of {display_name_plain.lower()} does IPP stock?",
        "a": f'<span class="src src-ims" data-src-label="Manufacturer field across IMS product pages">IPP stocks {display_name_plain.lower()} from {esc(top_mfrs_str)} and other manufacturers.</span> Browse the current inventory to see available manufacturers.'
    })
    if spec_questions:
        faq_tabs.append(("Specifications", spec_questions))

    # Process tab
    proc_questions = [
        {
            "q": f"How much can I save buying used {display_name_plain.lower()} versus new?",
            "a": f'<span class="src src-homepage" data-src-label="IPP homepage exact quote for used equipment systems savings">Buying used {esc(display_name_plain.lower())} from IPP can save up to 50% of capital and 90% of lead time versus buying new.</span><a href="https://internationalprocessplants.com" target="_blank" class="src-link"></a> The exact savings depend on manufacturer, capacity, material of construction, and condition. Contact IPP for pricing on specific units.'
        },
        {
            "q": f"How long does it take to receive {display_name_plain.lower()} from IPP?",
            "a": f'<span class="src src-category" data-src-label="IMS category page: used {esc(display_name_plain.lower())} in stock and ready to ship">In-stock {display_name_plain.lower()} are ready to ship.</span> <span class="src src-about" data-src-label="IPP About page: GPS \'12-16 week average delivery\'">IPP\'s GPS subsidiary provides new custom fabricated equipment with 12&ndash;16 week average delivery.</span><a href="https://internationalprocessplants.com/about/" target="_blank" class="src-link"></a> <span class="src src-about" data-src-label="IPP About page lists 15 countries">IPP ships from offices in 15 countries worldwide.</span>'
        },
        {
            "q": f"Does IPP handle shipping and freight?",
            "a": f'IPP coordinates packaging, crating, freight, and delivery to your plant site. <span class="src src-about" data-src-label="IPP About page: offices in 15 countries">With offices in 15 countries</span> and <span class="src src-homepage" data-src-label="IPP homepage: \'more than 160,000 customers worldwide\'">160,000+ customers served worldwide</span><a href="https://internationalprocessplants.com" target="_blank" class="src-link"></a>, IPP has extensive experience in global equipment logistics.'
        },
    ]
    faq_tabs.append(("Process", proc_questions))

    # Build HTML
    html = f"""
<!-- ===== FAQ SECTION ===== -->
<section id="faq">
    <div class="container">
        <div class="section-header">
            <h2>Frequently Asked Questions About <span>Buying Used {display_name}</span></h2>
            <p>Answers to the most common questions from engineers and procurement teams evaluating used {esc(display_name_plain.lower())}.</p>
        </div>

        <div class="faq-wrapper">
            <div class="faq-tab-nav" id="faqTabs">
"""
    first = True
    for tab_name, _ in faq_tabs:
        active = ' class="active"' if first else ''
        html += f'                <button{active} data-faqtab="faq-{make_safe_id(tab_name)}">{esc(tab_name)}</button>\n'
        first = False

    html += '            </div>\n\n'

    first = True
    for tab_name, questions in faq_tabs:
        active_class = ' active' if first else ''
        tab_id = f"faq-{make_safe_id(tab_name)}"
        html += f'            <div class="faq-tab-content{active_class}" id="{tab_id}">\n'

        for qa in questions:
            html += f"""                <div class="faq-item">
                    <button class="faq-question">{qa['q']} <i class="fas fa-chevron-down"></i></button>
                    <div class="faq-answer">{qa['a']}</div>
                </div>
"""
        html += '            </div>\n\n'
        first = False

    html += """        </div>
    </div>
</section>
"""
    return html


def generate_cross_sell(cat_tuple, cross_sell_items):
    """Generate the cross-sell section."""
    data_folder, landing_folder, display_name, url_path, ims_url, primary_query, eq_short = cat_tuple
    display_name_plain = display_name.replace("&amp;", "&")
    eq_type = get_equipment_type(data_folder)

    cards = ""
    for name, href, icon in cross_sell_items:
        cards += f"""            <a href="{esc(href)}" class="reactor-type-card">
                <i class="{icon}"></i>
                {esc(name)}
            </a>
"""

    return f"""
<!-- ===== RELATED EQUIPMENT ===== -->
<section id="related-equipment">
    <div class="container">
        <div class="section-header">
            <h2>Other <span>Equipment Types</span> from IPP</h2>
            <p>In addition to {esc(display_name_plain.lower())}, IPP stocks equipment across multiple categories for complete process solutions.</p>
        </div>

        <div class="reactor-type-grid">
{cards}        </div>
    </div>
</section>

<!-- ===== NEW EQUIPMENT CROSS-SELL ===== -->
<div style="background: var(--bg-alt); padding: 48px 0; text-align: center;">
    <div class="container">
        <h3 style="font-size: 22px; font-weight: 700; color: var(--primary); margin-bottom: 12px;">Looking for New {display_name}?</h3>
        <p style="color: var(--text-light); max-width: 700px; margin: 0 auto 24px; line-height: 1.8;"><span class="src src-about" data-src-label="IPP About page: GPS provides custom fabricated equipment with 12-16 week average delivery">IPP Group supplies new equipment through its Gale Process Solutions (GPS) subsidiary, which provides custom fabricated equipment with 12&ndash;16 week average delivery.</span><a href="https://internationalprocessplants.com/about/" target="_blank" class="src-link"></a> <span class="src src-about" data-src-label="IPP About page: UGE &mdash; glass-lined steel equipment subsidiary">IPP also offers re-glassed equipment through its UGE (Universal Glasteel Equipment) division.</span><a href="https://internationalprocessplants.com/about/" target="_blank" class="src-link"></a></p>
        <a href="/contact/" class="btn-primary"><i class="fas fa-envelope"></i> Ask About New Equipment</a>
    </div>
</div>
"""


# ============================================================
# STATIC BLOCKS (CSS, JS, Header, Footer, Review Banner)
# ============================================================

def get_css_block():
    """Return the full CSS block — exact copy from the approved template."""
    return """    <style>
        :root {
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
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        html, body {
            overflow-x: hidden;
            width: 100%;
            max-width: 100vw;
        }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text);
            line-height: 1.7;
            background: var(--bg);
        }

        .container { max-width: 1248px; margin: 0 auto; padding: 0 24px; }

        /* ===== HEADER ===== */
        .header {
            background: var(--primary);
            padding: 16px 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .header .container {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .header-logo {
            color: #fff;
            font-size: 20px;
            font-weight: 800;
            text-decoration: none;
            letter-spacing: -0.5px;
        }
        .header-logo span { color: var(--accent); }
        .header-nav { display: flex; gap: 28px; align-items: center; }
        .header-nav a {
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: color 0.2s;
        }
        .header-nav a:hover { color: #fff; }
        .header-nav .btn-quote {
            background: var(--accent);
            color: #fff;
            padding: 10px 22px;
            border-radius: 6px;
            font-weight: 600;
            transition: background 0.2s;
        }
        .header-nav .btn-quote:hover { background: var(--accent-hover); }

        /* ===== HERO ===== */
        .hero {
            background-color: #192e37;
            background-image: url('https://internationalprocessplants.com/wp-content/uploads/2024/07/ipp-featured-basic.jpg');
            background-size: cover;
            background-position: center;
            background-blend-mode: overlay;
            padding: 80px 0 70px;
            color: #fff;
            position: relative;
        }
        .hero::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(230deg, rgba(21, 75, 99, 0.92), rgba(25, 46, 55, 0.96));
            z-index: 0;
        }
        .hero > .container { position: relative; z-index: 1; }
        .hero-content { overflow-wrap: break-word; word-wrap: break-word; min-width: 0; }
        .hero-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
        }
        .hero h1 {
            font-size: 42px;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 24px;
            letter-spacing: -1px;
        }
        .hero h1 span { color: var(--accent); }
        .hero .intro-text {
            font-size: 16px;
            line-height: 1.8;
            color: rgba(255,255,255,0.85);
            margin-bottom: 32px;
        }
        .hero .intro-expand {
            font-size: 16px;
            line-height: 1.8;
            color: rgba(255,255,255,0.85);
            margin-bottom: 32px;
        }
        .hero .intro-expand summary {
            list-style: none;
            cursor: pointer;
            font-size: inherit;
            line-height: inherit;
            color: inherit;
        }
        .hero .intro-expand summary::-webkit-details-marker { display: none; }
        .hero .intro-expand .arrow-expand {
            color: var(--accent);
            font-size: 18px;
            cursor: pointer;
        }
        .hero .intro-expand[open] summary .truncated {
            display: none;
        }
        .hero .intro-expand[open] summary .arrow-expand {
            display: none;
        }
        .hero .intro-expand .intro-rest {
            margin-top: 16px;
        }
        .hero .intro-expand .arrow-collapse {
            color: var(--accent);
            font-size: 18px;
            cursor: pointer;
        }

        /* Trust badges */
        .trust-badges {
            display: flex;
            gap: 20px;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }
        .trust-badge {
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
        }
        .trust-badge i { color: var(--accent); font-size: 16px; }

        /* Hero CTA */
        .hero-cta-group { display: flex; gap: 16px; margin-bottom: 40px; }
        .btn-primary {
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
        }
        .btn-primary:hover { background: var(--accent-hover); transform: translateY(-1px); }
        .btn-secondary {
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
        }
        .btn-secondary:hover { border-color: #fff; }

        /* Hero stats */
        .hero-stats {
            display: flex;
            gap: 32px;
            padding-top: 24px;
            border-top: 1px solid rgba(255,255,255,0.15);
        }
        .hero-stat .number {
            font-size: 32px;
            font-weight: 800;
            color: var(--accent);
            display: block;
        }
        .hero-stat .label {
            font-size: 13px;
            color: rgba(255,255,255,0.7);
            line-height: 1.4;
        }

        /* Hero image area */
        .hero-image {
            position: relative;
            text-align: center;
        }
        .hero-image img {
            width: 100%;
            max-width: 520px;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .hero-image .savings-badge {
            position: absolute;
            bottom: -16px;
            right: 20px;
            background: var(--success);
            color: #fff;
            padding: 12px 20px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 14px;
            box-shadow: 0 4px 16px rgba(46, 125, 50, 0.4);
        }

        /* ===== SECTION COMMON ===== */
        section { padding: 80px 0; }
        section:nth-child(even) { background: var(--bg-alt); }

        .section-header {
            text-align: center;
            max-width: 720px;
            margin: 0 auto 48px;
        }
        .section-header h2 {
            font-size: 34px;
            font-weight: 800;
            margin-bottom: 16px;
            letter-spacing: -0.5px;
            color: var(--primary);
        }
        .section-header h2 span { color: var(--accent); }
        .section-header p {
            font-size: 16px;
            color: var(--text-light);
            line-height: 1.8;
        }

        /* ===== TABS ===== */
        .tab-nav {
            display: flex;
            gap: 4px;
            background: var(--bg-alt);
            padding: 5px;
            border-radius: 12px;
            justify-content: center;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }
        .tab-nav button {
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
        }
        .tab-nav button.active {
            background: #fff;
            color: var(--primary);
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .tab-nav button:hover:not(.active) { color: var(--primary); }
        .tab-nav button i { font-size: 16px; }

        .tab-content { display: none; }
        .tab-content.active { display: block; }

        /* ===== PRODUCT CARDS ===== */
        .product-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
        }
        .product-card {
            background: #fff;
            border-radius: 14px;
            border: 1px solid var(--border);
            overflow: hidden;
            transition: all 0.3s;
            position: relative;
        }
        .product-card:hover {
            box-shadow: var(--card-hover);
            transform: translateY(-4px);
            border-color: var(--accent);
        }
        .badge-popular {
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
        }
        .product-card-img {
            position: relative;
            height: 200px;
            background: var(--bg-alt);
            display: flex;
            align-items: center;
            justify-content: center;
            border-bottom: 1px solid var(--border);
            overflow: hidden;
        }
        .product-card-img i {
            font-size: 64px;
            color: var(--primary-light);
            opacity: 0.3;
        }
        .product-card-body { padding: 24px; }
        .product-card h3 {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--primary);
        }
        .product-card .card-desc {
            font-size: 14px;
            color: var(--text-light);
            margin-bottom: 16px;
            line-height: 1.6;
        }
        .product-card .specs {
            list-style: none;
            margin-bottom: 20px;
        }
        .product-card .specs li {
            font-size: 13px;
            padding: 6px 0;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--text);
        }
        .product-card .specs li:last-child { border-bottom: none; }
        .product-card .specs li i { color: var(--accent); font-size: 12px; width: 16px; }
        .product-card .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .product-card .price-hint {
            font-size: 13px;
            color: var(--success);
            font-weight: 600;
        }
        .btn-card {
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
        }
        .btn-card:hover { background: var(--primary-light); }
        .btn-inventory {
            color: var(--accent);
            font-size: 12px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: color 0.2s;
        }
        .btn-inventory:hover { color: var(--accent-hover); text-decoration: underline; }
        .card-footer-wrap {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .browse-all-link {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: var(--accent);
            font-weight: 600;
            font-size: 14px;
            text-decoration: none;
            margin-top: 16px;
            transition: color 0.2s;
        }
        .browse-all-link:hover { color: var(--accent-hover); text-decoration: underline; }

        /* ===== ADVANTAGE CARDS ===== */
        .advantage-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
        }
        .advantage-card {
            background: #fff;
            border-radius: 14px;
            padding: 32px;
            border: 1px solid var(--border);
            transition: all 0.3s;
        }
        .advantage-card:hover {
            box-shadow: var(--card-hover);
            transform: translateY(-4px);
        }
        .advantage-icon {
            width: 52px;
            height: 52px;
            background: rgba(26, 143, 196, 0.1);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
        }
        .advantage-icon i { font-size: 22px; color: var(--accent); }
        .advantage-card h3 {
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 10px;
            color: var(--primary);
        }
        .advantage-card p {
            font-size: 14px;
            color: var(--text-light);
            line-height: 1.7;
            margin-bottom: 16px;
        }
        .advantage-card .card-link {
            color: var(--accent);
            font-size: 13px;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        /* ===== FAQ ===== */
        .faq-wrapper {
            max-width: 880px;
            margin: 0 auto;
        }
        .faq-tab-nav {
            display: flex;
            gap: 4px;
            background: var(--bg-alt);
            padding: 5px;
            border-radius: 12px;
            justify-content: center;
            margin-bottom: 32px;
            flex-wrap: wrap;
        }
        .faq-tab-nav button {
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
        }
        .faq-tab-nav button.active {
            background: #fff;
            color: var(--primary);
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .faq-item {
            border: 1px solid var(--border);
            border-radius: 12px;
            margin-bottom: 12px;
            overflow: hidden;
            background: #fff;
        }
        .faq-question {
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
        }
        .faq-question:hover { background: var(--bg-alt); }
        .faq-question i { font-size: 14px; color: var(--accent); transition: transform 0.3s; }
        .faq-answer {
            padding: 0 24px 20px;
            font-size: 14px;
            color: var(--text-light);
            line-height: 1.8;
            display: none;
        }
        .faq-item.open .faq-answer { display: block; }
        .faq-item.open .faq-question i { transform: rotate(180deg); }

        /* ===== CTA BANNER ===== */
        .cta-banner {
            background: linear-gradient(230deg, var(--primary-light), var(--primary));
            padding: 64px 0;
            color: #fff;
            text-align: center;
        }
        .cta-banner h2 {
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 16px;
        }
        .cta-banner p {
            font-size: 16px;
            color: rgba(255,255,255,0.8);
            max-width: 600px;
            margin: 0 auto 32px;
            line-height: 1.7;
        }
        .cta-banner .btn-primary { font-size: 16px; padding: 16px 36px; }

        /* ===== INDUSTRIES ===== */
        .industry-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
        }
        .industry-tag {
            background: #fff;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
            text-align: center;
            font-size: 13px;
            font-weight: 600;
            color: var(--text);
            transition: all 0.2s;
        }
        .industry-tag:hover {
            border-color: var(--accent);
            color: var(--accent);
        }
        .industry-tag i {
            display: block;
            font-size: 24px;
            margin-bottom: 8px;
            color: var(--accent);
        }

        /* ===== PROCESS STEPS ===== */
        .process-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
        }
        .process-step {
            text-align: center;
            padding: 24px 16px;
            position: relative;
        }
        .process-step .step-number {
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
        }
        .process-step h4 {
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--primary);
        }
        .process-step p {
            font-size: 13px;
            color: var(--text-light);
            line-height: 1.5;
        }

        /* ===== COMPARISON TABLE ===== */
        .comparison-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border);
            margin: 32px 0;
        }
        .comparison-table thead th {
            background: var(--primary);
            color: #fff;
            padding: 16px 20px;
            font-size: 14px;
            font-weight: 600;
            text-align: left;
        }
        .comparison-table tbody td {
            padding: 14px 20px;
            font-size: 14px;
            border-bottom: 1px solid var(--border);
        }
        .comparison-table tbody tr:last-child td { border-bottom: none; }
        .comparison-table tbody tr:nth-child(even) { background: var(--bg-alt); }
        .comparison-table .highlight {
            color: var(--success);
            font-weight: 600;
        }

        /* ===== OTHER EQUIPMENT TYPES ===== */
        .reactor-type-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }
        .reactor-type-card {
            background: #fff;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            font-size: 14px;
            font-weight: 600;
            color: var(--text);
            text-decoration: none;
            transition: all 0.2s;
        }
        .reactor-type-card:hover {
            border-color: var(--accent);
            color: var(--accent);
            box-shadow: var(--card-shadow);
        }
        .reactor-type-card i {
            display: block;
            font-size: 28px;
            margin-bottom: 10px;
            color: var(--accent);
        }

        /* ===== FOOTER ===== */
        .footer {
            background: var(--primary);
            color: rgba(255,255,255,0.7);
            padding: 48px 0 24px;
        }
        .footer-grid {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 40px;
            margin-bottom: 40px;
        }
        .footer h4 {
            color: #fff;
            font-size: 15px;
            margin-bottom: 16px;
        }
        .footer p, .footer a {
            font-size: 14px;
            color: rgba(255,255,255,0.6);
            text-decoration: none;
            line-height: 1.8;
        }
        .footer a:hover { color: #fff; }
        .footer ul { list-style: none; }
        .footer ul li { margin-bottom: 8px; }
        .footer-bottom {
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 24px;
            font-size: 13px;
            text-align: center;
        }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 1024px) {
            .hero-grid { grid-template-columns: 1fr; }
            .hero-image { display: none; }
            .product-grid { grid-template-columns: repeat(2, 1fr); }
            .advantage-grid { grid-template-columns: repeat(2, 1fr); }
            .industry-grid { grid-template-columns: repeat(3, 1fr); }
            .process-grid { grid-template-columns: repeat(3, 1fr); }
            .footer-grid { grid-template-columns: 1fr 1fr; }
            .reactor-type-grid { grid-template-columns: repeat(2, 1fr); }
        }

        @media (max-width: 768px) {
            /* Header */
            .header-nav { display: none; }
            .header { padding: 12px 0; }
            .header-logo { font-size: 17px; }

            /* Hero */
            .hero { padding: 40px 0 36px; }
            .hero h1 { font-size: 26px; line-height: 1.2; }
            .hero h1 span { display: inline; }
            .hero-content > p, .hero .intro-expand, .hero .intro-text { font-size: 15px; line-height: 1.7; word-wrap: break-word; overflow-wrap: break-word; }
            .hero-cta-group { flex-direction: column; gap: 12px; }
            .hero-cta-group a { width: 100%; text-align: center; justify-content: center; }
            .btn-primary { padding: 14px 24px; font-size: 15px; }
            .btn-secondary { padding: 12px 24px; font-size: 14px; }

            /* Hero stats */
            .hero-stats {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 16px;
                padding-top: 20px;
            }
            .hero-stat { text-align: center; }
            .hero-stat .number { font-size: 26px; }
            .hero-stat .label { font-size: 12px; }

            /* Trust badges */
            .trust-badges {
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
                padding-bottom: 4px;
            }
            .trust-badge {
                font-size: 12px;
                padding: 8px 12px;
                white-space: nowrap;
            }

            /* Sections */
            section { padding: 40px 0; }
            .section-header { margin-bottom: 32px; }
            .section-header h2 { font-size: 24px; line-height: 1.3; }
            .section-header p { font-size: 14px; word-wrap: break-word; overflow-wrap: break-word; }
            .container { padding: 0 16px; max-width: 100%; overflow-x: hidden; }

            /* Tab nav */
            .tab-nav {
                justify-content: flex-start;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                scrollbar-width: none;
                flex-wrap: nowrap;
                padding: 4px;
                gap: 2px;
            }
            .tab-nav::-webkit-scrollbar { display: none; }
            .tab-nav button {
                padding: 10px 16px;
                font-size: 13px;
                white-space: nowrap;
                flex-shrink: 0;
            }

            /* Tab content */
            .tab-content h3 { font-size: 19px !important; margin-bottom: 8px !important; }
            .tab-content > p { font-size: 14px !important; line-height: 1.7 !important; margin-bottom: 24px !important; }

            /* Product cards */
            .product-grid { grid-template-columns: 1fr; gap: 16px; }
            .product-card-img { height: 140px; }
            .product-card-img i { font-size: 48px; }
            .product-card-body { padding: 16px; }
            .product-card h3 { font-size: 16px; }
            .product-card .card-desc { font-size: 13px; margin-bottom: 12px; }
            .product-card .specs li { font-size: 12px; padding: 5px 0; }
            .product-card .card-footer {
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
            }
            .card-footer-wrap {
                width: 100%;
                flex-direction: row;
                align-items: center;
                gap: 12px;
            }
            .btn-card {
                padding: 10px 16px;
                font-size: 13px;
                flex-shrink: 0;
            }
            .btn-inventory { font-size: 11px; }

            /* Featured badge */
            .badge-popular {
                font-size: 10px;
                padding: 3px 10px;
                top: 8px;
                right: 8px;
            }

            /* Browse all link */
            .browse-all-link { font-size: 13px; margin-top: 12px; }

            /* Comparison table */
            .comparison-table { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }
            .comparison-table thead th { padding: 12px 14px; font-size: 13px; white-space: nowrap; }
            .comparison-table tbody td { padding: 10px 14px; font-size: 13px; min-width: 140px; }

            /* Advantage cards */
            .advantage-grid { grid-template-columns: 1fr; gap: 16px; }
            .advantage-card { padding: 24px; }
            .advantage-card h3 { font-size: 16px; }
            .advantage-card p { font-size: 13px; }

            /* Process steps */
            .process-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
            .process-step { padding: 16px 12px; }
            .process-step .step-number { width: 36px; height: 36px; font-size: 14px; margin-bottom: 12px; }
            .process-step h4 { font-size: 13px; }
            .process-step p { font-size: 12px; }

            /* CTA banner */
            .cta-banner { padding: 40px 0; }
            .cta-banner h2 { font-size: 24px; }
            .cta-banner p { font-size: 14px; }
            .cta-banner .btn-primary { width: 100%; text-align: center; justify-content: center; font-size: 15px; padding: 14px 24px; }

            /* Industries */
            .industry-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
            .industry-tag { padding: 12px; font-size: 12px; }
            .industry-tag i { font-size: 20px; margin-bottom: 6px; }

            /* Equipment types */
            .reactor-type-grid { grid-template-columns: 1fr; gap: 10px; }

            /* FAQ */
            .faq-tab-nav {
                justify-content: flex-start;
                overflow-x: auto;
                -webkit-overflow-scrolling: touch;
                scrollbar-width: none;
                flex-wrap: nowrap;
                padding: 4px;
                gap: 2px;
            }
            .faq-tab-nav::-webkit-scrollbar { display: none; }
            .faq-tab-nav button {
                padding: 8px 14px;
                font-size: 12px;
                white-space: nowrap;
                flex-shrink: 0;
            }
            .faq-question { padding: 16px; font-size: 14px; }
            .faq-answer { padding: 0 16px 16px; font-size: 13px; }

            /* Footer */
            .footer-grid { grid-template-columns: 1fr; gap: 24px; }
            .footer { padding: 36px 0 20px; }
            .footer h4 { font-size: 14px; margin-bottom: 10px; }
            .footer p, .footer a { font-size: 13px; }
            .footer-bottom { font-size: 12px; }

            /* Expandable intro */
            .intro-expand summary p { font-size: 14px; }
            .intro-rest { font-size: 14px; line-height: 1.7; }
        }

            /* Ensure all content respects mobile width */
            img, video, iframe { max-width: 100%; height: auto; }
            .tab-content > p, .section-header p { max-width: 100% !important; }

        /* Small phones */
        @media (max-width: 400px) {
            .hero h1 { font-size: 22px; }
            .hero-stat .number { font-size: 22px; }
            .section-header h2 { font-size: 21px; }
            .cta-banner h2 { font-size: 21px; }
            .tab-nav button { padding: 8px 12px; font-size: 12px; }
            .process-grid { grid-template-columns: 1fr; }
            .industry-grid { grid-template-columns: 1fr 1fr; }
        }
    </style>
    <!-- ===== INTERNAL REVIEW OVERLAY ===== -->
    <style>
        .review-banner {
            position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
            background: #d32f2f; color: #fff; padding: 10px 24px;
            font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 600;
            display: flex; align-items: center; justify-content: space-between;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3);
        }
        .review-banner .legend { display: flex; gap: 16px; align-items: center; }
        .review-banner .legend-item { display: flex; align-items: center; gap: 4px; font-size: 12px; }
        .review-banner .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
        .review-banner .dot-ims { background: #4caf50; }
        .review-banner .dot-homepage { background: #2196f3; }
        .review-banner .dot-about { background: #ff9800; }
        .review-banner .dot-category { background: #9c27b0; }
        .review-banner .dot-product { background: #00bcd4; }
        .review-banner .dot-general { background: #607d8b; }
        .review-toggle { background: #fff; color: #d32f2f; border: none; padding: 6px 14px; border-radius: 4px; font-weight: 700; cursor: pointer; font-size: 12px; }
        body { margin-top: 44px !important; }
        .header { top: 44px !important; }

        /* Source badges */
        .src {
            position: relative;
            border-bottom: 2px dotted;
            cursor: help;
        }
        .src-ims { border-color: #4caf50; background: rgba(76,175,80,0.08); }
        .src-homepage { border-color: #2196f3; background: rgba(33,150,243,0.08); }
        .src-about { border-color: #ff9800; background: rgba(255,152,0,0.08); }
        .src-category { border-color: #9c27b0; background: rgba(156,39,176,0.08); }
        .src-product { border-color: #00bcd4; background: rgba(0,188,212,0.08); }
        .src-general { border-color: #607d8b; background: rgba(96,125,139,0.08); }

        .src-tooltip {
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
        }
        .src-tooltip a {
            color: #4caf50;
            text-decoration: underline;
            font-weight: 600;
            display: inline-block;
            margin-top: 6px;
        }
        .src-tooltip a:hover { color: #81c784; }
        .src-tooltip .close-tip {
            position: absolute;
            top: 4px;
            right: 8px;
            color: #999;
            cursor: pointer;
            font-size: 14px;
            font-weight: 700;
            line-height: 1;
        }
        .src-tooltip .close-tip:hover { color: #fff; }

        /* Source link icon */
        .src-link {
            display: inline-block;
            width: 14px; height: 14px;
            background: currentColor;
            mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3'/%3E%3C/svg%3E") no-repeat center;
            -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3'/%3E%3C/svg%3E") no-repeat center;
            vertical-align: middle;
            margin-left: 2px;
            opacity: 0.7;
        }
        .src-link:hover { opacity: 1; }

        .sources-hidden .src { border-bottom: none !important; background: none !important; }
        .sources-hidden .src::after { display: none !important; }
        .sources-hidden .src-link { display: none !important; }
        .sources-hidden .review-banner { opacity: 0.4; }
    </style>
"""


def get_review_banner():
    """Return the internal review banner HTML."""
    return """
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
"""


def get_header():
    """Return the header HTML."""
    return """
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
"""


def get_footer():
    """Return the footer HTML."""
    return """
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
"""


def get_js_block():
    """Return the JavaScript block."""
    return """
<script>
// Tab functionality
document.querySelectorAll('.tab-nav').forEach(nav => {
    nav.querySelectorAll('button').forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;
            const section = nav.closest('section');

            nav.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            section.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            section.querySelector(`#${tabId}`).classList.add('active');
        });
    });
});

// FAQ tab functionality
document.querySelectorAll('.faq-tab-nav').forEach(nav => {
    nav.querySelectorAll('button').forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.faqtab;

            nav.querySelectorAll('button').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            document.querySelectorAll('.faq-tab-content').forEach(content => {
                content.classList.remove('active');
                content.style.display = 'none';
            });
            const target = document.getElementById(tabId);
            target.classList.add('active');
            target.style.display = 'block';
        });
    });
});

// FAQ accordion
document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', () => {
        const item = question.closest('.faq-item');
        const wasOpen = item.classList.contains('open');

        // Close all in same tab
        item.closest('.faq-tab-content').querySelectorAll('.faq-item').forEach(i => {
            i.classList.remove('open');
        });

        if (!wasOpen) item.classList.add('open');
    });
});

// Initialize FAQ tabs display
document.querySelectorAll('.faq-tab-content').forEach((content, index) => {
    content.style.display = index === 0 ? 'block' : 'none';
});

// === SOURCE ANNOTATION TOOLTIPS ===
const globalTip = document.createElement('div');
globalTip.className = 'src-tooltip';
globalTip.style.display = 'none';
document.body.appendChild(globalTip);

let activeSrc = null;

function closeTooltip() {
    globalTip.style.display = 'none';
    if (activeSrc) activeSrc.classList.remove('active');
    activeSrc = null;
}

function openTooltip(el) {
    const label = el.getAttribute('data-src-label');
    const linkEl = el.nextElementSibling?.classList?.contains('src-link') ? el.nextElementSibling :
                   el.parentElement?.querySelector('.src-link');
    const href = linkEl ? linkEl.getAttribute('href') : null;

    let html = '<span class="close-tip">&times;</span>' + label;
    if (href) {
        html += '<br><a href="' + href + '" target="_blank">Verify source &rarr;</a>';
    }
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

    globalTip.querySelector('.close-tip').onclick = (e) => {
        e.stopPropagation();
        closeTooltip();
    };
}

document.querySelectorAll('.src[data-src-label]').forEach(el => {
    el.addEventListener('click', (e) => {
        e.preventDefault();
        if (activeSrc === el) {
            closeTooltip();
        } else {
            openTooltip(el);
        }
    });
});

document.addEventListener('mousedown', (e) => {
    if (!activeSrc) return;
    if (globalTip.contains(e.target)) return;
    if (activeSrc.contains(e.target)) return;
    closeTooltip();
});

window.addEventListener('scroll', closeTooltip, { passive: true });

document.querySelectorAll('.src-link').forEach(el => el.style.display = 'none');
</script>
"""


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 80)
    print("IPP Landing Page Generator — 37 Equipment Categories")
    print("=" * 80)
    print()

    results = []

    for cat_tuple in CATEGORIES:
        data_folder, landing_folder, display_name, url_path, ims_url, primary_query, eq_short = cat_tuple
        display_name_plain = display_name.replace("&amp;", "&")

        # Load and analyze
        products = load_products(data_folder)
        analysis = analyze_products(products)

        # Generate
        html = generate_page(cat_tuple)

        # Determine output path
        slug = get_slug(landing_folder)
        # Handle special slug cases
        if "/" in landing_folder:
            # e.g., "dryer/spray-dryer" -> slug is "spray-dryer"
            # For glass-lined-parts, append "s" if not already plural in slug
            if landing_folder.startswith("glass-lined-parts/"):
                if not slug.endswith("s") and slug != "pro-ring":
                    slug = slug + "s"

        filename = f"INTERNAL-REVIEW-{slug}.html"
        out_dir = LANDING_DIR / landing_folder
        out_path = out_dir / filename

        # Create directory
        os.makedirs(out_dir, exist_ok=True)

        # Write file
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        line_count = html.count("\n") + 1

        results.append({
            "name": display_name_plain,
            "products": analysis["count"],
            "tab_strategy": analysis["tab_strategy"],
            "tab_groups": len(analysis["tab_groups"]),
            "path": str(out_path),
            "lines": line_count,
        })

        print(f"  [OK] {display_name_plain:45s} | {analysis['count']:5d} products | tabs: {analysis['tab_strategy']:10s} ({len(analysis['tab_groups'])} groups) | {line_count:5d} lines")

    print()
    print("=" * 80)
    print(f"SUMMARY: Generated {len(results)} landing pages")
    print("=" * 80)
    print()
    print(f"{'Category':<45s} | {'Products':>8s} | {'Tab Strategy':>12s} | {'Groups':>6s} | {'Lines':>6s}")
    print("-" * 95)
    for r in results:
        print(f"{r['name']:<45s} | {r['products']:>8d} | {r['tab_strategy']:>12s} | {r['tab_groups']:>6d} | {r['lines']:>6d}")

    total_lines = sum(r["lines"] for r in results)
    total_products = sum(r["products"] for r in results)
    print("-" * 95)
    print(f"{'TOTAL':<45s} | {total_products:>8d} | {'':>12s} | {'':>6s} | {total_lines:>6d}")
    print()
    print("All files written to:")
    for r in results:
        print(f"  {r['path']}")


if __name__ == "__main__":
    main()
