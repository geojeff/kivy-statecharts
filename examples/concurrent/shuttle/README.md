Description
===========

*shuttle* is a mock control panel for the Space Shuttle's Reaction Control System (RCS) used for controlling forward and aft bays of small thrusters. 

You can see images and descriptions of the system on these web pages:

http://www.columbiassacrifice.com/&0_shttlovrvw.htm

http://www.spaceflight.nasa.gov/shuttle/reference/shutref/orbiter/rcs/overview.html

http://howthingsfly.si.edu/media/shuttle-reaction-control-system

The main background image for the mock control panel is from http://www.columbiassacrifice.com/subsections_Misc/RCS_Jet_Code.htm

Several other images are copied here to show the location of the forward and aft RCS thruster locations. In the main diagram, you will see thruster id codes for the aft system starting with the letter "F", e.g. "F4D", which is the 4th thruster with plume shooting downward. Labels for the aft RCS system are similar, either starting with the letter "R" for the aft-right set of thrusters or with "L" for the aft-left thrusters.

You can see one of the forward thrusters firing in these videos: http://www.youtube.com/watch?v=2ewbD2Pv5ag&feature=related and this one at about 45 seconds: http://www.youtube.com/watch?v=1xT4GstMyKs&feature=related

In reality, the RCS system is controlled by the autopilot system or manually controlled by the astronauts: http://science.ksc.nasa.gov/shuttle/technology/sts-newsref/sts-rcs.html, specifically by the rotational and translational hand controllers: http://science.ksc.nasa.gov/shuttle/technology/sts-newsref/sts-rhc.html#sts-rhc

The Shuttle App
===============

In the shuttle app, touches on the blue circles in the rectangular boxes along the bottom, for the rotational controllers (roll, pitch, yaw) and for the translational controllers (x, y, z), fire one or more of 14 thruster group controls marked by red circles. When a group of thrusters is firing, there will be a visual display of a pulsating red circle for that group.

Running
-------

Use of kivy.config to set the Window width and height in the python code hasn't worked yet, so pass app size as a command line argument:

    python main.py --size=600x714

The background image, RCS_Jet_Code.png, has the dimensions 600x714, the same as the window size passed in, but there is margin added to top and right. This can probably be fixed with a size hint, but a fix for the use of kivy.config is a better solution.
