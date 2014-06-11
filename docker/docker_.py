__title__ = 'sloth-ci.ext.docker'
__version__ = '0.1.0'
__author__ = 'Konstantin Molchanov'
__license__ = 'MIT'


from docker import Client, APIError


def extend(cls):
    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            self.docker_client = Client(self.config['docker'].get('base_url'))

            self.image = self.config['docker'].get('image') or self.name

        def execute(self, action):
            """Execute an action inside a container, then commit the changes to the image and remove the container.

            :param action: action to be executed

            :returns: True if successful, Exception otherwise
            """

            self.processing_logger.info('Executing action: %s', action)

            try:
                try:
                    container_id = self.docker_client.create_container(
                        self.image,
                        command=action,
                        working_dir=self.config.get('work_dir') or '.'
                    )['Id']

                except APIError as e:
                    if e.response.status_code == 404:
                        self.docker_client.build(
                            self.config['docker'].get('path_to_dockerfile') or '.',
                            tag=self.image
                        )

                        container_id = self.docker_client.create_container(
                            self.image,
                            command=action,
                            working_dir=self.config['work_dir']
                        )['Id']

                    else:
                        raise

                self.docker_client.start(container_id)
                self.docker_client.commit(
                    container_id,
                    self.image,
                    message=action
                )
                self.docker_client.remove_container(container_id)

                self.processing_logger.info('Action executed: %s', action)
                return True

            except Exception:
                raise

    return Sloth