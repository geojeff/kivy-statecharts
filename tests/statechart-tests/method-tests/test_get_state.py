'''
Statechart tests, getState
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
        kwargs['rootStateClass'] = self.RootState
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['value'] = 'state A'
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['value'] = 'state B'
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

class Statechart_2(StatechartManager):
    def __init__(self, **kwargs):
        self.rootStateClass = self.RootState
        super(Statechart_2, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            self.initialSubstateKey = 'A'
            super(Statechart_2.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['value'] = 'state A'
                self.initialSubstateKey = 'C'
                super(Statechart_2.RootState.A, self).__init__(**kwargs)

            class C(State):
                def __init__(self, **kwargs):
                    kwargs['value'] = 'state C'
                    super(Statechart_2.RootState.A.C, self).__init__(**kwargs)

            class D(State):
                def __init__(self, **kwargs):
                    kwargs['value'] = 'state D'
                    super(Statechart_2.RootState.A.D, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['value'] = 'state B'
                self.initialSubstateKey = 'E'
                super(Statechart_2.RootState.B, self).__init__(**kwargs)

            class E(State):
                def __init__(self, **kwargs):
                    kwargs['value'] = 'state E'
                    super(Statechart_2.RootState.B.E, self).__init__(**kwargs)

            class F(State):
                def __init__(self, **kwargs):
                    kwargs['value'] = 'state F'
                    super(Statechart_2.RootState.B.F, self).__init__(**kwargs)

class Statechart_3(StatechartManager):
    def __init__(self, **kwargs):
        self.rootStateClass = self.RootState
        super(Statechart_3, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            self.initialSubstateKey = 'A'
            super(Statechart_3.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['value'] = 'state A'
                super(Statechart_3.RootState.A, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['value'] = 'state B'
                self.initialSubstateKey = 'A'
                super(Statechart_3.RootState.B, self).__init__(**kwargs)

            class A(State):
                def __init__(self, **kwargs):
                    kwargs['value'] = 'state B.A'
                    super(Statechart_3.RootState.B.A, self).__init__(**kwargs)
    
            class C(State):
                def __init__(self, **kwargs):
                    kwargs['value'] = 'state C'
                    self.initialSubstateKey = 'A'
                    super(Statechart_3.RootState.B.C, self).__init__(**kwargs)

                class A(State):
                    def __init__(self, **kwargs):
                        kwargs['value'] = 'state B.C.A'
                        super(Statechart_3.RootState.B.C.A, self).__init__(**kwargs)

                class D(State):
                    def __init__(self, **kwargs):
                        kwargs['value'] = 'state D'
                        super(Statechart_3.RootState.B.C.D, self).__init__(**kwargs)

class Statechart_4(StatechartManager):
    def __init__(self, **kwargs):
        self.rootStateClass = self.RootState
        super(Statechart_4, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            self.initialSubstateKey = 'A'
            super(Statechart_4.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                kwargs['value'] = 'state A'
                self.initialSubstateKey = 'X'
                super(Statechart_4.RootState.A, self).__init__(**kwargs)

            class X(State):
                def __init__(self, **kwargs):
                    kwargs['value'] = 'state A.X'
                    super(Statechart_4.RootState.A.X, self).__init__(**kwargs)
    
            class Y(State):
                def __init__(self, **kwargs):
                    kwargs['value'] = 'state A.Y'
                    super(Statechart_4.RootState.A.Y, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                kwargs['value'] = 'state B'
                self.initialSubstateKey = 'X'
                super(Statechart_4.RootState.B, self).__init__(**kwargs)

            class X(State):
                def __init__(self, **kwargs):
                    kwargs['value'] = 'state B.X'
                    super(Statechart_4.RootState.B.X, self).__init__(**kwargs)
    
            class Y(State):
                def __init__(self, **kwargs):
                    kwargs['value'] = 'state B.Y'
                    super(Statechart_4.RootState.B.Y, self).__init__(**kwargs)

class StatechartGetStateTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global statechart_2
        global statechart_3
        global statechart_4

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        statechart_2 = Statechart_2()
        statechart_2.initStatechart()
        statechart_3 = Statechart_3()
        statechart_3.initStatechart()
        statechart_4 = Statechart_4()
        statechart_4.initStatechart()
        
    def test_access_states_statechart_1(self):
        state = statechart_1.getState('A')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state A') 

        state = statechart_1.getState('B')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state B') 

    def test_access_states_statechart_2(self):
        state = statechart_2.getState('A')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state A') 

        state = statechart_2.getState('B')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state B') 

        state = statechart_2.getState('C')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state C') 

        state = statechart_2.getState('D')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state D') 

        state = statechart_2.getState('E')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state E') 

        state = statechart_2.getState('F')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state F') 

        state = statechart_2.getState('A.C')
        self.assertIsNotNone(state)
        self.assertEqual(state, statechart_2.getState('C'))
        self.assertEqual(state.value, 'state C')

        state = statechart_2.getState('A.D')
        self.assertIsNotNone(state)
        self.assertEqual(state, statechart_2.getState('D'))
        self.assertEqual(state.value, 'state D')

        state = statechart_2.getState('B.E')
        self.assertIsNotNone(state)
        self.assertEqual(state, statechart_2.getState('E'))
        self.assertEqual(state.value, 'state E')

        state = statechart_2.getState('B.F')
        self.assertIsNotNone(state)
        self.assertEqual(state, statechart_2.getState('F'))
        self.assertEqual(state.value, 'state F')

    def test_access_states_statechart_3(self):
        state = statechart_3.getState('A')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state A') 

        state = statechart_3.getState('B.A')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state B.A') 

        state = statechart_3.getState('B.C.A')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state B.C.A') 

    def test_access_states_statechart_4(self):
        state_A = statechart_4.getState('A')
        state_B = statechart_4.getState('B')
      
        state = statechart_4.getState('A')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state A') 
  
        state = statechart_4.getState('A.X')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state A.X') 
  
        state = statechart_4.getState('A.Y')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state A.Y') 
  
        state = statechart_4.getState('B')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state B') 
  
        state = statechart_4.getState('B.X')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state B.X') 
  
        state = statechart_4.getState('B.Y')
        self.assertIsNotNone(state)
        self.assertEqual(state.value, 'state B.Y') 
  
        print 'expecting to get an error message...'
        state = statechart_4.getState('X')
        self.assertIsNone(state)
  
        print 'expecting to get an error message...'
        state = statechart_4.getState('Y')
        self.assertIsNone(state)


