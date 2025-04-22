import os
import json

CONFIG_FILE = os.path.join('.wen', 'config.json')


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"remotes": {}}
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def save_config(cfg):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(cfg, f, indent=2)
