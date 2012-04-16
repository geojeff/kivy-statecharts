'''
Statechart tests, transitioning, standard, without concurrent, core
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import StatechartManager

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

class StateTransitioningStandardCoreWithoutConcurrentTestCase(unittest.TestCase):
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

    # Check statechart state objects
    def test_statechart_state_objects(self):
        self.assertIsNotNone(state_G)
        self.assertEqual(state_G.name, 'G')
        self.assertTrue(state_G.isCurrentState())
        self.assertTrue(state_G.stateIsCurrentSubstate('G'))
        self.assertTrue(statechart_1.stateIsCurrentState('G'))
        self.assertTrue(statechart_1.stateIsCurrentState(state_G))
  
        self.assertIsNotNone(state_M)
        self.assertEqual(state_M.name, 'M')
        self.assertFalse(state_M.isCurrentState())
        self.assertFalse(state_G.stateIsCurrentSubstate('M'))
        self.assertFalse(statechart_1.stateIsCurrentState('M'))
        self.assertFalse(statechart_1.stateIsCurrentState(state_M))
  
        self.assertIsNotNone(state_A)
        self.assertFalse(state_A.isCurrentState())
        self.assertFalse(state_A.stateIsCurrentSubstate('A'))
        self.assertFalse(state_A.stateIsCurrentSubstate('C'))
        self.assertTrue(state_A.stateIsCurrentSubstate('G'))
        self.assertTrue(state_A.stateIsCurrentSubstate(state_G))
        self.assertFalse(state_A.stateIsCurrentSubstate(state_M))
 
        state_X = statechart_1.getState('X')
        self.assertIsNone(state_X)

    # Check statechart initialization
    def test_statechart_initialization(self):
        self.assertEqual(monitor_1.length, 4)

        self.assertTrue(monitor_1.matchSequence().begin().entered(rootState_1, 'A', 'C', 'G').end())
  
        self.assertEqual(len(statechart_1.currentStates), 1)
  
        self.assertTrue(statechart_1.stateIsCurrentState('G'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'A', 'C', 'G'))

    # Check go to state h
    def test_go_to_state_h(self):
        monitor_1.reset()
        statechart_1.gotoState('H')
  
        self.assertEqual(monitor_1.length, 2)
        self.assertTrue(monitor_1.matchSequence().begin().exited('G').entered('H').end())
        self.assertFalse(monitor_1.matchSequence().begin().exited('H').entered('G').end())
  
        self.assertEqual(len(statechart_1.currentStates), 1)
  
        self.assertTrue(statechart_1.stateIsCurrentState('H'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'A', 'C', 'H'))

    # Check go to states h and d
    def test_go_to_states_h_and_d(self):
        statechart_1.gotoState('H')

        monitor_1.reset()
        statechart_1.gotoState('D')
  
        self.assertEqual(monitor_1.length, 4)

        self.assertTrue(monitor_1.matchSequence().begin().exited('H', 'C').entered('D', 'I').end())
        self.assertFalse(monitor_1.matchSequence().begin().exited('H', 'C').entered('D', 'F').end())
        self.assertFalse(monitor_1.matchSequence().begin().exited('G', 'C').entered('D', 'I').end())

        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('I'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'A', 'D', 'I'))

    # Check go to states h, d, and h
    def test_go_to_states_h_d_and_h(self):
        statechart_1.gotoState('H')
        statechart_1.gotoState('D')

        monitor_1.reset()
        statechart_1.gotoState('H')
  
        self.assertEqual(monitor_1.length, 4)
  
        self.assertTrue(monitor_1.matchSequence().begin().exited('I', 'D').entered('C', 'H').end())

        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('H'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'A', 'C', 'H'))

    # Check go to state b
    def test_go_to_state_b(self):
        monitor_1.reset()
        statechart_1.gotoState('B')

        self.assertEqual(monitor_1.length, 6)

        self.assertTrue(monitor_1.matchSequence().begin().exited('G', 'C', 'A').entered('B', 'E', 'K').end())
        self.assertFalse(monitor_1.matchSequence().begin().exited('G', 'A', 'C').entered('B', 'E', 'K').end())
        self.assertFalse(monitor_1.matchSequence().begin().exited('G', 'C', 'A').entered('B', 'K', 'E').end())

        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('K'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'B', 'E', 'K'))

    # Check go to state f
    def test_go_to_state_f(self):
        monitor_1.reset()
        statechart_1.gotoState('F')

        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.matchSequence().begin().exited('G', 'C', 'A').entered('B', 'F', 'M').end())

        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('M'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'B', 'F', 'M'))

    # Check go to state n
    def test_go_to_state_n(self):
        monitor_1.reset()
        statechart_1.gotoState('N')

        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.matchSequence().begin().exited('G', 'C', 'A').entered('B', 'F', 'N').end())

        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('N'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'B', 'F', 'N'))

    # Check re-enter state G
    def test_reenter_state_g(self):
        monitor_1.reset()
        statechart_1.gotoState('G')

        self.assertEqual(monitor_1.length, 2)

        self.assertTrue(monitor_1.matchSequence().begin().exited('G').entered('G').end())

        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('G'))
  
        monitor_1.reset()
  
        self.assertEqual(monitor_1.length, 0)
  
        state = statechart_1.getState('G')
        state.reenter()
  
        self.assertEqual(monitor_1.length, 2)
        self.assertTrue(monitor_1.matchSequence().begin().exited('G').entered('G').end())
        
        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('G'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'A', 'C', 'G'))

    # Check go to g state's ancestor state a
    def test_go_to_g_state_ancestor_state_a(self):
        monitor_1.reset()
        statechart_1.gotoState('A')

        self.assertEqual(monitor_1.length, 6)

        self.assertTrue(monitor_1.matchSequence().begin().exited('G', 'C', 'A').entered('A', 'C', 'G').end())
        
        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('G'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'A', 'C', 'G'))


    # Check go to state b and then go to root state
    def test_go_to_state_b_then_to_root_state(self):
        statechart_1.gotoState('B')
        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('K'))
  
        monitor_1.reset()
        statechart_1.gotoState(statechart_1.rootStateInstance)
  
        root = statechart_1.rootStateInstance

        self.assertEqual(monitor_1.length, 8)
        self.assertTrue(monitor_1.matchSequence().begin().exited('K', 'E', 'B', root).entered(root, 'A', 'C', 'G').end())
        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('G'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(root, 'A', 'C', 'G'))

    # Check from state g, go to state m calling state g's gotoState
    def test_from_g_to_m_calling_state_g_gotoState(self):
        self.assertTrue(state_G.isCurrentState())
        self.assertFalse(state_M.isCurrentState())
  
        monitor_1.reset()
        state_G.gotoState('M')
  
        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.matchSequence().begin().exited('G', 'C', 'A').entered('B', 'F', 'M').end())
        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('M'))
  
        self.assertFalse(state_G.isCurrentState())
        self.assertTrue(state_M.isCurrentState())
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'B', 'F', 'M'))

    # Check from state g, go to state h using parentState syntax
    def test_from_g_to_h_using_parentState_syntax(self):
        monitor_1.reset()
        state_G.gotoState('H')
  
        self.assertTrue(monitor_1.matchSequence().begin().exited('G').entered('H').end())
