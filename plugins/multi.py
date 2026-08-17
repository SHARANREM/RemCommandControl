import subprocess

description = "Open multiple links"

required_packages = []

help = """
Usage:
/multi github yt

Open multiple saved links at once.
"""

suggestions = [
    "github",
    "yt",
    "chatgpt"
]

LINKS = {
    "github": "https://github.com",
    "yt": "https://youtube.com",
    "chatgpt": "https://chatgpt.com"
}


def run(*args):

    if not args:
        raise Exception(
            "Provide at least one link"
        )

    for key in args:

        key = key.lower()

        if key not in LINKS:
            raise Exception(
                f"Unknown link '{key}'"
            )

        subprocess.Popen(
            f'start "" "{LINKS[key]}"',
            shell=True
        )

    return {
        "success": True,
        "message": f"Opened {len(args)} links"
    }


if __name__ == "__main__":

    import sys

    run(*sys.argv[1:])