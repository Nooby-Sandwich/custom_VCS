import os
from core.utils import safe_mkdir, write_file, write_json

WEN_DIR = ".wen"

def init_repo():
    if os.path.exists(WEN_DIR):
        print("Repository already exists.")
        return

    # Create core directories
    safe_mkdir(WEN_DIR)
    safe_mkdir(os.path.join(WEN_DIR, "objects"))
    safe_mkdir(os.path.join(WEN_DIR, "refs"))

    # Initialize HEAD to point to main
    write_file(os.path.join(WEN_DIR, "HEAD"), "ref: refs/main")

    # Create an empty index
    write_json(os.path.join(WEN_DIR, "index.json"), {})

    print("Initialized empty wen repository in .wen/")

def get_repo_path(start="."):
    """Traverse up to find .wen directory."""
    current = os.path.abspath(start)

    while True:
        if os.path.isdir(os.path.join(current, WEN_DIR)):
            return os.path.join(current, WEN_DIR)

        parent = os.path.dirname(current)
        if parent == current:  # Reached filesystem root
            return None
        current = parent

def find_repo():
    """Return path to the repository root (i.e., the .wen dir)"""
    repo_path = get_repo_path()
    if repo_path:
        return repo_path
    else:
        print("Error: Not a wen repository.")
        return None

def get_repo_():
    """Alias for find_repo, used if needed later."""
    return find_repo()

def get_repo_root():
    """Return the parent directory where .wen exists (repo root)."""
    wen_path = get_repo_path()
    if wen_path:
        return os.path.dirname(wen_path)  # Go one level up from `.wen`
    return None
