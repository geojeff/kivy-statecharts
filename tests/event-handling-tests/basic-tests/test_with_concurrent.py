'''
Statechart tests, basic event handling, with concurrent states
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['rootState'] = self.RootState
        kwargs['monitorIsActive'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'X'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class X(State):
            fooInvokedCount = NumericProperty(0)

            def __init__(self, **kwargs):
                kwargs['substatesAreConcurrent'] = True
                super(Statechart_1.RootState.X, self).__init__(**kwargs)

            def foo(self, arg1=None, arg2=None):
                self.fooInvokedCount += 1

            class A(State):
                event_A_invoked = BooleanProperty(False)

                def __init__(self, **kwargs):
                    kwargs['initialSubstateKey'] = 'C'
                    super(Statechart_1.RootState.X.A, self).__init__(**kwargs)

                def event_A(self, arg1=None, arg2=None):
                    self.event_A_invoked = True

                class C(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.A.C, self).__init__(**kwargs)

                    def event_B(self, arg1=None, arg2=None):
                        self.gotoState('D')

                    def event_D(self, arg1=None, arg2=None):
                        self.gotoState('Y')

                class D(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.A.D, self).__init__(**kwargs)

                    def event_C(self, arg1=None, arg2=None):
                        self.gotoState('C')

            class B(State):
                event_A_invoked = BooleanProperty(False)

                def __init__(self, **kwargs):
                    kwargs['initialSubstateKey'] = 'E'
                    super(Statechart_1.RootState.X.B, self).__init__(**kwargs)

                def event_A(self, arg1=None, arg2=None):
                    self.event_A_invoked = True

                class E(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.B.E, self).__init__(**kwargs)

                    def event_B(self, arg1=None, arg2=None):
                        self.gotoState('F')

                    def event_D(self, arg1=None, arg2=None):
                        self.gotoState('Y')

                class F(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.B.F, self).__init__(**kwargs)

                    def event_C(self, arg1=None, arg2=None):
                        self.gotoState('E')

        class Y(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.Y, self).__init__(**kwargs)

class StateEventHandlingBasicWithConcurrentTestCase(unittest.TestCase):
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

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootState
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        state_C = statechart_1.getState('C')
        state_D = statechart_1.getState('D')
        state_E = statechart_1.getState('E')
        state_F = statechart_1.getState('F')

    # Send event event_A
    def test_send_event_a(self):
        monitor_1.reset()

        self.assertFalse(state_A.event_A_invoked)
        self.assertFalse(state_B.event_A_invoked)

        statechart_1.sendEvent('event_A')

        self.assertEqual(monitor_1.length, 0)

        self.assertTrue(statechart_1.stateIsCurrentState('C'))
        self.assertTrue(statechart_1.stateIsCurrentState('E'))

        self.assertTrue(state_A.event_A_invoked)
        self.assertTrue(state_B.event_A_invoked)

    # Send event event_B
    def test_send_event_b(self):
        monitor_1.reset()

        self.assertTrue(statechart_1.stateIsCurrentState('C'))
        self.assertTrue(statechart_1.stateIsCurrentState('E'))

        statechart_1.sendEvent('event_B')

        self.assertEqual(len(statechart_1.currentStates), 2)
        print statechart_1.currentStates
        self.assertTrue(statechart_1.stateIsCurrentState('D'))
        self.assertTrue(statechart_1.stateIsCurrentState('F'))

        self.assertEqual(monitor_1.length, 4)
        self.assertEqual(monitor_1.matchSequence().begin().beginConcurrent().beginSequence().exited('C').entered('D').endSequence().beginSequence().exited('E').entered('F').endSequence().endConcurrent().end(), True)

    # Send event event_B then event_C
    def test_send_event_b_then_c(self):
        statechart_1.sendEvent('event_B')

        self.assertTrue(statechart_1.stateIsCurrentState('D'))
        self.assertTrue(statechart_1.stateIsCurrentState('F'))

        monitor_1.reset()

        statechart_1.sendEvent('event_C')

        self.assertTrue(statechart_1.stateIsCurrentState('C'))
        self.assertTrue(statechart_1.stateIsCurrentState('E'))

        self.assertEqual(monitor_1.length, 4)
        self.assertEqual(monitor_1.matchSequence().begin().beginConcurrent().beginSequence().exited('D').entered('C').endSequence().beginSequence().exited('F').entered('E').endSequence().endConcurrent().end(), True)

    # Send event event_D
    def test_send_event_d(self):
        monitor_1.reset()

        self.assertTrue(statechart_1.stateIsCurrentState('C'))
        self.assertTrue(statechart_1.stateIsCurrentState('E'))

        statechart_1.sendEvent('event_D')

        self.assertEqual(monitor_1.length, 6)
        self.assertEqual(monitor_1.matchSequence().begin().beginConcurrent().beginSequence().exited('C', 'A').endSequence().beginSequence().exited('E', 'B').endSequence().endConcurrent().exited('X').entered('Y').end(), True)
                
        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertFalse(statechart_1.stateIsCurrentState('C'))
        self.assertFalse(statechart_1.stateIsCurrentState('E'))
        self.assertTrue(statechart_1.stateIsCurrentState('Y'))

    # Send event event_Z
    def test_send_event_z(self):
        monitor_1.reset()

        self.assertTrue(statechart_1.stateIsCurrentState('C'))
        self.assertTrue(statechart_1.stateIsCurrentState('E'))

        self.assertEqual(monitor_1.length, 0)

        statechart_1.sendEvent('event_Z')

        self.assertTrue(statechart_1.stateIsCurrentState('C'))
        self.assertTrue(statechart_1.stateIsCurrentState('E'))

    # Send event foo to statechart and ensure event is only handled once by state X
    def test_send_event_foo_and_check_handling_once_by_x(self):
        state_X = statechart_1.getState('X')

        self.assertEqual(state_X.fooInvokedCount, 0)

        statechart_1.sendEvent('foo')

        self.assertEqual(state_X.fooInvokedCount, 1)


