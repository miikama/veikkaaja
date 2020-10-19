"""
veikkaaja module, here we set up the logging

export VEIKKAAJA_DEBUG=1 environment variable to
set the log level to logging.DEBUG.
"""
import logging
import logging.handlers
import os
import sys
from datetime import datetime

__version__ = "0.1.0"

LOGGING_INITIALIZED = False

if not LOGGING_INITIALIZED:
    logger = logging.getLogger('veikkaaja')

    logger.setLevel(logging.INFO)
    if os.environ.get('VEIKKAAJA_DEBUG', False):
        logger.setLevel(logging.DEBUG)

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
