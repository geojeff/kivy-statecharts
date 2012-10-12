'''
Statechart tests, state create
==============================
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
        
    # Create a state
    def test_create(self):
        state_O = State(name='O')
        state_P = State(name='P')

        self.assertEqual(len(state_O._registered_substates), 0)

        state_P.parent_state = state_O
        state_P.init_state()

        self.assertEqual(len(state_O._registered_substates), 1)

        # Nothing should happen if init_state() called again.
        state_P.init_state()
        self.assertEqual(len(state_O._registered_substates), 1)

    def test_init_for_unnamed_state(self):
        state_O = State()
        state_P = State()

        state_P.parent_state = state_O

        with self.assertRaises(NameError) as cm:
            state_P.init_state()

        the_exception = cm.exception
        self.assertEqual(str(the_exception),
                         'Cannot init_state() an unnamed state.')

    def test_init_for_nonexistent_initial_substate_in_substates(self):


        # name has to be set as kwargs for this to work.
        class O(State):
            def __init__(self, **kwargs):
                kwargs['name'] = 'O'
                kwargs['initial_substate_key'] = 'I do not exist'
                super(O, self).__init__(**kwargs)

            class P(State):
                def __init__(self, **kwargs):
                    super(O.P, self).__init__(**kwargs)

            class Q(State):
                def __init__(self, **kwargs):
                    super(O.Q, self).__init__(**kwargs)


        o = O()

        msg = ("Unable to set initial substate {0} since it did not match any "
               "of state {1}'s substates").format("I do not exist", o)

        with self.assertRaises(AttributeError) as cm:
            o.init_state()

        self.assertEqual(str(cm.exception), msg)

    def test_init_for_state_with_initial_substate_but_no_substates(self):


        # name has to be set as kwargs for this to work.
        class O(State):
            def __init__(self, **kwargs):
                kwargs['name'] = 'O'
                kwargs['initial_substate_key'] = 'I do not exist'
                super(O, self).__init__(**kwargs)


        o = O()

        msg = ("Unable to make {0} an initial substate since state "
               "{1} has no substates").format("I do not exist", o)

        with self.assertRaises(AttributeError) as cm:
            o.init_state()

        self.assertEqual(str(cm.exception), msg)
        
    def test_init_for_state_with_both_initial_substate_and_concurrent_states(self):


        # name has to be set as kwargs for this to work.
        class O(State):
            def __init__(self, **kwargs):
                kwargs['name'] = 'O'
                kwargs['initial_substate_key'] = 'P'
                kwargs['substates_are_concurrent'] = True
                super(O, self).__init__(**kwargs)

            class P(State):
                def __init__(self, **kwargs):
                    super(O.P, self).__init__(**kwargs)

            class Q(State):
                def __init__(self, **kwargs):
                    super(O.Q, self).__init__(**kwargs)


        o = O()

        msg = ("Cannot use {0} as initial substate since "
               "substates are all concurrent for state "
               "{1}").format('P', o)

        with self.assertRaises(AttributeError) as cm:
            o.init_state()

        self.assertEqual(str(cm.exception), msg)


