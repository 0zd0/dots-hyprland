import sys

from loguru import logger

from state.execution import ExecutionState

logger.remove()
logger.level("PRINT", no=0, color='<white>')
logger.add(
    sys.stdout,
    format="<green>{time:DD-MM-YYYY HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "<level>{message}</level>",
)
logger.add(
    sys.stdout,
    format="{message}",
    level='PRINT',
    filter=lambda record: record["level"].no == 0,
)
log = logger

execution_state = ExecutionState(ask=True)
