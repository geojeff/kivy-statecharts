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

As of April 2012, most tests were ported.

Example Apps
------------

The examples directory contains several of the Kivy example apps adapted to use statecharts. New examples illustrate specific statechart functionality.

In a Nutshell
=============

The developer draws a statechart -- on a piece of paper is fine, but there are good drawing programs. This process is easy enough to start laying out what needs to happen as the app loads, and user interaction begins. As each user action is envisioned, it is drawn as a connector between states representing different parts of the user interface. More is added to the statechart, as details are realized and considered.

Once the developer has the hang of the simple coding constructs, it is a straightforward process to write the code corresponding to states and transitions on the statechart. 

Iteration of refining the statechart and writing code goes along as the app develops. 

For testing, a human-readable table of events and actions can be made from the statechart, and test cases made to cover each item.

Background
==========

If you are new to statecharts, or desire some deeper knowledge, you may wish to explore the origins of the concept. We can start with a look at the primary source of inspiration for Michael Cohen's Ki project, the paper by David Harel, *Statecharts: A Visual Formalism for Complex Systems*, Sci. Comput. Programming 8 (1987), 231-274 [pdf](http://www.wisdom.weizmann.ac.il/~harel/SCANNED.PAPERS/Statecharts.pdf). David Harel is a computer scientist at the Weizmann Institute of Science, Rehovot, Israel, who has published widely on this and related topics in programming. In the list of [David Harel's publications](http://www.wisdom.weizmann.ac.il/~harel/papers.html), the 1987 paper is #48 on the list, having come from a preliminary version published in 1984. If you scan the list for more recent offerings, you see some that pertain to statecharts in the pure programming sense of style, efficiency, software maintenance, etc., while others highlight the use of statecharts in specific subject areas, such as biological modeling. There is a larger literature, and many software projects that relate, but this list of Harel's publications serves as a good representation and starting point for a survey.

For an interesting personal account by Harel on the germination of the idea of statecharts, see: [Statecharts in the Making: A Personal Account](http://www.wisdom.weizmann.ac.il/%7Eharel/papers/Statecharts.History.pdf).

A Wikipedia article on [state diagrams](http://en.wikipedia.org/wiki/State_diagram), is good to read for the nature of the "Harel statechart" as a formalization of certain aspects of modeling the behavior of a system with a state diagram. From the article, "With Harel statecharts it is possible to model multiple cross-functional state diagrams within the statechart. Each of these cross-functional state machines can transition internally without affecting the other state machines in the statechart. The current state of each cross-functional state machine in the statechart defines the state of the system. The Harel statechart is equivalent to a state diagram but it improves the readability of the resulting diagram."

Reading the 1987 paper by Harel, you see in the abstract that statecharts concern "the notions of hierarchy, concurrency, and communication." Statecharts offer formalization to modularize code in a hierarchy of states that exist as discrete blocks that can act independently or concurrently, and communicate within an event system, allowing easier modeling of complexity.

So, statecharts help us build complex systems? Well, yes, but simple ones too. Besides, what software application stays simple for very long? Not many. Especially systems that involve many interacting parts -- typical software programs are "reactive" systems in the parlance of the 1987 Harel paper.

Speaking of the parlance of the Harel paper, here are some terms and concepts as used there, paraphrasing from the text:

**reactive system** -- an event-driven system that must react to external and internal stimuli driving behavior through sequences of changing conditions, relationships, events, and timing contraints.

**transformational system** -- systems in which a relationship between input and output is treated by a transformation, a function.

**state diagram** -- simple directed graph of states and transitions, with nodes denoting states and arrows denoting transitions, which may be labelled with triggering conditions and guarding conditions.

**superstate, "clustering," hierarchy, depth** -- A "cluster" of states is related somehow, e.g., "all airborne states." States are arranged hierarchically, with the hierarchy containing clusters of related states at various "levels." The visual side of statecharts is important, and you might prefer to "draw it out," but you should be able to imagine how the hierarchy set up in code is like a machine set up to react to events.

**orthogonal** -- independent. Contrast this with concurrent.

**concurrent** -- simultaneous. Contrast this with orthogonal, or independent.

**broadcast communication** -- event-driven, with the capability to send an event that can trigger action across states.

Now you can appreciate this, also from the Harel paper:

    statecharts = state-diagrams + depth + orthogonality + broadcast-communication

(where orthogonality implies functionality for handling concurrency as well).

To attempt a paraphrase:

    Statecharts add to basic state-diagrams the functionality to arrange states in a hierarchy, specifying which states are independent of one another and which ones are concurrent with each other. Code is written within states as discrete action functions that respond to events delivered to the statechart. Events firing to the action functions may have broadcast effect across multiple related or concurrent states.

Statecharts and Terminology in MVA/MVC Systems
----------------------------------------------

MVA = Model-View-Adapter System

MVC = Model-View-Controller System

Kivy seems closer to MVA, but ongoing current work on the framework will help to clarify. MVA/MVC terms are mentioned here because you will not see the term "controller" used much in Kivy, and the term "adapter" is just now starting to be used.

Statecharts are applicable to software systems in general, but Kivy, like so many other systems, involves a user interface with buttons and sliders and lists and custom views, tied to models of record types by means of adapters or controllers. Kivy has a sophisticated property bindings and observer system that is more similar to MVA design, than to MVC systems, generally. Regardless, whatever terminology is used, Kivy and other similar systems are "reactive" systems, so are amenable to statechart treatment.

Statecharts enhance the traditional MVA/MVC system. Where you may find some sort of event and callback system forming "adapter/controller" functionality, statecharts offer formalization beyond that, helping the programmer think more clearly about discrete elements and interactions.

For learning about "adapters/controllers" and terminology, we can read blog posts by Michael Cohen (nick: frozencanuck), the original author of the statecharts framework ported here from SproutCore. It will help you to realize that SproutCore is based on Cocoa. In Cocoa, we see differentation between coordinating vs. mediating controllers. Mediating controllers are a bit lower-level than coordinating controllers. Mediating controllers have some sort of backing content, usually data models with record types used in the system, that needs updating per user action in user interface views.

Coordinating controllers are more general than mediating controllers, and contain broader level application logic. Differences between these types of controllers are subtle and can be confused, a subject addressed by Michael Cohen in an important [blog post](http://frozencanuck.wordpress.com/2011/03/09/sproutcore-statecharts-vs-controllers/). The upshot of the blog post is that the higher level logic blocks in controllers will often "turn into brutish monsters containing many if-else or switch-case statements to know what state the application is currently in." 

Statecharts for Kivy
--------------------

Kivy has adapters that are like mediating controllers. Kivy has a property and bindings system, whereby a kind of view-mediating adapter coupling is built as a custom Widget.

Kivy does not formally have coordinatng controllers.

Code in Kivy that plays the "coordinating controller" role can be found in specific functions written to respond to user actions. A great example of clean layout for this can be seen in the DeflectTouch game that won the first Kivy app competition. For example, look at the substantial code in the level_button_pressed() function: https://github.com/stocyr/Deflectouch/blob/master/main.py#L181 -- this is "coordinating controller" code.

The code in the DeflecTouch level_button_pressed() function could just as well be put in a "ShowingMainScreen" state, in a "show_levels" action function. Rewriting DeflecTouch with statecharts would simply entail moving such code into discrete states, and to action functions that respond to events such as "show levels." And, in the process, benefit from the formalization and especially from the clarity that drawing an app statechart would bring.

Although good examples are starting to appear in the kivy-statechart framework, a version of DeflecTouch with statecharts will be highly illustrative... Stay tuned...
