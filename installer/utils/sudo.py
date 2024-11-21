import shutil
import subprocess
import sys

from loader import log


def check_sudo_privileges() -> None:
    """
    Checks if sudo is installed and if the current user has sudo privileges.
    Exits the script with an error if sudo is unavailable or privileges are missing.
    """
    if not shutil.which("sudo"):
        log.error("Error: sudo is not installed. Please install sudo and try again.")
        sys.exit(1)

    try:
        result = subprocess.run(
            ["sudo", "-n", "true"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            log.error("Error: You do not have sudo privileges. Please contact your administrator.")
            sys.exit(1)
    except Exception as e:
        log.error(f"Error: An issue occurred while checking sudo privileges: {e}")
        sys.exit(1)
