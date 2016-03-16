from setuptools import setup

import shields_io as ext


package = 'sloth_ci.ext'

setup(
    name=ext.__title__,
    version=ext.__version__,
    author=ext.__author__,
    description=ext.__description__,
    long_description=ext.__doc__,
    author_email=ext.__author_email__,
    url='https://bitbucket.org/sloth-ci/sloth-ci-extensions',
    py_modules=['%s.%s' % (package, ext.__name__)],
    packages=[package],
    package_dir={package: '.'},
    install_requires = [
        'sloth-ci>=2.1.1'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
)
