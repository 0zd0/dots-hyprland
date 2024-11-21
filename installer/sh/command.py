import subprocess
from typing import Union, List


def execute_command(cmd: Union[str, List[str]]) -> subprocess.CompletedProcess[str]:
    """
    Executes a command and streams its output in real-time.

    Args:
        cmd (List[str]): The command to execute as a list of arguments.
    """
    return subprocess.run(cmd, check=True, text=True, bufsize=0, shell=isinstance(cmd, str))


def try_command(cmd: Union[str, List[str]]) -> subprocess.CompletedProcess[str]:
    """
    Attempts to execute a shell command

    Args:
        cmd (Union[str, List[str]]): Command to execute as a string or list.
    """
    try:
        return execute_command(cmd)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
