'''
Statechart tests, transitioning, transient, without concurrent
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
                kwargs['initial_substate_key'] = 'B'
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

            class B(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.B, self).__init__(**kwargs)

                def event_C(self, arg1=None, arg2=None):
                    self.go_to_state('C')

                def event_D(self, arg1=None, arg2=None):
                    self.go_to_state('D')

                def event_E(self, arg1=None, arg2=None):
                    self.go_to_state('E')

                def event_X(self, arg1=None, arg2=None):
                    self.go_to_state('X')

            class C(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.C, self).__init__(**kwargs)

                def enter_state(self, context):
                    self.go_to_state('Z')

            class D(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.D, self).__init__(**kwargs)

                def enter_state(self, context):
                    self.go_to_state('C')

            class E(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.E, self).__init__(**kwargs)

                def enter_state(self, context):
                    self.go_to_state('F')

            class F(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.F, self).__init__(**kwargs)

            class G(State):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'X'
                    super(Statechart_1.RootState.A.G, self).__init__(**kwargs)

                def foo(self, arg1=None, arg2=None):
                    pass

                def enter_state(self, context):
                    return self.perform_async('foo')

                class X(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.G.X, self).__init__(**kwargs)

                    def enter_state(self, context):
                        self.go_to_state('H')

            class H(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.H, self).__init__(**kwargs)

        class Z(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.Z, self).__init__(**kwargs)

class StateTransitioningStandardCoreWithoutConcurrentTestCase(unittest.TestCase):
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
        global state_X
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
        state_X = statechart_1.get_state('X')
        state_Z = statechart_1.get_state('Z')

    # Enter transient state C
    def test_enter_transient_state_c(self):
        monitor_1.reset()
        
        statechart_1.send_event('event_C')

        self.assertEqual(monitor_1.length, 5)
        self.assertTrue(monitor_1.match_sequence().begin().exited('B').entered('C').exited('C', 'A').entered('Z').end())
        self.assertTrue(statechart_1.state_is_current_state('Z'))
        self.assertEqual(state_A.history_state, state_C)

    # Enter transient state D
    def test_enter_transient_state_d(self):
        monitor_1.reset()
        
        statechart_1.send_event('event_D')

        self.assertEqual(monitor_1.length, 7)
        self.assertTrue(monitor_1.match_sequence().begin().exited('B').entered('D').exited('D').entered('C').exited('C', 'A').entered('Z').end())
        self.assertTrue(statechart_1.state_is_current_state('Z'))
        self.assertEqual(state_A.history_state, state_C)

    # Enter transient state X
    def test_enter_transient_state_x(self):
        monitor_1.reset()
        
        statechart_1.send_event('event_X')

        self.assertEqual(monitor_1.length, 2)
        self.assertTrue(monitor_1.match_sequence().begin().exited('B').entered('G').end())
        self.assertTrue(statechart_1.go_to_state_active)
        self.assertTrue(statechart_1.go_to_state_suspended)

        statechart_1.resume_go_to_state()

        self.assertEqual(monitor_1.length, 6)

        self.assertTrue(monitor_1.match_sequence().begin().exited('B').entered('G', 'X').exited('X', 'G').entered('H').end())

        self.assertFalse(statechart_1.go_to_state_active)
        self.assertFalse(statechart_1.go_to_state_suspended)

        self.assertEqual(state_A.history_state, state_H)
