import subprocess
import sys
from typing import Union, List


def execute_command(cmd: Union[str, List[str]]) -> subprocess.CompletedProcess:
    """
    Executes a command and streams its output in real-time.

    Args:
        cmd (Union[str, List[str]]): The command to execute, either as a string or a list of arguments.

    Returns:
        subprocess.CompletedProcess: The result of the executed command.
    """
    process = subprocess.Popen(
        cmd,
        shell=isinstance(cmd, str),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    stdout_lines = []
    stderr_lines = []

    for line in process.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        stdout_lines.append(line)

    for line in process.stderr:
        sys.stdout.write(line)
        sys.stdout.flush()
        stderr_lines.append(line)

    process.wait()

    completed_process = subprocess.CompletedProcess(
        args=cmd,
        returncode=process.returncode,
        stdout="".join(stdout_lines),
        stderr="".join(stderr_lines)
    )

    if process.returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=process.returncode,
            cmd=cmd,
            output=completed_process.stdout,
            stderr=completed_process.stderr
        )

    return completed_process


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
