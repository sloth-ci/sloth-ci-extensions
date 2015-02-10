'''Sloth CI extension that adds a file logger (can be rotating and timed rotating) to Sloth CI apps.

Formerly known as "sloth-ci.ext.logs."

Extension params::
    
    # Use the module sloth-ci.ext.file-logs.
    module: file_logs

    # Set the log path. Default is the current dir.
    path: debug_logs
    
    # Log filename. If not given, slug of the app's listen point will be used.
    filename: test_debug.log

    # Log level (number or valid Python logging level name).
    level: DEBUG

    # Log format (refer to the Python logging module documentation). The default value is given below. 
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
__version__ = '1.0.9'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend(cls, extension):
    from os.path import abspath, join, exists
    from os import makedirs

    import logging
    import logging.handlers

    from slugify import slugify


    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)
            
            log_config = extension['config']
            
            log_dir = log_config.get('path', '.')
            log_filename = log_config.get('filename', slugify(self.listen_point) + '.log')

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
            super().stop()
            self.logger.removeHandler(self.log_handlers.pop(extension['name']))


    return Sloth
