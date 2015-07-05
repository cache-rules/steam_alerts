# Copyright 2015 jydo inc. All rights reserved.
import logging
import sys


class SingleLevelFilter(logging.Filter):
    def __init__(self, pass_level, reject):
        self.pass_level = pass_level
        self.reject = reject

    def filter(self, record):
        if self.reject:
            return (record.levelno != self.pass_level)
        else:
            return (record.levelno == self.pass_level)

formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')
logger = logging.getLogger('steam_alerts')
logger.setLevel(logging.DEBUG)
logger.propagate = 0

# Configure a StreamHandler to output all logs but errors to stdout.
stdout_filter = SingleLevelFilter(logging.ERROR, True)
stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.setFormatter(formatter)
stdout_handler.addFilter(stdout_filter)
logger.addHandler(stdout_handler)

# Configure a StreamHandler to output errors to stderr.
stderr_filter = SingleLevelFilter(logging.ERROR, False)
stderr_handler = logging.StreamHandler(stream=sys.stderr)
stderr_handler.setFormatter(formatter)
stderr_handler.addFilter(stderr_filter)
logger.addHandler(stderr_handler)
