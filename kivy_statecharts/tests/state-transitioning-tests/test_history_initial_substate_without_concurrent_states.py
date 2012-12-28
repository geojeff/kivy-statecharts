'''
Statechart tests, transitioning, history, initial substate, without concurrent
==============================================================================
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

            class InitialSubstate(HistoryState):
                def __init__(self, **kwargs):
                    kwargs['default_state'] = 'C'
                    super(Statechart_1.RootState.A.InitialSubstate, self).__init__(**kwargs)

            class C(State):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'G'
                    super(Statechart_1.RootState.A.C, self).__init__(**kwargs)

                class G(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.C.G, self).__init__(**kwargs)

                class H(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.C.H, self).__init__(**kwargs)

            class D(State):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'I'
                    super(Statechart_1.RootState.A.D, self).__init__(**kwargs)

                class I(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.D.I, self).__init__(**kwargs)

                class J(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.D.J, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.B, self).__init__(**kwargs)
        
            class InitialSubstate(HistoryState):
                def __init__(self, **kwargs):
                    kwargs['is_recursive'] = True
                    kwargs['default_state'] = 'E'
                    super(Statechart_1.RootState.B.InitialSubstate, self).__init__(**kwargs)

            class E(State):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'K'
                    super(Statechart_1.RootState.B.E, self).__init__(**kwargs)

                class K(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.B.E.K, self).__init__(**kwargs)

                class L(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.B.E.L, self).__init__(**kwargs)

            class F(State):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'M'
                    super(Statechart_1.RootState.B.F, self).__init__(**kwargs)

                class M(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.B.F.M, self).__init__(**kwargs)

                class N(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.B.F.N, self).__init__(**kwargs)

class StateTransitioningHistoryInitialSubstateWithoutConcurrentTestCase(unittest.TestCase):
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
        global state_G
        global state_H
        global state_I
        global state_J
        global state_K
        global state_L
        global state_M
        global state_N
        global initial_substate_A
        global initial_substate_B

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
        state_G = statechart_1.get_state('G')
        state_H = statechart_1.get_state('H')
        state_I = statechart_1.get_state('I')
        state_J = statechart_1.get_state('J')
        state_K = statechart_1.get_state('K')
        state_L = statechart_1.get_state('L')
        state_M = statechart_1.get_state('M')
        state_N = statechart_1.get_state('N')
        initial_substate_A = getattr(state_A, 'InitialSubstate')
        initial_substate_B = getattr(state_B, 'InitialSubstate')

    # Check initial statechart after statechart init
    def test_initial_statechart_after_statechart_init(self):
        self.assertEqual(monitor_1.length, 4)
        self.assertTrue(monitor_1.match_sequence().begin().entered(root_state_1, state_A, state_C, state_G).end())
      
        self.assertEqual(root_state_1.initial_substate_key, 'A')
        self.assertEqual(state_C.initial_substate_key, 'G')
        self.assertEqual(state_D.initial_substate_key, 'I')
        self.assertEqual(state_E.initial_substate_key, 'K')
        self.assertEqual(state_F.initial_substate_key, 'M')

        self.assertTrue(isinstance(initial_substate_A, HistoryState))
        self.assertFalse(initial_substate_A.is_recursive)
        self.assertEqual(initial_substate_A.default_state, 'C')
        self.assertEqual(initial_substate_A.statechart, statechart_1)
        self.assertEqual(initial_substate_A.parent_state, state_A)
        self.assertEqual(initial_substate_A.state(), state_C)

        self.assertTrue(isinstance(initial_substate_B, HistoryState))
        self.assertTrue(initial_substate_B.is_recursive)
        self.assertEqual(initial_substate_B.default_state, 'E')
        self.assertEqual(initial_substate_B.statechart, statechart_1)
        self.assertEqual(initial_substate_B.parent_state, state_B)
        self.assertEqual(initial_substate_B.state(), state_E)
  
        self.assertEqual(state_A.history_state, state_C)
        self.assertIsNone(state_B.history_state)

    def test_initial_state_without_default_state(self):
        msg = ("Initial substate is invalid. History state requires the name "
                "of a default state to be set.")

        state_P = State(name='P')
        state_P.InitialSubstate = HistoryState

        with self.assertRaises(Exception) as cm:
            state_P.init_state()

        self.assertEqual(str(cm.exception), msg)

    def test_get_substate_InitialSubstate_of_root(self):
        msg = ("Cannot find substate matching 'InitialSubstate' in state "
               "__ROOT_STATE__. Ambiguous with the following: "
               "B.InitialSubstate, A.InitialSubstate")
        with self.assertRaises(Exception) as cm:
            initial_substate = root_state_1.get_substate('InitialSubstate')

        self.assertEqual(str(cm.exception), msg)

    def test_get_substate_InitialSubstate_of_state_A(self):
        initial_substate = state_A.get_substate('InitialSubstate')

        self.assertEqual(initial_substate.default_state, 'C')

    def test_get_substate_InitialSubstate_of_state_B(self):
        initial_substate = state_B.get_substate('InitialSubstate')

        self.assertEqual(initial_substate.default_state, 'E')

