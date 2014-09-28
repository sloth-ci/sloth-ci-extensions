'''SSH executor for Sloth CI app extension that replaces the default executor and runs actions on a remote host (or multiple hosts) via SSH.

Config params::

    [ssh_exec]
    ;Hosts, comma-delimited. Optional port number can be provided after ':' (if not specified, 22 is used).
    hosts = ssh.example.com, myserver.com:23

    ;Username to use for authentication.
    username = admin

    ;Password to use for authentication or to unlock a private key.
    password = foobar

    ;Private key files. If not specified, only the keys from the default location are loaded (i.e. ~/.ssh).
    keys = ~/my_ssh_keys/key_rsa, somekey

Username and password config params are optional.
'''


__title__ = 'sloth-ci.ext.ssh_exec'
__description__ = 'SSH executor app extension for Sloth CI'
__version__ = '0.0.1'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


from paramiko import SSHClient
from urllib.parse import urlparse


def extend(cls):
    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            self._ssh_config = self.config['ssh_exec']

            self._ssh_client = SSHClient()

            self.processing_logger.debug('Loading system host keys.')
            self._ssh_client.load_system_host_keys()

            keys = self._ssh_config.get('keys')

            if keys:
                self.processing_logger.debug('Loading additional host keys: %s' % keys)
                
                for key in (keys,):
                    self._ssh_client.load_host_keys(key)

        def execute(self, action):
            '''Execute an action on a remote host (or hosts).

            :param action: action to be executed

            :returns: True if successful, Exception otherwise
            '''

            self.processing_logger.info('Executing action: %s', action)
            
            for host in (self._ssh_config.get('hosts'),):
                try:
                    hostname, port = host.split(':')[0], 22

                    username = self._ssh_config.get('username')
                    password = self._ssh_config.get('password')

                    self.processing_logger.debug('Connecting to %s:%d with username %s (password %s)' % (hostname, port, username, password))

                    self._ssh_client.connect(
                        hostname=hostname,
                        port=port,
                        username=username,
                        password=password,
                    )

                    stdin, stdout, stderr = self._ssh_client.exec_command(action)

                    for log in stdout:
                        self.processing_logger.debug('%s', log)

                    self.processing_logger.info('Action executed: %s', action)
                    return True

                except Exception:
                    raise

    return Sloth