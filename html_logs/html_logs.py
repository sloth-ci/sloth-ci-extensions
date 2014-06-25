"""Sloth CI extension that adds an extra HTML logger to Sloth CI apps.

.. important::

    The extension outputs **only** the table rows and columns, **not a complete HTML document**. This output can then be embedded into an HTML document between ``<table>`` and ``<table/>``.

Each log field has its own CSS class:

log-timestamp
    Entry timestamp.

log-name
    Name of the logger posting the entry.

log-level
    Entry level, e.g. ``INFO``.

log-message
    Entry message.

Config params::

    [html_logs]
    ;Directory to store the HTML logs. If missing, current directory is used.
    log_dir = logs/html

    ;Rotating or not. If missing, False is considered.
    rotating = True

    ;Rotating log param. Max filesize before the log is rotated. If missing, 0 is considered, i.e. never rotated.
    max_bytes = 500

    ;Rotating log param. Max number of log files. If missing, 0 is considered, i.e. unlimited.
    backup_count = 10

All config params are optional.
"""


__title__ = 'sloth-ci.ext.html-logs'
__description__ = 'HTML logs for Sloth CI apps'
__version__ = '1.0.5'
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

            html_log_config = self.config.get('html_logs') or {}

            html_log_dir = html_log_config.get('log_dir') or '.'

            html_formatter = logging.Formatter(
"""<tr>
    <td class="log-timestamp">%(asctime)s</td>
    <td class="log-name">%(name)s</td>
    <td class="log-level">%(levelname)s</td>
    <td class="log-message">%(message)s</td>
</tr>"""
            )

            if html_log_config.get('rotating'):
                html_file_handler = logging.handlers.RotatingFileHandler(
                    abspath(join(html_log_dir, self.name + '.html')),
                    'a+',
                    maxBytes=html_log_config.get('max_bytes') or 0,
                    backupCount=html_log_config.get('backup_count') or 0
                )
            else:
                html_file_handler = logging.FileHandler(abspath(join(html_log_dir, self.name + '.html')), 'a+')

            html_file_handler.setFormatter(html_formatter)

            self.logger.addHandler(html_file_handler)
    
    return Sloth
