'''
Statechart tests, find first relative current state, without concurrent state
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
        kwargs['initialStateKey'] = 'A'
        super(Statechart_1, self).__init__(**kwargs)

    class A(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'C'
            super(Statechart_1.A, self).__init__(**kwargs)

        class C(State):
            def __init__(self, **kwargs):
                super(Statechart_1.A.C, self).__init__(**kwargs)

        class D(State):
            def __init__(self, **kwargs):
                super(Statechart_1.A.D, self).__init__(**kwargs)

    class B(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'E'
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
        global rootState_1
        global state_A
        global state_B
        global state_C
        global state_D
        global state_E
        global state_F

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootState
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        state_C = statechart_1.getState('C')
        state_D = statechart_1.getState('D')
        state_E = statechart_1.getState('E')
        state_F = statechart_1.getState('F')

    # Check when current state is state C
    def test_check_when_current_state_is_state_c(self):
        self.assertEqual(rootState_1.findFirstRelativeCurrentState(), state_C)
        self.assertEqual(state_A.findFirstRelativeCurrentState(), state_C)
        self.assertEqual(state_B.findFirstRelativeCurrentState(), state_C)
        self.assertEqual(state_C.findFirstRelativeCurrentState(), state_C)
        self.assertEqual(state_D.findFirstRelativeCurrentState(), state_C)
        self.assertEqual(state_E.findFirstRelativeCurrentState(), state_C)
        self.assertEqual(state_F.findFirstRelativeCurrentState(), state_C)

    # Check when current state is state F
    def test_check_when_current_state_is_state_f(self):
        statechart_1.gotoState('F')
        self.assertEqual(rootState_1.findFirstRelativeCurrentState(), state_F)
        self.assertEqual(state_A.findFirstRelativeCurrentState(), state_F)
        self.assertEqual(state_B.findFirstRelativeCurrentState(), state_F)
        self.assertEqual(state_C.findFirstRelativeCurrentState(), state_F)
        self.assertEqual(state_D.findFirstRelativeCurrentState(), state_F)
        self.assertEqual(state_E.findFirstRelativeCurrentState(), state_F)
        self.assertEqual(state_F.findFirstRelativeCurrentState(), state_F)

