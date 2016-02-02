'''Utilities to help you develop extensions and validators for Sloth CI.


Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.ext.devtools


Usage
-----

Enable the extension in the server config:

.. code-block:: yaml
    :caption: devtools.yml

    extensions:
        dev:
            # Use the module sloth_ci.ext.devtools.
            module: devtools

Call the ``sci dev`` with ``-e`` or ``-v`` to create an extensions or a validator template:

.. code-block:: bash

    $ sci dev -e spam
    Extension "spam" created.

    $ sci dev -v eggs
    Validator "eggs" created.
'''


__title__ = 'sloth-ci.ext.devtools'
__description__ = 'Utilities for Sloth CI extension and validator development'
__version__ = '1.0.3'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend_bed(cls, extension):
    return cls


def extend_cli(cls, extension):
    '''Add CLI commands to create extension and validator templates.'''

    from os import mkdir
    from os.path import join, dirname, abspath

    from string import Template


    class CLI(cls):
        def __init__(self):
            super().__init__()

            self.template_path = join(dirname(__file__), 'dev_templates')

        def dev(self, name, extension=False, validator=False, destination='.'):
            '''create an extension or validator template in a given location (current directory by default)'''

            if bool(extension) == bool(validator):
                print('Run "sci dev -e NAME" to create an extension or "sci dev -v NAME" to create a validator.')

            else:
                destination_path = abspath(join(destination, name))

                mkdir(destination_path)

                if extension:
                    source_template = Template(open(join(self.template_path, 'extension', 'extension.py')).read())
                    setup_py_template = Template(open(join(self.template_path,'extension', 'setup.py')).read())

                    with open(join(destination_path, '%s.py' % name), 'w') as source:
                        source.write(source_template.safe_substitute(extension=name))

                    with open(join(destination_path, 'setup.py'), 'w') as setup_py:
                        setup_py.write(setup_py_template.safe_substitute(extension=name))

                    print('Extension "%s" created in %s' % (name, destination_path))

                elif validator:
                    source_template = Template(open(join(self.template_path, 'validator', 'validator.py')).read())
                    setup_py_template = Template(open(join(self.template_path, 'validator', 'setup.py')).read())

                    with open(join(destination_path, '%s.py' % name), 'w') as source:
                        source.write(source_template.safe_substitute(validator=name))

                    with open(join(destination_path, 'setup.py'), 'w') as setup_py:
                        setup_py.write(setup_py_template.safe_substitute(validator=name))

                    print('Validator "%s" created.' % name)

    return CLI
