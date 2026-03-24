#!/usr/bin/env python3
"""
IPP IMS URL Status Checker

Checks all URLs in a file for soft-404s (IMS returns 200 but page says "Not Found").

Usage:
    python3 check-status-codes.py --input urls.txt --output-dir ./results/
    python3 check-status-codes.py --input ../data/reactors/batch-type-agitated/urls.txt --output-dir ../data/reactors/batch-type-agitated/
"""

import urllib.request
import urllib.error
import ssl
import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter

CONCURRENCY = 20

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def check_url(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
            body = resp.read(10000).decode("utf-8", errors="ignore")
            if "Not Found" in body:
                return url, "SOFT-404", "Page says equipment not found"
            return url, "LIVE", ""
    except urllib.error.HTTPError as e:
        return url, e.code, str(e.reason)
    except Exception as e:
        return url, "ERROR", str(e)


def main():
    parser = argparse.ArgumentParser(description="Check IPP IMS URLs for soft 404s")
    parser.add_argument("--input", required=True, help="File with URLs (one per line)")
    parser.add_argument("--output-dir", required=True, help="Directory for output files")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.input) as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"Checking {len(urls)} URLs for soft 404s ({CONCURRENCY} threads)...\n")

    results = []
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        futures = {pool.submit(check_url, url): url for url in urls}
        for i, future in enumerate(as_completed(futures), 1):
            results.append(future.result())
            if i % 50 == 0 or i == len(urls):
                print(f"  Progress: {i}/{len(urls)}")

    results.sort(key=lambda x: (str(x[1]), x[0]))

    # Write CSV
    csv_path = os.path.join(args.output_dir, "status_code_results.csv")
    with open(csv_path, "w") as f:
        f.write("url,status,notes\n")
        for url, status, extra in results:
            f.write(f'"{url}","{status}","{str(extra).replace(chr(34), chr(34)+chr(34))}"\n')

    live = [r for r in results if r[1] == "LIVE"]
    dead = [r for r in results if r[1] == "SOFT-404"]
    errors = [r for r in results if r[1] not in ("LIVE", "SOFT-404")]

    # Write live URLs
    live_path = os.path.join(args.output_dir, "live_urls.txt")
    with open(live_path, "w") as f:
        for url, _, _ in sorted(live, key=lambda x: x[0]):
            f.write(url + "\n")

    # Write dead URLs
    dead_path = os.path.join(args.output_dir, "dead_urls.txt")
    with open(dead_path, "w") as f:
        for url, _, _ in sorted(dead, key=lambda x: x[0]):
            f.write(url + "\n")

    print(f"\n{'='*50}")
    print(f"RESULTS ({len(results)} URLs)")
    print(f"{'='*50}")
    print(f"  LIVE: {len(live)}")
    print(f"  SOFT-404: {len(dead)}")
    if errors:
        print(f"  ERRORS: {len(errors)}")
    print(f"\n  live_urls.txt: {live_path}")
    print(f"  dead_urls.txt: {dead_path}")
    print(f"  Full CSV: {csv_path}")


if __name__ == "__main__":
    main()
