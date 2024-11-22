import os
import pty
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

    master_fd, slave_fd = pty.openpty()
    process = subprocess.Popen(
        cmd,
        shell=isinstance(cmd, str),
        stdin=sys.stdin,
        stdout=slave_fd,
        stderr=slave_fd,
        text=True,
    )

    os.close(slave_fd)

    try:
        while True:
            try:
                output = os.read(master_fd, 1024).decode('utf-8', errors='replace')
                if output:
                    sys.stdout.write(output)
                    sys.stdout.flush()
            except OSError:
                break
    finally:
        os.close(master_fd)

    process.wait()
    return process.returncode


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
