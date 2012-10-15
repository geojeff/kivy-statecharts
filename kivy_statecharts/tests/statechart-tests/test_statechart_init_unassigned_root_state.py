'''
Statechart tests, init with assigned root state
===========
'''

import unittest

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

import os, inspect

owner = ObjectProperty(None)

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['A'] = self.A
        kwargs['B'] = self.B
        kwargs['initial_state_key'] = 'A'
        super(Statechart_1, self).__init__(**kwargs)

    class A(State):
        def foo(self, *l):
            self.statechart.go_to_state('B') # [PORT] self.go_to_state should work...

    class B(State):
        def bar(self, *l):
            self.statechart.go_to_state('A')

class C(State):
    def foo(self, *l):
        self.statechart.go_to_state('D') # [PORT] self.go_to_state should work...

class D(State):
    def bar(self, *l):
        self.statechart.go_to_state('C')

class Statechart_2(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['states_are_concurrent'] = True
        super(Statechart_2, self).__init__(**kwargs)

    C = C
    D = D

class RootStateExampleClass(State):
    def __init__(self, **kwargs):
        kwargs['test'] = 'foo'
        super(RootStateExampleClass, self).__init__(**kwargs) 

class E(State):
    pass

class Statechart_3(StatechartManager):
    def __init__(self):
        attrs = { 
            'owner': owner,
            'root_state_example_class': RootStateExampleClass,
            'initial_state_key': 'E',
            'E': E
            }
        super(Statechart_3, self).__init__(**attrs) 

class F(State):
    pass

class Statechart_4(StatechartManager):
    def __init__(self):
        attrs = { 
            'auto_init_statechart': False,
            'root_state_example_class': RootStateExampleClass,
            'initial_state_key': 'F',
            'F': F
            }
        super(Statechart_4, self).__init__(**attrs) 

class InvalidRootStateExampleClass(object):
    pass

class Statechart_5(StatechartManager):
    def __init__(self):
        attrs = { 
            'auto_init_statechart': False,
            'root_state_example_class': InvalidRootStateExampleClass,
            'initial_state_key': 'F',
            'F': F
            }
        super(Statechart_5, self).__init__(**attrs) 

class Statechart_6(StatechartManager):
    def __init__(self):
        attrs = { 
            'auto_init_statechart': False,
            'root_state_example_class': RootStateExampleClass,
            'initial_state_key': 'F',
            'F': F,
            'states_are_concurrent': True
            }
        super(Statechart_6, self).__init__(**attrs) 

#Statechart_1 = StatechartManager(**{
#    'initial_state_key': 'A',
#    'A': State(**{ 'foo': lambda self,*l: self.go_to_state('B')}),
#    'B': State(**{ 'bar': lambda self,*l: self.go_to_state('A')})
#    })

class TestApp(App):
    pass

class StatechartTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global statechart_2
        global statechart_3
        global statechart_4
        global root_state_1
        global root_state_2
        global root_state_3
        global state_A
        global state_B
        global state_C
        global state_D
        global state_E

        statechart_1 = Statechart_1()
        root_state_1 = statechart_1.root_state_instance
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        
        statechart_2 = Statechart_2()
        root_state_2 = statechart_2.root_state_instance
        state_C = statechart_2.get_state('C')
        state_D = statechart_2.get_state('D')

        statechart_3 = Statechart_3()
        root_state_3 = statechart_3.root_state_instance
        state_E = statechart_3.get_state('E')

        statechart_4 = Statechart_4()

    def test_statechart_1(self):
        self.assertTrue(statechart_1.is_statechart)
        self.assertTrue(statechart_1.statechart_is_initialized)
        self.assertTrue(isinstance(root_state_1, State))
        self.assertFalse(root_state_1.substates_are_concurrent)

        self.assertEqual(statechart_1.initial_state_key, state_A.name)
        self.assertEqual(root_state_1.initial_substate_key, 'A')
        self.assertEqual(state_A, root_state_1.get_substate('A'))
        self.assertEqual(state_B, root_state_1.get_substate('B'))
        
        self.assertEqual(root_state_1.owner, statechart_1)
        self.assertEqual(state_A.owner, statechart_1)
        self.assertEqual(state_B.owner, statechart_1)

        self.assertTrue(state_A.is_current_state())
        self.assertFalse(state_B.is_current_state())

        statechart_1.send_event('foo')

        self.assertFalse(state_A.is_current_state())
        self.assertTrue(state_B.is_current_state())

    def test_statechart_2(self):
        self.assertTrue(statechart_2.is_statechart)
        self.assertTrue(statechart_2.statechart_is_initialized)
        self.assertTrue(isinstance(root_state_2, State))
        self.assertTrue(root_state_2.substates_are_concurrent)

        self.assertEqual(statechart_2.initial_state_key, None)
        self.assertEqual(root_state_2.initial_substate_key, None)
        self.assertEqual(state_C, root_state_2.get_substate('C'))
        self.assertEqual(state_D, root_state_2.get_substate('D'))
        
        self.assertEqual(root_state_2.owner, statechart_2)
        self.assertEqual(state_C.owner, statechart_2)
        self.assertEqual(state_D.owner, statechart_2)

        self.assertTrue(state_C.is_current_state())
        self.assertTrue(state_D.is_current_state())

    def test_statechart_3(self):
        self.assertTrue(statechart_3.is_statechart)
        self.assertTrue(statechart_3.statechart_is_initialized)
        self.assertTrue(isinstance(root_state_3, RootStateExampleClass))
        self.assertFalse(root_state_3.substates_are_concurrent)
        
        self.assertEqual(root_state_3.owner, owner)
        self.assertEqual(state_E.owner, owner)

        self.assertEqual(statechart_3.initial_state_key, 'E')
        self.assertEqual(root_state_3.initial_substate_key, 'E')
        self.assertEqual(state_E, root_state_3.get_substate('E'))
        self.assertTrue(state_E.is_current_state())

    def test_statechart_4(self):
        self.assertTrue(statechart_4.is_statechart)
        self.assertFalse(statechart_4.statechart_is_initialized)
        self.assertEqual(statechart_4.root_state_instance, None)
        
        statechart_4.init_statechart()

        self.assertTrue(statechart_4.statechart_is_initialized)
        self.assertFalse(statechart_4.root_state_instance is None)
        self.assertEqual(statechart_4.root_state_instance.get_substate('F'), statechart_4.get_state('F'))

    def test_statechart_5_which_has_invalid_root_state_example_class(self):
        statechart_5 = Statechart_5()

        with self.assertRaises(Exception) as cm:
            statechart_5.init_statechart()

        self.assertEqual(str(cm.exception), "Invalid root state example")

    def test_statechart_6_which_has_an_initial_state_set_with_concurrent_states(self):
        statechart_6 = Statechart_6()

        with self.assertRaises(Exception) as cm:
            statechart_6.init_statechart()

        msg = "Cannot assign an initial state when states are concurrent"

        self.assertEqual(str(cm.exception), msg)

