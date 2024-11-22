import subprocess
from typing import Union, List


def execute_command(cmd: Union[str, List[str]]) -> subprocess.CompletedProcess:
    """
    Executes a command and streams its output in real-time.

    Args:
        cmd (Union[str, List[str]]): The command to execute, either as a string or a list of arguments.

    Returns:
        subprocess.CompletedProcess: The result of the executed command.
    """
    print(cmd)
    process = subprocess.Popen(
        cmd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=isinstance(cmd, str)
    )

    stdout_lines = []
    stderr_lines = []

    # Stream output in real-time
    for line in process.stdout:
        print(line, end="")  # Print stdout in real-time
        stdout_lines.append(line)

    for line in process.stderr:
        print(line, end="")  # Print stderr in real-time
        stderr_lines.append(line)

    process.wait()

    # Collect result for return
    return subprocess.CompletedProcess(
        args=cmd,
        returncode=process.returncode,
        stdout="".join(stdout_lines),
        stderr="".join(stderr_lines)
    )


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
