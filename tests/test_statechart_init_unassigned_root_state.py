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

class Statechart_1(StatechartManager):
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

class Statechart_2(StatechartManager):
    statesAreConcurrent = True

    C = C
    D = D

#Statechart_1 = StatechartManager(**{
#    'initialState': 'A',
#    'A': State(**{ 'foo': lambda self,*l: self.gotoState('B')}),
#    'B': State(**{ 'bar': lambda self,*l: self.gotoState('A')})
#    })

class TestApp(App):
    pass

class StatechartTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global statechart_2
        global rootState_1
        global state_A
        global state_B
        global stateC
        global stateD
        statechart_1 = Statechart_1()
        rootState_1 = statechart_1.rootState
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        statechart_2 = Statechart_2()
        rootState2 = statechart_2.rootState
        stateC = statechart_2.C
        stateD = statechart_2.D

    def test_statechart_1(self):
        self.assertTrue(statechart_1.isStatechart)
        self.assertTrue(statechart_1.statechartIsInitialized)
        self.assertTrue(isinstance(rootState_1, State))
        self.assertFalse(rootState_1.substatesAreConcurrent)

        self.assertEqual(statechart_1.initialState, state_A.name) # [PORT] See comments in statechart.py about this not being an actual class object comparison.
        self.assertEqual(rootState_1.initialSubstate, 'A')
        self.assertEqual(state_A, rootState_1.getSubstate('A'))
        self.assertEqual(state_B, rootState_1.getSubstate('B'))
        
        self.assertEqual(rootState_1.owner, statechart_1)
        self.assertEqual(state_A.owner, statechart_1)
        self.assertEqual(state_B.owner, statechart_1)

        self.assertTrue(state_A.isCurrentState)
        self.assertFalse(state_B.isCurrentState)

        statechart_1.sendEvent('foo')

        self.assertFalse(state_A.isCurrentState)
        self.assertTrue(state_B.isCurrentState)
