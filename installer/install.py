from pathlib import Path

from loader import execution_state
from sh.checkers.yay import is_yay_installed
from sh.installers.pkg import install_local_pkgbuild
from sh.installers.yay import install_yay
from sh.runners.interactive import run_interactive
from steps.info import start_info

from steps.options import set_options
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


if __name__ == '__main__':
    install()
