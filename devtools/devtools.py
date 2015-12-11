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
    return cls


def extend_cli(cls, extension):
    '''Add CLI commands to create extension and validator dev_templates.'''

    from os import mkdir
    from os.path import join, dirname
    from shutil import copy

    from cliar import set_name


    class CLI(cls):
        @set_name('create-extension')
        def create_extension(self, name):
            '''create an extension template'''

            extension_template = join(dirname(__file__), 'dev_templates/extension/extension.py')
            setup_py_template = join(dirname(__file__), 'dev_templates/extension/setup.py')

            mkdir(name)

            copy(extension_template, join(name, '%s.py' % name))
            copy(setup_py_template, name)

        @set_name('create-validator')
        def create_validator(self, name):
            '''create a validator template'''

            validator_template = join(dirname(__file__), 'dev_templates/validator/extension.py')
            setup_py_template = join(dirname(__file__), 'dev_templates/validator/setup.py')

            mkdir(name)

            copy(validator_template, join(name, '%s.py' % name))
            copy(setup_py_template, name)


    return CLI
