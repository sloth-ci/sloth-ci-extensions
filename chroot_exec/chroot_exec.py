'''Chroot executor Sloth CI app extension that replaces the default executor and changes the root directory before running actions.

Config params::

    [chroot_exec]
    ;Path to change the root directory of the current process to.
    path = ~/somepath
'''


__title__ = 'sloth-ci.ext.chroot_exec'
__description__ = 'Chroot executor extension for Sloth CI'
__version__ = '0.0.2'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


from os import chroot


def extend(cls):
    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            chroot_config = self.config.get('chroot_exec')

            self.path = chroot_config.get('path')

        def execute(self, action):
            self.processing_logger.debug('Changing the root directory to %s' % self.path)
            chroot(self.path)

            super().execute(action)
    
    return Sloth
