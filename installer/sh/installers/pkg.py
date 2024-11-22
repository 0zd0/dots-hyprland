import os
from pathlib import Path
import subprocess
from typing import List

from loader import log
from sh.runners.with_retry import run_with_retry
from state.execution import ExecutionState


def install_local_pkgbuild(
        location: Path,
        install_flags: List[str],
        execution_state: ExecutionState
) -> None:
    """
    Install a local PKGBUILD package.

    :param location:
    :param install_flags:
    :param execution_state:
    :return:
    """
    if not location.exists() or not location.is_dir():
        log.error(f"Error: Directory {location} does not exist.")
        return

    log.info(f"Processing {location}")
    current_dir = os.getcwd()
    try:
        os.chdir(location)
        run_with_retry(["yay", '-S', *install_flags, '--asdeps', *get_dependencies()])
        run_with_retry(["makepkg", '-si'] + (['--noconfirm'] if not execution_state.ask else []))
    finally:
        os.chdir(current_dir)


def get_dependencies() -> list[str]:
    """
    Parse dependencies from the PKGBUILD file.

    :return: List of dependencies.
    """
    pkgbuild = "PKGBUILD"
    if not Path(pkgbuild).exists():
        log.error(f"Error: PKGBUILD file not found")
        return []

    try:
        output = subprocess.check_output(
            f"source {pkgbuild} && echo ${'{'}depends[@]{'}'}",
            shell=True, executable="/bin/bash"
        )
        return output.decode().strip().split()
    except subprocess.CalledProcessError as e:
        log.error(f"Error parsing dependencies: {e}")
        return []
