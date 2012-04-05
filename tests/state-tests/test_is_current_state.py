'''
Statechart tests, is current state
===========
'''

import unittest, re

counter = 0

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy_statechart.system.state import State
from kivy_statechart.system.empty_state import EmptyState
from kivy_statechart.system.statechart import StatechartManager

import os, inspect

class Statechart_1(StatechartManager):
    def __init__(self, **kwargs):
        kwargs['monitorIsActive'] = True
        kwargs['rootState'] = self.RootState
        super(Statechart_1, self).__init__(**kwargs)

    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'A'
            super(Statechart_1.RootState, self).__init__(**kwargs)

        class A(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.A, self).__init__(**kwargs)

        class B(State):
            def __init__(self, **kwargs):
                super(Statechart_1.RootState.B, self).__init__(**kwargs)

class StateIsCurrentStateTestCase(unittest.TestCase):
    def setUp(self):
        global statechart_1
        global rootState_1
        global monitor_1
        global state_A
        global state_B

        statechart_1 = Statechart_1()
        statechart_1.initStatechart()
        rootState_1 = statechart_1.rootState
        monitor_1 = statechart_1.monitor
        state_A = statechart_1.getState('A')
        state_B = statechart_1.getState('B')
        
    # check binding to isCurrentState"
    def test_check_binding_to_isCurrentState_statechart_1(self):
        class o(object):
            def __init__(self):
                self.value = None
                #self.bind(value, state_A.isCurrentState) # [PORT] Won't work in kivy. Plus, isCurrentState() is now a method.

        self.assertEqual(rootState_1.initialSubstateKey, state_A.name)
