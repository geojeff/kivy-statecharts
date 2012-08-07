'''
Statechart tests, basic event handling, with concurrent states
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class AsyncState(State):
    counter = NumericProperty(0)
    
    def foo(self, arg1, arg2):
        self.counter += 1
        self.resumeGotoState()
      
    def enterState(self, context):
        print 'calling foo'
        return self.performAsync('foo')
      
    def exitState(self, context):
        def func(self, arg1, arg2):
            self.foo(arg1, arg2)
        return self.performAsync(func)

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['rootStateClass'] = self.RootState
        kwargs['monitorIsActive'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['substatesAreConcurrent'] = True
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

            class C(AsyncState):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.C, self).__init__(**kwargs)

            class D(AsyncState):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.D, self).__init__(**kwargs)

class StateStateTransitioningAsyncWithConcurrentTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global rootState_1
        global monitor_1
        global state_A
        global state_B
        global state_C
        global state_D

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootStateInstance
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        state_C = statechart_1.getState('C')
        state_D = statechart_1.getState('D')

    # Go to state B
    def test_go_to_state_B(self):
        monitor_1.reset()

        self.assertFalse(statechart_1.gotoStateActive)
        self.assertFalse(statechart_1.gotoStateSuspended)

        self.assertTrue(state_A.isCurrentState())
        self.assertFalse(state_B.isCurrentState())
        self.assertFalse(state_C.isCurrentState())
        self.assertFalse(state_D.isCurrentState())

        state_A.gotoState('B')

        self.assertFalse(statechart_1.gotoStateActive)
        self.assertFalse(statechart_1.gotoStateSuspended)

        self.assertEqual(monitor_1.matchSequence().begin().exited('A').entered('B').beginConcurrent().entered('C', 'D').endConcurrent().end(), True)

        self.assertEqual(len(statechart_1.currentStates), 2)
        self.assertTrue(state_C.isCurrentState())
        self.assertTrue(state_D.isCurrentState())
        self.assertEqual(state_C.counter, 1)
        self.assertEqual(state_D.counter, 1)

    # Go to state B, then back to state A
    def test_go_to_state_B_then_back_to_A(self):
        monitor_1.reset()

        self.assertFalse(statechart_1.gotoStateActive)
        self.assertFalse(statechart_1.gotoStateSuspended)

        self.assertTrue(state_A.isCurrentState())
        self.assertFalse(state_B.isCurrentState())
        self.assertFalse(state_C.isCurrentState())
        self.assertFalse(state_D.isCurrentState())

        state_A.gotoState('B')

        monitor_1.reset()

        state_C.gotoState('A')

        self.assertFalse(statechart_1.gotoStateActive)
        self.assertFalse(statechart_1.gotoStateSuspended)

        self.assertEqual(monitor_1.matchSequence().begin().exited('C', 'D', 'B').entered('A').end(), True)

        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(state_A.isCurrentState())
        self.assertFalse(state_C.isCurrentState())
        self.assertFalse(state_D.isCurrentState())
        self.assertEqual(state_C.counter, 2)
        self.assertEqual(state_D.counter, 2)

