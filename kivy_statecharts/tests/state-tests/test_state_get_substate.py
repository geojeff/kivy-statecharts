'''
Statechart tests, get substate
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['initial_state_key'] = 'FOO'
        super(Statechart_1, self).__init__(**kwargs)

    class FOO(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_1.FOO, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'A1'
                super(Statechart_1.FOO.A, self).__init__(**kwargs)

            class A1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.A.A1, self).__init__(**kwargs)
    
            class Z(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.A.Z, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'B1'
                super(Statechart_1.FOO.B, self).__init__(**kwargs)

            class B1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.B.B1, self).__init__(**kwargs)
    
            class Z(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.B.Z, self).__init__(**kwargs)

    class BAR(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'X'
            super(Statechart_1.BAR, self).__init__(**kwargs)

        class X(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'X1'
                super(Statechart_1.BAR.X, self).__init__(**kwargs)

            class X1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.X.X1, self).__init__(**kwargs)
    
            class Z(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.X.Z, self).__init__(**kwargs)

        class Y(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'Y1'
                super(Statechart_1.BAR.Y, self).__init__(**kwargs)

            class Y1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.Y.Y1, self).__init__(**kwargs)
    
            class Z(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.Y.Z, self).__init__(**kwargs)

    class X(State):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_1.X, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'A1'
                super(Statechart_1.X.A, self).__init__(**kwargs)

            class A1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.X.A.A1, self).__init__(**kwargs)
    
            class Z(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.X.A.Z, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'B1'
                super(Statechart_1.X.B, self).__init__(**kwargs)

            class B1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.X.B.B1, self).__init__(**kwargs)
    
            class Z(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.X.B.Z, self).__init__(**kwargs)

class CallbackManager_1:
    def __init__(self):
        self.callback_state = None
        self.callback_value = None
        self.callback_keys = None

    def callback_func(self, state, value, keys):
        self.callback_state = state
        self.callback_value = value
        self.callback_keys = keys

class CallbackManager_2:
    def __init__(self):
        self.callback_state = None
        self.callback_value = None
        self.callback_keys = None

    def callback_func(self, state, value, keys):
        self.callback_state = state
        self.callback_value = value
        self.callback_keys = keys

class StateGetSubstateTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global root_state_1

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        
    # Get immediate substates from root state
    def test_get_immediate_substates_from_root_state(self):
        state = root_state_1.get_substate('FOO')
        self.assertEqual(state.full_path, 'FOO')

        state = root_state_1.get_substate('self.FOO')
        self.assertEqual(state.full_path, 'FOO')

        state = root_state_1.get_substate('BAR')
        self.assertEqual(state.full_path, 'BAR')

        state = root_state_1.get_substate('self.BAR')
        self.assertEqual(state.full_path, 'BAR')

        print 'expecting error message...'
        state = root_state_1.get_substate('WRONG') # [PORT] javascript version had x, which is valid
        self.assertIsNone(state)

        state = root_state_1.get_substate('self.X')
        self.assertEqual(state.full_path, 'X')

    # Get immediate substates from bar state
    def test_get_immediate_substates_from_foo_state(self):
        foo = root_state_1.get_substate('FOO')

        state = foo.get_substate('A')
        self.assertEqual(state.full_path, 'FOO.A')

        state = foo.get_substate('self.A')
        self.assertEqual(state.full_path, 'FOO.A')

        state = foo.get_substate('B')
        self.assertEqual(state.full_path, 'FOO.B')

        state = foo.get_substate('self.B')
        self.assertEqual(state.full_path, 'FOO.B')

        state = foo.get_substate('MAH')
        self.assertIsNone(state)

        state = foo.get_substate('FOO')
        self.assertIsNone(state)

    # Get immediate substates from bar state
    def test_get_immediate_substates_from_bar_state(self):
        bar = root_state_1.get_substate('BAR')

        state = bar.get_substate('X')
        self.assertEqual(state.name, 'X')

        state = bar.get_substate('self.X')
        self.assertEqual(state.name, 'X')

        state = bar.get_substate('Y')
        self.assertEqual(state.name, 'Y')

        state = bar.get_substate('self.Y')
        self.assertEqual(state.name, 'Y')

        state = bar.get_substate('MAH')
        self.assertIsNone(state)

        state = bar.get_substate('BAR')
        self.assertIsNone(state)

    # Get substates from root state using full paths
    def test_get_substates_from_root_state_using_full_paths(self):
        state = root_state_1.get_substate('FOO.A')
        self.assertEqual(state.name, 'A')

        state = root_state_1.get_substate('FOO.B')
        self.assertEqual(state.name, 'B')

        state = root_state_1.get_substate('FOO.MAH')
        self.assertIsNone(state)

        state = root_state_1.get_substate('FOO.A.A1')
        self.assertEqual(state.name, 'A1')

        state = root_state_1.get_substate('FOO.A.Z')
        self.assertEqual(state.full_path, 'FOO.A.Z')

        state = root_state_1.get_substate('FOO.B.B1')
        self.assertEqual(state.name, 'B1')

        state = root_state_1.get_substate('FOO.B.Z')
        self.assertEqual(state.full_path, 'FOO.B.Z')

        state = root_state_1.get_substate('BAR.X')
        self.assertEqual(state.name, 'X')

        state = root_state_1.get_substate('BAR.Y')
        self.assertEqual(state.name, 'Y')

        state = root_state_1.get_substate('BAR.MAH')
        self.assertIsNone(state)

        state = root_state_1.get_substate('BAR.X.X1')
        self.assertEqual(state.name, 'X1')

        state = root_state_1.get_substate('BAR.X.Z')
        self.assertEqual(state.full_path, 'BAR.X.Z')

        state = root_state_1.get_substate('BAR.Y.Y1')
        self.assertEqual(state.name, 'Y1')

        state = root_state_1.get_substate('BAR.Y.Z')
        self.assertEqual(state.full_path, 'BAR.Y.Z')

        state = root_state_1.get_substate('X.A')
        self.assertEqual(state.full_path, 'X.A')

        state = root_state_1.get_substate('X.B')
        self.assertEqual(state.full_path, 'X.B')

        state = root_state_1.get_substate('X.A.A1')
        self.assertEqual(state.full_path, 'X.A.A1')

        state = root_state_1.get_substate('X.A.Z')
        self.assertEqual(state.full_path, 'X.A.Z')

        state = root_state_1.get_substate('X.B.B1')
        self.assertEqual(state.full_path, 'X.B.B1')

        state = root_state_1.get_substate('X.B.Z')
        self.assertEqual(state.full_path, 'X.B.Z')

    # Get substates from foo state using full paths
    def test_get_substates_from_foo_state_using_full_paths(self):
        foo = root_state_1.get_substate('FOO')

        state = foo.get_substate('A.A1')
        self.assertEqual(state.full_path, 'FOO.A.A1')

        state = foo.get_substate('self.A.A1')
        self.assertEqual(state.full_path, 'FOO.A.A1')

        state = foo.get_substate('A.Z')
        self.assertEqual(state.full_path, 'FOO.A.Z')

        state = foo.get_substate('self.A.Z')
        self.assertEqual(state.full_path, 'FOO.A.Z')

        state = foo.get_substate('MAH.Z')
        self.assertIsNone(state)

        state = foo.get_substate('FOO.Z')
        self.assertIsNone(state)
  
    # Get unambiguous substates from foo state using state names
    def test_get_unambiguous_substates_from_foo_state_using_state_names(self):
        foo = root_state_1.get_substate('FOO')

        state = foo.get_substate('A1')
        self.assertEqual(state.name, 'A1')

        state = foo.get_substate('B1')
        self.assertEqual(state.name, 'B1')

    # Get unambiguous substates from foo state using full paths
    def test_get_unambiguous_substates_from_foo_state_using_full_paths(self):
        foo = root_state_1.get_substate('FOO')

        state = foo.get_substate('A1')
        self.assertEqual(state.full_path, 'FOO.A.A1')

        state = foo.get_substate('B1')
        self.assertEqual(state.full_path, 'FOO.B.B1')

    # get z substates from foo state
    def test_z_substates_from_foo_state(self):
        foo = root_state_1.get_substate('FOO')

        with self.assertRaises(Exception) as cm:
            state = foo.get_substate('Z')
        msg = ("Cannot find substate matching 'Z' in state FOO. Ambiguous "
               "with the following: B.Z, A.Z")
        self.assertEqual(str(cm.exception), msg)

        state = foo.get_substate('A~Z')
        self.assertEqual(state.full_path, 'FOO.A.Z')

        state = foo.get_substate('B~Z')
        self.assertEqual(state.full_path, 'FOO.B.Z')

        state = root_state_1.get_substate('FOO.A~Z')
        self.assertEqual(state.full_path, 'FOO.A.Z')

        state = root_state_1.get_substate('FOO.B~Z')
        self.assertEqual(state.full_path, 'FOO.B.Z')


    # Get z substate from y state
    def test_z_substate_from_y_state(self):
        foo = root_state_1.get_substate('Y')

        state = root_state_1.get_substate('Y.Z')
        self.assertEqual(state.full_path, 'BAR.Y.Z')

    # Get A1 substate from Y state
    def test_a1_substate_from_y_state(self):
        with self.assertRaises(Exception) as cm:
            state = root_state_1.get_substate('A1')
        msg = ("Cannot find substate matching 'A1' in state __ROOT_STATE__. "
               "Ambiguous with the following: X.A.A1, FOO.A.A1")
        self.assertEqual(str(cm.exception), msg)

        state = root_state_1.get_substate('FOO~A1')
        self.assertEqual(state.full_path, 'FOO.A.A1')
  
        state = root_state_1.get_substate('FOO~A.A1')
        self.assertEqual(state.full_path, 'FOO.A.A1')
  
        state = root_state_1.get_substate('X~A1')
        self.assertEqual(state.full_path, 'X.A.A1')
  
        state = root_state_1.get_substate('X~A.A1')
        self.assertEqual(state.full_path, 'X.A.A1')

    # Get non-existing substate 'abc' using callback
    def test_get_non_existing_substate_abc_using_callback(self):
        callback_manager = CallbackManager_1()

        result = root_state_1.get_substate('ABC', callback_manager.callback_func)
        self.assertIsNone(result)
        self.assertEqual(callback_manager.callback_state, root_state_1)
        self.assertEqual(callback_manager.callback_value, 'ABC')
        self.assertIsNone(callback_manager.callback_keys)

    # Get ambiguous substate 'A1' with using callback
    def test_get_ambiguous_substate_x_with_callback(self):
        callback_manager = CallbackManager_1()

        result = root_state_1.get_substate('A1', callback_manager.callback_func)

        self.assertIsNone(result)
        self.assertEqual(callback_manager.callback_state, root_state_1)
        self.assertEqual(callback_manager.callback_value, 'A1')
        self.assertEqual(len(callback_manager.callback_keys), 2)
        print callback_manager.callback_keys
        self.assertTrue('X.A.A1' in callback_manager.callback_keys)
        self.assertTrue('FOO.A.A1' in callback_manager.callback_keys)

    def test_trying_to_get_substate_with_wrong_type(self):
        value_of_wrong_type = {'key': 1}

        with self.assertRaises(Exception) as cm:
            root_state_1.get_substate(value_of_wrong_type)

        msg = ("Cannot find matching substate. value must be a State "
               "class or string, not type: {0}").format(type(value_of_wrong_type))
        self.assertEqual(str(cm.exception), msg)







