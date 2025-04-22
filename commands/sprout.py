import os
import json
from core.repo import find_repo
from datetime import datetime


def sprout(branch_name):
    repo = find_repo()
    if not repo:
        print("[wen] Not inside a wen repository.")
        return

    pulses_path = os.path.join(repo, "pulses.json")
    branches_dir = os.path.join(repo, "branches")

    if not os.path.exists(branches_dir):
        os.makedirs(branches_dir)

    branch_file = os.path.join(branches_dir, f"{branch_name}.json")
    if os.path.exists(branch_file):
        print(f"[wen] Branch '{branch_name}' already exists.")
        return

    if not os.path.exists(pulses_path):
        print("[wen] No pulses found to base the branch on.")
        return

    with open(pulses_path, "r") as f:
        pulses = json.load(f)

    with open(branch_file, "w") as f:
        json.dump(pulses, f, indent=2)

    print(f"[wen] New branch '{branch_name}' created with {len(pulses)} pulse(s).")
