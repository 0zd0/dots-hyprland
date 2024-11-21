import subprocess
from typing import Union, List


def execute_command(command: List[str]) -> int:
    """
    Executes a command and streams its output in real-time.

    Args:
        command (List[str]): The command to execute as a list of arguments.

    Returns:
        int: The return code of the executed command.
    """
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    for line in iter(process.stdout.readline, ""):
        print(line, end="")

    process.wait()
    return process.returncode


def try_command(cmd: Union[str, List[str]]) -> None:
    """
    Attempts to execute a shell command

    Args:
        cmd (Union[str, List[str]]): Command to execute as a string or list.
    """
    try:
        if isinstance(cmd, str):
            subprocess.run(cmd, shell=True, check=True)
        else:
            subprocess.run(cmd, check=True, text=True, bufsize=0)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
