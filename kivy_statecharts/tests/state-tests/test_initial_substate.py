'''
Statechart tests, initial substate
==================================
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.empty_state import EmptyState
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['monitor_is_active'] = True
        kwargs['root_state_class'] = self.RootState
        kwargs['trace'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'C'
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
        global root_state_1
        global monitor_1
        global state_A
        global state_B
        global state_C
        global state_D
        global state_E
        global state_F

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        state_C = statechart_1.get_state('C')
        state_D = statechart_1.get_state('D')
        state_E = statechart_1.get_state('E')
        state_F = statechart_1.get_state('F')
        
    def test_initial_substates_statechart_1(self):
        self.assertEqual(root_state_1.initial_substate_key, state_A.name)
        self.assertEqual(state_A.initial_substate_key, state_C.name)
        self.assertEqual(state_C.initial_substate_key, '')
        self.assertEqual(state_D.initial_substate_key, '')
        initial_substate_of_B = state_B.get_substate(state_B.initial_substate_key)
        self.assertTrue(isinstance(initial_substate_of_B, EmptyState))
        self.assertEqual(state_E.initial_substate_key, '')
        self.assertEqual(state_F.initial_substate_key, '')

    def test_go_to_state_B_confirm_current_is_empty_state(self):
        print 'test_goto...', statechart_1.current_states, root_state_1.substates
        self.assertTrue(state_C.is_current_state())
        monitor_1.reset()
        statechart_1.go_to_state('B')
        initial_substate_of_B = state_B.get_substate(state_B.initial_substate_key)
        self.assertTrue(monitor_1.match_sequence().begin().exited(state_C, state_A).entered(state_B, initial_substate_of_B).end())
        self.assertTrue(state_B.get_substate(state_B.initial_substate_key).is_current_state())

