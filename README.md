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

Background
==========

If you are new to statecharts, or desire some deeper knowledge, you may wish to explore the origins of the concept. We can start with a look at the primary source of inspiration for Michael Cohen's Ki project, the paper by David Harel, *Statecharts: A Visual Formalism for Complex Systems*, Sci. Comput. Programming 8 (1987), 231-274 \[[pdf]\](http://www.wisdom.weizmann.ac.il/~harel/SCANNED.PAPERS/Statecharts.pdf). David Harel is a computer scientist at the Weizmann Institute of Science, Rehovot, Israel, who has published widely on this and related topics in programming. In the list of [David Harel's publications](http://www.wisdom.weizmann.ac.il/~harel/papers.html), the 1987 paper is #48 on the list, having come from a preliminary version published in 1984. If you scan the list for more recent offerings, you see some that pertain to statecharts in the pure programming sense of style, efficiency, software maintenance, etc., while others highlight the use of statecharts in specific subject areas, such as biological modeling. There is a larger literature, and many software projects that relate, but this list of Harel's publications serves as a good representation and starting point for a survey.

A Wikipedia article on [state diagrams](http://en.wikipedia.org/wiki/State_diagram), is good to read for the nature of the "Harel statechart" as a formalization of certain aspects of modeling the behavior of a system with a state diagram. From the article, "With Harel statecharts it is possible to model multiple cross-functional state diagrams within the statechart. Each of these cross-functional state machines can transition internally without affecting the other state machines in the statechart. The current state of each cross-functional state machine in the statechart defines the state of the system. The Harel statechart is equivalent to a state diagram but it improves the readability of the resulting diagram."

Reading the 1987 paper by Harel, you see in the abstract that statecharts concern "the notions of hierarchy, concurrency, and communication." Statecharts offer formalization to modularize code in a hierarchy of states that exist as discrete blocks that can act independently or concurrently, and communicate within an event system, allowing easier modeling of complexity.

So, statecharts help us build complex systems? Well, yes, but what software system stays simple? Not many. Especially systems that involve many interacting parts, "reactive" sytems in the parlance of the 1987 Harel paper.

Speaking of the parlance of the Harel paper, here are some terms and concepts as used there, paraphrasing from the text:

**reactive system** -- an event-driven system that must react to external and internal stimuli driving behavior through sequences of changing conditions, relationships, events, and timing contraints.

**transformational system** -- systems in which a relationship between input and output is treated by a transformation, a function.

**state diagram** -- simple directed graph of states and transitions, with nodes denoting states and arrows denoting transitions, which may be labelled with triggering conditions and guarding conditions.

**superstate, "clustering," hierarchy, depth** -- A "cluster" of states is related somehow, e.g., "all airborne states." States are arranged hierarchically, with the hierarchy containing clusters of related states at various "levels." The visual side of statecharts is important, and you might prefer to "draw it out," but you should be able to imagine how the hierarchy set up in code is like a machine set up to react to events.

**orthogonal** -- independent. Contrast this with concurrent.

**concurrent** -- simultaneous. Contrast this with orthogonal, or independent.

**broadcast communication** -- event-driven, with the capability to send an event that can trigger action across states.

Now you can appreciate this, also form the Harel paper:

    statecharts = state-diagrams + depth + orthogonality + broadcast-communication

(where orthogonality implies functionality for handling concurrency as well).

To attempt a paraphrase, we may say that statecharts add to basic state-diagrams the functionality to arrange states in a hierarchy, specifying which states are orthogonal to one another, which ones are concurrent with each other, and to write code for the states that responds to events delivered to the statechart, as discrete events that have narrow effect and as events that have broadcast effect across multiple related or concurrent states.

Application in Model-View-Controller Systems
--------------------------------------------

Statecharts are applicable to software systems in general, but Kivy, like SproutCore and so many other systems, involves a user interface with buttons and sliders and lists and custom views, tied to models of record types by means of controllers, which are like bridging connections. MVC systems are "reactive" systems, so are amenable to statechart treatment.

Statecharts enhance the traditional controller system. Where you may find some sort of event and callback system forming "controller" functionality, statecharts offer formalization beyond that, helping the programmer think more clearly about discrete elements and interactions. In Kivy there is an event system, and there are idioms for setting up a "controller" in python code that is tied to the user interface and responding to "action" events: http://kivy.org/docs/guide/designwithkv.html. You can build something elaborate with this existing functionality, but adding statecharts to the mix will offer the many benefits enjoyed in other systems. 

SproutCore had a system of controllers too, allowing very effective programming before statecharts were added. We can benefit from the similar history of introduction. Notably, for controllers, we can read blog posts by Michael Cohen (nick: frozencanuck) that help with concepts. It will help you to realize that SproutCore is based on Cocoa. Let's look back at some relevant history (history in the sense of SproutCore's heritage; Cocoa and related iOS programming is alive and well, as you know).

In Cocoa, we see differentation for terminology for controllers: primarily coordinating vs. mediating controllers. Mediating controllers are a bit lower-level than coordinating controllers. Mediating controllers have some sort of backing content that needs updating, usually models of record types used in the system. Coordinating controllers are more general, and can contain broader level application logic. Differences between these types of controllers are subtle and can be confused, a subject addressed by Michael Cohen in an important [blog post](http://frozencanuck.wordpress.com/2011/03/09/sproutcore-statecharts-vs-controllers/). The upshot is that the higher level logic blocks in controllers will often "turn into brutish monsters containing many if-else or switch-case statements to know what state the application is currently in." The title of the next section of the blog post is apt, and may be fitting as well for Kivy, and we borrow it here:

Here Comes Statecharts to the Rescue!
-------------------------------------

If you have been a Kivy developer, you may take all of this with a big grain of salt: "Hey, I am doing fine -- I don't need rescuing." Howevever, endeavoring to appreciate the port to kivy-statechart, and the history of related projects might open up new lines of thinking, and it might offer key advantages, as happened with SproutCore. So, what do statecharts offer the Kivy developer?

We still need mediating controllers as interfaces, but these should be small and operate via the bindings already fully functional in Kivy's property system, and the kv language system. By "small" here, we mean restricted in scope, not containing big logic blocks for application control. Keep that in the statechart system. The statechart system takes over *much* of the role played by coordinating controllers, offering the key advantages outlined above. 

For comparison, as you may be familiar with design patterns in general, the Michael Cohen blog post contains a full comparison to the [state design pattern](http://en.wikipedia.org/wiki/State_pattern) using traditional coordinating controller type treatments, as described in the "Gang of Four" book on [Design Patterns](http://en.wikipedia.org/wiki/Design_Patterns_%28book%29), concluding that to flesh it out with comparative functionality, you would be building a statecharts framework.

In a final parallel, because Kivy focuses on touch interactions, the points made near the end of the Michael Cohen blog post about the "delegate" pattern, for use in such things in drag-and-drop and between views, some equivalent to the concept of the coordinating controller is likely warranted in Kivy as well. Python has the concept of mixins, as well, so this might be a direct parallel.

So, perhaps a marching order for development effort relating to kivy-statechart, in addition to enhancement via startechart functionality directly, is the description of existing Kivy idioms for controllers and how they fit into the differentiation covered here and in linked posts, and maybe some coding of formal controller classes for Kivy.










