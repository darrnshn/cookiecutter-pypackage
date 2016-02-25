======================
cookiecutter-pypackage
======================

Cookiecutter template for a Python analytics, machine learning and statistics 
package. Based on `Nekroze/cookiecutter-pypackage`_

* Free software: Apache 2.0 License
* Pytest_ runner: Supports `unittest`, `pytest`, `nose` style tests and more
* Travis-CI_: Ready for Travis Continuous integration testing
* Tox_ testing: Setup to easily test for python 2.6, 2.7, 3.3 and PyPy_
* Sphinx_ docs: Documentation ready for generation with ReadTheDocs_, `Github Pages`_
* Wheel_ support: Use the newest Oython package distribution standard from the get-go

Usage
-----

Generate a Python package project::

    $ cookiecutter https://github.com/TerriaJS/cookiecutter-pypackage

* Initialize repo and push to Github.
* Add the repo to your Travis CI account.
* (For ReadTheDocs) Add the repo to your ReadTheDocs account + turn on the ReadTheDocs service hook.
* (For Github Pages) Run `make ghp`.
* Run `tox` to make sure all tests pass.
* Release your package the standard Python way.

.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _ReadTheDocs: https://readthedocs.org/
.. _`Nekroze/cookiecutter-pypackage`: https://github.com/Nekroze/cookiecutter-pypackage
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _Pytest: http://pytest.org/
.. _PyPy: http://pypy.org/
.. _Wheel: http://pythonwheels.com
.. _Github Pages: https://pages.github.com/