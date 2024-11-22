from pathlib import Path

from loader import execution_state
from sh.checkers.hyprland import is_hyprland_installed
from sh.checkers.yay import is_yay_installed
from sh.installers.hyprland import install_hyprland
from sh.installers.pkg import install_local_pkgbuild
from sh.installers.yay import install_yay
from sh.runners.interactive import run_interactive
from steps.folder import create_folders
from steps.gnome import set_gnome_font
from steps.info import start_info

from steps.options import set_options
from steps.user import add_user_to_groups
from utils.env import XDG_BIN_HOME, XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_DATA_HOME
from utils.sudo import check_sudo_privileges

META_PACKAGES_PATH = './arch-packages'
META_PACKAGES_PREFIX = 'zd-dots-hyprland'
META_PACKAGE_NAMES = [
    'basic',
    'audio',
    'screen',
    'widgets',
]


def install():
    check_sudo_privileges()
    start_info()
    set_options(execution_state)
    run_interactive(['sudo', 'pacman', '-Syu'], execution_state)

    if not is_yay_installed():
        install_yay()

    for name in META_PACKAGE_NAMES:
        install_flags = ['--needed']
        if not execution_state.ask:
            install_flags.append('--noconfirm')
        install_local_pkgbuild(
            Path(f"{META_PACKAGES_PATH}/{META_PACKAGES_PREFIX}-{name}"),
            install_flags,
            execution_state
        )

    if not is_hyprland_installed():
        install_hyprland(execution_state)

    add_user_to_groups(execution_state)
    # TODO: understand whether this is necessary for my use
    # bash -c "echo i2c-dev | sudo tee /etc/modules-load.d/i2c-dev.conf"
    # systemctl --user enable ydotool --now
    set_gnome_font(execution_state)

    create_folders(
        [
            XDG_BIN_HOME,
            XDG_CACHE_HOME,
            XDG_CONFIG_HOME,
            XDG_DATA_HOME,
        ],
        execution_state
    )


if __name__ == '__main__':
    install()
