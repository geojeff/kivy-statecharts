'''
Statechart tests, transitioning, history, standard, with concurrent
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
        kwargs['root_state_class'] = self.RootState
        kwargs['monitor_is_active'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'X'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class X(State):
            def __init__(self, **kwargs):
                kwargs['substates_are_concurrent'] = True
                super(Statechart_1.RootState.X, self).__init__(**kwargs)
    
            class A(State):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'C'
                    super(Statechart_1.RootState.X.A, self).__init__(**kwargs)
    
                class C(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.A.C, self).__init__(**kwargs)
    
                class D(State):
                    def __init__(self, **kwargs):
                        super(Statechart_1.RootState.X.A.D, self).__init__(**kwargs)
    
            class B(State):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'E'
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
        global root_state_1
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
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        state_C = statechart_1.get_state('C')
        state_D = statechart_1.get_state('D')
        state_E = statechart_1.get_state('E')
        state_F = statechart_1.get_state('F')
        state_X = statechart_1.get_state('X')
        state_Z = statechart_1.get_state('Z')
  
    # Send event event_A
    def test_initial_statechart_history_state_objects(self):
        state_C.go_to_state('D')
        state_E.go_to_state('F')

        self.assertEqual(state_A.history_state, state_D)
        self.assertEqual(state_B.history_state, state_F)
        self.assertTrue(state_D.is_current_state())
        self.assertTrue(state_F.is_current_state())
        self.assertFalse(state_E.is_current_state())

        monitor_1.reset()
  
        state_D.go_to_state('Z');
        self.assertTrue(state_Z.is_current_state())
 
        state_Z.go_to_history_state('A')

        self.assertEqual(state_A.history_state, state_D)
        self.assertEqual(state_B.history_state, state_E)
        self.assertTrue(state_D.is_current_state())
        self.assertFalse(state_F.is_current_state())
        self.assertTrue(state_E.is_current_state())
