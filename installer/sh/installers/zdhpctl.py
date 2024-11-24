from sh.runners.interactive import run_interactive
from state.execution import ExecutionState


def install_zdhpctl(
    state: ExecutionState
) -> None:
    run_interactive(['yay', '-S', 'zdhpctl'], state)
