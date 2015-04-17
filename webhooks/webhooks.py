'''Sloth CI extension that sends POST requests on build events in Sloth CI apps.

Extension params::
    
    # Use the module sloth-ci.ext.webhooks.
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
__description__ = 'Webhooks for Sloth CI apps'
__version__ = '1.0.0'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


from logging import Handler
from json import dumps
from requests import post


class POSTHandler(Handler):
    '''Log handler that sends a POST request to the specified URL.
    
    :param url: URL to send the requests to.
    '''
    
    def __init__(self, url):
        super().__init__()

        self.url = url

    def emit(self, record):
        '''Send a POST request to the specified URL.'''

        try:
            payload = {
                'name': record.name, 
                'level': record.levelname,
                'message': record.getMessage()
            }

            post(self.url, json=dumps(payload))

        except Exception:
            self.handleError(record)


def extend(cls, extension):
    from logging import WARNING

    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)
            
            webhooks_config = extension['config']
            
            webhooks_handler = POSTHandler(webhooks_config['url'])

            webhooks_handler.setLevel(webhooks_config.get('level', WARNING))
            
            self.build_logger.addHandler(webhooks_handler)

            self.log_handlers[extension['name']] = webhooks_handler

        def stop(self):
            super().stop()
            self.build_logger.removeHandler(self.log_handlers.pop(extension['name']))


    return Sloth