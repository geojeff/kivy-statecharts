'''
Statechart tests, try to handle event
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, DictProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    state_will_try_to_handle_event_info = DictProperty({})
    state_did_try_to_handle_event_info = DictProperty({})

    def __init__(self, **kwargs):
        kwargs['initial_state_key'] = 'FOO'
        super(Statechart_1, self).__init__(**kwargs)

    def state_will_try_to_handle_event(self, state, event, handler):
        self.state_will_try_to_handle_event_info = {
          'state': state,
          'event': event,
          'handler': handler
        }

    def state_did_try_to_handle_event(self, state, event, handler, handled):
        self.state_did_try_to_handle_event_info = {
          'state': state,
          'event': event,
          'handler': handler,
          'handled': handled
        }

    class FOO(State):
        event_handler_return_value = BooleanProperty(False)
        handled_event_info = DictProperty({})

        def __init__(self, **kwargs):
            kwargs['event_handler_return_value'] = True
            super(Statechart_1.FOO, self).__init__(**kwargs)

        def _notify_handled_event(self, handler, event, arg1, arg2):
            self.handled_event_info = {
                'handler': handler,
                'event': event,
                'arg1': arg1,
                'arg2': arg2
            }
 
        @State.event_handler(['event1']) 
        def event_handler1(self, event, arg1, arg2):
            self._notify_handled_event('event_handler1', 'event1', arg1, arg2)
            return self.event_handler_return_value
        
        @State.event_handler(['event2'])
        def event_handler2(self, event, arg1, arg2):
            self._notify_handled_event('event_handler2', event, arg1, arg2)
            return self.event_handler_return_value
        
        @State.event_handler([re.compile('^digit[0-9]$')])
        def event_handler3(self, event, arg1, arg2):
            self._notify_handled_event('event_handler3', event, arg1, arg2)
            return self.event_handler_return_value
        
        def unknown_event(self, event, arg1, arg2):
            self._notify_handled_event('unknown_event', event, arg1, arg2)
            return self.event_handler_return_value

class CallbackManager_1:
    def __init__(self):
        self.callback_state = None
        self.callback_value = None
        self.callback_keys = None

    def callback_func(self, state, value, keys):
        self.callback_state = state
        self.callback_value = value
        self.callback_keys = keys

class StateTryToHandleEventTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global root_state_1
        global foo

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        foo = statechart_1.get_state('FOO')
        
    # Try to invoke state foo's event_handler1 event handler
    def test_try_to_invoke_state_foo_eventhandler1(self):
        ret = foo.try_to_handle_event('event1', 100, 200)

        info = foo.handled_event_info

        self.assertTrue(ret)
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'event_handler1')
        self.assertEqual(info['event'], 'event1')
        self.assertEqual(info['arg1'], 100)
        self.assertEqual(info['arg2'], 200)

        info = statechart_1.state_will_try_to_handle_event_info

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'event1')
        self.assertEqual(info['handler'], 'event_handler1')
  
        info = statechart_1.state_did_try_to_handle_event_info

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'event1')
        self.assertEqual(info['handler'], 'event_handler1')
        self.assertTrue(info['handled'])

    # Try to invoke state foo's event_handler2 event handler
    def test_try_to_invoke_state_foo_eventhandler2(self):
        ret = foo.try_to_handle_event('event2', 100, 200)

        info = foo.handled_event_info

        self.assertTrue(ret)
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'event_handler2')
        self.assertEqual(info['event'], 'event2')
        self.assertEqual(info['arg1'], 100)
        self.assertEqual(info['arg2'], 200)

        info = statechart_1.state_will_try_to_handle_event_info

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'event2')
        self.assertEqual(info['handler'], 'event_handler2')
  
        info = statechart_1.state_did_try_to_handle_event_info

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'event2')
        self.assertEqual(info['handler'], 'event_handler2')
        self.assertTrue(info['handled'])

    # Try to invoke state foo's event_handler3 event handler
    def test_try_to_invoke_state_foo_eventhandler3(self):
        ret = foo.try_to_handle_event('digit3', 100, 200)

        info = foo.handled_event_info

        self.assertTrue(ret)
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'event_handler3')
        self.assertEqual(info['event'], 'digit3')
        self.assertEqual(info['arg1'], 100)
        self.assertEqual(info['arg2'], 200)

        info = statechart_1.state_will_try_to_handle_event_info

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'digit3')
        self.assertEqual(info['handler'], 'event_handler3')
  
        info = statechart_1.state_did_try_to_handle_event_info

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'digit3')
        self.assertEqual(info['handler'], 'event_handler3')
        self.assertTrue(info['handled'])

    # Try to invoke state foo's unknown event handler
    def test_try_to_invoke_state_foo_unknown_event_handler(self):
        ret = foo.try_to_handle_event('test', 100, 200)

        info = foo.handled_event_info

        self.assertTrue(ret)
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'unknown_event')
        self.assertEqual(info['event'], 'test')
        self.assertEqual(info['arg1'], 100)
        self.assertEqual(info['arg2'], 200)

        info = statechart_1.state_will_try_to_handle_event_info

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'test')
        self.assertEqual(info['handler'], 'unknown_event')
  
        info = statechart_1.state_did_try_to_handle_event_info

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'test')
        self.assertEqual(info['handler'], 'unknown_event')
        self.assertTrue(info['handled'])

    # Try not to invoke any of state foo's event handlers
    def test_try_not_to_invoke_any_state_foo_handlers(self):
        setattr(foo, 'unknown_event', None)

        ret = foo.try_to_handle_event('test', 100, 200)

        info = foo.handled_event_info

        self.assertFalse(ret)
        self.assertEqual(info, {})

        info = statechart_1.state_will_try_to_handle_event_info
        self.assertEqual(info, {})
  
        info = statechart_1.state_did_try_to_handle_event_info
        self.assertEqual(info, {})

    # Try to invoke state all of foo's handlers but try_to_handle_event returns false
    def test_try_to_invoke_all_state_foo_handlers_but_try_to_handle_event_returns_false(self):
        setattr(foo, 'event_handler_return_value', False)

        ret = foo.try_to_handle_event('event1')

        self.assertFalse(ret)
        info = foo.handled_event_info
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'event_handler1')
        self.assertTrue(statechart_1.state_will_try_to_handle_event_info)
        self.assertTrue(statechart_1.state_did_try_to_handle_event_info)

        ret = foo.try_to_handle_event('event2')
        
        self.assertFalse(ret)
        info = foo.handled_event_info
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'event_handler2')
        self.assertTrue(statechart_1.state_will_try_to_handle_event_info)
        self.assertTrue(statechart_1.state_did_try_to_handle_event_info)
  
        ret = foo.try_to_handle_event('digit3')
        
        self.assertFalse(ret)
        info = foo.handled_event_info
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'event_handler3')
        self.assertTrue(statechart_1.state_will_try_to_handle_event_info)
        self.assertTrue(statechart_1.state_did_try_to_handle_event_info)

        ret = foo.try_to_handle_event('blah')
        
        self.assertFalse(ret)
        info = foo.handled_event_info
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'unknown_event')
        self.assertTrue(statechart_1.state_will_try_to_handle_event_info)
        self.assertTrue(statechart_1.state_did_try_to_handle_event_info)
