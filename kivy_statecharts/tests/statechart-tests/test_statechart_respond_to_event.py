'''
Statechart tests, owner
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

# [PORT] Methods with fewer than 3 args, e.g. (self, context), (self, sender, context),
#        were given an additional catch-all *l, e.g. (self, context, *l).

class TestState(State):
    def __init__(self, **kwargs):
        self.return_value = None
        self.handled_event = False
        super(TestState, self).__init__(**kwargs)

    return_value = ObjectProperty(None, allownone=True)
    handled_event = BooleanProperty(False)
      
    def handle_event(self, *l):
        setattr(self, 'handled_event', True)
        return self.return_value
      
    def reset(self, *l):
        setattr(self, 'return_value', None)
        setattr(self, 'handled_event', False)

class A(TestState):
    def __init__(self, **kwargs):
        super(A, self).__init__(**kwargs)

    def foo(self, sender, context, *l):
        return self.handle_event()

class B(TestState):
    def __init__(self, **kwargs):
        super(B, self).__init__(**kwargs)

    def bar(self, sender, context, *l):
        return self.handle_event()

    @State.event_handler(['frozen', 'canuck']) 
    def event_handler(self, event, sender, context):
        return self.handle_event()

class C(TestState):
    def __init__(self, **kwargs):
        super(C, self).__init__(**kwargs)

    @State.event_handler(['yes']) 
    def event_handler_A(self, event, sender, context):
        return self.handle_event()

    @State.event_handler([re.compile('^num\d+')]) 
    def event_handler_B(self, event, sender, context):
        return self.handle_event()

class D(TestState):
    def __init__(self, **kwargs):
        super(D, self).__init__(**kwargs)

    def unknown_event(self, event, sender, context):
        return self.handle_event()

class F(TestState):
    def foo(self, context, *l):
        return self.handle_event()

class E(TestState):
    def __init__(self, **kwargs):
        kwargs['initial_substate_key'] = 'F'
        super(E, self).__init__(**kwargs)

    @State.event_handler(['plus', 'minus']) 
    def event_handler(self, event, sender, context):
        return self.handle_event()

    F = F

class X(TestState):
    def yellow(self, context, *l):
        return self.handle_event()

class Y(TestState):
    def orange(self, context, *l):
        return self.handle_event()

class Z(TestState):
    def __init__(self, **kwargs):
        kwargs['substates_are_concurrent'] = True
        super(Z, self).__init__(**kwargs)

    def blue(self, context, *l):
        return self.handle_event()

    X = X
    Y = Y

class RootState(TestState):
    def __init__(self, **kwargs):
        kwargs['initial_substate_key'] = 'A'
        super(RootState, self).__init__(**kwargs)
    
    A = A
    B = B
    C = C
    D = D
    E = E
    Z = Z

    def event_A(self, sender, context, *l):
        return self.handle_event()
        
    @State.event_handler(['event_B']) 
    def event_handler(self, event, sender, context):
        return self.handle_event()

class TestStatechart(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['root_state_class'] = RootState
        super(TestStatechart, self).__init__(**kwargs)

    some_method_invoked = BooleanProperty(False)
    some_method_return_value = BooleanProperty(False)
      
    def some_method(self, *l):
        setattr(self, 'some_method_invoked', True)
        return self.some_method_return_value
      
class StatechartRespondToEventTestCase(unittest.TestCase):
    def setUp(self):
        global statechart
        global root_state
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
        statechart.init_statechart()
        root_state = statechart.root_state_instance
        state_A = statechart.get_state('A')
        state_B = statechart.get_state('B')
        state_C = statechart.get_state('C')
        state_D = statechart.get_state('D')
        state_E = statechart.get_state('E')
        state_F = statechart.get_state('F')
        state_X = statechart.get_state('X')
        state_Y = statechart.get_state('Y')
        state_X = statechart.get_state('X')
        state_Z = statechart.get_state('Z')
        
    def test_state_A(self):
        self.assertTrue(state_A.responds_to_event('foo')) 
        self.assertFalse(state_A.responds_to_event('foox')) 
        self.assertFalse(state_A.responds_to_event('event_A')) 
        self.assertFalse(state_A.responds_to_event('event_B')) 

        self.assertTrue(state_A.is_current_state())

        self.assertTrue(statechart.responds_to('foo')) 
        self.assertTrue(statechart.responds_to('event_A')) 
        self.assertTrue(statechart.responds_to('event_B')) 
        self.assertFalse(statechart.responds_to('foox')) 
        self.assertFalse(statechart.responds_to('event_C')) 

    def test_state_B(self):
        self.assertTrue(state_B.responds_to_event('bar')) 
        self.assertTrue(state_B.responds_to_event('frozen')) 
        self.assertTrue(state_B.responds_to_event('canuck')) 
        self.assertFalse(state_B.responds_to_event('canuckx')) 
        self.assertFalse(state_B.responds_to_event('barx')) 
        self.assertFalse(state_B.responds_to_event('event_A')) 
        self.assertFalse(state_B.responds_to_event('event_B')) 
        self.assertFalse(state_B.responds_to_event('canuckx')) 

        self.assertFalse(statechart.responds_to('bar')) 
        self.assertFalse(statechart.responds_to('frozen')) 
        self.assertFalse(statechart.responds_to('canuck')) 

        statechart.go_to_state('B')

        self.assertTrue(state_B.is_current_state())
        self.assertTrue(statechart.responds_to('bar')) 
        self.assertTrue(statechart.responds_to('frozen')) 
        self.assertTrue(statechart.responds_to('canuck')) 
        self.assertTrue(statechart.responds_to('event_A')) 
        self.assertTrue(statechart.responds_to('event_B')) 
        self.assertFalse(statechart.responds_to('canuckx')) 
        self.assertFalse(statechart.responds_to('foox')) 
        self.assertFalse(statechart.responds_to('event_C')) 

    def test_state_C(self):
        self.assertTrue(state_C.responds_to_event('yes')) 
        self.assertTrue(state_C.responds_to_event('num1')) 
        self.assertTrue(state_C.responds_to_event('num2')) 
        self.assertFalse(state_C.responds_to_event('no')) 
        self.assertFalse(state_C.responds_to_event('xnum1')) 
        self.assertFalse(state_C.responds_to_event('event_A')) 
        self.assertFalse(state_C.responds_to_event('event_B')) 

        self.assertFalse(statechart.responds_to('yes')) 
        self.assertFalse(statechart.responds_to('num1')) 
        self.assertFalse(statechart.responds_to('num2')) 
  
        statechart.go_to_state('C')

        self.assertTrue(state_C.is_current_state())
        self.assertTrue(statechart.responds_to('yes')) 
        self.assertTrue(statechart.responds_to('num1')) 
        self.assertTrue(statechart.responds_to('num2')) 
        self.assertTrue(statechart.responds_to('event_A')) 
        self.assertTrue(statechart.responds_to('event_B')) 
        self.assertFalse(statechart.responds_to('no')) 
        self.assertFalse(statechart.responds_to('xnum1')) 
        self.assertFalse(statechart.responds_to('event_C')) 

    def test_state_D(self):
        self.assertTrue(state_D.responds_to_event('foo')) 
        self.assertTrue(state_D.responds_to_event('xyz')) 
        self.assertTrue(state_D.responds_to_event('event_A')) 
        self.assertTrue(state_D.responds_to_event('event_B')) 
  
        statechart.go_to_state('D')

        self.assertTrue(state_D.is_current_state())
        self.assertTrue(statechart.responds_to('foo')) 
        self.assertTrue(statechart.responds_to('xyz')) 
        self.assertTrue(statechart.responds_to('event_A')) 
        self.assertTrue(statechart.responds_to('event_B')) 
        self.assertTrue(statechart.responds_to('event_C')) 

    def test_state_E_and_F(self):
        self.assertTrue(state_E.responds_to_event('plus')) 
        self.assertTrue(state_E.responds_to_event('minus')) 
        self.assertFalse(state_E.responds_to_event('event_A')) 
        self.assertFalse(state_E.responds_to_event('event_B')) 

        self.assertTrue(state_F.responds_to_event('foo')) 
        self.assertFalse(state_F.responds_to_event('plus')) 
        self.assertFalse(state_F.responds_to_event('minus')) 

        self.assertFalse(statechart.responds_to('plus'))
        self.assertFalse(statechart.responds_to('minus'))
  
        statechart.go_to_state('E')

        self.assertFalse(state_E.is_current_state())
        self.assertTrue(state_F.is_current_state())

        self.assertTrue(statechart.responds_to('foo'))
        self.assertTrue(statechart.responds_to('plus'))
        self.assertTrue(statechart.responds_to('minus'))
        self.assertTrue(statechart.responds_to('event_A'))
        self.assertTrue(statechart.responds_to('event_B'))
        self.assertFalse(statechart.responds_to('foox'))
        self.assertFalse(statechart.responds_to('event_C'))

    def test_state_X_Y_and_Z(self):
        self.assertTrue(state_Z.responds_to_event('blue')) 
        self.assertFalse(state_Z.responds_to_event('yellow')) 
        self.assertFalse(state_Z.responds_to_event('orange')) 

        self.assertFalse(state_X.responds_to_event('blue')) 
        self.assertTrue(state_X.responds_to_event('yellow')) 
        self.assertFalse(state_X.responds_to_event('orange')) 

        self.assertFalse(state_Y.responds_to_event('blue')) 
        self.assertFalse(state_Y.responds_to_event('foo')) 
        self.assertTrue(state_Y.responds_to_event('orange')) 

        self.assertFalse(statechart.responds_to('blue')) 
        self.assertFalse(statechart.responds_to('yellow')) 
        self.assertFalse(statechart.responds_to('orange')) 

        statechart.go_to_state('Z')

        self.assertFalse(state_Z.is_current_state())
        self.assertTrue(state_X.is_current_state())
        self.assertTrue(state_Y.is_current_state())

        self.assertTrue(statechart.responds_to('blue')) 
        self.assertTrue(statechart.responds_to('yellow')) 
        self.assertTrue(statechart.responds_to('orange')) 
        self.assertTrue(statechart.responds_to('event_A')) 
        self.assertTrue(statechart.responds_to('event_B')) 
        self.assertFalse(statechart.responds_to('bluex')) 
        self.assertFalse(statechart.responds_to('yellowx')) 
        self.assertFalse(statechart.responds_to('orangex')) 
        self.assertFalse(statechart.responds_to('event_C')) 

    def test_some_method_on_current_states_A(self):
        self.assertTrue(statechart.responds_to('some_method')) 
        self.assertFalse(statechart.some_method_invoked) 
        self.assertTrue(statechart.try_to_perform('some_method')) 
        self.assertTrue(statechart.some_method_invoked) 

        statechart.some_method_invoked = False
        statechart.some_method_return_value = False

        self.assertTrue(statechart.responds_to('some_method')) 
        self.assertTrue(statechart.try_to_perform('some_method'))  # [PORT] False in js, but comment says otherwise.
        self.assertTrue(statechart.some_method_invoked) 

    def test_foo_on_current_states_A(self):
        self.assertTrue(statechart.try_to_perform('foo')) 
        self.assertTrue(state_A.handled_event)
        self.assertFalse(root_state.handled_event)

        state_A.reset()
        setattr(state_A, 'return_value', False)

        self.assertFalse(statechart.try_to_perform('foo'))
        self.assertTrue(state_A.handled_event)
        self.assertFalse(root_state.handled_event)

    def test_foox_on_current_states_A(self):
        self.assertFalse(statechart.try_to_perform('foox')) 
        self.assertFalse(state_A.handled_event)
        self.assertFalse(root_state.handled_event)

    def test_event_A_on_current_states_A(self):
        self.assertTrue(statechart.try_to_perform('event_A')) 
        self.assertFalse(state_A.handled_event)
        self.assertTrue(root_state.handled_event)

        root_state.reset()
        setattr(root_state, 'return_value', False)
        state_A.reset()

        self.assertFalse(statechart.try_to_perform('event_A'))
        self.assertFalse(state_A.handled_event)
        self.assertTrue(root_state.handled_event)

    def test_yes_on_current_states_C(self):
        statechart.go_to_state('C')

        self.assertTrue(state_C.is_current_state())

        self.assertTrue(statechart.try_to_perform('yes')) 
        self.assertTrue(state_C.handled_event)
        self.assertFalse(root_state.handled_event)

        state_C.reset()
        setattr(state_C, 'return_value', False)

        self.assertFalse(statechart.try_to_perform('yes'))
        self.assertTrue(state_C.handled_event)
        self.assertFalse(root_state.handled_event)

    def test_num1_on_current_states_C(self):
        statechart.go_to_state('C')

        self.assertTrue(state_C.is_current_state())

        self.assertTrue(statechart.try_to_perform('num1')) 
        self.assertTrue(state_C.handled_event)
        self.assertFalse(root_state.handled_event)

        state_C.reset()
        setattr(state_C, 'return_value', False)

        self.assertFalse(statechart.try_to_perform('num1'))
        self.assertTrue(state_C.handled_event)
        self.assertFalse(root_state.handled_event)

    def test_abc_on_current_states_D(self):
        statechart.go_to_state('D')

        self.assertTrue(state_D.is_current_state())

        self.assertTrue(statechart.try_to_perform('abc')) 
        self.assertTrue(state_D.handled_event)
        self.assertFalse(root_state.handled_event)

        state_D.reset()
        setattr(state_D, 'return_value', False)

        self.assertFalse(statechart.try_to_perform('abc'))
        self.assertTrue(state_D.handled_event)
        self.assertFalse(root_state.handled_event)

    def test_yellow_on_current_states_X_and_Y(self):
        statechart.go_to_state('Z')

        self.assertTrue(state_X.is_current_state())
        self.assertTrue(state_Y.is_current_state())

        self.assertTrue(statechart.try_to_perform('yellow')) 
        self.assertTrue(state_X.handled_event)
        self.assertFalse(state_Y.handled_event)
        self.assertFalse(state_Z.handled_event)
        self.assertFalse(root_state.handled_event)

        state_X.reset()
        setattr(state_X, 'return_value', False)

        self.assertFalse(statechart.try_to_perform('yellow'))
        self.assertTrue(state_X.handled_event)
        self.assertFalse(state_Y.handled_event)
        self.assertFalse(state_Z.handled_event)
        self.assertFalse(root_state.handled_event)

