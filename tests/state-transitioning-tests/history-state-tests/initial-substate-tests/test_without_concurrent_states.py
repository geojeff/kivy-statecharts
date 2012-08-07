'''
Statechart tests, transitioning, history, initial substate, without concurrent
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.history_state import HistoryState
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['rootStateClass'] = self.RootState
        kwargs['monitorIsActive'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

            class InitialSubstate(HistoryState):
                def __init__(self, **kwargs):
                    kwargs['defaultState'] = 'C'
                    super(Statechart_1.RootState.A.InitialSubstate, self).__init__(**kwargs)

            class C(State):
                def __init__(self, **kwargs):
                    kwargs['initialSubstateKey'] = 'G'
                    super(Statechart_1.RootState.A.C, self).__init__(**kwargs)

                class G(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.C.G, self).__init__(**kwargs)

                class H(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.C.H, self).__init__(**kwargs)

            class D(State):
                def __init__(self, **kwargs):
                    kwargs['initialSubstateKey'] = 'I'
                    super(Statechart_1.RootState.A.D, self).__init__(**kwargs)

                class I(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.D.I, self).__init__(**kwargs)

                class J(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.D.J, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.B, self).__init__(**kwargs)
        
            class InitialSubstate(HistoryState):
                def __init__(self, **kwargs):
                    kwargs['isRecursive'] = True
                    kwargs['defaultState'] = 'E'
                    super(Statechart_1.RootState.B.InitialSubstate, self).__init__(**kwargs)

            class E(State):
                def __init__(self, **kwargs):
                    kwargs['initialSubstateKey'] = 'K'
                    super(Statechart_1.RootState.B.E, self).__init__(**kwargs)

                class K(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.B.E.K, self).__init__(**kwargs)

                class L(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.B.E.L, self).__init__(**kwargs)

            class F(State):
                def __init__(self, **kwargs):
                    kwargs['initialSubstateKey'] = 'M'
                    super(Statechart_1.RootState.B.F, self).__init__(**kwargs)

                class M(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.B.F.M, self).__init__(**kwargs)

                class N(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.B.F.N, self).__init__(**kwargs)

class StateTransitioningHistoryInitialSubstateWithoutConcurrentTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global rootState_1
        global monitor_1
        global state_A
        global state_B
        global state_C
        global state_D
        global state_E
        global state_F
        global state_G
        global state_H
        global state_I
        global state_J
        global state_K
        global state_L
        global state_M
        global state_N
        global initialSubstate_A
        global initialSubstate_B

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootStateInstance
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        state_C = statechart_1.getState('C')
        state_D = statechart_1.getState('D')
        state_E = statechart_1.getState('E')
        state_F = statechart_1.getState('F')
        state_G = statechart_1.getState('G')
        state_H = statechart_1.getState('H')
        state_I = statechart_1.getState('I')
        state_J = statechart_1.getState('J')
        state_K = statechart_1.getState('K')
        state_L = statechart_1.getState('L')
        state_M = statechart_1.getState('M')
        state_N = statechart_1.getState('N')
        initialSubstate_A = getattr(state_A, 'InitialSubstate')
        initialSubstate_B = getattr(state_B, 'InitialSubstate')

    # Check initial statechart after statechart init
    def test_initial_statechart_after_statechart_init(self):
        self.assertEqual(monitor_1.length, 4)
        self.assertTrue(monitor_1.matchSequence().begin().entered(rootState_1, state_A, state_C, state_G).end())
      
        self.assertEqual(rootState_1.initialSubstateKey, 'A')
        self.assertEqual(state_C.initialSubstateKey, 'G')
        self.assertEqual(state_D.initialSubstateKey, 'I')
        self.assertEqual(state_E.initialSubstateKey, 'K')
        self.assertEqual(state_F.initialSubstateKey, 'M')

        self.assertTrue(isinstance(initialSubstate_A, HistoryState))
        self.assertFalse(initialSubstate_A.isRecursive)
        self.assertEqual(initialSubstate_A.defaultState, 'C')
        self.assertEqual(initialSubstate_A.statechart, statechart_1)
        self.assertEqual(initialSubstate_A.parentState, state_A)
        self.assertEqual(initialSubstate_A.state(), state_C)

        self.assertTrue(isinstance(initialSubstate_B, HistoryState))
        self.assertTrue(initialSubstate_B.isRecursive)
        self.assertEqual(initialSubstate_B.defaultState, 'E')
        self.assertEqual(initialSubstate_B.statechart, statechart_1)
        self.assertEqual(initialSubstate_B.parentState, state_B)
        self.assertEqual(initialSubstate_B.state(), state_E)
  
        self.assertEqual(state_A.historyState, state_C)
        self.assertIsNone(state_B.historyState)
