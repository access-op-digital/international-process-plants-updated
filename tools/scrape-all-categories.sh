#!/bin/bash
# Scrape all 37 remaining IPP equipment categories (headed browser)
# #1 and #2 (Reactor subtypes) already done.
#
# IMS type/subtype mapping VERIFIED against live dropdown on 2026-04-07.
# Types are specific (e.g., "Dryer-Porcupine", "Mixer-Muller").
# Only some types have a subtype dropdown.

TOOLS_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$TOOLS_DIR/../data"

scrape() {
    local type="$1"
    local subtype="$2"
    local folder="$3"

    local output_dir="$DATA_DIR/$folder"
    mkdir -p "$output_dir"

    echo ""
    echo "=============================================="
    if [ -n "$subtype" ]; then
        echo "SCRAPING: $type › $subtype"
    else
        echo "SCRAPING: $type (type-only)"
    fi
    echo "FOLDER:   $folder"
    echo "=============================================="

    if [ -n "$subtype" ]; then
        node "$TOOLS_DIR/scrape-equipment-urls.js" --type "$type" --subtype "$subtype" --output "$output_dir/urls.txt"
    else
        node "$TOOLS_DIR/scrape-equipment-urls.js" --type "$type" --output "$output_dir/urls.txt"
    fi

    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo ">>> FAILED: $type / $subtype → $folder (exit $exit_code)" >> "$DATA_DIR/scrape-errors.log"
        return $exit_code
    fi

    echo "--- Checking status codes ---"
    python3 "$TOOLS_DIR/check-status-codes.py" --input "$output_dir/urls.txt" --output-dir "$output_dir/"

    echo "--- Extracting product attributes ---"
    python3 "$TOOLS_DIR/extract-product-attributes.py" --input "$output_dir/live_urls.txt" --output-dir "$output_dir/"

    echo ">>> DONE: $folder"
    echo ""
}

> "$DATA_DIR/scrape-errors.log"

# ── #3  Tank (type-only)
scrape "Tank" "" "tank"

# ── #5  Dryer-Porcupine › Complete
scrape "Dryer-Porcupine" "Complete" "dryer/porcupine-dryer"

# ── #6  Dryer-Rotary Steam Tube (type-only)
scrape "Dryer-Rotary Steam Tube" "" "dryer/rotary-steam-tube-dryer"

# ── #7  Dryer-Rotary Vacuum (type-only)
scrape "Dryer-Rotary Vacuum" "" "dryer/rotary-vacuum-dryer"

# ── #8  Dryer-Spray (type-only)
scrape "Dryer-Spray" "" "dryer/spray-dryer"

# ── #9  Dryer-Holoflite & Screw (type-only)
scrape "Dryer-Holoflite & Screw" "" "dryer/holoflite-and-screw-dryer"

# ── #10 Dryer-Fluid Bed (type-only)
scrape "Dryer-Fluid Bed" "" "dryer/fluid-bed-dryer"

# ── #11 Dryer- Ribbon & Paddle (type-only) — note space after dash, matches IMS exactly
scrape "Dryer- Ribbon & Paddle" "" "dryer/ribbon-and-paddle-dryer"

# ── #12 Centrifuge-Basket › Auto Discharge-Bottom
scrape "Centrifuge-Basket" "Auto Discharge-Bottom" "centrifuge/auto-discharge-bottom"

# ── #13 Centrifuge-Basket › Manual Discharge-Top
scrape "Centrifuge-Basket" "Manual Discharge-Top" "centrifuge/manual-discharge-top"

# ── #14 Centrifuge-Basket › Parts Only
scrape "Centrifuge-Basket" "Parts Only" "centrifuge/basket-centrifuge-parts"

# ── #15 Centrifuge-Disc Bowl (type-only)
scrape "Centrifuge-Disc Bowl" "" "centrifuge/disc-bowl-centrifuge"

# ── #16 Centrifuge-Inverting Filter (type-only)
scrape "Centrifuge-Inverting Filter" "" "centrifuge/inverting-filter-centrifuge"

# ── #17 Centrifuge-Solid Bowl-Decanter (type-only)
scrape "Centrifuge-Solid Bowl-Decanter" "" "centrifuge/solid-bowl-decanter-centrifuge"

# ── #18 Filter › Rosenmund and Cogiem
scrape "Filter" "Rosenmund and Cogiem" "filter/rosenmund-and-cogiem"

# ── #19 Filter › Pressure Leaf
scrape "Filter" "Pressure Leaf" "filter/pressure-leaf"

# ── #20 Filter › Nutsche
scrape "Filter" "Nutsche" "filter/nutsche"

# ── #21 Heat Exchanger › Shell and Tube
scrape "Heat Exchanger" "Shell and Tube" "heat-exchanger/shell-and-tube"

# ── #22 Mixer-Muller (type-only)
scrape "Mixer-Muller" "" "mixer/muller-mixer"

# ── #23 Mixer-Nauta (type-only)
scrape "Mixer-Nauta" "" "mixer/nauta-mixer"

# ── #24 Mixer-Intensive (type-only)
scrape "Mixer-Intensive" "" "mixer/intensive-mixer"

# ── #25 Mixer-Twin Shell & Double Cone (type-only)
scrape "Mixer-Twin Shell & Double Cone" "" "mixer/twin-shell-and-double-cone-mixer"

# ── #26 Mixer-Ribbon & Paddle (type-only)
scrape "Mixer-Ribbon & Paddle" "" "mixer/ribbon-paddle-mixer"

# ── #27 Mixer-Double Arm (type-only)
scrape "Mixer-Double Arm" "" "mixer/double-arm-mixer"

# ── #28 Mixer-Continuous (type-only)
scrape "Mixer-Continuous" "" "mixer/continuous-mixer"

# ── #29 Glass Lined Parts › Agitator
scrape "Glass Lined Parts" "Agitator" "glass-lined-parts/agitator"

# ── #30 Glass Lined Parts › Baffle
scrape "Glass Lined Parts" "Baffle" "glass-lined-parts/baffle"

# ── #31 Glass Lined Parts › Cryo-Lock Blades
scrape "Glass Lined Parts" "Cryo-Lock Blades" "glass-lined-parts/cryo-lock-blades"

# ── #32 Glass Lined Parts › Pro-Ring
scrape "Glass Lined Parts" "Pro-Ring" "glass-lined-parts/pro-ring"

# ── #33 Evaporator › Crystalizer/Evaporator
scrape "Evaporator" "Crystalizer/Evaporator" "evaporator/crystalizer-evaporator"

# ── #34 Evaporator › Flash
scrape "Evaporator" "Flash" "evaporator/flash"

# ── #35 Evaporator › Rising/Falling Film
scrape "Evaporator" "Rising/Falling Film" "evaporator/rising-falling-film"

# ── #36 Evaporator › Wiped/Thin Film
scrape "Evaporator" "Wiped/Thin Film" "evaporator/wiped-thin-film"

# ── #37 Dryer-Twin Shell & Double Cone (type-only)
scrape "Dryer-Twin Shell & Double Cone" "" "dryer/twin-shell-and-double-cone-dryer"

# ── #38 Dryer-Wyssmont (type-only)
scrape "Dryer-Wyssmont" "" "dryer/wyssmont-dryer"

# ── #39 Dryer-Freeze (type-only)
scrape "Dryer-Freeze" "" "dryer/freeze-dryer"

# ── #40 Dryer-Horizontal Belt & Continuous (type-only)
scrape "Dryer-Horizontal Belt & Continuous" "" "dryer/horizontal-belt-continuous-dryer"

echo ""
echo "=============================================="
echo "ALL DONE — 37 categories processed"
echo "=============================================="
if [ -s "$DATA_DIR/scrape-errors.log" ]; then
    echo "ERRORS:"
    cat "$DATA_DIR/scrape-errors.log"
else
    echo "No errors."
fi
