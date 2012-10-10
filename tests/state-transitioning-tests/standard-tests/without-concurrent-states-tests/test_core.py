'''
Statechart tests, transitioning, standard, without concurrent, core
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

class StateTransitioningStandardCoreWithoutConcurrentTestCase(unittest.TestCase):
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

    # Check statechart state objects
    def test_statechart_state_objects(self):
        self.assertIsNotNone(state_G)
        self.assertEqual(state_G.name, 'G')
        self.assertTrue(state_G.is_current_state())
        self.assertTrue(state_G.state_is_current_substate('G'))
        self.assertTrue(statechart_1.state_is_current_state('G'))
        self.assertTrue(statechart_1.state_is_current_state(state_G))
  
        self.assertIsNotNone(state_M)
        self.assertEqual(state_M.name, 'M')
        self.assertFalse(state_M.is_current_state())
        self.assertFalse(state_G.state_is_current_substate('M'))
        self.assertFalse(statechart_1.state_is_current_state('M'))
        self.assertFalse(statechart_1.state_is_current_state(state_M))
  
        self.assertIsNotNone(state_A)
        self.assertFalse(state_A.is_current_state())
        self.assertFalse(state_A.state_is_current_substate('A'))
        self.assertFalse(state_A.state_is_current_substate('C'))
        self.assertTrue(state_A.state_is_current_substate('G'))
        self.assertTrue(state_A.state_is_current_substate(state_G))
        self.assertFalse(state_A.state_is_current_substate(state_M))
 
        state_X = statechart_1.get_state('X')
        self.assertIsNone(state_X)

    # Check statechart initialization
    def test_statechart_initialization(self):
        self.assertEqual(monitor_1.length, 4)

        self.assertTrue(monitor_1.match_sequence().begin().entered(root_state_1, 'A', 'C', 'G').end())
  
        self.assertEqual(len(statechart_1.current_states), 1)
  
        self.assertTrue(statechart_1.state_is_current_state('G'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'A', 'C', 'G'))

    # Check go to state h
    def test_go_to_state_h(self):
        monitor_1.reset()
        statechart_1.go_to_state('H')
  
        self.assertEqual(monitor_1.length, 2)
        self.assertTrue(monitor_1.match_sequence().begin().exited('G').entered('H').end())
        self.assertFalse(monitor_1.match_sequence().begin().exited('H').entered('G').end())
  
        self.assertEqual(len(statechart_1.current_states), 1)
  
        self.assertTrue(statechart_1.state_is_current_state('H'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'A', 'C', 'H'))

    # Check go to states h and d
    def test_go_to_states_h_and_d(self):
        statechart_1.go_to_state('H')

        monitor_1.reset()
        statechart_1.go_to_state('D')
  
        self.assertEqual(monitor_1.length, 4)

        self.assertTrue(monitor_1.match_sequence().begin().exited('H', 'C').entered('D', 'I').end())
        self.assertFalse(monitor_1.match_sequence().begin().exited('H', 'C').entered('D', 'F').end())
        self.assertFalse(monitor_1.match_sequence().begin().exited('G', 'C').entered('D', 'I').end())

        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('I'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'A', 'D', 'I'))

    # Check go to states h, d, and h
    def test_go_to_states_h_d_and_h(self):
        statechart_1.go_to_state('H')
        statechart_1.go_to_state('D')

        monitor_1.reset()
        statechart_1.go_to_state('H')
  
        self.assertEqual(monitor_1.length, 4)
  
        self.assertTrue(monitor_1.match_sequence().begin().exited('I', 'D').entered('C', 'H').end())

        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('H'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'A', 'C', 'H'))

    # Check go to state b
    def test_go_to_state_b(self):
        monitor_1.reset()
        statechart_1.go_to_state('B')

        self.assertEqual(monitor_1.length, 6)

        self.assertTrue(monitor_1.match_sequence().begin().exited('G', 'C', 'A').entered('B', 'E', 'K').end())
        self.assertFalse(monitor_1.match_sequence().begin().exited('G', 'A', 'C').entered('B', 'E', 'K').end())
        self.assertFalse(monitor_1.match_sequence().begin().exited('G', 'C', 'A').entered('B', 'K', 'E').end())

        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('K'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'B', 'E', 'K'))

    # Check go to state f
    def test_go_to_state_f(self):
        monitor_1.reset()
        statechart_1.go_to_state('F')

        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.match_sequence().begin().exited('G', 'C', 'A').entered('B', 'F', 'M').end())

        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('M'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'B', 'F', 'M'))

    # Check go to state n
    def test_go_to_state_n(self):
        monitor_1.reset()
        statechart_1.go_to_state('N')

        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.match_sequence().begin().exited('G', 'C', 'A').entered('B', 'F', 'N').end())

        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('N'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'B', 'F', 'N'))

    # Check re-enter state G
    def test_reenter_state_g(self):
        monitor_1.reset()
        statechart_1.go_to_state('G')

        self.assertEqual(monitor_1.length, 2)

        self.assertTrue(monitor_1.match_sequence().begin().exited('G').entered('G').end())

        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('G'))
  
        monitor_1.reset()
  
        self.assertEqual(monitor_1.length, 0)
  
        state = statechart_1.get_state('G')
        state.reenter()
  
        self.assertEqual(monitor_1.length, 2)
        self.assertTrue(monitor_1.match_sequence().begin().exited('G').entered('G').end())
        
        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('G'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'A', 'C', 'G'))

    # Check go to g state's ancestor state a
    def test_go_to_g_state_ancestor_state_a(self):
        monitor_1.reset()
        statechart_1.go_to_state('A')

        self.assertEqual(monitor_1.length, 6)

        self.assertTrue(monitor_1.match_sequence().begin().exited('G', 'C', 'A').entered('A', 'C', 'G').end())
        
        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('G'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'A', 'C', 'G'))


    # Check go to state b and then go to root state
    def test_go_to_state_b_then_to_root_state(self):
        statechart_1.go_to_state('B')
        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('K'))
  
        monitor_1.reset()
        statechart_1.go_to_state(statechart_1.root_state_instance)
  
        root = statechart_1.root_state_instance

        self.assertEqual(monitor_1.length, 8)
        self.assertTrue(monitor_1.match_sequence().begin().exited('K', 'E', 'B', root).entered(root, 'A', 'C', 'G').end())
        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('G'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root, 'A', 'C', 'G'))

    # Check from state g, go to state m calling state g's go_to_state
    def test_from_g_to_m_calling_state_g_go_to_state(self):
        self.assertTrue(state_G.is_current_state())
        self.assertFalse(state_M.is_current_state())
  
        monitor_1.reset()
        state_G.go_to_state('M')
  
        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.match_sequence().begin().exited('G', 'C', 'A').entered('B', 'F', 'M').end())
        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('M'))
  
        self.assertFalse(state_G.is_current_state())
        self.assertTrue(state_M.is_current_state())
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'B', 'F', 'M'))

    # Check from state g, go to state h using parent_state syntax
    def test_from_g_to_h_using_parent_state_syntax(self):
        monitor_1.reset()
        state_G.go_to_state('H')
  
        self.assertTrue(monitor_1.match_sequence().begin().exited('G').entered('H').end())
