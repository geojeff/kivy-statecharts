# ================================================================================
# Project:   Kivy.Statechart - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

from kivy.event import EventDispatcher
from kivy_statecharts.debug.monitor import StatechartMonitor
from kivy_statecharts.system.async import Async
from kivy_statecharts.system.state import State
from kivy_statecharts.system.history_state import HistoryState
from kivy_statecharts.system.empty_state import EmptyState
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.logger import Logger

from collections import deque

import inspect

"""
  @class

  The startchart manager mixin allows an object to be a statechart. By becoming a statechart, the
  object can then be manage a set of its own states.
  
  This implementation of the statechart manager closely follows the concepts stated in D. Harel's 
  original paper "Statecharts: A Visual Formalism For Complex Systems" 
  (www.wisdom.weizmann.ac.il/~harel/papers/Statecharts.pdf). 
  
  The statechart allows for complex state heircharies by nesting states within states, and 
  allows for state orthogonality based on the use of concurrent states.
  
  At minimum, a statechart must have one state: The root state. All other states in the statechart
  are a decendents (substates) of the root state.
  
  The following example shows how states are nested within a statechart:
  
      MyApp.Statechart = Object.extend(StatechartManager, {
        root_state: State.design({
          initial_substate_key: 'stateA',

          stateA: State.design({
            # ... can continue to nest further states
          }),
        
          stateB: State.design({
            # ... can continue to nest further states
          })
        })
      });
  
  Note how in the example above, the root state has an explicit initial substate to enter. If no
  initial substate is provided, then the statechart will default to the the state's first substate.
  
  You can also defined states without explicitly defining the root state. To do so, simply create properties
  on your object that represents states. Upon initialization, a root state will be constructed automatically
  by the mixin and make the states on the object substates of the root state. As an example:
  
      MyApp.Statechart = Object.extend(StatechartManager, {
        initial_state_key: 'stateA',

        stateA: State.design({
          # ... can continue to nest further states
        }),
      
        stateB: State.design({
          # ... can continue to nest further states
        })
      });
  
  If you specified a class that should be used as the root state but used the above method to defined
  states, you can set the root_state_example_class property with a class that extends from State. If the 
  root_state_example_class property is not explicitly assigned the then default class used will be State.
  
  To provide your statechart with orthogonality, you use concurrent states. If you use concurrent states,
  then your statechart will have multiple current states. That is because each concurrent state represents an
  independent state structure from other concurrent states. The following example shows how to provide your
  statechart with concurrent states:
  
      MyApp.Statechart = Object.extend(StatechartManager, {
        root_state: State.design({
          substates_are_concurrent: True,

          stateA: State.design({
            # ... can continue to nest further states
          }),
        
          stateB: State.design({
            # ... can continue to nest further states
          })
        })
      });
  
  Above, to indicate that a state's substates are concurrent, you just have to set the substates_are_concurrent to 
  True. Once done, then stateA and stateB will be independent of each other and each will manage their
  own current substates. The root state will then have more then one current substate.
  
  To define concurrent states directly on the object without explicitly defining a root, you can do the 
  following:
  
      MyApp.Statechart = Object.extend(StatechartManager, {
        states_are_concurrent: True,

        stateA: State.design({
          # ... can continue to nest further states
        }),
    
        stateB: State.design({
          # ... can continue to nest further states
        })
      });
  
  Remember that a startchart can have a mixture of nested and concurrent states in order for you to 
  create as complex of statecharts that suite your needs. Here is an example of a mixed state structure:
  
      MyApp.Statechart = Object.extend(StatechartManager, {
        root_state: State.design({
          initial_substate_key: 'stateA',

          stateA: State.design({
            substates_are_concurrent: True,

            stateM: State.design({ ... })
            stateN: State.design({ ... })
            stateO: State.design({ ... })
          }),
        
          stateB: State.design({
            initial_substate_key: 'stateX',

            stateX: State.design({ ... })
            stateY: State.desgin({ ... })
          })
        })
      });
  
  Depending on your needs, a statechart can have lots of states, which can become hard to manage all within
  one file. To modularize your states and make them easier to manage and maintain, you can plug-in states
  into other states. Let's say we are using the statechart in the last example above, and all the code is 
  within one file. We could update the code and split the logic across two or more files like so:

      # state_a.js

      MyApp.StateA = State.extend({
        substates_are_concurrent: True,

        stateM: State.design({ ... })
        stateN: State.design({ ... })
        stateO: State.design({ ... })
      });

      # state_b.js

      MyApp.StateB = State.extend({
        substates_are_concurrent: True,

        stateM: State.design({ ... })
        stateN: State.design({ ... })
        stateO: State.design({ ... })
      });

      # statechart.js

      MyApp.Statechart = Object.extend(StatechartManager, {
        root_state: State.design({
          initial_substate_key: 'stateA',
          stateA: State.plugin('MyApp.StateA'),
          stateB: State.plugin('MyApp.StateB')
        })
      });

  Using state plug-in functionality is optional. If you use the plug-in feature you can break up your statechart
  into as many files as you see fit.

  @author Michael Cohen
"""

class StatechartManager(EventDispatcher):

    current_states = ListProperty([])
    go_to_state_locked = BooleanProperty(False)
    go_to_state_active = BooleanProperty(True)
    go_to_state_suspended_point = ObjectProperty(None, allownone=True)
    go_to_state_suspended = BooleanProperty(False)
    statechart_log_prefix = StringProperty(None)
    details = ObjectProperty(None)

    # Walk like a duck
    is_responder_context = BooleanProperty(True)

    # Walk like a duck
    is_statechart = BooleanProperty(True)

    """
      Indicates if this statechart has been initialized
  
      @property {Boolean}
    """
    statechart_is_initialized = BooleanProperty(False)

    """
      Optional name you can provide the statechart. If set this will be included
      in tracing and error output as well as detail output. Useful for 
      debugging/diagnostic purposes
    """
    name = StringProperty(None)
    
    """
      The root state of this statechart. All statecharts must have a root state.
      
      If this property is left unassigned, then when the statechart is initialized
      it will use the root_state_example_class, initial_state_key, and states_are_concurrent
      properties to construct a root state.
      
      @see #root_state_example_class
      @see #initial_state_key
      @see #states_are_concurrent
      
      @property {State}
    """
    root_state_class = ObjectProperty(None)
    root_state_instance = ObjectProperty(None, allownone=True)
    
    """ 
      Represents the state used to construct a class that will be the root state for
      this statechart. The class must derive from State. 
      
      This property will only be used if the root_state property is not assigned.
    
      @see #root_state
    
      @property {State}
    """
    root_state_example_class = ObjectProperty(None)
    
    """ 
      Indicates what state should be the initial state of this statechart. The value
      assigned must be the name of a property on this object that represents a state.
      As well, the states_are_concurrent must be set to False.
      
      This property will only be used if the root_state property is not assigned.

      [PORT] This is a String in the original javascript, despite a conditional in init_statechart
             that sets it to the actual state in root_state, and despite a test that compares it
             to actual class objects. Here it is kept a String, and the conditional commented out,
             and the tests changed to check against strings, when either statechart.initial_state_key
             or state.initial_substate_key are used.
    
      @see #root_state
    
      @property {String} 
    """
    initial_state_key = StringProperty(None, allownone=True)
    
    """ 
      Indicates if properties on this object representing states are concurrent to each other.
      If True then they are concurrent, otherwise they are not. If True, then the
      initial_state_key property must not be assigned.
      
      This property will only be used if the root_state property is not assigned.
    
      @see #root_state
    
      @property {Boolean}
    """
    states_are_concurrent = BooleanProperty(False)
    
    """ 
      Indicates whether to use a monitor for the statechart's activities. If true then
      the monitor will be active, otherwise the monitor will not be used. Useful for debugging
      purposes.
      
      @property {Boolean}
    """
    monitor_is_active = BooleanProperty(False)
    
    """
      A statechart monitor that can be used to monitor this statechart. Useful for debugging purposes.
      A monitor will only be used if monitor_is_active is true.
      
      @property {StatechartMonitor}
    """
    monitor = ObjectProperty(None)
    
    """
      Indicates whether to trace the statecharts activities. If true then the statechart will output
      its activites to the logger. Useful for debugging purposes.
  
      @property {Boolean}
    """
    trace = BooleanProperty(False)
    
    """
      Used to specify what property (key) on the statechart should be used as the owner property. By
      default the property is 'owner'.
  
      @property {String}
    """
    statechart_owner_key = StringProperty('owner')
  
    """
      Sets who the owner is of this statechart. If None then the owner is this object otherwise
      the owner is the assigned object. 
  
      @see #statechart_owner_key
  
      @property {Object}
    """
    owner = ObjectProperty(None, allownone=True)
  
    """ 
      Indicates if the statechart should be automatically initialized by this
      object after it has been created. If True then init_statechart will be
      called automatically, otherwise it will not.
    
      @property {Boolean}
    """
    auto_init_statechart = BooleanProperty(True)
    
    """
      If yes, any warning messages produced by the statechart or any of its states will
      not be logged, otherwise all warning messages will be logged. 
      
      While designing and debugging your statechart, it's best to keep this value false.
      In production you can then suppress the warning messages.
      
      @property {Boolean}
    """
    suppress_statechart_warnings = BooleanProperty(False)
    
    def __init__(self, **kw):
        #self.bind(current_states=self._current_states)
        self.bind(monitor_is_active=self._monitor_is_active_did_change)
        #self.bind(root_state=self._current_states) # [PORT] Added current_states property -- moved this to the bottom of init_statechart().
        self.bind(statechart_owner_key=self._owner_did_change) # [PORT] Added, to use top-down updating approach in kivy.
        self.bind(owner=self._owner_did_change) # [PORT] Added, to use top-down updating approach in kivy.
        self.bind(go_to_state_locked=self._go_to_state_active)
        self.bind(go_to_state_locked=self._go_to_state_suspended)
        self.bind(go_to_state_suspended_point=self._go_to_state_suspended)

        for k,v in kw.items():
            setattr(self, k, v)

        # [PORT] NOTE: The binding, self.bind(root_state_instance=self._current_states) is set at the
        #              bottom of init_statechart(), after instantiation.

        super(StatechartManager, self).__init__(**kw)

        if self.auto_init_statechart == True:
            self.init_statechart()
        
    def _owner_did_change(self, *l):
        if self.root_state_instance: # [PORT] root_state can be None
            self.root_state_instance.statechart_owner_did_change()

    """
      Initializes the statechart. By initializing the statechart, it will create all the states and register
      them with the statechart. Once complete, the statechart can be used to go to states and send events to.
    """
    def init_statechart(self):
        if self.statechart_is_initialized:
            return
          
        self.go_to_state_locked = False
        self._send_event_locked = False
        self._pending_state_transitions = deque()
        self._pending_sent_events = deque()
          
        self.send_action = self.send_event
          
        if self.monitor_is_active:
            self.monitor = StatechartMonitor(statechart=self)
      
        # [PORT] Clarify in docs that root_state is None or is a class.
        msg = ''

        if self.trace:
            self.statechart_log_trace("BEGIN initialize statechart")
          
        # If no root state was explicitly defined then try to construct a root
        # state class
        if not self.root_state_class:
            self.root_state_class = self._construct_root_state_class()
          
        # [PORT] plugin system in javascript version removed in python version.
        # States are classes, declared either in the source file with the
        # statechart, or imported from individual files.

        if (inspect.isclass(self.root_state_class) 
                and not issubclass(self.root_state_class, State)):
            msg = ("Unable to initialize statechart. Root state must be a "
                   "state class")
            self.statechart_log_error(msg)
            raise Exception(msg)
          
        # Instantiate the root_state class.
        root_state_instance = \
                self.create_root_state(self.root_state_class, ROOT_STATE_NAME)
          
        # Set self.root_state_instance to be the instantiated object.
        self.root_state_instance = root_state_instance

        root_state_instance.init_state()
          
#        # The initialState of root_state must be a real state -- can't be the
#        # EmptyState.
#        problem_with_initial_root_state = False
#        if (hasattr(root_state_instance, 'initial_substate_key') 
#                and root_state_instance.initial_substate_key):
#            initial_root_state = root_state_instance.initial_substate_object
#            if initial_root_state is None:
#                problem_with_initial_root_state = True
#            elif isinstance(initial_root_state, EmptyState):
#                problem_with_initial_root_state = True
#        elif (not hasattr(root_state_instance, 'substates_are_concurrent') 
#                or not root_state_instance.substates_are_concurrent):
#            problem_with_initial_root_state = True
#
#        if problem_with_initial_root_state:
#            msg = ("Unable to initialize statechart. Root state must have an "
#                   "initial substate or substates_are_concurrent explicitly "
#                   "defined.")
#            self.statechart_log_error(msg)
#            raise Exception(msg)

    #if (SC.kindOf(root_state.get('initial_substate'), SC.EmptyState)) {
      #msg = "Unable to initialize statechart. Root state must have an initial substate explicilty defined";
      #this.statechart_log_error(msg);
      #throw msg;
    #}
    #
    ##if (!SC.empty(this.get('initialState'))) {
      #var key = 'initialState';
      #this.set(key, root_state.get(this.get(key)));
    #} 
          
        # In the original javascript, an if here did this:
        #
        #     If the initial_state_key here is set (a string), reset it to the actual state by that name in root_state
        #
        # This is not consistent with initial_state_key defined as a String, but it is consistent with tests that check initial_state_key
        # against actual class objects. Here we will leave it as a String, and skip this set.
        #
        #if self.initial_state_key:
            #self.initial_state_key = getattr(root_state, str(self.initial_state_key))
          
        self.statechart_is_initialized = True

        self.bind(root_state_instance=self._current_states)

        self.go_to_state(root_state_instance)
          
        if self.trace:
            self.statechart_log_trace("END initialize statechart")
        
    """
      Will create a root state for the statechart
    """
    def create_root_state(self, state, name):
        return state(statechart=self, name=name)
        
    #"""
      #Returns an array of all the current states for this statechart
      #
      #@returns {Array} the current states
    #"""
    def _current_states(self, *l):
        self.current_states = self.root_state_instance.current_substates

    """
      Checks if a given state is a current state of this statechart. 
      
      @param state {State|String} the state to check
      @returns {Boolean} true if the state is a current state, otherwise fals is returned
    """
    def state_is_current_state(self, state):
        return self.root_state_instance.state_is_current_substate(state)
        
    """
      Returns an array of all the states that are currently entered for
      this statechart.
      
      @returns {Array} the currently entered states
    """
    def entered_states(self):
        return self.root_state_instance.entered_substates

    """
      Checks if a given state is a currently entered state of this statechart.
      
      @param state {State|String} the state to check
      @returns {Boolean} true if the state is a currently entered state, otherwise false is returned
    """
    def state_is_entered(self, state):
        return self.root_state_instance.state_is_entered_substate(state)
        
    """
      Gets a state from the statechart that matches the given value
      
      @param value {State|String} either a state object or the name of a state
      @returns {State} if a match then the matching state is returned, otherwise None is returned 
    """
    def get_state(self, state):
        if isinstance(state, basestring):
            return self.root_state_instance if self.root_state_instance.name == state else self.root_state_instance.get_substate(state)
        else:
            return self.root_state_instance if self.root_state_instance is state else self.root_state_instance.get_substate(state)
      
    """
      When called, the statechart will proceed with making state transitions in the statechart starting from 
      a current state that meets the statechart conditions. When complete, some or all of the statechart's 
      current states will be changed, and all states that were part of the transition process will either 
      be exited or entered in a specific order.
      
      The state that is given to go to will not necessarily be a current state when the state transition process
      is complete. The final state or states are dependent on factors such an initial substates, concurrent 
      states, and history states.
      
      Because the statechart can have one or more current states, it may be necessary to indicate what current state
      to start from. If no current state to start from is provided, then the statechart will default to using
      the first current state that it has; depending of the make up of the statechart (no concurrent state vs.
      with concurrent states), the outcome may be unexpected. For a statechart with concurrent states, it is best
      to provide a current state in which to start from.
      
      When using history states, the statechart will first make transitions to the given state and then use that
      state's history state and recursively follow each history state's history state until there are no 
      more history states to follow. If the given state does not have a history state, then the statechart
      will continue following state transition procedures.
      
      Method can be called in the following ways:
      
          # With one argument. 
          go_to_state(<state>)
            
          # With two arguments.
          go_to_state(<state>, <state | boolean | hash>)
        
          # With three arguments.
          go_to_state(<state>, <state>, <boolean | hash>)
          go_to_state(<state>, <boolean>, <hash>)
        
          # With four arguments.
          go_to_state(<state>, <state>, <boolean>, <hash>)
      
      where <state> is either a State object or a string and <hash> is a
      regular JS hash object.
      
      @param state {State|String} the state to go to (may not be the final
        state in the transition process)
      @param from_current_state {State|String} Optional. The current state to
        start the transition process from.
      @param use_history {Boolean} Optional. Indicates whether to include using
        history states in the transition process
      @param context {Hash} Optional. A context object that will be passed to
        all exited and entered states
    """
    def go_to_state(self, state, from_current_state=None, use_history=None, context=None):
        if not self.statechart_is_initialized:
            msg = ("Cannot go to state {0}. Statechart has not yet been "
                   "initialized.").format(state)
            self.statechart_log_error(msg)
            raise Exception(msg)
          
        # [PORT] Removed isDestroyed check -- but this is a punt for a later time...
        #if self.isDestroyed:
            #self.statechart_log_error("Cannot go to state {0}. statechart is destroyed".format(this))
            #return
          
        pivot_state = None
        exit_states = deque()
        enter_states = deque()
        param_state = state
        param_from_current_state = from_current_state
          
        state = self.get_state(state)
          
        if state is None:
            msg = ("Cannot to goto state {0}. Not a recognized state in "
                   "statechart.").format(param_state)
            self.statechart_log_error(msg)
            raise Exception(msg)
          
        if self.go_to_state_locked:
            # There is a state transition currently happening. Add this requested state
            # transition to the queue of pending state transitions. The request will
            # be invoked after the current state transition is finished.
            self._pending_state_transitions.append({
              'state': state,
              'from_current_state': from_current_state,
              'use_history': use_history,
              'context': context
            })
            return
          
        # Lock the current state transition so that no other requested state
        # transition interferes. 
        self.go_to_state_locked = True
          
        if from_current_state is not None:
            # Check to make sure the current state given is actually a current
            # state of this statechart
            from_current_state = self.get_state(from_current_state)
            if (from_current_state is None
                    or not from_current_state.is_current_state()):
                msg = ("Cannot to goto state {0}. {1} is not a "
                       "recognized current state in "
                       "the statechart.").format(param_state,
                                                 param_from_current_state)
                self.statechart_log_error(msg)
                self.go_to_state_locked = False
                raise Exception(msg)
        else:
            # No explicit current state to start from; therefore, need to find a current state
            # to transition from.
            from_current_state = state.find_first_relative_current_state()
            if from_current_state is None:
                from_current_state = self.current_states[0] if self.current_states else None
              
        if self.trace:
            self.statechart_log_trace("BEGIN go_to_state: {0}".format(state))
            msg = "starting from current state: {0}"
            msg = msg.format(from_current_state if from_current_state else '---')
            self.statechart_log_trace(msg)
            msg = "current states before: {0}"
            msg = msg.format(self.current_states if self.current_states else '---')
            self.statechart_log_trace(msg)
      
        # If there is a current state to start the transition process from, then determine what
        # states are to be exited
        if from_current_state is not None:
            exit_states = self._create_state_chain(from_current_state)
          
        # Now determine the initial states to be entered
        enter_states = self._create_state_chain(state)
          
        # Get the pivot state to indicate when to go from exiting states to entering states
        pivot_state = self._find_pivot_state(exit_states, enter_states)
      
        if pivot_state is not None:
            if self.trace:
                self.statechart_log_trace("pivot state = {0}".format(pivot_state))
            if pivot_state.substates_are_concurrent and pivot_state is not state:
                msg = ("Cannot go to state {0} from {1}. Pivot state {2} has "
                       "concurrent substates.").format(state,
                                                       from_current_state,
                                                       pivot_state)
                self.statechart_log_error(msg)
                self.go_to_state_locked = False
                raise Exception(msg)
          
        # Collect what actions to perform for the state transition process
        go_to_state_actions = []

        # Go ahead and find states that are to be exited
        self._traverse_states_to_exit(exit_states.popleft() if exit_states else None, exit_states, pivot_state, go_to_state_actions)
          
        # Now go find states that are to be entered
        if pivot_state is not state:
            self._traverse_states_to_enter(enter_states.pop(), enter_states, pivot_state, use_history, go_to_state_actions)
        else:
            self._traverse_states_to_exit(pivot_state, deque(), None, go_to_state_actions)
            self._traverse_states_to_enter(pivot_state, None, None, use_history, go_to_state_actions)
          
        # Collected all the state transition actions to be performed. Now execute them.
        self._go_to_state_actions = go_to_state_actions
        self._execute_go_to_state_actions(state, go_to_state_actions, None, context)
        
    """
      Indicates if the statechart is in an active goto state process
    """
    def _go_to_state_active(self, *l):
        self.go_to_state_active = self.go_to_state_locked

    """
      Indicates if the statechart is in an active goto state process
      that has been suspended
    """
    def _go_to_state_suspended(self, *l):
        self.go_to_state_suspended = (self.go_to_state_locked 
                and self.go_to_state_suspended_point is not None)
        
    """
      Resumes an active goto state transition process that has been suspended.
    """
    def resume_go_to_state(self):
        if not self.go_to_state_suspended:
            msg = ("Cannot resume goto state since it has not been suspended.")
            self.statechart_log_error(msg)
            raise Exception(msg)
          
        point = self.go_to_state_suspended_point
        self._execute_go_to_state_actions(point['go_to_state'],
                                          point['actions'],
                                          point['marker'],
                                          point['context'])
        
    """ @private """
    def _execute_go_to_state_actions(self, go_to_state,
                                     actions, marker, context):
        action = None
        action_result = None
            
        marker = 0 if marker is None else marker
          
        number_of_actions = len(actions)
        while marker < number_of_actions:
            action = actions[marker]
            self._current_go_to_state_action = action
            if action['action'] == EXIT_STATE:
                action_result = self._exit_state(action['state'], context)
            elif action['action'] == ENTER_STATE:
                action_result = self._enter_state(action['state'], action['current_state'], context)
            
            # Check if the state wants to perform an asynchronous action during
            # the state transition process. If so, then we need to first
            # suspend the state transition process and then invoke the 
            # asynchronous action. Once called, it is then up to the state or something 
            # else to resume this statechart's state transition process by calling the
            # statechart's resume_go_to_state method.
            #
            #if action_result and inspect.isclass(action_result) and issubclass(action_result, Async):
            if action_result and isinstance(action_result, Async):
                self.go_to_state_suspended_point = {
                    'go_to_state': go_to_state,
                    'actions': actions,
                    'marker': marker + 1,
                    'context': context
                }
              
                action_result.try_to_perform(self.get_state(action['state'])) # [PORT] state arg must be object, not string key
                return

            marker += 1
          
        #self.beginPropertyChanges()
        #self.notifyPropertyChange('current_states') # [PORT] notify needed here in kivy?
        #self.endPropertyChanges()
        self._current_states()
          
        if self.trace:
            self.statechart_log_trace("current states after: {0}".format(self.current_states))
            self.statechart_log_trace("END go_to_state: {0}".format(go_to_state))
          
        self._clean_up_state_transition()
        
    """ @private """
    def _clean_up_state_transition(self):
        self._current_go_to_state_action = None
        self.go_to_state_suspended_point = None
        self._go_to_state_actions = None
        self.go_to_state_locked = False
        if self._pending_state_transitions: # [PORT] There is an error check in the function that this if now skips. But isn't it ok to be empty?
            self._flush_pending_state_transition()
        
    """ @private """
    def _exit_state(self, state, context):
        parent_state = None
          
        if state in state.current_substates:
            parent_state = state.parent_state
            while parent_state is not None:
                parent_state.current_substates.remove(state)
                parent_state = parent_state.parent_state
          
        parent_state = state;
        while parent_state is not None:
            if state in parent_state.entered_substates:
                parent_state.entered_substates.remove(state)
            parent_state = parent_state.parent_state
            
        if self.trace:
            self.statechart_log_trace("<-- exiting state: {0}".format(state))
          
        state.current_substates = []
          
        state.state_will_become_exited(context)
        result = self.exit_state(state, context)
        state.state_did_become_exited(context)
          
        if self.monitor_is_active:
            self.monitor.append_exited_state(state)
          
        setattr(state, '_traverse_states_to_exit_skip_state', False)
          
        return result
        
    """
      What will actually invoke a state's exit_state method.
        
      Called during the state transition process whenever the go_to_state method is
      invoked.
      
      @param state {State} the state whose enter_state method is to be invoked
      @param context {Hash} a context hash object to provide the enter_state method
    """
    def exit_state(self, state, context):
        return state.exit_state(context)
        
    """ @private """
    def _enter_state(self, state, current, context):
        state = self.get_state(state) # [PORT] Insure this is an obj and not a string.
        parent_state = state.parent_state
        if parent_state and not state.is_concurrent_state():
            parent_state.history_state = state
          
        if current:
            parent_state = state
            while parent_state is not None:
                parent_state.current_substates.append(state)
                parent_state = parent_state.parent_state
          
        parent_state = state;
        while parent_state is not None:
            parent_state.entered_substates.append(state)
            parent_state = parent_state.parent_state
          
        if self.trace:
             self.statechart_log_trace("--> entering state: {0}".format(state))
          
        state.state_will_become_entered(context)
        result = self.enter_state(state, context)
        state.state_did_become_entered(context)
          
        if self.monitor_is_active:
            self.monitor.append_entered_state(state)
          
        return result
        
    """
      What will actually invoke a state's enter_state method.
    
      Called during the state transition process whenever the go_to_state method is
      invoked.
      
      @param state {State} the state whose enter_state method is to be invoked
      @param context {Hash} a context hash object to provide the enter_state method
    """
    def enter_state(self, state, context):
        return state.enter_state(context)
        
    """
      When called, the statechart will proceed to make transitions to the given state then follow that
      state's history state. 
      
      You can either go to a given state's history recursively or non-recursively. To go to a state's history
      recursively means to following each history state's history state until no more history states can be
      followed. Non-recursively means to just to the given state's history state but do not recusively follow
      history states. If the given state does not have a history state, then the statechart will just follow
      normal procedures when making state transitions.
      
      Because a statechart can have one or more current states, depending on if the statechart has any concurrent
      states, it is optional to provided current state in which to start the state transition process from. If no
      current state is provided, then the statechart will default to the first current state that it has; which, 
      depending on the make up of that statechart, can lead to unexpected outcomes. For a statechart with concurrent
      states, it is best to explicitly supply a current state.
      
      Method can be called in the following ways:
      
          # With one arguments. 
          go_to_history_state(<state>)
        
          # With two arguments. 
          go_to_history_state(<state>, <state | boolean | hash>)
        
          # With three arguments.
          go_to_history_state(<state>, <state>, <boolean | hash>)
          go_to_history_state(<state>, <boolean>, <hash>)
        
          # With four argumetns
          go_to_history_state(<state>, <state>, <boolean>, <hash>)
      
      where <state> is either a State object or a string and <hash> is a regular JS hash object.
      
      @param state {State|String} the state to go to and follow it's history state
      @param from_current_state {State|String} Optional. the current state to start the state transition process from
      @param recursive {Boolean} Optional. whether to follow history states recursively.
    """
    def go_to_history_state(self, state, from_current_state=None, recursive=None, context=None):
        if not self.statechart_is_initialized:
            msg = ("Cannot go to state {0}'s history state. Statechart has "
                   "not yet been initialized").format(state)
            self.statechart_log_error(msg)
            raise Exception(msg)
          
        # [PORT] Assumming that in python argument handling will suffice.
        #args = self._process_go_to_state_args(arguments)
          
        #state = args.state
        #from_current_state = args.from_current_state
        #recursive = args.use_history
        #context = args.context
          
        state = self.get_state(state)
        
        if state is None:
            msg = ("Cannot to goto state {0}'s history state. Not a "
                   "recognized state in statechart").format(state)
            self.statechart_log_error(msg)
            raise Exception(msg)
          
        history_state = state.history_state
          
        if not recursive:
            if history_state is not None:
                self.go_to_state(state=history_state, from_current_state=from_current_state, context=context)
            else:
                self.go_to_state(state=state, from_current_state=from_current_state, context=context)
        else:
            self.go_to_state(state=state, from_current_state=from_current_state, use_history=True, context=context)

    """ 
      @private 
      Will process the arguments supplied to the go_to_state method.
    
      TODO: Come back to this and refactor the code. It works, but it
            could certainly be improved

      [PORT] Instead of this, made args optional, and made go_to_state and go_to_history_state 
             calls with explicit args
    """
    def _process_go_to_state_args(self, args):
        processed_args = { 
            'state': None, 
            'from_current_state': None, 
            'use_history': False, 
            'context': None 
        }
          
        args = (arg for arg in args if arg)
      
        if (len(args) < 1):
            return processed_args
      
        processed_args['state'] = args[0]
    
        if (len(args) == 2):
            value = args[1]
            if isinstance(value, bool):
                processed_args['use_history'] = value
            elif (isinstance(value, dict) or isinstance(value, object)) and not isinstance(value, State):
                processed_args['context'] = value
            else:
                processed_args['from_current_state'] = value
        elif (len(args) == 3):
            value = args[1]
            if isinstance(value, bool):
                processed_args['use_history'] = value
                processed_args['context'] = args[2]
            else:
                processed_args['from_current_state'] = value
                value = args[2]
                if isinstance(value, bool):
                    processed_args['use_history'] = value
                else:
                    processed_args['context'] = value
        else:
            processed_args['from_current_state'] = args[1]
            processed_args['use_history'] = args[2]
            processed_args['context'] = args[3]
      
        return processed_args
 
    """
      Sends a given event to all the statechart's current states.
          
      If a current state does cannot respond to the sent event, then the current state's parent state
      will be tried. This process is recursively done until no more parent state can be tried.
      
      Note that a state will only be checked once if it can respond to an event. Therefore, if
      there is a state S that handles event foo and S has concurrent substates, then foo will
      only be invoked once; not as many times as there are substates. 
      
      @param event {String} name of the event
      @param arg1 {Object} optional argument
      @param arg2 {Object} optional argument
      @returns {Responder} the responder that handled it or None
      
      @see #state_will_try_to_handle_event
      @see #state_did_try_to_handle_event
    """
    def send_event(self, event, arg1=None, arg2=None):
        # [PORT] Removed isDestroyed check -- but this is a punt for a later time...
        #if self.isDestroyed:
            #self.statechart_log_error("can send event {0}. statechart is destroyed".format(event))
            #return

        statechart_handled_event = False
        event_handled = False
        current_states_copy = self.current_states[:]
        checked_states = {}
        state = None
          
        if self._send_event_locked or self.go_to_state_locked:
            # Want to prevent any actions from being processed by the states until 
            # they have had a chance to handle the most immediate action or completed 
            # a state transition
            self._pending_sent_events.append({
                'event': event,
                'arg1': arg1,
                'arg2': arg2
            })
      
            return
          
        self._send_event_locked = True
          
        if self.trace:
            self.statechart_log_trace("BEGIN send_event: '{0}'".format(event))
          
        for state in current_states_copy:
            event_handled = False
            if not state.is_current_state():
                continue
            while not event_handled and state is not None:
                if not state.full_path in checked_states:
                    event_handled = state.try_to_handle_event(event, arg1, arg2)
                    checked_states[state.full_path] = True
                if not event_handled:
                    state = state.parent_state
                else:
                    statechart_handled_event = True
          
        # Now that all the states have had a chance to process the 
        # first event, we can go ahead and flush any pending sent events.
        self._send_event_locked = False
          
        if self.trace:
            if not statechart_handled_event:
                self.statechart_log_trace("No state was able handle event {0}".format(event))
            self.statechart_log_trace("END send_event: '{0}'".format(event))
          
        result = self._flush_pending_sent_events()
          
        return self if statechart_handled_event else (self if result else None)
        
    """
      Used to notify the statechart that a state will try to handle event that has been passed
      to it.
          
      @param {State} state the state that will try to handle the event
      @param {String} event the event the state will try to handle
      @param {String} handler the name of the method on the state that will try to handle the event 
    """
    def state_will_try_to_handle_event(self, state, event, handler):
        self._state_handle_event_info = {
            'state': state,
            'event': event,
            'handler': handler
        }
        
    """
      Used to notify the statechart that a state did try to handle event that has been passed
      to it.
          
      @param {State} state the state that did try to handle the event
      @param {String} event the event the state did try to handle
      @param {String} handler the name of the method on the state that did try to handle the event
      @param {Boolean} handled indicates if the handler was able to handle the event 
    """
    def state_did_try_to_handle_event(self, state, event, handler, handled):
        self._state_handle_event_info = None
      
    """ @private
    
      Creates a chain of states from the given state to the greatest ancestor state (the root state). Used
      when perform state transitions.
    """
    def _create_state_chain(self, state):
        chain = deque()
          
        while state is not None:
            chain.append(state)
            state = state.parent_state
          
        return chain
        
    """ @private
    
      Finds a pivot state from two given state chains. The pivot state is the state indicating when states
      go from being exited to states being entered during the state transition process. The value 
      returned is the fist matching state between the two given state chains. 
    """
    def _find_pivot_state(self, state_chain_1, state_chain_2):
        if len(state_chain_1) == 0 or len(state_chain_2) == 0:
            return None
          
        for state in state_chain_1:
            if state in state_chain_2:
                return state

    """ @private
          
      Recursively follow states that are to be exited during a state transition process. The exit
      process is to start from the given state and work its way up to when either all exit
      states have been reached based on a given exit path or when a stop state has been reached.
          
      @param state {State} the state to be exited
      @param exit_state_path {collections.deque} a deque representing a path of states that are to be exited
      @param stopState {State} an explicit state in which to stop the exiting process
    """
    def _traverse_states_to_exit(self, state, exit_state_path, stopState, go_to_state_actions):
        if state is None or state is stopState:
            return
          
        # This state has concurrent substates. Therefore we have to make sure we
        # exit them up to this state before we can go any further up the exit chain.
        if state.substates_are_concurrent:
            for current_state in state.current_substates:
                if hasattr(current_state, '_traverse_states_to_exit_skip_state') and current_state._traverse_states_to_exit_skip_state == True:
                    continue
                chain = self._create_state_chain(current_state)
                self._traverse_states_to_exit(chain.popleft() if chain else None, chain, state, go_to_state_actions)
          
        go_to_state_actions.append({ 'action': EXIT_STATE, 'state': state })
        if state.is_current_state():
            setattr(state, '_traverse_states_to_exit_skip_state', True)
        self._traverse_states_to_exit(exit_state_path.popleft() if exit_state_path else None, exit_state_path, stopState, go_to_state_actions)
        
    """ @private
        
      Recursively follow states that are to be entered during the state transition process. The
      enter process is to start from the given state and work its way down a given enter path. When
      the end of enter path has been reached, then continue entering states based on whether 
      an initial substate is defined, there are concurrent substates or history states are to be
      followed; when none of those condition are met then the enter process is done.
          
      @param state {State} the sate to be entered
      @param enter_state_path {collection.deque} a deque representing an initial path of states that are to be entered
      @param pivot_state {State} The state pivoting when to go from exiting states to entering states
      @param use_history {Boolean} indicates whether to recursively follow history states 
    """
    def _traverse_states_to_enter(self, state, enter_state_path, pivot_state, use_history, go_to_state_actions):
        if not state:
            return
          
        # We do not want to enter states in the enter path until the pivot state has been reached. After
        # the pivot state has been reached, then we can go ahead and actually enter states.
        if pivot_state:
            if state is not pivot_state:
                self._traverse_states_to_enter(enter_state_path.pop(), enter_state_path, pivot_state, use_history, go_to_state_actions) # [PORT] pop, now on deque
            else:
                self._traverse_states_to_enter(enter_state_path.pop(), enter_state_path, None, use_history, go_to_state_actions) # [PORT] pop, now on deque
          
        # If no more explicit enter path instructions, then default to enter states based on 
        # other criteria
        elif not enter_state_path or len(enter_state_path) == 0:
            go_to_state_action = { 'action': ENTER_STATE, 'state': state, 'current_state': False }
            go_to_state_actions.append(go_to_state_action)
            
            initial_substate_key = state.initial_substate_key if hasattr(state, 'initial_substate_key') else ''
            history_state = state.history_state
            
            # State has concurrent substates. Need to enter all of the substates
            state_obj = self.get_state(state)
            if state_obj.substates_are_concurrent:
                self._traverse_concurrent_states_to_enter(state_obj.substates, None, use_history, go_to_state_actions)
            
            # State has substates and we are instructed to recursively follow the state's
            # history state if it has one.
            elif state_obj.substates > 0 and history_state and use_history:
                self._traverse_states_to_enter(history_state, None, None, use_history, go_to_state_actions)
            
            # State has an initial substate to enter
            elif initial_substate_key:
                initial_substate_obj = getattr(state, initial_substate_key)
                if initial_substate_obj is not None and isinstance(initial_substate_obj, HistoryState):
                    if not use_history:
                        use_history = initial_substate_obj.is_recursive
                self._traverse_states_to_enter(initial_substate_obj, None, None, use_history, go_to_state_actions)
                
            # Looks like we hit the end of the road. Therefore the state has now become
            # a current state of the statechart.
            else:
                go_to_state_action['current_state'] = True
          
        # Still have an explicit enter path to follow, so keep moving through the path.
        elif len(enter_state_path) > 0:
            go_to_state_actions.append({ 'action': ENTER_STATE, 'state': state, 'current_state': False })
            next_state = enter_state_path.pop() # [PORT] pop, now on deque
            self._traverse_states_to_enter(next_state, enter_state_path, None, use_history, go_to_state_actions)
            
            # We hit a state that has concurrent substates. Must go through each of the substates
            # and enter them
            if state.substates_are_concurrent:
                self._traverse_concurrent_states_to_enter(state.substates, next_state, use_history, go_to_state_actions)
        
    """ @override
        
      Returns True if the named value translates into an executable function on
      any of the statechart's current states or the statechart itself.
          
      @param event {String} the property name to check
      @returns {Boolean}
    """
    def responds_to(self, event):
        for state in self.current_states:
            while state is not None:
                if (state.responds_to_event(event)):
                    return True
                state = state.parent_state
          
        # None of the current states can respond. Now check the statechart itself
        if not hasattr(self, event):
            return False

        return inspect.ismethod(getattr(self, event))
        
    """ @override
        
      Attempts to handle a given event against any of the statechart's current states and the
      statechart itself. If any current state can handle the event or the statechart itself can
      handle the event then True is returned, otherwise False is returned.
        
      @param event {String} what to perform
      @param arg1 {Object} Optional
      @param arg2 {Object} Optional
      @returns {Boolean} True if handled, False if not handled
    """
    def try_to_perform(self, event, arg1=None, arg2=None):
        if not self.responds_to(event):
            return False
      
        if hasattr(self, event) and inspect.ismethod(getattr(self, event)):
            result = getattr(self, event)(arg1, arg2)
            if result != None:
                return True
          
        return self.send_event(event, arg1, arg2) is not None
        
    """
      Used to invoke a method on current states. If the method cannot be executed
      on a current state, then the state's parent states will be tried in order
      of closest ancestry.
          
      A few notes: 
          
       1. Calling this is not the same as calling send_event or send_action.
          Rather, this should be seen as calling normal methods on a state that 
          will *not* call go_to_state or go_to_history_state.
       2. A state will only ever be invoked once per call. So if there are two 
          or more current states that have the same parent state, then that parent 
          state will only be invoked once if none of the current states are able
          to invoke the given method.
          
      When calling this method, you are able to supply zero ore more arguments
      that can be pass onto the method called on the states. As an example
          
          invoke_state_method('render', context, firstTime);
      
      The above call will invoke the render method on the current states
      and supply the context and firstTime arguments to the method. 
          
      Because a statechart can have more than one current state and the method 
      invoked may return a value, the addition of a callback function may be provided 
      in order to handle the returned value for each state. As an example, let's say
      we want to call a calculate method on the current states where the method
      will return a value when invoked. We can handle the returned values like so:
          
          invoke_state_method('calculate', value, function(state, result) {
            # .. handle the result returned from calculate that was invoked
            #    on the given state
          })
          
      If the method invoked does not return a value and a callback function is
      supplied, then result value will simply be undefined. In all cases, if
      a callback function is given, it must be the last value supplied to this
      method.
          
      invoke_state_method will return a value if only one state was able to have 
      the given method invoked on it, otherwise no value is returned. 
          
      @param method_name {String} method_name a method name
      @param args {Object...} Optional. any additional arguments
      @param func {Function} Optional. a callback function. Must be the last
             value supplied if provided.
             
      @returns a value if the number of current states is one, otherwise undefined
               is returned. The value is the result of the method that got invoked
               on a state.
    """
    def invoke_state_method(self, method_name, *args):
        if method_name == 'unknown_event':
            self.statechart_log_error("Cannot invoke method unkownEvent")
            return
          
        callback = None
        checked_states = {}
        called_states = 0
          
        # If last arg is a callback function, set it, popping it off args.
        args = list(args) if args else None
        if args and (inspect.isfunction(args[-1]) or inspect.ismethod(args[-1])):
            callback = args.pop()

        # Search current states for methods matching method_name, call the method on each,
        # and fire the callback on each, if it exists.
        for state in self.current_states:
            while state is not None:
                if state.full_path in checked_states:
                    break
                checked_states[state.full_path] = True
                method = getattr(state, method_name) if hasattr(state, method_name) else None
                if method and inspect.ismethod(method) and not (hasattr(method, 'is_event_handler') and not method.is_event_handler):
                    result = method(*tuple(args if args else []))
                    if callback is not None:
                        callback(state, result)
                    called_states += 1
                    break
                state = state.parent_state
          
        return result if called_states == 1 else None
        
    """ @private
        
      Iterate over all the given concurrent states and enter them
    """
    def _traverse_concurrent_states_to_enter(self, states, exclude, use_history, go_to_state_actions):
        for i in range(len(states)):
            state = states[i]
            if state is not exclude:
                self._traverse_states_to_enter(state, None, None, use_history, go_to_state_actions)
        
    """ @private
        
      Called by go_to_state to flush a pending state transition at the front of the 
      pending queue.
    """
    def _flush_pending_state_transition(self):
        if not self._pending_state_transitions:
            self.statechart_log_error("Unable to flush pending state transition. _pending_state_transitions is invalid.")
            return
        pending = self._pending_state_transitions.popleft() if self._pending_state_transitions else None
        if not pending:
            return
        self.go_to_state(state=pending['state'], from_current_state=pending['from_current_state'], use_history=pending['use_history'], context=pending['context'])
        
    """ @private
      
      Called by send_event to flush a pending actions at the front of the pending
      queue
    """
    def _flush_pending_sent_events(self):
        pending = self._pending_sent_events.popleft() if self._pending_sent_events else None
        if not pending:
            return None
        return self.send_event(pending['event'], pending['arg1'], pending['arg2'])
        
    """ @private """
    def _monitor_is_active_did_change(self, *l):
        if self.monitor_is_active and self.monitor is None:
            self.monitor = StatechartMonitor(self)
        
    """ @private 
        
      Will return a newly constructed root state class. The root state will have substates added to
      it based on properties found on this state that derive from a State class. For the
      root state to be successfully built, the following much be met:
          
       - The root_state_example_class property must be defined with a class that derives from State
       - Either the initial_state_key or states_are_concurrent property must be set, but not both
       - There must be one or more states that can be added to the root state
            
    """
    def _construct_root_state_class(self):
        state_count = 0
        attrs = {}
          
        if inspect.isclass(self.root_state_example_class) and not issubclass(self.root_state_example_class, State):
            self._log_statechart_creation_error("Invalid root state example")
            return None
          
        if self.states_are_concurrent and self.initial_state_key:
            self._log_statechart_creation_error("Cannot assign an initial state when states are concurrent")
        elif self.states_are_concurrent:
            attrs['substates_are_concurrent'] = True
        elif self.initial_state_key:
            attrs['initial_substate_key'] = self.initial_state_key
        else:
            self._log_statechart_creation_error("Must either define initial state or assign states as concurrent")
            return None
          
        # Find the states:
        for key in dir(self):
            if key == '__class__':
                continue

            if key == 'root_state_example_class':
                continue
            
            value = getattr(self, key)

            if inspect.isfunction(value): # [PORT] We don't care about functions here -- States must be classes.
                continue

            if inspect.ismethod(value): # [PORT] And same goes for methods.
                continue
            
            # [PORT] Check for value.plugin removed here. Substates are classes, either defined in-file or imported.
            
            #if isinstance(value, State) and inspect.isclass(value) and self[key] is not self.__init__:
            if inspect.isclass(value) and issubclass(value, State): # [PORT] Compare to same usage in state.py. Same here?
                if key != 'initial_state_key': # [PORT] Don't set this. root_state will only have initial_substate_key, not initial_state_key.
                    attrs[key] = value
                state_count += 1

        if state_count == 0:
            self._log_statechart_creation_error("Must define one or more states")
            return None
          
        # [PORT] Using python type to make a new class...

        if self.root_state_example_class is None:
            return type("RootState", (State,), attrs)
        else:
            return type("RootState", (self.root_state_example_class, ), attrs)

    """ @private """
    def _log_statechart_creation_error(self, msg):
        #Logger.debug("Unable to create statechart for {0}: {1}.".format(self, msg)) # [PORT] Where does debug go in Kivy?
        Logger.info("Unable to create statechart for {0}: {1}.".format(self, msg))
        
    """ 
      Used to log a statechart trace message
    """
    def statechart_log_trace(self, msg):
        Logger.info("{0}: {1}".format(self._statechart_log_prefix(), msg))
        
    """
      Used to log a statechart error message
    """
    def statechart_log_error(self, msg):
        Logger.info("ERROR {0}: {1}".format(self._statechart_log_prefix(), msg)) # [PORT] ditto?
        
    """ 
      Used to log a statechart warning message
    """
    def statechart_log_warning(self, msg):
        if self.suppress_statechart_warnings:
            return
        Logger.info("WARN {0}: {1}".format(self._statechart_log_prefix(), msg))
        
    """ @property """
    def _statechart_log_prefix(self):
        className = self.__class__.__name__
              
        if self.name is None:
            return "{0}".format(className)
        else:
            return "{0}<{1}".format(className, self.name)
      
    """
      @property
          
      Returns an object containing current detailed information about
      the statechart. This is primarily used for diagnostic/debugging
      purposes.
          
      Detailed information includes:
          
        - current states
        - state transtion information
        - event handling information
          
      [PORT] This was a property in javascript.

      @returns {Hash}
    """
    def details(self):
        details = { 'initialized': self.statechart_is_initialized }
          
        if self.name:
            details['name'] = getattr(self, 'name')
          
        if not self.statechart_is_initialized:
            return details
          
        details['current-states'] = []
        for state in self.current_states:
            details['current-states'].append(state.full_path)
          
        state_transition = { 'active': self.go_to_state_active, 'suspended': self.go_to_state_suspended }
      
        if self._go_to_state_actions:
            state_transition['transition-sequence'] = []
                
            for action in self.go_to_state_actions:
                actionName = "enter" if action['action'] == ENTER_STATE else "exit"
                actionName = "{0} {1}".format(actionName, action['state'].full_path)
                state_transition['transition-sequence'].append(actionName)
            
            actionName = "enter" if self._current_go_to_state_action['action'] == ENTER_STATE else "exit"
            actionName = "{0} {1}".format(actionName, self._current_go_to_state_action['state'].full_path)
            state_transition['current-transition'] = actionName
          
        details['state-transition'] = state_transition
          
        if self._state_handle_event_info:
            info = self._state_handle_event_info
            details['handling-event'] = {
              'state': info.state.full_path,
              'event': info.event,
              'handler': info.handler
            }
        else:
            details['handling-event'] = False
          
        return details

    """
      Returns a formatted string of detailed information about this statechart. Useful
      for diagnostic/debugging purposes.
          
      @returns {String}
          
      @see #details
    """
    def to_string_with_details(self):
        return "{0}\n{1}".format(self, self._hash_to_string(self.details, 2))
      
    """ @private """
    def _hash_to_string(self, hash_to_convert, indent):
        hash_as_string = ''
        for key in hash_to_convert:
            value = hash_to_convert[key]
            if isinstance(value, Array):
                hash_as_string += self._array_to_string(key, value, indent) + "\n";
            elif isinstance(value, Object):
                hash_as_string += "{0}{1}:\n".format(' ' * indent, key)
                hash_as_string += self._hash_to_string(value, indent + 2)
            else:
                hash_as_string += "{0}{1}: {2}\n".format(' ' * indent, key, value)
          
        return hash_as_string
        
    """ @private """
    def _array_to_string(self, key, array, indent):
        if len(array) == 0:
            return "{0}{1}: []".format(' ' * indent, key)
          
        array_as_string = "{0}{1}: [\n".format(' ' * indent, key)
          
        for item, idx in array:
            array_as_string += "{0}{1}\n".format(' ' * indent + 2, item)
          
        array_as_string += ' ' * indent + "]"
          
        return array_as_string
      
class StatechartMixin(StatechartManager):
    pass
      
""" 
  The default name given to a statechart's root state
"""
ROOT_STATE_NAME = "__ROOT_STATE__"

"""
  Constants used during the state transition process
"""
EXIT_STATE = 0
ENTER_STATE = 1

"""
  A Startchart class. 
"""
class Statechart(StatechartManager):
    def __init__(self, **kw):
        kw['auto_init_statechart'] = False
        super(Statechart, self).__init__(**kw)
        #StatechartManager.__init__(self)
