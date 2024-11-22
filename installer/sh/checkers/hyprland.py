from sh.command import execute_command


def is_hyprland_installed() -> bool:
    """
    Check if Hyprland is already installed on the system.
    Returns True if installed, otherwise False.
    """
    try:
        execute_command(["hyprctl", "version"])
        return True
    except (Exception,) as e:
        return False
