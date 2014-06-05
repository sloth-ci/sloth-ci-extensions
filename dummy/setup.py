from setuptools import setup

import dummy as ext


package = 'sloth_ci.ext'

setup(
    name=ext.__title__,
    version=ext.__version__,
    author=ext.__author__,
    description='Dummy app extension for Sloth CI',
    long_description='Dummy Sloth CI app extension that replaces the default executor.',
    author_email='moigagoo@live.com',
    url='https://bitbucket.org/moigagoo/sloth-ci-extensions',
    py_modules=['%s.dummy' % package],
    package_dir={package: '.'},
    install_requires = [
        'sloth_ci>=0.6.2'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
    )
