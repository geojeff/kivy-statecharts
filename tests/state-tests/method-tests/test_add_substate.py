'''
Statechart tests, add substate
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.empty_state import EmptyState
from kivy_statecharts.system.empty_state import EMPTY_STATE_NAME
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['rootStateClass'] = self.RootState
        kwargs['trace'] = True
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
                kwargs['substatesAreConcurrent'] = True
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

            class X(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.X, self).__init__(**kwargs)

            class Y(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.Y, self).__init__(**kwargs)

class StateAddSubstateTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global rootState_1
        global monitor_1
        global state_A
        global state_B
        global state_X
        global state_Y

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootStateInstance
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        state_X = statechart_1.getState('X')
        state_Y = statechart_1.getState('Y')
        
    # Add a substate to the statechart's root state
    def test_add_substate_to_root_state_statechart_1(self):
        self.assertIsNone(rootState_1.getSubstate('Z'))

        state = rootState_1.addSubstate('Z')

        self.assertTrue(isinstance(state, State))
        self.assertIsNotNone(rootState_1.getSubstate('Z'))
        self.assertTrue(state.stateIsInitialized)
        self.assertEqual(state.name, 'Z')
        self.assertFalse(state.isEnteredState())
        self.assertFalse(state.isCurrentState())

        statechart_1.gotoState('Z')

        self.assertTrue(state.isEnteredState())
        self.assertTrue(state.isCurrentState())

    # Add a substate to state A
    def test_add_substate_to_state_A_statechart_1(self):
        self.assertIsNone(state_A.getSubstate('Z'))
        # In [PORT], EmptyState is created only for states with substates, and no initialSubstate set. Correct?
        self.assertEqual(state_A.initialSubstateKey, '')

        state = state_A.addSubstate('Z')

        self.assertTrue(isinstance(state, State))
        self.assertEqual(state_A.getSubstate('Z'), state)
        self.assertEqual(state_A.initialSubstateKey, EMPTY_STATE_NAME)
        self.assertFalse(state.isEnteredState())
        self.assertFalse(state.isCurrentState())
        self.assertTrue(state_A.isEnteredState())
        self.assertTrue(state_A.isCurrentState())

        print 'reentering state A'
        setattr(state_A, 'initialSubstateKey', state.name)
        state_A.reenter()

        self.assertTrue(state.isEnteredState())
        self.assertTrue(state.isCurrentState())
        self.assertTrue(state_A.isEnteredState())
        self.assertFalse(state_A.isCurrentState())

    # Add a substate to state B
    def test_add_substate_to_state_B_statechart_1(self):
        self.assertIsNone(state_B.getSubstate('Z'))

        statechart_1.gotoState('B')

        state = state_B.addSubstate('Z')

        self.assertTrue(isinstance(state, State))
        self.assertEqual(state_B.getSubstate('Z'), state)
        self.assertFalse(state.isEnteredState())
        self.assertFalse(state.isCurrentState())
        self.assertFalse(state_B.isCurrentState())
        self.assertEqual(state_B.initialSubstateKey, '')
        self.assertTrue(state_B.isEnteredState())
        self.assertEqual(len(state_B.currentSubstates), 2)

        state_B.reenter()

        self.assertTrue(state.isEnteredState())
        self.assertTrue(state.isCurrentState())
        self.assertTrue(state_B.isEnteredState())
        self.assertEqual(len(state_B.currentSubstates), 3)


