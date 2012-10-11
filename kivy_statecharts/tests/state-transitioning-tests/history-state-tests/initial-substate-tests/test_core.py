'''
Statechart tests, transitioning, history, initial substate, core
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.history_state import HistoryState
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['root_state_class'] = self.RootState
        kwargs['monitor_is_active'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.A, self).__init__(**kwargs)
    
        class B(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.B, self).__init__(**kwargs)
    
        class C(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.C, self).__init__(**kwargs)
    
class StateTransitioningHistoryInitialSubstateCoreTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global root_state_1
        global monitor_1
        global state_A
        global state_B
        global state_C

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        state_C = statechart_1.get_state('C')
  
    # Check default history state
    def test_default_history_state(self):
        history_state = HistoryState()

        self.assertFalse(history_state.is_recursive)

    # Check assigned history state
    def test_assigned_history_state(self):
        history_state = HistoryState(is_recursive=True, statechart=statechart_1, parent_state=state_A, default_state='B')

        self.assertEqual(history_state.statechart, statechart_1)
        self.assertEqual(history_state.parent_state, state_A)
        self.assertEqual(history_state.default_state, state_B.name)
        self.assertTrue(history_state.is_recursive)
        self.assertEqual(history_state.state(), state_B)

        state_A.history_state = state_C

        self.assertEqual(history_state.state(), state_C)

        state_A.history_state = None

        self.assertEqual(history_state.state(), state_B)
