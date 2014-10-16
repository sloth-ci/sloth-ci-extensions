'''OpenVZ executor for Sloth CI app extension that replaces the default executor and runs actions inside a given OpenVZ container.

Config params::

    [openvz_exec]
    ;Container id.
    ctid = 123
'''


__title__ = 'sloth-ci.ext.openvz_exec'
__description__ = 'OpenVZ executor app extension for Sloth CI'
__version__ = '1.0.1'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend(cls):
    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            self._openvz_config = self.config['openvz_exec']
            self._openvz_ctid = self._openvz_config['ctid']

        def process_queue(self, params):
            self.processing_logger.debug('Starting OpenVZ container %d' % self._openvz_ctid)
            openvz_start_command = 'vzctl start %d' % self._openvz_ctid
            super().execute(openvz_start_command)
            
            super().process_queue()
            
            self.processing_logger.debug('Stopping OpenVZ container %d' % self._openvz_ctid)
            openvz_stop_command = 'vzctl stop %d' % self._openvz_ctid
            super().execute(openvz_stop_command)

        def execute(self, action):
            '''Execute an action inside an OpenVZ container. The container must exist and be running.

            :param action: action to be executed

            :returns: True if successful, Exception otherwise
            '''

            try:
                ctid = self._openvz_config['ctid']

                openvz_exec_command = 'vzctl exec %d' % ctid

                super().execute(openvz_exec_command + ' ' + action)

                return True

            except Exception:
                raise

    return Sloth