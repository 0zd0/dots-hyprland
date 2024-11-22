from sh.command import execute_command


def is_yay_installed() -> bool:
    """
    Check if Yay is already installed on the system.
    Returns True if installed, otherwise False.
    """
    try:
        execute_command(["yay", "--version"])
        return True
    except (Exception,) as e:
        return False
