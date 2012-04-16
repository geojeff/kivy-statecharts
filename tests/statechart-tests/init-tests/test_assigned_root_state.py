'''
Statechart tests
===========
'''

import unittest

counter = 0

from kivy.app import App
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

class A(State):
    def __init__(self, **kwargs):
        kwargs['name'] = 'A'
        super(A, self).__init__(**kwargs)

    def foo(self, *l):
        self.statechart.gotoState('B')

class B(State):
    def __init__(self, **kwargs):
        kwargs['name'] = 'B'
        super(B, self).__init__(**kwargs)

    def bar(self, *l):
        self.statechart.gotoState('A')

class RootState(State):
    def __init__(self, **kwargs):
        kwargs['initialSubstateKey'] = 'A'
        kwargs['A'] = A
        kwargs['B'] = B
        super(RootState, self).__init__(**kwargs)

class Statechart_1(StatechartManager):
    def __init__(self, app, **kwargs):
        kwargs['app'] = app
        kwargs['trace'] = True
        kwargs['rootStateClass'] = RootState
        super(Statechart_1, self).__init__(**kwargs)

# [PORT] State doesn't have initialSubstate or substatesAreConcurrent defined
#        by default, as apparently it was in the javascript version, because
#        in the test there, they set rootState to State. Here we force the set
#        of initialSubstate in a subclass, and will make the API require the set.
#
class TestState(State):
    def __init__(self, **kwargs):
        kwargs['initialSubstateKey'] = 'A'
        kwargs['A'] = A
        super(TestState, self).__init__(**kwargs)

class Statechart_2(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['trace'] = True
        kwargs['autoInitStatechart'] = False
        kwargs['rootStateClass'] = TestState
        super(Statechart_2, self).__init__(**kwargs)

class TestApp(App):
    pass

class StatechartTestCase(unittest.TestCase):
    def setUp(self):
        global app
        global statechart_1
        global statechart_2
        app = TestApp()
        statechart_1 = Statechart_1(app)
        app.statechart = statechart_1

        statechart_2 = Statechart_2()

    def test_init_with_assigned_root_state(self):
        self.assertTrue(app.statechart.isStatechart)
        self.assertTrue(app.statechart.statechartIsInitialized)
        self.assertEqual(app.statechart.rootStateInstance.name, '__ROOT_STATE__')
        self.assertTrue(isinstance(app.statechart.rootStateInstance, State))
        self.assertEqual(app.statechart.initialStateKey, '')

        self.assertTrue(app.statechart.getState('A').isCurrentState())
        self.assertFalse(app.statechart.getState('B').isCurrentState())

        self.assertEqual(app.statechart.rootStateInstance.owner, app.statechart)
        self.assertEqual(app.statechart.getState('A').owner, app.statechart)
        self.assertEqual(app.statechart.getState('B').owner, app.statechart)

        app.statechart.sendEvent('foo')

        self.assertFalse(app.statechart.getState('A').isCurrentState())
        self.assertTrue(app.statechart.getState('B').isCurrentState())

        self.assertTrue(statechart_2.isStatechart)
        self.assertFalse(statechart_2.statechartIsInitialized)

        statechart_2.initStatechart()

        self.assertTrue(statechart_2.statechartIsInitialized)
