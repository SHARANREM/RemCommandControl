# plugins/browse.py

import subprocess

description = """
Opens saved links in your default browser.
"""

suggestions = [
    "github",
    "yt",
    "chatgpt"
]

help = """
Browse saved links.

Usage:
/browse github
/browse yt
/browse chatgpt

Examples:
/browse github
/browse yt

Description:
Opens predefined URLs using your default browser.
"""

required_packages = []

LINKS = {
    "github": "https://github.com",
    "yt": "https://youtube.com",
    "chatgpt": "https://chatgpt.com"
}

def run(*args):

    if not args:
        raise Exception(
            "Missing link name"
        )

    key = args[0].lower()

    if key not in LINKS:
        raise Exception(
            f"Unknown link '{key}'"
        )

    subprocess.Popen(
        ["cmd", "/c", "start", LINKS[key]],
        shell=True
    )

    return {
        "success": True,
        "message": f"Opened {key}"
    }

if __name__ == "__main__":

    import sys

    run(*sys.argv[1:])


    