"""Module for custom logger"""
import logging
import sys
import os

# pylint: disable=too-few-public-methods


class DebugFormatter(logging.Formatter):
    """Formatting for debug"""

    def __init__(self):
        super().__init__('%(asctime)s  |  %(levelno)-2d  '
            '|  %(name)s  |  %(message)s')


class StdoutFormatter(logging.Formatter):
    """Formatting for stdout"""

    def __init__(self):
        super().__init__('%(message)s')


class StderrFormatter(logging.Formatter):
    """Formatting for stderr"""

    def __init__(self):
        super().__init__('[%(levelname)s] %(message)s')


class DebugFilter(logging.Filter):
    """Filter for debug"""

    def filter(self, record):
        """Returns true if record is DEBUG or higher"""

        return record.levelno >= logging.DEBUG


class StdoutFilter(logging.Filter):
    """Filter for stdout"""

    def filter(self, record):
        """Returns true if record is INFO"""

        _lower = record.levelno >= logging.INFO
        _upper = record.levelno < logging.WARNING
        return _lower and _upper


class StderrFilter(logging.Filter):
    """Filter for stderr"""

    def filter(self, record):
        """Returns true if record is WARNING or higher"""

        return record.levelno >= logging.WARNING


class DebugHandler(logging.FileHandler):
    """Event handler for debug"""

    def __init__(self):
        super().__init__('logs/debug.log', mode="w")
        self.setFormatter(DebugFormatter())
        self.addFilter(DebugFilter())


class StdoutHandler(logging.StreamHandler):
    """Event handler for stdout"""

    def __init__(self):
        super().__init__(sys.stdout)
        self.setFormatter(StdoutFormatter())
        self.addFilter(StdoutFilter())


class StderrHandler(logging.StreamHandler):
    """Event handler for stderr"""

    def __init__(self):
        super().__init__(sys.stderr)
        self.setFormatter(StderrFormatter())
        self.addFilter(StderrFilter())


class Logger:
    """Custom logger"""

    RUNNING = False

    def __init__(self, alias, level=logging.DEBUG):
        (self.alias, self.level) = (alias, level)
        self.logger = logging.getLogger(self.alias)
        self.logger.setLevel(self.level)
        if not self.RUNNING:
            os.makedirs("logs", exist_ok=True)
            self.logger.addHandler(StdoutHandler())
            self.logger.addHandler(StderrHandler())
            self.logger.addHandler(DebugHandler())
            Logger.RUNNING = True

    def get_logger(self, alias):
        """Returns child logger"""

        return Logger('.'.join([self.alias, alias]))

    def debug(self, *args, **kwargs):
        """Logs debug messages"""

        self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        """Logs info messages"""

        self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        """Logs warning messages"""

        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        """Logs error messages"""

        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        """Logs critical messages"""

        self.logger.critical(*args, **kwargs)


LOGGER = Logger('root', 10)
