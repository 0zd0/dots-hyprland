from loader import execution_state
from sh.checkers.yay import is_yay_installed
from sh.installers.yay import install_yay
from sh.runners.interactive import run_interactive
from steps.info import start_info

from steps.options import set_options
from utils.sudo import check_sudo_privileges


def install():
    check_sudo_privileges()

    start_info()
    set_options(execution_state)
    run_interactive(['sudo', 'pacman', '-Syu'], execution_state)

    if not is_yay_installed():
        install_yay()


if __name__ == '__main__':
    install()
