import os
import json
from core.repo import find_repo
from core.utils import load_wenignore, is_ignored

def echo():
    repo = find_repo()
    print('[wen] Echoing current pulse...')

    # repo already points to the .wen directory
    pulses_path = os.path.join(repo, "pulses.json")

    if not os.path.exists(pulses_path):
        print("No pulses found.")
        return

    with open(pulses_path, "r") as f:
        try:
            pulses = json.load(f)
        except json.JSONDecodeError as e:
            print("Error: Failed to parse pulses.json:", e)
            return

    if not pulses:
        print("No pulse history available.")
        return

    latest_pulse = pulses[-1]

    print("\n🔍 Current pulse:")
    print(f"🧠 {latest_pulse.get('message', 'No message')}")
    print(f"🕓 {latest_pulse.get('timestamp', 'No timestamp')}")

    # Now use the correct key from your pulses.json
    tracked_files = latest_pulse.get('files', [])

    if tracked_files:
        print("\n📂 Tracked files:")
        wenignore = load_wenignore(repo)
        for file in tracked_files:
            if not is_ignored(file, wenignore):
                print(f"   • {file}")
    else:
        print("\n(no files tracked in this pulse)")
