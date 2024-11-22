from pathlib import Path
from typing import List

from loader import log
from sh.runners.interactive import run_interactive
from state.execution import ExecutionState


def sync_configs(
        source_dir: Path,
        target_dir: Path,
        state: ExecutionState,
        excluded: List[str] | None = None,
) -> None:
    """
    Synchronizes configuration files from the source directory to the target directory.

    :param source_dir: Path to the source directory containing configuration files.
    :param target_dir: Path to the target directory where files will be synchronized.
    :param state: Execution state object for handling logging and interactive commands.
    :param excluded: List of directory names to exclude from synchronization. Defaults to None.
    :return: None
    """
    if not source_dir.is_dir():
        return log.error(f"Source directory '{source_dir}' does not exist or is not a directory.")

    for item in source_dir.iterdir():
        if excluded and item.name in excluded:
            continue

        target_path = target_dir / item.name
        log.info(f"Found target: {item}")

        if item.is_dir():
            run_interactive(
                ["rsync", "-av", "--delete", f"{item}/", f"{target_path}/"],
                state
            )
        elif item.is_file():
            run_interactive(
                ["rsync", "-av", str(item), str(target_path)],
                state
            )


def sync_hyprland_config(
    source_config: Path,
    target_config: Path,
    state: ExecutionState,
    hyprland_conf_name: str = "hyprland.conf",
    custom_dir_name: str = "custom"
) -> bool:
    """
    Synchronizes and manages Hyprland configuration files.

    :param source_config:
    :param target_config:
    :param state:
    :param hyprland_conf_name:
    :param custom_dir_name:
    :return: existed_hypr_conf
    """
    run_interactive(
        [
            "rsync",
            "-av",
            "--delete",
            f"--exclude=/{custom_dir_name}",
            f"--exclude=/{hyprland_conf_name}",
            f"{source_config}/",
            f"{target_config}/",
        ],
        state
    )
    hyprland_conf = target_config / hyprland_conf_name

    if hyprland_conf.is_file():
        log.info(f'"{hyprland_conf}" already exists.')
        run_interactive(
            [
                "cp",
                "-f",
                str(source_config / hyprland_conf_name),
                f"{hyprland_conf}.new",
            ],
            state
        )
        existed_hypr_conf = True
    else:
        log.warning(f'"{hyprland_conf}" does not exist yet.')
        run_interactive(
            [
                "cp",
                str(source_config / hyprland_conf_name),
                str(hyprland_conf),
            ],
            state
        )
        existed_hypr_conf = False

    custom_dir = target_config / custom_dir_name
    if custom_dir.is_dir():
        log.info(f'"{custom_dir}" already exists, will not do anything.')
    else:
        log.warning(f'"{custom_dir}" does not exist yet.')
        run_interactive(
            [
                "rsync",
                "-av",
                "--delete",
                f"{source_config / custom_dir_name}/",
                f"{custom_dir}/",
            ],
            state
        )

    return existed_hypr_conf
