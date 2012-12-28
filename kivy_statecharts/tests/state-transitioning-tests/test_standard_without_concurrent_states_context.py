'''
Statechart tests, transitioning, standard, without concurrent, context
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.history_state import HistoryState
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

"""
  Constants used during the state transition process
"""
EXIT_STATE = 0
ENTER_STATE = 1


class TestState(State):
    enter_stateContext = ObjectProperty(None)
    exit_stateContext = ObjectProperty(None)
      
    def __init__(self, **kwargs):
        super(TestState, self).__init__(**kwargs)

    def enter_state(self, context):
        self.enter_stateContext = context
      
    def exit_state(self, context):
        self.exit_stateContext = context


class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['root_state_class'] = self.RootState
        kwargs['monitor_is_active'] = True
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(TestState):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(TestState):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'C'
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

            class C(TestState):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.C, self).__init__(**kwargs)

            class D(TestState):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.A.D, self).__init__(**kwargs)

        class B(TestState):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'E'
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

            class E(TestState):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.E, self).__init__(**kwargs)

            class F(TestState):
                def __init__(self, **kwargs):
                    super(Statechart_1.RootState.B.F, self).__init__(**kwargs)

class TestState_2(State):
    enter_stateContext = ObjectProperty(None)
    exit_stateContext = ObjectProperty(None)
      
    def __init__(self, **kwargs):
        super(TestState_2, self).__init__(**kwargs)

    def enter_state(self, context):
        # Cause a delay.
        i = 0
        while i < 10000:
            j = i * 1
            i += 1
        self.enter_stateContext = context
      
    def exit_state(self, context):
        self.exit_stateContext = context

class Statechart_2(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['root_state_class'] = self.RootState
        kwargs['monitor_is_active'] = True
        kwargs['trace'] = True
        super(Statechart_2, self).__init__(**kwargs)

    class RootState(TestState_2):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            super(Statechart_2.RootState, self).__init__(**kwargs)

        class A(TestState_2):
            def __init__(self, **kwargs):
                kwargs['initial_substate_key'] = 'B'
                super(Statechart_2.RootState.A, self).__init__(**kwargs)

            class B(TestState_2):
                def __init__(self, **kwargs):
                    kwargs['initial_substate_key'] = 'C'
                    super(Statechart_2.RootState.A.B, self).__init__(**kwargs)

                class C(TestState_2):
                    def __init__(self, **kwargs):
                        kwargs['initial_substate_key'] = 'D'
                        super(Statechart_2.RootState.A.B.C, self).__init__(**kwargs)

                    class D(TestState_2):
                        def __init__(self, **kwargs):
                            kwargs['initial_substate_key'] = 'E'
                            super(Statechart_2.RootState.A.B.C.D, self).__init__(**kwargs)

                        class E(TestState_2):
                            def __init__(self, **kwargs):
                                kwargs['initial_substate_key'] = 'F'
                                super(Statechart_2.RootState.A.B.C.D.E, self).__init__(**kwargs)

                            class F(TestState_2):
                                def __init__(self, **kwargs):
                                    kwargs['initial_substate_key'] = 'G'
                                    super(Statechart_2.RootState.A.B.C.D.E.F, self).__init__(**kwargs)

                                class G(TestState_2):
                                    def __init__(self, **kwargs):
                                        kwargs['initial_substate_key'] = 'H'
                                        super(Statechart_2.RootState.A.B.C.D.E.F.G, self).__init__(**kwargs)

                                    class H(TestState_2):
                                        def __init__(self, **kwargs):
                                            super(Statechart_2.RootState.A.B.C.D.E.F.G.H, self).__init__(**kwargs)
        class X(TestState_2):
            def __init__(self, **kwargs):
                super(Statechart_2.RootState.X, self).__init__(**kwargs)


# For testing special case with _traverse_states_to_enter()
class Statechart_3(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['root_state_class'] = self.RootState
        kwargs['monitor_is_active'] = True
        kwargs['trace'] = True
        super(Statechart_3, self).__init__(**kwargs)

    class RootState(TestState_2):
        def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'A'
            kwargs['is_recursive'] = True
            super(Statechart_3.RootState, self).__init__(**kwargs)

        class A(HistoryState):
            def __init__(self, **kwargs):
                super(Statechart_3.RootState.A, self).__init__(**kwargs)


class StateTransitioningStandardContextWithoutConcurrentTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global root_state_1
        global monitor_1
        global state_A
        global state_B
        global state_C
        global state_D
        global state_E
        global state_F

        global context

        context = { 'foo': 100 }

        statechart_1 = Statechart_1()
        statechart_1.init_statechart()
        root_state_1 = statechart_1.root_state_instance
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        state_C = statechart_1.get_state('C')
        state_D = statechart_1.get_state('D')
        state_E = statechart_1.get_state('E')
        state_F = statechart_1.get_state('F')

    # Check statechart initializaton
    def test_statechart_initializaton(self):
        self.assertIsNone(root_state_1.enter_stateContext)
        self.assertIsNone(state_A.enter_stateContext)
        self.assertIsNone(state_C.enter_stateContext)

    # Pass no context when going to state f using statechart
    def test_pass_no_context_when_going_to_state_f_using_statechart(self):
        statechart_1.go_to_state('F')
        self.assertTrue(state_F.is_current_state())
        self.assertIsNone(state_C.exit_stateContext)
        self.assertIsNone(state_A.exit_stateContext)
        self.assertIsNone(state_B.enter_stateContext)
        self.assertIsNone(state_F.enter_stateContext)

    # Pass no context when going to state f using state
    def test_pass_no_context_when_going_to_state_f_using_state(self):
        state_C.go_to_state('F')
        self.assertTrue(state_F.is_current_state())
        self.assertIsNone(state_C.exit_stateContext)
        self.assertIsNone(state_A.exit_stateContext)
        self.assertIsNone(state_B.enter_stateContext)
        self.assertIsNone(state_F.enter_stateContext)

    # Pass context when going to state f using statechart - go_to_state('f', context)
    def test_pass_context_when_going_to_state_f_using_statechart_go_to_state_f_context(self):
        statechart_1.go_to_state('F', context=context)
        self.assertTrue(state_F.is_current_state())
        self.assertEqual(state_C.exit_stateContext, context)
        self.assertEqual(state_A.exit_stateContext, context)
        self.assertEqual(state_B.enter_stateContext, context)
        self.assertEqual(state_F.enter_stateContext, context)

    # Pass context when going to state f using state - go_to_state('f', context)
    def test_pass_context_when_going_to_state_f_using_state_go_to_state_f_context(self):
        state_C.go_to_state('F', context=context)
        self.assertTrue(state_F.is_current_state())
        self.assertEqual(state_C.exit_stateContext, context)
        self.assertEqual(state_A.exit_stateContext, context)
        self.assertEqual(state_B.enter_stateContext, context)
        self.assertEqual(state_F.enter_stateContext, context)

    # Pass context when going to state f using statechart - go_to_state('f', state_C, context)
    def test_pass_context_when_going_to_state_f_using_statechart_go_to_state_f_state_C_context(self):
        statechart_1.go_to_state('F', from_current_state=state_C, context=context)
        self.assertTrue(state_F.is_current_state())
        self.assertEqual(state_C.exit_stateContext, context)
        self.assertEqual(state_A.exit_stateContext, context)
        self.assertEqual(state_B.enter_stateContext, context)
        self.assertEqual(state_F.enter_stateContext, context)

    # Pass context when going to state f using statechart - go_to_state('f', false, context)
    def test_pass_context_when_going_to_state_f_using_statechart_go_to_state_f_false_context(self):
        statechart_1.go_to_state('F', use_history=False, context=context)
        self.assertTrue(state_F.is_current_state())
        self.assertEqual(state_C.exit_stateContext, context)
        self.assertEqual(state_A.exit_stateContext, context)
        self.assertEqual(state_B.enter_stateContext, context)
        self.assertEqual(state_F.enter_stateContext, context)

    # Pass context when going to state f using statechart - go_to_state('f', state_C, false, context)
    def test_pass_context_when_going_to_state_f_using_statechart_go_to_state_f_state_C_false_context(self):
        statechart_1.go_to_state('F', from_current_state=state_C, use_history=False, context=context)
        self.assertTrue(state_F.is_current_state())
        self.assertEqual(state_C.exit_stateContext, context)
        self.assertEqual(state_A.exit_stateContext, context)
        self.assertEqual(state_B.enter_stateContext, context)
        self.assertEqual(state_F.enter_stateContext, context)

    def test_calling_go_to_with_suspension_and_resume_to_trigger_pending_code(self):
        statechart_2 = Statechart_2()
        statechart_2.init_statechart()
        root_state_2 = statechart_2.root_state_instance
        monitor_2 = statechart_2.monitor
        state_A = statechart_2.get_state('A')
        state_B = statechart_2.get_state('B')
        state_C = statechart_2.get_state('C')
        state_D = statechart_2.get_state('D')
        state_E = statechart_2.get_state('E')
        state_F = statechart_2.get_state('F')
        state_G = statechart_2.get_state('G')
        state_H = statechart_2.get_state('H')
        state_X = statechart_2.get_state('X')

        self.assertTrue(state_H.is_current_state())
        statechart_2.go_to_state('X', from_current_state=state_H, use_history=False, context=context)
        self.assertTrue(state_X.is_current_state())

        actions = []
        actions.append({ 'action': EXIT_STATE, 'state': state_H })
        actions.append({ 'action': EXIT_STATE, 'state': state_G })
        actions.append({ 'action': EXIT_STATE, 'state': state_F })
        actions.append({ 'action': EXIT_STATE, 'state': state_E })
        actions.append({ 'action': EXIT_STATE, 'state': state_D })
        actions.append({ 'action': EXIT_STATE, 'state': state_C })
        actions.append({ 'action': EXIT_STATE, 'state': state_B })
        actions.append({ 'action': EXIT_STATE, 'state': state_A })
        actions.append({ 'action': ENTER_STATE, 'state': state_X, 'current_state': True })

        statechart_2.go_to_state_locked = True

        statechart_2.go_to_state_suspended_point = {
            'go_to_state': state_X,
            'actions': actions,
            'marker': None,
            'context': {}
        }

        statechart_2.go_to_state_suspended = True

        statechart_2.go_to_state('A.B.C.D.E.F.G.H', from_current_state=state_X, use_history=False, context=context)
        statechart_2.go_to_state('X', from_current_state=state_H, use_history=False, context=context)
        statechart_2.go_to_state('A.B.C.D.E.F.G.H', from_current_state=state_X, use_history=False, context=context)
        statechart_2.go_to_state('X', from_current_state=state_H, use_history=False, context=context)
        statechart_2.go_to_state('A.B.C.D.E.F.G.H', from_current_state=state_X, use_history=False, context=context)
        statechart_2.resume_go_to_state()

        statechart_2.go_to_state('X', from_current_state=state_H, use_history=False, context=context)
        self.assertTrue(state_X.is_current_state())
        
        # While we are here, test _create_state_chain()
        state_chain_to_H = statechart_2._create_state_chain(state_H)
        self.assertEqual(len(state_chain_to_H), 9)

    # Test special case for hitting code in _traverse_states_to_enter, when
    # the initial substate is a history state, with is_recursive True.
    # Also, call this function with no args.
    def test_calling_traverse_states_to_enter(self):
        statechart_3 = Statechart_3()
        statechart_3.init_statechart()
        root_state_3 = statechart_3.root_state_instance
        monitor_3 = statechart_3.monitor
        state_A = statechart_3.get_state('A')

        #self.assertTrue(root_state_3.is_current_state())

        # Hit the code for no args (no state).
        statechart_3._traverse_states_to_enter(None, None, None, None, None)

        enter_state_path = None 
        pivot_state = None
        use_history = False
        go_to_state_actions = []

        # state_A has is_recursive = True
        statechart_3._traverse_states_to_enter(root_state_3, enter_state_path, pivot_state,
                                  use_history, go_to_state_actions)
 
