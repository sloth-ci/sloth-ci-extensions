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
__version__ = '1.0.0'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend_bed(cls, extension):
    return cls


def extend_cli(cls, extension):
    '''Add CLI commands to create extension and validator dev_templates.'''

    from os import mkdir
    from os.path import join, dirname

    from string import Template


    class CLI(cls):
        def __init__(self):
            super().__init__()

            self.template_path = join(dirname(__file__), 'dev_templates')

        def dev(self, name, extension=False, validator=False):
            '''create an extension or validator template'''

            if bool(extension) == bool(validator):
                print('Run "sci dev -e NAME" to create an extension or "sci dev -v NAME" to create a validator.')

            else:
                mkdir(name)

                if extension:
                    source_template = Template(open(join(self.template_path, 'extension', 'extension.py')).read())
                    setup_py_template = Template(open(join(self.template_path,'extension', 'setup.py')).read())

                    with open(join(name, '%s.py' % name), 'w') as source:
                        source.write(source_template.safe_substitute(extension=name))

                    with open(join(name, 'setup.py'), 'w') as setup_py:
                        setup_py.write(setup_py_template.safe_substitute(extension=name))

                    print('Extension "%s" created.' % name)

                elif validator:
                    source_template = Template(open(join(self.template_path, 'validator', 'validator.py')).read())
                    setup_py_template = Template(open(join(self.template_path, 'validator', 'setup.py')).read())

                    with open(join(name, '%s.py' % name), 'w') as source:
                        source.write(source_template.safe_substitute(validator=name))

                    with open(join(name, 'setup.py'), 'w') as setup_py:
                        setup_py.write(setup_py_template.safe_substitute(validator=name))

                    print('Validator "%s" created.' % name)

    return CLI
