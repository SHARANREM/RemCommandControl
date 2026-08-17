import subprocess
import urllib.parse

description = """
Search Google directly from RemCheatControl.
"""

required_packages = []

help = """
Google Search Plugin

Usage:
/search something
"""

suggestions = [
    "python",
    "github",
    "chatgpt",
    "tkinter",
    "subprocess"
]


def run(*args):

    if not args:
        raise Exception(
            "Missing search query. Example: /search python"
        )

    query = " ".join(args)

    encoded_query = urllib.parse.quote_plus(
        query
    )

    url = (
        "https://www.google.com/search?q="
        f"{encoded_query}"
    )

    subprocess.Popen(
        f'start "" "{url}"',
        shell=True
    )


if __name__ == "__main__":

    import sys

    run(*sys.argv[1:])