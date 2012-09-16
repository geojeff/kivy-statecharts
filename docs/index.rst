.. kivy-statecharts documentation master file, created by
   sphinx-quickstart on Fri Sep 14 15:29:50 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to kivy-statecharts's documentation!
============================================

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
~/Development/kivy/kivy\_statechart, for a kivy-statecharts clone. Both
were added to PYTHONPATH in ~/.profile so imports would work during
development, as:

::

    export PYTHONPATH=$PYTHONPATH:/Users/geojeff/Development/kivy/kivy:/Users/geojeff/Development/kivy 

Tests
-----

Unit tests are done with
`nose <http://readthedocs.org/docs/nose/en/latest/>`_. In the
kivy\_statechart directory, run

::

    nosetests

As of April 2012, most tests were ported.

In a Nutshell
=============

The developer draws a statechart -- on a piece of paper is fine, but
there are good drawing programs. This process is easy enough to start
laying out what needs to happen as the app loads, and user interaction
begins. As each user action is envisioned, it is drawn as a connector
between states representing different parts of the user interface. More
is added to the statechart, as details are realized and considered.

Once the developer has the hang of the simple coding constructs, it is a
straightforward process to write the code corresponding to states and
transitions on the statechart.

Iteration of refining the statechart and writing code goes along as the
app develops.

For testing, a human-readable table of events and actions can be made
from the statechart, and test cases made to cover each item.

Example Apps
============

The examples directory contains several brand new apps and some of the Kivy
example apps adapted to use statecharts. These examples are presented in
order of increasing complexity, before turning to theoretical background for
statecharts.

Hello World Example App
-----------------------

The hello_world example app has a very simple statechart. With code removed,
the statechart consists of two states, the root state, and one app-specific
state called ShowingHelloWorld:

::

    class AppStatechart(StatechartManager):
        class RootState(State):
            initialSubstateKey = 'ShowingHelloWorld'
            class ShowingHelloWorld(State):

The statechart is defined by the root state and its substates. The root state
must have an initial substate or substatesAreConcurrent = True explicitly
defined. Here, we only have one state, ShowingHelloWorld, and it is the
initial substate. When the statechart is instantiated, control will flow
immediately from the root state to the ShowingHelloWorld state.

**Running**

Change to the hello_world directory, then run python main.py, and
you should see the app appear. Type any of the letters in "hello world" and
you will see buttons for those letters randomly added in the app window.
Click any of the buttons, and likewise, more buttons will be added. That's
all it does -- but, pretty fancy for a "hello world" app, eh?

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
                self.app.statechart.sendEvent(text)

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
            self.statechart.sendEvent(self.letter)


    class AppStatechart(StatechartManager):
        app = ObjectProperty(None)

        def __init__(self, **kw):
            self.trace = True
            self.rootStateClass = self.RootState
            super(AppStatechart, self).__init__(**kw)

        class RootState(State):
            initialSubstateKey = 'ShowingHelloWorld'

            class ShowingHelloWorld(State):
                root = ObjectProperty(None)

                def enterState(self, context=None):
                    print 'ShowingHelloWorld/enterState'
                    self.root = self.statechart.app.root

                def exitState(self, context=None):
                    print 'ShowingHelloWorld/exitState'

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
            self.statechart.initStatechart()


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
__init__() method, but here we do, because the trace and rootStateClass
properties are set.

The only thing declared in the root state is the inital substate,
ShowingHelloWorld, which contains the basic functionality for the app.

**ShowingHelloWorld, enterState() and exitState()**

If enterState() and/or exitState() are defined for a state, these will be
called automatically at the appropriate times. In a larger app, you would
think about what needs to happen on enter and exit, such as creating and
showing a dialog in the enterState, and tearing it down in the exit state,
or any manner of things that could happen. Here, we just print a message on
enterState() and exitState().

**Utility Methods**

A state is a normal python class. It can have properties, an __init__(),
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
key press happens, there is a call to statechart.sendEvent(letter), where
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

    @State.eventHandler(['h', 'e', 'l', 'o', 'w', 'r', 'd']) 
    def letter_event_handler(self, event, letter, context):
        self.add_label(letter)

This is a case where the eventHandler method approach is a perfect fit. The
first line is a function decorator on the State class that marks
letter_event_handler() as a handler for all the events in the list.

**Statechart Diagram**

If a developer wanted, a full program using statecharts could be written in
code straight-up, by the established process of writing software "in your
head." However, using vector drawing programs, we can draw statechart diagrams
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

The BallsView class has a serve_balls() method, to get the balls moving, and
an update method that is called on a timer, every 1/60th of a second, to move
the balls.

The statechart has the same basic setup as HelloWorldApp, but in the
ShowingBalls state, a new concept for states is introduced. In HelloWorldApp,
there is only one state within the root state, however in BallsApp, there is
a ShowingBalls state, and within that five "moving ball" states for each of
five balls. In many apps, states that are siblings of one another are
independent (also termed orthogonal) -- one or the other is active at a given
time. But in some apps, a set of sibling states can all be active at the same
time. These are called concurrent states. The ShowingBalls state contains five
concurrent substates, for each of the moving balls. Note the use of the
boolean property substatesAreConcurrent. If you omit this property for a state
that contains substates, the substates will be independent of one another
(orthogonal), but here they are concurrent:

::

    class AppStatechart(StatechartManager):
        class RootState(State):
            initialSubstateKey = 'ShowingBalls'
            class ShowingBalls(State):
                substatesAreConcurrent = True
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

The combination of velocity adjustments in the enterState() method for
each moving ball state, and the adjustments made in the speed_up() and 
slow_down() methods, forms an algorithm for this app, giving an interesting
effect, with balls moving in all directions at different velocities. This was
found by experimentation. The process illustrates how the developer can
learn to think in the realm of statecharts: what happens on entry, what
happens for given events, what happens on exit.

Background
==========

If you are new to statecharts, or want to learn about them, you may
wish to explore the origins of the concept. We can start with a look at
the primary source of inspiration for Michael Cohen's Ki project, the
paper by David Harel, *Statecharts: A Visual Formalism for Complex
Systems*, Sci. Comput. Programming 8 (1987), 231-274
`pdf <http://www.wisdom.weizmann.ac.il/~harel/SCANNED.PAPERS/Statecharts.pdf>`_.
David Harel is a computer scientist at the Weizmann Institute of
Science, Rehovot, Israel, who has published widely on this and related
topics in programming. In the list of `David Harel's
publications <http://www.wisdom.weizmann.ac.il/~harel/papers.html>`_,
the 1987 paper is #48 on the list, having come from a preliminary
version published in 1984. If you scan the list for more recent
offerings, you see some that pertain to statecharts in the pure
programming sense of style, efficiency, software maintenance, etc.,
while others highlight the use of statecharts in specific subject areas,
such as biological modeling. There is a larger literature, and many
software projects that relate, but this list of Harel's publications
serves as a good representation and starting point for a survey.

For an interesting personal account by Harel on the germination of the
idea of statecharts, see: `Statecharts in the Making: A Personal
Account <http://www.wisdom.weizmann.ac.il/%7Eharel/papers/Statecharts.History.pdf>`_.

A Wikipedia article on `state
diagrams <http://en.wikipedia.org/wiki/State_diagram>`_, is good to read
for the nature of the "Harel statechart" as a formalization of certain
aspects of modeling the behavior of a system with a state diagram. From
the article, "With Harel statecharts it is possible to model multiple
cross-functional state diagrams within the statechart. Each of these
cross-functional state machines can transition internally without
affecting the other state machines in the statechart. The current state
of each cross-functional state machine in the statechart defines the
state of the system. The Harel statechart is equivalent to a state
diagram but it improves the readability of the resulting diagram."

Reading the 1987 paper by Harel, you see in the abstract that
statecharts concern "the notions of hierarchy, concurrency, and
communication." Statecharts offer formalization to modularize code in a
hierarchy of states that exist as discrete blocks that can act
independently or concurrently, and communicate within an event system,
allowing easier modeling of complexity.

So, statecharts help us build complex systems? Well, yes, but simple
ones too. Besides, what software application stays simple for very long?
Not many. Especially systems that involve many interacting parts --
typical software programs are "reactive" systems in the parlance of the
1987 Harel paper.

Speaking of the parlance of the Harel paper, here are some terms and
concepts as used there, paraphrasing from the text:

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

Kivy seems closer to MVA, but ongoing current work on the framework will
help to clarify. MVA/MVC terms are mentioned here because you will not
see the term "controller" used much in Kivy, and the term "adapter" is
just now starting to be used.

Statecharts are applicable to software systems in general, but Kivy,
like so many other systems, involves a user interface with buttons and
sliders and lists and custom views, tied to models of record types by
means of adapters or controllers. Kivy has a sophisticated property
bindings and observer system that is more similar to MVA design, than to
MVC systems, generally. Regardless, whatever terminology is used, Kivy
and other similar systems are "reactive" systems, so are amenable to
statechart treatment.

Statecharts enhance the traditional MVA/MVC system. Where you may find
some sort of event and callback system forming "adapter/controller"
functionality, statecharts offer formalization beyond that, helping the
programmer think more clearly about discrete elements and interactions.

For learning about "adapters/controllers" and terminology, we can read
blog posts by Michael Cohen (nick: frozencanuck), the original author of
the statecharts framework ported here from SproutCore. It will help you
to realize that SproutCore is based on Cocoa. In Cocoa, we see
differentation between coordinating vs. mediating controllers. Mediating
controllers are a bit lower-level than coordinating controllers.
Mediating controllers have some sort of backing content, usually data
models with record types used in the system, that needs updating per
user action in user interface views.

Coordinating controllers are more general than mediating controllers,
and contain broader level application logic. Differences between these
types of controllers are subtle and can be confused, a subject addressed
by Michael Cohen in an important `blog
post <http://frozencanuck.wordpress.com/2011/03/09/sproutcore-statecharts-vs-controllers/>`_.
The upshot of the blog post is that the higher level logic blocks in
controllers will often "turn into brutish monsters containing many
if-else or switch-case statements to know what state the application is
currently in."

Statecharts for Kivy
--------------------

Kivy has adapters that are like mediating controllers. Kivy has a
property and bindings system, whereby a kind of view-mediating adapter
coupling is built as a custom Widget.

Kivy does not formally have coordinating controllers.

Code in Kivy that plays the "coordinating controller" role can be found
in specific functions written to respond to user actions. A great
example of clean layout for this can be seen in the DeflectTouch game
that won the first Kivy app competition. For example, look at the
substantial code in the level\_button\_pressed() function:
https://github.com/stocyr/Deflectouch/blob/master/main.py#L181 -- this
is "coordinating controller" code.

The code in the DeflecTouch level\_button\_pressed() function could just
as well be put in a "ShowingMainScreen" state, in a "show\_levels"
action method. Rewriting DeflecTouch with statecharts would simply
entail moving such code into discrete states, and to action methods
that respond to events such as "show levels." And, in the process,
benefit from the formalization and especially from the clarity that
drawing an app statechart would bring.

Although good examples are starting to appear in the kivy-statecharts
framework, a version of DeflecTouch with statecharts will be highly
illustrative... Stay tuned...

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

