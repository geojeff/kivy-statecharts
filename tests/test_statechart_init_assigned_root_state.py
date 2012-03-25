'''
Statechart tests
===========
'''

import unittest

counter = 0

from kivy.app import App
from kivy.statechart.system.state import State
from kivy.statechart.system.statechart import StatechartManager

import os, inspect

class A(State):
    def __init__(self, **kwargs):
        kwargs['name'] = 'A'
        super(A, self).__init__(**kwargs)

    def foo(self, *l):
        print 'foo called, trying to goto B'
        self.statechart.gotoState('B') # [PORT] self.gotoState should work...

class B(State):
    def __init__(self, **kwargs):
        kwargs['name'] = 'B'
        super(B, self).__init__(**kwargs)

    def bar(self, *l):
        print 'bar called, trying to goto A'
        self.statechart.gotoState('A')

class RootState(State):
    def __init__(self, **kwargs):
        super(RootState, self).__init__(**kwargs)
    
    initialSubstate = 'A'
    
    A = A
    B = B

class Statechart1(StatechartManager):
    def __init__(self, app, **kw):
        self.app = app
        self.trace = True
        self.rootState = RootState
        super(Statechart1, self).__init__(**kw)

class Statechart2(StatechartManager):
    def __init__(self, **kw):
        self.trace = True
        self.autoInitStatechart = False
        self.rootState = State
        super(Statechart2, self).__init__(**kw)

class TestApp(App):
    pass

class StatechartTestCase(unittest.TestCase):
    def setUp(self):
        global app
        global s1
        global s2
        app = TestApp()
        s1 = Statechart1(app)
        app.statechart = s1
        s2 = Statechart2()

    def test_init_with_assigned_root_state(self):
        self.assertTrue(app.statechart.isStatechart)
        self.assertTrue(app.statechart.statechartIsInitialized)
        self.assertEqual(app.statechart.rootState.name, '__ROOT_STATE__')
        self.assertTrue(isinstance(app.statechart.rootState, State))
        self.assertEqual(app.statechart.initialState, None)

        self.assertTrue(app.statechart.getState('A').isCurrentState)
        self.assertFalse(app.statechart.getState('B').isCurrentState)

        # [PORT] Except for the cross-object observing bit (commented out), owner is not set. Even with it, it seems.
        #self.assertEqual(app.statechart.rootState.owner, app.statechart)
        #self.assertEqual(app.statechart.getState('A').owner, app.statechart)
        #self.assertEqual(app.statechart.getState('B').owner, app.statechart)

        app.statechart.sendEvent('foo')

        self.assertFalse(app.statechart.getState('A').isCurrentState)
        self.assertTrue(app.statechart.getState('B').isCurrentState)

        self.assertTrue(s2.isStatechart)
        self.assertFalse(s2.statechartIsInitialized)

        s2.initStatechart()

        self.assertTrue(s2.statechartIsInitialized)
