Diagrammer
==========

NOTE: diagrammer uses new adapter, selection, list and dict property code in
      the data_changed_and_selection branch of kivy (Aug. 26, 2013).

NOTE: git-flow is being used for development, so work progresses on the
      develop branch, not on master. Releases on master will be started soon,
      but you will need to pay attention to master vs. develop branches. To
      play along or get involved, fork and clone your version, switch to the
      develop branch, and run 'python main.py' in the diagrammer directory.
      Communicate on #irc, and for development, learn about git-flow. We can
      collaborate on feature branches for larger needs.

Diagrammer is a Kivy app to draw statecharts, and perhaps other types of
diagrams later. Development started Summer 2013 and may progress with
substantial rapid changes, because the coding styles and conventions for both
Kivy graphics programming and for the design of statecharts are being
discovered in the process.

The focus has been on using the vector shape and on a nacent system
for drawing connections. There is the start of a user interface for selecting
shapes. There is nothing for selecting
connection end point styles (arrowheads, etc.) and the like.

See the help screen for current status of functionality.

Of course, there are quite a few things to improve in the existing
functionality, and there will need to be user interface elements added, new
states to support them, etc.

Early Inspirations and Help
---------------------------

- Christopher Bertonha (ghostbr) asked questions in irc about a little app he
  was working on, `SkydiveNavegation`_, that illustrates how to make a button
  with a Scatter. quanon helped him get this working. 

- For the graphics part, although the initial approach here is to use an image
  in a Scatter, it was helpful to look at the code and organization in the
  ``skeleton`` package by E. Roberts, D. Gries, L. Lee, S. Marschner, and W.
  White for their computer science course at Cornell University (`CS 1110`_). 

- tito and quanon helped with a primer on textures, labels, and kv lang rules.

.. _`SkydiveNavegation` https://github.com/Ghost-BR/SkydiveNavegation

.. _`CS 1110` http://www.cs.cornell.edu/courses/cs1110/2013sp/assignments/assignment7/
