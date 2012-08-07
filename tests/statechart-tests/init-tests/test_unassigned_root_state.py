'''
Statechart tests, init with assigned root state
===========
'''

import unittest

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

owner = ObjectProperty(None)

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['A'] = self.A
        kwargs['B'] = self.B
        kwargs['initialStateKey'] = 'A'
        super(Statechart_1, self).__init__(**kwargs)

    class A(State):
        def foo(self, *l):
            self.statechart.gotoState('B') # [PORT] self.gotoState should work...

    class B(State):
        def bar(self, *l):
            self.statechart.gotoState('A')

class C(State):
    def foo(self, *l):
        self.statechart.gotoState('D') # [PORT] self.gotoState should work...

class D(State):
    def bar(self, *l):
        self.statechart.gotoState('C')

class Statechart_2(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['statesAreConcurrent'] = True
        super(Statechart_2, self).__init__(**kwargs)

    C = C
    D = D

class RootStateExampleClass(State):
    def __init__(self, **kwargs):
        kwargs['test'] = 'foo'
        super(RootStateExampleClass, self).__init__(**kwargs) 

class E(State):
    pass

class Statechart_3(StatechartManager):
    def __init__(self):
        attrs = { 
            'owner': owner,
            'rootStateExampleClass': RootStateExampleClass,
            'initialStateKey': 'E',
            'E': E
            }
        super(Statechart_3, self).__init__(**attrs) 

class F(State):
    pass

class Statechart_4(StatechartManager):
    def __init__(self):
        attrs = { 
            'autoInitStatechart': False,
            'rootStateExampleClass': RootStateExampleClass,
            'initialStateKey': 'F',
            'F': F
            }
        super(Statechart_4, self).__init__(**attrs) 

#Statechart_1 = StatechartManager(**{
#    'initialStateKey': 'A',
#    'A': State(**{ 'foo': lambda self,*l: self.gotoState('B')}),
#    'B': State(**{ 'bar': lambda self,*l: self.gotoState('A')})
#    })

class TestApp(App):
    pass

class StatechartTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global statechart_2
        global statechart_3
        global statechart_4
        global rootState_1
        global rootState_2
        global rootState_3
        global state_A
        global state_B
        global state_C
        global state_D
        global state_E

        statechart_1 = Statechart_1()
        rootState_1 = statechart_1.rootStateInstance
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        
        statechart_2 = Statechart_2()
        rootState_2 = statechart_2.rootStateInstance
        state_C = statechart_2.getState('C')
        state_D = statechart_2.getState('D')

        statechart_3 = Statechart_3()
        rootState_3 = statechart_3.rootStateInstance
        state_E = statechart_3.getState('E')

        statechart_4 = Statechart_4()

    def test_statechart_1(self):
        self.assertTrue(statechart_1.isStatechart)
        self.assertTrue(statechart_1.statechartIsInitialized)
        self.assertTrue(isinstance(rootState_1, State))
        self.assertFalse(rootState_1.substatesAreConcurrent)

        self.assertEqual(statechart_1.initialStateKey, state_A.name)
        self.assertEqual(rootState_1.initialSubstateKey, 'A')
        self.assertEqual(state_A, rootState_1.getSubstate('A'))
        self.assertEqual(state_B, rootState_1.getSubstate('B'))
        
        self.assertEqual(rootState_1.owner, statechart_1)
        self.assertEqual(state_A.owner, statechart_1)
        self.assertEqual(state_B.owner, statechart_1)

        self.assertTrue(state_A.isCurrentState())
        self.assertFalse(state_B.isCurrentState())

        statechart_1.sendEvent('foo')

        self.assertFalse(state_A.isCurrentState())
        self.assertTrue(state_B.isCurrentState())

    def test_statechart_2(self):
        self.assertTrue(statechart_2.isStatechart)
        self.assertTrue(statechart_2.statechartIsInitialized)
        self.assertTrue(isinstance(rootState_2, State))
        self.assertTrue(rootState_2.substatesAreConcurrent)

        self.assertEqual(statechart_2.initialStateKey, '')
        self.assertEqual(rootState_2.initialSubstateKey, '')
        self.assertEqual(state_C, rootState_2.getSubstate('C'))
        self.assertEqual(state_D, rootState_2.getSubstate('D'))
        
        self.assertEqual(rootState_2.owner, statechart_2)
        self.assertEqual(state_C.owner, statechart_2)
        self.assertEqual(state_D.owner, statechart_2)

        self.assertTrue(state_C.isCurrentState())
        self.assertTrue(state_D.isCurrentState())

    def test_statechart_3(self):
        self.assertTrue(statechart_3.isStatechart)
        self.assertTrue(statechart_3.statechartIsInitialized)
        self.assertTrue(isinstance(rootState_3, RootStateExampleClass))
        self.assertFalse(rootState_3.substatesAreConcurrent)
        
        self.assertEqual(rootState_3.owner, owner)
        self.assertEqual(state_E.owner, owner)

        self.assertEqual(statechart_3.initialStateKey, 'E')
        self.assertEqual(rootState_3.initialSubstateKey, 'E')
        self.assertEqual(state_E, rootState_3.getSubstate('E'))
        self.assertTrue(state_E.isCurrentState())

    def test_statechart_4(self):
        self.assertTrue(statechart_4.isStatechart)
        self.assertFalse(statechart_4.statechartIsInitialized)
        self.assertEqual(statechart_4.rootStateInstance, None)
        
        statechart_4.initStatechart()

        self.assertTrue(statechart_4.statechartIsInitialized)
        self.assertFalse(statechart_4.rootStateInstance is None)
        self.assertEqual(statechart_4.rootStateInstance.getSubstate('F'), statechart_4.getState('F'))
