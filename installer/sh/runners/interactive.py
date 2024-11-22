from typing import List
from enum import Enum
from colorama import Fore, Style

from loader import log
from sh.runners.with_retry import run_with_retry
from state.execution import ExecutionState


class UserAction(Enum):
    YES = "y"
    EXIT = "e"
    SKIP = "s"
    YES_FOR_ALL = "yesforall"


PROMPT_DESCRIPTIONS = {
    UserAction.YES: "Yes",
    UserAction.EXIT: "Exit now",
    UserAction.SKIP: "Skip this command (NOT recommended - your setup might not work correctly)",
    UserAction.YES_FOR_ALL: "Yes and don't ask again; NOT recommended unless you're really sure",
}


def run_interactive(command: List[str], state: ExecutionState) -> None:
    """
    Executes a command interactively with user confirmation and colorful output.

    :param command: The command to execute as a list of arguments.
    :param state: Shared execution state containing the `ask` flag.
    :return:
    """
    log.info("#" * 52)
    log.info('Next command:')
    log.success(" ".join(command))

    execute = True

    if state.ask:
        def execute_action():
            log.info('Executing...')

        def exit_action():
            log.info('Exiting...')
            exit(0)

        def skip_action():
            nonlocal execute
            log.info('Skipping this one...')
            execute = False

        def yes_for_all_action():
            log.info("Won't ask again.")
            state.ask = False

        actions = {
            UserAction.YES: execute_action,
            UserAction.EXIT: exit_action,
            UserAction.SKIP: skip_action,
            UserAction.YES_FOR_ALL: yes_for_all_action,
        }

        while True:
            log.info("Execute?")
            for action, description in PROMPT_DESCRIPTIONS.items():
                log.log('PRINT', f"{Fore.YELLOW}{action.value}{Style.RESET_ALL} = {description}")

            user_input = input(Fore.BLUE + "====> ").strip().lower()

            try:
                selected_action = UserAction(user_input)
                actions[selected_action]()
                break
            except ValueError:
                log.error("Please enter a valid option: [y/e/s/yesforall].")

    if execute:
        run_with_retry(command)
    else:
        log.warning(f"Skipped command: {" ".join(command)}")
