'''Dummy Sloth CI app extension that replaces the default executor.

Formerly known as "sloth-ci.dummy."

Extension params::

    # Use the module sloth_ci.ext.dummy_app.
    module: dummy_app

    # Some param. If missing, "baz" is used.
    foo: bar

The ``foo`` param is optional.

.. hint:: This extension can be used as a reference when creating *real* app extensions.

Sloth app extensions extend the base Sloth class. An extension can override default methods and attributes, as well as add its own. Extensions have access to the app config.

Extensions are declared in the ``extensions`` section in the Sloth app config.

An extension is a module containing a single function ``extend(cls, extension)`` that returns the class ``Sloth``. It inherits from ``cls``. Its minimal ``__init__`` method calls its parent's ``__init__``.

Methods of the Sloth class will replace the methods of the same name in the original sloth_ci.sloth.Sloth class.
'''


__title__ = 'sloth-ci.ext.dummy_app'
__description__ = 'Dummy app extension for Sloth CI'
__version__ = '1.1.1'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend(cls, extension):
    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            dummy_config = extension['config']

            self.foo = dummy_config.get('foo') or 'baz'

        def execute(self, action):
            print('Hello from a dummy executor that ignores the action and just does nothing.')
            print('Here is a config value extracted from the "dummy" section: foo = %s' % self.foo)

    return Sloth
