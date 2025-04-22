import os
import json
from core.repo import find_repo

def roots():
    repo = find_repo()
    if not repo:
        print("Error: Not a wen repository.")
        return

    pulses_path = os.path.join(repo, "pulses.json")

    if not os.path.exists(pulses_path):
        print("[wen] No pulses found.")
        return

    with open(pulses_path, "r") as f:
        pulses = json.load(f)

    if not pulses:
        print("[wen] No pulses recorded yet.")
        return

    print("\n[wen] Pulse History:")
    for pulse in reversed(pulses):
        print(f"\n🧠 {pulse['message']}")
        print(f"🕓 {pulse['timestamp']}")
