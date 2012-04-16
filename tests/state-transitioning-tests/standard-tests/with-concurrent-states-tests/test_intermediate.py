'''
Statechart tests, transitioning, standard, with concurrent, intermediate
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
                        super(Statechart_1.RootState.A.C.F, self).__init__(**kwargs)

                class G(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.A.C.G, self).__init__(**kwargs)

        class Z(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.Z, self).__init__(**kwargs)

class StateTransitioningStandardIntermediateWithConcurrentTestCase(unittest.TestCase):
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
        state_Z = statechart_1.getState('Z')

    # Test statechart initialization
    def test_statechart_initialization(self):
        self.assertEqual(monitor_1.length, 6)

        self.assertTrue(monitor_1.matchSequence().begin().entered(rootState_1, 'A').beginConcurrent().beginSequence().entered('B', 'D').endSequence().beginSequence().entered('C', 'F').endSequence().endConcurrent().end())
  
        self.assertEqual(len(statechart_1.currentStates), 2)
  
        self.assertTrue(statechart_1.stateIsCurrentState('D'))
        self.assertTrue(statechart_1.stateIsCurrentState('F'))
        self.assertTrue(state_A.stateIsCurrentSubstate('D'))
        self.assertTrue(state_A.stateIsCurrentSubstate('F'))
        self.assertFalse(state_A.stateIsCurrentSubstate('E'))
        self.assertFalse(state_A.stateIsCurrentSubstate('G'))
        self.assertTrue(state_B.stateIsCurrentSubstate('D'))
        self.assertFalse(state_B.stateIsCurrentSubstate('E'))
        self.assertTrue(state_C.stateIsCurrentSubstate('F'))
        self.assertFalse(state_C.stateIsCurrentSubstate('G'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'A', 'B', 'C', 'D', 'F'))

    # Test from state D, go to state Z
    def test_from_d_to_z(self):
        monitor_1.reset()
        state_D.gotoState('Z')
  
        self.assertEqual(monitor_1.length, 6)
        self.assertTrue(monitor_1.matchSequence().begin().exited('D', 'B', 'F', 'C', 'A').entered('Z').end())
        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('Z'))
        self.assertEqual(len(state_A.currentSubstates), 0)
        self.assertFalse(state_A.stateIsCurrentSubstate('D'))
        self.assertFalse(state_A.stateIsCurrentSubstate('F'))
        self.assertFalse(state_A.stateIsCurrentSubstate('E'))
        self.assertFalse(state_A.stateIsCurrentSubstate('G'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'Z'))

    # Test from state A, go to state Z, and then back to state A
    def test_from_a_to_z_and_back_to_a(self):
        monitor_1.reset()
        state_A.gotoState('Z')
  
        self.assertEqual(monitor_1.length, 6)

        self.assertTrue(monitor_1.matchSequence().begin().beginConcurrent().beginSequence().exited('D', 'B').endSequence().beginSequence().exited('F', 'C').endSequence().endConcurrent().exited('A').entered('Z').end())
  
        self.assertEqual(len(statechart_1.currentStates), 1)
        self.assertTrue(statechart_1.stateIsCurrentState('Z'))
  
        monitor_1.reset()
        state_Z.gotoState('A')
  
        self.assertEqual(monitor_1.length, 6)

        self.assertTrue(monitor_1.matchSequence().begin().exited('Z').entered('A').beginConcurrent().beginSequence().entered('B', 'D').endSequence().beginSequence().entered('C', 'F').endSequence().endConcurrent().end())
  
        self.assertEqual(len(statechart_1.currentStates), 2)
        self.assertTrue(statechart_1.stateIsCurrentState('D'))
        self.assertTrue(statechart_1.stateIsCurrentState('F'))
        self.assertEqual(len(statechart_1.currentStates), 2)
        self.assertTrue(state_A.stateIsCurrentSubstate('D'))
        self.assertFalse(state_A.stateIsCurrentSubstate('E'))
        self.assertTrue(state_A.stateIsCurrentSubstate('F'))
        self.assertFalse(state_A.stateIsCurrentSubstate('G'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'A', 'B', 'C', 'D', 'F'))
