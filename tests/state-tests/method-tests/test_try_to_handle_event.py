'''
Statechart tests, try to handle event
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, DictProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    stateWillTryToHandleEventInfo = DictProperty({})
    stateDidTryToHandleEventInfo = DictProperty({})

    def __init__(self, **kwargs):
        kwargs['initialStateKey'] = 'FOO'
        super(Statechart_1, self).__init__(**kwargs)

    def stateWillTryToHandleEvent(self, state, event, handler):
        self.stateWillTryToHandleEventInfo = {
          'state': state,
          'event': event,
          'handler': handler
        }

    def stateDidTryToHandleEvent(self, state, event, handler, handled):
        self.stateDidTryToHandleEventInfo = {
          'state': state,
          'event': event,
          'handler': handler,
          'handled': handled
        }

    class FOO(State):
        eventHandlerReturnValue = BooleanProperty(False)
        handledEventInfo = DictProperty({})

        def __init__(self, **kwargs):
            kwargs['eventHandlerReturnValue'] = True
            super(Statechart_1.FOO, self).__init__(**kwargs)

        def _notifyHandledEvent(self, handler, event, arg1, arg2):
            self.handledEventInfo = {
                'handler': handler,
                'event': event,
                'arg1': arg1,
                'arg2': arg2
            }
 
        @State.eventHandler(['event1']) 
        def eventHandler1(self, event, arg1, arg2):
            self._notifyHandledEvent('eventHandler1', 'event1', arg1, arg2)
            return self.eventHandlerReturnValue
        
        @State.eventHandler(['event2'])
        def eventHandler2(self, event, arg1, arg2):
            self._notifyHandledEvent('eventHandler2', event, arg1, arg2)
            return self.eventHandlerReturnValue
        
        @State.eventHandler([re.compile('^digit[0-9]$')])
        def eventHandler3(self, event, arg1, arg2):
            self._notifyHandledEvent('eventHandler3', event, arg1, arg2)
            return self.eventHandlerReturnValue
        
        def unknownEvent(self, event, arg1, arg2):
            self._notifyHandledEvent('unknownEvent', event, arg1, arg2)
            return self.eventHandlerReturnValue

class CallbackManager_1:
    def __init__(self):
        self.callbackState = None
        self.callbackValue = None
        self.callbackKeys = None

    def callbackFunc(self, state, value, keys):
        self.callbackState = state
        self.callbackValue = value
        self.callbackKeys = keys

class StateTryToHandleEventTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global rootState_1
        global foo

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootState
        foo = statechart_1.getState('FOO')
        
    # Try to invoke state foo's eventHandler1 event handler
    def test_try_to_invoke_state_foo_eventhandler1(self):
        ret = foo.tryToHandleEvent('event1', 100, 200)

        info = foo.handledEventInfo

        self.assertTrue(ret)
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'eventHandler1')
        self.assertEqual(info['event'], 'event1')
        self.assertEqual(info['arg1'], 100)
        self.assertEqual(info['arg2'], 200)

        info = statechart_1.stateWillTryToHandleEventInfo

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'event1')
        self.assertEqual(info['handler'], 'eventHandler1')
  
        info = statechart_1.stateDidTryToHandleEventInfo

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'event1')
        self.assertEqual(info['handler'], 'eventHandler1')
        self.assertTrue(info['handled'])

    # Try to invoke state foo's eventHandler2 event handler
    def test_try_to_invoke_state_foo_eventhandler2(self):
        ret = foo.tryToHandleEvent('event2', 100, 200)

        info = foo.handledEventInfo

        self.assertTrue(ret)
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'eventHandler2')
        self.assertEqual(info['event'], 'event2')
        self.assertEqual(info['arg1'], 100)
        self.assertEqual(info['arg2'], 200)

        info = statechart_1.stateWillTryToHandleEventInfo

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'event2')
        self.assertEqual(info['handler'], 'eventHandler2')
  
        info = statechart_1.stateDidTryToHandleEventInfo

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'event2')
        self.assertEqual(info['handler'], 'eventHandler2')
        self.assertTrue(info['handled'])

    # Try to invoke state foo's eventHandler3 event handler
    def test_try_to_invoke_state_foo_eventhandler3(self):
        ret = foo.tryToHandleEvent('digit3', 100, 200)

        info = foo.handledEventInfo

        self.assertTrue(ret)
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'eventHandler3')
        self.assertEqual(info['event'], 'digit3')
        self.assertEqual(info['arg1'], 100)
        self.assertEqual(info['arg2'], 200)

        info = statechart_1.stateWillTryToHandleEventInfo

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'digit3')
        self.assertEqual(info['handler'], 'eventHandler3')
  
        info = statechart_1.stateDidTryToHandleEventInfo

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'digit3')
        self.assertEqual(info['handler'], 'eventHandler3')
        self.assertTrue(info['handled'])

    # Try to invoke state foo's unknown event handler
    def test_try_to_invoke_state_foo_unknown_event_handler(self):
        ret = foo.tryToHandleEvent('test', 100, 200)

        info = foo.handledEventInfo

        self.assertTrue(ret)
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'unknownEvent')
        self.assertEqual(info['event'], 'test')
        self.assertEqual(info['arg1'], 100)
        self.assertEqual(info['arg2'], 200)

        info = statechart_1.stateWillTryToHandleEventInfo

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'test')
        self.assertEqual(info['handler'], 'unknownEvent')
  
        info = statechart_1.stateDidTryToHandleEventInfo

        self.assertIsNotNone(info)
        self.assertEqual(info['state'], foo)
        self.assertEqual(info['event'], 'test')
        self.assertEqual(info['handler'], 'unknownEvent')
        self.assertTrue(info['handled'])

    # Try not to invoke any of state foo's event handlers
    def test_try_not_to_invoke_any_state_foo_handlers(self):
        setattr(foo, 'unknownEvent', None)

        ret = foo.tryToHandleEvent('test', 100, 200)

        info = foo.handledEventInfo

        self.assertFalse(ret)
        self.assertEqual(info, {})

        info = statechart_1.stateWillTryToHandleEventInfo
        self.assertEqual(info, {})
  
        info = statechart_1.stateDidTryToHandleEventInfo
        self.assertEqual(info, {})

    # Try to invoke state all of foo's handlers but tryToHandleEvent returns false
    def test_try_to_invoke_all_state_foo_handlers_but_tryToHandleEvent_returns_false(self):
        setattr(foo, 'eventHandlerReturnValue', False)

        ret = foo.tryToHandleEvent('event1')

        self.assertFalse(ret)
        info = foo.handledEventInfo
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'eventHandler1')
        self.assertTrue(statechart_1.stateWillTryToHandleEventInfo)
        self.assertTrue(statechart_1.stateDidTryToHandleEventInfo)

        ret = foo.tryToHandleEvent('event2')
        
        self.assertFalse(ret)
        info = foo.handledEventInfo
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'eventHandler2')
        self.assertTrue(statechart_1.stateWillTryToHandleEventInfo)
        self.assertTrue(statechart_1.stateDidTryToHandleEventInfo)
  
        ret = foo.tryToHandleEvent('digit3')
        
        self.assertFalse(ret)
        info = foo.handledEventInfo
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'eventHandler3')
        self.assertTrue(statechart_1.stateWillTryToHandleEventInfo)
        self.assertTrue(statechart_1.stateDidTryToHandleEventInfo)

        ret = foo.tryToHandleEvent('blah')
        
        self.assertFalse(ret)
        info = foo.handledEventInfo
        self.assertIsNotNone(info)
        self.assertEqual(info['handler'], 'unknownEvent')
        self.assertTrue(statechart_1.stateWillTryToHandleEventInfo)
        self.assertTrue(statechart_1.stateDidTryToHandleEventInfo)
