'''Robots.txt for the Sloth CI server.

`Robots.txt <https://en.wikipedia.org/wiki/Robots_exclusion_standard>`__ is a file you put on your server to protect certain URLs from being accessed by crawler bots.

By default,tThis extension serves *robots.txt* on the server root, e.g. http://example.com:8080/robots.txt. However, you can specify your own file to serve and the URL to serve it on.


Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.ext.robots_txt


Usage
-----

.. code-block:: yaml
    :caption: sloth.yml

    extensions:
        robots_txt:
            # Use the sloth_ci.ext.robots_txt module.
            module: robots_txt

            # Absolute path to the custom robots.txt file.
            # If not given, the bundled one is used (disallows everything to everyone).
            # file: ~/robots.txt
 
            # URL path to robots.txt.
            # By default the file is available in the root: *http://example.com:8080/robots.txt*.
            # path: /static/robots.txt
'''


__title__ = 'sloth-ci.ext.robots_txt'
__description__ = 'Robots.txt for the Sloth CI server'
__version__ = '1.0.3'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend_bed(cls, extension):
    '''Mount *robots.txt* on the `CherryPy tree <http://docs.cherrypy.org/en/latest/pkg/cherrypy.html?#cherrypy._cptree.Tree>`__ during server configuration.'''

    from os.path import dirname, join

    import cherrypy


    class Bed(cls):
        def _configure(self):
            '''Add the robots.txt route to the CherryPy tree.'''

            super()._configure()

            robots_txt_config = extension['config']

            robots_txt_file = robots_txt_config.get('file') or join(dirname(__file__), 'robots.txt')
            robots_txt_path = robots_txt_config.get('path') or '/robots.txt'

            cherrypy.tree.mount(None, robots_txt_path, config={'/': {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': robots_txt_file
            }})


    return Bed