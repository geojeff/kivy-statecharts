'''
Statechart tests, owner
===========
'''

import unittest

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

class Owner_1_MC(type):
    def __repr__(self):
        return 'Owner_1'
class Owner_1(object):
    __metaclass__ = Owner_1_MC

class Owner_2_MC(type):
    def __repr__(self):
        return 'Owner_2'
class Owner_2(object):
    __metaclass__ = Owner_2_MC

class Owner_3_MC(type):
    def __repr__(self):
        return 'Owner_3'
class Owner_3(object):
    __metaclass__ = Owner_3_MC

class TestState(State):
    def __init__(self, **kwargs):
        super(TestState, self).__init__(**kwargs)

    accessedOwner = ObjectProperty(None, allownone=True)
      
    def reset(self, *l):
        setattr(self, 'accessedOwner', None)
      
    def render(self, *l):
        setattr(self, 'accessedOwner', self.owner)
      
class TestStatechart(StatechartManager):
    def __init__(self, **kwargs):
        super(TestStatechart, self).__init__(**kwargs)

    def render(self, *l):
        self.invokeStateMethod('render')

class A(TestState):
    def __init__(self, **kwargs):
        super(A, self).__init__(**kwargs)

    def foo(self, *l):
        self.gotoState('B')

class B(TestState):
    def __init__(self, **kwargs):
        super(B, self).__init__(**kwargs)

    def bar(self, *l):
        self.gotoState('A')

class Z(TestState):
    pass 

class Y(TestState):
    def __init__(self, **kwargs):
        self.initialSubstateKey = 'Z'
        super(Y, self).__init__(**kwargs)

    Z = Z

class X(TestState):
    def __init__(self, **kwargs):
        self.initialSubstateKey = 'Y'
        super(X, self).__init__(**kwargs)

    Y = Y

class Statechart_1(TestStatechart):
    def __init__(self, **kwargs):
        kwargs['initialStateKey'] = 'A'
        super(Statechart_1, self).__init__(**kwargs)
      
    A = A
    B = B
    X = X

class C(TestState):
    def foo(self, *l):
        self.gotoState('D')

class D(TestState):
    def bar(self, *l):
        self.gotoState('C')

class Statechart_2(TestStatechart):
    def __init__(self, **kwargs):
        super(Statechart_2, self).__init__(**kwargs)
      
    C = C
    D = D

class E(TestState):
    def foo(self, *l):
        self.gotoState('F')

class F(TestState):
    def bar(self, *l):
        self.gotoState('E')

class Statechart_3(TestStatechart):
    def __init__(self, **kwargs):
        super(Statechart_3, self).__init__(**kwargs)

    E = E
    F = F

class StatechartOwnerTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global statechart_2
        global statechart_3
        global owner_1
        global owner_2
        global owner_3
        global rootState_1
        global rootState_2
        global rootState_3
        global state_A
        global state_B
        global state_C
        global state_D
        global state_E
        global state_F
        global state_X
        global state_Y
        global state_Z

        statechart_1 = Statechart_1()
        rootState_1 = statechart_1.rootStateInstance
        owner_1 = Owner_1()
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        state_X = statechart_1.getState('X')
        state_Y = statechart_1.getState('Y')
        state_X = statechart_1.getState('X')
        state_Z = statechart_1.getState('Z')
        
        owner_2 = Owner_2()
        statechart_2 = Statechart_2(owner=owner_2, initialStateKey='C')
        rootState_2 = statechart_2.rootStateInstance
        state_C = statechart_2.getState('C')
        state_D = statechart_2.getState('D')

        owner_3 = Owner_3()
        statechart_3 = Statechart_3(initialStateKey='E', statechartOwnerKey='fooOwner', fooOwner=owner_3)
        rootState_3 = statechart_3.rootStateInstance
        state_E = statechart_3.getState('E')
        state_F = statechart_3.getState('F')

    # Basic owner get and set
    def test_statechart_1(self):
        self.assertEqual(rootState_1.owner, statechart_1) 
        self.assertEqual(state_A.owner, statechart_1) 
        self.assertEqual(state_B.owner, statechart_1) 
        self.assertEqual(state_X.owner, statechart_1) 
        self.assertEqual(state_Y.owner, statechart_1) 
        self.assertEqual(state_Z.owner, statechart_1) 

        statechart_1.owner = owner_1

        self.assertEqual(rootState_1.owner, owner_1) 
        self.assertEqual(state_A.owner, owner_1) 
        self.assertEqual(state_B.owner, owner_1) 
        self.assertEqual(state_X.owner, owner_1) 
        self.assertEqual(state_Y.owner, owner_1) 
        self.assertEqual(state_Z.owner, owner_1) 

        statechart_1.owner = None

        self.assertEqual(rootState_1.owner, statechart_1) 
        self.assertEqual(state_A.owner, statechart_1) 
        self.assertEqual(state_B.owner, statechart_1) 
        self.assertEqual(state_X.owner, statechart_1) 
        self.assertEqual(state_Y.owner, statechart_1) 
        self.assertEqual(state_Z.owner, statechart_1) 

    # access owner via invokeStateMethod
    def test_state_A(self):
        self.assertTrue(state_A.isCurrentState())
        self.assertIsNone(state_A.accessedOwner)

        statechart_1.render()

        self.assertEqual(state_A.accessedOwner, statechart_1)

        state_A.reset()
        setattr(statechart_1, 'owner', owner_1)
        statechart_1.render()

        self.assertEqual(state_A.accessedOwner, owner_1)

    # access owner via invokeStateMethod
    def test_state_Z(self):
        statechart_1.gotoState('Z')
        self.assertTrue(state_Z.isCurrentState())
        self.assertIsNone(state_Z.accessedOwner)
  
        statechart_1.render()

        self.assertEqual(state_Z.accessedOwner, statechart_1)

        state_Z.reset()
        setattr(statechart_1, 'owner', owner_1)
        statechart_1.render()

        self.assertEqual(state_Z.accessedOwner, owner_1)

    # [PORT] This actually sets owner.
    # statechartOwnerKey
    def test_statechart_2(self):
        self.assertEqual(rootState_2.owner, owner_2)
        self.assertEqual(state_C.owner, owner_2)
        self.assertEqual(state_D.owner, owner_2)

        setattr(statechart_2, 'owner', None)

        self.assertEqual(rootState_2.owner, statechart_2)
        self.assertEqual(state_C.owner, statechart_2)
        self.assertEqual(state_D.owner, statechart_2)

    # basic owner get and set
    def test_statechart_3(self):
        self.assertEqual(statechart_3.statechartOwnerKey, 'fooOwner')
        self.assertEqual(statechart_3.fooOwner, owner_3)
  
        self.assertEqual(rootState_3.owner, owner_3)
        self.assertEqual(state_E.owner, owner_3)
        self.assertEqual(state_F.owner, owner_3)
  
        # [PORT] The javascript version had a dynamic system of observing the property with the
        #        name given by the value of statechartOwnerKey. However, in kivy-statechart, as of now,
        #        you can't just change fooOwner (it isn't being observed), you have to reset the
        #        statechartOwnerKey to trigger an update.
        #
        setattr(statechart_3, 'fooOwner', None)
        setattr(statechart_3, 'statechartOwnerKey', 'owner')
  
        self.assertEqual(rootState_3.owner, statechart_3)
        self.assertEqual(state_E.owner, statechart_3)
        self.assertEqual(state_F.owner, statechart_3)
  
        setattr(statechart_3, 'fooOwner', owner_3)
        setattr(statechart_3, 'statechartOwnerKey', 'fooOwner')
  
        self.assertEqual(rootState_3.owner, owner_3)
        self.assertEqual(state_E.owner, owner_3)
        self.assertEqual(state_F.owner, owner_3)
  
        # [PORT] How to do destroy in kivy? applicable?

        #ok(obj3.hasObserverFor('fooOwner'));
        #equals(rootState3.get('owner'), owner2);
  
        #obj3.destroy();
  
        #ok(!obj3.hasObserverFor('fooOwner'));
        #equals(rootState3.get('owner'), null);
