from typing import List

from sh.runners.interactive import run_interactive
from state.execution import ExecutionState


def create_folders(
    folders: List[str],
    state: ExecutionState
) -> None:
    run_interactive(
        ['mkdir', '-p', *folders],
        state
    )
