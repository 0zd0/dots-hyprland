import os
from pathlib import Path
from typing import Set

from pydantic import BaseModel
from environs import Env

env = Env()

XDG_CONFIG_HOME = env.str('XDG_CONFIG_HOME', default='~/.config')
HOME_CONFIGS_FULL_PATH = os.path.expanduser(XDG_CONFIG_HOME)
PROJECT_CONFIG_PATH = '../../.config'
DEFAULT_EXCLUDE = {'~', '___jb_', '.tmp', 'node_modules'}
HYPRLAND_CONFIG_NAME = 'hypr'


class SyncPair(BaseModel):
    source: Path
    target: Path
    excludes: Set[str]


config = [
    SyncPair(
        source=Path(os.path.abspath(f'{PROJECT_CONFIG_PATH}/{HYPRLAND_CONFIG_NAME}')),
        target=Path(os.path.join(HOME_CONFIGS_FULL_PATH, HYPRLAND_CONFIG_NAME)),
        excludes={*DEFAULT_EXCLUDE, 'local'}
    )
]
