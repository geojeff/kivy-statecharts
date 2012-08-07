'''
Statechart tests, transitioning, standard, with concurrent, basic
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
            kwargs['substatesAreConcurrent'] = True
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'C'
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

            class C(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.C, self).__init__(**kwargs)

            class D(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.D, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'E'
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

            class E(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.E, self).__init__(**kwargs)

            class F(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.F, self).__init__(**kwargs)

class StateTransitioningStandardBasicWithConcurrentTestCase(unittest.TestCase):
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

    # Check statechart initialization
    def test_statechart_initialization(self):
        self.assertEqual(monitor_1.length, 5)

        self.assertTrue(monitor_1.matchSequence().begin().entered(rootState_1).beginConcurrent().beginSequence().entered('A', 'C').endSequence().beginSequence().entered('B', 'E').endSequence().endConcurrent() .end())
        self.assertFalse(monitor_1.matchSequence().begin().entered(rootState_1).beginConcurrent().entered('A', 'B').endConcurrent().beginConcurrent().entered('C', 'E').endConcurrent().end())
  
        self.assertEqual(len(statechart_1.currentStates), 2)
  
        self.assertTrue(statechart_1.stateIsCurrentState('C'))
        self.assertTrue(statechart_1.stateIsCurrentState('E'))
        self.assertFalse(statechart_1.stateIsCurrentState('D'))
        self.assertFalse(statechart_1.stateIsCurrentState('F'))
  
        self.assertTrue(state_A.stateIsCurrentSubstate('C'))
        self.assertFalse(state_A.stateIsCurrentSubstate('D'))
        self.assertTrue(state_B.stateIsCurrentSubstate('E'))
        self.assertFalse(state_B.stateIsCurrentSubstate('F'))
  
        self.assertFalse(state_A.isCurrentState())
        self.assertFalse(state_B.isCurrentState())
        self.assertTrue(state_C.isCurrentState())
        self.assertFalse(state_D.isCurrentState())
        self.assertTrue(state_E.isCurrentState())
        self.assertFalse(state_F.isCurrentState())

    # From state C, go to state D, and from state E, go to state F
    def test_from_C_to_D_and_from_E_to_F(self):
        monitor_1.reset()

        state_C.gotoState('D')

        self.assertEqual(monitor_1.length, 2)

        self.assertTrue(monitor_1.matchSequence().begin().exited('C').entered('D').end())
  
        monitor_1.reset()
  
        state_E.gotoState('F')

        self.assertEqual(monitor_1.length, 2)
        self.assertTrue(monitor_1.matchSequence().begin().exited('E').entered('F').end())
  
        self.assertEqual(len(statechart_1.currentStates), 2)
  
        self.assertTrue(statechart_1.stateIsCurrentState('D'))
        self.assertTrue(statechart_1.stateIsCurrentState('F'))
  
        self.assertFalse(state_A.stateIsCurrentSubstate('C'))
        self.assertTrue(state_A.stateIsCurrentSubstate('D'))
        self.assertFalse(state_B.stateIsCurrentSubstate('E'))
        self.assertTrue(state_B.stateIsCurrentSubstate('F'))
  
        self.assertFalse(state_A.isCurrentState())
        self.assertFalse(state_B.isCurrentState())
        self.assertFalse(state_C.isCurrentState())
        self.assertTrue(state_D.isCurrentState())
        self.assertFalse(state_E.isCurrentState())
        self.assertTrue(state_F.isCurrentState())
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'A', 'D', 'B', 'F'))

    # From state A, go to sibling concurrent state B
    def test_from_a_to_sibling_concurrent_state_b(self):
        monitor_1.reset()

        print 'expecting to get an error...'
        state_A.gotoState('B')

        self.assertEqual(monitor_1.length, 0)
        self.assertEqual(len(statechart_1.currentStates), 2)
        self.assertTrue(statechart_1.stateIsCurrentState('C'))
        self.assertTrue(statechart_1.stateIsCurrentState('E'))
        self.assertTrue(state_A.stateIsCurrentSubstate('C'))
        self.assertFalse(state_A.stateIsCurrentSubstate('D'))
        self.assertTrue(state_B.stateIsCurrentSubstate('E'))
        self.assertFalse(state_B.stateIsCurrentSubstate('F'))
  
        self.assertIsNotNone(monitor_1.matchEnteredStates(rootState_1, 'A', 'C', 'B', 'E'))
