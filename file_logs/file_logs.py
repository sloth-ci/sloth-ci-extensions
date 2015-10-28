'''Add file logging to Sloth CI apps.

You can customize your logging in a number of ways: set the output dir and filename, set log level and format, toggle and configure log rotation.

Installation
------------

.. code-block:: bash
    
    $ pip install sloth-ci.ext.file_logs


Usage
-----

.. code-block:: yaml
    :caption: file_logs.yml

    extensions:
        logs:
            # Use the module sloth_ci.ext.file_logs.
            module: file_logs

            # Set the log path. Default is the current dir.
            path: debug_logs

            # Log filename. If not given, the app's listen point is used.
            filename: test_debug.log

            # Log level (number or valid Python logging level name).
            level: DEBUG

            # Log format (refer to the https://docs.python.org/3/library/logging.html#logrecord-attributes).
            # By default, this format is used: 
            # format: '%(asctime)s | %(name)30s | %(levelname)10s | %(message)s'

            # Make logs rotating. Default is false.
            # rotating: true

            # If rotating, maximum size of a log file in bytes.
            # max_bytes: 500

            # If rotating, maximum number or log files to keep.
            # backup_count: 10
'''


__title__ = 'sloth-ci.ext.file_logs'
__description__ = 'File logs for Sloth CI apps'
__version__ = '1.1.3'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend_sloth(cls, extension):
    '''Add a file handler to the default logger when the app is created and remove it when the app stops.'''

    from os.path import abspath, join, exists
    from os import makedirs

    import logging
    import logging.handlers


    class Sloth(cls):
        def __init__(self, config):
            '''Add a file handler to the app logger.'''

            super().__init__(config)

            log_config = extension['config']

            log_dir = log_config.get('path', '.')
            log_filename = log_config.get('filename', self.listen_point + '.log')

            if not exists(abspath(log_dir)):
                makedirs(abspath(log_dir))

            log_formatter = logging.Formatter(
                log_config.get('format') or '%(asctime)s | %(name)30s | %(levelname)10s | %(message)s'
            )

            if log_config.get('rotating'):
                file_handler = logging.handlers.RotatingFileHandler(
                    abspath(join(log_dir, log_filename)),
                    'a+',
                    maxBytes=log_config.get('max_bytes') or 0,
                    backupCount=log_config.get('backup_count') or 0
                )

            else:
                file_handler = logging.FileHandler(abspath(join(log_dir, log_filename)), 'a+')

            file_handler.setFormatter(log_formatter)

            file_handler.setLevel(log_config.get('level', logging.INFO))

            self.logger.addHandler(file_handler)

            self.log_handlers[extension['name']] = file_handler

        def stop(self):
            '''Remove the file handler when the app stops.'''

            super().stop()
            self.logger.removeHandler(self.log_handlers.pop(extension['name']))


    return Sloth
