'''robots.txt for Sloth CI.

Extension params::

    # Use the sloth_ci.ext.robots_txt module.
    module: robots_txt

    # Absolute path to the custom robots.txt file.
    # If not given, the bundled one is used (disallows everything to everyone).
    # file: ~/robots.txt
 
    # URL path to robots.txt.
    # By default the file is available in the root: *http://example.com:8080/robots.txt*.
    # path: /static/robots.txt

File and path params are optional.
'''


__title__ = 'sloth-ci.ext.robots_txt'
__description__ = 'robots.txt for Sloth CI'
__version__ = '1.0.0'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend(cls, extension):
    from os.path import dirname, join

    import cherrypy

    class Bed(cls):
        def __init__(self, config):
            super().__init__(config)

        def _configure(self):
            super()._configure()

            robots_txt_config = extension['config']

            robots_txt_file = robots_txt_config.get('file') or join(dirname(__file__), 'robots.txt')
            robots_txt_path = robots_txt_config.get('path') or '/robots.txt'

            cherrypy.tree.mount(None, robots_txt_path, config={'/': {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': robots_txt_file
            }})

    return Bed