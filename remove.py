import os
import glob

def remove_sanitized_prompt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    marker = 'SANITIZED PROMPT:'
    idx = content.find(marker)
    
    if idx == -1:
        print(f"  [SKIP] No marker found: {file_path}")
        return
    
    # Also remove the separator line (e.g. "====...====") that typically precedes the marker
    # Walk backwards to remove that line too
    before_marker = content[:idx]
    
    # Strip trailing whitespace/newlines and any trailing separator line
    lines = before_marker.splitlines()
    while lines and lines[-1].strip('=').strip() == '':
        lines.pop()
    
    cleaned = '\n'.join(lines) + '\n'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    print(f"  [OK] Cleaned: {file_path}")

def process_folders(folders):
    for folder in folders:
        if not os.path.isdir(folder):
            print(f"[WARNING] Folder not found: '{folder}' — skipping.")
            continue
        
        txt_files = sorted(glob.glob(os.path.join(folder, 'email_*.txt')))
        
        if not txt_files:
            print(f"[WARNING] No email_*.txt files found in '{folder}'.")
            continue
        
        print(f"\nProcessing folder: '{folder}' ({len(txt_files)} files)")
        for file_path in txt_files:
            remove_sanitized_prompt(file_path)

if __name__ == '__main__':
    folders = ['Enterprise', 'Simple']
    process_folders(folders)
    print("\nDone.")