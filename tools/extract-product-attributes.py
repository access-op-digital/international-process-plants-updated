#!/usr/bin/env python3
"""
IPP IMS Product Attribute Extractor

Extracts all product attributes from a list of IMS product URLs.
Dynamically discovers attributes per product — no fixed template.
Stops at "Similar Equipment" section to avoid pulling suggested products.

Usage:
    python3 extract-product-attributes.py --input urls.txt --output-dir ./results/
    python3 extract-product-attributes.py --input ../data/reactors/batch-type-agitated/urls.txt --output-dir ../data/reactors/batch-type-agitated/
"""

import urllib.request
import urllib.error
import ssl
import re
import json
import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

CONCURRENCY = 15

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def extract_product(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
            html = resp.read().decode("utf-8", errors="ignore")

        # Soft 404 check
        if "Not Found" in html and "Equipment" in html:
            return {"url": url, "stock_number": url.split("/")[-1], "error": "SOFT-404", "title": "", "attributes": {}}

        # Product title
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else ""

        # Trim at 'Similar' section — everything after is suggested products
        similar_idx = html.find("Similar")
        if similar_idx > 0:
            html = html[:similar_idx]

        # Dynamically extract ALL attribute label/value pairs
        pattern = r'class="attributeLabel">(.*?)</label>\s*<div class="attributeValue">\s*(.*?)\s*</div>'
        matches = re.findall(pattern, html, re.DOTALL)
        attrs = {}
        for label, value in matches:
            label = re.sub(r'<[^>]+>', '', label).strip().rstrip(":")
            value = re.sub(r'<[^>]+>', '', value).strip()
            value = re.sub(r'\s+', ' ', value)
            # Clean HTML entities
            for entity, char in [("&#xB0;", "°"), ("&quot;", '"'), ("&amp;", "&"),
                                  ("&#x27;", "'"), ("&lt;", "<"), ("&gt;", ">")]:
                value = value.replace(entity, char)
            if label and value:
                attrs[label] = value

        return {
            "url": url,
            "stock_number": url.split("/")[-1],
            "title": title,
            "attribute_count": len(attrs),
            "attributes": attrs
        }
    except Exception as e:
        return {"url": url, "stock_number": url.split("/")[-1], "error": str(e), "title": "", "attributes": {}}


def main():
    parser = argparse.ArgumentParser(description="Extract product attributes from IPP IMS pages")
    parser.add_argument("--input", required=True, help="File with URLs (one per line)")
    parser.add_argument("--output-dir", required=True, help="Directory for output files")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.input) as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"Extracting product data from {len(urls)} pages ({CONCURRENCY} concurrent)...\n")

    results = []
    errors = []
    all_attribute_names = set()

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = {pool.submit(extract_product, url): url for url in urls}
        for i, future in enumerate(as_completed(futures), 1):
            data = future.result()
            results.append(data)
            all_attribute_names.update(data.get("attributes", {}).keys())
            if data.get("error"):
                errors.append(data)
            if i % 25 == 0 or i == len(urls):
                print(f"  Progress: {i}/{len(urls)} | Unique attrs: {len(all_attribute_names)}")

    results.sort(key=lambda x: x["stock_number"])

    # Save JSON
    json_path = os.path.join(args.output_dir, "all_products.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)

    # Save CSV
    sorted_attrs = sorted(all_attribute_names)
    csv_path = os.path.join(args.output_dir, "all_products.csv")
    with open(csv_path, "w") as f:
        header = ["stock_number", "title", "url", "attribute_count"] + sorted_attrs
        f.write(",".join(f'"{h}"' for h in header) + "\n")
        for r in results:
            row = [r["stock_number"], r.get("title", ""), r["url"], str(r.get("attribute_count", 0))]
            for attr in sorted_attrs:
                row.append(r.get("attributes", {}).get(attr, ""))
            f.write(",".join(f'"{v}"' for v in row) + "\n")

    print(f"\n{'='*60}")
    print(f"EXTRACTION COMPLETE")
    print(f"{'='*60}")
    print(f"  Products: {len(results)}")
    print(f"  Errors: {len(errors)}")
    print(f"  Unique attributes: {len(all_attribute_names)}")
    print(f"\n  Attribute coverage:")
    for attr in sorted_attrs:
        count = sum(1 for r in results if attr in r.get("attributes", {}))
        print(f"    {attr}: {count}/{len(results)}")
    print(f"\n  JSON: {json_path}")
    print(f"  CSV:  {csv_path}")


if __name__ == "__main__":
    main()
