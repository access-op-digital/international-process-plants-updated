#!/bin/bash
# Re-scrape the 21 categories that failed due to incorrect type names.
# Now using verified IMS dropdown names (e.g., "Dryer-Porcupine" not "Dryer" > "Porcupine").

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
        echo ">>> FAILED: $type / $subtype → $folder (exit $exit_code)" >> "$DATA_DIR/scrape-errors-retry.log"
        return $exit_code
    fi

    echo "--- Checking status codes ---"
    python3 "$TOOLS_DIR/check-status-codes.py" --input "$output_dir/urls.txt" --output-dir "$output_dir/"

    echo "--- Extracting product attributes ---"
    python3 "$TOOLS_DIR/extract-product-attributes.py" --input "$output_dir/live_urls.txt" --output-dir "$output_dir/"

    echo ">>> DONE: $folder"
    echo ""
}

> "$DATA_DIR/scrape-errors-retry.log"

# 11 Dryers (type-only, except Porcupine which has subtype "Complete")
scrape "Dryer-Porcupine" "Complete" "dryer/porcupine-dryer"
scrape "Dryer-Rotary Steam Tube" "" "dryer/rotary-steam-tube-dryer"
scrape "Dryer-Rotary Vacuum" "" "dryer/rotary-vacuum-dryer"
scrape "Dryer-Spray" "" "dryer/spray-dryer"
scrape "Dryer-Holoflite & Screw" "" "dryer/holoflite-and-screw-dryer"
scrape "Dryer-Fluid Bed" "" "dryer/fluid-bed-dryer"
scrape "Dryer- Ribbon & Paddle" "" "dryer/ribbon-and-paddle-dryer"
scrape "Dryer-Twin Shell & Double Cone" "" "dryer/twin-shell-and-double-cone-dryer"
scrape "Dryer-Wyssmont" "" "dryer/wyssmont-dryer"
scrape "Dryer-Freeze" "" "dryer/freeze-dryer"
scrape "Dryer-Horizontal Belt & Continuous" "" "dryer/horizontal-belt-continuous-dryer"

# 3 Centrifuges (type-only)
scrape "Centrifuge-Disc Bowl" "" "centrifuge/disc-bowl-centrifuge"
scrape "Centrifuge-Inverting Filter" "" "centrifuge/inverting-filter-centrifuge"
scrape "Centrifuge-Solid Bowl-Decanter" "" "centrifuge/solid-bowl-decanter-centrifuge"

# 7 Mixers (type-only)
scrape "Mixer-Muller" "" "mixer/muller-mixer"
scrape "Mixer-Nauta" "" "mixer/nauta-mixer"
scrape "Mixer-Intensive" "" "mixer/intensive-mixer"
scrape "Mixer-Twin Shell & Double Cone" "" "mixer/twin-shell-and-double-cone-mixer"
scrape "Mixer-Ribbon & Paddle" "" "mixer/ribbon-paddle-mixer"
scrape "Mixer-Double Arm" "" "mixer/double-arm-mixer"
scrape "Mixer-Continuous" "" "mixer/continuous-mixer"

echo ""
echo "=============================================="
echo "RETRY DONE — 21 categories"
echo "=============================================="
if [ -s "$DATA_DIR/scrape-errors-retry.log" ]; then
    echo "ERRORS:"
    cat "$DATA_DIR/scrape-errors-retry.log"
else
    echo "No errors."
fi
