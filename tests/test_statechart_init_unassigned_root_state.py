'''
Statechart tests, init with assigned root state
===========
'''

import unittest

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

owner = ObjectProperty(None)

class A(State):
    def foo(self, *l):
        print 'foo called, trying to goto B'
        self.statechart.gotoState('B') # [PORT] self.gotoState should work...

class B(State):
    def bar(self, *l):
        print 'bar called, trying to goto A'
        self.statechart.gotoState('A')

class Statechart1(StatechartManager):
    initialState = 'A'

    A = A
    B = B

class C(State):
    def foo(self, *l):
        print 'foo called, trying to goto D'
        self.statechart.gotoState('D') # [PORT] self.gotoState should work...

class D(State):
    def bar(self, *l):
        print 'bar called, trying to goto C'
        self.statechart.gotoState('C')

class Statechart2(StatechartManager):
    statesAreConcurrent = True

    C = C
    D = D

#Statechart1 = StatechartManager(**{
#    'initialState': 'A',
#    'A': State(**{ 'foo': lambda self,*l: self.gotoState('B')}),
#    'B': State(**{ 'bar': lambda self,*l: self.gotoState('A')})
#    })

class TestApp(App):
    pass

class StatechartTestCase(unittest.TestCase):
    def setUp(self):
        global s1
        global s2
        global rootState1
        global stateA
        global stateB
        global stateC
        global stateD
        s1 = Statechart1()
        rootState1 = s1.rootState
        stateA = s1.A
        stateB = s1.B
        s2 = Statechart2()
        rootState2 = s2.rootState
        stateC = s2.C
        stateD = s2.D

    def test_init_with_unassigned_root_state(self):
        self.assertTrue(s1.isStatechart)
        self.assertTrue(s1.statechartIsInitialized)
        self.assertTrue(isinstance(rootState1, State))
        self.assertFalse(rootState1.substatesAreConcurrent)

        self.assertEqual(s1.initialState, stateA.__name__) # [PORT] See comments in statechart.py about this not being an actual class object comparison.
        self.assertEqual(rootState1.initialSubstate, 'A')
        self.assertEqual(stateA, type(rootState1.getSubstate('A')))
        self.assertEqual(stateB, type(rootState1.getSubstate('B')))
        
        self.assertEqual(rootState1.owner, s1)
