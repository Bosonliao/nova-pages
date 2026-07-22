#!/usr/bin/env python3
"""Batch geocode all shops in west-end-brisbane.html using Google Geocoding API."""

import re
import json
import time
import urllib.request
import urllib.parse
import os
import sys

# Fix encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "west-end-brisbane.html")
API_KEY = "REDACTED"

def geocode(name):
    """Query Google Geocoding API for a shop name in West End Brisbane."""
    address = f"{name} West End Brisbane Australia"
    encoded = urllib.parse.quote(address)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded}&key={API_KEY}&language=en"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data.get("results"):
            loc = data["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]
        else:
            return None, None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None, None

def main():
    # Read HTML
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract shop names from top-level DATA objects only
    # Top-level objects: { name: "XXX", cat: "YYY", ...
    # Dishes: {name:"XXX",desc:"YYY"}  (no space before name, no cat after)
    # Pattern: { name: "..." followed by , cat: "
    pattern = re.compile(r'\{\s*name:\s*"([^"]+)"\s*,\s*cat:\s*"')
    matches = list(pattern.finditer(html))
    names = [m.group(1) for m in matches]
    
    print(f"Found {len(names)} shops in DATA")
    
    if not names:
        print("No shops found! Check the HTML structure.")
        return
    
    # Geocode each shop
    coords = {}
    print(f"Geocoding {len(names)} shops...")
    
    for i, name in enumerate(names):
        print(f"[{i+1}/{len(names)}] {name}", end="")
        lat, lng = geocode(name)
        if lat is not None:
            coords[name] = (lat, lng)
            print(f" -> {lat:.4f}, {lng:.4f}")
        else:
            print(" -> FAILED")
        time.sleep(0.2)
    
    print(f"\nSuccessfully geocoded {len(coords)}/{len(names)} shops")
    
    if not coords:
        print("No coordinates obtained. Exiting.")
        return
    
    # Insert lat/lng into the HTML for each shop
    # For each top-level object `{ name: "XXX", cat: "YYY", ...`,
    # insert `lat: XX.XXXXXX, lng: XX.XXXXXX,` after the `cat: "YYY",` part
    # This avoids touching the dishes sub-objects
    
    modified = html
    insertions = 0
    
    for name, (lat, lng) in coords.items():
        escaped_name = re.escape(name)
        # Pattern: { name: "name", cat: "xxx", 
        # Group 1 = `{ name: "name", cat: "xxx", `
        # We insert lat and lng after group 1
        cat_pattern = re.compile(r'(\{\s*name:\s*"' + escaped_name + r'"\s*,\s*cat:\s*"[^"]*"\s*,\s*)')
        
        # Check if already has lat/lng
        def replace_if_needed(m):
            nonlocal insertions
            # Look ahead to see if lat: already exists within this object
            after = modified[m.end():m.end()+1000]
            # Check if there's a lat: before the next `{ name:` or end of object
            if re.search(r'\blat:\s*[\d.-]+', after[:500]):
                return m.group(0)  # Already has lat, skip
            insertions += 1
            return m.group(1) + f' lat: {lat:.6f}, lng: {lng:.6f},'
        
        new_modified = cat_pattern.sub(replace_if_needed, modified, count=1)
        if new_modified != modified:
            modified = new_modified
    
    print(f"Made {insertions} coordinate insertions")
    
    # Write to temp file first, then replace
    tmp_path = HTML_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(modified)
    
    # Verify the file
    with open(tmp_path, "r", encoding="utf-8") as f:
        verify_html = f.read()
    verify_matches = pattern.findall(verify_html)
    if len(verify_matches) != len(names):
        print(f"WARNING: Shop count changed from {len(names)} to {len(verify_matches)}! Not replacing.")
        os.remove(tmp_path)
        return
    
    # Replace original
    os.replace(tmp_path, HTML_PATH)
    print(f"Updated {HTML_PATH}")
    print(f"Total shops: {len(names)}, Coordinates added: {insertions}")
    
    # Print summary
    coded = sum(1 for n in names if n in coords)
    failed = [n for n in names if n not in coords]
    print(f"Success: {coded}, Failed: {len(failed)}")
    if failed:
        print("Failed shops:")
        for n in failed:
            print(f"  - {n}")

if __name__ == "__main__":
    main()
