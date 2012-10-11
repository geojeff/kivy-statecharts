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
        self.resume_go_to_state()
      
    def enter_state(self, context):
        print 'calling foo'
        return self.perform_async('foo')
      
    def exit_state(self, context):
        def func(self, arg1, arg2):
            self.foo(arg1, arg2)
        return self.perform_async(func)

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
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['substates_are_concurrent'] = True
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
        global root_state_1
        global monitor_1
        global state_A
        global state_B
        global state_C
        global state_D

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        state_C = statechart_1.get_state('C')
        state_D = statechart_1.get_state('D')

    # Go to state B
    def test_go_to_state_B(self):
        monitor_1.reset()

        self.assertFalse(statechart_1.go_to_state_active)
        self.assertFalse(statechart_1.go_to_state_suspended)

        self.assertTrue(state_A.is_current_state())
        self.assertFalse(state_B.is_current_state())
        self.assertFalse(state_C.is_current_state())
        self.assertFalse(state_D.is_current_state())

        state_A.go_to_state('B')

        self.assertFalse(statechart_1.go_to_state_active)
        self.assertFalse(statechart_1.go_to_state_suspended)

        self.assertEqual(monitor_1.match_sequence().begin().exited('A').entered('B').begin_concurrent().entered('C', 'D').end_concurrent().end(), True)

        self.assertEqual(len(statechart_1.current_states), 2)
        self.assertTrue(state_C.is_current_state())
        self.assertTrue(state_D.is_current_state())
        self.assertEqual(state_C.counter, 1)
        self.assertEqual(state_D.counter, 1)

    # Go to state B, then back to state A
    def test_go_to_state_B_then_back_to_A(self):
        monitor_1.reset()

        self.assertFalse(statechart_1.go_to_state_active)
        self.assertFalse(statechart_1.go_to_state_suspended)

        self.assertTrue(state_A.is_current_state())
        self.assertFalse(state_B.is_current_state())
        self.assertFalse(state_C.is_current_state())
        self.assertFalse(state_D.is_current_state())

        state_A.go_to_state('B')

        monitor_1.reset()

        state_C.go_to_state('A')

        self.assertFalse(statechart_1.go_to_state_active)
        self.assertFalse(statechart_1.go_to_state_suspended)

        self.assertEqual(monitor_1.match_sequence().begin().exited('C', 'D', 'B').entered('A').end(), True)

        self.assertEqual(len(statechart_1.current_states), 1)
        self.assertTrue(state_A.is_current_state())
        self.assertFalse(state_C.is_current_state())
        self.assertFalse(state_D.is_current_state())
        self.assertEqual(state_C.counter, 2)
        self.assertEqual(state_D.counter, 2)

