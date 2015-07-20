'''Dummy Sloth CI server extension that replaces the app creator.

Extension params::

    # Use the module sloth_ci.ext.dummy_server.
    module: dummy_server

    # Some param. If missing, "baz" is used.
    foo: bar

The ``foo`` param is optional.

.. hint:: This extension can be used as a reference when creating *real* app extensions.

Sloth server extensions extend the base Bed class. An extension can override default methods and attributes, as well as add its own. Extensions have access to the app config.

Extensions are declared in the ``extensions`` section in the Sloth server config.

An extension is a module containing a single function ``extend(cls, extension)`` that returns the class ``Bed``. It inherits from ``cls``. Its minimal ``__init__`` method calls its parent's ``__init__``.

Methods of the Bed class will replace the methods of the same name in the original sloth_ci.bed.Bed class.
'''


__title__ = 'sloth-ci.ext.dummy_server'
__description__ = 'Dummy server extension for Sloth CI'
__version__ = '1.0.0'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend(cls, extension):
    class Bed(cls):
        def __init__(self, config):
            super().__init__(config)

            dummy_config = extension['config']

            self.foo = dummy_config.get('foo') or 'baz'

        def create_from_config(self, config):
            print('Hello from the dummy app creator that ignores the config and just does nothing.')
            print('Here is a config value extracted from the "dummy" section: foo = %s' % self.foo)

            return 'spam'

    return Bed