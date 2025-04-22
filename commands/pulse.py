import os
import json
from datetime import datetime
from core.repo import find_repo
from core.utils import load_wenignore, is_ignored

def pulse(message):
    repo = find_repo()
    if not repo:
        print("Error: Not a wen repository.")
        return

    ignore_patterns = load_wenignore(repo)

    included_files = []

    for root, dirs, files in os.walk("."):
        # Skip .wen directory itself
        if ".wen" in root:
            continue

        # Clean up dirs (ignore dirs inside walk)
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), ignore_patterns)]

        for f in files:
            filepath = os.path.relpath(os.path.join(root, f), start=".")  # relative path
            if is_ignored(filepath, ignore_patterns):
                continue
            included_files.append(filepath)

    # Save the pulse (like before)
    pulses_path = os.path.join(repo, "pulses.json")
    if os.path.exists(pulses_path):
        with open(pulses_path, "r") as f:
            pulses = json.load(f)
    else:
        pulses = []

    new_pulse = {
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "files": included_files,
    }

    pulses.append(new_pulse)

    with open(pulses_path, "w") as f:
        json.dump(pulses, f, indent=4)

    print(f"[wen] Pulse recorded: {message}")
    if included_files:
        print("\n📦 Tracked files:")
        for file in included_files:
            print("  -", file)
    else:
        print("\n[wen] No files to track (all ignored or nothing new).")
