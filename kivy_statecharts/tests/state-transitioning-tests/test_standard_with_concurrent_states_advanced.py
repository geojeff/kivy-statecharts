'''
Statechart tests, transitioning, standard, with concurrent, advanced
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
                kwargs['substates_are_concurrent'] = True
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

            class B(State):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'D'
                    super(Statechart_1.RootState.A.B, self).__init__(**kwargs)

                class D(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.B.D, self).__init__(**kwargs)

                class E(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.B.E, self).__init__(**kwargs)

            class C(State):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'F'
                    super(Statechart_1.RootState.A.C, self).__init__(**kwargs)

                class F(State):
                    def __init__(self, **kwargs):
                        kwargs['substates_are_concurrent'] = True
                        super(Statechart_1.RootState.A.C.F, self).__init__(**kwargs)

                    class H(State):
                        def __init__(self, **kwargs):
                            kwargs['initial_substate_key'] = 'L'
                            super(Statechart_1.RootState.A.C.F.H, self).__init__(**kwargs)

                        class L(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.F.H.L, self).__init__(**kwargs)

                        class M(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.F.H.M, self).__init__(**kwargs)

                    class I(State):
                        def __init__(self, **kwargs):
                            kwargs['initial_substate_key'] = 'N'
                            super(Statechart_1.RootState.A.C.F.I, self).__init__(**kwargs)

                        class N(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.F.I.N, self).__init__(**kwargs)

                        class O(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.F.I.O, self).__init__(**kwargs)

                class G(State):
                    def __init__(self, **kwargs):
                        kwargs['substates_are_concurrent'] = True
                        super(Statechart_1.RootState.A.C.G, self).__init__(**kwargs)

                    class J(State):
                        def __init__(self, **kwargs):
                            kwargs['initial_substate_key'] = 'P'
                            super(Statechart_1.RootState.A.C.G.J, self).__init__(**kwargs)

                        class P(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.G.J.P, self).__init__(**kwargs)

                        class Q(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.G.J.Q, self).__init__(**kwargs)

                    class K(State):
                        def __init__(self, **kwargs):
                            kwargs['initial_substate_key'] = 'R'
                            super(Statechart_1.RootState.A.C.G.K, self).__init__(**kwargs)

                        class R(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.G.K.R, self).__init__(**kwargs)

                        class S(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.G.K.S, self).__init__(**kwargs)

        class Z(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.Z, self).__init__(**kwargs)

class StateTransitioningStandardAdvancedWithConcurrentTestCase(unittest.TestCase):
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
        global state_O
        global state_P
        global state_Q
        global state_R
        global state_S
        global state_Z

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
        state_O = statechart_1.get_state('O')
        state_P = statechart_1.get_state('P')
        state_Q = statechart_1.get_state('Q')
        state_R = statechart_1.get_state('R')
        state_S = statechart_1.get_state('S')
        state_Z = statechart_1.get_state('Z')

    # Test statechart initialization
    def test_statechart_initialization(self):
        self.assertEqual(monitor_1.length, 10)
        self.assertTrue(monitor_1.match_sequence().begin().entered(root_state_1, 'A').begin_concurrent().begin_sequence().entered('B', 'D').end_sequence().begin_sequence().entered('C', 'F').begin_concurrent().begin_sequence().entered('H', 'L').end_sequence().begin_sequence().entered('I', 'N').end_sequence().end_concurrent().end_sequence().end_concurrent().entered().end())
  
        self.assertEqual(len(statechart_1.current_states), 3)
        self.assertTrue(statechart_1.state_is_current_state('D'))
        self.assertTrue(statechart_1.state_is_current_state('L'))
        self.assertTrue(statechart_1.state_is_current_state('N'))
  
        self.assertFalse(statechart_1.state_is_current_state('H'))
        self.assertFalse(statechart_1.state_is_current_state('I'))
        self.assertFalse(statechart_1.state_is_current_state('P'))
        self.assertFalse(statechart_1.state_is_current_state('Q'))
        self.assertFalse(statechart_1.state_is_current_state('R'))
        self.assertFalse(statechart_1.state_is_current_state('S'))
  
        self.assertEqual(len(state_A.current_substates), 3)
        self.assertTrue(state_A.state_is_current_substate('D'))
        self.assertTrue(state_A.state_is_current_substate('L'))
        self.assertTrue(state_A.state_is_current_substate('N'))
  
        self.assertEqual(len(state_C.current_substates), 2)
        self.assertTrue(state_C.state_is_current_substate('L'))
        self.assertTrue(state_C.state_is_current_substate('N'))
  
        self.assertEqual(len(state_F.current_substates), 2)
        self.assertTrue(state_F.state_is_current_substate('L'))
        self.assertTrue(state_F.state_is_current_substate('N'))
  
        self.assertEqual(len(state_G.current_substates), 0)
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'A', 'B', 'D', 'C', 'F', 'H', 'I', 'L', 'N'))


    # Test from state L to state G
    def test_from_l_to_g(self):
        monitor_1.reset()
        state_L.go_to_state('G')
  
        self.assertEqual(monitor_1.length, 10)
        self.assertTrue(monitor_1.match_sequence().begin().begin_concurrent().begin_sequence().exited('L', 'H').end_sequence().begin_sequence().exited('N', 'I').end_sequence().end_concurrent().exited('F').entered('G').begin_concurrent().begin_sequence().entered('J', 'P').end_sequence().begin_sequence().entered('K', 'R').end_sequence().end_concurrent().end())
  
        self.assertEqual(len(statechart_1.current_states), 3)
        self.assertTrue(statechart_1.state_is_current_state('D'))
        self.assertFalse(statechart_1.state_is_current_state('L'))
        self.assertFalse(statechart_1.state_is_current_state('N'))
        self.assertTrue(statechart_1.state_is_current_state('P'))
        self.assertTrue(statechart_1.state_is_current_state('R'))
  
        self.assertEqual(len(state_A.current_substates), 3)
        self.assertTrue(state_A.state_is_current_substate('D'))
        self.assertTrue(state_A.state_is_current_substate('P'))
        self.assertTrue(state_A.state_is_current_substate('R'))
  
        self.assertEqual(len(state_C.current_substates), 2)
        self.assertTrue(state_C.state_is_current_substate('P'))
        self.assertTrue(state_C.state_is_current_substate('R'))
  
        self.assertEqual(len(state_F.current_substates), 0)
  
        self.assertEqual(len(state_G.current_substates), 2)
        self.assertTrue(state_G.state_is_current_substate('P'))
        self.assertTrue(state_G.state_is_current_substate('R'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'A', 'B', 'D', 'C', 'G', 'J', 'K', 'P', 'R'))

    # Test from state L to state Z
    def test_from_l_to_z(self):
        monitor_1.reset()
        state_L.go_to_state('Z')
  
        self.assertEqual(monitor_1.length, 10)

        self.assertTrue(monitor_1.match_sequence().begin().exited('L', 'H', 'N', 'I', 'F', 'C', 'D', 'B', 'A').entered('Z').end())
         
        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('Z'))
        self.assertFalse(statechart_1.state_is_current_state('L'))
        self.assertFalse(statechart_1.state_is_current_state('N'))
        self.assertFalse(statechart_1.state_is_current_state('D'))
   
        self.assertEqual(len(state_A.current_substates), 0)
        self.assertEqual(len(state_B.current_substates), 0)
        self.assertEqual(len(state_C.current_substates), 0)
        self.assertEqual(len(state_F.current_substates), 0)
        self.assertEqual(len(state_G.current_substates), 0)
   
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'Z'))

    # Test from state L to state Z, and then to S
    def test_from_l_to_z_to_s(self):
        state_L.go_to_state('Z')
  
        monitor_1.reset()
        state_Z.go_to_state('S')

        self.assertEqual(monitor_1.length, 10)

        self.assertTrue(monitor_1.match_sequence().begin().exited('Z').entered('A', 'C', 'G', 'K', 'S', 'J', 'P', 'B', 'D').end())
         
        self.assertEqual(len(statechart_1.current_states), 3)
        self.assertFalse(statechart_1.state_is_current_state('Z'))
        self.assertTrue(statechart_1.state_is_current_state('S'))
        self.assertTrue(statechart_1.state_is_current_state('P'))
        self.assertTrue(statechart_1.state_is_current_state('D'))
   
        self.assertEqual(len(state_A.current_substates), 3)
        self.assertEqual(len(state_B.current_substates), 1)
        self.assertEqual(len(state_C.current_substates), 2)
        self.assertEqual(len(state_F.current_substates), 0)
        self.assertEqual(len(state_G.current_substates), 2)
   
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'A', 'B', 'D', 'C', 'G', 'J', 'K', 'P', 'S'))
