================
kivy-statecharts
================

kivy-statecharts offers a high-level approach to using the Kivy system. It is a
system for programming with statecharts and other elements of design that
compliments core Kivy. 

kivy-statecharts has goals including:

* Examining software design patterns, such as model-view-controller,
  model-view-adapter, and others, to see how Kivy programming can be adapted,
  with statecharts playing a primary role.

* Exploring statecharts programming, providing examples that demonstrate basic
  app structure, and applications of standard, history, concurrent, and other
  state usage.

* Describing app structures that exemplify good options for developing large Kivy
  applications and projects.

kivy-statecharts was started as a port of Michael Cohen's Ki framework, which
became SproutCore.statechart. The kivy-statecharts project has taken on the
broad tasks listed above, to become a high-level extension to Kivy that
includes substantial documentation and code on its own.

`Original Ki repo`_
https://github.com/frozenCanuck/ki

`SC.Statechart repo`_
https://github.com/sproutcore/sproutcore/tree/master/frameworks/statechart

SC.Statechart was used as the basis for this port to Python.

`Find out more about Kivy`_

Setting up kivy-statecharts
===========================

A virtual environment works well for Kivy and kivy-statecharts development.
But if you have Kivy already running locally and wish to take a quick look at
kivy-statecharts, clone kivy-statecharts and cd to its examples directory, and
to the hello_world example. If you simply run python main.py, kivy-statecharts
will not be found, because it is not on PYTHONPATH.  You can augment paths on
PYTHONPATH on the command line as described in the answers for this
`Stackoverflow question about PYTHONPATH`_. So the following should bring up
the hello_world example app::

    PYTHONPATH=/path/to/kivy_statecharts python main.py

The hello_world app appears to do nothing, but if you type letters for "hello
world", (h, e, l, o, w, r, d), you will see buttons with these letters appear
in random locations. If you click or touch any button, even more random buttons
will appear. When you look at the `hello_world example app code`_, you will see
one real state in a simple statechart. There are bindings to fire action events
to the statechart with h, e, l, o, w, r, and d keyboard entries, and for the
same events to be fire when buttons are clicked. The action events correspond
to methods of the single state in the statechart. We would say that the current
state has action methods that handle the keyboard action events. A statechart
is an organization structure holding states with such actions and helper
methods.

From the hello_world example app, you can move to the Balls example app, and to
the more involved examples from there. diagrammer is the most representative of
best practices, as of Summer 2013.

Setting up kivy-statecharts for Development
===========================================

If you are debugging or adding features to kivy-statecharts, here is one way to
work with it. Make a `virtualenv`_ for doing kivy-statechart work::

    virtualenv kivy_statecharts

    cd kivy_statecharts

    source bin/activate

Also, here are steps using the `virtualenvwrapper`_ system, which is a nice way
to work, because you can switch between virtualenvs easily::

    mkvirtualenv kivy_statecharts
    
    cdvirtualenv

    workon kivy_statecharts

Either way, whether by using virtualenv directly, or by using
virtualenvwrapper, you now have a kivy_statecharts virtualenv, and it should be
active. For Unix systems, to make sure that you have it activated, you can
check which python is active with::

    which python

and you should see the path to the python in your virtualenv, not to the system
Python interpreter.

Do steps to install kivy; if using master, install dependencies, then git clone
it, and inside kivy, do::

    python setup.py develop

Clone the kivy-statecharts repo::

    git clone https://github.com/kivy/kivy-statecharts.git

    cd kivy_statecharts

    python setup develop

    python setup dev (for setting up for testing)

Be warned: This project is in alpha state. Use it at your own risk.

Using kivy-statecharts
======================

Source Sphinx docs are in the docs directory.

See the examples.

Status
======

``kivy-statecharts`` is perhaps becoming suitable for use in production
environments, judging by a good set of tests, but not yet by any known apps in
the wild (as of April, 2013).  A proper release program will be started in
Summer 2013 so that, to use, you can make sure to pin the exact version in your
requirements. It is expected that releases, although they will start with an
alpha designation, will soon move to beta status. The main reason for the
present status is that despite a full set of tests, there aren't yet enough
examples covering fuller treatments of some of the features and uses.

Development
===========

Contributions to ``kivy-statecharts`` are very welcome.  Just clone its `GitHub
repository`_ and submit your contributions as pull requests.

Note that all development is done on the ``develop`` branch. ``master`` is reserved
for "production-ready state".  Therefore, make sure to always base development work
on the current state of the ``develop`` branch.

This follows the highly recommended `A successful Git branching model`_ pattern,
which is implemented by the excellent `gitflow`_ git extension.

Testing
-------

|build status|_

``kivy-statecharts`` has 100% test coverage. Use `nose`_ or `py.test`_.

Please make sure that you add tests for new features and that all tests pass before
submitting pull requests.  Running the test suite is as easy as running ``py.test``
from the source directory. Presently, both py.test and nosetests work. Run
``python setup.py dev`` to have all the test requirements installed in your virtualenv.

Unit tests have previously been done with `nose`_.  In the kivy_statechart directory,
run:

    nosetests

As of April 2012, most tests were ported from the original javascript version.


.. _Original Ki repo: https://github.com/frozenCanuck/ki
.. _SC.Statechart repo: https://github.com/sproutcore/sproutcore/tree/master/frameworks/statechart
.. _Find out more about Kivy: http://kivy.org
.. _GitHub repository: https://github.com/kivy/kivy-statecharts
.. _gitflow: https://github.com/nvie/gitflow
.. _A successful Git branching model: http://nvie.com/posts/a-successful-git-branching-model/
.. _hello_world example app code: https://github.com/kivy/kivy-statecharts/blob/master/examples/hello_world/main.py
.. _nose: http://readthedocs.org/docs/nose/en/latest/
.. _py.test: http://pytest.org/latest/
.. _Stackoverflow question about PYTHONPATH: http://stackoverflow.com/questions/4580101/python-add-pythonpath-during-command-line-module-run
.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
