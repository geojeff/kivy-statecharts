# ================================================================================
# Project:   Kivy.Statechart - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

from kivy.statechart.system.state import State

"""
  The default name given to an empty state
"""
EMPTY_STATE_NAME = "__EMPTY_STATE__"

"""
  @class
  
  Represents an empty state that gets assigned as a state's initial substate 
  if the state does not have an initial substate defined.

  @extends State
"""
class EmptyState(State):
    def __init__(self, **kw):
        self.name = EMPTY_STATE_NAME
        super(EmptyState, self).__init__(**kw)
  
    def enterState(self):
        msg = "No initial substate was defined for state {0}. Entering default empty state"
        this.stateLogWarning(msg.format(self.parentState))
