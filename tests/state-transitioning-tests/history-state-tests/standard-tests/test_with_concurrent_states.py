'''
Statechart tests, transitioning, history, standard, with concurrent
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
        kwargs['rootState'] = self.RootState
        kwargs['monitorIsActive'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'X'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class X(State):
            def __init__(self, **kwargs):
                kwargs['substatesAreConcurrent'] = True
                super(Statechart_1.RootState.X, self).__init__(**kwargs)
    
            class A(State):
                def __init__(self, **kwargs):
                    kwargs['initialSubstateKey'] = 'C'
                    super(Statechart_1.RootState.X.A, self).__init__(**kwargs)
    
                class C(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.A.C, self).__init__(**kwargs)
    
                class D(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.A.D, self).__init__(**kwargs)
    
            class B(State):
                def __init__(self, **kwargs):
                    kwargs['initialSubstateKey'] = 'E'
                    super(Statechart_1.RootState.X.B, self).__init__(**kwargs)
    
                class E(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.B.E, self).__init__(**kwargs)
    
                class F(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.B.F, self).__init__(**kwargs)

        class Z(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.Z, self).__init__(**kwargs)
    
class StateTransitioningHistoryStandardWithConcurrentTestCase(unittest.TestCase):
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
        global state_X
        global state_Z

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootState
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        state_C = statechart_1.getState('C')
        state_D = statechart_1.getState('D')
        state_E = statechart_1.getState('E')
        state_F = statechart_1.getState('F')
        state_X = statechart_1.getState('X')
        state_Z = statechart_1.getState('Z')
  
    # Send event event_A
    def test_initial_statechart_history_state_objects(self):
        state_C.gotoState('D')
        state_E.gotoState('F')

        self.assertEqual(state_A.historyState, state_D)
        self.assertEqual(state_B.historyState, state_F)
        self.assertTrue(state_D.isCurrentState())
        self.assertTrue(state_F.isCurrentState())
        self.assertFalse(state_E.isCurrentState())

        monitor_1.reset()
  
        state_D.gotoState('Z');
        self.assertTrue(state_Z.isCurrentState())
 
        state_Z.gotoHistoryState('A')

        self.assertEqual(state_A.historyState, state_D)
        self.assertEqual(state_B.historyState, state_E)
        self.assertTrue(state_D.isCurrentState())
        self.assertFalse(state_F.isCurrentState())
        self.assertTrue(state_E.isCurrentState())
