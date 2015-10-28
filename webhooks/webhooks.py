'''Send POST requests on build events in Sloth CI apps.

Executing actions of an app is called *build*. A build is considered *completed* if all its actions were completed. If some actions were completed and some failed, it's a *partially completed*; if all actions fail, the build *failed*.

This extension sends POST requests when your builds complete (fully or partially) or fail; just pick the desired notification level and the target URL.


Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.ext.webhooks


Usage
-----

.. code-block:: yaml
    :caption: webhooks.yml

    extensions:
        webhooks:
            # Use the module sloth_ci.ext.webhooks.
            module: webhooks

            # Log level (number or valid Python logging level name).
            # ERROR includes only build fails, WARNING adds partial completions,
            # INFO adds completion, and DEBUG adds trigger notifications.
            # Default is WARNING.
            level: INFO

            # URL to send the requests to.
            url: http://example.com
'''


__title__ = 'sloth-ci.ext.webhooks'
__description__ = 'Webhooks for Sloth CI'
__version__ = '1.0.2'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


from logging import Handler
from json import dumps
from requests import post


class POSTHandler(Handler):
    '''Log handler that sends records in POST requests to a particular URL.

    :param url: URL to send the requests to.
    '''

    def __init__(self, url):
        super().__init__()

        self.url = url

    def emit(self, record):
        '''Send a log record in a POST request to the specified URL.
        
        :param record: the record to send
        '''

        try:
            payload = {
                'name': record.name, 
                'level': record.levelname,
                'message': record.getMessage()
            }

            post(self.url, json=dumps(payload))

        except Exception:
            self.handleError(record)


def extend_sloth(cls, extension):
    '''Add a POST handler to the default logger when the app is created and remove it when the app stops.'''

    from logging import WARNING

    class Sloth(cls):
        def __init__(self, config):
            '''Add a POST handler to the app logger.'''

            super().__init__(config)

            webhooks_config = extension['config']

            webhooks_handler = POSTHandler(webhooks_config['url'])

            webhooks_handler.setLevel(webhooks_config.get('level', WARNING))

            self.build_logger.addHandler(webhooks_handler)

            self.log_handlers[extension['name']] = webhooks_handler

        def stop(self):
            '''Remove the POST handler when the app stops.'''

            super().stop()
            self.build_logger.removeHandler(self.log_handlers.pop(extension['name']))


    return Sloth
