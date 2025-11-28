import os
import shutil
import re

def move_and_rename_images(base_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    files_dir = os.path.join(base_dir, 'files')
    
    # Image extensions to look for
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    moved_files = []

    for root, dirs, files in os.walk(files_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in image_extensions:
                # Get the parent folder name
                parent_folder = os.path.basename(root)
                
                # Extract date prefix (assuming format like 250617_oberengadin)
                match = re.match(r'^(\d{6})_', parent_folder)
                if match:
                    date_prefix = match.group(1)
                    new_filename = f"{date_prefix}_{file}"
                else:
                    # If no date prefix in folder, just use the file name or handle otherwise?
                    # The plan said "Extract the date prefix from the parent folder name".
                    # If it doesn't match, maybe we should skip or just copy?
                    # Let's assume for now we only care about those with the pattern.
                    # But wait, files/2025/2025.qmd is a file, but we are looking in subdirs.
                    # The subdirs in files/2025/ are like 250617_oberengadin.
                    # Let's log if we can't find a prefix.
                    print(f"Skipping {file} in {parent_folder} (no date prefix found)")
                    continue

                source_path = os.path.join(root, file)
                target_path = os.path.join(target_dir, new_filename)
                
                # Check if target exists to avoid overwriting different files with same name (unlikely with date prefix but possible)
                if os.path.exists(target_path):
                    print(f"Warning: {target_path} already exists. Skipping {source_path}")
                    continue

                print(f"Moving {source_path} to {target_path}")
                shutil.move(source_path, target_path)
                moved_files.append((source_path, new_filename))

    return moved_files

if __name__ == "__main__":
    base_dir = os.getcwd()
    target_dir = os.path.join(base_dir, 'images')
    move_and_rename_images(base_dir, target_dir)
