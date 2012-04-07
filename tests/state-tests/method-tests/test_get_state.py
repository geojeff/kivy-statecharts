'''
Statechart tests, get state
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['rootState'] = self.RootState
        kwargs['trace'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'X'
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
                kwargs['initialSubstateKey'] = 'X'
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
                kwargs['initialSubstateKey'] = 'X'
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
        global rootState_1
        global monitor_1
        global state_A
        global state_B
        global state_C

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootState
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        state_C = statechart_1.getState('C')
        
    # Get existing, umambiguous states from state Z
    def test_get_existing_unambiguous_states_from_state_z(self):
        z = statechart_1.getState('Z')

        state = z.getState('Z')
        self.assertEqual(z, state)

        state = z.getState(z)
        self.assertEqual(z, state)

        state = z.getState('A')
        self.assertEqual(state.fullPath, 'A')
        self.assertEqual(z.getState(state).fullPath, 'A')

        state = z.getState('B')
        self.assertEqual(state.fullPath, 'B')

        state = z.getState('C')
        self.assertEqual(state.fullPath, 'C')

        state = z.getState('FOO')
        self.assertEqual(state.fullPath, 'A.FOO')

        state = z.getState('A.FOO')
        self.assertEqual(state.fullPath, 'A.FOO')

        state = z.getState('BAR')
        self.assertEqual(state.fullPath, 'B.BAR')

        state = z.getState('B.BAR')
        self.assertEqual(state.fullPath, 'B.BAR')

        state = z.getState('A.X')
        self.assertEqual(state.fullPath, 'A.X')

        state = z.getState('A.Y')
        self.assertEqual(state.fullPath, 'A.Y')

        state = z.getState('B.X')
        self.assertEqual(state.fullPath, 'B.X')

        state = z.getState('B.Y')
        self.assertEqual(state.fullPath, 'B.Y')

        state = z.getState('C.X')
        self.assertEqual(state.fullPath, 'C.X')

    # Get state x from sibling states
    def test_get_state_x_from_sibling_states(self):
        foo = rootState_1.getState('A.FOO')
        bar = rootState_1.getState('B.BAR')
        z = rootState_1.getState('C.Z')

        state = foo.getState('X')
        self.assertEqual(state.fullPath, 'A.X')

        state = bar.getState('X')
        self.assertEqual(state.fullPath, 'B.X')

        state = z.getState('X')
        self.assertEqual(state.fullPath, 'C.X')

    # Get state x from state a
    def test_get_state_from_state_a(self):
        a = rootState_1.getState('A')

        state = a.getState('X')
        self.assertEqual(state.fullPath, 'A.X')

    # Get state x from state a
    def test_attempt_to_get_state_y_from_state_z(self):
        z = rootState_1.getState('C.Z')

        print 'expecting to get an error...'
        state = z.getState('Y')
        self.assertIsNone(state)


