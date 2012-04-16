'''
Statechart tests, transitioning, transient, without concurrent
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
        kwargs['rootStateClass'] = self.RootState
        kwargs['monitorIsActive'] = True
        super(Statechart_1, self).__init__(**kwargs)
    
    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'B'
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

            class B(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.B, self).__init__(**kwargs)

                def event_C(self, arg1=None, arg2=None):
                    self.gotoState('C')

                def event_D(self, arg1=None, arg2=None):
                    self.gotoState('D')

                def event_E(self, arg1=None, arg2=None):
                    self.gotoState('E')

                def event_X(self, arg1=None, arg2=None):
                    self.gotoState('X')

            class C(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.C, self).__init__(**kwargs)

                def enterState(self, context):
                    self.gotoState('Z')

            class D(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.D, self).__init__(**kwargs)

                def enterState(self, context):
                    self.gotoState('C')

            class E(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.E, self).__init__(**kwargs)

                def enterState(self, context):
                    self.gotoState('F')

            class F(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.F, self).__init__(**kwargs)

            class G(State):
                def __init__(self, **kwargs):
                    kwargs['initialSubstateKey'] = 'X'
                    super(Statechart_1.RootState.A.G, self).__init__(**kwargs)

                def foo(self, arg1=None, arg2=None):
                    pass

                def enterState(self, context):
                    return self.performAsync('foo')

                class X(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.G.X, self).__init__(**kwargs)

                    def enterState(self, context):
                        self.gotoState('H')

            class H(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.H, self).__init__(**kwargs)

        class Z(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.Z, self).__init__(**kwargs)

class StateTransitioningStandardCoreWithoutConcurrentTestCase(unittest.TestCase):
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
        global state_G
        global state_H
        global state_X
        global state_Z

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
        state_G = statechart_1.getState('G')
        state_H = statechart_1.getState('H')
        state_X = statechart_1.getState('X')
        state_Z = statechart_1.getState('Z')

    # Enter transient state C
    def test_enter_transient_state_c(self):
        monitor_1.reset()
        
        statechart_1.sendEvent('event_C')

        self.assertEqual(monitor_1.length, 5)
        self.assertTrue(monitor_1.matchSequence().begin().exited('B').entered('C').exited('C', 'A').entered('Z').end())
        self.assertTrue(statechart_1.stateIsCurrentState('Z'))
        self.assertEqual(state_A.historyState, state_C)

    # Enter transient state D
    def test_enter_transient_state_d(self):
        monitor_1.reset()
        
        statechart_1.sendEvent('event_D')

        self.assertEqual(monitor_1.length, 7)
        self.assertTrue(monitor_1.matchSequence().begin().exited('B').entered('D').exited('D').entered('C').exited('C', 'A').entered('Z').end())
        self.assertTrue(statechart_1.stateIsCurrentState('Z'))
        self.assertEqual(state_A.historyState, state_C)

    # Enter transient state X
    def test_enter_transient_state_x(self):
        monitor_1.reset()
        
        statechart_1.sendEvent('event_X')

        self.assertEqual(monitor_1.length, 2)
        self.assertTrue(monitor_1.matchSequence().begin().exited('B').entered('G').end())
        self.assertTrue(statechart_1.gotoStateActive)
        self.assertTrue(statechart_1.gotoStateSuspended)

        statechart_1.resumeGotoState()

        self.assertEqual(monitor_1.length, 6)

        self.assertTrue(monitor_1.matchSequence().begin().exited('B').entered('G', 'X').exited('X', 'G').entered('H').end())

        self.assertFalse(statechart_1.gotoStateActive)
        self.assertFalse(statechart_1.gotoStateSuspended)

        self.assertEqual(state_A.historyState, state_H)
