__title__ = 'sloth-ci.ext.html-logs'
__version__ = '0.0.2'
__author__ = 'Konstantin Molchanov'
__license__ = 'MIT'


"""This Sloth CI extension adds an extra HTML logger to Sloth CI apps."""


import logging


def extend(cls):
    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            html_file_handler = logging.FileHandler(abspath(join(self.config['log_dir'], self.name + '.html')), 'a+')

            html_formatter = logging.Formatter(
'''<tr>
    <td class="timestamp">%(asctime)s</td>
    <td class="name">%(name)20s</td>
    <td class="level">%(levelname)10s</td>
    <td class="message">%(message)s</td>
</tr>'''
            )

            html_file_handler.setFormatter(html_formatter)

            self.logger.addHandler(html_file_handler)
    
    return Sloth
