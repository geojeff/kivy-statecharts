'''
Statechart tests, get state
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
        kwargs['root_state_class'] = self.RootState
        kwargs['trace'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'X'
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

            class X(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.X, self).__init__(**kwargs)

            class Y(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.Y, self).__init__(**kwargs)

            class FOO(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.FOO, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'X'
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

            class X(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.X, self).__init__(**kwargs)

            class Y(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.Y, self).__init__(**kwargs)

            class BAR(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.BAR, self).__init__(**kwargs)

        class C(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'X'
                super(Statechart_1.RootState.C, self).__init__(**kwargs)

            class X(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.C.X, self).__init__(**kwargs)

            class Z(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.C.Z, self).__init__(**kwargs)

class StateGetStateTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global root_state_1
        global monitor_1
        global state_A
        global state_B
        global state_C

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        state_C = statechart_1.get_state('C')
        
    # Get existing, umambiguous states from state Z
    def test_get_existing_unambiguous_states_from_state_z(self):
        z = statechart_1.get_state('Z')

        state = z.get_state('Z')
        self.assertEqual(z, state)

        state = z.get_state(z)
        self.assertEqual(z, state)

        state = z.get_state('A')
        self.assertEqual(state.full_path, 'A')
        self.assertEqual(z.get_state(state).full_path, 'A')

        state = z.get_state('B')
        self.assertEqual(state.full_path, 'B')

        state = z.get_state('C')
        self.assertEqual(state.full_path, 'C')

        state = z.get_state('FOO')
        self.assertEqual(state.full_path, 'A.FOO')

        state = z.get_state('A.FOO')
        self.assertEqual(state.full_path, 'A.FOO')

        state = z.get_state('BAR')
        self.assertEqual(state.full_path, 'B.BAR')

        state = z.get_state('B.BAR')
        self.assertEqual(state.full_path, 'B.BAR')

        state = z.get_state('A.X')
        self.assertEqual(state.full_path, 'A.X')

        state = z.get_state('A.Y')
        self.assertEqual(state.full_path, 'A.Y')

        state = z.get_state('B.X')
        self.assertEqual(state.full_path, 'B.X')

        state = z.get_state('B.Y')
        self.assertEqual(state.full_path, 'B.Y')

        state = z.get_state('C.X')
        self.assertEqual(state.full_path, 'C.X')

    # Get state x from sibling states
    def test_get_state_x_from_sibling_states(self):
        foo = root_state_1.get_state('A.FOO')
        bar = root_state_1.get_state('B.BAR')
        z = root_state_1.get_state('C.Z')

        state = foo.get_state('X')
        self.assertEqual(state.full_path, 'A.X')

        state = bar.get_state('X')
        self.assertEqual(state.full_path, 'B.X')

        state = z.get_state('X')
        self.assertEqual(state.full_path, 'C.X')

    # Get state x from state a
    def test_get_state_from_state_a(self):
        a = root_state_1.get_state('A')

        state = a.get_state('X')
        self.assertEqual(state.full_path, 'A.X')

    # Get state x from state a
    def test_attempt_to_get_state_y_from_state_z(self):
        z = root_state_1.get_state('C.Z')

        print 'expecting to get an error...'
        state = z.get_state('Y')
        self.assertIsNone(state)


