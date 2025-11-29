import json
import os
import re
import base64
import glob

# Base directory for files
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "files", "2025"))

# Target notebooks to update
NOTEBOOKS = [
    "250629_maderanertal/maderanertal.ipynb",
    "250706_hauenstein/hauenstein.ipynb",
    "250712_guscha/guscha.ipynb",
    "250719_appenzell/appenzell.ipynb",
    "250722_aelpli/aelpli.ipynb",
    "250727_dalpe/dalpe.ipynb",
    "250731_isone/isone.ipynb",
    "250803_suedrampe/suedrampe.ipynb",
    "250805_zuerich/zuerich.ipynb",
    "250807_hautrive/hauterive.ipynb"
]

def extract_variables(notebook_content):
    """Extracts center, cener_swiss_grid, and path from the notebook."""
    variables = {}
    for cell in notebook_content['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            # Look for variables
            center_match = re.search(r"center\s*=\s*\[([\d\.]+),\s*([\d\.]+)\]", source)
            grid_match = re.search(r"(?:cener|center)_swiss_grid\s*=\s*\[([\d\.]+),\s*([\d\.]+)\]", source)
            path_match = re.search(r"path\s*=\s*\"([^\"]+)\"", source)
            
            if center_match:
                variables['center'] = [float(center_match.group(1)), float(center_match.group(2))]
            if grid_match:
                variables['swiss_grid'] = [float(grid_match.group(1)), float(grid_match.group(2))]
            if path_match:
                variables['path'] = path_match.group(1)
            
            if 'center' in variables and 'swiss_grid' in variables and 'path' in variables:
                break
    return variables

def create_urls(variables):
    """Constructs the Swisstopo URLs."""
    path = variables['path']
    # Extract folder and filename from path (e.g., "../../../files/2025/250629_maderanertal/250629_golzeren.gpx")
    # We assume the path structure is consistent relative to the notebook or absolute-ish
    # Actually, let's just grab the part after "files/2025/"
    match = re.search(r"files/2025/(.+)$", path)
    if not match:
        print(f"Could not parse path: {path}")
        return None
    
    rel_path = match.group(1)
    github_raw_url = f"https://raw.githubusercontent.com/Jacques-Mock-Schindler/wanderalbum_illustriert/main/files/2025/{rel_path}"
    
    # Swisstopo Web URL
    swiss_grid = variables['swiss_grid']
    web_url = f"https://map.geo.admin.ch/#/map?lang=de&center={swiss_grid[0]},{swiss_grid[1]}&z=6&bgLayer=ch.swisstopo.pixelkarte-farbe&topic=ech&layers=GPX|{github_raw_url}"
    
    # Mobile App URL (Base64 encoded)
    url_bytes = github_raw_url.encode('utf-8')
    encoded_bytes = base64.b64encode(url_bytes)
    encoded_string = encoded_bytes.decode('utf-8')
    mobile_url = f"https://swisstopo.app/u/{encoded_string}"
    
    return {
        'web_url': web_url,
        'mobile_url': mobile_url
    }

def create_cells(urls):
    """Creates the new cells to be inserted."""
    
    # 1. Markdown Link Cell
    markdown_source = [
        "Die Karte auf der Website von \n",
        f"[swisstopo.ch]({urls['web_url']})\n",
        "oder in der \n",
        f"[Mobile App]({urls['mobile_url']})\n",
        "von swisstopo öffnen."
    ]
    
    markdown_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": markdown_source
    }
    
    # 2. Code QR Cell
    code_source = [
        f"generate_qr_code_for_url(\"{urls['mobile_url']}\")"
    ]
    
    code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code_source
    }
    
    # 3. PDF QR Cell
    # Using qr_tag.png as it is generated in the CWD by the script
    pdf_source = [
        "::: {.content-visible when-format=\"pdf\"}\n",
        "| Swisstopo.ch | Mobile App |\n",
        "| --- | --- |\n",
        "| ![](qr_tag.png){width=3cm height=3cm} | ![](qr_tag.png){width=3cm height=3cm} |\n",
        ":::"
    ]
    
    pdf_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": pdf_source
    }
    
    return [markdown_cell, code_cell, pdf_cell]

def update_notebook(file_path):
    print(f"Processing {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    variables = extract_variables(notebook)
    if not variables or 'swiss_grid' not in variables:
        print(f"Skipping {file_path}: Could not find necessary variables.")
        return

    urls = create_urls(variables)
    if not urls:
        return

    new_cells = create_cells(urls)
    
    # Find insertion point
    insert_index = -1
    for i, cell in enumerate(notebook['cells']):
        # We look for the profile(path) call
        if cell['cell_type'] == 'code' and 'profile(path)' in "".join(cell['source']):
            insert_index = i + 1
            break
    
    if insert_index == -1:
        # Fallback: look for create_map
        for i, cell in enumerate(notebook['cells']):
            if cell['cell_type'] == 'code' and 'create_map' in "".join(cell['source']):
                insert_index = i + 2 # Skip the map output markdown cell usually following it
                break
    
    if insert_index == -1:
        print(f"Skipping {file_path}: Could not find insertion point (profile or create_map).")
        return

    # Check if cells already exist (idempotency)
    # We check the next few cells to see if they look like our target cells
    # If they do, we update them. If not, we insert.
    
    # Simple check: does "Die Karte auf der Website von" exist in the notebook?
    existing_link_index = -1
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'markdown' and "Die Karte auf der Website von" in "".join(cell['source']):
            existing_link_index = i
            break
            
    if existing_link_index != -1:
        print(f"Updating existing cells in {file_path}...")
        # Update the existing markdown cell
        notebook['cells'][existing_link_index] = new_cells[0]
        # Assuming the next ones are the code and PDF cells, we update them too if they match type
        # But safer to just replace/insert around that area.
        # Actually, let's just replace the found cell and insert the others if missing.
        
        # Check for QR code cell
        if existing_link_index + 1 < len(notebook['cells']) and \
           notebook['cells'][existing_link_index + 1]['cell_type'] == 'code' and \
           "generate_qr_code_for_url" in "".join(notebook['cells'][existing_link_index + 1]['source']):
            notebook['cells'][existing_link_index + 1] = new_cells[1]
        else:
            notebook['cells'].insert(existing_link_index + 1, new_cells[1])
            
        # Check for PDF cell
        if existing_link_index + 2 < len(notebook['cells']) and \
           notebook['cells'][existing_link_index + 2]['cell_type'] == 'markdown' and \
           "content-visible when-format=\"pdf\"" in "".join(notebook['cells'][existing_link_index + 2]['source']) and \
           "qr_tag" in "".join(notebook['cells'][existing_link_index + 2]['source']):
             notebook['cells'][existing_link_index + 2] = new_cells[2]
        else:
             notebook['cells'].insert(existing_link_index + 2, new_cells[2])

    else:
        print(f"Inserting new cells in {file_path} at index {insert_index}...")
        # Insert all 3 cells
        for cell in reversed(new_cells):
            notebook['cells'].insert(insert_index, cell)

    # Save notebook
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1)
        print(f"Successfully updated {file_path}")
    except Exception as e:
        print(f"Error writing {file_path}: {e}")

def main():
    for rel_path in NOTEBOOKS:
        file_path = os.path.join(BASE_DIR, rel_path)
        if os.path.exists(file_path):
            update_notebook(file_path)
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    main()
