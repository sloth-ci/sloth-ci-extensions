'''OpenVZ executor for Sloth CI app extension that replaces the default executor and runs actions inside a given OpenVZ container.

Config params::

    # Use the sloth-ci.ext.openvz_exec module.
    module: openvz_exec

    # Container name.
    container_name = foo
        
    # Container ID.
    # container_id = 123

If name is provided, ID is ignored. If name is not provided, ID is mandatory.
'''


__title__ = 'sloth-ci.ext.openvz_exec'
__description__ = 'OpenVZ executor app extension for Sloth CI'
__version__ = '1.0.2'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend(cls, extension):
    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            self._openvz_config = self.config['extensions'][extension]

        def execute(self, action):
            '''Execute an action inside an OpenVZ container. The container must exist and be running.

            :param action: action to be executed

            :returns: True if successful, Exception otherwise
            '''

            try:
                container_name = self._openvz_config.get('container_name')

                if container_name:
                    openvz_exec_command = 'vzctl exec %s' % container_name

                else:
                    container_id = self._openvz_config['container_id']
                    
                    openvz_exec_command = 'vzctl exec %d' % container_id

                super().execute(openvz_exec_command + ' ' + action)

                return True

            except Exception:
                raise

    return Sloth