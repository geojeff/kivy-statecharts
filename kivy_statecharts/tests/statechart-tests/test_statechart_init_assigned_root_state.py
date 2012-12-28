'''
Statechart tests
===========
'''

import unittest

counter = 0

from kivy.app import App
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class A(State):
    def __init__(self, **kwargs):
        kwargs['name'] = 'A'
        super(A, self).__init__(**kwargs)

    def foo(self, *l):
        self.statechart.go_to_state('B')

class B(State):
    def __init__(self, **kwargs):
        kwargs['name'] = 'B'
        super(B, self).__init__(**kwargs)

    def bar(self, *l):
        self.statechart.go_to_state('A')

class RootState(State):
    def __init__(self, **kwargs):
        kwargs['initial_substate_key'] = 'A'
        kwargs['A'] = A
        kwargs['B'] = B
        super(RootState, self).__init__(**kwargs)

class Statechart_1(StatechartManager):
    def __init__(self, app, **kwargs):
        kwargs['app'] = app
        kwargs['trace'] = True
        kwargs['root_state_class'] = RootState
        super(Statechart_1, self).__init__(**kwargs)

# [PORT] State doesn't have initial_substate or substates_are_concurrent defined
#        by default, as apparently it was in the javascript version, because
#        in the test there, they set root_state to State. Here we force the set
#        of initial_substate in a subclass, and will make the API require the set.
#
class TestState(State):
    def __init__(self, **kwargs):
        kwargs['initial_substate_key'] = 'A'
        kwargs['A'] = A
        super(TestState, self).__init__(**kwargs)

class Statechart_2(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['trace'] = True
        kwargs['auto_init_statechart'] = False
        kwargs['root_state_class'] = TestState
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
        self.assertTrue(app.statechart.is_statechart)
        self.assertTrue(app.statechart.statechart_is_initialized)
        self.assertEqual(app.statechart.root_state_instance.name, '__ROOT_STATE__')
        self.assertTrue(isinstance(app.statechart.root_state_instance, State))
        self.assertEqual(app.statechart.initial_state_key, None)

        self.assertTrue(app.statechart.get_state('A').is_current_state())
        self.assertFalse(app.statechart.get_state('B').is_current_state())

        self.assertEqual(app.statechart.root_state_instance.owner, app.statechart)
        self.assertEqual(app.statechart.get_state('A').owner, app.statechart)
        self.assertEqual(app.statechart.get_state('B').owner, app.statechart)

        app.statechart.send_event('foo')

        self.assertFalse(app.statechart.get_state('A').is_current_state())
        self.assertTrue(app.statechart.get_state('B').is_current_state())

        self.assertTrue(statechart_2.is_statechart)
        self.assertFalse(statechart_2.statechart_is_initialized)

        statechart_2.init_statechart()

        self.assertTrue(statechart_2.statechart_is_initialized)

        # Trigger parts of the logging code system.
        statechart_2.suppress_statechart_warnings = True
        statechart_2.statechart_log_warning('Ignore me')

        statechart_2.suppress_statechart_warnings = False
        statechart_2.name = 'STATECHART 2'
        statechart_2.statechart_log_warning('Ignore me, now with a name')

    def test_init_with_root_state_class_of_wrong_type(self):
        class Statechart_3(StatechartManager):
            def __init__(self, **kwargs):
                kwargs['auto_init_statechart'] = False
                kwargs['root_state_class'] = dict
                super(Statechart_3, self).__init__(**kwargs)

        statechart_3 = Statechart_3()

        with self.assertRaises(Exception) as cm:
            statechart_3.init_statechart()

        msg = "Unable to initialize statechart. Root state must be a state class"
        self.assertEqual(str(cm.exception), msg)


