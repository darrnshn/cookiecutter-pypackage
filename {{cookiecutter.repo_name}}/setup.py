#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        super(PyTest, self).initialize_options()
        self.pytest_args = []

    def finalize_options(self):
        super(PyTest, self).finalize_options()
        self.test_suite = True
        self.test_args = []

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        exit(pytest.main(self.pytest_args))

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://nicta.github.io/{{ cookiecutter.repo_name }}/."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='{{ cookiecutter.repo_name }}',
    version='{{ cookiecutter.version }}',
    description='{{ cookiecutter.project_short_description }}',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='{{ cookiecutter.full_name }}',
    author_email='{{ cookiecutter.email }}',
    url='https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}',
    packages=find_packages(),
    package_dir={'{{ cookiecutter.repo_name }}': '{{ cookiecutter.repo_name }}'},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.repo_name }}_cli_script = scripts.{{ cookiecutter.repo_name }}_cli_script:cli'
        ],
        'gui_scripts': [
            '{{ cookiecutter.repo_name }}_gui_script = scripts.{{ cookiecutter.repo_name }}_gui_script:gui'
        ]
    },
    install_requires=[
        'scipy',
        'numpy',
    ],
    extras_require={
        'demos': [
            'click',
            'matplotlib'
        ],
        'dev': [
            'sphinx',
            'ghp-import'
        ]
    },
    cmdclass={
        'test': PyTest
    },
    tests_require=[
        'pytest',
        'pytest-cov',
        'codecov',
        'tox',
    ],
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='{{ cookiecutter.repo_name }}',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis"
    ],
)
