'''
Statechart tests, add substate
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.empty_state import EmptyState
from kivy_statecharts.system.empty_state import EMPTY_STATE_NAME
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['root_state_class'] = self.RootState
        kwargs['trace'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['substates_are_concurrent'] = True
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

            class X(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.X, self).__init__(**kwargs)

            class Y(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.Y, self).__init__(**kwargs)


# name has to be set as kwargs for this to work.
class O(State):
    def __init__(self, **kwargs):
        kwargs['name'] = 'O'
        kwargs['initial_substate_key'] = 'P'
        super(O, self).__init__(**kwargs)

    def do_not_tread_on_me(self):
        pass

    class P(State):
        def __init__(self, **kwargs):
            super(O.P, self).__init__(**kwargs)

    class Q(State):
        def __init__(self, **kwargs):
            super(O.Q, self).__init__(**kwargs)


class StateAddSubstateTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global root_state_1
        global monitor_1
        global state_A
        global state_B
        global state_X
        global state_Y

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        state_X = statechart_1.get_state('X')
        state_Y = statechart_1.get_state('Y')
        
    # Add a substate to the statechart's root state
    def test_add_substate_to_root_state_statechart_1(self):
        self.assertIsNone(root_state_1.get_substate('Z'))

        state = root_state_1.add_substate('Z')

        self.assertTrue(isinstance(state, State))
        self.assertIsNotNone(root_state_1.get_substate('Z'))
        self.assertTrue(state.state_is_initialized)
        self.assertEqual(state.name, 'Z')
        self.assertFalse(state.is_entered_state())
        self.assertFalse(state.is_current_state())

        statechart_1.go_to_state('Z')

        self.assertTrue(state.is_entered_state())
        self.assertTrue(state.is_current_state())

    # Add a substate to state A
    def test_add_substate_to_state_A_statechart_1(self):
        self.assertIsNone(state_A.get_substate('Z'))
        # [PORT] EmptyState is created only for states with substates,
        #        and no initial_substate set. Correct?
        self.assertEqual(state_A.initial_substate_key, None)

        state = state_A.add_substate('Z')

        self.assertTrue(isinstance(state, State))
        self.assertEqual(state_A.get_substate('Z'), state)
        self.assertEqual(state_A.initial_substate_key, EMPTY_STATE_NAME)
        self.assertFalse(state.is_entered_state())
        self.assertFalse(state.is_current_state())
        self.assertTrue(state_A.is_entered_state())
        self.assertTrue(state_A.is_current_state())

        print 'reentering state A'
        setattr(state_A, 'initial_substate_key', state.name)
        state_A.reenter()

        self.assertTrue(state.is_entered_state())
        self.assertTrue(state.is_current_state())
        self.assertTrue(state_A.is_entered_state())
        self.assertFalse(state_A.is_current_state())

    # Add a substate to state B
    def test_add_substate_to_state_B_statechart_1(self):
        self.assertIsNone(state_B.get_substate('Z'))

        statechart_1.go_to_state('B')

        state = state_B.add_substate('Z')

        self.assertTrue(isinstance(state, State))
        self.assertEqual(state_B.get_substate('Z'), state)
        self.assertFalse(state.is_entered_state())
        self.assertFalse(state.is_current_state())
        self.assertFalse(state_B.is_current_state())
        self.assertEqual(state_B.initial_substate_key, None)
        self.assertTrue(state_B.is_entered_state())
        self.assertEqual(len(state_B.current_substates), 2)

        state_B.reenter()

        self.assertTrue(state.is_entered_state())
        self.assertTrue(state.is_current_state())
        self.assertTrue(state_B.is_entered_state())
        self.assertEqual(len(state_B.current_substates), 3)

    def test_adding_unnamed_substate(self):
        o = O()
        o.init_state()

        name = 'do_not_tread_on_me'

        with self.assertRaises(Exception) as cm:
            o.add_substate(name)

        msg = ("Cannot add substate '{0}'. Already a defined "
               "property").format(name)
        self.assertEqual(str(cm.exception), msg)

    def test_adding_unnamed_substate(self):
        o = O()

        name = 'A'

        with self.assertRaises(Exception) as cm:
            o.add_substate(name)

        msg = ("Cannot add substate '{0}'. Parent state is not yet "
               "initialized").format(name)
        self.assertEqual(str(cm.exception), msg)

