'''
Statechart tests, basic event handling, without concurrent states
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
        kwargs['trace'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'C'
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

            def event_B(self, arg1=None, arg2=None):
                self.gotoState('B')

            class C(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.C, self).__init__(**kwargs)

                def event_A(self, arg1=None, arg2=None):
                    self.gotoState('D')

            class D(State):
                sender = ObjectProperty(None)
                context = ObjectProperty(None)

                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.D, self).__init__(**kwargs)

                def event_C(self, sender=None, context=None):
                    self.sender = sender
                    self.context = context
                    self.gotoState('F')

        class B(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'E'
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

            class E(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.E, self).__init__(**kwargs)

            class F(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.F, self).__init__(**kwargs)

class StateEventHandlingBasicWithoutConcurrentTestCase(unittest.TestCase):
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

    # Send event event_A while in state C
    def test_send_event_a_while_in_state_c(self):
        monitor_1.reset()

        statechart_1.sendEvent('event_A')

        self.assertEqual(monitor_1.length, 2)
        self.assertTrue(monitor_1.matchSequence().begin().exited('C').entered('D').end())
        self.assertTrue(statechart_1.stateIsCurrentState('D'))

    # Send event event_B while in parent state A
    def test_send_event_b_while_in_parent_state_a(self):
        monitor_1.reset()

        statechart_1.sendEvent('event_B')

        self.assertEqual(monitor_1.length, 4)
        self.assertTrue(monitor_1.matchSequence().begin().exited('C', 'A').entered('B', 'E').end())
        self.assertTrue(statechart_1.stateIsCurrentState('E'))

    # Send event event_C while in state D
    def test_send_event_c_while_in_state_d(self):
        statechart_1.gotoState('D')

        monitor_1.reset()

        statechart_1.sendEvent('event_C', statechart_1, 'foobar')

        self.assertEqual(monitor_1.length, 4)
        self.assertTrue(monitor_1.matchSequence().begin().exited('D', 'A').entered('B', 'F').end())
        self.assertTrue(statechart_1.stateIsCurrentState('F'))
        self.assertEqual(state_D.sender, statechart_1)
        self.assertEqual(state_D.context, 'foobar')

    # Send event event_C while in state C
    def test_send_event_c_while_in_state_c(self):
        monitor_1.reset()

        statechart_1.sendEvent('event_C')

        self.assertEqual(monitor_1.length, 0)
        self.assertTrue(statechart_1.stateIsCurrentState('C'))

    # Send event event_D while in state C
    def test_send_event_d_while_in_state_c(self):
        monitor_1.reset()

        statechart_1.sendEvent('event_D')

        self.assertEqual(monitor_1.length, 0)
        self.assertTrue(statechart_1.stateIsCurrentState('C'))


