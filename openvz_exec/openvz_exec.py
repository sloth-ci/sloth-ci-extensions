'''Run actions inside an `OpenVZ <http://openvz.org>`__ container.


Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.ext.openvz_exec


Usage
-----

.. code-block:: yaml
    :caption: openvz_exec.yml

    extensions:
        run_in_openvz:
            # Use the sloth_ci.ext.openvz_exec module.
            module: openvz_exec

            # Container name.
            container_name: foo

            # Container ID.
            # container_id: 123

If ``container_name`` is provided, ``container_id`` is ignored. If ``container_name`` is *not* provided, ``container_id`` is mandatory.
'''


__title__ = 'sloth-ci.ext.openvz_exec'
__description__ = 'OpenVZ executor for Sloth CI'
__version__ = '1.0.5'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend_sloth(cls, extension):
    '''Replace the default ``execute`` method with the OpenVZ-based one.'''

    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            self._openvz_config = extension['config']

        def execute(self, action):
            '''Execute an action inside an OpenVZ container. The container must exist and must be running.

            :param action: action to be executed

            :returns: True if the execution was successful; raises exception otherwise
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
