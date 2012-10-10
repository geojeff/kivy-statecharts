'''
Statechart tests, transitioning, standard, without concurrent, context
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

class StateTransitioningStandardContextWithoutConcurrentTestCase(unittest.TestCase):
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

    # Check statechart initializaton
    def test_statechart_initializaton(self):
        self.assertIsNone(root_state_1.enter_stateContext)
        self.assertIsNone(state_A.enter_stateContext)
        self.assertIsNone(state_C.enter_stateContext)

    # Pass no context when going to state f using statechart
    def test_pass_no_context_when_going_to_state_f_using_statechart(self):
        statechart_1.go_to_state('F')
        self.assertTrue(state_F.is_current_state())
        self.assertIsNone(state_C.exit_stateContext)
        self.assertIsNone(state_A.exit_stateContext)
        self.assertIsNone(state_B.enter_stateContext)
        self.assertIsNone(state_F.enter_stateContext)

    # Pass no context when going to state f using state
    def test_pass_no_context_when_going_to_state_f_using_state(self):
        state_C.go_to_state('F')
        self.assertTrue(state_F.is_current_state())
        self.assertIsNone(state_C.exit_stateContext)
        self.assertIsNone(state_A.exit_stateContext)
        self.assertIsNone(state_B.enter_stateContext)
        self.assertIsNone(state_F.enter_stateContext)

    # Pass context when going to state f using statechart - go_to_state('f', context)
    def test_pass_context_when_going_to_state_f_using_statechart_go_to_state_f_context(self):
        statechart_1.go_to_state('F', context=context)
        self.assertTrue(state_F.is_current_state())
        self.assertEqual(state_C.exit_stateContext, context)
        self.assertEqual(state_A.exit_stateContext, context)
        self.assertEqual(state_B.enter_stateContext, context)
        self.assertEqual(state_F.enter_stateContext, context)

    # Pass context when going to state f using state - go_to_state('f', context)
    def test_pass_context_when_going_to_state_f_using_state_go_to_state_f_context(self):
        state_C.go_to_state('F', context=context)
        self.assertTrue(state_F.is_current_state())
        self.assertEqual(state_C.exit_stateContext, context)
        self.assertEqual(state_A.exit_stateContext, context)
        self.assertEqual(state_B.enter_stateContext, context)
        self.assertEqual(state_F.enter_stateContext, context)

    # Pass context when going to state f using statechart - go_to_state('f', state_C, context)
    def test_pass_context_when_going_to_state_f_using_statechart_go_to_state_f_state_C_context(self):
        statechart_1.go_to_state('F', from_current_state=state_C, context=context)
        self.assertTrue(state_F.is_current_state())
        self.assertEqual(state_C.exit_stateContext, context)
        self.assertEqual(state_A.exit_stateContext, context)
        self.assertEqual(state_B.enter_stateContext, context)
        self.assertEqual(state_F.enter_stateContext, context)

    # Pass context when going to state f using statechart - go_to_state('f', false, context)
    def test_pass_context_when_going_to_state_f_using_statechart_go_to_state_f_false_context(self):
        statechart_1.go_to_state('F', use_history=False, context=context)
        self.assertTrue(state_F.is_current_state())
        self.assertEqual(state_C.exit_stateContext, context)
        self.assertEqual(state_A.exit_stateContext, context)
        self.assertEqual(state_B.enter_stateContext, context)
        self.assertEqual(state_F.enter_stateContext, context)

    # Pass context when going to state f using statechart - go_to_state('f', state_C, false, context)
    def test_pass_context_when_going_to_state_f_using_statechart_go_to_state_f_state_C_false_context(self):
        statechart_1.go_to_state('F', from_current_state=state_C, use_history=False, context=context)
        self.assertTrue(state_F.is_current_state())
        self.assertEqual(state_C.exit_stateContext, context)
        self.assertEqual(state_A.exit_stateContext, context)
        self.assertEqual(state_B.enter_stateContext, context)
        self.assertEqual(state_F.enter_stateContext, context)

