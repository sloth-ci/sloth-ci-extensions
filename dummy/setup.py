from setuptools import setup

import dummy as ext


setup(
    name=ext.__title__,
    version=ext.__version__,
    author=ext.__author__,
    description='Dummy app extension for Sloth CI',
    long_description='Dummy Sloth CI app extension that replaces the default executor',
    author_email='moigagoo@live.com',
    url='https://bitbucket.org/moigagoo/sloth-ci-extensions',
    py_modules=['sloth_ci.ext.dummy'],
    package_dir={'sloth_ci.ext': '.'},
    install_requires = [
        'sloth_ci'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
    )
