from sh.runners.interactive import run_interactive
from state.execution import ExecutionState


def add_user_to_groups(
    state: ExecutionState
) -> None:
    run_interactive(
        ['sudo', 'usermod', '-aG', 'video,i2c,input', '"$(whoami)"'],
        state
    )
