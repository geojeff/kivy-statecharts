'''
Statechart tests, destroy
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

class A(State):
    pass

class B(State):
    pass

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['initial_state_key'] = 'A'
        super(Statechart_1, self).__init__(**kwargs)

    A = A
    B = B

class StatechartDestroyTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global root_state_1
        global state_A
        global state_B

        statechart_1 = Statechart_1()
        root_state_1 = statechart_1.root_state_instance
        state_A = statechart_1.get_state('A')
        state_B = statechart_1.get_state('B')
        
    def test_statechart_1(self):
        self.assertIsNotNone(statechart_1) 
        # [PORT] js tests have check of 'owner' and 'trace observers on statechart, but here they are on states.
        #        Not sure how to check on observer existence anyway... Maybe something like:
        #self.assertTrue(hasattr(statechart_1.root_state.__storage[SOMETHING]['observers'], 'owner'))
        #self.assertTrue(hasattr(statechart_1.root_state.__storage[SOMETHING]['observers'], 'trace'))
        self.assertEqual(statechart_1.root_state_instance, root_state_1)

        #self.assertFalse(root_state_1.isDestroyed) # [PORT] There is no isDestroyed in kivy.
        self.assertEqual(len(root_state_1.substates), 2)
        self.assertEqual(len(root_state_1.current_substates), 1)
        self.assertEqual(root_state_1.history_state, statechart_1.get_state('A'))
        self.assertEqual(root_state_1.initial_substate_key, 'A')
        self.assertEqual(root_state_1.statechart, statechart_1)
        self.assertEqual(root_state_1.owner, statechart_1)
        
        #self.assertFalse(state_A.isDestroyed)
        self.assertEqual(state_A.parent_state, root_state_1)

        #self.assertFalse(state_B.isDestroyed)
        self.assertEqual(state_B.parent_state, root_state_1)

        # [PORT] Statechart might need a destroy method that does the SC equivalent, that is
        #        if the destroy functionality is appropriate for kivy... Commenting out all below...
        #statechart_1.destroy()

        #self.assertIsNone(statechart_1) 
        #self.assertFalse(statechart_1.root_state.is_event_type('owner')) # [PORT] not on statechart, but on states; is_event_type isn't it anyway.
        #self.assertFalse(statechart_1.root_state.is_event_type('trace'))
        #self.assertEqual(statechart_1.root_state_instance, None)

        #self.assertTrue(root_state_1.isDestroyed)
        #self.assertEqual(root_state_1.substates, None)
        #self.assertEqual(root_state_1.current_substates, None)
        #self.assertEqual(root_state_1.history_state, None)
        #self.assertEqual(root_state_1.initial_substate_key, None)
        #self.assertEqual(root_state_1.statechart, None)
        #self.assertEqual(root_state_1.owner, None)
        
        #self.assertTrue(state_A.isDestroyed)
        #self.assertEqual(state_A.parent_state, None)

        #self.assertTrue(state_B.isDestroyed)
        #self.assertEqual(state_B.parent_state, None)

