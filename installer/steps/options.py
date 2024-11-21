import sys
from enum import Enum

from colorama import Fore, Style

from loader import log
from state.execution import ExecutionState


class UserAction(Enum):
    YES = "y"
    NO = "n"
    ABORT = "a"


PROMPT_DESCRIPTIONS = {
    UserAction.YES: "Yes, ask me before executing each of them. (DEFAULT)",
    UserAction.NO: "No, just execute them automatically",
    UserAction.ABORT: "Abort",
}


def set_options(state: ExecutionState):
    def no():
        state.ask = False

    def yes():
        state.ask = True

    def abort():
        exit(1)

    actions = {
        UserAction.YES: yes,
        UserAction.NO: no,
        UserAction.ABORT: abort,
    }

    while True:
        log.info('Do you want to confirm every time before a command executes?')
        for action, description in PROMPT_DESCRIPTIONS.items():
            log.log('PRINT', f"{Fore.YELLOW}{action.value}{Style.RESET_ALL} = {description}")

        user_input = input(Fore.BLUE + "====> ").strip().lower()

        try:
            selected_action = UserAction(user_input)
            actions[selected_action]()
            break
        except ValueError:
            log.error("Please enter a valid option: [y/n/a].")
