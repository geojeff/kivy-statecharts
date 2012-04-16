'''
Statechart tests, transitioning, standard, without concurrent, context
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

class TestState(State):
    enterStateContext = ObjectProperty(None)
    exitStateContext = ObjectProperty(None)
      
    def __init__(self, **kwargs):
        super(TestState, self).__init__(**kwargs)

    def enterState(self, context):
        self.enterStateContext = context
      
    def exitState(self, context):
        self.exitStateContext = context

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['rootStateClass'] = self.RootState
        kwargs['monitorIsActive'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(TestState):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(TestState):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'C'
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

            class C(TestState):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.C, self).__init__(**kwargs)

            class D(TestState):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.D, self).__init__(**kwargs)

        class B(TestState):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'E'
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
        global rootState_1
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
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootStateInstance
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        state_C = statechart_1.getState('C')
        state_D = statechart_1.getState('D')
        state_E = statechart_1.getState('E')
        state_F = statechart_1.getState('F')

    # Check statechart initializaton
    def test_statechart_initializaton(self):
        self.assertIsNone(rootState_1.enterStateContext)
        self.assertIsNone(state_A.enterStateContext)
        self.assertIsNone(state_C.enterStateContext)

    # Pass no context when going to state f using statechart
    def test_pass_no_context_when_going_to_state_f_using_statechart(self):
        statechart_1.gotoState('F')
        self.assertTrue(state_F.isCurrentState())
        self.assertIsNone(state_C.exitStateContext)
        self.assertIsNone(state_A.exitStateContext)
        self.assertIsNone(state_B.enterStateContext)
        self.assertIsNone(state_F.enterStateContext)

    # Pass no context when going to state f using state
    def test_pass_no_context_when_going_to_state_f_using_state(self):
        state_C.gotoState('F')
        self.assertTrue(state_F.isCurrentState())
        self.assertIsNone(state_C.exitStateContext)
        self.assertIsNone(state_A.exitStateContext)
        self.assertIsNone(state_B.enterStateContext)
        self.assertIsNone(state_F.enterStateContext)

    # Pass context when going to state f using statechart - gotoState('f', context)
    def test_pass_context_when_going_to_state_f_using_statechart_gotoState_f_context(self):
        statechart_1.gotoState('F', context=context)
        self.assertTrue(state_F.isCurrentState())
        self.assertEqual(state_C.exitStateContext, context)
        self.assertEqual(state_A.exitStateContext, context)
        self.assertEqual(state_B.enterStateContext, context)
        self.assertEqual(state_F.enterStateContext, context)

    # Pass context when going to state f using state - gotoState('f', context)
    def test_pass_context_when_going_to_state_f_using_state_gotoState_f_context(self):
        state_C.gotoState('F', context=context)
        self.assertTrue(state_F.isCurrentState())
        self.assertEqual(state_C.exitStateContext, context)
        self.assertEqual(state_A.exitStateContext, context)
        self.assertEqual(state_B.enterStateContext, context)
        self.assertEqual(state_F.enterStateContext, context)

    # Pass context when going to state f using statechart - gotoState('f', state_C, context)
    def test_pass_context_when_going_to_state_f_using_statechart_gotoState_f_state_C_context(self):
        statechart_1.gotoState('F', fromCurrentState=state_C, context=context)
        self.assertTrue(state_F.isCurrentState())
        self.assertEqual(state_C.exitStateContext, context)
        self.assertEqual(state_A.exitStateContext, context)
        self.assertEqual(state_B.enterStateContext, context)
        self.assertEqual(state_F.enterStateContext, context)

    # Pass context when going to state f using statechart - gotoState('f', false, context)
    def test_pass_context_when_going_to_state_f_using_statechart_gotoState_f_false_context(self):
        statechart_1.gotoState('F', useHistory=False, context=context)
        self.assertTrue(state_F.isCurrentState())
        self.assertEqual(state_C.exitStateContext, context)
        self.assertEqual(state_A.exitStateContext, context)
        self.assertEqual(state_B.enterStateContext, context)
        self.assertEqual(state_F.enterStateContext, context)

    # Pass context when going to state f using statechart - gotoState('f', state_C, false, context)
    def test_pass_context_when_going_to_state_f_using_statechart_gotoState_f_state_C_false_context(self):
        statechart_1.gotoState('F', fromCurrentState=state_C, useHistory=False, context=context)
        self.assertTrue(state_F.isCurrentState())
        self.assertEqual(state_C.exitStateContext, context)
        self.assertEqual(state_A.exitStateContext, context)
        self.assertEqual(state_B.enterStateContext, context)
        self.assertEqual(state_F.enterStateContext, context)

