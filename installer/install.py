from loader import execution_state
from steps.info import start_info
from colorama import init

# from sh.runners.interactive import run_interactive
from steps.options import set_options
from utils.sudo import check_sudo_privileges


init(autoreset=True)


def install():
    check_sudo_privileges()

    start_info()
    set_options(execution_state)

    # commands = [
    #     ["echo", "Hello, World!"],
    #     ["pacman", "-S", "pppp"],  # Эта команда вызовет ошибку
    #     ["ls", "-l"],  # Пример успешной команды
    # ]

    # for cmd in commands:
        # run_with_retry(cmd)
        # run_interactive(cmd, execution_state)


if __name__ == '__main__':
    install()
