# ================================================================================
# Project:   Kivy.Statechart - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

from kivy.event import EventDispatcher
from kivy_statechart.debug.monitor import StatechartMonitor
from kivy_statechart.system.async import Async
from kivy_statechart.system.state import State
from kivy_statechart.system.history_state import HistoryState
from kivy_statechart.system.empty_state import EmptyState
from kivy_statechart.mixins.statechart_delegate import StatechartDelegate
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
        rootState: State.design({
          initialSubstateKey: 'stateA',

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
        initialStateKey: 'stateA',

        stateA: State.design({
          # ... can continue to nest further states
        }),
      
        stateB: State.design({
          # ... can continue to nest further states
        })
      });
  
  If you specified a class that should be used as the root state but used the above method to defined
  states, you can set the rootStateExampleClass property with a class that extends from State. If the 
  rootStateExampleClass property is not explicitly assigned the then default class used will be State.
  
  To provide your statechart with orthogonality, you use concurrent states. If you use concurrent states,
  then your statechart will have multiple current states. That is because each concurrent state represents an
  independent state structure from other concurrent states. The following example shows how to provide your
  statechart with concurrent states:
  
      MyApp.Statechart = Object.extend(StatechartManager, {
        rootState: State.design({
          substatesAreConcurrent: True,

          stateA: State.design({
            # ... can continue to nest further states
          }),
        
          stateB: State.design({
            # ... can continue to nest further states
          })
        })
      });
  
  Above, to indicate that a state's substates are concurrent, you just have to set the substatesAreConcurrent to 
  True. Once done, then stateA and stateB will be independent of each other and each will manage their
  own current substates. The root state will then have more then one current substate.
  
  To define concurrent states directly on the object without explicitly defining a root, you can do the 
  following:
  
      MyApp.Statechart = Object.extend(StatechartManager, {
        statesAreConcurrent: True,

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
        rootState: State.design({
          initialSubstateKey: 'stateA',

          stateA: State.design({
            substatesAreConcurrent: True,

            stateM: State.design({ ... })
            stateN: State.design({ ... })
            stateO: State.design({ ... })
          }),
        
          stateB: State.design({
            initialSubstateKey: 'stateX',

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
        substatesAreConcurrent: True,

        stateM: State.design({ ... })
        stateN: State.design({ ... })
        stateO: State.design({ ... })
      });

      # state_b.js

      MyApp.StateB = State.extend({
        substatesAreConcurrent: True,

        stateM: State.design({ ... })
        stateN: State.design({ ... })
        stateO: State.design({ ... })
      });

      # statechart.js

      MyApp.Statechart = Object.extend(StatechartManager, {
        rootState: State.design({
          initialSubstateKey: 'stateA',
          stateA: State.plugin('MyApp.StateA'),
          stateB: State.plugin('MyApp.StateB')
        })
      });

  Using state plug-in functionality is optional. If you use the plug-in feature you can break up your statechart
  into as many files as you see fit.

  @author Michael Cohen
"""

class StatechartManager(EventDispatcher):
    """
      Computed property that returns an object that adheres to the
      {@link StatechartDelegate} mixin. If the {@link #delegate} is not
      assigned then this object is the default value returned.
      
      @see StatechartDelegate
      @see #delegate
    """
    statechartDelegate = ObjectProperty(None)

    currentStates = ListProperty([])
    gotoStateLocked = BooleanProperty(False)
    gotoStateActive = BooleanProperty(True)
    gotoStateSuspendedPoint = ObjectProperty(None, allownone=True)
    gotoStateSuspended = BooleanProperty(False)
    statechartLogPrefix = StringProperty(None)
    allowStatechartTracing = BooleanProperty(True)
    details = ObjectProperty(None)

    # Walk like a duck
    isResponderContext = BooleanProperty(True)

    # Walk like a duck
    isStatechart = BooleanProperty(True)

    """
      Indicates if this statechart has been initialized
  
      @property {Boolean}
    """
    statechartIsInitialized = BooleanProperty(False)

    """
      Optional name you can provide the statechart. If set this will be included
      in tracing and error output as well as detail output. Useful for 
      debugging/diagnostic purposes
    """
    name = StringProperty(None)
    
    """
      The root state of this statechart. All statecharts must have a root state.
      
      If this property is left unassigned, then when the statechart is initialized
      it will use the rootStateExampleClass, initialStateKey, and statesAreConcurrent
      properties to construct a root state.
      
      @see #rootStateExampleClass
      @see #initialStateKey
      @see #statesAreConcurrent
      
      @property {State}
    """
    rootStateClass = ObjectProperty(None)
    rootStateInstance = ObjectProperty(None, allownone=True)
    
    """ 
      Represents the state used to construct a class that will be the root state for
      this statechart. The class must derive from State. 
      
      This property will only be used if the rootState property is not assigned.
    
      @see #rootState
    
      @property {State}
    """
    rootStateExampleClass = ObjectProperty(None)
    
    """ 
      Indicates what state should be the initial state of this statechart. The value
      assigned must be the name of a property on this object that represents a state.
      As well, the statesAreConcurrent must be set to False.
      
      This property will only be used if the rootState property is not assigned.

      [PORT] This is a String in the original javascript, despite a conditional in initStatechart
             that sets it to the actual state in rootState, and despite a test that compares it
             to actual class objects. Here it is kept a String, and the conditional commented out,
             and the tests changed to check against strings, when either statechart.initialStateKey
             or state.initialSubstateKey are used.
    
      @see #rootState
    
      @property {String} 
    """
    initialStateKey = StringProperty('')
    
    """ 
      Indicates if properties on this object representing states are concurrent to each other.
      If True then they are concurrent, otherwise they are not. If True, then the
      initialStateKey property must not be assigned.
      
      This property will only be used if the rootState property is not assigned.
    
      @see #rootState
    
      @property {Boolean}
    """
    statesAreConcurrent = BooleanProperty(False)
    
    """ 
      Indicates whether to use a monitor for the statechart's activities. If true then
      the monitor will be active, otherwise the monitor will not be used. Useful for debugging
      purposes.
      
      @property {Boolean}
    """
    monitorIsActive = BooleanProperty(False)
    
    """
      A statechart monitor that can be used to monitor this statechart. Useful for debugging purposes.
      A monitor will only be used if monitorIsActive is true.
      
      @property {StatechartMonitor}
    """
    monitor = ObjectProperty(None)
    
    """
      Used to specify what property (key) on the statechart should be used as the trace property. By
      default the property is 'trace'.
  
      @property {String}
    """
    statechartTraceKey = StringProperty('trace')
  
    """
      Indicates whether to trace the statecharts activities. If true then the statechart will output
      its activites to the browser's JS console. Useful for debugging purposes.
  
      @see #statechartTraceKey
  
      @property {Boolean}
    """
    trace = BooleanProperty(False)
    
    """
      Used to specify what property (key) on the statechart should be used as the owner property. By
      default the property is 'owner'.
  
      @property {String}
    """
    statechartOwnerKey = StringProperty('owner')
  
    """
      Sets who the owner is of this statechart. If None then the owner is this object otherwise
      the owner is the assigned object. 
  
      @see #statechartOwnerKey
  
      @property {Object}
    """
    owner = ObjectProperty(None, allownone=True)
  
    """ 
      Indicates if the statechart should be automatically initialized by this
      object after it has been created. If True then initStatechart will be
      called automatically, otherwise it will not.
    
      @property {Boolean}
    """
    autoInitStatechart = BooleanProperty(True)
    
    """
      If yes, any warning messages produced by the statechart or any of its states will
      not be logged, otherwise all warning messages will be logged. 
      
      While designing and debugging your statechart, it's best to keep this value false.
      In production you can then suppress the warning messages.
      
      @property {Boolean}
    """
    suppressStatechartWarnings = BooleanProperty(False)
    
    """
      A statechart delegate used by the statechart and the states that the statechart 
      manages. The value assigned must adhere to the {@link StatechartDelegate} mixin.
      
      @property {Object}
      
      @see StatechartDelegate
    """
    delegate = ObjectProperty(None)

    def __init__(self, **kw):
        #self.bind(currentStates=self._currentStates)
        self.bind(monitorIsActive=self._monitorIsActiveDidChange)
        self.bind(statechartTraceKey=self._statechartTraceDidChange)
        self.bind(delegate=self._statechartDelegate)
        #self.bind(rootState=self._currentStates) # [PORT] Added currentStates property -- moved this to the bottom of initStatechart().
        self.bind(statechartOwnerKey=self._ownerDidChange) # [PORT] Added, to use top-down updating approach in kivy.
        self.bind(owner=self._ownerDidChange) # [PORT] Added, to use top-down updating approach in kivy.
        self.bind(gotoStateLocked=self._gotoStateActive)
        self.bind(gotoStateLocked=self._gotoStateSuspended)
        self.bind(gotoStateSuspendedPoint=self._gotoStateSuspended)

        for k,v in kw.items():
            if k == 'allowStatechartTracing': # [PORT] hack to set self.trace -- why is there also allowStatechartTracing? limit to one or other.
                setattr(self, 'trace', v)
            setattr(self, k, v)

        # [PORT] NOTE: The binding, self.bind(rootStateInstance=self._currentStates) is set at the
        #              bottom of initStatechart(), after instantiation.

        super(StatechartManager, self).__init__(**kw)

        if self.autoInitStatechart == True:
            self.initStatechart()
        
    def _ownerDidChange(self, *l):
        if self.rootStateInstance: # [PORT] rootState can be None
            self.rootStateInstance.statechartOwnerDidChange()

    def _statechartDelegate(self):
        self.statechartDelegate = self.delegateFor('isStatechartDelegate', self.delegate);
        
    def destroyMixin(self):
        self.unbind(statechartTraceKey=_statechartTraceDidChange)
        self.rootStateInstance.destroy();
        self.rootStateInstance = None
      
    """
      Initializes the statechart. By initializing the statechart, it will create all the states and register
      them with the statechart. Once complete, the statechart can be used to go to states and send events to.
    """
    def initStatechart(self):
        if self.statechartIsInitialized:
            return
          
        self.gotoStateLocked = False
        self._sendEventLocked = False
        self._pendingStateTransitions = deque()
        self._pendingSentEvents = deque()
          
        self.sendAction = self.sendEvent
          
        if self.monitorIsActive:
            self.monitor = StatechartMonitor(statechart=self)
      
        self._statechartTraceDidChange() # [PORT] this call needed for kivy?
      
        trace = self.allowStatechartTracing
        rootStateClass = self.rootStateClass # [PORT] Clarify in docs that rootState is None or is a class.
        msg = ''
          
        if trace:
            self.statechartLogTrace("BEGIN initialize statechart")
          
        # If no root state was explicitly defined then try to construct a root state class
        if not rootStateClass:
            rootStateClass = self._constructRootStateClass()
          
        # [PORT] plugin system in javascript version removed in python version. States are classes, declared
        #        either in the source file with the statechart, or imported from individual files.

        if inspect.isclass(rootStateClass) and not issubclass(rootStateClass, State):
            msg = "Unable to initialize statechart. Root state must be a state class"
            self.statechartLogError(msg)
            raise Exception(msg)
          
        # Instantiate the rootState class.
        rootStateInstance = self.createRootState(rootStateClass, ROOT_STATE_NAME)
          
        # Set self.rootStateInstance to be the instantiated object.
        self.rootStateInstance = rootStateInstance

        rootStateInstance.initState()
          
        # The initialState of rootState must be a real state -- can't be the EmptyState.
        problemWithInitialRootState = False
        if hasattr(rootStateInstance, 'initialSubstateKey') and rootStateInstance.initialSubstateKey:
            initialRootState = rootStateInstance.initialSubstateObject
            if initialRootState is None:
                problemWithInitialRootState = True
            elif isinstance(initialRootState, EmptyState):
                problemWithInitialRootState = True
        elif not hasattr(rootStateInstance, 'substatesAreConcurrent') or not rootStateInstance.substatesAreConcurrent:
            problemWithInitialRootState = True

        if problemWithInitialRootState:
            msg = "Unable to initialize statechart. Root state must have an initial substate or substatesAreConcurrent explicitly defined."
            self.statechartLogError(msg)
            raise Exception(msg)

    #if (SC.kindOf(rootState.get('initialSubstate'), SC.EmptyState)) {
      #msg = "Unable to initialize statechart. Root state must have an initial substate explicilty defined";
      #this.statechartLogError(msg);
      #throw msg;
    #}
    #
    ##if (!SC.empty(this.get('initialState'))) {
      #var key = 'initialState';
      #this.set(key, rootState.get(this.get(key)));
    #} 
          
        # In the original javascript, an if here did this:
        #
        #     If the initialStateKey here is set (a string), reset it to the actual state by that name in rootState
        #
        # This is not consistent with initialStateKey defined as a String, but it is consistent with tests that check initialStateKey
        # against actual class objects. Here we will leave it as a String, and skip this set.
        #
        #if self.initialStateKey:
            #self.initialStateKey = getattr(rootState, str(self.initialStateKey))
          
        self.statechartIsInitialized = True

        self.bind(rootStateInstance=self._currentStates)

        self.gotoState(rootStateInstance)
          
        if trace:
            self.statechartLogTrace("END initialize statechart")
        
    """
      Will create a root state for the statechart
    """
    def createRootState(self, state, name):
        return state(statechart=self, name=name)
        
    #"""
      #Returns an array of all the current states for this statechart
      #
      #@returns {Array} the current states
    #"""
    def _currentStates(self, *l):
        self.currentStates = self.rootStateInstance.currentSubstates

    """
      Checks if a given state is a current state of this statechart. 
      
      @param state {State|String} the state to check
      @returns {Boolean} true if the state is a current state, otherwise fals is returned
    """
    def stateIsCurrentState(self, state):
        return self.rootStateInstance.stateIsCurrentSubstate(state)
        
    """
      Returns an array of all the states that are currently entered for
      this statechart.
      
      @returns {Array} the currently entered states
    """
    def enteredStates(self):
        return self.rootStateInstance.enteredSubstates

    """
      Checks if a given state is a currently entered state of this statechart.
      
      @param state {State|String} the state to check
      @returns {Boolean} true if the state is a currently entered state, otherwise false is returned
    """
    def stateIsEntered(self, state):
        return self.rootStateInstance.stateIsEnteredSubstate(state)
        
    """
      Checks if the given value represents a state is this statechart
      
      @param value {State|String} either a state object or the name of a state
      @returns {Boolean} true if the state does belong ot the statechart, otherwise false is returned
    """
    def doesContainState(self, value):
        return self.getState(value) is not None
        
    """
      Gets a state from the statechart that matches the given value
      
      @param value {State|String} either a state object or the name of a state
      @returns {State} if a match then the matching state is returned, otherwise None is returned 
    """
    def getState(self, state):
        if isinstance(state, basestring):
            return self.rootStateInstance if self.rootStateInstance.name == state else self.rootStateInstance.getSubstate(state)
        else:
            return self.rootStateInstance if self.rootStateInstance is state else self.rootStateInstance.getSubstate(state)
      
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
          gotoState(<state>)
            
          # With two arguments.
          gotoState(<state>, <state | boolean | hash>)
        
          # With three arguments.
          gotoState(<state>, <state>, <boolean | hash>)
          gotoState(<state>, <boolean>, <hash>)
        
          # With four arguments.
          gotoState(<state>, <state>, <boolean>, <hash>)
      
      where <state> is either a State object or a string and <hash> is a regular JS hash object.
      
      @param state {State|String} the state to go to (may not be the final state in the transition process)
      @param fromCurrentState {State|String} Optional. The current state to start the transition process from.
      @param useHistory {Boolean} Optional. Indicates whether to include using history states in the transition process
      @param context {Hash} Optional. A context object that will be passed to all exited and entered states
    """
    def gotoState(self, state, fromCurrentState=None, useHistory=None, context=None):
        if not self.statechartIsInitialized:
            self.statechartLogError("can not go to state {0}. statechart has not yet been initialized".format(state))
            return
          
        # [PORT] Removed isDestroyed check -- but this is a punt for a later time...
        #if self.isDestroyed:
            #self.statechartLogError("can not go to state {0}. statechart is destroyed".format(this))
            #return
          
        pivotState = None
        exitStates = deque()
        enterStates = deque()
        trace = self.allowStatechartTracing
        paramState = state
        paramFromCurrentState = fromCurrentState
          
        state = self.getState(state)
          
        if state is None:
            self.statechartLogError("Can not to goto state {0}. Not a recognized state in statechart".format(paramState))
            return
          
        if self.gotoStateLocked:
            # There is a state transition currently happening. Add this requested state
            # transition to the queue of pending state transitions. The request will
            # be invoked after the current state transition is finished.
            self._pendingStateTransitions.append({
              'state': state,
              'fromCurrentState': fromCurrentState,
              'useHistory': useHistory,
              'context': context
            })
            return
          
        # Lock the current state transition so that no other requested state transition 
        # interferes. 
        self.gotoStateLocked = True
          
        if fromCurrentState is not None:
            # Check to make sure the current state given is actually a current state of this statechart
            fromCurrentState = self.getState(fromCurrentState)
            if fromCurrentState is None or not fromCurrentState.isCurrentState():
                msg = "Can not to goto state {0}. {1} is not a recognized current state in statechart"
                self.statechartLogError(msg.format(paramState, paramFromCurrentState))
                self.gotoStateLocked = False
                return
        else:
            # No explicit current state to start from; therefore, need to find a current state
            # to transition from.
            fromCurrentState = state.findFirstRelativeCurrentState()
            if fromCurrentState is None:
                fromCurrentState = self.currentStates[0] if self.currentStates else None
              
        if trace:
            self.statechartLogTrace("BEGIN gotoState: {0}".format(state))
            msg = "starting from current state: {0}"
            msg = msg.format(fromCurrentState if fromCurrentState else '---')
            self.statechartLogTrace(msg)
            msg = "current states before: {0}"
            msg = msg.format(self.currentStates if self.currentStates else '---')
            self.statechartLogTrace(msg)
      
        # If there is a current state to start the transition process from, then determine what
        # states are to be exited
        if fromCurrentState is not None:
            exitStates = self._createStateChain(fromCurrentState)
          
        # Now determine the initial states to be entered
        enterStates = self._createStateChain(state)
          
        # Get the pivot state to indicate when to go from exiting states to entering states
        pivotState = self._findPivotState(exitStates, enterStates)
      
        if pivotState is not None:
            if trace:
                self.statechartLogTrace("pivot state = {0}".format(pivotState))
            if pivotState.substatesAreConcurrent and pivotState is not state:
                msg = "Can not go to state {0} from {1}. Pivot state {2} has concurrent substates."
                self.statechartLogError(msg.format(state, fromCurrentState, pivotState))
                self.gotoStateLocked = False
                return
          
        # Collect what actions to perform for the state transition process
        gotoStateActions = []

        # Go ahead and find states that are to be exited
        self._traverseStatesToExit(exitStates.popleft() if exitStates else None, exitStates, pivotState, gotoStateActions)
          
        # Now go find states that are to be entered
        if pivotState is not state:
            self._traverseStatesToEnter(enterStates.pop(), enterStates, pivotState, useHistory, gotoStateActions)
        else:
            self._traverseStatesToExit(pivotState, deque(), None, gotoStateActions)
            self._traverseStatesToEnter(pivotState, None, None, useHistory, gotoStateActions)
          
        # Collected all the state transition actions to be performed. Now execute them.
        self._gotoStateActions = gotoStateActions
        self._executeGotoStateActions(state, gotoStateActions, None, context)
        
    """
      Indicates if the statechart is in an active goto state process
    """
    def _gotoStateActive(self, *l):
        self.gotoStateActive = self.gotoStateLocked

    """
      Indicates if the statechart is in an active goto state process
      that has been suspended
    """
    def _gotoStateSuspended(self, *l):
        self.gotoStateSuspended = self.gotoStateLocked and self.gotoStateSuspendedPoint is not None # [PORT] this was !!self.gotoStateSuspendedPoint -- boolean force?
        
    """
      Resumes an active goto state transition process that has been suspended.
    """
    def resumeGotoState(self):
        if not self.gotoStateSuspended:
            self.statechartLogError("Can not resume goto state since it has not been suspended")
            return
          
        point = self.gotoStateSuspendedPoint
        self._executeGotoStateActions(point['gotoState'], point['actions'], point['marker'], point['context'])
        
    """ @private """
    def _executeGotoStateActions(self, gotoState, actions, marker, context):
        action = None
        actionResult = None
            
        marker = 0 if marker is None else marker
          
        numberOfActions = len(actions)
        while marker < numberOfActions:
            action = actions[marker]
            self._currentGotoStateAction = action
            if action['action'] == EXIT_STATE:
                actionResult = self._exitState(action['state'], context)
            elif action['action'] == ENTER_STATE:
                actionResult = self._enterState(action['state'], action['currentState'], context)
            
            # Check if the state wants to perform an asynchronous action during
            # the state transition process. If so, then we need to first
            # suspend the state transition process and then invoke the 
            # asynchronous action. Once called, it is then up to the state or something 
            # else to resume this statechart's state transition process by calling the
            # statechart's resumeGotoState method.
            #
            #if actionResult and inspect.isclass(actionResult) and issubclass(actionResult, Async):
            if actionResult and isinstance(actionResult, Async):
                self.gotoStateSuspendedPoint = {
                    'gotoState': gotoState,
                    'actions': actions,
                    'marker': marker + 1,
                    'context': context
                }
              
                actionResult.tryToPerform(self.getState(action['state'])) # [PORT] state arg must be object, not string key
                return

            marker += 1
          
        #self.beginPropertyChanges()
        #self.notifyPropertyChange('currentStates') # [PORT] notify needed here in kivy?
        #self.endPropertyChanges()
        self._currentStates()
          
        if self.allowStatechartTracing:
            self.statechartLogTrace("current states after: {0}".format(self.currentStates))
            self.statechartLogTrace("END gotoState: {0}".format(gotoState))
          
        self._cleanupStateTransition()
        
    """ @private """
    def _cleanupStateTransition(self):
        self._currentGotoStateAction = None
        self.gotoStateSuspendedPoint = None
        self._gotoStateActions = None
        self.gotoStateLocked = False
        if self._pendingStateTransitions: # [PORT] There is an error check in the function that this if now skips. But isn't it ok to be empty?
            self._flushPendingStateTransition()
        
    """ @private """
    def _exitState(self, state, context):
        parentState = None
          
        if state in state.currentSubstates:
            parentState = state.parentState
            while parentState is not None:
                parentState.currentSubstates.remove(state)
                parentState = parentState.parentState
          
        parentState = state;
        while parentState is not None:
            if state in parentState.enteredSubstates:
                parentState.enteredSubstates.remove(state)
            parentState = parentState.parentState
            
        if self.allowStatechartTracing:
            self.statechartLogTrace("<-- exiting state: {0}".format(state))
          
        state.currentSubstates = []
          
        state.stateWillBecomeExited(context)
        result = self.exitState(state, context)
        state.stateDidBecomeExited(context)
          
        if self.monitorIsActive:
            self.monitor.appendExitedState(state)
          
        setattr(state, '_traverseStatesToExit_skipState', False)
          
        return result
        
    """
      What will actually invoke a state's exitState method.
        
      Called during the state transition process whenever the gotoState method is
      invoked.
      
      @param state {State} the state whose enterState method is to be invoked
      @param context {Hash} a context hash object to provide the enterState method
    """
    def exitState(self, state, context):
        return state.exitState(context)
        
    """ @private """
    def _enterState(self, state, current, context):
        state = self.getState(state) # [PORT] Insure this is an obj and not a string.
        parentState = state.parentState
        if parentState and not state.isConcurrentState():
            parentState.historyState = state
          
        if current:
            parentState = state
            while parentState is not None:
                parentState.currentSubstates.append(state)
                parentState = parentState.parentState
          
        parentState = state;
        while parentState is not None:
            parentState.enteredSubstates.append(state)
            parentState = parentState.parentState
          
        if self.allowStatechartTracing:
             self.statechartLogTrace("--> entering state: {0}".format(state))
          
        state.stateWillBecomeEntered(context)
        result = self.enterState(state, context)
        state.stateDidBecomeEntered(context)
          
        if self.monitorIsActive:
            self.monitor.appendEnteredState(state)
          
        return result
        
    """
      What will actually invoke a state's enterState method.
    
      Called during the state transition process whenever the gotoState method is
      invoked.
      
      If the context provided is a state route context object 
      ({@link StateRouteContext}), then if the given state has a enterStateByRoute 
      method, that method will be invoked, otherwise the state's enterState method 
      will be invoked by default. The state route context object will be supplied to 
      both enter methods in either case.
      
      @param state {State} the state whose enterState method is to be invoked
      @param context {Hash} a context hash object to provide the enterState method
    """
    def enterState(self, state, context):
        if hasattr(state, 'enterStateByRoute') and issubclass(context, StateRouteHandlerContext):
            return state.enterStateByRoute(context)
        else:
            return state.enterState(context)
        
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
          gotoHistoryState(<state>)
        
          # With two arguments. 
          gotoHistoryState(<state>, <state | boolean | hash>)
        
          # With three arguments.
          gotoHistoryState(<state>, <state>, <boolean | hash>)
          gotoHistoryState(<state>, <boolean>, <hash>)
        
          # With four argumetns
          gotoHistoryState(<state>, <state>, <boolean>, <hash>)
      
      where <state> is either a State object or a string and <hash> is a regular JS hash object.
      
      @param state {State|String} the state to go to and follow it's history state
      @param fromCurrentState {State|String} Optional. the current state to start the state transition process from
      @param recursive {Boolean} Optional. whether to follow history states recursively.
    """
    def gotoHistoryState(self, state, fromCurrentState=None, recursive=None, context=None):
        if not self.statechartIsInitialized:
            self.statechartLogError("can not go to state {0}'s history state. Statechart has not yet been initialized".format(state))
            return
          
        # [PORT] Assumming that in python argument handling will suffice.
        #args = self._processGotoStateArgs(arguments)
          
        #state = args.state
        #fromCurrentState = args.fromCurrentState
        #recursive = args.useHistory
        #context = args.context
          
        state = self.getState(state)
        
        if state is None:
            self.statechartLogError("Can not to goto state {0}'s history state. Not a recognized state in statechart".format(state))
            return
          
        historyState = state.historyState
          
        if not recursive:
            if historyState is not None:
                self.gotoState(state=historyState, fromCurrentState=fromCurrentState, context=context)
            else:
                self.gotoState(state=state, fromCurrentState=fromCurrentState, context=context)
        else:
            self.gotoState(state=state, fromCurrentState=fromCurrentState, useHistory=True, context=context)

    """ 
      @private 
      Will process the arguments supplied to the gotoState method.
    
      TODO: Come back to this and refactor the code. It works, but it
            could certainly be improved

      [PORT] Instead of this, made args optional, and made gotoState and gotoHistoryState 
             calls with explicit args
    """
    def _processGotoStateArgs(self, args):
        processedArgs = { 
            'state': None, 
            'fromCurrentState': None, 
            'useHistory': False, 
            'context': None 
        }
          
        args = (arg for arg in args if arg)
      
        if (len(args) < 1):
            return processedArgs
      
        processedArgs['state'] = args[0]
    
        if (len(args) == 2):
            value = args[1]
            if isinstance(value, bool):
                processedArgs['useHistory'] = value
            elif (isinstance(value, dict) or isinstance(value, object)) and not isinstance(value, State):
                processedArgs['context'] = value
            else:
                processedArgs['fromCurrentState'] = value
        elif (len(args) == 3):
            value = args[1]
            if isinstance(value, bool):
                processedArgs['useHistory'] = value
                processedArgs['context'] = args[2]
            else:
                processedArgs['fromCurrentState'] = value
                value = args[2]
                if isinstance(value, bool):
                    processedArgs['useHistory'] = value
                else:
                    processedArgs['context'] = value
        else:
            processedArgs['fromCurrentState'] = args[1]
            processedArgs['useHistory'] = args[2]
            processedArgs['context'] = args[3]
      
        return processedArgs
 
    """
      Sends a given event to all the statechart's current states.
          
      If a current state does can not respond to the sent event, then the current state's parent state
      will be tried. This process is recursively done until no more parent state can be tried.
      
      Note that a state will only be checked once if it can respond to an event. Therefore, if
      there is a state S that handles event foo and S has concurrent substates, then foo will
      only be invoked once; not as many times as there are substates. 
      
      @param event {String} name of the event
      @param arg1 {Object} optional argument
      @param arg2 {Object} optional argument
      @returns {Responder} the responder that handled it or None
      
      @see #stateWillTryToHandleEvent
      @see #stateDidTryToHandleEvent
    """
    def sendEvent(self, event, arg1=None, arg2=None):
        # [PORT] Removed isDestroyed check -- but this is a punt for a later time...
        #if self.isDestroyed:
            #self.statechartLogError("can send event {0}. statechart is destroyed".format(event))
            #return

        statechartHandledEvent = False
        eventHandled = False
        currentStatesCopy = self.currentStates[:]
        checkedStates = {}
        state = None
        trace = self.allowStatechartTracing
          
        if self._sendEventLocked or self.gotoStateLocked:
            # Want to prevent any actions from being processed by the states until 
            # they have had a chance to handle the most immediate action or completed 
            # a state transition
            self._pendingSentEvents.append({
                'event': event,
                'arg1': arg1,
                'arg2': arg2
            })
      
            return
          
        self._sendEventLocked = True
          
        if trace:
            self.statechartLogTrace("BEGIN sendEvent: '{0}'".format(event))
          
        for state in currentStatesCopy:
            eventHandled = False
            if not state.isCurrentState():
                continue
            while not eventHandled and state is not None:
                if not state.fullPath in checkedStates:
                    eventHandled = state.tryToHandleEvent(event, arg1, arg2)
                    checkedStates[state.fullPath] = True
                if not eventHandled:
                    state = state.parentState
                else:
                    statechartHandledEvent = True
          
        # Now that all the states have had a chance to process the 
        # first event, we can go ahead and flush any pending sent events.
        self._sendEventLocked = False
          
        if trace:
            if not statechartHandledEvent:
                self.statechartLogTrace("No state was able handle event {0}".format(event))
            self.statechartLogTrace("END sendEvent: '{0}'".format(event))
          
        result = self._flushPendingSentEvents()
          
        return self if statechartHandledEvent else (self if result else None)
        
    """
      Used to notify the statechart that a state will try to handle event that has been passed
      to it.
          
      @param {State} state the state that will try to handle the event
      @param {String} event the event the state will try to handle
      @param {String} handler the name of the method on the state that will try to handle the event 
    """
    def stateWillTryToHandleEvent(self, state, event, handler):
        self._stateHandleEventInfo = {
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
    def stateDidTryToHandleEvent(self, state, event, handler, handled):
        self._stateHandleEventInfo = None
      
    """ @private
    
      Creates a chain of states from the given state to the greatest ancestor state (the root state). Used
      when perform state transitions.
    """
    def _createStateChain(self, state):
        chain = deque()
          
        while state is not None:
            chain.append(state)
            state = state.parentState
          
        return chain
        
    """ @private
    
      Finds a pivot state from two given state chains. The pivot state is the state indicating when states
      go from being exited to states being entered during the state transition process. The value 
      returned is the fist matching state between the two given state chains. 
    """
    def _findPivotState(self, stateChain1, stateChain2):
        if len(stateChain1) == 0 or len(stateChain2) == 0:
            return None
          
        for state in stateChain1:
            if state in stateChain2:
                return state

    """ @private
          
      Recursively follow states that are to be exited during a state transition process. The exit
      process is to start from the given state and work its way up to when either all exit
      states have been reached based on a given exit path or when a stop state has been reached.
          
      @param state {State} the state to be exited
      @param exitStatePath {collections.deque} a deque representing a path of states that are to be exited
      @param stopState {State} an explicit state in which to stop the exiting process
    """
    def _traverseStatesToExit(self, state, exitStatePath, stopState, gotoStateActions):
        if state is None or state is stopState:
            return
          
        trace = self.allowStatechartTracing
          
        # This state has concurrent substates. Therefore we have to make sure we
        # exit them up to this state before we can go any further up the exit chain.
        if state.substatesAreConcurrent:
            for currentState in state.currentSubstates:
                if hasattr(currentState, '_traverseStatesToExit_skipState') and currentState._traverseStatesToExit_skipState == True:
                    continue
                chain = self._createStateChain(currentState)
                self._traverseStatesToExit(chain.popleft() if chain else None, chain, state, gotoStateActions)
          
        gotoStateActions.append({ 'action': EXIT_STATE, 'state': state })
        if state.isCurrentState():
            setattr(state, '_traverseStatesToExit_skipState', True)
        self._traverseStatesToExit(exitStatePath.popleft() if exitStatePath else None, exitStatePath, stopState, gotoStateActions)
        
    """ @private
        
      Recursively follow states that are to be entered during the state transition process. The
      enter process is to start from the given state and work its way down a given enter path. When
      the end of enter path has been reached, then continue entering states based on whether 
      an initial substate is defined, there are concurrent substates or history states are to be
      followed; when none of those condition are met then the enter process is done.
          
      @param state {State} the sate to be entered
      @param enterStatePath {collection.deque} a deque representing an initial path of states that are to be entered
      @param pivotState {State} The state pivoting when to go from exiting states to entering states
      @param useHistory {Boolean} indicates whether to recursively follow history states 
    """
    def _traverseStatesToEnter(self, state, enterStatePath, pivotState, useHistory, gotoStateActions):
        if not state:
            return
          
        trace = self.allowStatechartTracing
          
        # We do not want to enter states in the enter path until the pivot state has been reached. After
        # the pivot state has been reached, then we can go ahead and actually enter states.
        if pivotState:
            if state is not pivotState:
                self._traverseStatesToEnter(enterStatePath.pop(), enterStatePath, pivotState, useHistory, gotoStateActions) # [PORT] pop, now on deque
            else:
                self._traverseStatesToEnter(enterStatePath.pop(), enterStatePath, None, useHistory, gotoStateActions) # [PORT] pop, now on deque
          
        # If no more explicit enter path instructions, then default to enter states based on 
        # other criteria
        elif not enterStatePath or len(enterStatePath) == 0:
            gotoStateAction = { 'action': ENTER_STATE, 'state': state, 'currentState': False }
            gotoStateActions.append(gotoStateAction)
            
            initialSubstateKey = state.initialSubstateKey if hasattr(state, 'initialSubstateKey') else ''
            historyState = state.historyState
            
            # State has concurrent substates. Need to enter all of the substates
            stateObj = self.getState(state)
            if stateObj.substatesAreConcurrent:
                self._traverseConcurrentStatesToEnter(stateObj.substates, None, useHistory, gotoStateActions)
            
            # State has substates and we are instructed to recursively follow the state's
            # history state if it has one.
            elif stateObj.substates > 0 and historyState and useHistory:
                self._traverseStatesToEnter(historyState, None, None, useHistory, gotoStateActions)
            
            # State has an initial substate to enter
            elif initialSubstateKey:
                initialSubstateObj = getattr(state, initialSubstateKey)
                if initialSubstateObj is not None and isinstance(initialSubstateObj, HistoryState):
                    if not useHistory:
                        useHistory = initialSubstateObj.isRecursive
                self._traverseStatesToEnter(initialSubstateObj, None, None, useHistory, gotoStateActions)
                
            # Looks like we hit the end of the road. Therefore the state has now become
            # a current state of the statechart.
            else:
                gotoStateAction['currentState'] = True
          
        # Still have an explicit enter path to follow, so keep moving through the path.
        elif len(enterStatePath) > 0:
            gotoStateActions.append({ 'action': ENTER_STATE, 'state': state, 'currentState': False })
            nextState = enterStatePath.pop() # [PORT] pop, now on deque
            self._traverseStatesToEnter(nextState, enterStatePath, None, useHistory, gotoStateActions)
            
            # We hit a state that has concurrent substates. Must go through each of the substates
            # and enter them
            if state.substatesAreConcurrent:
                self._traverseConcurrentStatesToEnter(state.substates, nextState, useHistory, gotoStateActions)
        
    """ @override
        
      Returns True if the named value translates into an executable function on
      any of the statechart's current states or the statechart itself.
          
      @param event {String} the property name to check
      @returns {Boolean}
    """
    def respondsTo(self, event):
        for state in self.currentStates:
            while state is not None:
                if (state.respondsToEvent(event)):
                    return True
                state = state.parentState
          
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
    def tryToPerform(self, event, arg1=None, arg2=None):
        if not self.respondsTo(event):
            return False
      
        if hasattr(self, event) and inspect.ismethod(getattr(self, event)):
            result = getattr(self, event)(arg1, arg2)
            if result != None:
                return True
          
        return self.sendEvent(event, arg1, arg2) is not None
        
    """
      Used to invoke a method on current states. If the method can not be executed
      on a current state, then the state's parent states will be tried in order
      of closest ancestry.
          
      A few notes: 
          
       1. Calling this is not the same as calling sendEvent or sendAction.
          Rather, this should be seen as calling normal methods on a state that 
          will *not* call gotoState or gotoHistoryState.
       2. A state will only ever be invoked once per call. So if there are two 
          or more current states that have the same parent state, then that parent 
          state will only be invoked once if none of the current states are able
          to invoke the given method.
          
      When calling this method, you are able to supply zero ore more arguments
      that can be pass onto the method called on the states. As an example
          
          invokeStateMethod('render', context, firstTime);
      
      The above call will invoke the render method on the current states
      and supply the context and firstTime arguments to the method. 
          
      Because a statechart can have more than one current state and the method 
      invoked may return a value, the addition of a callback function may be provided 
      in order to handle the returned value for each state. As an example, let's say
      we want to call a calculate method on the current states where the method
      will return a value when invoked. We can handle the returned values like so:
          
          invokeStateMethod('calculate', value, function(state, result) {
            # .. handle the result returned from calculate that was invoked
            #    on the given state
          })
          
      If the method invoked does not return a value and a callback function is
      supplied, then result value will simply be undefined. In all cases, if
      a callback function is given, it must be the last value supplied to this
      method.
          
      invokeStateMethod will return a value if only one state was able to have 
      the given method invoked on it, otherwise no value is returned. 
          
      @param methodName {String} methodName a method name
      @param args {Object...} Optional. any additional arguments
      @param func {Function} Optional. a callback function. Must be the last
             value supplied if provided.
             
      @returns a value if the number of current states is one, otherwise undefined
               is returned. The value is the result of the method that got invoked
               on a state.
    """
    def invokeStateMethod(self, methodName, *args):
        if methodName == 'unknownEvent':
            self.statechartLogError("can not invoke method unkownEvent")
            return
          
        callback = None
        checkedStates = {}
        calledStates = 0
          
        # If last arg is a callback function, set it, popping it off args.
        args = list(args) if args else None
        if args and (inspect.isfunction(args[-1]) or inspect.ismethod(args[-1])):
            callback = args.pop()

        # Search current states for methods matching methodName, call the method on each,
        # and fire the callback on each, if it exists.
        for state in self.currentStates:
            while state is not None:
                if state.fullPath in checkedStates:
                    break
                checkedStates[state.fullPath] = True
                method = getattr(state, methodName) if hasattr(state, methodName) else None
                if method and inspect.ismethod(method) and not (hasattr(method, 'isEventHandler') and not method.isEventHandler):
                    result = method(*tuple(args if args else []))
                    if callback is not None:
                        callback(state, result)
                    calledStates += 1
                    break
                state = state.parentState
          
        return result if calledStates == 1 else None
        
    """ @private
        
      Iterate over all the given concurrent states and enter them
    """
    def _traverseConcurrentStatesToEnter(self, states, exclude, useHistory, gotoStateActions):
        for i in range(len(states)):
            state = states[i]
            if state is not exclude:
                self._traverseStatesToEnter(state, None, None, useHistory, gotoStateActions)
        
    """ @private
        
      Called by gotoState to flush a pending state transition at the front of the 
      pending queue.
    """
    def _flushPendingStateTransition(self):
        if not self._pendingStateTransitions:
            self.statechartLogError("Unable to flush pending state transition. _pendingStateTransitions is invalid.")
            return
        pending = self._pendingStateTransitions.popleft() if self._pendingStateTransitions else None
        if not pending:
            return
        self.gotoState(state=pending['state'], fromCurrentState=pending['fromCurrentState'], useHistory=pending['useHistory'], context=pending['context'])
        
    """ @private
      
      Called by sendEvent to flush a pending actions at the front of the pending
      queue
    """
    def _flushPendingSentEvents(self):
        pending = self._pendingSentEvents.popleft() if self._pendingSentEvents else None
        if not pending:
            return None
        return self.sendEvent(pending['event'], pending['arg1'], pending['arg2'])
        
    """ @private """
    def _monitorIsActiveDidChange(self, *l):
        if self.monitorIsActive and self.monitor is None:
            self.monitor = StatechartMonitor(self)
        
    """ @private 
        
      Will return a newly constructed root state class. The root state will have substates added to
      it based on properties found on this state that derive from a State class. For the
      root state to be successfully built, the following much be met:
          
       - The rootStateExampleClass property must be defined with a class that derives from State
       - Either the initialStateKey or statesAreConcurrent property must be set, but not both
       - There must be one or more states that can be added to the root state
            
    """
    def _constructRootStateClass(self):
        stateCount = 0
        attrs = {}
          
        if inspect.isclass(self.rootStateExampleClass) and not issubclass(self.rootStateExampleClass, State):
            self._logStatechartCreationError("Invalid root state example")
            return None
          
        if self.statesAreConcurrent and self.initialStateKey:
            self._logStatechartCreationError("Can not assign an initial state when states are concurrent")
        elif self.statesAreConcurrent:
            attrs['substatesAreConcurrent'] = True
        elif self.initialStateKey:
            attrs['initialSubstateKey'] = self.initialStateKey
        else:
            self._logStatechartCreationError("Must either define initial state or assign states as concurrent")
            return None
          
        # Find the states:
        for key in dir(self):
            if key == '__class__':
                continue

            if key == 'rootStateExampleClass':
                continue
            
            value = getattr(self, key)

            if inspect.isfunction(value): # [PORT] We don't care about functions here -- States must be classes.
                continue

            if inspect.ismethod(value): # [PORT] And same goes for methods.
                continue
            
            # [PORT] Check for value.plugin removed here. Substates are classes, either defined in-file or imported.
            
            #if isinstance(value, State) and inspect.isclass(value) and self[key] is not self.__init__:
            if inspect.isclass(value) and issubclass(value, State): # [PORT] Compare to same usage in state.py. Same here?
                if key != 'initialStateKey': # [PORT] Don't set this. rootState will only have initialSubstateKey, not initialStateKey.
                    attrs[key] = value
                stateCount += 1

        if stateCount == 0:
            self._logStatechartCreationError("Must define one or more states")
            return None
          
        # [PORT] Using python type to make a new class...

        if self.rootStateExampleClass is None:
            return type("RootState", (State,), attrs)
        else:
            return type("RootState", (self.rootStateExampleClass, ), attrs)

    """ @private """
    def _logStatechartCreationError(self, msg):
        #Logger.debug("Unable to create statechart for {0}: {1}.".format(self, msg)) # [PORT] Where does debug go in Kivy?
        Logger.info("Unable to create statechart for {0}: {1}.".format(self, msg))
        
    """ 
      Used to log a statechart trace message
    """
    def statechartLogTrace(self, msg):
        Logger.info("{0}: {1}".format(self.statechartLogPrefix, msg))
        
    """
      Used to log a statechart error message
    """
    def statechartLogError(self, msg):
        Logger.info("ERROR {0}: {1}".format(self.statechartLogPrefix, msg)) # [PORT] ditto?
        
    """ 
      Used to log a statechart warning message
    """
    def statechartLogWarning(self, msg):
        if self.suppressStatechartWarnings:
            return
        Logger.info("WARN {0}: {1}".format(self.statechartLogPrefix, msg))
        
    """ @property """
    def _statechartLogPrefix(self):
        className = self.__name__
        name = self.name, prefix;
              
        if self.name is None:
            prefix = "{0}<{1}>".format(className, guidFor(self))
        else:
            prefix = "{0}<{1}, {2}>".format(className, name, guidFor(self))
          
        self.statechartLogPrefix = prefix
      
    """ @private @property """
    def _allowStatechartTracing(self):
        self.allowStatechartTracing = getattr(self, self.statechartTraceKey)
      
    """ @private """
    def _statechartTraceDidChange(self):
        #self.notifyPropertyChange('allowStatechartTracing')
        #pass # [PORT] notify needed here in kivy?
        self._allowStatechartTracing()
        
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
        details = { 'initialized': self.statechartIsInitialized }
          
        if self.name:
            details['name'] = getattr(self, 'name')
          
        if not self.statechartIsInitialized:
            return details
          
        details['current-states'] = []
        for state in self.currentStates:
            details['current-states'].append(state.fullPath)
          
        stateTransition = { 'active': self.gotoStateActive, 'suspended': self.gotoStateSuspended }
      
        if self._gotoStateActions:
            stateTransition['transition-sequence'] = []
                
            for action in self.gotoStateActions:
                actionName = "enter" if action['action'] == ENTER_STATE else "exit"
                actionName = "{0} {1}".format(actionName, action['state'].fullPath)
                stateTransition['transition-sequence'].append(actionName)
            
            actionName = "enter" if self._currentGotoStateAction['action'] == ENTER_STATE else "exit"
            actionName = "{0} {1}".format(actionName, self._currentGotoStateAction['state'].fullPath)
            stateTransition['current-transition'] = actionName
          
        details['state-transition'] = stateTransition
          
        if self._stateHandleEventInfo:
            info = self._stateHandleEventInfo
            details['handling-event'] = {
              'state': info.state.fullPath,
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
    def toStringWithDetails(self):
        str = ""
        header = self.toString()
        details = self.details
          
        str += header + "\n"
        str += self._hashToString(details, 2)
          
        return str;
      
    """ @private """
    def _hashToString(self, hashToConvert, indent):
        hashAsString = ''
        for key in hashToConvert:
            value = hashToConvert[key]
            if isinstance(value, Array):
                hashAsString += self._arrayToString(key, value, indent) + "\n";
            elif isinstance(value, Object):
                hashAsString += "{0}{1}:\n".format(' ' * indent, key)
                hashAsString += self._hashToString(value, indent + 2)
            else:
                hashAsString += "{0}{1}: {2}\n".format(' ' * indent, key, value)
          
        return hashAsString
        
    """ @private """
    def _arrayToString(self, key, array, indent):
        if len(array) == 0:
            return "{0}{1}: []".format(' ' * indent, key)
          
        arrayAsString = "{0}{1}: [\n".format(' ' * indent, key)
          
        for item, idx in array:
            arrayAsString += "{0}{1}\n".format(' ' * indent + 2, item)
          
        arrayAsString += ' ' * indent + "]"
          
        return arrayAsString
      
class StatechartMixin(StatechartManager, StatechartDelegate): # [PORT] also sublassed here was DelegateSupport, from SC
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
        kw['autoInitStatechart'] = False
        super(Statechart, self).__init__(**kw)
        #StatechartManager.__init__(self)
