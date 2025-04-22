import os
import json
from core.repo import find_repo


def graft(branch_name):
    repo = find_repo()
    if not repo:
        print("[wen] Not inside a wen repository.")
        return

    pulses_path = os.path.join(repo, "pulses.json")
    branches_dir = os.path.join(repo, "branches")
    branch_file = os.path.join(branches_dir, f"{branch_name}.json")

    if not os.path.exists(branch_file):
        print(f"[wen] Branch '{branch_name}' not found")
        return

    if not os.path.exists(pulses_path):
        print("[wen] No current pulses to merge into.")
        return

    with open(pulses_path, "r") as f:
        current_pulses = json.load(f)

    with open(branch_file, "r") as f:
        other_pulses = json.load(f)

    # Avoid duplicate pulses by message+timestamp (custom logic if needed)
    seen = {(p['message'], p['timestamp']) for p in current_pulses}
    for pulse in other_pulses:
        if (pulse['message'], pulse['timestamp']) not in seen:
            current_pulses.append(pulse)

    # Save the updated pulse history
    with open(pulses_path, "w") as f:
        json.dump(current_pulses, f, indent=2)

    print(f"[wen] Grafted branch '{branch_name}' into current pulse history.")
