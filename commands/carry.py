import os
import requests
import base64
from core.repo import get_repo_root
from core.config import load_config


def carry(args):
    """
    Pull files from GitHub remote into working directory.
    Usage: wen pull <remote-name>
    Requires GITHUB_TOKEN env var.
    """
    if not args:
        print("Error: Missing remote name. Usage: wen pull <remote>")
        return

    remote_name = args[0]
    repo_root = get_repo_root()
    if not repo_root:
        print("Not inside a wen repository.")
        return

    cfg = load_config()
    remotes = cfg.get('remotes', {})
    if remote_name not in remotes:
        print(f"Remote '{remote_name}' not found.")
        return

    url = remotes[remote_name]
    if url.endswith('.git'):
        url = url[:-4]
    parts = url.split('/')
    owner, repo = parts[-2], parts[-1]

    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Set GITHUB_TOKEN in environment to pull.")
        return

    headers = {'Authorization': f'token {token}'}

    def fetch_dir(path="", target_dir=repo_root):
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        r = requests.get(api_url, headers=headers)
        if r.status_code != 200:
            print(f"Failed to list {path}: {r.text}")
            return
        for item in r.json():
            if item['type'] == 'dir':
                new_dir = os.path.join(target_dir, item['path'])
                os.makedirs(new_dir, exist_ok=True)
                fetch_dir(item['path'], target_dir)
            elif item['type'] == 'file':
                r2 = requests.get(item['download_url'], headers=headers)
                if r2.status_code == 200:
                    file_path = os.path.join(target_dir, item['path'])
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    open(file_path, 'wb').write(r2.content)
                else:
                    print(f"Failed to download {item['path']}: {r2.text}")

    fetch_dir()
    print("Pull complete.")