kivy-statechart is a port of the Ki/SproutCore statechart framework to Python for use in Kivy projects.

Original repos: [Ki](https://github.com/frozenCanuck/ki) and [SC.Statechart](https://github.com/sproutcore/sproutcore/tree/master/frameworks/statechart)

SC.Statechart was used as the basis for this port to Python and Kivy.

Installation
------------

kivy-statechart is a standalone Python module that you may wish to put alongside your local clone of Kivy if you are doing development. I have the
following setup for development:

~/Development/kivy/kivy, where I cloned Kivy, and ~/Development/kivy/kivy_statechart, where I cloned kivy-statechart. I added both of these to my
~/.profile file's PYTHONPATH.

Then in a separate work area, I copied kivy_statechart/examples/editor/* and used that as the basis of a new Kivy app.

kivy-statechart requires no changes to Kivy proper, but Kivy needs to be installed properly.  I used homebrew to make a python 2.7.2 and to use its
easy_install to install Kivy and python dependencies of Kivy that were not installed by bre directly.

Tests
-----

Unit tests are done with [nose](http://readthedocs.org/docs/nose/en/latest/). In the kivy_statechart directory, run

    nosetests
