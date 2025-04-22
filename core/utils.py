import os
import json
import fnmatch

def safe_mkdir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def write_file(path: str, content: str):
    with open(path, 'w') as f:
        f.write(content)

def write_json(path: str, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def write_object(obj_hash, data):
    object_path = os.path.join(".wen", "objects")
    with open(os.path.join(object_path, obj_hash), "w") as f:
        f.write(data)

def find_repo():
    current_dir = os.getcwd()
    while current_dir != os.path.dirname(current_dir):
        if os.path.exists(os.path.join(current_dir, ".wen")):
            return os.path.join(current_dir, ".wen")
        current_dir = os.path.dirname(current_dir)
    return None  # Not found

def load_wenignore(repo_path):
    ignore_file = os.path.join(repo_path, ".wenignore")
    ignore_patterns = []

    if os.path.exists(ignore_file):
        with open(ignore_file) as f:
            ignore_patterns = [line.strip() for line in f if line.strip()]

    return ignore_patterns

def is_ignored(filepath, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(filepath, pattern) or filepath.startswith(pattern):
            return True
    return False
