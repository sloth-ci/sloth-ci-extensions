from setuptools import setup

import docker_ as ext


package = 'sloth_ci.ext'

setup(
    name=ext.__title__,
    version=ext.__version__,
    author=ext.__author__,
    description='Docker app extension for Sloth CI',
    long_description='Docker Sloth CI app extension that replaces the default executor with a Docker-based one.',
    author_email='moigagoo@live.com',
    url='https://bitbucket.org/moigagoo/sloth-ci-extensions',
    py_modules=['%s.%s' % (package, ext.__name__)],
    package_dir={package: '.'},
    install_requires = [
        'sloth_ci>=0.6.2',
        'docker-py'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
    )
