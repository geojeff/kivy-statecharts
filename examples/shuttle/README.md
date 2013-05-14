Shuttle App
===========

*shuttle* is a mock control panel for the Space Shuttle's Reaction Control
System (RCS) used for controlling forward and aft bays of small thrusters.

Usage
-----

The app is a one-panel display of the RCS diagram of 14 thruster groups in the
three areas of the shuttle: forward, aft-left, and aft-right. There are red
dots at each of the thruster group locations. Along the bottom are rectangular
blocks for the main user interface controls that fire the thruster groups
(Touch the blue cicles to apply thrust). On the left side are the rotational
motion controls, for yaw, pitch, and roll, and on the right are translational
motion controls for x, y, and z.  For example, if you tap the blue circle in
the "yaw plus" motion control block, the G2 and G10 thruster groups will fire.
Tap repeatedly, and you will see the affected thruster groups pulsate more and
more. If you want to throttle back on the thrusters, switch the mode control
from "More" to "Less" and tap the same blue buttons.

Running at a Given Window Size
------------------------------

You can pass the window app size as a command line argument like this::

    python main.py --size=700x774

This will fit the user interface size exactly. The background image,
RCS_Jet_Code.png, has the dimensions 600x714, and shows on the right, with a
100 pixel wide list view on the left.

Because the user interface is inherently "portrait," because of the aspect of
the background image used, if you resize the window on a desktop or laptop with
a large display, the user interface will resize, but stay in portrait. On a
small device, the same portrait mode forcing should apply. See the original
viewport code on the Kivy wiki, that rotates a user interface, depending on
portrait or landscape, if you are designing an app that needs this. In the
shuttle app, we simplify to force portrait display.

To experiment with a given app window size, change the numbers::

    python main.py --size=1200x800

Running with the touchring Module
---------------------------------

Also, when developing Kivy apps and precise touch interfaces like this one, you
can activate the touchring module in your ~/.kivy/config.ini file, with::

[modules]
touchring =

touchring =, with just the = sign, will activate the module to show a large
circle around each touch. This helps to see touches when using the touchpad on
Mac OSX, for example, which is activated with::

[input]
touchpad = mactouch

Read the Kivy docs for help configuring for your platform, if needed.

For the touchring module, if the circle that shows for touches is too large,
scale it down like this::

[modules]
touchring = scale=.3

Description of Space Shuttle Thruster System
============================================

There are 44 thrusters that individually fire in some combination when the fuel
is mixed with an oxidizing substance (hypergolic combination), so that there is
no need for an igniter device. Most of the 44 are a larger type called primary
thrusters; six of the 44 are smaller vernier thrusters.

"Each RCS thruster burns a combination of monomethyl hydrazine and nitrogen
tetroxide liquid fuel. Each primary thruster can produce a thrust of 870
pounds, while each vernier thruster can produce a thrust of 24 pounds. The RCS
thrusters can be fired in a plethora of combinations depending on the specific
mission requirements." (from
http://spaceline.org/rocketsum/orbiter-systems.html).

The OMS, the Orbital Maneuvering System, is a different system consisting of
two larger engines.

You can see images and descriptions of the RCS system on these web pages:

http://www.columbiassacrifice.com/&0_shttlovrvw.htm

http://www.spaceflight.nasa.gov/shuttle/reference/shutref/orbiter/rcs/overview.html

http://howthingsfly.si.edu/media/shuttle-reaction-control-system

The main background image for the mock RCS control panel in the shuttle app is
from http://www.columbiassacrifice.com/subsections_Misc/RCS_Jet_Code.htm

Several other images are copied here to show the location of the forward and
aft RCS thruster locations. In the main diagram, you will see thruster id codes
for the aft system starting with the letter "F", e.g. "F4D", which is the 4th
thruster with plume shooting downward. Labels for the aft RCS system are
similar, either starting with the letter "R" for the aft-right set of thrusters
or with "L" for the aft-left thrusters.

You can see one of the forward thrusters firing in these videos:
http://www.youtube.com/watch?v=2ewbD2Pv5ag&feature=related and this one at
about 45 seconds: http://www.youtube.com/watch?v=1xT4GstMyKs&feature=related.
Nice still images of thruster testing:
http://www.nasa.gov/centers/wstf/propulsion/shuttleFleetLeader.html

In reality, the RCS system is controlled by the autopilot system, or by adhoc
software control, or manually controlled by the astronauts:
http://science.ksc.nasa.gov/shuttle/technology/sts-newsref/sts-rcs.html,
specifically by the rotational and translational hand controllers:
http://science.ksc.nasa.gov/shuttle/technology/sts-newsref/sts-rhc.html#sts-rhc

NASA space shuttle mission reports like [this
one](http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19960001496_1996901496.pdf)
include coverage of the operation of the RCS system.

System Design
=============

If you read the README for the kivy-statecharts project, you will see use of
the term "reactive system" in the 1987 research paper by David Harel on
statecharts. Statecharts are ready-made for reactive systems that have many
"stimuli" and complexity. It is no coincidence that the subject of the shuttle
app is the space shuttles "reaction control system." Specifically, we highlight
the use of orthogonality and concurrency in this app. The individual motion
controls (yaw-plus, translate_x_minus, etc.) are orthogonal to one another:
they happen independently. The same goes for the individual thruster groups,
were they not linked together within the motion controls. Within a given
thruster group, however, the affected thrusters operate concurrently. 

This app has the benefit of adapting to an existing real, physical system, but
you can imagine the usefullness of statecharts if such a touch-screen interface
were to be developed (and the undoubted requirement for something similar, at
least in the thought processes and electronics design, for the engineers who
built this system).
