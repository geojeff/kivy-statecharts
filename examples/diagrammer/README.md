Diagrammer
==========

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

As of June 21, the focus has been on using the triangle vector shape and on a
nacent system for drawing connections. There is not yet a user interface for
selecting shapes, connection end point styles (arrowheads, etc.) and the like.
So far, after the app loads, this has been accomplished:

After app loads, you see a blank rectangle display, but the full area of the
window is actually the drawing area. You can do this:

1) Touch (or click) once to draw a triangle shape.
2) Touch again in another area to draw a second shape.
3) Touch the perimeter of a triangle and drag to move it.
4) Touch and drag in the center of one rectangle to the center of another.
4a) On touch up, bubbles will appear on either end of the connection. 
4b) In a given bubble, touch and drag within the Drag button to move the
    connection point for the end (dragging out of the drag button will
    terminate the move, presently -- needs event handling in state for
    drawing_area).
4c) Repeat drag ops on the Drag button, for now to drag the given connection
    point further, clockwise (too jerky and skips for now).
4d) Once the connection point is ok, touch Accept.
5) You can add more triangles and connections.
6) You can move triangles with connections, and the connections will adjust.

That's it for now. Of course, there is quite a few things to improve in the
existing functionality, and there will need to be user interface elements
added, new states to support them, etc.

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
