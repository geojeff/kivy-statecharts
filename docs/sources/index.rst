.. kivy-statecharts documentation master file, created by
   sphinx-quickstart on Fri Sep 14 15:29:50 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

kivy-statecharts
================

Contents:

.. toctree::
   :maxdepth: 2

kivy-statecharts is a port of the Ki/SproutCore statechart framework to
Python for use in Kivy projects.

Original repos: `Ki <https://github.com/frozenCanuck/ki>`_ and
`SC.Statechart <https://github.com/sproutcore/sproutcore/tree/master/frameworks/statechart>`_

SC.Statechart was used as the basis for this port to Python and Kivy.

Installation
------------

kivy-statecharts is a standalone Python module that you may wish to put
alongside your local clone of Kivy if you are doing development. For
development, consider the following setup:

~/Development/kivy/kivy, for a Kivy clone, and
~/Development/kivy/kivy-statecharts, for a kivy-statecharts clone.
Add the kivy-statecharts directory to PYTHONPATH so imports would will during
development.

Tests
-----

Unit tests are done with
`nose <http://readthedocs.org/docs/nose/en/latest/>`_. In the
kivy\_statechart directory, run

::

    nosetests

As of April 2012, most tests were ported.

Introduction
============

The kivy-statecharts framework might be called "advanced," because it is an
add-on to basic widget, kv, and idiomatic Kivy programming style. However, as
we will see in the examples, even a simple application can be made using
statecharts. However, because there is a natural progression and dedicated
documentation for learning basic Kivy programming, it is assumed here that you
already understand Kivy bindings and the events system, how to build widgets
with both python and kv language approaches, and general concepts of using
Kivy.

Why Use Statecharts?
--------------------

Michael Cohen provided a good summary: https://github.com/FrozenCanuck/Ki.

If you are just starting to develop an app, consider using statecharts, even
though you may not see the advantage when your app is small.

If you aren't using statecharts, and you find yourself mired in complexity,
adapting your app to use statecharts should help.

Programming with statecharts can provide a comfort level, even for structuring
code for a basic application, and the facilities are there for realizing
solutions to handle complex situations such as those requiring concurrent
processing, intricate start-and-stop action for subprocesses, and so on. There
is a learning curve for these facilities, but it is probably worth the
investment.

Making a Statechart
-------------------

The developer may code the statechart for a new app directly, or a statechart
drawing may be done first. At some point, making a statechart drawing is
advised, but it is not required.

If the direct-coding method is used, the developer starts by writing the root
state and its primary substates, and from there builds up the hierarchy of
states. Individual states often code for specific views and widgets. This can
be done in a step-wise fashion, with the state for the main widget coded first,
followed by addition of new states as the user interface for the app is
constructed. The statechart will usually contain much or all of the application
logic code, as well as user interface definitions and operations.

If a statechart drawing is made either initially or after some coding has been
done, a piece of paper works fine for getting started, but there are good
drawing programs and python libraries that are recommended. Several of the
examples have drawings made with ``yEd``, a free diagram editor, or with the
``blockdiag`` python library. Some developers may have available commercial
tools such as ``OmniGraffle``, which is capable of drawing statecharts.

Look in the examples directory for a work-in-progress app called diagrammer
that aspires to make statechart diagrams, and may prove viable for other
drawing uses, for diagram generation from code, and for code generation from
a statechart diagram. As of Summer 2013, this app is getting the development
attention, for finding code layout, programming idioms, and structure that
define a set of best practices.

Regardless of methods used, the process of statechart construction is easy to
start by laying out what needs to happen as the app loads, and user interaction
begins.  As each user interface component and user action is envisioned, it is
drawn as a connector between states representing different parts of the user
interface or coded directly as the action method used to go to from one state
to another. More is added to the statechart, as details are realized and
considered through iterative testing of the app and coding.

Once the developer has the hang of the simple coding constructs, it is a
straightforward process to write code corresponding to states, action methods,
and state transitions.

For testing, a human-readable table of events and actions can be made
from the statechart, and test cases made to cover each item in the table.

States
======

In a typical case, there is a state for each major user interface element or
activity, and there may be substates for smaller elements. A state is coded as
a normal Python class, a subclass of the State class. Each state has an
enter_state() method and an exit_state() method. The given user interface
element involved in the activity is constructed or refreshed by code in the
enter_state() method, and the opposite, either bringing down or hiding, is
defined in code of the exit_state() method.  This makes for a very clean
design.

A state can have nothing to do with the user interface, however, and the same
arrangement of code applies. Any initialization or setup code needed for the
task at hand is done in the enter_state() method, and any tear-down type code
is put into the exit_state() method.

Utility methods and application code methods are added to a state also. As you
will find in the examples, having states available as "hubs" of application
flow, as holders of such applicaition code methods, is a very powerful concept.

Action methods are added to states to handle specific tasks triggered by user
action or code flow events. Action methods can call for a state transition,
which would entail, in turn, calling the state's exit_state() method and the
enter_state() method of the next state. 

Once you get the hang of those constructs, you will begin to think in terms of
states and state transitions, an approach that may seem unfamiliar at first,
but can be refreshing for long-time coders who have used a more informal style
of coding. The formalization offered by statecharts is not cumbersome after it
becomes familiar. You may wonder why anyone would prefer to code without it.
A well-designed system that does not use statecharts will in some fashion use
similar techniques in statecharts, so the question is probably moot.

Coding Style
------------

State classes may be declared "inline" in an indented fashion::

    class AppStatechart(StatechartManager):
        class RootState(State):
            class ShowingHelloWorld(State):
                ...
                code for state here
                ...

Or, state classes may be declared in their own files and imported to build the
statechart. An attractive approach is to put state classes in their own files
in a states package, e.g. myapp/states/showing_hello_world/ShowingHelloWorld.
They would be imported like this::

    from states.showing_hello_world import ShowingHelloWorld

and would be available by their class names in the source file where the
statechart is declared, e.g. as ShowingHelloWorld, and used in one of several
ways. An __init__() method and kwargs may be used to declare states::

    class AppStatechart(StatechartManager):
        class RootState(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'ShowingHelloWorld'
                kwargs['ShowingHelloWorld'] = ShowingHelloWorld
                super(RootState, self).__init__(**kwargs)

Or, you may prefer to declare them in shorthand fashion, that does not require
an __init__() method::

    class AppStatechart(StatechartManager):
        class RootState(State):
            initial_substate_key = 'ShowingHelloWorld'
            ShowingHelloWorld = ShowingHelloWorld

Regardless of coding style, for more deeply nested substates, we would declare
them in the same fashion to build a substate hierarchy in the statechart.

Example Apps
============

The examples are presented here in order of increasing complexity, before
turning to the academic background of statecharts.

Hello World Example App
-----------------------

The hello_world example app has a very simple statechart. With code removed,
the statechart consists of two states, the root state, and one app-specific
state called ShowingHelloWorld:

::

    class AppStatechart(StatechartManager):
        class RootState(State):
            initial_substate_key = 'ShowingHelloWorld'
            class ShowingHelloWorld(State):

The statechart is defined by the root state and its substates. The root state
has an initial substate set. Here, we only have one state, ShowingHelloWorld,
and it is the initial substate. When the statechart is instantiated, control
will flow immediately from the root state to the ShowingHelloWorld state.

**Running**

Change to the hello_world directory, then run python main.py, and
you should see the app appear. Type any of the letters in "hello world" and
you will see buttons for those letters randomly added in the app window.
Click any of the buttons, and likewise, more buttons will be added. That's
all it does -- but, pretty fancy for a "hello world" app, eh?

.. figure::  ../examples/hello_world/design/screencapture.png
   :align:   center

   Screen capture of HelloWorldApp

Each of the randomly placed buttons were added either by the keyboard or by
clicks/touches on any of the buttons after they have appeared.

**HelloWorldApp, main.py**

There is only one file for the app, main.py:

::

    from kivy.app import App
    from kivy.core.window import Window
    from kivy.uix.widget import Widget
    from kivy.uix.button import Button

    from kivy.properties import ObjectProperty

    from kivy_statecharts.system.state import State
    from kivy_statecharts.system.statechart import StatechartManager

    import random


    class HelloWorldView(Widget):
        app = ObjectProperty(None)

        def __init__(self, **kwargs):
            super(HelloWorldView, self).__init__(**kwargs)
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

        def _keyboard_closed(self):
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard = None

        def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
            if text in ['h', 'e', 'l', 'o', 'w', 'r', 'd']:
                self.app.statechart.send_event(text)

            if keycode[1] == 'escape':
                keyboard.release()

            return True


    class LetterButton(Button):
        statechart = ObjectProperty(None)

        def __init__(self, statechart, letter, **kwargs):
            self.statechart = statechart
            self.letter = letter
            super(LetterButton, self).__init__(**kwargs)
            self.bind(on_press=self.letter_clicked)

        def letter_clicked(self, *args):
            print 'letter clicked', self.letter
            self.statechart.send_event(self.letter)


    class AppStatechart(StatechartManager):
        app = ObjectProperty(None)

        def __init__(self, **kw):
            self.trace = True
            self.root_state_class = self.RootState
            super(AppStatechart, self).__init__(**kw)

        class RootState(State):
            initial_substate_key = 'ShowingHelloWorld'

            class ShowingHelloWorld(State):
                root = ObjectProperty(None)

                def enter_state(self, context=None):
                    print 'ShowingHelloWorld/enter_state'
                    self.root = self.statechart.app.root

                def exit_state(self, context=None):
                    print 'ShowingHelloWorld/exit_state'

                # Utility method:
                #
                def add_label(self, letter):
                    width, height = self.statechart.app.hello_world_view.size
                    button_size = (20, 20)

                    x = random.randint(0, width - button_size[0])
                    y = random.randint(0, height - button_size[0])

                    self.root.add_widget(LetterButton(self.statechart, letter,
                                                      pos=(x, y),
                                                      size=button_size,
                                                      text=letter))

                # Action methods:
                #
                def h(self, *args):
                    self.add_label('h')

                def e(self, *args):
                    self.add_label('e')

                def l(self, *args):
                    self.add_label('l')

                def o(self, *args):
                    self.add_label('o')

                def w(self, *args):
                    self.add_label('w')

                def r(self, *args):
                    self.add_label('r')

                def d(self, *args):
                    self.add_label('d')


    class HelloWorldApp(App):
        statechart = ObjectProperty(None)
        hello_world_view = ObjectProperty(None)

        def build(self):
            self.hello_world_view = HelloWorldView(app=self)
            return self.hello_world_view

        def on_start(self):
            self.statechart = AppStatechart(app=self)
            self.statechart.init_statechart()


    if __name__ in ('__android__', '__main__'):
        HelloWorldApp().run()

The definition for HelloWorldApp has a statechart property and a property for
the main widget, hello_world_view. The build() method instantiates
HelloWorldView and returns it -- the widget returned from build() is the root
widget, available as app.root. The on_start() method is called when the app is
run. This is when we instantiate the statechart. 

The app starts when HelloWorldApp().run() is called in main. build()
happens first, then on_start(), and the app and its statechart are up and
running.

We've already seen the basic structure of the statechart, but let's take a
more thorough look. 

First, AppStatechart has an app reference property, for convenience, that is
passed on instantiation. Any Kivy property defined in the body of a class is
automatically set if passed as an argument. You don't even have to have an
__init__() method, but here we do, because the trace and root_state_class
properties are set.

The only thing declared in the root state is the inital substate,
ShowingHelloWorld, which contains the basic functionality for the app.

**ShowingHelloWorld, enter_state() and exit_state()**

If enter_state() and/or exit_state() are defined for a state, these will be
called automatically at the appropriate times. In a larger app, you would
think about what needs to happen on enter and exit, such as creating and
showing a dialog in the enter_state, and tearing it down in the exit state,
or any manner of things that could happen. Here, we just print a message on
enter_state() and exit_state().

**Utility Methods**

A state, as a normal python class, can have properties, an __init__(),
specialized methods, etc. Here we are calling the add_label() method a
"utility" method, meaning a normal method that does whatever work is
necessary. add_label() creates a randomly located button for a given
letter in "hello world."

**Action Methods**

There is nothing special about the type of action methods used in the
hello_world app. The action methods here, h(), e(), l(), o(), w(), r(), and
d() respond to events of the same names: 'h', 'e', 'l', 'o', 'w', 'r', and
'd'. These events happen either from keyboard presses or from mouse clicks or
touches on letter buttons. When the app first loads, there are no letter
buttons until keyboard presses add some. Then the events could come from
additional keyboard presses or from the buttons.

Look at the HelloWorldView class for setup of the keyboard actions (We can use
the terms action and event interchangeably here). You see there that when a
key press happens, there is a call to statechart.send_event(letter), where
letter is one of the letters in "hello world."

In a larger app, action method names could be anything, but examples tend to
have a demonstrative aspect, such as collide_with_barrier(), for a game, or
load_users() for an admin panel, or delete_comment() for a media app.

It is easy to rapidly prototype an app, because of the organization you can do
with states and their actions, arranged in a hierarchy. You can do this in
code only, or you can draw out the statechart in a diagram before coding, or
you can use some combination of approaches, often in interation. A statechart
diagram for hello_world would be:

Before we leave the subject of action methods, there is an alternative to
having separate action methods, when there is a related set of events to be
handled, as we have with the letter events in our hello_world app. We could
define a single handler method, as follows:

::

    @State.event_handler(['h', 'e', 'l', 'o', 'w', 'r', 'd']) 
    def letter_event_handler(self, event, letter, context):
        self.add_label(letter)

This is a case where the event_handler method approach is a perfect fit. The
first line is a function decorator on the State class that marks
letter_event_handler() as a handler for all the events in the list.

**Statechart Diagram**

If a developer wanted, a full program using statecharts could be written in
code directly, by the established process of writing software "in your head."
However, using drawing programs or libraries, we can draw statechart diagrams
that can really aid the process, especially for more complicated software. As
this diagram shows, there are conventions we may follow in the drawing:

.. figure::  ../examples/hello_world/design/statechart.png
   :align:   center

   Statechart diagram for HelloWorldApp

There is a single open circle to mark the root state, and an arrow from that
to the initial state, ShowingHelloWorld. In this app, this is the only state.
The ShowingHelloWorld state responds to keyboard events, by creating new
letter buttons. Once a letter button exists, a click or touch event will also
fire a "letter event," resulting in the creation of yet another letter button.
There is also a representation of the app exit, which is triggered by a
control-C or by closing the app window.

Balls Example App
-----------------

Balls is a small Kivy app that bounces balls around the screen.  It is like
pong without the paddles, and with the capacity to send the balls out of
control. The kv file for the program, balls.kv, consists of the Ball class
and the BallsView main container class. Each ball is 50x50 in size, and begins
with a location at the center of the parent window.

.. figure::  ../examples/balls/design/screencapture.png
   :align:   center

   Screen capture of BallsApp

The BallsView class has a serve_balls() method, to get the balls moving, and
an update method that is called on a timer, every 1/60th of a second, to move
the balls.

The statechart has the same basic setup as HelloWorldApp, but in the
ShowingBalls state, a new concept for states is introduced. In HelloWorldApp,
there is only one state within the root state, however in BallsApp, there is a
ShowingBalls state, and within that five "moving ball" substates for each of
five balls. In many apps, states that are siblings of one another are
``independent`` (also termed ``orthogonal``) -- one or the other is active at a
given time. But in some apps, a set of sibling states can all be active at the
same time. These are called ``concurrent`` states. The ShowingBalls state
contains five concurrent substates, for each of the moving balls. Note the use
of the boolean property substates_are_concurrent. If you omit this property for
a state that contains substates, the substates will be independent of one
another (orthogonal), but here they are concurrent:

::

    class AppStatechart(StatechartManager):
        class RootState(State):
            initial_substate_key = 'ShowingBalls'
            class ShowingBalls(State):
                substates_are_concurrent = True
                class MovingBall_1(MovingBall):
                class MovingBall_2(MovingBall):
                class MovingBall_3(MovingBall):
                class MovingBall_4(MovingBall):
                class MovingBall_5(MovingBall):

The moving ball states each subclass MovingBall, a state which is defined
separately from the statechart -- recall that states are normal python
classes, so you may use your imagination for design of state subclassing in
the construction of state hierarchies. Each moving ball state controls the
movement of a given ball, and has its own unique velocity, designated simply
as 1, 2, 3, 4, and 5, respectively, for both velocity_x and velocity_y. Change
these for interesting effects. The associated between ball and state is
maintained by a ball_key key.

The balls are sped up by a key press of 'u' and slowed down by a key press of
'd'. When the 'u' key is pressed, the 'speed_up' event is sent to the
statechart, and, because each of the moving ball states is a sublass of
MovingBall, each has an action method named speed_up(), and so will respond
to that event. Likewise for the 'd' key and the 'slow_down' event, and the
slow_down() action method.

.. figure::  ../examples/balls/design/statechart.png
   :align:   center

   Statechart diagram for BallsApp

As you can see in the diagram, the 'speed_up' and 'slow_down' events are
``broadcast actions`` -- they apply to multiple states concurrently.

The combination of velocity adjustments in the enter_state() method for each
moving ball state, and the adjustments made in the speed_up() and slow_down()
methods, forms an algorithm for this app, giving an interesting effect, with
balls moving in all directions at different velocities. This was found by
experimentation. The process illustrates how the developer can learn to think
in the realm of statecharts: for a given state, what happens on entry, what
happens for given events, what happens on exit.

Fruits Example App
------------------

The "Fruits" example borrows from the set of examples for ListView in Kivy, and
uses ScreenManager along with the statechart to present four main user
interface screens: Lists (the equivalent of the list_cascade_dict.py example in
Kivy), Search, Data, and Detail. There are states for each of these screens:
ShowingListsState, ShowingSearchState, ShowingDataScreen, and
ShowingDetailScreen.  Views for each of the states are constructed the first
time their enter_state() methods are called. On subsequent transitions into the
states, the current screen in the ScreenManager instance is simply switched. No
tear-down tasks are needed in the exit_state() methods of the states, because
the screens are not destroyed on exit. Revisits to a screen will see it in its
previously visited state, except for the Detail screen, which always shows the
fruit selected in the Lists screen.

.. figure::  ../examples/fruits/design/screencapture.png
   :align:   center

   Screen capture of Fruits App

A toolbar at the top of each screen has buttons bound to action methods in the
states, of the form go_to_search(), go_to_data(), etc. Each of these methods
does a state transition with a call such as go_to_state('ShowingSearchState').

The screen capture shows the Search screen, which has text boxes for the lower
and upper bounds of search criteria for each of the fruit data properties. On
the right is a list of all the fruits, with the ones matching the current
search criteria shown in red. In the example, we see fruits that have protein
values between 5 and 16 grams per serving.

The "Data" screen shows a list of the raw data values for reference when making
search criteria. The "Detail" screen shows the data for the fruit currently
selected in the "Lists" screen.

The "Fruits" example shows how the statechart itself can be used as a storage
point for application data. Likewise, properties and methods of individual
states are related to the views the state classes serve. Here are the states
and methods of the "Fruits" app statechart, with code collapsed::

    class AppStatechart(StatechartManager):
        def create_searchable_data(self):
        def create_adapters(self):
        class RootState(State):
            initial_substate_key = 'ShowingListsScreen'
            class ShowingListsScreen(State):
                def enter_state(self, context=None):
                def exit_state(self, context=None):
                def create_adapter_bindings(self):
                def fruit_category_changed(self, fruit_categories_adapter, *args):
                def fruit_changed(self, list_adapter, *args):
                def go_to_search(self, *args):
                def go_to_data(self, *args):
                def go_to_detail(self, *args):
            class ShowingSearchScreen(State):
                def enter_state(self, context=None):
                def exit_state(self, context=None):
                def list_item_args_converter(self, row_index, record):
                def criterion_entered(self, text_input):
                def search(self):
                def go_to_lists(self, *args):
                def go_to_data(self, *args):
                def go_to_detail(self, *args):
            class ShowingDataScreen(State):
                def enter_state(self, context=None):
                def exit_state(self, context=None):
                def go_to_lists(self, *args):
                def go_to_search(self, *args):
                def go_to_detail(self, *args):
            class ShowingDetailScreen(State):
                def enter_state(self, context=None):
                def exit_state(self, context=None):
                def go_to_lists(self, *args):
                def go_to_search(self, *args):
                def go_to_data(self, *args):

The statechart has several methods for setting up data and adapters. There is a
root state, with 'ShowingListsScreen' set as the initial state. And, there are
the four states for showing the screens in the app. Each of these states has an
enter_state() and exit_state() method. The enter_state() method of each state
contains the bulk of the code in the app. The Data and Detail screen states are
simple: they only contain enter_state() and exit_state() methods along with
methods for transitioning to the other states. The Lists and Search screen
states are substantial, and have utility and action callback methods that form
an important part of application logic.

.. figure::  ../examples/fruits/design/statechart.png
   :align:   center

   Statechart diagram for Fruits App

The statechart diagram shows that any of the states have possible transitions
to any other state, in a simple tabbed app design.

ShuttleControl Example App
--------------------------

The ShuttleControlApp example presents a graphical display of the thrusters in
the Space Shuttle's Reaction Control System (RCS), as an overlay of labels and
buttons on a technical drawing.

.. figure::  ../examples/shuttle/design/screencapture.png
   :align:   center

   Screen capture of ShuttleControlApp

There are 44 individual thrusters, grouped into 14 thruster groups. Thrusters
are not fired individually, but as sets, in the 14 groups. The blue buttons
along the bottom of the display are clicked/touched to fire thrusters in the
the groups. If you repeatedly fire a group, you will see the thrusters in the
group begin to pulsate, getting larger with more thrust applied. The list on
the left and the table display at the top are also updated for individual
thruster amount. If you want to decrease thrust, toggle the "more / less"
control mode at left center.

There is really just one main state, ShowingThrusterControls, which contains
states for each of the 14 thruster groups.


.. figure::  ../examples/shuttle/design/statechart.png
   :align:   center

   Statechart diagram for ShuttleControlApp

The Thruster_Group_x states are concurrent, so multitouch is allowed. If this
were a real app, say for an astronaut cockpit display, the layout of the RCS
control buttons (blue) could be rearranged into something more intuitive, but
this example app just plops a UI on top of a technical drawing.

Deflectouch-With-Statecharts App
--------------------------------

The Deflectouch app was written by Cyril Stoller for a Kivy game competition,
which it won (https://github.com/stocyr/Deflectouch). It is modified here to
adapt for statecharts, without fundamentally changing the design of the game,
through moving blocks of code around, simplifying where possible, and adding
necessary bits here and there. The game presents a tank on the left, which
has a moveable barrel, a game screen with barrier blocks and blue target
blocks, and a button panel at right. If you have a clear line of sight to a
target, you can just aim and fire. However, usually the barriers are in the
way, so you must create deflectors with a two-finger pinch-and-expand action.
You are limited by the amount of deflector "stock," which is shown in a bottom
bar graph display. So, you can create more than one deflector, but there is a
limit to how long the sum-total length of deflectors can be -- sometimes you
need to do multiple deflections around corners.

.. figure::  ../examples/deflectouch_with_statecharts/design/screencapture.png
   :align:   center

   Screen capture of Deflectouch-With-Statecharts App

The statechart diagram for the Delectouch-with-statecharts app shows several
major areas of concern. There are the main display states at top left, actions
and states for deflectors toward top right, all that happens when a bullet is
in flight at bottom right, and the rest as odds and ends at left, and at far
right, where you see the game level changing action.

.. figure::  ../examples/deflectouch_with_statecharts/design/statechart.png
   :align:   center

   Statechart diagram for Deflectouch-With-Statecharts App

A new concept is introduced here for states: transient states, which are shown
by dashed line borders. These states do something in their enter_state()
method, then immediately fire to another state. You also see that the Tank is
autonomous -- it doesn't send events to the statechart, it has internally
operating bindings between touch events and moving and barrel adjustment
methods. Deflector has one autonomous function like that, for moving, but the
other events fire to the statechart.


Academic Background of Statecharts
==================================

You may wish to explore the origins of the statecharts concept. We can start
with a look at the primary source of inspiration for Michael Cohen's Ki
project, the paper by David Harel, *Statecharts: A Visual Formalism for Complex
Systems*, Sci.  Comput. Programming 8 (1987), 231-274 `pdf
<http://www.wisdom.weizmann.ac.il/~harel/SCANNED.PAPERS/Statecharts.pdf>`_.
David Harel is a computer scientist at the Weizmann Institute of Science,
Rehovot, Israel, who has published widely on this and related topics in
programming. In the list of `David Harel's publications
<http://www.wisdom.weizmann.ac.il/~harel/papers.html>`_, the 1987 paper is #48
on the list, having come from a preliminary version published in 1984. If you
scan the list for more recent offerings, you see some that pertain to
statecharts in the pure programming sense of style, efficiency, software
maintenance, etc., while others highlight the use of statecharts in specific
subject areas, such as biological modeling. There is a larger literature, and
many software projects that relate, but this list of Harel's publications
serves as a good representation and starting point for a survey.

For an interesting personal account by Harel on the germination of the
idea of statecharts, see: `Statecharts in the Making: A Personal
Account <http://www.wisdom.weizmann.ac.il/%7Eharel/papers/Statecharts.History.pdf>`_.

A Wikipedia article on `state
diagrams <http://en.wikipedia.org/wiki/State_diagram>`_, is good to read
for the nature of the "Harel statechart" as a formalization of certain
aspects of modeling the behavior of a system with a state diagram. From
the article::

    "With Harel statecharts it is possible to model multiple cross-functional
    state diagrams within the statechart. Each of these cross-functional state
    machines can transition internally without affecting the other state
    machines in the statechart. The current state of each cross-functional
    state machine in the statechart defines the state of the system. The Harel
    statechart is equivalent to a state diagram but it improves the readability
    of the resulting diagram."

Reading the 1987 paper by Harel, you see in the abstract of the paper that
statecharts concern "the notions of hierarchy, concurrency, and communication."
Statecharts offer formalization to modularize code in a hierarchy of states
that exist as discrete blocks that can act independently or concurrently, and
communicate within an event system, allowing easier modeling of complexity.

So, statecharts help us build complex systems? Yes they do, but simple ones
too. What software application stays simple for very long?  Not many.
Especially systems that involve many interacting parts. Typical software
programs are "reactive" systems in the parlance of the 1987 Harel paper.

From the parlance of the Harel paper, here are some terms and concepts as used
there, paraphrasing from the text:

**reactive system** -- an event-driven system that must react to
external and internal stimuli driving behavior through sequences of
changing conditions, relationships, events, and timing contraints.

**transformational system** -- systems in which a relationship between
input and output is treated by a transformation, a function.

**state diagram** -- simple directed graph of states and transitions,
with nodes denoting states and arrows denoting transitions, which may be
labelled with triggering conditions and guarding conditions.

**superstate, "clustering," hierarchy, depth** -- A "cluster" of states
is related somehow, e.g., "all airborne states." States are arranged
hierarchically, with the hierarchy containing clusters of related states
at various "levels." The visual side of statecharts is important, and
you might prefer to "draw it out," but you should be able to imagine how
the hierarchy set up in code is like a machine set up to react to
events.

**orthogonal** -- independent. Contrast this with concurrent.

**concurrent** -- simultaneous. Contrast this with orthogonal, or
independent.

**broadcast communication** -- event-driven, with the capability to send
an event that can trigger action across states.

From these terms, perhaps you can appreciate this, also from the Harel paper:

::

    statecharts = state-diagrams + depth + orthogonality + broadcast-communication

(where orthogonality implies functionality for handling concurrency as
well).

To attempt a paraphrase:

::

    Statecharts add to basic state-diagrams the functionality to arrange
    states in a hierarchy, specifying which states are independent of one
    another and which ones are concurrent with each other. Action methods
    within states respond to events delivered to the statechart. Events
    firing to the action methods may have broadcast effect across multiple
    related or concurrent states.


Statecharts and Terminology in MVA/MVC Systems
----------------------------------------------

MVA = Model-View-Adapter System

MVC = Model-View-Controller System

Statecharts form part of the "controller layer" in traditional MVC systems,
when statecharts are present, serving in the coordinating controller realm.

Kivy is a hybrid MVA/MVC system.  Although the term ``controller`` has been
used sparingly in the documentation for Kivy, the term ``adapter`` became a
formal part of the system with the addition of kivy/adapters in Kivy 1.5.
Adapters in Kivy are bridges between views and data models, but serve something
of a dual role, being controller-like in the way data is accessed for views and
how selection is managed, and acting in a view-servicing capacity, as a view
building/managing/caching system for multi-view widgets such as ListView. 

Statecharts are applicable to software systems in general, but Kivy, like so
many other systems, involves code for building a user interface with buttons
and sliders and lists and custom views, tied to models of record types by means
of bindings generally, and adapters for ListView and related multi-view
widgets. The property bindings and observer system in Kivy is sophisticated,
like that used in controllers in MVC systems.

Regardless of terminology used for controllers, bindings, adapters, and the
like, Kivy is a strongly "reactive" system, so is very amenable to statechart
treatment.

For learning about "adapters/controllers" and terminology, we can read blog and
mailing list posts by Michael Cohen (nick: frozencanuck), the original author
of the statecharts framework ported here from SproutCore. It will help you to
appreciate that SproutCore is based on Cocoa. In Cocoa, we see differentation
between coordinating vs. mediating controllers.

Mediating controllers are a bit lower-level than coordinating controllers.
Mediating controllers have some sort of backing content, usually data models
with record types used in the system, that needs updating per user action in
user interface views.

Coordinating controllers are more general than mediating controllers, and
contain broader level application logic. Differences between these types of
controllers are subtle and can be confused, a subject addressed by Michael
Cohen in an important `blog post
<http://frozencanuck.wordpress.com/2011/03/09/sproutcore-statecharts-vs-controllers/>`_
and this succinct `mailing list post <https://groups.google.com/forum/#!msg/sproutcore/dn1HN8Wtwf8/U3qDW_bb9QkJ/>`_.
The upshot of discussion is that the higher level logic blocks in
controllers will often "turn into brutish monsters containing many if-else or
switch-case statements" to be able to manage application state. Statecharts
fix the problem of over-stuffed controllers, perhaps with "spagetti code,"
and adds clean logic to the system, offering structure to better coordinate
an application.

Kivy also now has adapters, so we have another term to examine. Adapters, as
described in this `article <http://en.wikipedia.org/wiki/Model–view–adapter/>`_,
have a more "linear" relationship to data and views. An adapter serves more
directly to "service" a view, to help create the view or its child views, by
interacting with data as needed. Kivy gets its adapter system, in part, from
Adroid, although it has some aspects, for selection especially, that come from
Cocoa / SproutCore. Where you have read above about the term "controller," you
can mostly do direct substitution for the term adapter. We may settle on a
split in Kivy, where we have a "controller layer" that consists, as of Summer
2013, of:

* controllers - Should be kept lean and mean; do not create and cache views;
  stick to the roles of mediating to data, selection, and filtering. May
  contain raw data record type items, views, such as shapes in a graphical
  application, etc., but the management of the items is by external control.
  The API is the same as the Kivy property wrapped, with the addition of
  filtering methods, AliasProperty "computed property" interfaces, etc.

* adapters - Very similar to controllers, but doing a view servicing job for
  some collection view, such as the ListView widget. This servicing includes
  caching views so that scrolling and other intensive filtering of data item
  views it more efficient.

* statecharts - (One or more) Contains states in a hierarchy, with code for
  the main application logic; Code can become substantial, in contrast to the
  restricted scope of the leaner controllers and adapters. Coordinates the
  loading of data into controllers and adapters when needed, and does
  construction, management, and destruction of user interface elements as user
  action dictates.

* Widgets, which are essentially views primarily, contain Kivy properties,
  which act as mediating controllers. This is copacetic. However, with the
  proper use of controllers, adapters, and states in statecharts, the amount of
  code in widgets for performing "coordinating controller" "application logic"
  is minimized.

Please follow development of the diagrammer app to see how it pans out!

Summary
-------

Kivy has a strong property and bindings system, whereby a close view-mediating
controller coupling is built into widgets.  Kivy has adapters for ListView and
related views that partly serve in a mediating role as well.

Using these mediating controller features, along with a statechart providing
the coordinating controller framework, a robust controller system can be built
for an app.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

