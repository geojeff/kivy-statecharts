'''
Statechart tests, find first relative current state, with concurrent state
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
        kwargs['initial_state_key'] = 'FOO'
        super(Statechart_1, self).__init__(**kwargs)

    class FOO(State):
        def __init__(self, **kwargs):
            kwargs['substates_are_concurrent'] = True
            super(Statechart_1.FOO, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'A1'
                super(Statechart_1.FOO.A, self).__init__(**kwargs)

            class A1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.A.A1, self).__init__(**kwargs)
    
            class A2(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.A.A2, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'B1'
                super(Statechart_1.FOO.B, self).__init__(**kwargs)

            class B1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.B.B1, self).__init__(**kwargs)
    
            class B2(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.B.B2, self).__init__(**kwargs)

    class BAR(State):
        def __init__(self, **kwargs):
            kwargs['substates_are_concurrent'] = True
            super(Statechart_1.BAR, self).__init__(**kwargs)

        class X(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'X1'
                super(Statechart_1.BAR.X, self).__init__(**kwargs)

            class X1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.X.X1, self).__init__(**kwargs)
    
            class X2(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.X.X2, self).__init__(**kwargs)

        class Y(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'Y1'
                super(Statechart_1.BAR.Y, self).__init__(**kwargs)

            class Y1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.Y.Y1, self).__init__(**kwargs)
    
            class Y2(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.Y.Y2, self).__init__(**kwargs)

class StateGetSubstateTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global root_state_1
        global state_FOO
        global state_BAR
        global state_A
        global state_B
        global state_X
        global state_Y
        global state_A1
        global state_A2
        global state_B1
        global state_B2
        global state_X1
        global state_X2
        global state_Y1
        global state_Y2

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        state_FOO = statechart_1.get_state('FOO')
        state_BAR = statechart_1.get_state('BAR')
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        state_X = statechart_1.get_state('X')
        state_Y = statechart_1.get_state('Y')
        state_A1 = statechart_1.get_state('A1')
        state_A2 = statechart_1.get_state('A2')
        state_B1 = statechart_1.get_state('B1')
        state_B2 = statechart_1.get_state('B2')
        state_X1 = statechart_1.get_state('X1')
        state_X2 = statechart_1.get_state('X2')
        state_Y1 = statechart_1.get_state('Y1')
        state_Y2 = statechart_1.get_state('Y2')
        
    # Check using state A1 with state foo entered
    def test_check_using_state_a1_with_state_foo_entered(self):
        self.assertEqual(state_A1.find_first_relative_current_state(), state_A1)

    # Check using state A2 with state foo entered
    def test_check_using_state_a2_with_state_foo_entered(self):
        self.assertEqual(state_A2.find_first_relative_current_state(), state_A1)

    # Check using state A with state foo entered
    def test_check_using_state_a_with_state_foo_entered(self):
        self.assertEqual(state_A.find_first_relative_current_state(), state_A1)

    # Check using state foo with state foo entered
    def test_check_using_state_foo_with_state_foo_entered(self):
        self.assertTrue(state_FOO.is_entered_state)
        self.assertTrue(state_A.is_entered_state)
        self.assertTrue(state_B.is_entered_state)
        self.assertTrue(state_A1.is_current_state)
        self.assertTrue(state_B1.is_current_state)

        result = state_FOO.find_first_relative_current_state()
        self.assertTrue(result in [state_A1, state_B1])

        self.assertEqual(state_FOO.find_first_relative_current_state(state_A), state_A1)
        self.assertEqual(state_FOO.find_first_relative_current_state('A'), state_A1)
        self.assertEqual(state_FOO.find_first_relative_current_state(state_A1), state_A1)
        self.assertEqual(state_FOO.find_first_relative_current_state('A1'), state_A1)
        self.assertEqual(state_FOO.find_first_relative_current_state('A.A1'), state_A1)
        self.assertEqual(state_FOO.find_first_relative_current_state(state_A2), state_A1)
        self.assertEqual(state_FOO.find_first_relative_current_state('A2'), state_A1)
        self.assertEqual(state_FOO.find_first_relative_current_state('A.A2'), state_A1)

        self.assertEqual(state_FOO.find_first_relative_current_state(state_B), state_B1)
        self.assertEqual(state_FOO.find_first_relative_current_state('B'), state_B1)
        self.assertEqual(state_FOO.find_first_relative_current_state(state_B1), state_B1)
        self.assertEqual(state_FOO.find_first_relative_current_state('B1'), state_B1)
        self.assertEqual(state_FOO.find_first_relative_current_state('B.B1'), state_B1)
        self.assertEqual(state_FOO.find_first_relative_current_state(state_B2), state_B1)
        self.assertEqual(state_FOO.find_first_relative_current_state('B2'), state_B1)
        self.assertEqual(state_FOO.find_first_relative_current_state('B.B2'), state_B1)

    # Check using root state with state foo entered
    def test_check_using_root_state_with_state_foo_entered(self):
        result = root_state_1.find_first_relative_current_state()
        self.assertTrue(result in [state_A1, state_B1])

        result = root_state_1.find_first_relative_current_state(state_FOO)
        self.assertTrue(result in [state_A1, state_B1])

        result = root_state_1.find_first_relative_current_state(state_BAR)
        self.assertTrue(result in [state_A1, state_B1])

        self.assertEqual(root_state_1.find_first_relative_current_state(state_A), state_A1)
        self.assertEqual(root_state_1.find_first_relative_current_state('A'), state_A1)
        self.assertEqual(root_state_1.find_first_relative_current_state('FOO.A'), state_A1)

        self.assertEqual(root_state_1.find_first_relative_current_state(state_B), state_B1)
        self.assertEqual(root_state_1.find_first_relative_current_state('B'), state_B1)
        self.assertEqual(root_state_1.find_first_relative_current_state('FOO.B'), state_B1)

        result = root_state_1.find_first_relative_current_state(state_X)
        self.assertTrue(result in [state_A1, state_B1])

        result = root_state_1.find_first_relative_current_state(state_Y)
        self.assertTrue(result in [state_A1, state_B1])

    # Check using root state with state bar entered
    def test_check_using_root_state_with_state_bar_entered(self):
        statechart_1.go_to_state('BAR')

        result = root_state_1.find_first_relative_current_state()
        self.assertTrue(result in [state_X1, state_Y1])

        result = root_state_1.find_first_relative_current_state(state_FOO)
        self.assertTrue(result in [state_X1, state_Y1])

        result = root_state_1.find_first_relative_current_state(state_BAR)
        self.assertTrue(result in [state_X1, state_Y1])

        self.assertEqual(root_state_1.find_first_relative_current_state(state_X), state_X1)
        self.assertEqual(root_state_1.find_first_relative_current_state('X'), state_X1)
        self.assertEqual(root_state_1.find_first_relative_current_state('BAR.X'), state_X1)

        self.assertEqual(root_state_1.find_first_relative_current_state(state_Y), state_Y1)
        self.assertEqual(root_state_1.find_first_relative_current_state('Y'), state_Y1)
        self.assertEqual(root_state_1.find_first_relative_current_state('BAR.Y'), state_Y1)

        result = root_state_1.find_first_relative_current_state(state_A)
        self.assertTrue(result in [state_X1, state_Y1])

        result = root_state_1.find_first_relative_current_state(state_B)
        self.assertTrue(result in [state_X1, state_Y1])

