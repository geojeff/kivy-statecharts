'''
Statechart tests, transitioning, async, core
===========
'''

import unittest

from kivy.properties import ObjectProperty, BooleanProperty
from kivy_statechart.system.async import Async

import os, inspect

class Obj:
    def __init__(self):
        self.fooInvoked = False
        self.arg1 = None
        self.arg2 = None

    def foo(self, arg1, arg2):
        self.fooInvoked = True
        self.arg1 = arg1
        self.arg2 = arg2

class StateTransitioningAsyncCore(unittest.TestCase):
    def setUp(self):
        pass

    # Test async - Async.perform('foo')
    def test_async_perform(self):
        obj = Obj()
        async = Async.perform(Async(None, None, None), 'foo')

        self.assertTrue(isinstance(async, Async))
        self.assertEqual(async.func, 'foo')
        self.assertEqual(async.arg1, None)
        self.assertEqual(async.arg2, None)

        async.tryToPerform(obj)
        self.assertEqual(obj.fooInvoked, True)
        self.assertEqual(async.arg1, None)
        self.assertEqual(async.arg2, None)

    # Test async - Async.perform('foo', 'hello', 'world')
    def test_async_perform_foo_hello_world(self):
        async = Async.perform(Async('foo', 'hello', 'world'), 'foo', 'hello', 'world')
        self.assertEqual(async.func, 'foo')
        self.assertEqual(async.arg1, 'hello')
        self.assertEqual(async.arg2, 'world')

        obj = Obj()
        async.tryToPerform(obj)
        self.assertEqual(obj.fooInvoked, True)
        self.assertEqual(async.arg1, 'hello')
        self.assertEqual(async.arg2, 'world')

    # Test async - Async.perform(function())
    def test_async_perform_function(self):
        def func(self, arg1, arg2):
            self.foo(arg1, arg2)
        async = Async.perform(Async('foo', 'hello', 'world'), func)
        self.assertEqual(async.func, func)
        self.assertEqual(async.arg1, None)
        self.assertEqual(async.arg2, None)

        obj = Obj()
        async.tryToPerform(obj)
        self.assertEqual(obj.fooInvoked, True)
        self.assertEqual(async.arg1, None)
        self.assertEqual(async.arg2, None)

    # Test async - Async.perform(function(), with args)
    def test_async_perform_function_with_args(self):
        def func(self, arg1, arg2):
            self.foo(arg1, arg2)
        async = Async.perform(Async('foo', 'hello', 'world'), func, 'aaa', 'bbb')
        self.assertEqual(async.func, func)
        self.assertEqual(async.arg1, 'aaa')
        self.assertEqual(async.arg2, 'bbb')

        obj = Obj()
        async.tryToPerform(obj)
        self.assertEqual(obj.fooInvoked, True)
        self.assertEqual(async.arg1, 'aaa')
        self.assertEqual(async.arg2, 'bbb')

    # Test async - Async.perform('bar')
    def test_async_perform(self):
        obj = Obj()
        async = Async.perform(Async(None, None, None), 'bar')

        self.assertEqual(async.func, 'bar')

        async.tryToPerform(obj)
        self.assertEqual(obj.fooInvoked, False)
