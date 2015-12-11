'''Utilities to help you develop extensions and validators for Sloth CI.


Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.ext.devtools


Usage
-----

.. code-block:: yaml
    :caption: devtools.yml

    extensions:
        dev:
            # Use the module sloth_ci.ext.devtools.
            module: devtools
'''

__title__ = 'sloth-ci.ext.devtools'
__description__ = 'Utilities for Sloth CI extension and validator development'
__version__ = '0.0.1'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend_bed(cls, extension):
    '''Modify ``sloth_ci.bed.Bed`` to add API endpoints and custom URI handlers.

    :param cls: the base ``sloth_ci.bed.Bed`` class
    :param extension: ``{'name': '{extension}', 'config': {param1: value2, param2: value2, ...}}``, extracted from the server config
    '''

    return cls


def extend_cli(cls, extension):
    '''Modify ``sloth_ci.cli.CLI`` to add new ``sci`` commands.

    :param cls: the base ``sloth_ci.cli.CLI`` class
    :param extension: ``{'name': '{extension}', 'config': {param1: value2, param2: value2, ...}}``, extracted from the server config
    '''

    return cls


def extend_sloth(cls, extension):
    '''Modify ``sloth_ci.sloth.Sloth`` to change affect app behavior: add loggers, override action executing routine, etc.

    :param cls: the base ``sloth_ci.sloth.Sloth`` class
    :param extension: ``{'name': '{extension}', 'config': {param1: value2, param2: value2, ...}}``, extracted from the app config
    '''

    return cls