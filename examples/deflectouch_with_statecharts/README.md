PORT to STATECHART Treatment
============================

Deflectouch-with-Statecharts has changes needed to move code to
a statechart treatment. The port is meant as an example for
comparison to a full Kivy app with and without statecharts.

See Cyril Stoller's Deflectouch repo for the original code:

    https://github.com/stocyr/Deflectouch

As of July, 2012, this port is a work-in-progress ...

Review Notes About Porting to Statechart Version
------------------------------------------------

The process is something of a reverse-engineering affair, involving
iterative work thinking about how a statechart would have been drawn
if the app had been developed with statecharts in the first place,
and examining the code to see how it would be shifted around, 
accordingly. "Coordinating" code was moved from widgets to the
enter and exit functions of new states, and to specialized functions
and action functions of the states, leaving the widgets, and their
associated kv definitions, as simpler, a goal of coding the
"mediating" controller part of an app.

The user interface consists of Tank, the Tank's tower
("gun barrel"), Deflector, buttons, and the Background widget for
receiving touch events. Code was moved from these to the statechart.
Tank and Deflector remained with more code, because they work, in part,
as autonomous user interface elements. Deflector still has code that
can be moved to the statechart. As the original widgets were pared
down, separate source files were collapsed to main.py, with the kv
file remaining largely unmodified.

The statechart drawing changed quite a bit in an incremental fashion,
with refactoring happening as two books about statecharts on hand
were consulted (Harel and Politi, 1998, "Modeling Reactive Systems
With Statecharts: The Statemate Approach" and Horrocks, 1999,
"Constructing the User Interface with Statecharts"). Learning the
graphics program used to draw the statechart, yEd, was also important.
yEd does not have a dedicated "statechart" menu of graphics
drawing elements, but does have a menu of general "flowchart" drawing
features and several menus that are close in application: UML and
BPMN (Business Process Modeling Notation). From these, an assortment
of rounded rectangle, double-bordered rectangle, arrow, circle, and
annotation drawing objects were used. This assortment could be made
into a menu for statechart drawing, after the dust settles on the
notation preferred. Some invention of new notation was done in
the course of work on this project. View the statechart drawing
and please express likes and dislikes.

Using statecharts brings to the forefront the "art of programming,"
where thinking in the abstract and imagination are important. You can
go back and forth between a focus on the graphics representation of
app design, to the code, at once shifting the mental process. With
either emphasis, imagination is important: "thinking graphically," vs.
"thinking in code." When writing an app from scratch, following the
suggestion in the books and other sources, you would start drawing the
statechart at the get-go, and might stay in "graphics mode" for an
extended period to get the statechart fleshed out, then closer to
fully developed. At some point, you would dive in to coding, in constant
consultation to the statechart drawing, and with frequent revision,
as the act of coding prompts for details. It is very much an
iterative process, and can present a heightened sense of programming
"satisfaction." Whether the programmer's strong suit is "thinking
graphically" or "thinking in code," both are involved. Although work
on this project has been to "reverse engineer" an existing app, after
initial fits and starts, the process became more streamlined, as
described.

Several aspects of statecharts and of a treatment in Python were
examined along the way. A statechart is hierarchical, and there is
more than one way to arrange states in an app. As development 
proceeds, more "correct" arrangements are discovered. More "correct"
involves notions of simplicity and effectiveness -- dare we say, it
equates to "more parsimonius." Refinement is an apt term used for the
statechart programming process. 

Through establishing and modifying the hierarchy, the similarity to
subclassing in object-oriented design may come to mind, as, for
instance, when considering the arrangement of the "collision" section
of the BulletMoving state. Actual Python subclassing is used
in concert, with CollisionWithEdge and CollisionWithObstacle
subclassing CollisionWithObject. Here the statechart drawing depicts
the hierarchy, and the code reflects the hierarchy, in the way the states
are indented as substates, and in the way the states are declared as
subclasses. There can be tradeoffs, but this is the way development
proceeded in this case. Subclassing states may not always be needed,
or desired.

Another aspect of statechart programming came up: the choice of putting
code in action functions vs. creating transient states. After
experimenting, transient states seemed to offer a more fine-grained
organization that made drawing the statechart easier. Transient
states are marked with dashed lines in the statechart drawing. They
might have some processing code, or not, and this code can be
substantial, involving several utility functions in the body of the
state, but there is a gotoState() call at the end of enterState() to
move control directly to another state.

yEd Operation
=============

The statechart drawing was made with yEd, a free cross-platform tool.
The program was used on MAC OS X, in this project.

yEd is a very capable program dedicated to the task of drawing diagrams
like statecharts, although there is no (yet) dedicated palette for
statecharts. It is like other vector-drawing programs, generally, but
has a difference or two that are noteworthy.

To move an element, don't click and drag it, click it once to select it,
then drag it. This is to disambiguate click-and-drag ops done for
drawing connectors.

The connector-handling and labels of connectors is a strong suit of
yEd. With an arrow object selected from in a menu, e.g., the sequence
flow arrow under the BPMN palette menu, you click away from any graphics
element to make sure nothing is selected, then you drag from one state
to another to draw the connector, hovering over the interior of the
target state to connect to its center, or hovering over one of its
borders to connect to a border. Use the detailed Properties View at
lower right in the yEd display to add a label, by clicking in the box
next to "Text" -- a dialog will pop up. After adding text for the label,
click or double-click the label to change it. Click to fire the dialog
again if you prefer. Click once to select the label, then drag it to one
of six positions, by default, that dynamically appear for the label drag.
There are several choices for label positioning -- resort to "Smartfree:
Anywhere" when you need special label placement.

Complicated selection, as with any vector-drawing tool, can be a bit
fiddly. Combine single-click ops with the shift and control keys, along
with marquee selection with the mouse. 

Statechart Notation Notes
=========================

The notation used is probably fairly standard for statechart drawings,
but a couple of items need explanation or comment:

Connection Symbology: State Transitions
---------------------------------------

"Edges," in the sense of a graph, are shown in the statechart drawing
as arrows connecting states. These represent state transitions that
happen when certain events occur, and are labeled with the "action" to
be performed and the triggering event. These state transition "edge"
labels have the action first and a description of the event (a trigger,
a requirement, a guard condition, etc.) shown in parentheses, e.g.
show_level_accomplished (goal hit). The action names are the names
of the actual Python functions in the states. This notation follows
the style in the Horrocks book. In the Harel and Politi book,
the notation is to use a slash, which would be something like:
show_level_accomplished / goal hit. Use of parentheses seems to
convey better that the thing in parentheses is the explanation of
the reason for the action.

Double Borders: "States with Substates"
---------------------------------------

A double-bordered rectangle is used for ShowingGameScreen and
ShowingLevel states, which is consistent with the style for
representing "a state with substates" seen on some websites and
examples. The double-border usage is not seen in either the Harel
and Politi or Horrocks books. The "state with substates" arrangement
should be apparent, just by looking at the encapsulation of shapes
within shapes, so there should be some additional meaning. For this
project, double bordered states are "major" states, but the usage is
arbitary -- should BulletMoving also be considered a "major" state?
Why use double borders at all? Shading can also be used to draw
attention to a composite state, as they are sometimes called.

Dashed Borders: Transient States
--------------------------------

Transient states are marked on the statechart drawing by dashed
borders. Neither the Harel and Politi nor the Horrocks books use
the dashed border notation, but it is used in other statechart
treatments, and is visually appropriate. The term transient, as
used by Horrocks, is preferred over the term transitional,
because of connotation and to lessen confusion with the general
use of "state transition" in discussion.

Transient states can fire to the next state for a variety of
reasons and means of decision:

  -- immediate transition (Can be an isolated "stand alone" state
     (See ChangingTrajectory or ShowingLevelAccomplished states),
     or perhaps the state is a substate of an "or-state" in the
     sense of Harel: See substates of the Collision state.)

  -- transition after a bit of conditional logic (Effectively,
     this is what the structure of the CollisionWithObject state
     and its two substates do. Contrast this with what could be done
     in a single state with an if statement in its enterState.
     Having discrete CollisionWithEdge and CollisionWithObstacle
     states, however, offers a clearer picture, pardon the pun.)

  -- transition after a call to a database (Horrocks uses this as
     an example. Consider that at the time of the event causing the
     database call, the next state transition can perhaps not be
     known. Only after information has been gathered by the call, e.g.
     for the status of a record, can the next state be decided.)

  -- transition after a substantial processing sequence (This item
     is added here to emphasize that transient states, anti the
     typical use of the term in everyday life, do not have to fire
     immediately to the next state.)

  -- transition after a timer (e.g., the ShowingLevelAccomplished
     state, which pops up an image for a few seconds, then goes to
     the ShowingLevel state to load the next game level.)

-----------------------------------------------------------------

The original Deflectouch README is shown from here down.

-----------------------------------------------------------------

Deflectouch
==============

![game play](http://a4.sphotos.ak.fbcdn.net/hphotos-ak-ash4/336216_290902887635727_1130435368_o.jpg)
![help screen](http://a6.sphotos.ak.fbcdn.net/hphotos-ak-ash4/412143_290904047635611_100001480546056_829367_173788384_o.jpg)
![levels](http://a8.sphotos.ak.fbcdn.net/hphotos-ak-ash4/325221_290902854302397_100001480546056_829364_127504812_o.jpg)
![settings](http://a2.sphotos.ak.fbcdn.net/hphotos-ak-snc7/324444_290902874302395_100001480546056_829365_1671324817_o.jpg)


**[Thread on NUI-group](http://nuigroup.com/forums/viewthread/13600/)**

**[Youtube video](http://www.youtube.com/watch?v=1Qa98oSPgi0)**

READ THIS FIRST
---------------

This application runs on the open source multitouch framework <Kivy>.
For informations on the Kivy framework, please refer to http://kivy.org

To install Kivy on your computer, see the Kivy documentation at
http://kivy.org/docs/installation/installation.html

...or, for windows, read the section "Getting Started under Windows" which is a
heavily summarized version of the above one.


Copyright and Contact
---------------------

Deflectouch Copyright (C) 2012 Cyril Stoller

This program comes with ABSOLUTELY NO WARRANTY. This is free software,
and you are welcome to redistribute it under certain conditions;
see the source code for details.

For comments, suggestions or other messages contact me at:
cyril.stoller@gmail.com


Credits
-------

* Sound:
  * beep.ogg, reset.ogg, select.ogg and switch.ogg are from the game *GUNSHIP!* from Microprose
  * All other sound files are created by myself
* Music:
  * The deflectouch.ogg song is created by myself
* Images:
  * www.gestureworks.com


Release Notes
-------------

Release history:

* **V1.0**: *first released version*

