================
kivy_statecharts
================

This is an extension to the Kivy framework that adds a system for programming
with statecharts. It is a port of Michael Cohen's Ki framework, which became
SproutCore.statechart.

`Original Ki repo`_
https://github.com/frozenCanuck/ki

`SC.Statechart repo`_
https://github.com/sproutcore/sproutcore/tree/master/frameworks/statechart

SC.Statechart was used as the basis for this port to Python.

`Find out more about Kivy`_

Setting up kivy_statecharts
===========================

A virtual environment works well for Kivy and kivy_statecharts development.
Using the virtualenvwrapper framework is a good approach. After installing the
base system prerequisites for Kivy (sdl, sdl_image, sdl_mixer, sdl_ttf,
smpeg, portmidi), and after installing virtualenvwrapper and mercurial, do:

    mkvirtualenv myproject
    workon myproject
    pip install cython
    pip install pil
    pip install hg+http://bitbucket.org/pygame/pygame
    pip install kivy

If you are only using kivy_statecharts, just install it:

    pip install kivy_statecharts (when available on PyPI)

NOTE: Until kivy_statecharts is on PyPI, do clone and setup as below:

If you are debugging or adding features to kivy_statecharts, clone the repo
and set up for development:

    git clone https://github.com/geojeff/kivy-statecharts.git
    python setup develop
    python setup dev (See below; For setting up for testing)

Be warned: This addon is in alpha state. Use it at your own risk.

Using kivy_statecharts
======================

[Refer to new docs when they get on readthedocs.org.]

For now, source Sphinx docs are in the docs directory.

See the examples.

Work in progress
================

``kivy_statecharts`` is considered alpha software, not yet suitable for use in
production environments.  The current state of the project is in no way feature
complete nor API stable.  If you really want to use it in your project(s), make
sure to pin the exact version in your requirements.  Not doing so will likely
break your project when future releases become available.

Development
===========

Contributions to ``kivy_statecharts`` are very welcome.
Just clone its `GitHub repository`_ and submit your contributions as pull requests.

Note that all development is done on the ``develop`` branch. ``master`` is reserved
for "production-ready state".  Therefore, make sure to always base development work
on the current state of the ``develop`` branch.

This follows the highly recommended `A successful Git branching model`_ pattern,
which is implemented by the excellent `gitflow`_ git extension.

Testing
-------

|build status|_

``kivy_statecharts`` has 100% test coverage. Use nosetests or py.test.

Please make sure that you add tests for new features and that all tests pass before
submitting pull requests.  Running the test suite is as easy as running ``py.test``
from the source directory. Presently, both py.test and nosetests work. Run
``python setup.py dev`` to have all the test requirements installed in your virtualenv.


Unit tests have previously been done with `nose`_.  In the kivy_statechart directory,
run:

    nosetests

As of April 2012, most tests were ported.


.. _Original Ki repo: https://github.com/frozenCanuck/ki
.. _SC.Statechart repo: https://github.com/sproutcore/sproutcore/tree/master/frameworks/statechart
.. _Find out more about Kivy: http://kivy.org
.. _GitHub repository: https://github.com/geojeff/kivy_statecharts
.. _gitflow: https://github.com/nvie/gitflow
.. _A successful Git branching model: http://nvie.com/posts/a-successful-git-branching-model/
.. _nose: http://readthedocs.org/docs/nose/en/latest/
