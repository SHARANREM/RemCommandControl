description = """
Set system volume percentage
"""

required_packages = [
    "pycaw",
    "comtypes"
]

help = """
Volume Plugin

Usage:
/vol 50
/vol 100
/vol 0

Examples:
/vol 25
/vol 75
/vol 100

Sets Windows master volume.
"""

suggestions = [
    "0",
    "25",
    "50",
    "75",
    "100"
]


def run(*args):

    if not args:
        raise Exception(
            "Usage: /vol <0-100>"
        )

    try:
        volume_percent = int(args[0])

    except ValueError:

        raise Exception(
            "Volume must be a number"
        )

    volume_percent = max(
        0,
        min(100, volume_percent)
    )

    from pycaw.pycaw import AudioUtilities

    speakers = AudioUtilities.GetSpeakers()

    volume = speakers.EndpointVolume

    volume.SetMasterVolumeLevelScalar(
        volume_percent / 100,
        None
    )

    return {
        "success": True,
        "volume": volume_percent
    }


if __name__ == "__main__":

    import sys

    try:

        result = run(
            *sys.argv[1:]
        )

        print(result)

    except Exception as e:

        print(
            f"Error: {e}"
        )