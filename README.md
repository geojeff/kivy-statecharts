kivy-statechart is a port of the Ki/SproutCore statechart framework to Python for use in Kivy projects.

Original repos: [Ki](https://github.com/frozenCanuck/ki) and [SC.Statechart](https://github.com/sproutcore/sproutcore/tree/master/frameworks/statechart)

SC.Statechart was used as the basis for this port to Python and Kivy.

Installation
------------

kivy-statechart is a standalone Python module that you may wish to put alongside your local clone of Kivy if you are doing development. For development, consider the following setup:

~/Development/kivy/kivy, for a Kivy clone, and ~/Development/kivy/kivy_statechart, for a kivy-statechart clone. Both were added to PYTHONPATH in
~/.profile so imports would work during development, as:

    export PYTHONPATH=$PYTHONPATH:/Users/geojeff/Development/kivy/kivy:/Users/geojeff/Development/kivy 

Tests
-----

Unit tests are done with [nose](http://readthedocs.org/docs/nose/en/latest/). In the kivy_statechart directory, run

    nosetests

As of April 2012, most tests have been ported.

Example Apps
------------

The examples directory contains several of the Kivy example apps adapted to use statecharts. New examples illustrate specific statechart functionality.
