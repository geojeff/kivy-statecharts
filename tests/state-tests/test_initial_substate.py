'''
Statechart tests, initial substate
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.empty_state import EmptyState
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['monitorIsActive'] = True
        kwargs['rootState'] = self.RootState
        kwargs['trace'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'C'
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

            class C(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.C, self).__init__(**kwargs)

            class D(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.D, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

            class E(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.E, self).__init__(**kwargs)

            class F(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.F, self).__init__(**kwargs)

class StateInitialSubstateTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global rootState_1
        global monitor_1
        global state_A
        global state_B
        global state_C
        global state_D
        global state_E
        global state_F

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootState
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        state_C = statechart_1.getState('C')
        state_D = statechart_1.getState('D')
        state_E = statechart_1.getState('E')
        state_F = statechart_1.getState('F')
        
    def test_initial_substates_statechart_1(self):
        self.assertEqual(rootState_1.initialSubstateKey, state_A.name)
        self.assertEqual(state_A.initialSubstateKey, state_C.name)
        self.assertEqual(state_C.initialSubstateKey, '')
        self.assertEqual(state_D.initialSubstateKey, '')
        initialSubstateOfB = state_B.getSubstate(state_B.initialSubstateKey)
        self.assertTrue(isinstance(initialSubstateOfB, EmptyState))
        self.assertEqual(state_E.initialSubstateKey, '')
        self.assertEqual(state_F.initialSubstateKey, '')

    def test_gotoState_B_confirm_current_is_empty_state(self):
        print 'test_goto...', statechart_1.currentStates, rootState_1.substates
        self.assertTrue(state_C.isCurrentState())
        monitor_1.reset()
        statechart_1.gotoState('B')
        initialSubstateOfB = state_B.getSubstate(state_B.initialSubstateKey)
        self.assertTrue(monitor_1.matchSequence().begin().exited(state_C, state_A).entered(state_B, initialSubstateOfB).end())
        self.assertTrue(state_B.getSubstate(state_B.initialSubstateKey).isCurrentState())

