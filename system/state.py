# ================================================================================
# Project:   Kivy.Statechart - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

from kivy.event import EventDispatcher
from kivy_statechart.private.state_path_matcher import StatePathMatcher
from kivy_statechart.system.async import AsyncMixin
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty, StringProperty
from collections import deque

import inspect, re

REGEX_TYPE = type(re.compile(''))

"""
  @class

  Represents a state within a statechart. 
  
  The statechart actively manages all states belonging to it. When a state is created, 
  it immediately registers itself with it parent states. 
  
  You do not create an instance of a state itself. The statechart manager will go through its 
  state heirarchy and create the states itself.

  For more information on using statecharts, see StatechartManager.

  @author Michael Cohen
  @extends Object
"""
class State(EventDispatcher):
    """ 
      Indicates if this state should trace actions. Useful for debugging
      purposes. Managed by the statechart.
        
      @see StatechartManager#trace
        
      @property {Boolean}
    """
    trace = BooleanProperty(False)

    """ 
      Indicates who the owner is of this state. If not set on the statechart
      then the owner is the statechart, otherwise it is the assigned
      object. Managed by the statechart.
          
      @see StatechartManager#owner
        
      @property {Object}
    """
    owner = ObjectProperty(None)

    """
      Returns the statechart's assigned delegate. A statechart delegate is one
      that adheres to the {@link StatechartDelegate} mixin. 
        
      @property {Object}
          
      @see StatechartDelegate
    """
    statechartDelegate = ObjectProperty(None)

    """
      A volatile property used to get and set the app's current location. 
          
      This computed property defers to the the statechart's delegate to 
      actually update and acquire the app's location.
          
      Note: Binding for this pariticular case is discouraged since in most
      cases we need the location value immediately. If we were to use
      bindings then the location value wouldn't be updated until at least
      the end of one run loop. It is also advised that the delegate not
      have its `statechartUpdateLocationForState` and
      `statechartAcquireLocationForState` methods implemented where bindings
      are used since they will inadvertenly stall the location value from
      propogating immediately.
          
      @property {String}
          
      @see StatechartDelegate#statechartUpdateLocationForState
      @see StatechartDelegate#statechartAcquireLocationForState
    """
    location = StringProperty(None) # [TODO] marked as idempotent in js

    fullPath = StringProperty(None)

    """
      The name of the state
          
      @property {String}
    """
    name = StringProperty(None)

    """
      This state's parent state. Managed by the statechart
   
      @property {State}
    """
    parentState = ObjectProperty(None)

    """
      This state's history state. Can be null. Managed by the statechart.
          
      @property {State}
    """
    historyState = ObjectProperty(None)

    """
      Used to indicate the initial substate of this state to enter into. 
          
      You assign the value with the name of the state. Upon creation of 
      the state, the statechart will automatically change the property 
      to be a corresponding state object
      
      The substate is only to be this state's immediate substates. If
      no initial substate is assigned then this states initial substate
      will be an instance of an empty state (EmptyState).
      
      Note that a statechart's root state must always have an explicity
      initial substate value assigned else an error will be thrown.
      
      @property {String|State}
    """
    initialSubstateKey = StringProperty('')

    """
      Used to indicates if this state's immediate substates are to be
      concurrent (orthogonal) to each other. 
      
      @property {Boolean}
    """
    substatesAreConcurrent = BooleanProperty(False)

    """
      The immediate substates of this state. Managed by the statechart.
      
      @property {Array}
    """
    substates = ListProperty([])

    """
      The statechart that this state belongs to. Assigned by the owning
      statechart.
    
      @property {Statechart}
    """
    statechart = ObjectProperty(None)

    """
      Indicates if this state has been initialized by the statechart
      
      @propety {Boolean}
    """
    stateIsInitialized = BooleanProperty(False)

    """
      An array of this state's current substates. Managed by the statechart
      
      @propety {Array}
    """
    currentSubstates = ListProperty([])

    """ 
      An array of this state's substates that are currently entered. Managed by
      the statechart.
      
      @property {Array}
    """
    enteredSubstates = ListProperty([])

    """
      Can optionally assign what route this state is to represent. 
      
      If assigned then this state will be notified to handle the route when triggered
      any time the app's location changes and matches this state's assigned route. 
      The handler invoked is this state's {@link #routeTriggered} method. 
      
      The value assigned to this property is dependent on the underlying routing 
      mechanism used by the application. The default routing mechanism is to use 
      routes.
      
      @property {String|Hash}
      
      @see #routeTriggered
      @see #location
      @see StatechartDelegate
    """
    representRoute = StringProperty(None)

    #isRootState = BooleanProperty(False)
    #isCurrentState = BooleanProperty(False)
    #isConcurrentState = BooleanProperty(False)
    #isEnteredState = BooleanProperty(False)
    #hasCurrentSubstates = BooleanProperty(False)
    #hasEnteredSubstates = BooleanProperty(False)

    def __init__(self, **kwargs):
        #self.bind(currentSubstates=self._isCurrentState)
        #self.bind(enteredSubstates=self._isEnteredState)
        #self.bind(currentSubstates=self._hasCurrentSubstates)
        #self.bind(enteredSubstates=self._hasEnteredSubstates)
        #self.bind(enteredSubstates=self._enteredSubstatesDidChange) # [PORT] .observes("*enteredSubstates.[]")
        #self.bind(currentSubstates=self._currentSubstatesDidChange) # [PORT] .observes("*currentSubstates.[]")

        self.bind(name=self._fullPath)
        self.bind(parentState=self._fullPath)
        #self.bind(parentState=self._isConcurrentState) # [PORT] Why is this commented out?

        self.bind(statechart=self._trace)
        self.bind(statechart=self._owner)
        self.bind(statechart=self._statechartDelegate)
        self.bind(statechartDelegate=self._location)

        self._registeredEventHandlers = {}
        self._registeredStringEventHandlers = {}
        self._registeredRegExpEventHandlers = []
        self._registeredStateObserveHandlers = {}
        self._registeredSubstatePaths = {}
        self._registeredSubstates = []
        self._isEnteringState = False
        self._isExitingState = False
        
        # [PORT] Not sure: ...

        # Setting up observes this way is faster then using .observes,
        # which adds a noticable increase in initialization time.
    
        sc = self.statechart
    
        self.ownerKey = sc.statechartOwnerKey if sc else None
        self.traceKey = sc.statechartOwnerKey if sc else None
    
        if sc is not None:
            self.bind(ownerKey=self._statechartOwnerDidChange) # [PORT] Changed to bind to self, to try to do it from here...
            self.bind(traceKey=self._statechartTraceDidChange)

        for k,v in kwargs.items():
            if k == 'initialSubstateKey':
                # [PORT] Force initialSubstateKey to always be string.
                if isinstance(v, basestring):
                    self.initialSubstateKey = v
                else:
                    name = v.name if hasattr(v, 'name') else None
                    if not name:
                        name = v.__name__ if hasattr(v, '__name__') else None
                    self.initialSubstateKey = name if name else None
            else:
                setattr(self, k, v)

        super(State, self).__init__() # [PORT] initialize how? We have also initState()

    def _trace(self, *l):
        key = self.statechart.statechartTraceKey
        self.trace = getattr(self.statechart, key) if hasattr(self.statechart, key) else None

    def _owner(self, *l):
        sc = self.statechart
        key = sc.statechartOwnerKey if sc else None
        owner = getattr(sc, key) if sc else None
        self.owner = owner if owner else sc

    def statechartOwnerDidChange(self):
        self._owner()

        for substate in self.substates:
            substate.statechartOwnerDidChange()

    def _statechartDelegate(self, *l):
        self.statechartDelegate = self.statechart.statechartDelegate

    def _location(self, instance, value, *l):
        sc = self.statechart
        delegate = self.statechartDelegate
        delegate.statechartUpdateLocationForState(sc, value, self if value else None)
        self.location = delegate.statechartAcquireLocationForState(sc, self)
        
    def destroy(self):
        sc = self.statechart

        self.ownerKey = sc.statechartOwnerKey if sc else None
        self.traceKey = sc.statechartOwnerKey if sc else None
    
        if sc is not None:
            self.unbind(ownerKey=self._statechartOwnerDidChange)
            self.unbind(traceKey=self._statechartTraceDidChange)

        substates = self.substates
    
        if substates is not None:
            for state in substates:
                state.destroy()
    
        self._teardownAllStateObserveHandlers()
    
        self.substates = None
        self.currentSubstates = None
        self.enteredSubstates = None
        self.parentState = None
        self.historyState = None
        self.initialSubstateKey = ''
        self.statechart = None
    
        #self.notifyPropertyChange("trace") # [PORT] Use kivy's dispatch?
        #self.notifyPropertyChange("owner")
    
        self._registeredEventHandlers = None
        self._registeredStringEventHandlers = None
        self._registeredRegExpEventHandlers = None
        self._registeredStateObserveHandlers = None
        self._registeredSubstatePaths = None
        self._registeredSubstates = None
    
        #sc_super()

    """
      Used to initialize this state. To only be called by the owning statechart.
    """
    def initState(self):
        if self.stateIsInitialized:
            return  
    
        self._registerWithParentStates()
        self._setupRouteHandling()
    
        substates = []
        matchedInitialSubstate = False
        valueIsMethod = False
        historyState = None
    
        self.substates = substates
    
        if self.initialSubstateKey:
            initialSubstate = self.getSubstate(self.initialSubstateKey)
            from kivy_statechart.system.history_state import HistoryState
            if initialSubstate is not None and issubclass(initialSubstate, HistoryState):
                historyState = self.createSubstate(self.initialSubstateKey)
          
                self.initialSubstateKey = historyState.name
          
                if not historyState.defaultState:
                    self.stateLogError("Initial substate is invalid. History state requires the name of a default state to be set")
                    self.initialSubstateKey = ''
                    historyState = None
    
        # Iterate through all this state's substates, if any, create them, and then initialize
        # them. This causes a recursive process.
        for key in dir(self):
            if key == '__class__':
                continue

            value = getattr(self, key)
            if not inspect.ismethod(value) and not inspect.isclass(value):
                continue

            valueIsMethod = inspect.ismethod(value)
      
            if valueIsMethod and hasattr(value, 'isEventHandler') and value.isEventHandler == True:
                self._registerEventHandler(key, value)
                continue

            if valueIsMethod and hasattr(value, 'isStateObserveHandler') and value.isStateObserveHandler == True:
                self._registerStateObserveHandler(key, value)
                continue

            # [PORT] Removed statePlugin system. Use import in python.

            #if inspect.isclass(value) and issubclass(value, State) and getattr(self, key) is not self.__init__: # [PORT] using inspect
            if inspect.isclass(value) and issubclass(value, State):
                state = self._addSubstate(key, value, None)
                if key == self.initialSubstateKey:
                    self.initialSubstateKey = state if isinstance(state, basestring) else state.name # [PORT] Needs to always be a string.
                    matchedInitialSubstate = True
                elif historyState and historyState.defaultState == key:
                    historyState.defaultState = state if isinstance(state, basestring) else state.name # [PORT] Needs to always be a string.
                    matchedInitialSubstate = True

        if self.initialSubstateKey and not matchedInitialSubstate:
            msg = "Unable to set initial substate {0} since it did not match any of state {1}'s substates"
            self.stateLogError(msg.format(self.initialSubstateKey, self))

        if len(self.substates) == 0:
            if self.initialSubstateKey:
                msg = "Unable to make {0} an initial substate since state {1} has no substates"
                self.stateLogWarning(msg.format(self.initialSubstateKey, self))
        elif len(self.substates) > 0:
              state = self._addEmptyInitialSubstateIfNeeded()
              if state is None and self.initialSubstateKey and self.substatesAreConcurrent:
                    self.initialSubstateKey = ''
                    msg = "Can not use {0} as initial substate since substates are all concurrent for state {1}"
                    self.stateLogWarning(msg.format(self.initialSubstateKey, self))

        #self.notifyPropertyChange("substates")
        # [PORT] substates have changed. Call _currentStates on statechart, which is bound to rootState,
        #        and updates self.currentStates = self.rootState.substates. That binding won't fire if 
        #        rootState.substates changes, so we manually call it in kivy.
        self.statechart._currentStates()

        self.currentSubstates = []
        self.enteredSubstates = []
        self.stateIsInitialized = True

    """ @private 
    
      Used to bind this state with a route this state is to represent if a route has been assigned.
      
      When invoked, the method will delegate the actual binding strategy to the statechart delegate 
      via the delegate's {@link StatechartDelegate#statechartBindStateToRoute} method.
      
      Note that a state cannot be bound to a route if this state is a concurrent state.
      
      @see #representRoute
      @see StatechartDelegate#statechartBindStateToRoute
    """
    def _setupRouteHandling(self):
        route = self.representRoute
        sc = self.statechart
        delegate = self.statechartDelegate

        if route is None:
            return
    
        if self.isConcurrentState():
            self.stateLogError("State {0} cannot handle route '{1}' since state is concurrent".format(self, route))
            return
    
        delegate.statechartBindStateToRoute(sc, self, route, self.routeTriggered)

    """
      Main handler that gets triggered whenever the app's location matches this state's assigned
      route. 
      
      When invoked the handler will first refer to the statechart delegate to determine if it
      should actually handle the route via the delegate's 
      {@see StatechartDelegate#statechartShouldStateHandleTriggeredRoute} method. If the 
      delegate allows the handling of the route then the state will continue on with handling
      the triggered route by calling the state's {@link #handleTriggeredRoute} method, otherwise 
      the state will cancel the handling and inform the delegate through the delegate's 
      {@see StatechartDelegate#statechartStateCancelledHandlingRoute} method.
      
      The handler will create a state route context ({@link StateRouteContext}) object 
      that packages information about what is being currently handled. This context object gets 
      passed along to the delegate's invoked methods as well as the state transition process. 
      
      Note that this method is not intended to be directly called or overridden.
      
      @see #representRoute
      @see StatechartDelegate#statechartShouldStateHandleRoute
      @see StatechartDelegate#statechartStateCancelledHandlingRoute
      @see #createStateRouteHandlerContext
      @see #handleTriggeredRoute
    """
    def routeTriggered(self, params):
        if self._isEnteringState:
            return

        sc = self.statechart
        delegate = self.statechartDelegate
        loc = self.location
    
        attr = {
            'state': self,
            'location': loc,
            'params': params,
            'handler': self.routeTriggered
        }

        context = self.createStateRouteHandlerContext(attr)

        if delegate.statechartShouldStateHandleTriggeredRoute(sc, self, context):
            if self.trace and loc:
                self.stateLogTrace("will handle route '{0}'".format(loc))
            self.handleTriggeredRoute(context)
        else:
            delegate.statechartStateCancelledHandlingTriggeredRoute(sc, self, context)

    """
      Constructs a new instance of a state routing context object.
      
      @param {Hash} attr attributes to apply to the constructed object
      @return {StateRouteContext}
      
      @see #handleRoute
    """
    def createStateRouteHandlerContext(attr):
        return StateRouteHandlerContext.create(attr)

    """
      Invoked by this state's {@link #routeTriggered} method if the state is
      actually allowed to handle the triggered route. 
      
      By default the method invokes a state transition to this state.
    """
    def handleTriggeredRoute(self, context):
        self.gotoState(state=self, context=context)

    """ @private """
    def _addEmptyInitialSubstateIfNeeded(self):
        from kivy_statechart.system.empty_state import EmptyState

        if self.initialSubstateKey or self.substatesAreConcurrent:
            return None

        state = self.createSubstate(EmptyState)

        self.initialSubstateKey = state.name

        self.substates.append(state)

        setattr(self, state.name, state)

        state.initState()

        self.stateLogWarning("state {0} has no initial substate defined. Will default to using an empty state as initial substate".format(self))

        return state

    """ @private """
    def _addSubstate(self, name, state, attr):
        attr = dict.copy(attr) if attr else {}
        attr['name'] = name

        state = self.createSubstate(state, attr)

        self.substates.append(state)

        setattr(self, name, state)

        state.initState()

        return state

    """
      Used to dynamically add a substate to this state. Once added successfully you
      are then able to go to it from any other state within the owning statechart.
     
      A couple of notes when adding a substate:
      
      - If this state does not have any substates, then in addition to the 
        substate being added, an empty state will also be added and set as the 
        initial substate. To make the added substate the initial substate, set
        this object's initialSubstateKey property.
         
      - If this state is a current state, the added substate will not be entered. 
      
      - If this state is entered and its substates are concurrent, the added 
        substate will not be entered.  
     
      If this state is either entered or current and you'd like the added substate
      to take affect, you will need to explicitly reenter this state by calling
      its `reenter` method.
     
      Be aware that the name of the state you are adding must not conflict with
      the name of a property on this state or else you will get an error. 
      In addition, this state must be initialized to add substates.
    
      @param {String} name a unique name for the given substate.
      @param {State} state a class that derives from `State`
      @param {Hash} [attr] liternal to be applied to the substate
      @returns {State} an instance of the given state class
    """
    def addSubstate(self, name, state=None, attr={}):
        if not name: # [PORT] this used the empty(name) function.
            self.stateLogError("Can not add substate. name required")
            return None

        if hasattr(self, name):
            self.stateLogError("Can not add substate '{0}'. Already a defined property".format(name))
            return None

        if not self.stateIsInitialized:
            self.stateLogError("Can not add substate '{0}'. this state is not yet initialized".format(name))
            return None

        if state is None:
            state = State
        elif state is not None and isinstance(state, dict):
            attr = state
            state = State

        stateIsValid = inspect.isclass(state) and issubclass(state, State)

        if not stateIsValid:
            self.stateLogError("Can not add substate '{0}'. must provide a state class".format(name))
            return None

        state = self._addSubstate(name, state, attr)

        self._addEmptyInitialSubstateIfNeeded()

        # [PORT] Should there be a manual update call here?
        #self.dispatch('substates')
        #self.notifyPropertyChange("substates")

        return state

    """
      creates a substate for this state
    """
    def createSubstate(self, state, attr=None):
        attr = dict.copy(attr) if attr else {}
        attr['parentState'] = self
        attr['statechart'] = self.statechart
        return state(**attr)

    """ @private 
    
      Registers event handlers with this state. Event handlers are special
      functions on the state that are intended to handle more than one event. This
      compared to basic functions that only respond to a single event that reflects
      the name of the method.
    """
    def _registerEventHandler(self, name, handler):
        self._registeredEventHandlers[name] = handler

        for event in handler.events:
            if isinstance(event, basestring): # [PORT] checking for string and unicode -- need unicode? otherwise just str?
                self._registeredStringEventHandlers[event] = { 'name': name, 'handler': handler }
                continue

            if isinstance(event, REGEX_TYPE):
                self._registeredRegExpEventHandlers.append({ 'name': name, 'handler': handler, 'regexp': event })
                continue

            self.stateLogError("Invalid event {0} for event handler {1} in state {1}".format(event, name, self))

    """ @private 
    
      Registers state observe handlers with this state. State observe handlers behave just like
      when you apply observes() on a method but will only be active when the state is currently 
      entered, otherwise the handlers are inactive until the next time the state is entered
    """
    def _registerStateObserveHandler(self, name, handler):
        i = 0
        args = handler.args
        numberOfArgs = len(args)
        arg = None
        handlersAreValid = True

        while i < numberOfArgs:
            arg = args[i]
            if not isinstance(arg, basestring) or not arg: # [PORT] this used the empty(name) function.
                self.stateLogError("Invalid argument {0} for state observe handler {1} in state {2}".format(arg, name, self))
                handlersAreValid = False
            i += 1

        if not handlersAreValid:
            return

        self._registeredStateObserveHandlers[name] = handler.args

    """ @private
      Will traverse up through this state's parent states to register
      this state with them.
    """
    def _registerWithParentStates(self):
        parent = self.parentState
        
        while parent is not None:
            parent._registerSubstate(self)
            parent = parent.parentState

    """ @private
      Will register a given state as a substate of this state
    """
    def _registerSubstate(self, state):
        path = state.pathRelativeTo(self)

        if path is None:
            return

        self._registeredSubstates.append(state)

        # Keep track of states based on their relative path to this state. 
        if not state.name in self._registeredSubstatePaths:
            self._registeredSubstatePaths[state.name] = {}
        
        self._registeredSubstatePaths[state.name][path] = state

    """
      Will generate path for a given state that is relative to this state. It is
      required that the given state is a substate of this state.
      
      If the heirarchy of the given state to this state is the following:
      A > B > C, where A is this state and C is the given state, then the 
      relative path generated will be "B.C"
    """
    def pathRelativeTo(self, state):
        path = self.name
        parent = self.parentState

        #while parent is not None and parent is not state and state != type(self):
        while parent is not None and parent is not state:
            path = "{0}.{1}".format(parent.name, path)
            parent = parent.parentState

        if parent is not state and state is not type(self):
            self.stateLogError("Can not generate relative path from {0} since it not a parent state of {1}".format(state, self))
            return None

        return path

    """
      Used to get a substate of this state that matches a given value. 
      
      If the value is a state object, then the value will be returned if it is indeed 
      a substate of this state, otherwise null is returned. 
      
      If the given value is a string, then the string is assumed to be a path expression 
      to a substate. The value is then parsed to find the closes match. For path expression
      syntax, refer to the {@link StatePathMatcher} class.
      
      If there is no match then null is returned. If there is more than one match then null 
      is return and an error is generated indicating ambiguity of the given value. 
      
      An optional callback can be provided to handle the scenario when either no 
      substate is found or there is more than one match. The callback is then given
      the opportunity to further handle the outcome and return a result which the
      getSubstate method will then return. The callback should have the following
      signature:
      
        function(state, value, paths) 
        
      - state: The state getState was invoked on
      - value: The value supplied to getState 
      - paths: An array of substate paths that matched the given value
      
      If there were no matches then `paths` is not provided to the callback. 
      
      You can also optionally provide a target that the callback is invoked on. If no
      target is provided then this state is used as the target. 
      
      @param value {State|String} used to identify a substate of this state
      @param [callback] {Function} the callback
      @param [target] {Object} the target
    """
    def getSubstate(self, value, callback=None, target=None):
        if value is None:
            return None

        # If the value is an object then just check if the value is 
        # a registered substate of this state, and if so return it. 
        if not isinstance(value, basestring): # [PORT] if not a string, is an object
            return value if value in self._registeredSubstates else None

        if not isinstance(value, basestring):
            self.stateLogError("Can not find matching subtype. value must be a State class or string: {0}".format(value))
            return None
        
        # [PORT] Considered this, but it seemed to match on what should remain ambiguous.
        #for state in self._registeredSubstates:
            #if value == state.name:
                #return state

        # Not found yet, so look deeper for a nested substate.
        matcher = StatePathMatcher(state=self, expression=value)
        matches = []
        if len(matcher.tokens) == 0:
            return None

        # Grab the paths associated with this state name.
        paths = self._registeredSubstatePaths[matcher.lastPart] if matcher.lastPart in self._registeredSubstatePaths else None

        if paths is None:
            return self._notifySubstateNotFound(callback, target, value)

        for path in paths:
            if matcher.match(path):
                matches.append(paths[path])

        if len(matches) == 1:
            return self.getState(matches[0])

        if len(matches) > 1:
            matchedPaths = []
            for path in paths:
                # [PORT] Added this. Perhaps the matcher should return only the exact match, if it exists.
                #        This will catch substate A, when there are also substates X.A and B.Y.A. Otherwise,
                #        as apparently the way the javascript version works, there would be no match, because
                #        of that ambiguity. This way, state references must be explicit.
                if path == value: 
                    return self.getState(paths[path])
                matchedPaths.append(path)

            if callback is not None:
                return self._notifySubstateNotFound(callback, target, value, matchedPaths)

            msg = "Can not find substate matching '{0}' in state {1}. Ambiguous with the following: {2}"
            self.stateLogError(msg.format(value, self.fullPath, ', '.join(matchedPaths)))

        self._notifySubstateNotFound(callback, target, value)

    """ @private """
    def _notifySubstateNotFound(self, callback=None, target=None, value=None, keys=None):
        return callback(target or self, value, keys) if callback is not None else None

    """
      Will attempt to get a state relative to this state. 
      
      A state is returned based on the following:
      
      1. First check this state's substates for a match; and
      2. If no matching substate then attempt to get the state from
         this state's parent state.
         
      Therefore states are recursively traversed up to the root state
      to identify a match, and if found is ultimately returned, otherwise
      null is returned. In the case that the value supplied is ambiguous
      an error message is returned.
      
      The value provided can either be a state object or a state path expression.
      For path expression syntax, refer to the {@link StatePathMatcher} class.
    """
    def getState(self, value):
        if value == self.name or value == self: # [PORT] Added the second part. See get_state tests.
            return self

        # [PORT] This doesn't make sense. It is like a protection for a wrong call.
        if inspect.isclass(value) and issubclass(value, State):
            return value

        # [PORT] Added this call to self.statechart.getState, and the conditional following. The original
        #        javascript test only had the last line, but there is a difference in the way getState in
        #        state.py and in statechart.py work in the python port. Tests pass if this call is punted
        #        up to the statechart.
        state = self.statechart.getState(value)

        if state is not None:
            return state
        else:
            return self.getSubstate(value, self._handleSubstateNotFound)

    """ @private """
    def _handleSubstateNotFound(self, state, value, keys=None):
        parentState = self.parentState

        if parentState is not None:
            return parentState.getState(value)

        if keys is not None:
            msg = "Can not find state matching '{0}'. Ambiguous with the following: {1}"
            self.stateLogError(msg.format(value, ', '.join(keys)))

        return None

    """
      Used to go to a state in the statechart either directly from this state if it is a current state,
      or from the first relative current state from this state.
      
      If the value given is a string then it is considered a state path expression. The path is then
      used to find a state relative to this state based on rules of the {@link #getState} method.
      
      @param value {State|String} the state to go to
      @param [context] {Hash|Object} context object that will be supplied to all states that are
             exited and entered during the state transition process. Context can not be an instance of 
             State.
    """
    def gotoState(self, value, context=None):
        state = self.getState(value)

        if state is None:
            msg = "can not go to state {0} from state {1}. Invalid value."
            self.stateLogError(msg.format(value, self))
            return

        fromState = self.findFirstRelativeCurrentState(state)

        self.statechart.gotoState(state=state, fromCurrentState=fromState, useHistory=False, context=context)

    """
      Used to go to a given state's history state in the statechart either directly from this state if it
      is a current state or from one of this state's current substates. 
      
      If the value given is a string then it is considered a state path expression. The path is then
      used to find a state relative to this state based on rules of the {@link #getState} method.
      
      Method can be called in the following ways:
      
          // With one argument
          gotoHistoryState(<value>)
      
          // With two arguments
          gotoHistoryState(<value>, <boolean | hash>)
      
          // With three arguments
          gotoHistoryState(<value>, <boolean>, <hash>)
      
      Where <value> is either a string or a State object and <hash> is a regular JS hash object.
      
      @param value {State|String} the state whose history state to go to
      @param [recusive] {Boolean} indicates whether to follow history states recusively starting
             from the given state
      @param [context] {Hash|Object} context object that will be supplied to all states that are exited
             entered during the state transition process. Context can not be an instance of State.
    """
    def gotoHistoryState(self, value, recursive=None, context=None):
        state = self.getState(value)

        if state is None:
            msg = "can not go to history state {0} from state {1}. Invalid value."
            self.stateLogError(msg.format(value, self))
            return

        fromState = self.findFirstRelativeCurrentState(state)

        self.statechart.gotoHistoryState(state=state, fromCurrentState=fromState, recursive=recursive, context=context)

    """
      Resumes an active goto state transition process that has been suspended.
    """
    def resumeGotoState(self):
        self.statechart.resumeGotoState()

    """
      Used to check if a given state is a current substate of this state. Mainly used in cases
      when this state is a concurrent state.
      
      @param state {State|String} either a state object or the name of a state
      @returns {Boolean} true is the given state is a current substate, otherwise False is returned
    """
    def stateIsCurrentSubstate(self, state=None):
        stateObj = None
        if isinstance(state, basestring):
            stateObj = self.statechart.getState(state)
        else:
            stateObj = state

        if not stateObj:
            return False

        return True if stateObj in self.currentSubstates else False

    """
      Used to check if a given state is a current substate of this state. Mainly used in cases
      when this state is a concurrent state.
      
      @param state {State|String} either a state object or the name of a state
      @returns {Boolean} true is the given state is a current substate, otherwise False is returned
    """
    def stateIsEnteredSubstate(self, state=None):
        stateObj = None
        if isinstance(state, basestring):
            stateObj = self.statechart.getState(state)
        else:
            stateObj = state

        if not stateObj:
            return False

        return True if stateObj in self.enteredSubstates else False

    """
      Indicates if this state is the root state of the statechart.
      
      @property {Boolean}
    """
    def isRootState(self):
        return True if self.statechart.rootState is self else False

    """
      Indicates if this state is a current state of the statechart.
      
      @property {Boolean} 
    """
    def isCurrentState(self):
        return True if self.stateIsCurrentSubstate(self) else False

    """
      Indicates if this state is a concurrent state
      
      @property {Boolean}
    """
    def isConcurrentState(self):
        return True if self.parentState.substatesAreConcurrent else False

    """
      Indicates if this state is a currently entered state. 
      
      A state is currently entered if during a state transition process the
      state's enterState method was invoked, but only after its exitState method 
      was called, if at all.
    """
    def isEnteredState(self):
        return True if self.stateIsEnteredSubstate(self) else False

    """
      Will attempt to find a current state in the statechart that is relative to 
      this state. 
      
      Ordered set of rules to find a relative current state:
      
        1. If this state is a current state then it will be returned
        
        2. If this state has no current states and this state has a parent state then
          return parent state's first relative current state, otherwise return null
          
        3. If this state has more than one current state then use the given anchor state
           to get a corresponding substate that can be used to find a current state relative
           to the substate, if a substate was found. 
          
        4. If (3) did not find a relative current state then default to returning
           this state's first current substate. 
  
      @param anchor {State|String} Optional. a substate of this state used to help direct 
        finding a current state
      @return {State} a current state
    """
    def findFirstRelativeCurrentState(self, anchor=None):
        if self.isCurrentState():
            return self

        if not self.currentSubstates:
            return self.parentState.findFirstRelativeCurrentState() if self.parentState is not None else None

        if len(self.currentSubstates) > 1:
            anchor = self.getSubstate(anchor)
            if anchor is not None:
                return anchor.findFirstRelativeCurrentState()

        return self.currentSubstates[0]

    """
      Used to re-enter this state. Call this only when the state is a current state of
      the statechart.  
    """
    def reenter(self):
        if self.isEnteredState():
            # [PORT] Changed this from self to self.name, after str and key changes. Then, had
            #        to change it form self.gotoState to self.statechart.gotoState -- need to pin
            #        down that difference.
            self.statechart.gotoState(state=self.name)
        else:
            Logger.error("Can not re-enter state {0} since it is not an entered state in the statechart".format(self))

    """
      Called by the statechart to allow a state to try and handle the given event. If the
      event is handled by the state then YES is returned, otherwise NO.
      
      There is a particular order in how an event is handled by a state:
      
       1. Basic function whose name matches the event
       2. Registered event handler that is associated with an event represented as a string
       3. Registered event handler that is associated with events matching a regular expression
       4. The unknownEvent function
        
      Use of event handlers that are associated with events matching a regular expression may
      incur a performance hit, so they should be used sparingly.
      
      The unknownEvent function is only invoked if the state has it, otherwise it is skipped. Note that
      you should be careful when using unknownEvent since it can be either abused or cause unexpected
      behavior.
      
      Example of a state using all four event handling techniques:
      
          State.extend({
        
            // Basic function handling event 'foo'
            foo: function(arg1, arg2) { ... },
          
            // event handler that handles 'frozen' and 'canuck'
            eventHandlerA: function(event, arg1, arg2) {
              ...
            }.handleEvent('frozen', 'canuck'),
          
            // event handler that handles events matching the regular expression /num\d/
            //   ex. num1, num2
            eventHandlerB: function(event, arg1, arg2) {
              ...
            }.handleEvent(/num\d/),
          
            // Handle any event that was not handled by some other
            // method on the state
            unknownEvent: function(event, arg1, arg2) {
          
            }
        
          });
    """
    def tryToHandleEvent(self, event, arg1=None, arg2=None):
        trace = self.trace
        sc = self.statechart
        ret = None

        # First check if the name of the event is the same as a registered event handler. If so,
        # then do not handle the event.
        #
        # [PORT] So, this means that if you have a method called eventHandler1, you need to call the
        #        associated event event1, not eventHandler1. This is confusing. Methods in a state class
        #        are by definition event handlers, registerd by the method names. These are handled below.
        #        Special 'event handlers', capable of handling more than one event are the ones marked with the
        #        State.eventHandler([]) decorator. And then there are plain event handlers, treated by this
        #        conditional. What are they? There probably be better terminology to differentiate,
        #        e.g., registeredMethods vs. eventHandlers vs. multipleEventHanders, perhaps.
        #
        if event in self._registeredEventHandlers:
            self.stateLogWarning("state {0} can not handle event '{1}' since it is a registered event handler".format(self, event))
            return False

        if event in self._registeredStateObserveHandlers:
            self.stateLogWarning("state {0} can not handle event '{1}' since it is a registered state observe handler".format(self, event))
            return False

        # Now begin by trying a basic method on the state to respond to the event
        if hasattr(self, event) and inspect.ismethod(getattr(self, event)):
            if trace:
                self.stateLogTrace("will handle event '{0}'".format(event))

            sc.stateWillTryToHandleEvent(self, event, event)
            ret = getattr(self, event)(arg1, arg2) != False
            sc.stateDidTryToHandleEvent(self, event, event, ret)
            return ret

        # Try an event handler that is associated with an event represented as a string
        handler = self._registeredStringEventHandlers[event] if event in self._registeredStringEventHandlers else None
        if handler is not None:
            if trace:
                self.stateLogTrace("{0} will handle event '{1}'".format(handler['name'], event))

            sc.stateWillTryToHandleEvent(self, event, handler['name'])
            ret = handler['handler'](event, arg1, arg2) != False
            sc.stateDidTryToHandleEvent(self, event, handler['name'], ret)
            return ret

        # Try an event handler that is associated with events matching a regular expression
        numberOfHandlers = len(self._registeredRegExpEventHandlers)
        i = 0
        while i < numberOfHandlers:
            handler = self._registeredRegExpEventHandlers[i]
            if handler['regexp'].match(event):
                if trace:
                    self.stateLogTrace("{0} will handle event '{1}'".format(handler['name'], event))

                sc.stateWillTryToHandleEvent(self, event, handler['name'])
                ret = handler['handler'](event, arg1, arg2) != False
                sc.stateDidTryToHandleEvent(self, event, handler['name'], ret)
                return ret
            i += 1

        # Final attempt. If the state has an unknownEvent function then invoke it to 
        # handle the event
        if hasattr(self, 'unknownEvent') and inspect.ismethod(getattr(self, 'unknownEvent')):
            if trace:
                self.stateLogTrace("unknownEvent will handle event '{0}'".format(event))

            sc.stateWillTryToHandleEvent(self, event, "unknownEvent")
            ret = self.unknownEvent(event, arg1, arg2) != False
            sc.stateDidTryToHandleEvent(self, event, "unknownEvent", ret)
            return ret

        # Nothing was able to handle the given event for this state
        return False

    """
      Called whenever this state is to be entered during a state transition process. This 
      is useful when you want the state to perform some initial set up procedures. 
      
      If when entering the state you want to perform some kind of asynchronous action, such
      as an animation or fetching remote data, then you need to return an asynchronous 
      action, which is done like so:
      
          enterState: function() {
            return this.performAsync('foo');
          }
      
      After returning an action to be performed asynchronously, the statechart will suspend
      the active state transition process. In order to resume the process, you must call
      this state's resumeGotoState method or the statechart's resumeGotoState. If no asynchronous 
      action is to be perform, then nothing needs to be returned.
      
      When the enterState method is called, an optional context value may be supplied if
      one was provided to the gotoState method.
      
      In the case that the context being supplied is a state context object 
      ({@link StateRouteHandlerContext}), an optional `enterStateByRoute` method can be invoked
      on this state if the state has implemented the method. If `enterStateByRoute` is
      not part of this state then the `enterState` method will be invoked by default. The
      `enterStateByRoute` is simply a convenience method that helps removes checks to 
      determine if the context provide is a state route context object. 
      
      @param {Hash} [context] value if one was supplied to gotoState when invoked
      
      @see #representRoute
    """
    def enterState(self, context=None):
        pass

    """
      Notification called just before enterState is invoked. 
      
      Note: This is intended to be used by the owning statechart but it can be overridden if 
      you need to do something special.
      
      @param {Hash} [context] value if one was supplied to gotoState when invoked
      @see #enterState
    """
    def stateWillBecomeEntered(self, context=None):
        self._isEnteringState = True

    """
      Notification called just after enterState is invoked. 
      
      Note: This is intended to be used by the owning statechart but it can be overridden if 
      you need to do something special.
      
      @param context {Hash} Optional value if one was supplied to gotoState when invoked
      @see #enterState
    """
    def stateDidBecomeEntered(self, context=None):
        self._setupAllStateObserveHandlers()
        self._isEnteringState = False

    """
      Called whenever this state is to be exited during a state transition process. This is 
      useful when you want the state to peform some clean up procedures.
      
      If when exiting the state you want to perform some kind of asynchronous action, such
      as an animation or fetching remote data, then you need to return an asynchronous 
      action, which is done like so:
      
          exitState: function() {
            return this.performAsync('foo');
          }
      
      After returning an action to be performed asynchronously, the statechart will suspend
      the active state transition process. In order to resume the process, you must call
      this state's resumeGotoState method or the statechart's resumeGotoState. If no asynchronous 
      action is to be perform, then nothing needs to be returned.
      
      When the exitState method is called, an optional context value may be supplied if
      one was provided to the gotoState method.
      
      @param context {Hash} Optional value if one was supplied to gotoState when invoked
    """
    def exitState(self, context=None):
        pass

    """
      Notification called just before exitState is invoked. 
      
      Note: This is intended to be used by the owning statechart but it can be overridden 
      if you need to do something special.
      
      @param context {Hash} Optional value if one was supplied to gotoState when invoked
      @see #exitState
    """
    def stateWillBecomeExited(self, context=None):
        self._isExitingState = True
        self._teardownAllStateObserveHandlers()

    """
      Notification called just after exitState is invoked. 
      
      Note: This is intended to be used by the owning statechart but it can be overridden 
      if you need to do something special.
      
      @param context {Hash} Optional value if one was supplied to gotoState when invoked
      @see #exitState
    """
    def stateDidBecomeExited(self, context=None):
        self._isExitingState = False

    """ @private 
    
      Used to setup all the state observer handlers. Should be done when
      the state has been entered.
    """
    def _setupAllStateObserveHandlers(self):
        self._configureAllStateObserveHandlers("addObserver")

    """ @private 
    
      Used to teardown all the state observer handlers. Should be done when
      the state is being exited.
    """
    def _teardownAllStateObserveHandlers(self):
        self._configureAllStateObserveHandlers("removeObserver")

    """ @private 
    
      Primary method used to either add or remove this state as an observer
      based on all the state observe handlers that have been registered with
      this state.
      
      Note: The code to add and remove the state as an observer has been
      taken from the observerable mixin and made slightly more generic. However,
      having this code in two different places is not ideal, but for now this
      will have to do. In the future the code should be refactored so that
      there is one common function that both the observerable mixin and the 
      statechart framework use.  
    """
    def _configureAllStateObserveHandlers(self, action):
        values = []
        for key in self._registeredStateObserveHandlers:
            values = self._registeredStateObserveHandlers[key]

        i = 0
        while i < len(values):
            path = values[i]
            observer = key
            dotIndex = path.find(".")

            if dotIndex < 0:
                getattr(self, action)(path, self, observer)
            elif path.find("*") == 0:
                getattr(self, action)(path[1], self, observer)
            else:
                root = None
                if dotIndex == 0:
                    root = this
                    path = path[1]
                elif dotIndex == 4 and path[0, 5] == "self.":
                    root = self
                    path = path[5]
                elif dotIndex < 0 and len(path) == 4 and path == "self":
                    root = self
                    path = ""
                Observers[action](path, self, observer, root)
            i += 1

    """
      Call when an asynchronous action need to be performed when either entering or exiting
      a state.
      
      @see enterState
      @see exitState
    """
    def performAsync(self, func, arg1=None, arg2=None):
        return AsyncMixin().perform(func, arg1=arg1, arg2=arg2)

    """ @override
    
      Returns YES if this state can respond to the given event, otherwise
      NO is returned
    
      @param event {String} the value to check
      @returns {Boolean}
    """
    def respondsToEvent(self, event):
        if event in self._registeredEventHandlers:
            return False
        if hasattr(self, event) and inspect.ismethod(getattr(self, event)):
            return True
        if event in self._registeredStringEventHandlers:
            return True
        if event in self._registeredStateObserveHandlers:
            return False

        for handler in self._registeredRegExpEventHandlers:
            if handler['regexp'].match(event):
                return True

        return hasattr(self, 'unknownEvent') and inspect.ismethod(getattr(self, 'unknownEvent'))

    """
      Returns the path for this state relative to the statechart's
      root state. 
      
      The path is a dot-notation string representing the path from
      this state to the statechart's root state, but without including
      the root state in the path. For instance, if the name of this
      state if "foo" and the parent state's name is "bar" where bar's
      parent state is the root state, then the full path is "Bar.foo"
    
      @property {String}
    """
    def _fullPath(self, *l): # [PORT] Added *l
        root = self.statechart.rootState if self.statechart else None
        if root is None:
            self.fullPath = self.name
        else:
            self.fullPath = self.pathRelativeTo(root)

    def toString(self):
        return self.fullPath

    """ @private """
    def _enteredSubstatesDidChange(self, *l):
        #self.notifyPropertyChange("enteredSubstates")
        pass

    """ @private """
    def _currentSubstatesDidChange(self, *l):
        #self.notifyPropertyChange("currentSubstates")
        pass

    """ @private """
    def _statechartTraceDidChange(self, *l):
        #self.notifyPropertyChange("trace")
        pass

    """ @private """
    def _statechartOwnerDidChange(self, *l):
        #self.notifyPropertyChange("owner")
        pass

    """ 
      Used to log a state trace message
    """
    def stateLogTrace(self, msg):
        self.statechart.statechartLogTrace("{0}: {1}".format(self, msg))

    """ 
      Used to log a state warning message
    """
    def stateLogWarning(self, msg):
        self.statechart.statechartLogWarning(msg)

    """ 
      Used to log a state error message
    """
    def stateLogError(self, msg):
        sc = self.statechart
        sc.statechartLogError(msg)

    # [PORT] plugin() method removed in python version.

    @classmethod
    def eventHandler(self, events):
        def eventHandlerDecorator(fn):
            fn.isEventHandler = True
            fn.events = events
            return fn
        return eventHandlerDecorator

    #def eventHandler(events):
        #def eventHandlerDecorator(self, *args, **kwargs):
            #fn.isEventHandler = True
            #fn.events = events
            #return fn
        #return eventHandlerDecorator(self, *args, **kwargs)

