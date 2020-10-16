"""veikkaaja module, here we set up the logging"""
import sys
import logging
import logging.handlers
from datetime import datetime

logging_initialized = False

if not logging_initialized:
    logger = logging.getLogger('veikkaaja')
    logger.setLevel(logging.INFO)

    class NiceFormatter(logging.Formatter):
        def format(self, record):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"[{record.levelname:>6} ] {current_time} | {record.msg}"

    sys_out_handler = logging.StreamHandler(sys.stdout)
    sys_out_handler.setFormatter(NiceFormatter())

    logger.addHandler(sys_out_handler)

    logging.root = logger

    logging_initialized = True
