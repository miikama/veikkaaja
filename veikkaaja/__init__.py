"""veikkaaja module, here we set up the logging"""
import logging
import logging.handlers
import sys
from datetime import datetime

LOGGING_INITIALIZED = False

if not LOGGING_INITIALIZED:
    logger = logging.getLogger('veikkaaja')
    logger.setLevel(logging.INFO)

    class NiceFormatter(logging.Formatter):
        """Format: [  INFO ] 2020-10-17 10:42:41 | The message."""

        def format(self, record):
            record.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return super().format(record)

    sys_out_handler = logging.StreamHandler(sys.stdout)
    sys_out_handler.setFormatter(
        NiceFormatter(fmt="[%(levelname)7s ] %(current_time)s | %(message)s"))

    logger.addHandler(sys_out_handler)

    LOGGING_INITIALIZED = True
