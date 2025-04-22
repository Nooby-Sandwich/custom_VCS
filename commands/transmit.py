import os
import base64
import json
import requests

from core.repo import find_repo
from core.utils import load_wenignore, is_ignored

GITHUB_API = "https://api.github.com"

def transmit(args):
    repo = find_repo()
    if not repo:
        print("[wen] Not inside a wen repository.")
        return

    # Load remotes from config
    cfg_path = os.path.join(repo, "config.json")
    if not os.path.exists(cfg_path):
        print("[wen] No remotes configured. Use `wen link add` first.")
        return

    with open(cfg_path) as f:
        config = json.load(f)

    name = args[0] if args else os.getenv("DEFAULT_REMOTE", "origin")
    if name not in config.get("remotes", {}):
        print(f"[wen] Remote '{name}' not found in config.")
        return

    remote_url = config["remotes"][name]
    # Expect URL like https://github.com/owner/repo.git
    owner, repo_name = remote_url.rstrip(".git").rsplit("/", 2)[-2:]

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("[wen] GITHUB_TOKEN not set; cannot transmit.")
        return

    ignore_patterns = load_wenignore(repo)
    root_dir = os.getcwd()

    for root, dirs, files in os.walk(root_dir):
        # skip .wen entirely
        if os.path.abspath(root).startswith(os.path.abspath(os.path.join(root_dir, ".wen"))):
            continue

        # filter out ignored directories
        dirs[:] = [d for d in dirs 
                   if not is_ignored(os.path.relpath(os.path.join(root, d), root_dir), ignore_patterns)]

        for fname in files:
            relpath = os.path.relpath(os.path.join(root, fname), root_dir).replace("\\", "/")

            # skip ignored files
            if is_ignored(relpath, ignore_patterns):
                continue

            full_path = os.path.join(root, fname)
            with open(full_path, "rb") as f:
                content_b64 = base64.b64encode(f.read()).decode()

            api_path = f"/repos/{owner}/{repo_name}/contents/{relpath}"
            url = GITHUB_API + api_path
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }

            # Check if file exists to get its sha
            get_resp = requests.get(url, headers=headers)
            if get_resp.status_code == 200:
                sha = get_resp.json()["sha"]
            else:
                sha = None

            payload = {
                "message": f"wen transmit {relpath}",
                "content": content_b64
            }
            if sha:
                payload["sha"] = sha

            put_resp = requests.put(url, headers=headers, json=payload)
            if put_resp.status_code in (200, 201):
                action = "Updated" if sha else "Created"
                print(f"[wen] {action}: {relpath}")
            else:
                print(f"[wen] Failed to upload {relpath}: {put_resp.json()}")

    print("[wen] Transmit complete.")
