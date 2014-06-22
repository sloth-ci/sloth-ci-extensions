__title__ = 'sloth-ci.ext.html-logs'
__description__ = 'HTML logs for Sloth CI apps'
__long_desciption__ = 'Sloth CI extension that adds a HTML logger to Sloth CI apps.'
__version__ = '1.0.1'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


"""Sloth CI extension that adds an extra HTML logger to Sloth CI apps."""


from os.path import abspath, join

import logging


def extend(cls):
    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            html_file_handler = logging.FileHandler(abspath(join(self.config['log_dir'], self.name + '.html')), 'a+')

            html_formatter = logging.Formatter(
'''<tr>
    <td class="timestamp">%(asctime)s</td>
    <td class="name">%(name)s</td>
    <td class="level">%(levelname)s</td>
    <td class="message">%(message)s</td>
</tr>'''
            )

            html_file_handler.setFormatter(html_formatter)

            self.logger.addHandler(html_file_handler)
    
    return Sloth
