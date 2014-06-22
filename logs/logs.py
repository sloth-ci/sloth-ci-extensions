__title__ = 'sloth-ci.ext.logs'
__description__ = 'Logs for Sloth CI apps'
__long_desciption__ = 'Sloth CI extension that adds a logger (can be rotating) to Sloth CI apps.'
__version__ = '0.0.4'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


"""Sloth CI extension that adds a logger (can be rotating and timed rotating) to Sloth CI apps."""


from os.path import abspath, join

import logging


def extend(cls):
    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)
            
            log_config = self.config.get('logs') or {}

            formatter = logging.Formatter(
                log_config.get('format') or '%(asctime)s | %(name)30s | %(levelname)10s | %(message)s'
            )
            
            if log_config.get('rotating'):
                file_handler = logging.handlers.RotatingFileHandler(
                    abspath(join(self.config['log_dir'], self.name + '.log')),
                    'a+',
                    maxBytes=log_config.get('max_bytes') or 0,
                    backupCount=self.log_config.get('backup_count') or 0
                )
            else:
                file_handler = logging.FileHandler(abspath(join(self.config['log_dir'], self.name + '.log')), 'a+')

            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
    
    return Sloth
