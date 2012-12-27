# ================================================================================
# Project: kivy-statecharts - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

from kivy_statecharts.system.state import State

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
    def __init__(self, **kwargs):
        kwargs['name'] = EMPTY_STATE_NAME
        super(EmptyState, self).__init__(**kwargs)

    def enter_state(self, context=None):
        msg = "No initial substate was defined for state {0}. Entering default empty state"
        self.state_log_warning(msg.format(self.parent_state))
