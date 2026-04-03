#!/usr/bin/python3

"""
Miniature wrapper script to execute a shell outside the Flatpak sandbox.
"""

import functools
import os
import re
import subprocess
import sys
from pathlib import Path, PurePath

APP_ID = "dev.zed.Zed"
SPAWN_HOST_NO_PTY = ("/app/bin/host-spawn", "-no-pty")
SPAWN_HOST = ("/app/bin/host-spawn",)


@functools.cache
def flatpak_host_location() -> PurePath:
    "Get the location of this app on the host"
    result = subprocess.run(
        [
            *SPAWN_HOST_NO_PTY,
            "flatpak",
            "info",
            "--show-location",
            APP_ID,
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return PurePath(result.stdout.strip()) / "files"


def app_to_host_path(m: re.Match) -> str:
    "Remap a /app/* path to the corresponding path on the host."
    return str(flatpak_host_location() / m[1])


def identify_shell(arg0: str) -> str:
    "Decide on the shell to execute"

    # If we are running through a symlink, act as a shim
    arg0_path = Path(arg0)
    if arg0_path.is_symlink():
        return arg0_path.name

    # Attempt to find the user's default shell using getent
    try:
        result = subprocess.run(
            [*SPAWN_HOST_NO_PTY, "getent", "passwd", os.environ["USER"]],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip().split(":")[6]
    except (KeyError, subprocess.SubprocessError):
        pass

    # Otherwise choose a poor but almost certainly present default
    return "sh"


def fix_args(args: list[str]) -> list[str]:
    "Fix up the list of arguments to pass to the shell itself"

    def fix_arg(arg: str) -> str:
        # Zed tries to run itself to identify the shell environment, but since this
        # command runs outside the sandbox, /app/ isn't mounted and thus crashes.
        # Remap these specific paths to their matching host path.
        return re.sub(r"/app/((?:bin|libexec)/zed)", app_to_host_path, arg)

    return [fix_arg(arg) for arg in args]


if __name__ == "__main__":
    os.execv(
        SPAWN_HOST[0],
        [*SPAWN_HOST, identify_shell(sys.argv[0]), *fix_args(sys.argv[1:])],
    )
