'''
Statechart tests, debug, sequence matcher
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager
from kivy_statecharts.debug.monitor import StatechartMonitor

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['initial_state_key'] = 'A'
        super(Statechart_1, self).__init__(**kwargs)

    class A(State):
        def __init__(self, **kwargs):
            super(Statechart_1.A, self).__init__(**kwargs)

    class B(State):
        def __init__(self, **kwargs):
            super(Statechart_1.B, self).__init__(**kwargs)

    class C(State):
        def __init__(self, **kwargs):
            super(Statechart_1.C, self).__init__(**kwargs)

    class D(State):
        def __init__(self, **kwargs):
            super(Statechart_1.D, self).__init__(**kwargs)

    class E(State):
        def __init__(self, **kwargs):
            super(Statechart_1.E, self).__init__(**kwargs)

    class M(State):
        def __init__(self, **kwargs):
            super(Statechart_1.M, self).__init__(**kwargs)

    class N(State):
        def __init__(self, **kwargs):
            super(Statechart_1.N, self).__init__(**kwargs)

    class O(State):
        def __init__(self, **kwargs):
            super(Statechart_1.O, self).__init__(**kwargs)

    class P(State):
        def __init__(self, **kwargs):
            super(Statechart_1.P, self).__init__(**kwargs)

    class X(State):
        def __init__(self, **kwargs):
            super(Statechart_1.X, self).__init__(**kwargs)

    class Y(State):
        def __init__(self, **kwargs):
            super(Statechart_1.Y, self).__init__(**kwargs)

class StateSequenceMatcherTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global root_state_1
        global monitor_1
        global state_A
        global state_B
        global state_C
        global state_D
        global state_E
        global state_M
        global state_N
        global state_O
        global state_P
        global state_X
        global state_Y

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        monitor_1 = StatechartMonitor(statechart_1)
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        state_C = statechart_1.get_state('C')
        state_D = statechart_1.get_state('D')
        state_E = statechart_1.get_state('E')
        state_M = statechart_1.get_state('M')
        state_N = statechart_1.get_state('N')
        state_O = statechart_1.get_state('O')
        state_P = statechart_1.get_state('P')
        state_X = statechart_1.get_state('X')
        state_Y = statechart_1.get_state('Y')

    # Match against sequence entered A
    def test_match_against_sequence_entered_A(self):
        monitor_1.append_entered_state(state_A)

        matcher = monitor_1.match_sequence()

        self.assertTrue(matcher.begin().entered(state_A).end())
        self.assertTrue(matcher.begin().entered('A').end())
        self.assertFalse(matcher.begin().entered(state_B).end())
        self.assertFalse(matcher.begin().exited(state_A).end())
        self.assertFalse(matcher.begin().exited(state_B).end())
        self.assertFalse(matcher.begin().entered(state_A, state_B).end())
        self.assertFalse(matcher.begin().entered(state_A).entered(state_B).end())

    # Match against sequence exited A
    def test_match_against_sequence_exited_A(self):
        monitor_1.append_exited_state(state_A)
  
        matcher = monitor_1.match_sequence()

        self.assertTrue(matcher.begin().exited(state_A).end())
        self.assertTrue(matcher.begin().exited('A').end())
        self.assertFalse(matcher.begin().exited(state_B).end())
        self.assertFalse(matcher.begin().entered(state_A).end())
        self.assertFalse(matcher.begin().entered(state_B).end())
        self.assertFalse(matcher.begin().exited(state_A, state_B).end())
        self.assertFalse(matcher.begin().exited(state_A).exited(state_B).end())

    # Match against sequence entered A, entered B
    def test_match_against_sequence_entered_A_entered_B(self):
        monitor_1.append_entered_state(state_A)
        monitor_1.append_entered_state(state_B)
  
        matcher = monitor_1.match_sequence()

        self.assertTrue(matcher.begin().entered(state_A, state_B).end())
        self.assertTrue(matcher.begin().entered('A', 'B').end())
        self.assertTrue(matcher.begin().entered(state_A).entered(state_B).end())
        self.assertFalse(matcher.begin().entered(state_A).end())
        self.assertFalse(matcher.begin().entered(state_B).end())
        self.assertFalse(matcher.begin().exited(state_B, state_A).end())
        self.assertFalse(matcher.begin().exited('B', 'A').end())
        self.assertFalse(matcher.begin().exited(state_A, state_C).exited(state_B).end())
        self.assertFalse(matcher.begin().exited('A', 'C').exited(state_B).end())
        self.assertFalse(matcher.begin().entered(state_A).entered(state_C).end())
        self.assertFalse(matcher.begin().exited(state_A, state_B, state_C).exited(state_B).end())

    # Match against sequence exited A, exited B
    def test_match_against_sequence_exited_A_exited_B(self):
        monitor_1.append_exited_state(state_A)
        monitor_1.append_exited_state(state_B)
  
        matcher = monitor_1.match_sequence()

        self.assertTrue(matcher.begin().exited(state_A, state_B).end())
        self.assertTrue(matcher.begin().exited('A', 'B').end())
        self.assertTrue(matcher.begin().exited(state_A).exited(state_B).end())
        self.assertFalse(matcher.begin().exited(state_A).end())
        self.assertFalse(matcher.begin().exited(state_B).end())
        self.assertFalse(matcher.begin().exited(state_B, state_A).end())
        self.assertFalse(matcher.begin().exited('B', 'A').end())
        self.assertFalse(matcher.begin().exited(state_B).exited(state_A).exited(state_B).end())
        self.assertFalse(matcher.begin().exited(state_A, state_C).exited(state_B).end())
        self.assertFalse(matcher.begin().exited('A', 'C').exited(state_B).end())
        self.assertFalse(matcher.begin().exited(state_A).exited(state_C).end())

    # Match against sequence exited A, entered B
    def test_match_against_sequence_exited_A_entered_B(self):
        monitor_1.append_exited_state(state_A)
        monitor_1.append_entered_state(state_B)
  
        matcher = monitor_1.match_sequence()

        self.assertTrue(matcher.begin().exited(state_A).entered(state_B).end())
        self.assertTrue(matcher.begin().exited('A').entered('B').end())
        self.assertFalse(matcher.begin().entered(state_A).exited(state_A).end())
        self.assertFalse(matcher.begin().entered('A').exited('B').end())
        self.assertFalse(matcher.begin().exited(state_A).entered(state_C).end())
        self.assertFalse(matcher.begin().exited(state_A).entered(state_B, state_C).end())
        self.assertFalse(matcher.begin().exited(state_A).entered(state_B).entered(state_C).end())
        self.assertFalse(matcher.begin().exited(state_A).entered(state_B).exited(state_C).end())

    # Match against sequence seq(enter A), seq(enter B)
    def test_match_against_seq_enter_A_seq_enter_B(self):
        monitor_1.append_entered_state(state_A)
        monitor_1.append_entered_state(state_B)
  
        matcher = monitor_1.match_sequence()

        matcher.begin().begin_sequence().entered(state_A).end_sequence().begin_sequence().entered(state_B).end_sequence().end()
        self.assertTrue(matcher.match)

        matcher.begin().begin_sequence().entered(state_A).entered(state_B).end_sequence().end()
        self.assertTrue(matcher.match)
  
        matcher.begin().begin_sequence().entered(state_A).entered(state_B).end_sequence().end()
        self.assertTrue(matcher.match)
  
        matcher.begin().begin_sequence().entered(state_A, state_B).end_sequence().end()
        self.assertTrue(matcher.match)

        matcher.begin().begin_sequence().entered(state_A).end_sequence().end()
        self.assertFalse(matcher.match)
  
        matcher.begin().begin_sequence().entered(state_A).end_sequence().begin_sequence().entered(state_C).end_sequence().end()
        self.assertFalse(matcher.match)
  
        matcher.begin().begin_sequence().entered(state_A).end_sequence().begin_sequence().entered(state_B).end_sequence().begin_sequence().entered(state_C).end_sequence().end()
        self.assertFalse(matcher.match)

    # Match against sequence con(entered A)
    def test_match_against_seq_con_entered_A(self):
        monitor_1.append_entered_state(state_A)
  
        matcher = monitor_1.match_sequence()

        matcher.begin().begin_concurrent().entered(state_A).end_concurrent().end() 
        self.assertTrue(matcher.match)

        matcher.begin().begin_concurrent().begin_sequence().entered(state_A).end_sequence().end_concurrent().end()
        self.assertTrue(matcher.match)

        matcher.begin().begin_concurrent().entered(state_B).end_concurrent().end()
        self.assertFalse(matcher.match)
   
        matcher.begin().begin_concurrent().exited(state_A).end_concurrent().end()
        self.assertFalse(matcher.match)
  
        matcher.begin().begin_concurrent().entered(state_A).entered(state_B).end_concurrent().end()
        self.assertFalse(matcher.match)
  
        matcher.begin().begin_concurrent().entered(state_B).entered(state_A).end_concurrent().end()
        self.assertFalse(matcher.match)

    # Match against sequence con(entered A entered B)
    def test_match_against_seq_con_entered_A_entered_B(self):
        monitor_1.append_entered_state(state_A)
        monitor_1.append_entered_state(state_B)
  
        matcher = monitor_1.match_sequence()

        matcher.begin().begin_concurrent().entered(state_A).entered(state_B).end_concurrent().end()
        self.assertTrue(matcher.match)
   
        matcher.begin().begin_concurrent().entered(state_B).entered(state_A).end_concurrent().end()
        self.assertTrue(matcher.match)
   
        matcher.begin().begin_concurrent().begin_sequence().entered(state_A).end_sequence().entered(state_B).end_concurrent().end()
        self.assertTrue(matcher.match)
  
        matcher.begin().begin_concurrent().begin_sequence().entered(state_A).end_sequence().begin_sequence().entered(state_B).end_sequence().end_concurrent().end()
        self.assertTrue(matcher.match)
   
        matcher.begin().begin_concurrent().entered(state_A, state_B).end_concurrent().end()
        self.assertTrue(matcher.match)
  
        matcher.begin().begin_concurrent().begin_sequence().entered(state_A).entered(state_B).end_sequence().end_concurrent().end()
        self.assertTrue(matcher.match)
   
        matcher.begin().begin_concurrent().entered(state_A).end_concurrent().end()
        self.assertFalse(matcher.match)
  
        matcher.begin().begin_concurrent().entered(state_A).entered(state_C).end_concurrent().end()
        self.assertFalse(matcher.match)
   
        matcher.begin().begin_concurrent().entered(state_A).entered(state_B).entered(state_C).end_concurrent().end()
        self.assertFalse(matcher.match)
   
    # Match against sequence con(entered A entered B) 2
    def test_match_against_seq_con_entered_A_entered_B_2(self):
        monitor_1.append_entered_state(state_A)
        monitor_1.append_entered_state(state_B)
        monitor_1.append_entered_state(state_X)
        monitor_1.append_entered_state(state_M)
        monitor_1.append_entered_state(state_N)
        monitor_1.append_entered_state(state_Y)
        monitor_1.append_entered_state(state_O)
        monitor_1.append_entered_state(state_P)
        monitor_1.append_entered_state(state_C)
  
        matcher = monitor_1.match_sequence()
  
        matcher.begin().entered(state_A).entered(state_B).begin_concurrent().begin_sequence().entered(state_X, state_M, state_N).end_sequence().begin_sequence().entered(state_Y, state_O, state_P).end_sequence().end_concurrent().entered(state_C).end()
        self.assertTrue(matcher.match)
  
        matcher.begin().entered(state_A).entered(state_B).begin_concurrent().begin_sequence().entered(state_Y, state_O, state_P).end_sequence().begin_sequence().entered(state_X, state_M, state_N).end_sequence().end_concurrent().entered(state_C).end()
        self.assertTrue(matcher.match)

        matcher.begin().entered(state_A).entered(state_B).begin_concurrent().begin_sequence().entered(state_X, state_M).end_sequence().begin_sequence().entered(state_Y, state_O, state_P).end_sequence().end_concurrent().entered(state_C).end()
        self.assertFalse(matcher.match)
    
        matcher.begin().entered(state_A).entered(state_B).begin_concurrent().begin_sequence().entered(state_X, state_M, state_N).end_sequence().begin_sequence().entered(state_Y, state_O).end_sequence().end_concurrent().entered(state_C).end()
        self.assertFalse(matcher.match)

        matcher.begin().entered(state_A).entered(state_B).begin_concurrent().begin_sequence().entered(state_X, state_M, state_N).end_sequence().begin_sequence().entered(state_Y, state_O, state_P).end_sequence().entered(state_E).end_concurrent().entered(state_C).end()
        self.assertFalse(matcher.match)


    # Call match_entered_states() with incorrect arguments
    def test_match_entered_states_with_incorrect_arguments(self):
        monitor_1.append_entered_state(state_A)

        matcher = monitor_1.match_sequence()

        self.assertTrue(matcher.begin().entered(state_A).end())
        self.assertTrue(len(statechart_1.entered_states()), 1)
  
        self.assertTrue(monitor_1.match_entered_states(root_state_1, state_A))
        self.assertTrue(monitor_1.match_entered_states(root_state_1, 'A'))

        self.assertFalse(monitor_1.match_entered_states(root_state_1, state_A, state_B))
        self.assertFalse(monitor_1.match_entered_states(root_state_1, 'A', 'B'))

        self.assertEqual(str(monitor_1), '[entered A]')
