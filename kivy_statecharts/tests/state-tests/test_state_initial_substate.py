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


class X(State):
    pass


class Y(State):
    pass


class Statechart_2(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['initial_state_key'] = 'X'
        super(Statechart_2, self).__init__(**kwargs)

    X = X
    Y = Y


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
        global state_X
        global state_Y

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

        statechart_2 = Statechart_2()
        statechart_2.init_statechart()
        root_state_2 = statechart_2.root_state_instance
        monitor_2 = statechart_2.monitor
        state_X = statechart_2.get_state('X')
        state_Y = statechart_2.get_state('Y')

    def test_initial_substates_statechart_1(self):
        self.assertEqual(root_state_1.initial_substate_key, state_A.name)
        self.assertEqual(state_A.initial_substate_key, state_C.name)
        self.assertEqual(state_C.initial_substate_key, None)
        self.assertEqual(state_D.initial_substate_key, None)
        initial_substate_of_B = state_B.get_substate(state_B.initial_substate_key)
        self.assertTrue(isinstance(initial_substate_of_B, EmptyState))
        self.assertEqual(state_E.initial_substate_key, None)
        self.assertEqual(state_F.initial_substate_key, None)

    def test_go_to_state_B_confirm_current_is_empty_state(self):
        print 'test_goto...', statechart_1.current_states, root_state_1.substates
        self.assertTrue(state_C.is_current_state())
        monitor_1.reset()
        statechart_1.go_to_state('B')
        initial_substate_of_B = state_B.get_substate(state_B.initial_substate_key)
        self.assertTrue(monitor_1.match_sequence().begin().exited(state_C, state_A).entered(state_B, initial_substate_of_B).end())
        self.assertTrue(state_B.get_substate(state_B.initial_substate_key).is_current_state())

    def test_initial_substate_as_object(self):
        # state_X is in statechart_2, and is initial substate
        self.assertTrue(state_X.is_current_state())

        # Make a new state, isolated (not in a statechart), and set initial
        # state as an object, not a string key. Test if set as string key.
        state_Z = State(initial_substate_key=state_Y)
        self.assertEqual(state_Z.initial_substate_key, 'Y')

    def test_initial_substate_as_nameless_object(self):
        # To get a nameless state, we must create in isolation, because if in
        # a statechart, name for the state would be set.
        state_U = State()

        # Make a new state, isolated (not in a statechart), and set initial
        # state as an object, not a string key.
        state_W = State(initial_substate_key=state_U)
        self.assertEqual(state_W.initial_substate_key, None)
        self.assertEqual(state_W.initial_substate_object, state_U)
