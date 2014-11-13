'''Dummy Sloth CI app extension that replaces the default executor.

Config params::

    [dummy]
    ;Some param. If missing, "baz" is used.
    foo = bar

All config params are optional.

This extension can be used as a reference when creating *real* extensions.

Sloth app extensions extend the base Sloth class. An extension can override default methods and attributes, as well as add its own. Extensions have access to the app config. The convention is to keep all extension-related settings in the section of the same name, e.g. [dummy].

Extensions are declared in the [extensions] section in the Sloth app config and are plugged in in the order they are declared.

An extension is a module containing a single function ``extend(cls)``, which in turn declares a new class called by convention Sloth. It inherits from ``cls``. Its minimal ``__init__`` method must initialize the parent class instance.

Methods of the Sloth class will replace the methods of the same name in the original sloth_ci.sloth.Sloth class.
'''


__title__ = 'sloth-ci.ext.dummy'
__description__ = 'Dummy app extension for Sloth CI'
__version__ = '1.0.5'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend(cls, extension):
    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            dummy_config = self.config['extensions'][extension]

            self.foo = dummy_config.get('foo') or 'baz'

        def execute(self, action):
            print('Hello from a dummy executor that ignores the action and just does nothing.')
            print('Here is a config value extracted from the [dummy] section: foo = %s' % self.foo)
    
    return Sloth
