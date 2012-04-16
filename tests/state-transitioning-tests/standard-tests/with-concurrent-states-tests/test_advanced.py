'''
Statechart tests, transitioning, standard, with concurrent, advanced
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
                kwargs['substatesAreConcurrent'] = True
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

            class B(State):
                def __init__(self, **kwargs):
                    kwargs['initialSubstateKey'] = 'D'
                    super(Statechart_1.RootState.A.B, self).__init__(**kwargs)

                class D(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.B.D, self).__init__(**kwargs)

                class E(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.B.E, self).__init__(**kwargs)

            class C(State):
                def __init__(self, **kwargs):
                    kwargs['initialSubstateKey'] = 'F'
                    super(Statechart_1.RootState.A.C, self).__init__(**kwargs)

                class F(State):
                    def __init__(self, **kwargs):
                        kwargs['substatesAreConcurrent'] = True
                        super(Statechart_1.RootState.A.C.F, self).__init__(**kwargs)

                    class H(State):
                        def __init__(self, **kwargs):
                            kwargs['initialSubstateKey'] = 'L'
                            super(Statechart_1.RootState.A.C.F.H, self).__init__(**kwargs)

                        class L(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.F.H.L, self).__init__(**kwargs)

                        class M(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.F.H.M, self).__init__(**kwargs)

                    class I(State):
                        def __init__(self, **kwargs):
                            kwargs['initialSubstateKey'] = 'N'
                            super(Statechart_1.RootState.A.C.F.I, self).__init__(**kwargs)

                        class N(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.F.I.N, self).__init__(**kwargs)

                        class O(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.F.I.O, self).__init__(**kwargs)

                class G(State):
                    def __init__(self, **kwargs):
                        kwargs['substatesAreConcurrent'] = True
                        super(Statechart_1.RootState.A.C.G, self).__init__(**kwargs)

                    class J(State):
                        def __init__(self, **kwargs):
                            kwargs['initialSubstateKey'] = 'P'
                            super(Statechart_1.RootState.A.C.G.J, self).__init__(**kwargs)

                        class P(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.G.J.P, self).__init__(**kwargs)

                        class Q(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.G.J.Q, self).__init__(**kwargs)

                    class K(State):
                        def __init__(self, **kwargs):
                            kwargs['initialSubstateKey'] = 'R'
                            super(Statechart_1.RootState.A.C.G.K, self).__init__(**kwargs)

                        class R(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.G.K.R, self).__init__(**kwargs)

                        class S(State):
                            def __init__(self, **kwargs):
                                super(Statechart_1.RootState.A.C.G.K.S, self).__init__(**kwargs)

        class Z(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.Z, self).__init__(**kwargs)

class StateTransitioningStandardAdvancedWithConcurrentTestCase(unittest.TestCase):
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
        global state_O
        global state_P
        global state_Q
        global state_R
        global state_S
        global state_Z

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
        state_O = statechart_1.getState('O')
        state_P = statechart_1.getState('P')
        state_Q = statechart_1.getState('Q')
        state_R = statechart_1.getState('R')
        state_S = statechart_1.getState('S')
        state_Z = statechart_1.getState('Z')

    # Test statechart initialization
    def test_statechart_initialization(self):
        self.assertEqual(monitor_1.length, 10)
        self.assertTrue(monitor_1.matchSequence().begin().entered(rootState_1, 'A').beginConcurrent().beginSequence().entered('B', 'D').endSequence().beginSequence().entered('C', 'F').beginConcurrent().beginSequence().entered('H', 'L').endSequence().beginSequence().entered('I', 'N').endSequence().endConcurrent().endSequence().endConcurrent().entered().end())
  
        self.assertEqual(len(statechart_1.currentStates), 3)
        self.assertTrue(statechart_1.stateIsCurrentState('D'))
        self.assertTrue(statechart_1.stateIsCurrentState('L'))
        self.assertTrue(statechart_1.stateIsCurrentState('N'))
  
        self.assertFalse(statechart_1.stateIsCurrentState('H'))
        self.assertFalse(statechart_1.stateIsCurrentState('I'))
        self.assertFalse(statechart_1.stateIsCurrentState('P'))
        self.assertFalse(statechart_1.stateIsCurrentState('Q'))
        self.assertFalse(statechart_1.stateIsCurrentState('R'))
        self.assertFalse(statechart_1.stateIsCurrentState('S'))
  
        self.assertEqual(len(state_A.currentSubstates), 3)
        self.assertTrue(state_A.stateIsCurrentSubstate('D'))
        self.assertTrue(state_A.stateIsCurrentSubstate('L'))
        self.assertTrue(state_A.stateIsCurrentSubstate('N'))
  
        self.assertEqual(len(state_C.currentSubstates), 2)
        self.assertTrue(state_C.stateIsCurrentSubstate('L'))
        self.assertTrue(state_C.stateIsCurrentSubstate('N'))
  
        self.assertEqual(len(state_F.currentSubstates), 2)
        self.assertTrue(state_F.stateIsCurrentSubstate('L'))
        self.assertTrue(state_F.stateIsCurrentSubstate('N'))
  
        self.assertEqual(len(state_G.currentSubstates), 0)
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'A', 'B', 'D', 'C', 'F', 'H', 'I', 'L', 'N'))


    # Test from state L to state G
    def test_from_l_to_g(self):
        monitor_1.reset()
        state_L.gotoState('G')
  
        self.assertEqual(monitor_1.length, 10)
        self.assertTrue(monitor_1.matchSequence().begin().beginConcurrent().beginSequence().exited('L', 'H').endSequence().beginSequence().exited('N', 'I').endSequence().endConcurrent().exited('F').entered('G').beginConcurrent().beginSequence().entered('J', 'P').endSequence().beginSequence().entered('K', 'R').endSequence().endConcurrent().end())
  
        self.assertEqual(len(statechart_1.currentStates), 3)
        self.assertTrue(statechart_1.stateIsCurrentState('D'))
        self.assertFalse(statechart_1.stateIsCurrentState('L'))
        self.assertFalse(statechart_1.stateIsCurrentState('N'))
        self.assertTrue(statechart_1.stateIsCurrentState('P'))
        self.assertTrue(statechart_1.stateIsCurrentState('R'))
  
        self.assertEqual(len(state_A.currentSubstates), 3)
        self.assertTrue(state_A.stateIsCurrentSubstate('D'))
        self.assertTrue(state_A.stateIsCurrentSubstate('P'))
        self.assertTrue(state_A.stateIsCurrentSubstate('R'))
  
        self.assertEqual(len(state_C.currentSubstates), 2)
        self.assertTrue(state_C.stateIsCurrentSubstate('P'))
        self.assertTrue(state_C.stateIsCurrentSubstate('R'))
  
        self.assertEqual(len(state_F.currentSubstates), 0)
  
        self.assertEqual(len(state_G.currentSubstates), 2)
        self.assertTrue(state_G.stateIsCurrentSubstate('P'))
        self.assertTrue(state_G.stateIsCurrentSubstate('R'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'A', 'B', 'D', 'C', 'G', 'J', 'K', 'P', 'R'))

    # Test from state L to state Z
    def test_from_l_to_z(self):
        monitor_1.reset()
        state_L.gotoState('Z')
  
        self.assertEqual(monitor_1.length, 10)

        self.assertTrue(monitor_1.matchSequence().begin().exited('L', 'H', 'N', 'I', 'F', 'C', 'D', 'B', 'A').entered('Z').end())
         
        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('Z'))
        self.assertFalse(statechart_1.stateIsCurrentState('L'))
        self.assertFalse(statechart_1.stateIsCurrentState('N'))
        self.assertFalse(statechart_1.stateIsCurrentState('D'))
   
        self.assertEqual(len(state_A.currentSubstates), 0)
        self.assertEqual(len(state_B.currentSubstates), 0)
        self.assertEqual(len(state_C.currentSubstates), 0)
        self.assertEqual(len(state_F.currentSubstates), 0)
        self.assertEqual(len(state_G.currentSubstates), 0)
   
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'Z'))

    # Test from state L to state Z, and then to S
    def test_from_l_to_z_to_s(self):
        state_L.gotoState('Z')
  
        monitor_1.reset()
        state_Z.gotoState('S')

        self.assertEqual(monitor_1.length, 10)

        self.assertTrue(monitor_1.matchSequence().begin().exited('Z').entered('A', 'C', 'G', 'K', 'S', 'J', 'P', 'B', 'D').end())
         
        self.assertEqual(len(statechart_1.currentStates), 3)
        self.assertFalse(statechart_1.stateIsCurrentState('Z'))
        self.assertTrue(statechart_1.stateIsCurrentState('S'))
        self.assertTrue(statechart_1.stateIsCurrentState('P'))
        self.assertTrue(statechart_1.stateIsCurrentState('D'))
   
        self.assertEqual(len(state_A.currentSubstates), 3)
        self.assertEqual(len(state_B.currentSubstates), 1)
        self.assertEqual(len(state_C.currentSubstates), 2)
        self.assertEqual(len(state_F.currentSubstates), 0)
        self.assertEqual(len(state_G.currentSubstates), 2)
   
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'A', 'B', 'D', 'C', 'G', 'J', 'K', 'P', 'S'))
