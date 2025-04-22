import os
import json
from core.repo import find_repo


def tag(tag_name: str, message: str):
    """
    Create a tag pointing to the latest pulse.
    Usage: wen tag <tag_name> <message>
    """
    repo = find_repo()
    if not repo:
        print("[wen] Error: Not a wen repository.")
        return

    tag_file = os.path.join(repo, "tags.json")
    pulses_file = os.path.join(repo, "pulses.json")

    # Ensure pulses exist
    if not os.path.exists(pulses_file):
        print("[wen] Error: No pulses found to tag.")
        return

    with open(pulses_file, "r") as f:
        pulses = json.load(f)

    if not pulses:
        print("[wen] Error: No pulses recorded yet.")
        return

    # Tag the latest pulse
    latest_pulse = pulses[-1]
    latest_message = latest_pulse.get("message")
    latest_timestamp = latest_pulse.get("timestamp")

    # Load or initialize tags data
    tags = {}
    if os.path.exists(tag_file):
        with open(tag_file, "r") as f:
            tags = json.load(f)

    # Prevent duplicate tag names
    if tag_name in tags:
        print(f"[wen] Error: Tag '{tag_name}' already exists.")
        return

    # Add new tag entry
    tags[tag_name] = {
        "message": message,
        "pulse_message": latest_message,
        "timestamp": latest_timestamp
    }

    # Write back
    with open(tag_file, "w") as f:
        json.dump(tags, f, indent=2)

    print(f"[wen] Tag '{tag_name}' created for pulse: {latest_message}")
