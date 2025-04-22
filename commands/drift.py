import os

def drift(name=None):

    head_path = os.path.join(".wen", "HEAD")
    refs_path = os.path.join(".wen", "refs", name) if name else None

    if name is None:
        print("Usage: wen drift <pulse-id|branch-name>")
        return

    if os.path.exists(refs_path):
        # Drift to a branch
        with open(refs_path, "r") as f:
            pulse_id = f.read().strip()
        with open(head_path, "w") as f:
            f.write(pulse_id)
        print(f"Drifted to branch '{name}' with pulse {pulse_id}")
    else:
        # Drift to a pulse directly
        with open(head_path, "w") as f:
            f.write(name)
        print(f"Drifted to pulse {name}")
