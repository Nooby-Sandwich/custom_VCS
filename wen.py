#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
import json
import base64
import requests
from core.repo import get_repo_root
from core.config import load_config
from core.utils import load_wenignore, is_ignored
# Load environment variables from .env
load_dotenv()

def print_usage():
    print(
        "Usage: wen <command> [args]\n"
        "Commands:\n"
        "  seed                      Initialize a new wen repository\n"
        "  pulse <message>           Record a new pulse (commit) with MESSAGE\n"
        "  tag <name> <message>      Create a tag NAME pointing to the latest pulse\n"
        "  roots                     Show pulse history\n"
        "  ripple                    Show log of pulses\n"
        "  sprout <name>             Create a new branch from current pulses\n"
        "  graft <branch>            Merge pulses from another branch\n"
        "  echo                      Show the current state of the latest pulse\n"
        "  drift <pulse-id|branch>   Switch to a pulse or branch\n"
        "  link [list|add|remove]    Manage remotes\n"
        "  transmit [remote]         Push working tree to GitHub remote\n"
        "  carry [remote]            Pull from GitHub remote\n"
    )


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    # Core commands
    if cmd == "seed":
        from commands.seed import seed
        seed()

    elif cmd == "pulse":
        if not args:
            print("Error: Missing pulse message.")
            print_usage()
            sys.exit(1)
        from commands.pulse import pulse
        pulse(" ".join(args))

    elif cmd == "tag":
        if len(args) < 2:
            print("Error: Missing tag name or message.")
            print_usage()
            sys.exit(1)
        from commands.tag import tag
        tag(args[0], " ".join(args[1:]))

    elif cmd == "roots":
        from commands.roots import roots
        roots()

    elif cmd == "ripple":
        from commands.ripple import ripple
        ripple()

    elif cmd == "sprout":
        if not args:
            print("Error: Missing branch name for sprout.")
            print_usage()
            sys.exit(1)
        from commands.sprout import sprout
        sprout(args[0])

    elif cmd == "graft":
        if not args:
            print("Error: Missing source branch name for graft.")
            print_usage()
            sys.exit(1)
        from commands.graft import graft
        graft(args[0])

    elif cmd == "echo":
        from commands.echo import echo
        echo()

    elif cmd == "drift":
        if not args:
            print("Error: Missing pulse-id or branch name for drift.")
            print_usage()
            sys.exit(1)
        from commands.drift import drift
        drift(args[0])

    # Remote management
    elif cmd == "link":
        from commands.link import link
        link(args)

    # Push (transmit) to GitHub
    elif cmd == "transmit":
        remote_name = args[0] if args else os.getenv("DEFAULT_REMOTE", "origin")
        from commands.transmit import transmit
        transmit([remote_name])

    # Pull (carry) from GitHub
    elif cmd == "carry":
        remote_name = args[0] if args else os.getenv("DEFAULT_REMOTE", "origin")
        from commands.carry import carry
        carry([remote_name])

    else:
        print(f"Unknown command: {cmd}\n")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
