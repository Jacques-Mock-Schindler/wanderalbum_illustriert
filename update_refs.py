import os
import re
import json

def update_references(base_dir):
    images_dir_name = 'images'
    files_dir = os.path.join(base_dir, 'files')
    
    # Extensions to look for in references
    img_exts = r'(png|jpg|jpeg|gif|webp)'
    
    for root, dirs, files in os.walk(files_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Determine relative path to images directory
            # root is like C:\...\files\2025\250617_oberengadin
            # base_dir is C:\...\wanderalbum
            # rel_path from root to base_dir/images
            
            # Calculate depth
            rel_from_base = os.path.relpath(root, base_dir)
            # e.g. files\2025\250617_oberengadin
            depth = len(rel_from_base.split(os.sep))
            rel_prefix = "../" * depth + images_dir_name
            
            # Determine date prefix from folder name
            folder_name = os.path.basename(root)
            match = re.match(r'^(\d{6})_', folder_name)
            if match:
                date_prefix = match.group(1) + "_"
            else:
                continue

            if file.endswith('.ipynb'):
                process_ipynb(file_path, rel_prefix, date_prefix, img_exts, images_dir_name)
            elif file.endswith('.md') or file.endswith('.qmd'):
                process_md(file_path, rel_prefix, date_prefix, img_exts, images_dir_name)

def process_ipynb(file_path, rel_prefix, date_prefix, img_exts, images_dir_name):
    print(f"Processing notebook: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    changed = False
    
    for cell in data['cells']:
        if cell['cell_type'] == 'markdown':
            new_source = []
            for line in cell['source']:
                # Pattern for markdown image
                pattern_md = r'!\[(.*?)\]\(((?!http|/|\\)(?:[^)]+)\.(?:' + img_exts + r'))\)'
                
                def replace_md(m):
                    alt = m.group(1)
                    filename = m.group(2)
                    if images_dir_name in filename: 
                        return m.group(0)
                    return f"![{alt}]({rel_prefix}/{date_prefix}{filename})"
                
                new_line = re.sub(pattern_md, replace_md, line)
                
                if new_line != line:
                    changed = True
                new_source.append(new_line)
            cell['source'] = new_source
            
        elif cell['cell_type'] == 'code':
            new_source = []
            for line in cell['source']:
                # Pattern: (['"])([^'"]+\.{img_exts})(['"])
                pattern_code = r'([\'"])((?!http|/|\\)(?:[^\'"]+)\.(?:' + img_exts + r'))(\1)'
                
                def replace_code(m):
                    quote = m.group(1)
                    filename = m.group(2)
                    if images_dir_name in filename:
                        return m.group(0)
                    return f"{quote}{rel_prefix}/{date_prefix}{filename}{quote}"
                
                new_line = re.sub(pattern_code, replace_code, line)
                
                if new_line != line:
                    changed = True
                new_source.append(new_line)
            cell['source'] = new_source

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1)
        print(f"Updated {file_path}")

def process_md(file_path, rel_prefix, date_prefix, img_exts, images_dir_name):
    print(f"Processing markdown: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern_md = r'!\[(.*?)\]\(((?!http|/|\\)(?:[^)]+)\.(?:' + img_exts + r'))\)'
    
    def replace_md(m):
        alt = m.group(1)
        filename = m.group(2)
        if images_dir_name in filename:
            return m.group(0)
        return f"![{alt}]({rel_prefix}/{date_prefix}{filename})"
    
    new_content = re.sub(pattern_md, replace_md, content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {file_path}")

if __name__ == "__main__":
    base_dir = os.getcwd()
    update_references(base_dir)
