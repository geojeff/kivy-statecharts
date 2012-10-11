# ================================================================================
# Project:   Kivy.Statechart - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

from kivy_statecharts.system.state import State
from kivy.properties import BooleanProperty

MISMATCH = {}

class StatechartSequenceMatcher:
    match = BooleanProperty(False)

    def __init__(self, statechart_monitor):
        self.statechart_monitor = statechart_monitor
  
    def begin(self):
        self._stack = []
        self.begin_sequence()
        self._start = self._stack[0]
        return self
  
    def end(self):
        self.end_sequence()
    
        if len(self._stack) > 0:  # pragma: no cover
            raise "Can not match sequence. Sequence matcher has been left in an invalid state"
    
        result = False
        
        if self._match_sequence(self._start, 0) == len(self.statechart_monitor.sequence):
            result = True

        self.match = result
    
        return result
  
    def entered(self, *states):
        self._add_states_to_current_group('entered', states) # [PORT] js arguments, so *states added here
        return self
  
    def exited(self, *states):
        self._add_states_to_current_group('exited', states)
        return self
  
    def begin_concurrent(self):
        group = { 'token_type': 'concurrent', 'values': [] }

        if self._peek():
            self._peek()['values'].append(group)

        self._stack.append(group)

        return self
  
    def end_concurrent(self):
        self._stack.pop()
        return self
  
    def begin_sequence(self):
        group = { 'token_type': 'sequence', 'values': [] }

        if self._peek():
            self._peek()['values'].append(group)

        self._stack.append(group)
        return self
  
    def end_sequence(self):
        self._stack.pop()
        return self
  
    def _peek(self):
        return None if len(self._stack) == 0 else self._stack[-1]
  
    def _add_states_to_current_group(self, action, states):
        group = self._peek()

        for state in states:
            group['values'].append({ 'action': action, 'state': state })
  
    def _match_sequence(self, sequence, marker):
        values = sequence['values']
        
        if not values:
            return marker

        if marker > len(self.statechart_monitor.sequence):
            return MISMATCH
        
        # values is hierarchical, so that it is: {values: [{ values: [{ values: ...
        # and actions are mixed in there.
        for val in values:
            if 'token_type' in val:
                if val['token_type'] == 'sequence':
                    marker = self._match_sequence(val, marker)
                elif val['token_type'] == 'concurrent':
                    marker = self._match_concurrent(val, marker)
            elif marker > len(self.statechart_monitor.sequence)-1 or not self._match_items(val, self.statechart_monitor.sequence[marker]):
                return MISMATCH
            else:
                marker += 1
      
            if marker == MISMATCH:
                return MISMATCH
    
        return marker

    # A
    # B (concurrent [X, Y])
    #   X
    #     M
    #     N
    #   Y
    #     O
    #     P
    # C
    # 
    # 0 1  2 3 4   5 6 7  8
    #      ^       ^
    # A B (X M N) (Y O P) C
    #      ^       ^
    # A B (Y O P) (X M N) C
  
    def _match_concurrent(self, concurrent, marker):
        values = list(concurrent['values']) # copy
        temp_marker = marker
        match = False
        monitor = self.statechart_monitor
        
        if not values:
            return marker
    
        if marker > len(monitor.sequence):
            return MISMATCH
    
        # values is hierarchical, so that it is: {values: [{ values: [{ values: ... , token_type: 'sequence'}
        # and actions are list items in values lists, with token_type as the second key/value pair in the dicts.
        while len(values) > 0:
            for val in values:
                if 'token_type' in val:
                    if val['token_type'] == 'sequence':
                        temp_marker = self._match_sequence(val, marker)
                    elif val['token_type'] == 'concurrent':
                        temp_marker = self._match_concurrent(val, marker)
                elif marker > len(self.statechart_monitor.sequence)-1 or not self._match_items(val, monitor.sequence[marker]):
                    temp_marker = MISMATCH
                else:
                    temp_marker = marker + 1
      
                if temp_marker != MISMATCH:
                    break
      
            if temp_marker == MISMATCH:
                return MISMATCH

            values.remove(val)
              
            marker = temp_marker
    
        return marker
  
    def _match_items(self, matcher_item, monitor_item):
        if matcher_item is None or monitor_item is None:
            return False
  
        if 'action' in matcher_item and matcher_item['action'] != monitor_item['action']:
            return False
    
        if 'state' in matcher_item and isinstance(matcher_item['state'], State) and matcher_item['state'] is monitor_item['state']:
            return True
    
        if 'state' in matcher_item and matcher_item['state'] == monitor_item['state'].name:
            return True
  
        return False
