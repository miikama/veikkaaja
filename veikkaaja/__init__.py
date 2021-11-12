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

__version__ = "0.1.3"

LOGGING_INITIALIZED = False

if not LOGGING_INITIALIZED:
    # pylint: disable=invalid-name
    logger = logging.getLogger('veikkaaja')

    logger.setLevel(logging.INFO)
    try:
        if 'VEIKKAAJA_DEBUG' in os.environ and int(os.environ['VEIKKAAJA_DEBUG']) > 0:
            logger.setLevel(logging.DEBUG)
    except ValueError:
        pass

    class NiceFormatter(logging.Formatter):
        """Format: [  INFO ] 2020-10-17 10:42:41 | The message."""

        def format(self, record):
            record.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return super().format(record)

    # pylint: disable=invalid-name
    sys_out_handler = logging.StreamHandler(sys.stdout)
    sys_out_handler.setFormatter(
        NiceFormatter(fmt="[%(levelname)7s ] %(current_time)s | %(message)s"))

    logger.addHandler(sys_out_handler)

    LOGGING_INITIALIZED = True
