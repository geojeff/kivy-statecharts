'''
Statechart tests, basic event handling, without concurrent states
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
        kwargs['trace'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'C'
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

            def event_B(self, arg1=None, arg2=None):
                self.go_to_state('B')

            class C(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.C, self).__init__(**kwargs)

                def event_A(self, arg1=None, arg2=None):
                    self.go_to_state('D')

            class D(State):
                sender = ObjectProperty(None)
                context = ObjectProperty(None)

                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.D, self).__init__(**kwargs)

                def event_C(self, sender=None, context=None):
                    self.sender = sender
                    self.context = context
                    self.go_to_state('F')

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

class StateEventHandlingBasicWithoutConcurrentTestCase(unittest.TestCase):
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

    # Send event event_A while in state C
    def test_send_event_a_while_in_state_c(self):
        monitor_1.reset()

        statechart_1.send_event('event_A')

        self.assertEqual(monitor_1.length, 2)
        self.assertTrue(monitor_1.match_sequence().begin().exited('C').entered('D').end())
        self.assertTrue(statechart_1.state_is_current_state('D'))

    # Send event event_B while in parent state A
    def test_send_event_b_while_in_parent_state_a(self):
        monitor_1.reset()

        statechart_1.send_event('event_B')

        self.assertEqual(monitor_1.length, 4)
        self.assertTrue(monitor_1.match_sequence().begin().exited('C', 'A').entered('B', 'E').end())
        self.assertTrue(statechart_1.state_is_current_state('E'))

    # Send event event_C while in state D
    def test_send_event_c_while_in_state_d(self):
        statechart_1.go_to_state('D')

        monitor_1.reset()

        statechart_1.send_event('event_C', statechart_1, 'foobar')

        self.assertEqual(monitor_1.length, 4)
        self.assertTrue(monitor_1.match_sequence().begin().exited('D', 'A').entered('B', 'F').end())
        self.assertTrue(statechart_1.state_is_current_state('F'))
        self.assertEqual(state_D.sender, statechart_1)
        self.assertEqual(state_D.context, 'foobar')

    # Send event event_C while in state C
    def test_send_event_c_while_in_state_c(self):
        monitor_1.reset()

        statechart_1.send_event('event_C')

        self.assertEqual(monitor_1.length, 0)
        self.assertTrue(statechart_1.state_is_current_state('C'))

    # Send event event_D while in state C
    def test_send_event_d_while_in_state_c(self):
        monitor_1.reset()

        statechart_1.send_event('event_D')

        self.assertEqual(monitor_1.length, 0)
        self.assertTrue(statechart_1.state_is_current_state('C'))


