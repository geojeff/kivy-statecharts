'''
Statechart tests, transitioning, history, standard, without concurrent, context
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class TestState(State):
    enter_stateContext = ObjectProperty(None)
    exit_stateContext = ObjectProperty(None)
      
    def __init__(self, **kwargs):
        super(TestState, self).__init__(**kwargs)

    def enter_state(self, context):
        self.enter_stateContext = context
      
    def exit_state(self, context):
        self.exit_stateContext = context

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['root_state_class'] = self.RootState
        kwargs['monitor_is_active'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(TestState):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(TestState):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'C'
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

            class C(TestState):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.C, self).__init__(**kwargs)

            class D(TestState):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.D, self).__init__(**kwargs)

        class B(TestState):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'E'
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

            class E(TestState):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.E, self).__init__(**kwargs)

            class F(TestState):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.F, self).__init__(**kwargs)

class StateTransitioningHistoryStandardContextWithoutConcurrentTestCase(unittest.TestCase):
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

        global context

        context = { 'foo': 100 }

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

        statechart_1.go_to_state('D')

    # Check statechart initializaton
    def test_statechart_initializaton(self):
        self.assertIsNone(root_state_1.enter_stateContext)
        self.assertIsNone(state_A.enter_stateContext)
        self.assertIsNone(state_D.enter_stateContext)

    # Pass no context when going to state a's history state using statechart
    def test_pass_no_context_when_going_to_state_f_then_state_a_history_state_using_statechart(self):
        statechart_1.go_to_state('F')
        statechart_1.go_to_history_state('A')
        self.assertTrue(state_D.is_current_state())
        self.assertIsNone(state_D.enter_stateContext)
        self.assertIsNone(state_A.enter_stateContext)
        self.assertIsNone(state_B.exit_stateContext)
        self.assertIsNone(state_F.exit_stateContext)

    # Pass no context when going to state a's history state using state
    def test_pass_no_context_when_going_to_state_f_then_state_a_history_state_using_state(self):
        state_D.go_to_state('F')
        state_F.go_to_history_state('A')
        self.assertTrue(state_D.is_current_state())
        self.assertIsNone(state_D.enter_stateContext)
        self.assertIsNone(state_A.enter_stateContext)
        self.assertIsNone(state_B.exit_stateContext)
        self.assertIsNone(state_F.exit_stateContext)

    # Pass context when going to state a history state using statechart - go_to_history_state('f', context)
    def test_pass_context_when_going_to_state_a_history_state_using_statechart_go_to_state_f_context(self):
        statechart_1.go_to_state('F')
        statechart_1.go_to_history_state('A', context=context)
        self.assertTrue(state_D.is_current_state())
        self.assertEqual(state_D.enter_stateContext, context)
        self.assertEqual(state_A.enter_stateContext, context)
        self.assertEqual(state_B.exit_stateContext, context)
        self.assertEqual(state_F.exit_stateContext, context)

    # Pass context when going to state a history state using state - go_to_history_state('f', context)
    def test_pass_context_when_going_to_state_f_using_state_go_to_state_f_context(self):
        statechart_1.go_to_state('F')
        state_F.go_to_history_state('A', context=context)
        self.assertTrue(state_D.is_current_state())
        self.assertEqual(state_D.enter_stateContext, context)
        self.assertEqual(state_A.enter_stateContext, context)
        self.assertEqual(state_B.exit_stateContext, context)
        self.assertEqual(state_F.exit_stateContext, context)

    # Pass context when going to state a history state using statechart - go_to_state('f', state_F, context)
    def test_pass_context_when_going_to_state_a_history_state_using_statechart_go_to_state_f_state_C_context(self):
        statechart_1.go_to_state('F')
        statechart_1.go_to_history_state('A', from_current_state=state_F, context=context)
        self.assertTrue(state_D.is_current_state())
        self.assertEqual(state_D.enter_stateContext, context)
        self.assertEqual(state_A.enter_stateContext, context)
        self.assertEqual(state_B.exit_stateContext, context)
        self.assertEqual(state_F.exit_stateContext, context)

    # Pass context when going to state a history state using statechart - go_to_state('f', true, context)
    def test_pass_context_when_going_to_state_a_history_state_using_statechart_go_to_state_f_true_context(self):
        statechart_1.go_to_state('F')
        statechart_1.go_to_history_state('A', recursive=True, context=context)
        self.assertTrue(state_D.is_current_state())
        self.assertEqual(state_D.enter_stateContext, context)
        self.assertEqual(state_A.enter_stateContext, context)
        self.assertEqual(state_B.exit_stateContext, context)
        self.assertEqual(state_F.exit_stateContext, context)

    # Pass context when going to state a history state using statechart - go_to_state('f', state_F, true, context)
    def test_pass_context_when_going_to_state_a_history_state_using_statechart_go_to_state_f_state_f_true_context(self):
        statechart_1.go_to_state('F')
        statechart_1.go_to_history_state('A', from_current_state=state_F, recursive=True, context=context)
        self.assertTrue(state_D.is_current_state())
        self.assertEqual(state_D.enter_stateContext, context)
        self.assertEqual(state_A.enter_stateContext, context)
        self.assertEqual(state_B.exit_stateContext, context)
        self.assertEqual(state_F.exit_stateContext, context)

    # Pass context when going to state a history state using statechart - go_to_state('f', true, context)
    def test_pass_context_when_going_to_state_a_history_state_using_statechart_go_to_state_f_true_context(self):
        statechart_1.go_to_state('F')
        state_F.go_to_history_state('A', recursive=True, context=context)
        self.assertTrue(state_D.is_current_state())
        self.assertEqual(state_D.enter_stateContext, context)
        self.assertEqual(state_A.enter_stateContext, context)
        self.assertEqual(state_B.exit_stateContext, context)
        self.assertEqual(state_F.exit_stateContext, context)
