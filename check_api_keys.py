
import os

# The string to search for.
SEARCH_STRING = "OPENAI_API_KEY"

# The root directory to start the scan from. '.' means the current directory.
ROOT_DIRECTORY = '.'

def scan_files():
    """
    Recursively searches for the SEARCH_STRING in all files under ROOT_DIRECTORY.
    """
    found_count = 0
    print(f"[*] Starting scan for '{SEARCH_STRING}' in '{os.path.abspath(ROOT_DIRECTORY)}'...")

    # Common directories to exclude from the scan
    exclude_dirs = ['.git', 'node_modules', '.venv', '__pycache__', 'build', 'dist']

    for dirpath, dirnames, filenames in os.walk(ROOT_DIRECTORY):
        # Modify dirnames in-place to prevent `os.walk` from descending into excluded directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if SEARCH_STRING in line:
                            print(f"  [!] FOUND in: {file_path} (line {line_num})")
                            found_count += 1
            except (IOError, UnicodeDecodeError):
                # This can happen with binary files, so we just skip them.
                pass
    
    print("-" * 40)
    if found_count == 0:
        print("[+] Scan complete. No potential keys found. Your files look clean!")
    else:
        print(f"[!] WARNING: Scan complete. Found {found_count} potential key exposure(s). Please review the files listed above.")

if __name__ == "__main__":
    scan_files()
