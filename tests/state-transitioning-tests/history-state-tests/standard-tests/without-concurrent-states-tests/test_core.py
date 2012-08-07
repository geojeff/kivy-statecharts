'''
Statechart tests, transitioning, history, standard, without concurrent, core
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
        kwargs['rootStateClass'] = self.RootState
        kwargs['monitorIsActive'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'C'
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

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
                kwargs['initialSubstateKey'] = 'E'
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

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

class StateTransitioningHistoryStandardCoreWithoutConcurrentTestCase(unittest.TestCase):
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

    # Check initial statechart history state objects
    def test_initial_statechart_history_state_objects(self):
        self.assertEqual(statechart_1.rootStateInstance.historyState, statechart_1.getState('A'))

        self.assertEqual(statechart_1.getState('A').historyState, statechart_1.getState('C'))
        self.assertEqual(statechart_1.getState('C').historyState, statechart_1.getState('G'))
        self.assertIsNone(statechart_1.getState('G').historyState)

        self.assertIsNone(statechart_1.getState('H').historyState)
        self.assertIsNone(statechart_1.getState('D').historyState)

        self.assertIsNone(statechart_1.getState('B').historyState)
        self.assertIsNone(statechart_1.getState('E').historyState)
        self.assertIsNone(statechart_1.getState('F').historyState)

    # Check go to state h and check history states
    def test_go_to_h_and_check_history_states(self):
        monitor_1.reset()

        statechart_1.gotoState('H')

        self.assertEqual(statechart_1.getState('A').historyState, statechart_1.getState('C'))
        self.assertEqual(statechart_1.getState('C').historyState, statechart_1.getState('H'))
        self.assertIsNone(statechart_1.getState('H').historyState)
        self.assertIsNone(statechart_1.getState('G').historyState)

        self.assertIsNone(statechart_1.getState('D').historyState)
        self.assertIsNone(statechart_1.getState('B').historyState)

    # Check go to state d and check history states
    def test_go_to_d_and_check_history_states(self):
        monitor_1.reset()

        statechart_1.gotoState('D')

        self.assertEqual(statechart_1.getState('A').historyState, statechart_1.getState('D'))
        self.assertEqual(statechart_1.getState('D').historyState, statechart_1.getState('I'))
        self.assertEqual(statechart_1.getState('C').historyState, statechart_1.getState('G'))
        self.assertIsNone(statechart_1.getState('H').historyState)
        self.assertIsNone(statechart_1.getState('G').historyState)
        self.assertIsNone(statechart_1.getState('I').historyState)
        self.assertIsNone(statechart_1.getState('J').historyState)

        self.assertIsNone(statechart_1.getState('B').historyState)

    # Check go to state b and check history states
    def test_go_to_b_and_check_history_states(self):
        monitor_1.reset()

        statechart_1.gotoState('B')
        self.assertTrue(monitor_1.matchSequence().begin().exited('G', 'C', 'A').entered('B', 'E', 'K').end())

        self.assertEqual(statechart_1.rootStateInstance.historyState, statechart_1.getState('B'))
        self.assertEqual(statechart_1.getState('B').historyState, statechart_1.getState('E'))
        self.assertEqual(statechart_1.getState('E').historyState, statechart_1.getState('K'))
        self.assertEqual(statechart_1.getState('A').historyState, statechart_1.getState('C'))
        self.assertEqual(statechart_1.getState('C').historyState, statechart_1.getState('G'))


    # Check go to state j, then state m, then go to state a's history state (non-recursive)
    def test_to_j_then_to_m_then_to_state_a_history_state_non_recursive(self):
        statechart_1.gotoState('J')
        statechart_1.gotoState('M')

        monitor_1.reset()
        statechart_1.gotoHistoryState('A')
  
        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.matchSequence().begin().exited('M', 'F', 'B').entered('A', 'D', 'I').end())
        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('I'))
        self.assertEqual(statechart_1.rootStateInstance.historyState, statechart_1.getState('A'))
        self.assertEqual(statechart_1.getState('A').historyState, statechart_1.getState('D'))
        self.assertEqual(statechart_1.getState('D').historyState, statechart_1.getState('I'))

# [PORT] Failure on J

#    # Check go to state j, then state m, then go to state a's history state (recursive)
#    def test_to_j_then_to_m_then_to_state_a_history_state_recursive(self):
#        statechart_1.gotoState('J')
#        statechart_1.gotoState('M')
#
#        monitor_1.reset()
#        statechart_1.gotoHistoryState('A', fromCurrentState=None, recursive=True)
#  
#        self.assertEqual(monitor_1.length, 6)
#        self.assertTrue(monitor_1.matchSequence().begin().exited('M', 'F', 'B').entered('A', 'D', 'J').end())
#        self.assertEqual(len(statechart_1.currentStates), 1)
#        self.assertTrue(statechart_1.stateIsCurrentState('J'))
#        self.assertEqual(statechart_1.rootStateInstance.historyState, statechart_1.getState('A'))
#        self.assertEqual(statechart_1.getState('A').historyState, statechart_1.getState('D'))
#        self.assertEqual(statechart_1.getState('D').historyState, statechart_1.getState('I'))

    # Check go to state b's history state (non-recursive)
    def test_go_to_state_b_history_state_non_recursive(self):
        monitor_1.reset()

        statechart_1.gotoHistoryState('B')
  
        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.matchSequence().begin().exited('G', 'C', 'A').entered('B', 'E', 'K').end())
        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('K'))
        self.assertEqual(statechart_1.rootStateInstance.historyState, statechart_1.getState('B'))
        self.assertEqual(statechart_1.getState('B').historyState, statechart_1.getState('E'))
        self.assertEqual(statechart_1.getState('E').historyState, statechart_1.getState('K'))


    # Check go to state b's history state (recursive)
    def test_go_to_state_b_history_state_recursive(self):
        monitor_1.reset()

        statechart_1.gotoHistoryState('B', fromCurrentState=None, recursive=True)
  
        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.matchSequence().begin().exited('G', 'C', 'A').entered('B', 'E', 'K').end())
        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('K'))
        self.assertEqual(statechart_1.rootStateInstance.historyState, statechart_1.getState('B'))
        self.assertEqual(statechart_1.getState('B').historyState, statechart_1.getState('E'))
        self.assertEqual(statechart_1.getState('E').historyState, statechart_1.getState('K'))

