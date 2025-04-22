import json
import os

from core.repo import get_repo_root

def write_pulses(pulses):
    """
    Writes the list of pulses to the .wen/pulses.json file.
    """
    repo_root = get_repo_root()
    pulses_path = os.path.join(repo_root, ".wen", "pulses.json")
    os.makedirs(os.path.dirname(pulses_path), exist_ok=True)

    with open(pulses_path, "w") as f:
        json.dump(pulses, f, indent=2)

def write_tags(tags):
    """
    Writes the list of tags to the .wen/tags.json file.
    """
    repo_root = get_repo_root()
    tags_path = os.path.join(repo_root, ".wen", "tags.json")
    os.makedirs(os.path.dirname(tags_path), exist_ok=True)

    with open(tags_path, "w") as f:
        json.dump(tags, f, indent=2)
