'''
Statechart tests, get substate
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['initialStateKey'] = 'FOO'
        super(Statechart_1, self).__init__(**kwargs)

    class FOO(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
            super(Statechart_1.FOO, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'A1'
                super(Statechart_1.FOO.A, self).__init__(**kwargs)

            class A1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.A.A1, self).__init__(**kwargs)
    
            class Z(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.A.Z, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'B1'
                super(Statechart_1.FOO.B, self).__init__(**kwargs)

            class B1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.B.B1, self).__init__(**kwargs)
    
            class Z(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.FOO.B.Z, self).__init__(**kwargs)

    class BAR(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'X'
            super(Statechart_1.BAR, self).__init__(**kwargs)

        class X(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'X1'
                super(Statechart_1.BAR.X, self).__init__(**kwargs)

            class X1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.X.X1, self).__init__(**kwargs)
    
            class Z(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.X.Z, self).__init__(**kwargs)

        class Y(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'Y1'
                super(Statechart_1.BAR.Y, self).__init__(**kwargs)

            class Y1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.Y.Y1, self).__init__(**kwargs)
    
            class Z(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.BAR.Y.Z, self).__init__(**kwargs)

    class X(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
            super(Statechart_1.X, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'A1'
                super(Statechart_1.X.A, self).__init__(**kwargs)

            class A1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.X.A.A1, self).__init__(**kwargs)
    
            class Z(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.X.A.Z, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'B1'
                super(Statechart_1.X.B, self).__init__(**kwargs)

            class B1(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.X.B.B1, self).__init__(**kwargs)
    
            class Z(State):
                def __init__(self, **kwargs):
                    super(Statechart_1.X.B.Z, self).__init__(**kwargs)

class CallbackManager_1:
    def __init__(self):
        self.callbackState = None
        self.callbackValue = None
        self.callbackKeys = None

    def callbackFunc(self, state, value, keys):
        self.callbackState = state
        self.callbackValue = value
        self.callbackKeys = keys

class StateGetSubstateTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global rootState_1

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootStateInstance
        
    # Get immediate substates from root state
    def test_get_immediate_substates_from_root_state(self):
        state = rootState_1.getSubstate('FOO')
        self.assertEqual(state.fullPath, 'FOO')

        state = rootState_1.getSubstate('self.FOO')
        self.assertEqual(state.fullPath, 'FOO')

        state = rootState_1.getSubstate('BAR')
        self.assertEqual(state.fullPath, 'BAR')

        state = rootState_1.getSubstate('self.BAR')
        self.assertEqual(state.fullPath, 'BAR')

        print 'expecting error message...'
        state = rootState_1.getSubstate('WRONG') # [PORT] javascript version had x, which is valid
        self.assertIsNone(state)

        state = rootState_1.getSubstate('self.X')
        self.assertEqual(state.fullPath, 'X')

    # Get immediate substates from bar state
    def test_get_immediate_substates_from_foo_state(self):
        foo = rootState_1.getSubstate('FOO')

        state = foo.getSubstate('A')
        self.assertEqual(state.fullPath, 'FOO.A')

        state = foo.getSubstate('self.A')
        self.assertEqual(state.fullPath, 'FOO.A')

        state = foo.getSubstate('B')
        self.assertEqual(state.fullPath, 'FOO.B')

        state = foo.getSubstate('self.B')
        self.assertEqual(state.fullPath, 'FOO.B')

        state = foo.getSubstate('MAH')
        self.assertIsNone(state)

        state = foo.getSubstate('FOO')
        self.assertIsNone(state)

    # Get immediate substates from bar state
    def test_get_immediate_substates_from_bar_state(self):
        bar = rootState_1.getSubstate('BAR')

        state = bar.getSubstate('X')
        self.assertEqual(state.name, 'X')

        state = bar.getSubstate('self.X')
        self.assertEqual(state.name, 'X')

        state = bar.getSubstate('Y')
        self.assertEqual(state.name, 'Y')

        state = bar.getSubstate('self.Y')
        self.assertEqual(state.name, 'Y')

        state = bar.getSubstate('MAH')
        self.assertIsNone(state)

        state = bar.getSubstate('BAR')
        self.assertIsNone(state)

    # Get substates from root state using full paths
    def test_get_substates_from_root_state_using_full_paths(self):
        state = rootState_1.getSubstate('FOO.A')
        self.assertEqual(state.name, 'A')

        state = rootState_1.getSubstate('FOO.B')
        self.assertEqual(state.name, 'B')

        state = rootState_1.getSubstate('FOO.MAH')
        self.assertIsNone(state)

        state = rootState_1.getSubstate('FOO.A.A1')
        self.assertEqual(state.name, 'A1')

        state = rootState_1.getSubstate('FOO.A.Z')
        self.assertEqual(state.fullPath, 'FOO.A.Z')

        state = rootState_1.getSubstate('FOO.B.B1')
        self.assertEqual(state.name, 'B1')

        state = rootState_1.getSubstate('FOO.B.Z')
        self.assertEqual(state.fullPath, 'FOO.B.Z')

        state = rootState_1.getSubstate('BAR.X')
        self.assertEqual(state.name, 'X')

        state = rootState_1.getSubstate('BAR.Y')
        self.assertEqual(state.name, 'Y')

        state = rootState_1.getSubstate('BAR.MAH')
        self.assertIsNone(state)

        state = rootState_1.getSubstate('BAR.X.X1')
        self.assertEqual(state.name, 'X1')

        state = rootState_1.getSubstate('BAR.X.Z')
        self.assertEqual(state.fullPath, 'BAR.X.Z')

        state = rootState_1.getSubstate('BAR.Y.Y1')
        self.assertEqual(state.name, 'Y1')

        state = rootState_1.getSubstate('BAR.Y.Z')
        self.assertEqual(state.fullPath, 'BAR.Y.Z')

        state = rootState_1.getSubstate('X.A')
        self.assertEqual(state.fullPath, 'X.A')

        state = rootState_1.getSubstate('X.B')
        self.assertEqual(state.fullPath, 'X.B')

        state = rootState_1.getSubstate('X.A.A1')
        self.assertEqual(state.fullPath, 'X.A.A1')

        state = rootState_1.getSubstate('X.A.Z')
        self.assertEqual(state.fullPath, 'X.A.Z')

        state = rootState_1.getSubstate('X.B.B1')
        self.assertEqual(state.fullPath, 'X.B.B1')

        state = rootState_1.getSubstate('X.B.Z')
        self.assertEqual(state.fullPath, 'X.B.Z')

    # Get substates from foo state using full paths
    def test_get_substates_from_foo_state_using_full_paths(self):
        foo = rootState_1.getSubstate('FOO')

        state = foo.getSubstate('A.A1')
        self.assertEqual(state.fullPath, 'FOO.A.A1')

        state = foo.getSubstate('self.A.A1')
        self.assertEqual(state.fullPath, 'FOO.A.A1')

        state = foo.getSubstate('A.Z')
        self.assertEqual(state.fullPath, 'FOO.A.Z')

        state = foo.getSubstate('self.A.Z')
        self.assertEqual(state.fullPath, 'FOO.A.Z')

        state = foo.getSubstate('MAH.Z')
        self.assertIsNone(state)

        state = foo.getSubstate('FOO.Z')
        self.assertIsNone(state)
  
    # Get unambiguous substates from foo state using state names
    def test_get_unambiguous_substates_from_foo_state_using_state_names(self):
        foo = rootState_1.getSubstate('FOO')

        state = foo.getSubstate('A1')
        self.assertEqual(state.name, 'A1')

        state = foo.getSubstate('B1')
        self.assertEqual(state.name, 'B1')

    # Get unambiguous substates from foo state using full paths
    def test_get_unambiguous_substates_from_foo_state_using_full_paths(self):
        foo = rootState_1.getSubstate('FOO')

        state = foo.getSubstate('A1')
        self.assertEqual(state.fullPath, 'FOO.A.A1')

        state = foo.getSubstate('B1')
        self.assertEqual(state.fullPath, 'FOO.B.B1')

    # get z substates from foo state
    def test_z_substates_from_foo_state(self):
        foo = rootState_1.getSubstate('FOO')

        state = foo.getSubstate('Z')
        self.assertIsNone(state)

        state = foo.getSubstate('A~Z')
        self.assertEqual(state.fullPath, 'FOO.A.Z')

        state = foo.getSubstate('B~Z')
        self.assertEqual(state.fullPath, 'FOO.B.Z')

        state = rootState_1.getSubstate('FOO.A~Z')
        self.assertEqual(state.fullPath, 'FOO.A.Z')

        state = rootState_1.getSubstate('FOO.B~Z')
        self.assertEqual(state.fullPath, 'FOO.B.Z')


    # Get z substate from y state
    def test_z_substate_from_y_state(self):
        foo = rootState_1.getSubstate('Y')

        state = rootState_1.getSubstate('Y.Z')
        self.assertEqual(state.fullPath, 'BAR.Y.Z')

    # Get A1 substate from Y state
    def test_a1_substate_from_y_state(self):
        print 'expecting an error message...'
        state = rootState_1.getSubstate('A1')
        self.assertIsNone(state)

        state = rootState_1.getSubstate('FOO~A1')
        self.assertEqual(state.fullPath, 'FOO.A.A1')
  
        state = rootState_1.getSubstate('FOO~A.A1')
        self.assertEqual(state.fullPath, 'FOO.A.A1')
  
        state = rootState_1.getSubstate('X~A1')
        self.assertEqual(state.fullPath, 'X.A.A1')
  
        state = rootState_1.getSubstate('X~A.A1')
        self.assertEqual(state.fullPath, 'X.A.A1')

    # Get non-existing substate 'abc' using callback
    def test_get_non_existing_substate_abc_using_callback(self):
        callbackManager = CallbackManager_1()

        result = rootState_1.getSubstate('ABC', callbackManager.callbackFunc)
        self.assertIsNone(result)
        self.assertEqual(callbackManager.callbackState, rootState_1)
        self.assertEqual(callbackManager.callbackValue, 'ABC')
        self.assertIsNone(callbackManager.callbackKeys)

    # Get ambiguous substate 'x' with using callback
    #def test_get_ambiguous_substate_x_with_callback(self):
        #callbackManager = CallbackManager_1()

        # [PORT] The javascript version treats X as ambiguous -- there is an X
        #        as a direct substate of root, and another X that is a substate
        #        as root.BAR.X. In the python version, root.getSubstate('X') will
        #        not be ambiguous, as the direct substate X will be returned.
        #
        #        So, this test is ignored, and the previous will be deemed sufficient.
        #
        #result = rootState_1.getSubstate('X', callbackManager.callbackFunc)
        #print callbackManager.callbackKeys
        #self.assertIsNone(result)
        #self.assertEqual(callbackManager.callbackState, rootState_1)
        #self.assertEqual(callbackManager.callbackValue, 'X')
        #self.assertEqual(len(callbackManager.callbackKeys), 2)
        #self.assertTrue('X' in callbackManager.callbackKeys)
        #self.assertTrue('BAR.X' in callbackManager.callbackKeys)








