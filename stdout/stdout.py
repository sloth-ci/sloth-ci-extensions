'''Describe your extension.


Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.ext.stdout


Usage
-----

.. code-block:: yaml
    :caption: stdout.yml

    extensions:
        stdout:
            # Use the module sloth_ci.ext.stdout.
            module: stdout
'''

__title__ = 'sloth-ci.ext.stdout'
__description__ = 'Get stdout and stderr of Sloth CI apps.'
__version__ = '0.0.1'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend_bed(cls, extension):
    '''Add the ``stdout`` endpoint.

    :param cls: the base ``sloth_ci.bed.Bed`` class
    :param extension: ``{'name': '{extension}', 'config': {param1: value2, param2: value2, ...}}``, extracted from the server config
    '''

    class Bed(cls):
        def __init__(self, config):
            super().__init__(config)

            self.actions['stdout'] = self.stdout

        def stdout(self, kwargs):
            '''Get paginated app stdout and stderr output.'''

            if not self.db_path:
                raise cherrypy.HTTPError(501, "This Sloth server doesn't have a database to store logs")

            listen_point = kwargs.get('listen_point')

            if not listen_point:
                raise cherrypy.HTTPError(400, 'Missing parameter "listen_point"')

            try:
                if listen_point not in self.sloths:
                    raise KeyError(listen_point)

                from_page = int(kwargs.get('from_page', 1))
                to_page = int(kwargs.get('to_page', from_page))
                per_page = int(kwargs.get('per_page', 10))

                connection = sqlite3.connect(self.db_path)
                cursor = connection.cursor()

                query = 'SELECT * FROM app_logs \
                    WHERE logger_name=? \
                    AND level_number = 10 \
                    ORDER BY timestamp DESC \
                    LIMIT ? OFFSET ?'

                query_params = (
                    listen_point + '.exec',
                    (to_page - from_page + 1) * per_page,
                    (from_page - 1) * per_page
                )

                cursor.execute(query, query_params)

                column_names = [column[0] for column in cursor.description]

                stdout = [dict(zip(column_names, record)) for record in cursor.fetchall()]

                connection.close()

                cherrypy.response.status = 200

                return stdout

            except KeyError as e:
                raise cherrypy.HTTPError(404, 'Listen point %s not found' % e)

            except Exception as e:
                raise cherrypy.HTTPError(500, 'Failed to get app stdout: %s' % e)

    return Bed


def extend_cli(cls, extension):
    '''Modify ``sloth_ci.cli.CLI`` to add new ``sci`` commands.

    :param cls: the base ``sloth_ci.cli.CLI`` class
    :param extension: ``{'name': 'stdout', 'config': {param1: value2, param2: value2, ...}}``, extracted from the server config
    '''


    from cliar import add_aliases


    class CLI(cls):
        @add_aliases(['out', 'stderr'])
        def stdout(self, app, from_page:int=1, to_page:int=1, per_page:int=10, raw=False):
            '''get stdout and strerr for APP'''

            response = self.send_api_request(
                {
                    'action': 'stdout',
                    'listen_point': app,
                    'from_page': from_page,
                    'to_page': to_page,
                    'per_page': per_page,
                }
            )

            if response.status_code == 200:
                rows = [
                    [
                        ctime(record['timestamp']),
                        record['message'],
                    ] for record in response.content
                ]

                headers = [
                    'Timestamp',
                    'Message'
                ]

                if raw:
                    pass
                else:
                    table = tabulate(
                        colorize(rows, based_on_column=-1),
                        headers=headers
                    )

                print(table)

            else:
                print('Failed to get app stdout: %s' % response.content)

    return CLI


def extend_sloth(cls, extension):
    '''Modify ``sloth_ci.sloth.Sloth`` to affect app behavior: add loggers, override action executing routine, etc.

    :param cls: the base ``sloth_ci.sloth.Sloth`` class
    :param extension: ``{'name': 'stdout', 'config': {param1: value2, param2: value2, ...}}``, extracted from the app config
    '''

    return cls
