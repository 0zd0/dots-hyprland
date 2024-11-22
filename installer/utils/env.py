from environs import Env

env = Env()

XDG_BIN_HOME = env.str('XDG_BIN_HOME', default='~/.local/bin')
XDG_CACHE_HOME = env.str('XDG_CACHE_HOME', default='~/.cache')
XDG_CONFIG_HOME = env.str('XDG_CONFIG_HOME', default='~/.config')
XDG_DATA_HOME = env.str('XDG_DATA_HOME', default='~/.local/share')
XDG_STATE_HOME = env.str('XDG_STATE_HOME', default='~/.local/state')
BACKUP_DIR = env.str('BACKUP_DIR', default='~/backup')
