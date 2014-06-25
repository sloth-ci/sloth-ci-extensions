"""Sloth CI extension that adds a logger (can be rotating and timed rotating) to Sloth CI apps.

Config params::

    [logs]
    ;Directory to store the logs. If missing, current directory is used.
    log_dir = logs

    ;Logging level. Can be either a numeric value (e.g. 10) or a level name (e.g. DEBUG). If missing, Sloth CI's defalt is used (20, INFO). Refer to https://docs.python.org/3.4/library/logging.html#levels.
    level = 10

    ;Log message format. If missing, the default format is used: %(asctime)s | %(name)30s | %(levelname)10s | %(message)s
    format = %(asctime)s - %(name)s - %(levelname)s - %(message)s

    ;Rotating or not. If missing, False is considered.
    rotating = True

    ;Rotating log param. Max filesize before the log is rotated. If missing, 0 is considered, i.e. never rotated.
    max_bytes = 500

    ;Rotating log param. Max number of log files. If missing, 0 is considered, i.e. unlimited.
    backup_count = 10

All config params are optional.
"""


__title__ = 'sloth-ci.ext.logs'
__description__ = 'Logs for Sloth CI apps'
__version__ = '1.0.2'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


from os.path import abspath, join

import logging
import logging.handlers


def extend(cls):
    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)
            
            log_config = self.config.get('logs') or {}

            log_dir = log_config.get('log_dir') or '.'

            log_formatter = logging.Formatter(
                log_config.get('format') or '%(asctime)s | %(name)30s | %(levelname)10s | %(message)s'
            )
            
            if log_config.get('rotating'):
                file_handler = logging.handlers.RotatingFileHandler(
                    abspath(join(log_dir, self.name + '.log')),
                    'a+',
                    maxBytes=log_config.get('max_bytes') or 0,
                    backupCount=log_config.get('backup_count') or 0
                )
            else:
                file_handler = logging.FileHandler(abspath(join(log_dir, self.name + '.log')), 'a+')

            file_handler.setFormatter(log_formatter)

            self.logger.addHandler(file_handler)

            if log_config.get('level'):
                self.logger.setLevel(log_config.get('level'))

    return Sloth
