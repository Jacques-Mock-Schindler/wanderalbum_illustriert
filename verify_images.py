import os
import re
import json

def verify_references(base_dir):
    images_dir_name = 'images'
    files_dir = os.path.join(base_dir, 'files')
    images_dir = os.path.join(base_dir, images_dir_name)
    
    # Extensions to look for in references
    img_exts = r'(?:png|jpg|jpeg|gif|webp)'
    
    broken_links = []
    checked_files = 0
    
    for root, dirs, files in os.walk(files_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            if file.endswith('.ipynb'):
                checked_files += 1
                check_ipynb(file_path, base_dir, img_exts, broken_links)
            elif file.endswith('.md') or file.endswith('.qmd'):
                checked_files += 1
                check_md(file_path, base_dir, img_exts, broken_links)

    print(f"Checked {checked_files} files.")
    if broken_links:
        print(f"Found {len(broken_links)} broken links:")
        for source, link in broken_links:
            print(f"  In {source}: {link}")
    else:
        print("No broken links found!")

def check_link(link, file_path, base_dir, broken_links):
    # Resolve link
    # If it starts with http, ignore
    if link.startswith('http') or link.startswith('https'):
        return

    # If it is absolute path (unlikely in md), ignore or check
    if os.path.isabs(link):
        if not os.path.exists(link):
            broken_links.append((file_path, link))
        return

    # Relative path
    # Resolve relative to file_path
    file_dir = os.path.dirname(file_path)
    target_path = os.path.normpath(os.path.join(file_dir, link))
    
    if not os.path.exists(target_path):
        broken_links.append((file_path, link))

def check_ipynb(file_path, base_dir, img_exts, broken_links):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    for cell in data['cells']:
        if cell['cell_type'] == 'markdown':
            for line in cell['source']:
                # Pattern for markdown image
                pattern_md = r'!\[.*?\]\(((?!http|/|\\)(?:[^)]+)\.(?:' + img_exts + r'))\)'
                matches = re.findall(pattern_md, line)
                for link in matches:
                    check_link(link, file_path, base_dir, broken_links)
        elif cell['cell_type'] == 'code':
            for line in cell['source']:
                # Pattern: (['"])([^'"]+\.{img_exts})(['"])
                pattern_code = r'([\'"])((?!http|/|\\)(?:[^\'"]+)\.(?:' + img_exts + r'))(\1)'
                matches = re.findall(pattern_code, line)
                for _, link, _ in matches:
                    check_link(link, file_path, base_dir, broken_links)

def check_md(file_path, base_dir, img_exts, broken_links):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    pattern_md = r'!\[.*?\]\(((?!http|/|\\)(?:[^)]+)\.(?:' + img_exts + r'))\)'
    matches = re.findall(pattern_md, content)
    for link in matches:
        check_link(link, file_path, base_dir, broken_links)

if __name__ == "__main__":
    base_dir = os.getcwd()
    verify_references(base_dir)
