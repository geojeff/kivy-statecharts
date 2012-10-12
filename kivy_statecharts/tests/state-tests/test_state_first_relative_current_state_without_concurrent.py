'''
Statechart tests, find first relative current state, without concurrent state
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['initial_state_key'] = 'A'
        super(Statechart_1, self).__init__(**kwargs)

    class A(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'C'
            super(Statechart_1.A, self).__init__(**kwargs)

        class C(State):
            def __init__(self, **kwargs):
                super(Statechart_1.A.C, self).__init__(**kwargs)

        class D(State):
            def __init__(self, **kwargs):
                super(Statechart_1.A.D, self).__init__(**kwargs)

    class B(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'E'
            super(Statechart_1.B, self).__init__(**kwargs)

        class E(State):
            def __init__(self, **kwargs):
                super(Statechart_1.B.E, self).__init__(**kwargs)

        class F(State):
            def __init__(self, **kwargs):
                super(Statechart_1.B.F, self).__init__(**kwargs)

class StateFirstRelativeCurrentStateWithoutConcurrentTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global root_state_1
        global state_A
        global state_B
        global state_C
        global state_D
        global state_E
        global state_F

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        state_C = statechart_1.get_state('C')
        state_D = statechart_1.get_state('D')
        state_E = statechart_1.get_state('E')
        state_F = statechart_1.get_state('F')

    # Check when current state is state C
    def test_check_when_current_state_is_state_c(self):
        self.assertEqual(root_state_1.find_first_relative_current_state(), state_C)
        self.assertEqual(state_A.find_first_relative_current_state(), state_C)
        self.assertEqual(state_B.find_first_relative_current_state(), state_C)
        self.assertEqual(state_C.find_first_relative_current_state(), state_C)
        self.assertEqual(state_D.find_first_relative_current_state(), state_C)
        self.assertEqual(state_E.find_first_relative_current_state(), state_C)
        self.assertEqual(state_F.find_first_relative_current_state(), state_C)

    # Check when current state is state F
    def test_check_when_current_state_is_state_f(self):
        statechart_1.go_to_state('F')
        self.assertEqual(root_state_1.find_first_relative_current_state(), state_F)
        self.assertEqual(state_A.find_first_relative_current_state(), state_F)
        self.assertEqual(state_B.find_first_relative_current_state(), state_F)
        self.assertEqual(state_C.find_first_relative_current_state(), state_F)
        self.assertEqual(state_D.find_first_relative_current_state(), state_F)
        self.assertEqual(state_E.find_first_relative_current_state(), state_F)
        self.assertEqual(state_F.find_first_relative_current_state(), state_F)

