'''
Statechart tests, invoke state method
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

class TestState(State):
    testInvoked = BooleanProperty(False)
    testInvokedCount = NumericProperty(0)
    returnValue = NumericProperty(None)
    arg1 = StringProperty(None)
    arg2 = StringProperty(None)
      
    def __init__(self, **kwargs):
        self.bind(testInvokedCount=self._testInvokedCountChanged)
        super(TestState, self).__init__(**kwargs)

    def _testInvokedCountChanged(self, *l):
        self.testInvoked = True if self.testInvokedCount > 0 else False

    def test(self, *args):
        arg1 = None
        arg2 = None
        if len(args) == 1:
            arg1 = args[0]
        if len(args) > 1: # Ignore args beyond the second.
            arg1 = args[0]
            arg2 = args[1]
        setattr(self, 'arg1', arg1)
        setattr(self, 'arg2', arg2)
        setattr(self, 'testInvokedCount', getattr(self, 'testInvokedCount') + 1)
        return self.returnValue if self.returnValue else None
      
class RootStateExample_1(TestState):
    def __init__(self, **kwargs):
        kwargs['initialSubstateKey'] = 'A'
        super(RootStateExample_1, self).__init__(**kwargs)

    def testX(self, *args):
        arg1 = None
        arg2 = None
        if args:
            if len(args) == 1:
                arg1 = args[0]
            else:
                arg1 = args[0]
                arg2 = args[1]
        if arg1:
            setattr(self, 'arg1', arg1)
        if arg2:
            setattr(self, 'arg2', arg2)
        setattr(self, 'testInvokedCount', getattr(self, 'testInvokedCount') + 1)
        return self.returnValue if self.returnValue else None

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['initialStateKey'] = 'A'
        kwargs['rootStateExample'] = RootStateExample_1
        kwargs['A'] = self.A
        kwargs['B'] = self.B
        super(Statechart_1, self).__init__(**kwargs)

    class A(TestState):
        def __init__(self, **kwargs):
            super(Statechart_1.A, self).__init__(**kwargs)

    class B(TestState):
        def __init__(self, **kwargs):
            super(Statechart_1.B, self).__init__(**kwargs)

class RootStateExample_2(TestState):
    def __init__(self, **kwargs):
        kwargs['substatesAreConcurrent'] = True
        super(RootStateExample_2, self).__init__(**kwargs)

    def testX(self, *args):
        arg1 = None
        arg2 = None
        if args:
            if len(args) == 1:
                arg1 = args[0]
            else:
                arg1 = args[0]
                arg2 = args[1]
        if arg1:
            setattr(self, 'arg1', arg1)
        if arg2:
            setattr(self, 'arg2', arg2)
        setattr(self, 'testInvokedCount', getattr(self, 'testInvokedCount') + 1)
        return self.returnValue if self.returnValue else None

class Statechart_2(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['statesAreConcurrent'] = True
        kwargs['rootStateExample'] = RootStateExample_2
        kwargs['C'] = self.C
        kwargs['D'] = self.D
        super(Statechart_2, self).__init__(**kwargs)

    class C(TestState):
        def __init__(self, **kwargs):
            super(Statechart_2.C, self).__init__(**kwargs)

    class D(TestState):
        def __init__(self, **kwargs):
            super(Statechart_2.D, self).__init__(**kwargs)

class CallbackManager_1:
    def __init__(self):
        self.callbackState = None
        self.callbackResult = None

    def callbackFunc(self, state, result):
        self.callbackState = state
        self.callbackResult = result

class CallbackManager_2:
    def __init__(self):
        self.numCallbacks = 0
        self.callbackInfo = {}

    def callbackFunc(self, state, result):
        self.numCallbacks += 1
        self.callbackInfo['state{0}'.format(self.numCallbacks)] = state
        self.callbackInfo['result{0}'.format(self.numCallbacks)] = result

class StatechartInvokeStateMethodTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global statechart_2
        global rootState_1
        global rootState_2
        global state_A
        global state_B
        global state_C
        global state_D

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootState
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        statechart_2 = Statechart_2()
        statechart_2.initStatechart()
        rootState_2 = statechart_2.rootState
        state_C = statechart_2.getState('C')
        state_D = statechart_2.getState('D')
        
    # invoke method test1
    def test_invoke_method_test1_statechart_1(self):
        result = statechart_1.invokeStateMethod('test1')
        self.assertFalse(rootState_1.testInvoked)
        self.assertFalse(state_A.testInvoked)
        self.assertFalse(state_B.testInvoked)

    # invoke method test, current state A, no args, no return value
    def test_invoke_method_test_state_A_no_args_no_return_statechart_1(self):
        result = statechart_1.invokeStateMethod('test')
        self.assertEqual(state_A.testInvokedCount, 1)
        self.assertIsNone(state_A.arg1)
        self.assertIsNone(state_A.arg2)
        self.assertIsNone(result)
        self.assertFalse(rootState_1.testInvoked)
        self.assertFalse(state_B.testInvoked)

    # invoke method test, current state A, one args, no return value
    def test_invoke_method_test_state_A_one_args_no_return_statechart_1(self):
        result = statechart_1.invokeStateMethod('test', 'frozen')
        self.assertTrue(state_A.testInvoked)
        self.assertEqual(state_A.arg1, 'frozen')
        self.assertIsNone(state_A.arg2)
        self.assertFalse(rootState_1.testInvoked)
        self.assertFalse(state_B.testInvoked)

    # check obj1 - invoke method test, current state A, two args, no return value
    def test_invoke_method_test_state_A_two_args_no_return_statechart_1(self):
        result = statechart_1.invokeStateMethod('test', 'frozen', 'canuck')
        self.assertTrue(state_A.testInvoked)
        self.assertEqual(state_A.arg1, 'frozen')
        self.assertEqual(state_A.arg2, 'canuck')
        self.assertFalse(rootState_1.testInvoked)
        self.assertFalse(state_B.testInvoked)

    # check obj1 - invoke method test, current state A, no args, return value
    def test_invoke_method_test_state_A_no_args_return_statechart_1(self):
        setattr(state_A, 'returnValue', 100)
        result = statechart_1.invokeStateMethod('test')
        self.assertTrue(state_A.testInvoked)
        self.assertFalse(rootState_1.testInvoked)
        self.assertFalse(state_B.testInvoked)

    # check obj1 - invoke method test, current state B, two args, return value
    def test_invoke_method_test_state_B_two_args_return_statechart_1(self):
        setattr(state_B, 'returnValue', 100)
        statechart_1.gotoState('B')
        self.assertTrue(state_B.isCurrentState())
        result = statechart_1.invokeStateMethod('test', 'frozen', 'canuck')
        self.assertFalse(state_A.testInvoked)
        self.assertEqual(state_B.testInvokedCount, 1)
        self.assertEqual(state_B.arg1, 'frozen')
        self.assertEqual(state_B.arg2, 'canuck')
        self.assertEqual(result, 100)
        self.assertFalse(rootState_1.testInvoked)

    # check obj1 - invoke method test, current state A, use callback
    def test_invoke_method_test_state_A_use_callback_statechart_1(self):
        callbackManager = CallbackManager_1()

        result = statechart_1.invokeStateMethod('test', callbackManager.callbackFunc)
        self.assertTrue(state_A.testInvoked)
        self.assertFalse(state_B.testInvoked)
        self.assertEqual(callbackManager.callbackState, state_A)
        self.assertIsNone(callbackManager.callbackResult)
        self.assertFalse(rootState_1.testInvoked)

    # check obj1- invoke method test, current state B, use callback
    def test_invoke_method_test_state_B_use_callback_statechart_1(self):
        statechart_1.gotoState('B')
        setattr(state_B, 'returnValue', 100)

        callbackManager = CallbackManager_1()

        result = statechart_1.invokeStateMethod('test', callbackManager.callbackFunc)
        self.assertFalse(state_A.testInvoked)
        self.assertTrue(state_B.testInvoked)
        self.assertEqual(callbackManager.callbackState, state_B)
        self.assertEqual(callbackManager.callbackResult, 100)
        self.assertFalse(rootState_1.testInvoked)

    # check obj1 - invoke method testX
    def test_invoke_method_testX_statechart_1(self):
        setattr(rootState_1, 'returnValue', 100)
        result = statechart_1.invokeStateMethod('testX')
        self.assertEqual(rootState_1.testInvokedCount, 1)
        self.assertEqual(result, 100)
        self.assertFalse(state_A.testInvoked)
        self.assertFalse(state_B.testInvoked)

    # check obj2 - invoke method test1
    def test_invoke_method_test1_statechart_2(self):
        result = statechart_2.invokeStateMethod('test1')
        self.assertFalse(rootState_2.testInvoked)
        self.assertFalse(state_C.testInvoked)
        self.assertFalse(state_D.testInvoked)

    # check obj2 - invoke test, no args, no return value
    def test_invoke_method_test_no_args_no_return_statechart_2(self):
        result = statechart_2.invokeStateMethod('test')
        self.assertEqual(state_C.testInvokedCount, 1)
        self.assertEqual(state_D.testInvokedCount, 1)
        self.assertFalse(rootState_2.testInvoked)
        self.assertIsNone(state_C.arg1)
        self.assertIsNone(state_C.arg2)
        self.assertIsNone(state_D.arg1)
        self.assertIsNone(state_D.arg2)
        self.assertIsNone(result)

    # check obj2 - invoke test, two args, return value, callback
    def test_invoke_method_test_two_args_return_value_use_callback_statechart_2(self):
        setattr(state_C, 'returnValue', 100)
        setattr(state_D, 'returnValue', 200)

        callbackManager = CallbackManager_2()

        result = statechart_2.invokeStateMethod('test', 'frozen', 'canuck', callbackManager.callbackFunc)

        self.assertFalse(rootState_2.testInvoked)
        self.assertEqual(state_C.testInvokedCount, 1)
        self.assertEqual(state_D.testInvokedCount, 1)

        self.assertEqual(state_C.arg1, 'frozen')
        self.assertEqual(state_C.arg2, 'canuck')

        self.assertEqual(state_D.arg1, 'frozen')
        self.assertEqual(state_D.arg2, 'canuck')

        self.assertEqual(callbackManager.numCallbacks, 2)
        self.assertEqual(callbackManager.callbackInfo['state1'], state_C)
        self.assertEqual(callbackManager.callbackInfo['result1'], 100)
        self.assertEqual(callbackManager.callbackInfo['state2'], state_D)
        self.assertEqual(callbackManager.callbackInfo['result2'], 200)

        self.assertIsNone(result)

    def test_invoke_method_testX_statechart_2(self):
        setattr(rootState_2, 'returnValue', 100)
        result = statechart_2.invokeStateMethod('testX')
        self.assertEqual(rootState_2.testInvokedCount, 1)
        self.assertEqual(result, 100)
        self.assertFalse(state_C.testInvoked)
        self.assertFalse(state_D.testInvoked)


