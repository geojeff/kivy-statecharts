'''
Statechart tests, transitioning, history, standard, without concurrent, core
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy_statecharts.system.state import State
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
                kwargs['initial_substate_key'] = 'C'
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

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
                kwargs['initial_substate_key'] = 'E'
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

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

class StateTransitioningHistoryStandardCoreWithoutConcurrentTestCase(unittest.TestCase):
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

    # Check initial statechart history state objects
    def test_initial_statechart_history_state_objects(self):
        self.assertEqual(statechart_1.root_state_instance.history_state, statechart_1.get_state('A'))

        self.assertEqual(statechart_1.get_state('A').history_state, statechart_1.get_state('C'))
        self.assertEqual(statechart_1.get_state('C').history_state, statechart_1.get_state('G'))
        self.assertIsNone(statechart_1.get_state('G').history_state)

        self.assertIsNone(statechart_1.get_state('H').history_state)
        self.assertIsNone(statechart_1.get_state('D').history_state)

        self.assertIsNone(statechart_1.get_state('B').history_state)
        self.assertIsNone(statechart_1.get_state('E').history_state)
        self.assertIsNone(statechart_1.get_state('F').history_state)

    # Check go to state h and check history states
    def test_go_to_h_and_check_history_states(self):
        monitor_1.reset()

        statechart_1.go_to_state('H')

        self.assertEqual(statechart_1.get_state('A').history_state, statechart_1.get_state('C'))
        self.assertEqual(statechart_1.get_state('C').history_state, statechart_1.get_state('H'))
        self.assertIsNone(statechart_1.get_state('H').history_state)
        self.assertIsNone(statechart_1.get_state('G').history_state)

        self.assertIsNone(statechart_1.get_state('D').history_state)
        self.assertIsNone(statechart_1.get_state('B').history_state)

    # Check go to state d and check history states
    def test_go_to_d_and_check_history_states(self):
        monitor_1.reset()

        statechart_1.go_to_state('D')

        self.assertEqual(statechart_1.get_state('A').history_state, statechart_1.get_state('D'))
        self.assertEqual(statechart_1.get_state('D').history_state, statechart_1.get_state('I'))
        self.assertEqual(statechart_1.get_state('C').history_state, statechart_1.get_state('G'))
        self.assertIsNone(statechart_1.get_state('H').history_state)
        self.assertIsNone(statechart_1.get_state('G').history_state)
        self.assertIsNone(statechart_1.get_state('I').history_state)
        self.assertIsNone(statechart_1.get_state('J').history_state)

        self.assertIsNone(statechart_1.get_state('B').history_state)

    # Check go to state b and check history states
    def test_go_to_b_and_check_history_states(self):
        monitor_1.reset()

        statechart_1.go_to_state('B')
        self.assertTrue(monitor_1.match_sequence().begin().exited('G', 'C', 'A').entered('B', 'E', 'K').end())

        self.assertEqual(statechart_1.root_state_instance.history_state, statechart_1.get_state('B'))
        self.assertEqual(statechart_1.get_state('B').history_state, statechart_1.get_state('E'))
        self.assertEqual(statechart_1.get_state('E').history_state, statechart_1.get_state('K'))
        self.assertEqual(statechart_1.get_state('A').history_state, statechart_1.get_state('C'))
        self.assertEqual(statechart_1.get_state('C').history_state, statechart_1.get_state('G'))


    # Check go to state j, then state m, then go to state a's history state (non-recursive)
    def test_to_j_then_to_m_then_to_state_a_history_state_non_recursive(self):
        statechart_1.go_to_state('J')
        statechart_1.go_to_state('M')

        monitor_1.reset()
        statechart_1.go_to_history_state('A')
  
        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.match_sequence().begin().exited('M', 'F', 'B').entered('A', 'D', 'I').end())
        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('I'))
        self.assertEqual(statechart_1.root_state_instance.history_state, statechart_1.get_state('A'))
        self.assertEqual(statechart_1.get_state('A').history_state, statechart_1.get_state('D'))
        self.assertEqual(statechart_1.get_state('D').history_state, statechart_1.get_state('I'))

# [PORT] Failure on J

#    # Check go to state j, then state m, then go to state a's history state (recursive)
#    def test_to_j_then_to_m_then_to_state_a_history_state_recursive(self):
#        statechart_1.go_to_state('J')
#        statechart_1.go_to_state('M')
#
#        monitor_1.reset()
#        statechart_1.go_to_history_state('A', from_current_state=None, recursive=True)
#  
#        self.assertEqual(monitor_1.length, 6)
#        self.assertTrue(monitor_1.match_sequence().begin().exited('M', 'F', 'B').entered('A', 'D', 'J').end())
#        self.assertEqual(len(statechart_1.current_states), 1)
#        self.assertTrue(statechart_1.state_is_current_state('J'))
#        self.assertEqual(statechart_1.root_state_instance.history_state, statechart_1.get_state('A'))
#        self.assertEqual(statechart_1.get_state('A').history_state, statechart_1.get_state('D'))
#        self.assertEqual(statechart_1.get_state('D').history_state, statechart_1.get_state('I'))

    # Check go to state b's history state (non-recursive)
    def test_go_to_state_b_history_state_non_recursive(self):
        monitor_1.reset()

        statechart_1.go_to_history_state('B')
  
        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.match_sequence().begin().exited('G', 'C', 'A').entered('B', 'E', 'K').end())
        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('K'))
        self.assertEqual(statechart_1.root_state_instance.history_state, statechart_1.get_state('B'))
        self.assertEqual(statechart_1.get_state('B').history_state, statechart_1.get_state('E'))
        self.assertEqual(statechart_1.get_state('E').history_state, statechart_1.get_state('K'))


    # Check go to state b's history state (recursive)
    def test_go_to_state_b_history_state_recursive(self):
        monitor_1.reset()

        statechart_1.go_to_history_state('B', from_current_state=None, recursive=True)
  
        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.match_sequence().begin().exited('G', 'C', 'A').entered('B', 'E', 'K').end())
        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('K'))
        self.assertEqual(statechart_1.root_state_instance.history_state, statechart_1.get_state('B'))
        self.assertEqual(statechart_1.get_state('B').history_state, statechart_1.get_state('E'))
        self.assertEqual(statechart_1.get_state('E').history_state, statechart_1.get_state('K'))

