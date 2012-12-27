# ================================================================================
# Project: kivy-statecharts - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy_statecharts.system.state import State

"""
  @class

  Represents a history state that can be assigned to a State object's
  initial_substate property.

  If a HistoryState object is assigned to a state's initial substate,
  then after a state is entered the statechart will refer to the history
  state object to determine the next course of action. If the state has
  its history_state property assigned then that state will be entered,
  otherwise the default state assigned to history state object will be entered.

  [PORT] API is to use a state called InitialSubstate. See tests.

  An example of how to use:

    stateA = State()

    stateA.initial_substate = HistoryState()
    stateA.initial_substate.default_state = 'stateB'

    stateA.stateB = State()
    stateA.stateC = State()

  @author Michael Cohen
  @extends Object
"""
class HistoryState(State):
    """
      Used to indicate if the statechart should recurse the
      history states after entering the this object's parent state

      @property {Boolean}
    """
    is_recursive = BooleanProperty(False)

    """
      The default state to enter if the parent state does not
      yet have its history_state property assigned to something
      other than null.

      The value assigned to this property must be the name of an
      immediate substate that belongs to the parent state. The
      statechart will manage the property upon initialization.

      @property {String}
    """
    default_state = StringProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super(HistoryState, self).__init__(**kwargs)

    """
      Used by the statechart during a state transition process.

      Returns a state to enter based on whether the parent state has
      its history_state property assigned. If not then this object's
      assigned default state is returned.

      PORT: This was a simple computed property, so it could be observed.
            Here, we make it a simple dynamic method.
    """
    def state(self):
        default_state = self.get_state(self.default_state)
        history_state = self.parent_state.history_state

        return history_state if history_state else default_state
