'''
Statechart tests, advanced event handling, without concurrent states
====================================================================
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class TestState(State):
    event = ObjectProperty(None, allownone=True)
    sender = ObjectProperty(None, allownone=True)
    context = ObjectProperty(None, allownone=True)
    handler = ObjectProperty(None, allownone=True)
      
    def _handled_event(self, handler, event, sender, context):
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
        kwargs['root_state_class'] = self.RootState
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(TestState):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        def foo(self, sender, context):
            self._handled_event('foo', None, sender, context)
 
        @State.event_handler(['plus', 'minus', 'multiply', 'divide']) 
        def event_handler_A(self, event, sender, context):
            self._handled_event('event_handler_A', event, sender, context)

        @State.event_handler([re.compile('num\d')]) 
        def event_handler_B(self, event, sender, context):
            self._handled_event('event_handler_B', event, sender, context)

        def unknown_event(self, event, sender, context):
            self._handled_event('unknown_event', event, sender, context)

        class A(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.B, self).__init__(**kwargs)


class Statechart_2(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['root_state_class'] = self.RootState
        super(Statechart_2, self).__init__(**kwargs)

    class RootState(TestState):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_2.RootState, self).__init__(**kwargs)

        def foo(self, sender, context):
            self._handled_event('foo', None, sender, context)
 
        class A(State):
            def __init__(self, **kwargs):
                super(Statechart_2.RootState.A, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                super(Statechart_2.RootState.B, self).__init__(**kwargs)


class Statechart_3(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['root_state_class'] = self.RootState
        super(Statechart_3, self).__init__(**kwargs)

    class RootState(TestState):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_3.RootState, self).__init__(**kwargs)

        @State.event_handler([re.compile('num\d'), 'decimal']) 
        def event_handler_A(self, event, sender, context):
            self._handled_event('event_handler_A', event, sender, context)

        @State.event_handler([re.compile('foo'), re.compile('bar')]) 
        def event_handler_B(self, event, sender, context):
            self._handled_event('event_handler_B', event, sender, context)

        class A(State):
            def __init__(self, **kwargs):
                super(Statechart_3.RootState.A, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                super(Statechart_3.RootState.B, self).__init__(**kwargs)


class Statechart_4(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['root_state_class'] = self.RootState
        super(Statechart_4, self).__init__(**kwargs)

    class RootState(TestState):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_4.RootState, self).__init__(**kwargs)

        def foo(self, sender, context):
            self._handled_event('foo', None, sender, context)
 
        @State.event_handler(['yes', 'no']) 
        def event_handler_Root(self, event, sender, context):
            self._handled_event('event_handler_Root', event, sender, context)

        def unknown_event(self, event, sender, context):
            self._handled_event('unknown_event', event, sender, context)
        
        class A(TestState):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'B'
                super(Statechart_4.RootState.A, self).__init__(**kwargs)

            def bar(self, sender, context):
                self._handled_event('bar', None, sender, context)
 
            @State.event_handler(['frozen', 'canuck']) 
            def event_handler_A(self, event, sender, context):
                self._handled_event('event_handler_A', event, sender, context)

            class B(TestState):
                def __init__(self, **kwargs):
                    super(Statechart_4.RootState.A.B, self).__init__(**kwargs)
    
                def cat(self, sender, context):
                    self._handled_event('cat', None, sender, context)
     
                @State.event_handler([re.compile('apple'), re.compile('orange')]) 
                def event_handler_B(self, event, sender, context):
                    self._handled_event('event_handler_B', event, sender, context)


class StateEventHandlingAdvancedWithoutConcurrentTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global root_state_1
        global statechart_2
        global root_state_2
        global statechart_3
        global root_state_3
        global statechart_4
        global root_state_4
        global state_A
        global state_B

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        statechart_2 = Statechart_2()
        statechart_2.init_statechart()
        root_state_2 = statechart_2.root_state_instance
        statechart_3 = Statechart_3()
        statechart_3.init_statechart()
        root_state_3 = statechart_3.root_state_instance
        statechart_4 = Statechart_4()
        statechart_4.init_statechart()
        root_state_4 = statechart_4.root_state_instance
        state_A = statechart_4.get_state('A')
        state_B = statechart_4.get_state('B')

    # Check statechart_1 event handling
    def test_statechart_1_event_handling(self):
        class Sender:
            pass
        class Context:
            pass
        sender = Sender()
        context = Context()

        root_state_1.reset();
        statechart_1.send_event('foo', sender, context)
        self.assertEqual(root_state_1.handler, 'foo')
        self.assertEqual(root_state_1.event, None)
        self.assertEqual(root_state_1.sender, sender)
        self.assertEqual(root_state_1.context, context)

        root_state_1.reset();
        statechart_1.send_event('plus', sender, context)
        self.assertEqual(root_state_1.handler, 'event_handler_A')
        self.assertEqual(root_state_1.event, 'plus')
        self.assertEqual(root_state_1.sender, sender)
        self.assertEqual(root_state_1.context, context)

        root_state_1.reset();
        statechart_1.send_event('divide', sender, context)
        self.assertEqual(root_state_1.handler, 'event_handler_A')
        self.assertEqual(root_state_1.event, 'divide')
        self.assertEqual(root_state_1.sender, sender)
        self.assertEqual(root_state_1.context, context)

        root_state_1.reset();
        statechart_1.send_event('num1', sender, context)
        self.assertEqual(root_state_1.handler, 'event_handler_B')
        self.assertEqual(root_state_1.event, 'num1')
        self.assertEqual(root_state_1.sender, sender)
        self.assertEqual(root_state_1.context, context)

        root_state_1.reset();
        statechart_1.send_event('bar', sender, context)
        self.assertEqual(root_state_1.handler, 'unknown_event')
        self.assertEqual(root_state_1.event, 'bar')
        self.assertEqual(root_state_1.sender, sender)
        self.assertEqual(root_state_1.context, context)

    # Check statechart_2 event handling
    def test_statechart_2_event_handling(self):
        class Sender:
            pass
        class Context:
            pass
        sender = Sender()
        context = Context()

        root_state_2.reset();
        statechart_2.send_event('foo', sender, context)
        self.assertEqual(root_state_2.handler, 'foo')
        self.assertEqual(root_state_2.event, None)
        self.assertEqual(root_state_2.sender, sender)
        self.assertEqual(root_state_2.context, context)

        root_state_2.reset();
        statechart_2.send_event('bar', sender, context)
        self.assertEqual(root_state_2.handler, None)
        self.assertEqual(root_state_2.event, None)
        self.assertEqual(root_state_2.sender, None)
        self.assertEqual(root_state_2.context, None)

    # Check statechart_3 event handling
    def test_statechart_3_event_handling(self):
        root_state_3.reset();
        statechart_3.send_event('num2')
        self.assertEqual(root_state_3.handler, 'event_handler_A')
        self.assertEqual(root_state_3.event, 'num2')

        root_state_3.reset();
        statechart_3.send_event('decimal')
        self.assertEqual(root_state_3.handler, 'event_handler_A')
        self.assertEqual(root_state_3.event, 'decimal')

        root_state_3.reset();
        statechart_3.send_event('foo')
        self.assertEqual(root_state_3.handler, 'event_handler_B')
        self.assertEqual(root_state_3.event, 'foo')

        root_state_3.reset();
        statechart_3.send_event('bar')
        self.assertEqual(root_state_3.handler, 'event_handler_B')
        self.assertEqual(root_state_3.event, 'bar')

    # Check statechart_4 event handling
    def test_statechart_4_event_handling(self):
        root_state_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.send_event('foo')
        self.assertEqual(root_state_4.handler, 'foo')
        self.assertEqual(root_state_4.event, None)
        self.assertEqual(state_A.handler, None)
        self.assertEqual(state_A.event, None)
        self.assertEqual(state_B.handler, None)
        self.assertEqual(state_B.event, None)

        root_state_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.send_event('yes')
        self.assertEqual(root_state_4.handler, 'event_handler_Root')
        self.assertEqual(root_state_4.event, 'yes')
        self.assertEqual(state_A.handler, None)
        self.assertEqual(state_A.event, None)
        self.assertEqual(state_B.handler, None)
        self.assertEqual(state_B.event, None)

        root_state_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.send_event('xyz')
        self.assertEqual(root_state_4.handler, 'unknown_event')
        self.assertEqual(root_state_4.event, 'xyz')
        self.assertEqual(state_A.handler, None)
        self.assertEqual(state_A.event, None)
        self.assertEqual(state_B.handler, None)
        self.assertEqual(state_B.event, None)

        root_state_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.send_event('bar')
        self.assertEqual(root_state_4.handler, None)
        self.assertEqual(root_state_4.event, None)
        self.assertEqual(state_A.handler, 'bar')
        self.assertEqual(state_A.event, None)
        self.assertEqual(state_B.handler, None)
        self.assertEqual(state_B.event, None)

        root_state_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.send_event('canuck')
        self.assertEqual(root_state_4.handler, None)
        self.assertEqual(root_state_4.event, None)
        self.assertEqual(state_A.handler, 'event_handler_A')
        self.assertEqual(state_A.event, 'canuck')
        self.assertEqual(state_B.handler, None)
        self.assertEqual(state_B.event, None)

        root_state_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.send_event('cat')
        self.assertEqual(root_state_4.handler, None)
        self.assertEqual(root_state_4.event, None)
        self.assertEqual(state_A.handler, None)
        self.assertEqual(state_A.event, None)
        self.assertEqual(state_B.handler, 'cat')
        self.assertEqual(state_B.event, None)

        root_state_4.reset();
        state_A.reset();
        state_B.reset();
        statechart_4.send_event('orange')
        self.assertEqual(root_state_4.handler, None)
        self.assertEqual(root_state_4.event, None)
        self.assertEqual(state_A.handler, None)
        self.assertEqual(state_A.event, None)
        self.assertEqual(state_B.handler, 'event_handler_B')
        self.assertEqual(state_B.event, 'orange')

    # Check for bad handler in statechart_5
    def test_for_bad_handler(self):
        class BadState(TestState):
            def __init__(self, **kwargs):
                kwargs['name'] = 'bad_state'  # name needed for test
                super(BadState, self).__init__(**kwargs)
    
            # Only event types allowed are strings and regexes.
            @State.event_handler(['yes', 'no', dict]) 
            def bad_event_handler(self, event, sender, context):
                pass

        bad = BadState()

        with self.assertRaises(Exception) as cm:
            bad.init_state()

        msg = ("Invalid event {0} for event handler {1} in "
               "state {1}").format(dict, 'bad_event_handler', bad)
        self.assertEqual(str(cm.exception), msg)


