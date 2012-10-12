'''
Statechart tests, invoke state method
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class TestState(State):
    test_invoked = BooleanProperty(False)
    test_invoked_count = NumericProperty(0)
    return_value = NumericProperty(None)
    arg1 = StringProperty(None)
    arg2 = StringProperty(None)
      
    def __init__(self, **kwargs):
        self.bind(test_invoked_count=self._test_invoked_countChanged)
        super(TestState, self).__init__(**kwargs)

    def _test_invoked_countChanged(self, *l):
        self.test_invoked = True if self.test_invoked_count > 0 else False

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
        setattr(self, 'test_invoked_count', getattr(self, 'test_invoked_count') + 1)
        return self.return_value if self.return_value else None
      
class RootStateExample_1(TestState):
    def __init__(self, **kwargs):
        kwargs['initial_substate_key'] = 'A'
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
        setattr(self, 'test_invoked_count', getattr(self, 'test_invoked_count') + 1)
        return self.return_value if self.return_value else None

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['initial_state_key'] = 'A'
        kwargs['root_state_example_class'] = RootStateExample_1
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
        kwargs['substates_are_concurrent'] = True
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
        setattr(self, 'test_invoked_count', getattr(self, 'test_invoked_count') + 1)
        return self.return_value if self.return_value else None

class Statechart_2(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['states_are_concurrent'] = True
        kwargs['root_state_example_class'] = RootStateExample_2
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
        self.callback_state = None
        self.callback_result = None

    def callback_func(self, state, result):
        self.callback_state = state
        self.callback_result = result

class CallbackManager_2:
    def __init__(self):
        self.num_callbacks = 0
        self.callback_info = {}

    def callback_func(self, state, result):
        self.num_callbacks += 1
        self.callback_info['state{0}'.format(self.num_callbacks)] = state
        self.callback_info['result{0}'.format(self.num_callbacks)] = result

class StatechartInvokeStateMethodTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global statechart_2
        global root_state_1
        global root_state_2
        global state_A
        global state_B
        global state_C
        global state_D

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        statechart_2 = Statechart_2()
        statechart_2.init_statechart()
        root_state_2 = statechart_2.root_state_instance
        state_C = statechart_2.get_state('C')
        state_D = statechart_2.get_state('D')
        
    # invoke method test1
    def test_invoke_method_test1_statechart_1(self):
        result = statechart_1.invoke_state_method('test1')
        self.assertFalse(root_state_1.test_invoked)
        self.assertFalse(state_A.test_invoked)
        self.assertFalse(state_B.test_invoked)

    # invoke method test, current state A, no args, no return value
    def test_invoke_method_test_state_A_no_args_no_return_statechart_1(self):
        result = statechart_1.invoke_state_method('test')
        self.assertEqual(state_A.test_invoked_count, 1)
        self.assertIsNone(state_A.arg1)
        self.assertIsNone(state_A.arg2)
        self.assertIsNone(result)
        self.assertFalse(root_state_1.test_invoked)
        self.assertFalse(state_B.test_invoked)

    # invoke method test, current state A, one args, no return value
    def test_invoke_method_test_state_A_one_args_no_return_statechart_1(self):
        result = statechart_1.invoke_state_method('test', 'frozen')
        self.assertTrue(state_A.test_invoked)
        self.assertEqual(state_A.arg1, 'frozen')
        self.assertIsNone(state_A.arg2)
        self.assertFalse(root_state_1.test_invoked)
        self.assertFalse(state_B.test_invoked)

    # check obj1 - invoke method test, current state A, two args, no return value
    def test_invoke_method_test_state_A_two_args_no_return_statechart_1(self):
        result = statechart_1.invoke_state_method('test', 'frozen', 'canuck')
        self.assertTrue(state_A.test_invoked)
        self.assertEqual(state_A.arg1, 'frozen')
        self.assertEqual(state_A.arg2, 'canuck')
        self.assertFalse(root_state_1.test_invoked)
        self.assertFalse(state_B.test_invoked)

    # check obj1 - invoke method test, current state A, no args, return value
    def test_invoke_method_test_state_A_no_args_return_statechart_1(self):
        setattr(state_A, 'return_value', 100)
        result = statechart_1.invoke_state_method('test')
        self.assertTrue(state_A.test_invoked)
        self.assertFalse(root_state_1.test_invoked)
        self.assertFalse(state_B.test_invoked)

    # check obj1 - invoke method test, current state B, two args, return value
    def test_invoke_method_test_state_B_two_args_return_statechart_1(self):
        setattr(state_B, 'return_value', 100)
        statechart_1.go_to_state('B')
        self.assertTrue(state_B.is_current_state())
        result = statechart_1.invoke_state_method('test', 'frozen', 'canuck')
        self.assertFalse(state_A.test_invoked)
        self.assertEqual(state_B.test_invoked_count, 1)
        self.assertEqual(state_B.arg1, 'frozen')
        self.assertEqual(state_B.arg2, 'canuck')
        self.assertEqual(result, 100)
        self.assertFalse(root_state_1.test_invoked)

    # check obj1 - invoke method test, current state A, use callback
    def test_invoke_method_test_state_A_use_callback_statechart_1(self):
        callback_manager = CallbackManager_1()

        result = statechart_1.invoke_state_method('test', callback_manager.callback_func)
        self.assertTrue(state_A.test_invoked)
        self.assertFalse(state_B.test_invoked)
        self.assertEqual(callback_manager.callback_state, state_A)
        self.assertIsNone(callback_manager.callback_result)
        self.assertFalse(root_state_1.test_invoked)

    # check obj1- invoke method test, current state B, use callback
    def test_invoke_method_test_state_B_use_callback_statechart_1(self):
        statechart_1.go_to_state('B')
        setattr(state_B, 'return_value', 100)

        callback_manager = CallbackManager_1()

        result = statechart_1.invoke_state_method('test', callback_manager.callback_func)
        self.assertFalse(state_A.test_invoked)
        self.assertTrue(state_B.test_invoked)
        self.assertEqual(callback_manager.callback_state, state_B)
        self.assertEqual(callback_manager.callback_result, 100)
        self.assertFalse(root_state_1.test_invoked)

    # check obj1 - invoke method testX
    def test_invoke_method_testX_statechart_1(self):
        setattr(root_state_1, 'return_value', 100)
        result = statechart_1.invoke_state_method('testX')
        self.assertEqual(root_state_1.test_invoked_count, 1)
        self.assertEqual(result, 100)
        self.assertFalse(state_A.test_invoked)
        self.assertFalse(state_B.test_invoked)

    # check obj2 - invoke method test1
    def test_invoke_method_test1_statechart_2(self):
        result = statechart_2.invoke_state_method('test1')
        self.assertFalse(root_state_2.test_invoked)
        self.assertFalse(state_C.test_invoked)
        self.assertFalse(state_D.test_invoked)

    # check obj2 - invoke test, no args, no return value
    def test_invoke_method_test_no_args_no_return_statechart_2(self):
        result = statechart_2.invoke_state_method('test')
        self.assertEqual(state_C.test_invoked_count, 1)
        self.assertEqual(state_D.test_invoked_count, 1)
        self.assertFalse(root_state_2.test_invoked)
        self.assertIsNone(state_C.arg1)
        self.assertIsNone(state_C.arg2)
        self.assertIsNone(state_D.arg1)
        self.assertIsNone(state_D.arg2)
        self.assertIsNone(result)

    # check obj2 - invoke test, two args, return value, callback
    def test_invoke_method_test_two_args_return_value_use_callback_statechart_2(self):
        setattr(state_C, 'return_value', 100)
        setattr(state_D, 'return_value', 200)

        callback_manager = CallbackManager_2()

        result = statechart_2.invoke_state_method('test', 'frozen', 'canuck', callback_manager.callback_func)

        self.assertFalse(root_state_2.test_invoked)
        self.assertEqual(state_C.test_invoked_count, 1)
        self.assertEqual(state_D.test_invoked_count, 1)

        self.assertEqual(state_C.arg1, 'frozen')
        self.assertEqual(state_C.arg2, 'canuck')

        self.assertEqual(state_D.arg1, 'frozen')
        self.assertEqual(state_D.arg2, 'canuck')

        self.assertEqual(callback_manager.num_callbacks, 2)
        self.assertEqual(callback_manager.callback_info['state1'], state_C)
        self.assertEqual(callback_manager.callback_info['result1'], 100)
        self.assertEqual(callback_manager.callback_info['state2'], state_D)
        self.assertEqual(callback_manager.callback_info['result2'], 200)

        self.assertIsNone(result)

    def test_invoke_method_testX_statechart_2(self):
        setattr(root_state_2, 'return_value', 100)
        result = statechart_2.invoke_state_method('testX')
        self.assertEqual(root_state_2.test_invoked_count, 1)
        self.assertEqual(result, 100)
        self.assertFalse(state_C.test_invoked)
        self.assertFalse(state_D.test_invoked)


