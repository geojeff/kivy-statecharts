'''
Statechart tests, private, state path matcher
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager
from kivy_statecharts.private.state_path_matcher import StatePathMatcher

import os, inspect

class State_1:
    def __init__(self):
        self.substates = [self.Substate()]

    class Substate:
        def __init__(self):
            self.name = 'A'
            
class State_2:
    def __init__(self):
        self.substates = [self.Substate()]

    class Substate:
        def __init__(self):
            self.name = 'B'
            
class StatePathMatcherTestCase(unittest.TestCase):
    def setUp(self):
        global state_1
        global state_2

        state_1 = State_1()
        state_2 = State_2()

    # Test with expression A
    def test_with_expression_a(self):
        spm = StatePathMatcher(expression='A')

        self.assertTrue(spm.match('A'))
        self.assertTrue(spm.match('B.A'))
        self.assertFalse(spm.match('B'))
        self.assertFalse(spm.match('A.B'))

    # Test with expression A.B
    def test_with_expression_a_dot_b(self):
        spm = StatePathMatcher(expression='A.B')

        self.assertTrue(spm.match('A.B'))
        self.assertTrue(spm.match('X.A.B'))

        self.assertFalse(spm.match('B'))
        self.assertFalse(spm.match('A'))
        self.assertFalse(spm.match('B.A'))
        self.assertFalse(spm.match('A.B.X'))

    # Test with expression A~B
    def test_with_expression_a_tilde_b(self):
        spm = StatePathMatcher(expression='A~B')

        self.assertTrue(spm.match('A.B'))
        self.assertTrue(spm.match('A.X.B'))
        self.assertTrue(spm.match('A.X.Y.B'))
        self.assertTrue(spm.match('X.A.B'))
        self.assertTrue(spm.match('X.A.Y.B'))

        self.assertFalse(spm.match('B'))
        self.assertFalse(spm.match('A'))
        self.assertFalse(spm.match('A.B.X'))
        self.assertFalse(spm.match('A.Y.B.X'))
        self.assertFalse(spm.match('Y.A.B.X'))

    # Test with expression A.B~C.D
    def test_with_expression_a_dot_b_tilde_c_dot_d(self):
        spm = StatePathMatcher(expression='A.B~C.D')

        self.assertTrue(spm.match('A.B.C.D'))
        self.assertTrue(spm.match('A.B.X.C.D'))
        self.assertTrue(spm.match('A.B.X.Y.C.D'))
        self.assertTrue(spm.match('Z.A.B.X.Y.C.D'))

        self.assertFalse(spm.match('A.B.C.D.X'))
        self.assertFalse(spm.match('B.C.D'))
        self.assertFalse(spm.match('A.B.C'))
        self.assertFalse(spm.match('A.B.D'))
        self.assertFalse(spm.match('A.C.D'))
        self.assertFalse(spm.match('A.B.Y.C.D.X'))

    # Test with expression self.A
    def test_with_expression_self_dot_a(self):
        spm = StatePathMatcher(expression='self.A')

        spm.state = state_1

        self.assertTrue(spm.match('A'))

        self.assertFalse(spm.match('B'))
        self.assertFalse(spm.match('A.B'))

        spm.state = state_2

        self.assertFalse(spm.match('A'))

    # Test with expression self.A.B
    def test_with_expression_self_dot_a_dot_b(self):
        spm = StatePathMatcher(expression='self.A.B')

        spm.state = state_1

        self.assertTrue(spm.match('A.B'))

        self.assertFalse(spm.match('A'))
        self.assertFalse(spm.match('B'))

    # Test with expression self.A~B
    def test_with_expression_self_dot_a_tilde_b(self):
        spm = StatePathMatcher(expression='self.A~B')

        spm.state = state_1

        self.assertTrue(spm.match('A.B'))
        self.assertTrue(spm.match('A.X.B'))

        self.assertFalse(spm.match('A'))
        self.assertFalse(spm.match('B'))
        self.assertFalse(spm.match('B.A'))
        
    # Test with expression A~B~C -- too many ~
    def test_with_expression_a_tilde_b_tilde_c(self):

        with self.assertRaises(Exception) as cm:
            spm = StatePathMatcher(expression='A~B~C')

        msg = "Invalid use of '~' at part 0"
        self.assertEqual(str(cm.exception), msg)

    # Test with expression A.self.A.B.C -- embedded self
    def test_with_expression_a_dot_self_dot_a_dot_b_dot_c(self):

        with self.assertRaises(Exception) as cm:
            spm = StatePathMatcher(expression='A.self.A.B.C')

        msg = "Invalid use of 'self' at part 1"
        self.assertEqual(str(cm.exception), msg)

    # Test with bad match arguments
    def test_with_bad_match_arguments(self):
        spm = StatePathMatcher(expression='self.A~B')

        self.assertFalse(spm.match(None))
        self.assertFalse(spm.match(''))
        self.assertFalse(spm.match(dict))

