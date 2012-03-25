# ================================================================================
# Project:   Kivy.Statechart - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

from kivy.event import EventDispatcher
from kivy.properties import ListProperty, NumericProperty

class StatechartMonitor(EventDispatcher):
    length = NumericProperty(0)
    statechart = ObjectProperty(None)
    sequence = ListProperty([])

    def __init__(self, **kwargs):
        self.bind(sequence=self._length)
        self.reset();
        super(StatechartMonitor, self).__init__(**kwargs)
  
    def reset(self):
        #self.propertyWillChange('length') #[PORT]
        self.sequence = []
        #self.propertyDidChange('length') #[PORT]
  
    def _length(self):
        self.length = len(self.sequence)
  
    def pushEnteredState(self, state):
        #self.propertyWillChange('length') #[PORT]
        self.sequence.push({ action: 'entered', state: state })
        #self.propertyDidChange('length') #[PORT]
  
    def pushExitedState(self, state):
        #self.propertyWillChange('length') #[PORT]
        self.sequence.push({ action: 'exited', state: state })
        #self.propertyDidChange('length') #[PORT]
  
    def matchSequence(self):
        return StatechartSequenceMatcher(self) # [PORT] call was ({ statechartMonitor: self }), but __init__ on SSM was changed to take monitor
  
    # [PORT] Check how arguments is used in the call. 
    def matchEnteredStates(self, *arguments):
        expected = arguments[0] if len(arguments) == 1 else arguments # [PORT] arguments, in javascript. so *arguments was added here
        actual = self.statechart.enteredStates
        matched = 0
        statechart = self.statechart
    
        if len(expected) != len(actual):
            return False
    
        for item in expected:
            if instanceof(item, basestring):
                item = statechart.getState(item)
            if item is None:
                return
            if statechart.stateIsEntered(item) and item.isEnteredState:
                matched += 1
    
        return matched == len(actual)
  
    def toString(self):
        seq = ""
        i = 0
        item = null
    
        seq += "["

        for i in range(len(self.sequence)):
            item = self.sequence[i]
            seq += "{0} {1}".format(item.action, item.state.fullPath)
            if i < len(self.sequence)-1:
                seq += ", "

        seq += "]"

        return seq;
