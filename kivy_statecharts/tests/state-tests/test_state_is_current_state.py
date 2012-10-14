'''
Statechart tests, is current state
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.empty_state import EmptyState
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['monitor_is_active'] = True
        kwargs['root_state_class'] = self.RootState
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
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

class StateIsCurrentStateTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global root_state_1
        global monitor_1
        global state_A
        global state_B

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        
    # check binding to is_current_state"
    def test_check_binding_to_is_current_state_statechart_1(self):
        class o(object):
            def __init__(self):
                self.value = None
                # [PORT] Won't work in kivy. Plus, is_current_state() is now a method.
                #self.bind(value, state_A.is_current_state) 

        self.assertEqual(root_state_1.initial_substate_key, state_A.name)

    # check if state is current substate of another?
    def test_if_state_is_current_substate(self):
        self.assertTrue(root_state_1.state_is_current_substate(state_A))
        self.assertFalse(state_B.state_is_current_substate(state_A))
