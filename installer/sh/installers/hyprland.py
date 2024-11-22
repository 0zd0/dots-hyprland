from sh.command import execute_command
from sh.runners.interactive import run_interactive
from state.execution import ExecutionState


def install_hyprland(
    state: ExecutionState
) -> None:
    run_interactive(['yay', '-S', 'hyprland'], state)
