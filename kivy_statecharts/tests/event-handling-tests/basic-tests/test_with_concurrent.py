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

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['root_state_class'] = self.RootState
        kwargs['monitor_is_active'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'X'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class X(State):
            foo_invoked_count = NumericProperty(0)

            def __init__(self, **kwargs):
                kwargs['substates_are_concurrent'] = True
                super(Statechart_1.RootState.X, self).__init__(**kwargs)

            def foo(self, arg1=None, arg2=None):
                self.foo_invoked_count += 1

            class A(State):
                event_A_invoked = BooleanProperty(False)

                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'C'
                    super(Statechart_1.RootState.X.A, self).__init__(**kwargs)

                def event_A(self, arg1=None, arg2=None):
                    self.event_A_invoked = True

                class C(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.A.C, self).__init__(**kwargs)

                    def event_B(self, arg1=None, arg2=None):
                        self.go_to_state('D')

                    def event_D(self, arg1=None, arg2=None):
                        self.go_to_state('Y')

                class D(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.A.D, self).__init__(**kwargs)

                    def event_C(self, arg1=None, arg2=None):
                        self.go_to_state('C')

            class B(State):
                event_A_invoked = BooleanProperty(False)

                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'E'
                    super(Statechart_1.RootState.X.B, self).__init__(**kwargs)

                def event_A(self, arg1=None, arg2=None):
                    self.event_A_invoked = True

                class E(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.B.E, self).__init__(**kwargs)

                    def event_B(self, arg1=None, arg2=None):
                        self.go_to_state('F')

                    def event_D(self, arg1=None, arg2=None):
                        self.go_to_state('Y')

                class F(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.B.F, self).__init__(**kwargs)

                    def event_C(self, arg1=None, arg2=None):
                        self.go_to_state('E')

        class Y(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.Y, self).__init__(**kwargs)

class StateEventHandlingBasicWithConcurrentTestCase(unittest.TestCase):
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

    # Send event event_A
    def test_send_event_a(self):
        monitor_1.reset()

        self.assertFalse(state_A.event_A_invoked)
        self.assertFalse(state_B.event_A_invoked)

        statechart_1.send_event('event_A')

        self.assertEqual(monitor_1.length, 0)

        self.assertTrue(statechart_1.state_is_current_state('C'))
        self.assertTrue(statechart_1.state_is_current_state('E'))

        self.assertTrue(state_A.event_A_invoked)
        self.assertTrue(state_B.event_A_invoked)

    # Send event event_B
    def test_send_event_b(self):
        monitor_1.reset()

        self.assertTrue(statechart_1.state_is_current_state('C'))
        self.assertTrue(statechart_1.state_is_current_state('E'))

        statechart_1.send_event('event_B')

        self.assertEqual(len(statechart_1.current_states), 2)
        print statechart_1.current_states
        self.assertTrue(statechart_1.state_is_current_state('D'))
        self.assertTrue(statechart_1.state_is_current_state('F'))

        self.assertEqual(monitor_1.length, 4)
        self.assertEqual(monitor_1.match_sequence().begin().begin_concurrent().begin_sequence().exited('C').entered('D').end_sequence().begin_sequence().exited('E').entered('F').end_sequence().end_concurrent().end(), True)

    # Send event event_B then event_C
    def test_send_event_b_then_c(self):
        statechart_1.send_event('event_B')

        self.assertTrue(statechart_1.state_is_current_state('D'))
        self.assertTrue(statechart_1.state_is_current_state('F'))

        monitor_1.reset()

        statechart_1.send_event('event_C')

        self.assertTrue(statechart_1.state_is_current_state('C'))
        self.assertTrue(statechart_1.state_is_current_state('E'))

        self.assertEqual(monitor_1.length, 4)
        self.assertEqual(monitor_1.match_sequence().begin().begin_concurrent().begin_sequence().exited('D').entered('C').end_sequence().begin_sequence().exited('F').entered('E').end_sequence().end_concurrent().end(), True)

    # Send event event_D
    def test_send_event_d(self):
        monitor_1.reset()

        self.assertTrue(statechart_1.state_is_current_state('C'))
        self.assertTrue(statechart_1.state_is_current_state('E'))

        statechart_1.send_event('event_D')

        self.assertEqual(monitor_1.length, 6)
        self.assertEqual(monitor_1.match_sequence().begin().begin_concurrent().begin_sequence().exited('C', 'A').end_sequence().begin_sequence().exited('E', 'B').end_sequence().end_concurrent().exited('X').entered('Y').end(), True)
                
        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertFalse(statechart_1.state_is_current_state('C'))
        self.assertFalse(statechart_1.state_is_current_state('E'))
        self.assertTrue(statechart_1.state_is_current_state('Y'))

    # Send event event_Z
    def test_send_event_z(self):
        monitor_1.reset()

        self.assertTrue(statechart_1.state_is_current_state('C'))
        self.assertTrue(statechart_1.state_is_current_state('E'))

        self.assertEqual(monitor_1.length, 0)

        statechart_1.send_event('event_Z')

        self.assertTrue(statechart_1.state_is_current_state('C'))
        self.assertTrue(statechart_1.state_is_current_state('E'))

    # Send event foo to statechart and ensure event is only handled once by state X
    def test_send_event_foo_and_check_handling_once_by_x(self):
        state_X = statechart_1.get_state('X')

        self.assertEqual(state_X.foo_invoked_count, 0)

        statechart_1.send_event('foo')

        self.assertEqual(state_X.foo_invoked_count, 1)


