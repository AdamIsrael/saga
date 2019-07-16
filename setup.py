import os

from setuptools import setup

VERSION = "0.1.0"


def readme():
    """ Load the contents of the README file """
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_path, "r") as f:
        return f.read()

setup(
    name="saga",
    version=VERSION,
    author="Adam Israel",
    author_email="adam@adamisrael.com",
    description="A Python library and command line interface for compiling Markdown documents",
    long_description=readme(),
    # install_requires=["pycrypto", "pbkdf2", "fuzzywuzzy"],
    # license="MIT",
    url="http://github.com/adamisrael/saga",
    # classifiers=[],
    packages=["saga"],
    # scripts=["bin/saga"],
    entry_points = {
        'console_scripts': [
            'saga=saga.saga:main'
        ],
    }
    # tests_require=["nose", "mock"],
    # test_suite="nose.collector",
)
