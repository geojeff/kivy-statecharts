'''
Statechart tests, destroy
===========
'''

import unittest

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

owner = ObjectProperty(None)

class A(State):
    pass

class B(State):
    pass

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['initialStateKey'] = 'A'
        super(Statechart_1, self).__init__(**kwargs)

    A = A
    B = B

class StatechartDestroyTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global rootState_1
        global state_A
        global state_B

        statechart_1 = Statechart_1()
        rootState_1 = statechart_1.rootStateInstance
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        
    def test_statechart_1(self):
        self.assertIsNotNone(statechart_1) 
        # [PORT] js tests have check of 'owner' and 'trace observers on statechart, but here they are on states.
        #        Not sure how to check on observer existence anyway... Maybe something like:
        #self.assertTrue(hasattr(statechart_1.rootState.__storage[SOMETHING]['observers'], 'owner'))
        #self.assertTrue(hasattr(statechart_1.rootState.__storage[SOMETHING]['observers'], 'trace'))
        self.assertEqual(statechart_1.rootStateInstance, rootState_1)

        #self.assertFalse(rootState_1.isDestroyed) # [PORT] There is no isDestroyed in kivy.
        self.assertEqual(len(rootState_1.substates), 2)
        self.assertEqual(len(rootState_1.currentSubstates), 1)
        self.assertEqual(rootState_1.historyState, statechart_1.getState('A'))
        self.assertEqual(rootState_1.initialSubstateKey, 'A')
        self.assertEqual(rootState_1.statechart, statechart_1)
        self.assertEqual(rootState_1.owner, statechart_1)
        
        #self.assertFalse(state_A.isDestroyed)
        self.assertEqual(state_A.parentState, rootState_1)

        #self.assertFalse(state_B.isDestroyed)
        self.assertEqual(state_B.parentState, rootState_1)

        # [PORT] Statechart might need a destroy method that does the SC equivalent, that is
        #        if the destroy functionality is appropriate for kivy... Commenting out all below...
        #statechart_1.destroy()

        #self.assertIsNone(statechart_1) 
        #self.assertFalse(statechart_1.rootState.is_event_type('owner')) # [PORT] not on statechart, but on states; is_event_type isn't it anyway.
        #self.assertFalse(statechart_1.rootState.is_event_type('trace'))
        #self.assertEqual(statechart_1.rootStateInstance, None)

        #self.assertTrue(rootState_1.isDestroyed)
        #self.assertEqual(rootState_1.substates, None)
        #self.assertEqual(rootState_1.currentSubstates, None)
        #self.assertEqual(rootState_1.historyState, None)
        #self.assertEqual(rootState_1.initialSubstateKey, None)
        #self.assertEqual(rootState_1.statechart, None)
        #self.assertEqual(rootState_1.owner, None)
        
        #self.assertTrue(state_A.isDestroyed)
        #self.assertEqual(state_A.parentState, None)

        #self.assertTrue(state_B.isDestroyed)
        #self.assertEqual(state_B.parentState, None)

