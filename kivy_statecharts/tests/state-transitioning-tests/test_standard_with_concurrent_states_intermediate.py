'''
Statechart tests, transitioning, standard, with concurrent, intermediate
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
                        super(Statechart_1.RootState.A.C.F, self).__init__(**kwargs)

                class G(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.C.G, self).__init__(**kwargs)

        class Z(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.Z, self).__init__(**kwargs)

class StateTransitioningStandardIntermediateWithConcurrentTestCase(unittest.TestCase):
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
        state_Z = statechart_1.get_state('Z')

    # Test statechart initialization
    def test_statechart_initialization(self):
        self.assertEqual(monitor_1.length, 6)

        self.assertTrue(monitor_1.match_sequence().begin().entered(root_state_1, 'A').begin_concurrent().begin_sequence().entered('B', 'D').end_sequence().begin_sequence().entered('C', 'F').end_sequence().end_concurrent().end())
  
        self.assertEqual(len(statechart_1.current_states), 2)
  
        self.assertTrue(statechart_1.state_is_current_state('D'))
        self.assertTrue(statechart_1.state_is_current_state('F'))
        self.assertTrue(state_A.state_is_current_substate('D'))
        self.assertTrue(state_A.state_is_current_substate('F'))
        self.assertFalse(state_A.state_is_current_substate('E'))
        self.assertFalse(state_A.state_is_current_substate('G'))
        self.assertTrue(state_B.state_is_current_substate('D'))
        self.assertFalse(state_B.state_is_current_substate('E'))
        self.assertTrue(state_C.state_is_current_substate('F'))
        self.assertFalse(state_C.state_is_current_substate('G'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'A', 'B', 'C', 'D', 'F'))

    # Test from state D, go to state Z
    def test_from_d_to_z(self):
        monitor_1.reset()
        state_D.go_to_state('Z')
  
        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.match_sequence().begin().exited('D', 'B', 'F', 'C', 'A').entered('Z').end())
        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('Z'))
        self.assertEqual(len(state_A.current_substates), 0)
        self.assertFalse(state_A.state_is_current_substate('D'))
        self.assertFalse(state_A.state_is_current_substate('F'))
        self.assertFalse(state_A.state_is_current_substate('E'))
        self.assertFalse(state_A.state_is_current_substate('G'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'Z'))

    # Test from state A, go to state Z, and then back to state A
    def test_from_a_to_z_and_back_to_a(self):
        monitor_1.reset()
        state_A.go_to_state('Z')
  
        self.assertEqual(monitor_1.length, 6)

        self.assertTrue(monitor_1.match_sequence().begin().begin_concurrent().begin_sequence().exited('D', 'B').end_sequence().begin_sequence().exited('F', 'C').end_sequence().end_concurrent().exited('A').entered('Z').end())
  
        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(statechart_1.state_is_current_state('Z'))
  
        monitor_1.reset()
        state_Z.go_to_state('A')
  
        self.assertEqual(monitor_1.length, 6)

        self.assertTrue(monitor_1.match_sequence().begin().exited('Z').entered('A').begin_concurrent().begin_sequence().entered('B', 'D').end_sequence().begin_sequence().entered('C', 'F').end_sequence().end_concurrent().end())
  
        self.assertEqual(len(statechart_1.current_states), 2)
        self.assertTrue(statechart_1.state_is_current_state('D'))
        self.assertTrue(statechart_1.state_is_current_state('F'))
        self.assertEqual(len(statechart_1.current_states), 2)
        self.assertTrue(state_A.state_is_current_substate('D'))
        self.assertFalse(state_A.state_is_current_substate('E'))
        self.assertTrue(state_A.state_is_current_substate('F'))
        self.assertFalse(state_A.state_is_current_substate('G'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'A', 'B', 'C', 'D', 'F'))
