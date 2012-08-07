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
        kwargs['rootStateClass'] = self.RootState
        kwargs['monitorIsActive'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
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
        global rootState_1
        global monitor_1
        global state_A
        global state_B
        global state_C

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootStateInstance
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        state_C = statechart_1.getState('C')
  
    # Check default history state
    def test_default_history_state(self):
        historyState = HistoryState()

        self.assertFalse(historyState.isRecursive)

    # Check assigned history state
    def test_assigned_history_state(self):
        historyState = HistoryState(isRecursive=True, statechart=statechart_1, parentState=state_A, defaultState='B')

        self.assertEqual(historyState.statechart, statechart_1)
        self.assertEqual(historyState.parentState, state_A)
        self.assertEqual(historyState.defaultState, state_B.name)
        self.assertTrue(historyState.isRecursive)
        self.assertEqual(historyState.state(), state_B)

        state_A.historyState = state_C

        self.assertEqual(historyState.state(), state_C)

        state_A.historyState = None

        self.assertEqual(historyState.state(), state_B)
