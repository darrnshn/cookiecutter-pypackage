#!/usr/bin/env python

from setuptools import setup, find_packages, Extension
from setuptools.command.test import test as TestCommand
from setuptools.command.build_ext import build_ext as BuildExtCommand
import sys, os, re


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

class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

# From https://github.com/dfm/transit/blob/master/setup.py
def find_eigen(hint=None):
    """
    Find the location of the Eigen 3 include directory. This will return
    ``None`` on failure.
    """
    # List the standard locations including a user supplied hint.
    search_dirs = [] if hint is None else hint
    search_dirs += [
        "/usr/local/include/eigen3",
        "/usr/local/homebrew/include/eigen3",
        "/opt/local/var/macports/software/eigen3",
        "/opt/local/include/eigen3",
        "/usr/include/eigen3",
        "/usr/include/local",
        "/usr/include",
    ]

    # Loop over search paths and check for the existence of the Eigen/Dense
    # header.
    for d in search_dirs:
        path = os.path.join(d, "Eigen", "Dense")
        if os.path.exists(path):
            # Determine the version.
            vf = os.path.join(d, "Eigen", "src", "Core", "util", "Macros.h")
            if not os.path.exists(vf):
                continue
            src = open(vf, "r").read()
            v1 = re.findall("#define EIGEN_WORLD_VERSION (.+)", src)
            v2 = re.findall("#define EIGEN_MAJOR_VERSION (.+)", src)
            v3 = re.findall("#define EIGEN_MINOR_VERSION (.+)", src)
            if not len(v1) or not len(v2) or not len(v3):
                continue
            v = "{0}.{1}.{2}".format(v1[0], v2[0], v3[0])
            print("Found Eigen version {0} in: {1}".format(v, d))
            return d
    return None

ext_modules = [
    Extension(
        '{{ cookiecutter.repo_name }}.ext',
        ['{{ cookiecutter.repo_name }}/src/main.cpp'],
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True),
            find_eigen()
        ],
        language='c++'
    ),
]

# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.
    The c++14 is prefered over c++11 (when it is available).
    """
    if has_flag(compiler, '-std=c++14'):
        return '-std=c++14'
    elif has_flag(compiler, '-std=c++11'):
        return '-std=c++11'
    else:
        raise RuntimeError('Unsupported compiler -- at least C++11 support '
'is needed!')


class BuildExt(BuildExtCommand):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }

    if sys.platform == 'darwin':
        c_opts['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
        BuildExtCommand.build_extensions(self)

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
    ext_modules=ext_modules,
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.repo_name }}_cli_script = {{ cookiecutter.repo_name }}.scripts.cli_script:cli'
        ],
        'gui_scripts': [
            '{{ cookiecutter.repo_name }}_gui_script = {{ cookiecutter.repo_name }}.scripts.gui_script:gui'
        ]
    },
    install_requires=[
        'scipy',
        'numpy',
        'pycontracts',
        'pybind11'
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
        'test': PyTest,
        'build_ext': BuildExt
    },
    tests_require=[
        'pytest',
        'pytest-cov',
        'coverage',
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
