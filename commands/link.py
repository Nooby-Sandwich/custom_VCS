import os
from core.config import load_config, save_config


def link(args):
    """
    Manage remotes: list, add, remove
    Usage: wen link list
           wen link add <name> <url>
           wen link remove <name>
    """
    cfg = load_config()
    remotes = cfg.setdefault('remotes', {})

    if not args or args[0] == 'list':
        print("Configured remotes:")
        for name, url in remotes.items():
            print(f"  {name}\t{url}")
        return

    action = args[0]
    if action == 'add' and len(args) == 3:
        name, url = args[1], args[2]
        remotes[name] = url
        save_config(cfg)
        print(f"Remote '{name}' added: {url}")
        return

    if action == 'remove' and len(args) == 2:
        name = args[1]
        if remotes.pop(name, None):
            save_config(cfg)
            print(f"Remote '{name}' removed.")
        else:
            print(f"Remote '{name}' not found.")
        return

    print("Usage: wen link [list|add <name> <url>|remove <name>]")
