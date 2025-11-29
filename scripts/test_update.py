import json
import base64
from pathlib import Path

def encode_gpx_url_for_mobile_app(gpx_url):
    """Encode GPX URL to base64 for Swisstopo Mobile App."""
    encoded = base64.b64encode(gpx_url.encode('utf-8')).decode('utf-8')
    return f"https://swisstopo.app/u/{encoded}"

def extract_gpx_url_from_swisstopo_link(swisstopo_url):
    """Extract the GPX URL from a Swisstopo map link."""
    if 'layers=GPX|' in swisstopo_url:
        return swisstopo_url.split('layers=GPX|')[1]
    return None

# Test with one notebook
notebook_path = Path(r"c:\Users\jcms\Documents\wanderalbum\files\2025\250629_maderanertal\maderanertal.ipynb")

print(f"Testing: {notebook_path}")

with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

for cell_idx, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'markdown':
        source = cell['source']
        print(f"\nCell {cell_idx}: {len(source)} lines")
        
        for i, line in enumerate(source):
            if '[Die Karte auf der Website von swisstopo.ch' in line:
                print(f"  Found at line {i}: {line[:50]}...")
                print(f"  Next line exists: {i + 1 < len(source)}")
                if i + 1 < len(source):
                    print(f"  Next line: {source[i + 1][:50]}...")
