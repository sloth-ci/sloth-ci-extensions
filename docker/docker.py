__title__ = 'sloth-ci.ext.docker'
__version__ = '0.0.6'
__author__ = 'Konstantin Molchanov'
__license__ = 'MIT'


from docker import Client as DockerClient


def extend(cls):
    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            self.docker_client = DockerClient()
            self.image = self.name

        def execute(self, action):
            """Execute an action inside a container, then commit the changes to the image and remove the container.

            :param action: action to be executed

            :returns: True if successful, Exception otherwise
            """

            self.processing_logger.info('Executing action: %s', action)

            try:
                try:
                    container_id = self.docker_client.create_container(self.image, command=action, workdir=self.config['work_dir'])['Id']

                except docker.APIError as e:
                    if e.response.status_code == 404:
                        self.docker_client.build(self.config['docker']['path_to_dockerfile'], tag=self.image)

                        container_id = self.docker_client.create_container(self.image, command=action, workdir=self.config['work_dir'])['Id']

                    else:
                        raise

                self.docker_client.start(container_id)
                self.docker_client.attach(container_id, logs=True)
                self.docker_client.commit(container_id, self.image)
                self.docker_client.remove_container(container_id)

                self.processing_logger.info('Action executed: %s', action)
                return True

            except Exception:
                raise

    return Sloth