import os
import json
from core.repo import find_repo


def ripple():
    repo = find_repo()
    if not repo:
        print("No repo found")
        return

    pulses_path = os.path.join(repo, "pulses.json")
    tags_path = os.path.join(repo, "tags")

    if not os.path.exists(pulses_path):
        print("[wen] No pulses found.")
        return

    with open(pulses_path, "r") as f:
        pulses = json.load(f)

    if os.path.exists(tags_path):
        with open(tags_path, "r") as f:
            tags = json.load(f)

    else:
        tags = {}

    tag_lookup = {v: k for k, v in tags.items()}

    print("\n[wen] Looking up pulses...")

    for i, pulse in reversed(list(enumerate(pulses))):
        tag_str = f"🏷️ {tag_lookup[str(i)]}" if str(i) in tag_lookup else ""
        print(f"🔸 {pulse['message']} {tag_str}")
        print(f"   🕓 {pulse['timestamp']}\n")