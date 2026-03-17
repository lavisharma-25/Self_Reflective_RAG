import os

# Folder(s) to ignore
EXCLUDE = {'.venv', '.git', '__pycache__', '.vscode'}

# Output file
OUTPUT_FILE = 'tree.txt'

def write_tree(path, prefix=''):
    items = sorted(os.listdir(path))
    items = [i for i in items if i not in EXCLUDE]

    for index, item in enumerate(items):
        full_path = os.path.join(path, item)
        connector = "└── " if index == len(items) - 1 else "├── "
        line = f"{prefix}{connector}{item}"

        # Write line to file
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            f.write(line + '\n')

        # Recurse if directory
        if os.path.isdir(full_path):
            new_prefix = prefix + ("    " if index == len(items) - 1 else "│   ")
            write_tree(full_path, new_prefix)

# Clear previous output
open(OUTPUT_FILE, 'w').close()

# Run from current directory
write_tree(os.getcwd())

print(f"Tree structure saved to {OUTPUT_FILE}")