'''
Statechart tests, transitioning, standard, with concurrent, basic
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
            kwargs['substates_are_concurrent'] = True
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
                kwargs['initial_substate_key'] = 'E'
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

            class E(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.E, self).__init__(**kwargs)

            class F(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.F, self).__init__(**kwargs)

class StateTransitioningStandardBasicWithConcurrentTestCase(unittest.TestCase):
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

    # Check statechart initialization
    def test_statechart_initialization(self):
        self.assertEqual(monitor_1.length, 5)

        self.assertTrue(monitor_1.match_sequence().begin().entered(root_state_1).begin_concurrent().begin_sequence().entered('A', 'C').end_sequence().begin_sequence().entered('B', 'E').end_sequence().end_concurrent() .end())
        self.assertFalse(monitor_1.match_sequence().begin().entered(root_state_1).begin_concurrent().entered('A', 'B').end_concurrent().begin_concurrent().entered('C', 'E').end_concurrent().end())
  
        self.assertEqual(len(statechart_1.current_states), 2)
  
        self.assertTrue(statechart_1.state_is_current_state('C'))
        self.assertTrue(statechart_1.state_is_current_state('E'))
        self.assertFalse(statechart_1.state_is_current_state('D'))
        self.assertFalse(statechart_1.state_is_current_state('F'))
  
        self.assertTrue(state_A.state_is_current_substate('C'))
        self.assertFalse(state_A.state_is_current_substate('D'))
        self.assertTrue(state_B.state_is_current_substate('E'))
        self.assertFalse(state_B.state_is_current_substate('F'))
  
        self.assertFalse(state_A.is_current_state())
        self.assertFalse(state_B.is_current_state())
        self.assertTrue(state_C.is_current_state())
        self.assertFalse(state_D.is_current_state())
        self.assertTrue(state_E.is_current_state())
        self.assertFalse(state_F.is_current_state())

    # From state C, go to state D, and from state E, go to state F
    def test_from_C_to_D_and_from_E_to_F(self):
        monitor_1.reset()

        state_C.go_to_state('D')

        self.assertEqual(monitor_1.length, 2)

        self.assertTrue(monitor_1.match_sequence().begin().exited('C').entered('D').end())
  
        monitor_1.reset()
  
        state_E.go_to_state('F')

        self.assertEqual(monitor_1.length, 2)
        self.assertTrue(monitor_1.match_sequence().begin().exited('E').entered('F').end())
  
        self.assertEqual(len(statechart_1.current_states), 2)
  
        self.assertTrue(statechart_1.state_is_current_state('D'))
        self.assertTrue(statechart_1.state_is_current_state('F'))
  
        self.assertFalse(state_A.state_is_current_substate('C'))
        self.assertTrue(state_A.state_is_current_substate('D'))
        self.assertFalse(state_B.state_is_current_substate('E'))
        self.assertTrue(state_B.state_is_current_substate('F'))
  
        self.assertFalse(state_A.is_current_state())
        self.assertFalse(state_B.is_current_state())
        self.assertFalse(state_C.is_current_state())
        self.assertTrue(state_D.is_current_state())
        self.assertFalse(state_E.is_current_state())
        self.assertTrue(state_F.is_current_state())
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'A', 'D', 'B', 'F'))

    # From state A, go to sibling concurrent state B
    def test_from_a_to_sibling_concurrent_state_b(self):
        monitor_1.reset()

        with self.assertRaises(Exception) as cm:
            state_A.go_to_state('B')
        msg = ("Cannot go to state B from A.C. Pivot state __ROOT_STATE__ "
               "has concurrent substates.")
        self.assertEqual(str(cm.exception), msg)

        self.assertEqual(monitor_1.length, 0)
        self.assertEqual(len(statechart_1.current_states), 2)
        self.assertTrue(statechart_1.state_is_current_state('C'))
        self.assertTrue(statechart_1.state_is_current_state('E'))
        self.assertTrue(state_A.state_is_current_substate('C'))
        self.assertFalse(state_A.state_is_current_substate('D'))
        self.assertTrue(state_B.state_is_current_substate('E'))
        self.assertFalse(state_B.state_is_current_substate('F'))
  
        self.assertIsNotNone(monitor_1.match_entered_states(root_state_1, 'A', 'C', 'B', 'E'))
