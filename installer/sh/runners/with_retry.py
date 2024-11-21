import subprocess
from enum import Enum
from typing import List
from colorama import Fore, Style

from enums.command import CommandStatus
from loader import log
from sh.command import execute_command


class CommandAction(Enum):
    REPEAT = "r"
    EXIT = "e"
    IGNORE = "i"


ACTION_DESCRIPTIONS = {
    CommandAction.REPEAT: "Repeat this command (DEFAULT)",
    CommandAction.EXIT: "Exit now",
    CommandAction.IGNORE: "Ignore this error and continue (your setup might not work correctly)",
}


def run_with_retry(command: List[str]) -> None:
    """
    Executes a command with retry and error-handling options.

    Args:
        command (List[str]): The command to execute as a list of arguments.
    """
    cmd_status = CommandStatus.FAILED

    while cmd_status == CommandStatus.FAILED:
        try:
            execute_command(command)
            cmd_status = CommandStatus.SUCCESS
        except subprocess.CalledProcessError:
            log.error(f"Command \"{' '.join(command)}\" has failed.")
            log.warning("You may need to resolve the problem manually BEFORE repeating this command.")

            log.info("Options:")
            for action, description in ACTION_DESCRIPTIONS.items():
                log.log('PRINT', f"{Fore.YELLOW}{action.value}{Style.RESET_ALL} = {description}")

            user_input = input(f"{Fore.BLUE} [r/e/i]: {Style.RESET_ALL}").strip().lower()

            try:
                selected_action = CommandAction(user_input)
                if selected_action == CommandAction.IGNORE:
                    log.info("Alright, ignore and continue...")
                    cmd_status = 2
                elif selected_action == CommandAction.EXIT:
                    log.info("Alright, will exit.")
                    exit(1)
                else:
                    log.info("OK, repeating...")
            except ValueError:
                log.error("Invalid input. Please choose one of the available options.")

    if cmd_status == CommandStatus.SUCCESS:
        log.success(f"Command \"{' '.join(command)}\" finished.")
    elif cmd_status == CommandStatus.IGNORED:
        log.warning(f"Command \"{' '.join(command)}\" failed but was ignored by user.")

