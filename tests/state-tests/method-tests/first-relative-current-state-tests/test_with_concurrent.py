'''
Statechart tests, find first relative current state, with concurrent state
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
        kwargs['initialStateKey'] = 'FOO'
        super(Statechart_1, self).__init__(**kwargs)

    class FOO(State):
        def __init__(self, **kwargs):
            kwargs['substatesAreConcurrent'] = True
            super(Statechart_1.FOO, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'A1'
                super(Statechart_1.FOO.A, self).__init__(**kwargs)

            class A1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.A.A1, self).__init__(**kwargs)
    
            class A2(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.A.A2, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'B1'
                super(Statechart_1.FOO.B, self).__init__(**kwargs)

            class B1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.B.B1, self).__init__(**kwargs)
    
            class B2(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.B.B2, self).__init__(**kwargs)

    class BAR(State):
        def __init__(self, **kwargs):
            kwargs['substatesAreConcurrent'] = True
            super(Statechart_1.BAR, self).__init__(**kwargs)

        class X(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'X1'
                super(Statechart_1.BAR.X, self).__init__(**kwargs)

            class X1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.X.X1, self).__init__(**kwargs)
    
            class X2(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.X.X2, self).__init__(**kwargs)

        class Y(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'Y1'
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
        global rootState_1
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
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootStateInstance
        state_FOO = statechart_1.getState('FOO')
        state_BAR = statechart_1.getState('BAR')
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        state_X = statechart_1.getState('X')
        state_Y = statechart_1.getState('Y')
        state_A1 = statechart_1.getState('A1')
        state_A2 = statechart_1.getState('A2')
        state_B1 = statechart_1.getState('B1')
        state_B2 = statechart_1.getState('B2')
        state_X1 = statechart_1.getState('X1')
        state_X2 = statechart_1.getState('X2')
        state_Y1 = statechart_1.getState('Y1')
        state_Y2 = statechart_1.getState('Y2')
        
    # Check using state A1 with state foo entered
    def test_check_using_state_a1_with_state_foo_entered(self):
        self.assertEqual(state_A1.findFirstRelativeCurrentState(), state_A1)

    # Check using state A2 with state foo entered
    def test_check_using_state_a2_with_state_foo_entered(self):
        self.assertEqual(state_A2.findFirstRelativeCurrentState(), state_A1)

    # Check using state A with state foo entered
    def test_check_using_state_a_with_state_foo_entered(self):
        self.assertEqual(state_A.findFirstRelativeCurrentState(), state_A1)

    # Check using state foo with state foo entered
    def test_check_using_state_foo_with_state_foo_entered(self):
        self.assertTrue(state_FOO.isEnteredState)
        self.assertTrue(state_A.isEnteredState)
        self.assertTrue(state_B.isEnteredState)
        self.assertTrue(state_A1.isCurrentState)
        self.assertTrue(state_B1.isCurrentState)

        result = state_FOO.findFirstRelativeCurrentState()
        self.assertTrue(result in [state_A1, state_B1])

        self.assertEqual(state_FOO.findFirstRelativeCurrentState(state_A), state_A1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState('A'), state_A1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState(state_A1), state_A1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState('A1'), state_A1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState('A.A1'), state_A1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState(state_A2), state_A1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState('A2'), state_A1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState('A.A2'), state_A1)

        self.assertEqual(state_FOO.findFirstRelativeCurrentState(state_B), state_B1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState('B'), state_B1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState(state_B1), state_B1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState('B1'), state_B1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState('B.B1'), state_B1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState(state_B2), state_B1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState('B2'), state_B1)
        self.assertEqual(state_FOO.findFirstRelativeCurrentState('B.B2'), state_B1)

    # Check using root state with state foo entered
    def test_check_using_root_state_with_state_foo_entered(self):
        result = rootState_1.findFirstRelativeCurrentState()
        self.assertTrue(result in [state_A1, state_B1])

        result = rootState_1.findFirstRelativeCurrentState(state_FOO)
        self.assertTrue(result in [state_A1, state_B1])

        result = rootState_1.findFirstRelativeCurrentState(state_BAR)
        self.assertTrue(result in [state_A1, state_B1])

        self.assertEqual(rootState_1.findFirstRelativeCurrentState(state_A), state_A1)
        self.assertEqual(rootState_1.findFirstRelativeCurrentState('A'), state_A1)
        self.assertEqual(rootState_1.findFirstRelativeCurrentState('FOO.A'), state_A1)

        self.assertEqual(rootState_1.findFirstRelativeCurrentState(state_B), state_B1)
        self.assertEqual(rootState_1.findFirstRelativeCurrentState('B'), state_B1)
        self.assertEqual(rootState_1.findFirstRelativeCurrentState('FOO.B'), state_B1)

        result = rootState_1.findFirstRelativeCurrentState(state_X)
        self.assertTrue(result in [state_A1, state_B1])

        result = rootState_1.findFirstRelativeCurrentState(state_Y)
        self.assertTrue(result in [state_A1, state_B1])

    # Check using root state with state bar entered
    def test_check_using_root_state_with_state_bar_entered(self):
        statechart_1.gotoState('BAR')

        result = rootState_1.findFirstRelativeCurrentState()
        self.assertTrue(result in [state_X1, state_Y1])

        result = rootState_1.findFirstRelativeCurrentState(state_FOO)
        self.assertTrue(result in [state_X1, state_Y1])

        result = rootState_1.findFirstRelativeCurrentState(state_BAR)
        self.assertTrue(result in [state_X1, state_Y1])

        self.assertEqual(rootState_1.findFirstRelativeCurrentState(state_X), state_X1)
        self.assertEqual(rootState_1.findFirstRelativeCurrentState('X'), state_X1)
        self.assertEqual(rootState_1.findFirstRelativeCurrentState('BAR.X'), state_X1)

        self.assertEqual(rootState_1.findFirstRelativeCurrentState(state_Y), state_Y1)
        self.assertEqual(rootState_1.findFirstRelativeCurrentState('Y'), state_Y1)
        self.assertEqual(rootState_1.findFirstRelativeCurrentState('BAR.Y'), state_Y1)

        result = rootState_1.findFirstRelativeCurrentState(state_A)
        self.assertTrue(result in [state_X1, state_Y1])

        result = rootState_1.findFirstRelativeCurrentState(state_B)
        self.assertTrue(result in [state_X1, state_Y1])

