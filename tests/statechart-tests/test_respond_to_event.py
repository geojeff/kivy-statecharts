'''
Statechart tests, owner
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

# [PORT] Methods with fewer than 3 args, e.g. (self, context), (self, sender, context),
#        were given an additional catch-all *l, e.g. (self, context, *l).

class TestState(State):
    def __init__(self, **kwargs):
        self.returnValue = None
        self.handledEvent = False
        super(TestState, self).__init__(**kwargs)

    returnValue = ObjectProperty(None, allownone=True)
    handledEvent = BooleanProperty(False)
      
    def handleEvent(self, *l):
        setattr(self, 'handledEvent', True)
        return self.returnValue
      
    def reset(self, *l):
        setattr(self, 'returnValue', None)
        setattr(self, 'handledEvent', False)

class A(TestState):
    def __init__(self, **kwargs):
        super(A, self).__init__(**kwargs)

    def foo(self, sender, context, *l):
        return self.handleEvent()

class B(TestState):
    def __init__(self, **kwargs):
        super(B, self).__init__(**kwargs)

    def bar(self, sender, context, *l):
        return self.handleEvent()

    @State.eventHandler(['frozen', 'canuck']) 
    def eventHandler(self, event, sender, context):
        return self.handleEvent()

class C(TestState):
    def __init__(self, **kwargs):
        super(C, self).__init__(**kwargs)

    @State.eventHandler(['yes']) 
    def eventHandler_A(self, event, sender, context):
        return self.handleEvent()

    @State.eventHandler([re.compile('^num\d+')]) 
    def eventHandler_B(self, event, sender, context):
        return self.handleEvent()

class D(TestState):
    def __init__(self, **kwargs):
        super(D, self).__init__(**kwargs)

    def unknownEvent(self, event, sender, context):
        return self.handleEvent()

class F(TestState):
    def foo(self, context, *l):
        return self.handleEvent()

class E(TestState):
    def __init__(self, **kwargs):
        kwargs['initialSubstateKey'] = 'F'
        super(E, self).__init__(**kwargs)

    @State.eventHandler(['plus', 'minus']) 
    def eventHandler(self, event, sender, context):
        return self.handleEvent()

    F = F

class X(TestState):
    def yellow(self, context, *l):
        return self.handleEvent()

class Y(TestState):
    def orange(self, context, *l):
        return self.handleEvent()

class Z(TestState):
    def __init__(self, **kwargs):
        kwargs['substatesAreConcurrent'] = True
        super(Z, self).__init__(**kwargs)

    def blue(self, context, *l):
        return self.handleEvent()

    X = X
    Y = Y

class RootState(TestState):
    def __init__(self, **kwargs):
        kwargs['initialSubstateKey'] = 'A'
        super(RootState, self).__init__(**kwargs)
    
    A = A
    B = B
    C = C
    D = D
    E = E
    Z = Z

    def event_A(self, sender, context, *l):
        return self.handleEvent()
        
    @State.eventHandler(['event_B']) 
    def eventHandler(self, event, sender, context):
        return self.handleEvent()

class TestStatechart(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['rootState'] = RootState
        super(TestStatechart, self).__init__(**kwargs)

    someMethodInvoked = BooleanProperty(False)
    someMethodReturnValue = BooleanProperty(False)
      
    def someMethod(self, *l):
        setattr(self, 'someMethodInvoked', True)
        return self.someMethodReturnValue
      
class StatechartRespondToEventTestCase(unittest.TestCase):
    def setUp(self):
        global statechart
        global rootState
        global state_A
        global state_B
        global state_C
        global state_D
        global state_E
        global state_F
        global state_X
        global state_Y
        global state_Z

        statechart = TestStatechart()
        statechart.initStatechart()
        rootState = statechart.rootState
        state_A = statechart.getState('A')
        state_B = statechart.getState('B')
        state_C = statechart.getState('C')
        state_D = statechart.getState('D')
        state_E = statechart.getState('E')
        state_F = statechart.getState('F')
        state_X = statechart.getState('X')
        state_Y = statechart.getState('Y')
        state_X = statechart.getState('X')
        state_Z = statechart.getState('Z')
        
    def test_state_A(self):
        self.assertTrue(state_A.respondsToEvent('foo')) 
        self.assertFalse(state_A.respondsToEvent('foox')) 
        self.assertFalse(state_A.respondsToEvent('event_A')) 
        self.assertFalse(state_A.respondsToEvent('event_B')) 

        self.assertTrue(state_A.isCurrentState())

        self.assertTrue(statechart.respondsTo('foo')) 
        self.assertTrue(statechart.respondsTo('event_A')) 
        self.assertTrue(statechart.respondsTo('event_B')) 
        self.assertFalse(statechart.respondsTo('foox')) 
        self.assertFalse(statechart.respondsTo('event_C')) 

    def test_state_B(self):
        self.assertTrue(state_B.respondsToEvent('bar')) 
        self.assertTrue(state_B.respondsToEvent('frozen')) 
        self.assertTrue(state_B.respondsToEvent('canuck')) 
        self.assertFalse(state_B.respondsToEvent('canuckx')) 
        self.assertFalse(state_B.respondsToEvent('barx')) 
        self.assertFalse(state_B.respondsToEvent('event_A')) 
        self.assertFalse(state_B.respondsToEvent('event_B')) 
        self.assertFalse(state_B.respondsToEvent('canuckx')) 

        self.assertFalse(statechart.respondsTo('bar')) 
        self.assertFalse(statechart.respondsTo('frozen')) 
        self.assertFalse(statechart.respondsTo('canuck')) 

        statechart.gotoState('B')

        self.assertTrue(state_B.isCurrentState())
        self.assertTrue(statechart.respondsTo('bar')) 
        self.assertTrue(statechart.respondsTo('frozen')) 
        self.assertTrue(statechart.respondsTo('canuck')) 
        self.assertTrue(statechart.respondsTo('event_A')) 
        self.assertTrue(statechart.respondsTo('event_B')) 
        self.assertFalse(statechart.respondsTo('canuckx')) 
        self.assertFalse(statechart.respondsTo('foox')) 
        self.assertFalse(statechart.respondsTo('event_C')) 

    def test_state_C(self):
        self.assertTrue(state_C.respondsToEvent('yes')) 
        self.assertTrue(state_C.respondsToEvent('num1')) 
        self.assertTrue(state_C.respondsToEvent('num2')) 
        self.assertFalse(state_C.respondsToEvent('no')) 
        self.assertFalse(state_C.respondsToEvent('xnum1')) 
        self.assertFalse(state_C.respondsToEvent('event_A')) 
        self.assertFalse(state_C.respondsToEvent('event_B')) 

        self.assertFalse(statechart.respondsTo('yes')) 
        self.assertFalse(statechart.respondsTo('num1')) 
        self.assertFalse(statechart.respondsTo('num2')) 
  
        statechart.gotoState('C')

        self.assertTrue(state_C.isCurrentState())
        self.assertTrue(statechart.respondsTo('yes')) 
        self.assertTrue(statechart.respondsTo('num1')) 
        self.assertTrue(statechart.respondsTo('num2')) 
        self.assertTrue(statechart.respondsTo('event_A')) 
        self.assertTrue(statechart.respondsTo('event_B')) 
        self.assertFalse(statechart.respondsTo('no')) 
        self.assertFalse(statechart.respondsTo('xnum1')) 
        self.assertFalse(statechart.respondsTo('event_C')) 

    def test_state_D(self):
        self.assertTrue(state_D.respondsToEvent('foo')) 
        self.assertTrue(state_D.respondsToEvent('xyz')) 
        self.assertTrue(state_D.respondsToEvent('event_A')) 
        self.assertTrue(state_D.respondsToEvent('event_B')) 
  
        statechart.gotoState('D')

        self.assertTrue(state_D.isCurrentState())
        self.assertTrue(statechart.respondsTo('foo')) 
        self.assertTrue(statechart.respondsTo('xyz')) 
        self.assertTrue(statechart.respondsTo('event_A')) 
        self.assertTrue(statechart.respondsTo('event_B')) 
        self.assertTrue(statechart.respondsTo('event_C')) 

    def test_state_E_and_F(self):
        self.assertTrue(state_E.respondsToEvent('plus')) 
        self.assertTrue(state_E.respondsToEvent('minus')) 
        self.assertFalse(state_E.respondsToEvent('event_A')) 
        self.assertFalse(state_E.respondsToEvent('event_B')) 

        self.assertTrue(state_F.respondsToEvent('foo')) 
        self.assertFalse(state_F.respondsToEvent('plus')) 
        self.assertFalse(state_F.respondsToEvent('minus')) 

        self.assertFalse(statechart.respondsTo('plus'))
        self.assertFalse(statechart.respondsTo('minus'))
  
        statechart.gotoState('E')

        self.assertFalse(state_E.isCurrentState())
        self.assertTrue(state_F.isCurrentState())

        self.assertTrue(statechart.respondsTo('foo'))
        self.assertTrue(statechart.respondsTo('plus'))
        self.assertTrue(statechart.respondsTo('minus'))
        self.assertTrue(statechart.respondsTo('event_A'))
        self.assertTrue(statechart.respondsTo('event_B'))
        self.assertFalse(statechart.respondsTo('foox'))
        self.assertFalse(statechart.respondsTo('event_C'))

    def test_state_X_Y_and_Z(self):
        self.assertTrue(state_Z.respondsToEvent('blue')) 
        self.assertFalse(state_Z.respondsToEvent('yellow')) 
        self.assertFalse(state_Z.respondsToEvent('orange')) 

        self.assertFalse(state_X.respondsToEvent('blue')) 
        self.assertTrue(state_X.respondsToEvent('yellow')) 
        self.assertFalse(state_X.respondsToEvent('orange')) 

        self.assertFalse(state_Y.respondsToEvent('blue')) 
        self.assertFalse(state_Y.respondsToEvent('foo')) 
        self.assertTrue(state_Y.respondsToEvent('orange')) 

        self.assertFalse(statechart.respondsTo('blue')) 
        self.assertFalse(statechart.respondsTo('yellow')) 
        self.assertFalse(statechart.respondsTo('orange')) 

        statechart.gotoState('Z')

        self.assertFalse(state_Z.isCurrentState())
        self.assertTrue(state_X.isCurrentState())
        self.assertTrue(state_Y.isCurrentState())

        self.assertTrue(statechart.respondsTo('blue')) 
        self.assertTrue(statechart.respondsTo('yellow')) 
        self.assertTrue(statechart.respondsTo('orange')) 
        self.assertTrue(statechart.respondsTo('event_A')) 
        self.assertTrue(statechart.respondsTo('event_B')) 
        self.assertFalse(statechart.respondsTo('bluex')) 
        self.assertFalse(statechart.respondsTo('yellowx')) 
        self.assertFalse(statechart.respondsTo('orangex')) 
        self.assertFalse(statechart.respondsTo('event_C')) 

    def test_someMethod_on_current_states_A(self):
        self.assertTrue(statechart.respondsTo('someMethod')) 
        self.assertFalse(statechart.someMethodInvoked) 
        self.assertTrue(statechart.tryToPerform('someMethod')) 
        self.assertTrue(statechart.someMethodInvoked) 

        statechart.someMethodInvoked = False
        statechart.someMethodReturnValue = False

        self.assertTrue(statechart.respondsTo('someMethod')) 
        self.assertTrue(statechart.tryToPerform('someMethod'))  # [PORT] False in js, but comment says otherwise.
        self.assertTrue(statechart.someMethodInvoked) 

    def test_foo_on_current_states_A(self):
        self.assertTrue(statechart.tryToPerform('foo')) 
        self.assertTrue(state_A.handledEvent)
        self.assertFalse(rootState.handledEvent)

        state_A.reset()
        setattr(state_A, 'returnValue', False)

        self.assertFalse(statechart.tryToPerform('foo'))
        self.assertTrue(state_A.handledEvent)
        self.assertFalse(rootState.handledEvent)

    def test_foox_on_current_states_A(self):
        self.assertFalse(statechart.tryToPerform('foox')) 
        self.assertFalse(state_A.handledEvent)
        self.assertFalse(rootState.handledEvent)

    def test_event_A_on_current_states_A(self):
        self.assertTrue(statechart.tryToPerform('event_A')) 
        self.assertFalse(state_A.handledEvent)
        self.assertTrue(rootState.handledEvent)

        rootState.reset()
        setattr(rootState, 'returnValue', False)
        state_A.reset()

        self.assertFalse(statechart.tryToPerform('event_A'))
        self.assertFalse(state_A.handledEvent)
        self.assertTrue(rootState.handledEvent)

    def test_yes_on_current_states_C(self):
        statechart.gotoState('C')

        self.assertTrue(state_C.isCurrentState())

        self.assertTrue(statechart.tryToPerform('yes')) 
        self.assertTrue(state_C.handledEvent)
        self.assertFalse(rootState.handledEvent)

        state_C.reset()
        setattr(state_C, 'returnValue', False)

        self.assertFalse(statechart.tryToPerform('yes'))
        self.assertTrue(state_C.handledEvent)
        self.assertFalse(rootState.handledEvent)

    def test_num1_on_current_states_C(self):
        statechart.gotoState('C')

        self.assertTrue(state_C.isCurrentState())

        self.assertTrue(statechart.tryToPerform('num1')) 
        self.assertTrue(state_C.handledEvent)
        self.assertFalse(rootState.handledEvent)

        state_C.reset()
        setattr(state_C, 'returnValue', False)

        self.assertFalse(statechart.tryToPerform('num1'))
        self.assertTrue(state_C.handledEvent)
        self.assertFalse(rootState.handledEvent)

    def test_abc_on_current_states_D(self):
        statechart.gotoState('D')

        self.assertTrue(state_D.isCurrentState())

        self.assertTrue(statechart.tryToPerform('abc')) 
        self.assertTrue(state_D.handledEvent)
        self.assertFalse(rootState.handledEvent)

        state_D.reset()
        setattr(state_D, 'returnValue', False)

        self.assertFalse(statechart.tryToPerform('abc'))
        self.assertTrue(state_D.handledEvent)
        self.assertFalse(rootState.handledEvent)

    def test_yellow_on_current_states_X_and_Y(self):
        statechart.gotoState('Z')

        self.assertTrue(state_X.isCurrentState())
        self.assertTrue(state_Y.isCurrentState())

        self.assertTrue(statechart.tryToPerform('yellow')) 
        self.assertTrue(state_X.handledEvent)
        self.assertFalse(state_Y.handledEvent)
        self.assertFalse(state_Z.handledEvent)
        self.assertFalse(rootState.handledEvent)

        state_X.reset()
        setattr(state_X, 'returnValue', False)

        self.assertFalse(statechart.tryToPerform('yellow'))
        self.assertTrue(state_X.handledEvent)
        self.assertFalse(state_Y.handledEvent)
        self.assertFalse(state_Z.handledEvent)
        self.assertFalse(rootState.handledEvent)

