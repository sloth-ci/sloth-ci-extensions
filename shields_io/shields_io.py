'''Status build badges for Sloth CI apps, powered by http://shields.io.


Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.ext.shields_io


Usage
-----

#.  Enable the extension in the server config:

        .. code-block:: yaml
            :caption: sloth.yml for Shields.io

            extensions:
                shields:
                    # Use the module sloth_ci.ext.shields_io.
                    module: shields_io

                    # Badge label. You can use the ``{app}`` and ``{timestamp}`` placeholders for app name and build timestamp.
                    # label: "My Sloth CI Status for {app}" # default is ``Sloth CI: {app}``

                    # Badge status. You can use ``{status}``, ``{app}``, and ``{timestamp}`` placeholders build status, app name, and build timestamp
                    # status: "{status}" # default is ``{status}, {timestamp}``

                    # Badge style: ``plastic``, ``flat``, ``flat-square``, or ``social``
                    # style: social # default is ``flat``

                    # Badge format: svg, png, jpg, or gif
                    # format: png # default is svg

                    # Color map for build statuses
                    # colors:
                    #    INFO: green # default is ``brightgreen``
                    #    WARNING: yellowgreen # default is ``yellow``
                    #    ERROR: orange # default is ``red``
                    ...

    All params are optional.

#.  Use the URL http://host:port/app?action=shield to get your badge.

    You can customize the badge on the fly by passing ``label``, ``style``, and ``format`` query params:

    -   http://host:port/app?action=shield&label=Build%20for%20{app}
    -   http://host:port/app?action=shield&style=social
    -   http://host:port/app?action=shield&format=png

'''

__title__ = 'sloth-ci.ext.shields_io'
__description__ = 'Status build shields for Sloth CI powered by http://shields.io'
__version__ = '1.0.5'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend_bed(cls, extension):
    '''Replace the default app listener with the one that returns a shield from http://shields.io.'''

    from time import ctime

    import cherrypy
    from requests import get


    class Bed(cls):
        def __init__(self, config):
            super().__init__(config)

            self._shields_config = extension['config']

            self._shield_label = self._shields_config.get('label', 'Sloth CI: {app}')
            self._shield_status = self._shields_config.get('status', '{status}, {timestamp}')
            self._shield_colors = {
                'INFO': 'brightgreen',
                'WARNING': 'yellow',
                'ERROR': 'red'
            }
            self._shield_style = self._shields_config.get('style', 'flat')
            self._shield_format = self._shields_config.get('format', 'svg')

        @cherrypy.expose
        @cherrypy.tools.proxy()
        @cherrypy.tools.json_in()
        def _app_listener(self, listen_point, **kwargs):
            '''If the app listen point is requested with ``?action=shield``, returns a shield image from http://shields.io.

            Otherwise, passes control to the parent listener.

            :param listen_point: Sloth app listen point (part of the URL after the server host)
            :param dict colors: mapping of logging statuses to colors
            :param style: see available styles on http://shields.io/
            :param format: see available formats on http://shields.io/
            '''

            listen_point = listen_point.strip('/')

            if kwargs.get('action') != 'shield':
                super()._app_listener(listen_point, **kwargs)

            else:
                try:
                    if not listen_point in self.sloths:
                        raise KeyError(listen_point)

                    shield_label = kwargs.get('label', self._shield_label)

                    shield_status = kwargs.get('status', self._shield_status)

                    shield_colors = self._shield_colors
                    shield_colors.update(self._shields_config.get('colors', {}))

                    shield_style = kwargs.get('style', self._shield_style)

                    shield_format = kwargs.get('format', self._shield_format)

                    info = self.info({'listen_point': listen_point})
                    status, level = info['last_build_status_message'], info['last_build_status_level']
                    timestamp = ctime(info['last_build_timestamp'])

                    shield_url = (
                        'https://img.shields.io/badge/' +
                        '-{status}-{color}.{format}' +
                        '?label={label}&style={style}'
                    ).format(
                        status=shield_status.format(
                            app=listen_point,
                            timestamp=timestamp,
                            status=status
                        ),
                        color=shield_colors[level],
                        format=shield_format,
                        label=shield_label.format(
                            app=listen_point,
                            timestamp=timestamp
                        ),
                        style=shield_style
                    )

                    shield = get(shield_url)

                    cherrypy.response.headers['Content-Type'] = shield.headers['Content-Type']

                    return shield.content

                except KeyError as e:
                    raise cherrypy.HTTPError(404, 'Listen point %s not found' % e)

                except cherrypy.HTTPRedirect as e:
                    raise e

                except Exception as e:
                    raise cherrypy.HTTPError(500, 'Failed to get a shield: %s' % e)


    return Bed
