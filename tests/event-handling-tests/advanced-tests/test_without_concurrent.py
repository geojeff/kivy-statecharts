'''
Statechart tests, advanced event handling, without concurrent states
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

class TestState(State):
    event = ObjectProperty(None)
    sender = ObjectProperty(None)
    context = ObjectProperty(None)
    handler = ObjectProperty(None)
      
    def _handledEvent(self, handler, event, sender, context):
        setattr(self, 'handler', handler);
        setattr(self, 'event', event);
        setattr(self, 'sender', sender);
        setattr(self, 'context', context);
      
    def reset(self):
        setattr(self, 'handler', None);
        setattr(self, 'event', None);
        setattr(self, 'sender', None);
        setattr(self, 'context', None);

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['rootStateClass'] = self.RootState
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(TestState):
        def __init__(self, **kwargs):
            super(Statechart_1.RootState, self).__init__(**kwargs)

        def foo(self, context):
            self._handledEvent('foo', None, sender, context)
 
        @State.eventHandler(['plus', 'minus', 'multiply', 'divide']) 
        def eventHandler_A(self, event, sender, context):
            self._handledEvent('eventHandler_A', event, sender, context)

        @State.eventHandler([re.compile('num\d')]) 
        def eventHandler_B(self, event, sender, context):
            self._handledEvent('eventHandler_B', event, sender, context)

        def unknownEvent(self, event, sender, context):
            self._handledEvent('unknownEvent', event, sender, context)
        
class Statechart_2(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['rootStateClass'] = self.RootState
        super(Statechart_2, self).__init__(**kwargs)

    class RootState(TestState):
        def __init__(self, **kwargs):
            super(Statechart_2.RootState, self).__init__(**kwargs)

        def foo(self, context):
            self._handledEvent('foo', None, sender, context)
 
class Statechart_3(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['rootStateClass'] = self.RootState
        super(Statechart_3, self).__init__(**kwargs)

    class RootState(TestState):
        def __init__(self, **kwargs):
            super(Statechart_3.RootState, self).__init__(**kwargs)

        @State.eventHandler([re.compile('num\d'), 'decimal']) 
        def eventHandler_A(self, event, sender, context):
            self._handledEvent('eventHandler_A', event, sender, context)

        @State.eventHandler([re.compile('foo'), re.compile('bar')]) 
        def eventHandler_B(self, event, sender, context):
            self._handledEvent('eventHandler_B', event, sender, context)

class Statechart_4(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['rootStateClass'] = self.RootState
        super(Statechart_4, self).__init__(**kwargs)

    class RootState(TestState):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
            super(Statechart_4.RootState, self).__init__(**kwargs)

        def foo(self, context):
            self._handledEvent('foo', None, sender, context)
 
        @State.eventHandler(['yes', 'no']) 
        def eventHandler_Root(self, event, sender, context):
            self._handledEvent('eventHandler_Root', event, sender, context)

        def unknownEvent(self, event, sender, context):
            self._handledEvent('unknownEvent', event, sender, context)
        
        class A(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'B'
                super(Statechart_4.RootState.A, self).__init__(**kwargs)

            def bar(self, context):
                self._handledEvent('bar', None, sender, context)
 
            @State.eventHandler(['frozen', 'canuck']) 
            def eventHandler_A(self, event, sender, context):
                self._handledEvent('eventHandler_A', event, sender, context)

            class B(State):
                def __init__(self, **kwargs):
                    super(Statechart_4.RootState.A.B, self).__init__(**kwargs)
    
                def cat(self, context):
                    self._handledEvent('cat', None, sender, context)
     
                @State.eventHandler([re.compile('apple'), re.compile('orange')]) 
                def eventHandler_B(self, event, sender, context):
                    self._handledEvent('eventHandler_B', event, sender, context)

class StateEventHandlingAdvancedWithoutConcurrentTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global rootState_1
        global statechart_2
        global rootState_2
        global statechart_3
        global rootState_3
        global statechart_4
        global rootState_4
        global state_A
        global state_B

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootStateInstance
        statechart_2 = Statechart_2()
        statechart_2.initStatechart()
        rootState_2 = statechart_2.rootStateInstance
        statechart_3 = Statechart_3()
        statechart_3.initStatechart()
        rootState_3 = statechart_3.rootStateInstance
        statechart_4 = Statechart_4()
        statechart_4.initStatechart()
        rootState_4 = statechart_4.rootStateInstance
        state_A = statechart_4.getState('A')
        state_B = statechart_4.getState('B')

    # Check statechart_1 event handling
    def check_statechart_1_event_handling(self):
        class Sender:
            pass
        class Context:
            pass
        sender = Sender()
        context = Context()

        rootState_1.reset();
        statechart_1.sendEvent('foo', sender, context)
        self.assertEqual(rootState_1.handler, 'foo')
        self.assertEqual(rootState_1.event, None)
        self.assertEqual(rootState_1.sender, sender)
        self.assertEqual(rootState_1.context, context)

        rootState_1.reset();
        statechart_1.sendEvent('plus', sender, context)
        self.assertEqual(rootState_1.handler, 'eventHandler_A')
        self.assertEqual(rootState_1.event, 'plus')
        self.assertEqual(rootState_1.sender, sender)
        self.assertEqual(rootState_1.context, context)

        rootState_1.reset();
        statechart_1.sendEvent('divide', sender, context)
        self.assertEqual(rootState_1.handler, 'eventHandler_A')
        self.assertEqual(rootState_1.event, 'divide')
        self.assertEqual(rootState_1.sender, sender)
        self.assertEqual(rootState_1.context, context)

        rootState_1.reset();
        statechart_1.sendEvent('num1', sender, context)
        self.assertEqual(rootState_1.handler, 'eventHandler_B')
        self.assertEqual(rootState_1.event, 'num1')
        self.assertEqual(rootState_1.sender, sender)
        self.assertEqual(rootState_1.context, context)

        rootState_1.reset();
        statechart_1.sendEvent('bar', sender, context)
        self.assertEqual(rootState_1.handler, 'unknownEvent')
        self.assertEqual(rootState_1.event, 'bar')
        self.assertEqual(rootState_1.sender, sender)
        self.assertEqual(rootState_1.context, context)

    # Check statechart_2 event handling
    def check_statechart_2_event_handling(self):
        class Sender:
            pass
        class Contect:
            pass
        sender = Sender()
        context = Context()

        rootState_2.reset();
        statechart_2.sendEvent('foo', sender, context)
        self.assertEqual(rootState_2.handler, 'foo')
        self.assertEqual(rootState_2.event, None)
        self.assertEqual(rootState_2.sender, sender)
        self.assertEqual(rootState_2.context, context)

        rootState_2.reset();
        statechart_2.sendEvent('bar', sender, context)
        self.assertEqual(rootState_2.handler, None)
        self.assertEqual(rootState_2.event, None)
        self.assertEqual(rootState_2.sender, None)
        self.assertEqual(rootState_2.context, None)

    # Check statechart_3 event handling
    def check_statechart_3_event_handling(self):
        rootState_3.reset();
        statechart_3.sendEvent('num2')
        self.assertEqual(rootState_3.handler, 'eventHandler_A')
        self.assertEqual(rootState_3.event, 'num2')

        rootState_3.reset();
        statechart_3.sendEvent('decimal')
        self.assertEqual(rootState_3.handler, 'eventHandler_A')
        self.assertEqual(rootState_3.event, 'decimal')

        rootState_3.reset();
        statechart_3.sendEvent('foo')
        self.assertEqual(rootState_3.handler, 'eventHandler_B')
        self.assertEqual(rootState_3.event, 'foo')

        rootState_3.reset();
        statechart_3.sendEvent('bar')
        self.assertEqual(rootState_3.handler, 'eventHandler_B')
        self.assertEqual(rootState_3.event, 'bar')

    # Check statechart_4 event handling
    def check_statechart_4_event_handling(self):
        rootState_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.sendEvent('foo')
        self.assertEqual(rootState_4.handler, 'foo')
        self.assertEqual(rootState_4.event, None)
        self.assertEqual(state_A.handler, None)
        self.assertEqual(state_A.event, None)
        self.assertEqual(state_B.handler, None)
        self.assertEqual(state_B.event, None)

        rootState_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.sendEvent('yes')
        self.assertEqual(rootState_4.handler, 'eventHandler_Root')
        self.assertEqual(rootState_4.event, 'yes')
        self.assertEqual(state_A.handler, None)
        self.assertEqual(state_A.event, None)
        self.assertEqual(state_B.handler, None)
        self.assertEqual(state_B.event, None)

        rootState_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.sendEvent('xyz')
        self.assertEqual(rootState_4.handler, 'unknownEvent')
        self.assertEqual(rootState_4.event, 'xyz')
        self.assertEqual(state_A.handler, None)
        self.assertEqual(state_A.event, None)
        self.assertEqual(state_B.handler, None)
        self.assertEqual(state_B.event, None)

        rootState_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.sendEvent('bar')
        self.assertEqual(rootState_4.handler, None)
        self.assertEqual(rootState_4.event, None)
        self.assertEqual(state_A.handler, 'bar')
        self.assertEqual(state_A.event, None)
        self.assertEqual(state_B.handler, None)
        self.assertEqual(state_B.event, None)

        rootState_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.sendEvent('canuck')
        self.assertEqual(rootState_4.handler, None)
        self.assertEqual(rootState_4.event, None)
        self.assertEqual(state_A.handler, 'eventHandler_A')
        self.assertEqual(state_A.event, 'canuck')
        self.assertEqual(state_B.handler, None)
        self.assertEqual(state_B.event, None)

        rootState_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.sendEvent('cat')
        self.assertEqual(rootState_4.handler, None)
        self.assertEqual(rootState_4.event, None)
        self.assertEqual(state_A.handler, None)
        self.assertEqual(state_A.event, None)
        self.assertEqual(state_B.handler, 'cat')
        self.assertEqual(state_B.event, None)

        rootState_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.sendEvent('orange')
        self.assertEqual(rootState_4.handler, None)
        self.assertEqual(rootState_4.event, None)
        self.assertEqual(state_A.handler, None)
        self.assertEqual(state_A.event, None)
        self.assertEqual(state_B.handler, 'eventHandler_B')
        self.assertEqual(state_B.event, 'orange')





