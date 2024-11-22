from sh.runners.interactive import run_interactive
from state.execution import ExecutionState


def set_gnome_font(
        state: ExecutionState
) -> None:
    run_interactive(['gsettings', 'set', 'org.gnome.desktop.interface', 'font-name', "'Rubik 11'"], state)


def set_gnome_dark_theme(
        state: ExecutionState
) -> None:
    run_interactive(
        ['gsettings', 'set', 'org.gnome.desktop.interface', 'color-scheme', "'prefer-dark'"],
        state
    )
