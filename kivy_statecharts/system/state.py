# Project:   Kivy.Statechart - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

from kivy.event import EventDispatcher
from kivy_statecharts.private.state_path_matcher import StatePathMatcher
from kivy_statecharts.system.async import AsyncMixin
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

    # [PORT] Adding owner_key as property
    #
    owner_key = StringProperty(None)

    # [PORT] Adding trace_key as property
    #
    trace_key = StringProperty(None)

    """
      Returns the statechart's assigned delegate. A statechart delegate is one
      that adheres to the {@link StatechartDelegate} mixin. 
        
      @property {Object}
          
      @see StatechartDelegate
    """
    statechart_delegate = ObjectProperty(None)

    """
      A volatile property used to get and set the app's current location. 
          
      This computed property defers to the the statechart's delegate to 
      actually update and acquire the app's location.
          
      Note: Binding for this pariticular case is discouraged since in most
      cases we need the location value immediately. If we were to use
      bindings then the location value wouldn't be updated until at least
      the end of one run loop. It is also advised that the delegate not
      have its `statechart_update_location_for_state` and
      `statechart_acquire_location_for_state` methods implemented where bindings
      are used since they will inadvertenly stall the location value from
      propogating immediately.
          
      @property {String}
          
      @see StatechartDelegate#statechart_update_location_for_state
      @see StatechartDelegate#statechart_acquire_location_for_state
    """
    location = StringProperty(None) # [TODO] marked as idempotent in js

    full_path = StringProperty(None)

    """
      The name of the state
          
      @property {String}
    """
    name = StringProperty(None)

    """
      This state's parent state. Managed by the statechart
   
      @property {State}
    """
    parent_state = ObjectProperty(None)

    """
      This state's history state. Can be null. Managed by the statechart.
          
      @property {State}
    """
    history_state = ObjectProperty(None, allownone=True)

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
    initial_substate_key = StringProperty('')

    initial_substate_object = ObjectProperty(None)

    """
      Used to indicates if this state's immediate substates are to be
      concurrent (orthogonal) to each other. 
      
      @property {Boolean}
    """
    substates_are_concurrent = BooleanProperty(False)

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
    state_is_initialized = BooleanProperty(False)

    """
      An array of this state's current substates. Managed by the statechart
      
      @propety {Array}
    """
    current_substates = ListProperty([])

    """ 
      An array of this state's substates that are currently entered. Managed by
      the statechart.
      
      @property {Array}
    """
    entered_substates = ListProperty([])

    """
      Can optionally assign what route this state is to represent. 
      
      If assigned then this state will be notified to handle the route when triggered
      any time the app's location changes and matches this state's assigned route. 
      The handler invoked is this state's {@link #route_triggered} method. 
      
      The value assigned to this property is dependent on the underlying routing 
      mechanism used by the application. The default routing mechanism is to use 
      routes.
      
      @property {String|Hash}
      
      @see #route_triggered
      @see #location
      @see StatechartDelegate
    """
    represented_route = StringProperty(None)

    #is_root_state = BooleanProperty(False)
    #is_current_state = BooleanProperty(False)
    #is_concurrent_state = BooleanProperty(False)
    #is_entered_state = BooleanProperty(False)
    #hasCurrentSubstates = BooleanProperty(False)
    #hasEnteredSubstates = BooleanProperty(False)

    def __init__(self, **kwargs):
        #self.bind(current_substates=self._is_current_state)
        #self.bind(entered_substates=self._is_entered_state)
        #self.bind(current_substates=self._hasCurrentSubstates)
        #self.bind(entered_substates=self._hasEnteredSubstates)
        #self.bind(entered_substates=self._entered_substates_did_change) # [PORT] .observes("*entered_substates.[]")
        #self.bind(current_substates=self._current_substates_did_change) # [PORT] .observes("*current_substates.[]")

        self.bind(name=self._full_path)
        self.bind(parent_state=self._full_path)
        #self.bind(parent_state=self._is_concurrent_state) # [PORT] Why is this commented out?

        self.bind(statechart=self._trace)
        self.bind(statechart=self._owner)
        self.bind(statechart=self._statechart_delegate)
        self.bind(statechart_delegate=self._location)

        self._registered_event_handlers = {}
        self._registered_string_event_handlers = {}
        self._registered_reg_exp_event_handlers = []
        self._registered_state_observe_handlers = {}
        self._registered_substate_paths = {}
        self._registered_substates = []
        self._is_entering_state = False
        self._is_exiting_state = False
        
        # [PORT] Not sure: ...

        # Setting up observes this way is faster then using .observes,
        # which adds a noticable increase in initialization time.
    
        sc = self.statechart
    
        self.owner_key = sc.statechart_owner_key if sc else None
        self.trace_key = sc.statechart_owner_key if sc else None
    
        if sc is not None:
            self.bind(owner_key=self._statechart_owner_did_change) # [PORT] Changed to bind to self, to try to do it from here...
            self.bind(trace_key=self._statechart_trace_did_change)

        for k,v in kwargs.items():
            if k == 'initial_substate_key':
                # [PORT] Force initial_substate_key to always be string.
                if isinstance(v, basestring):
                    self.initial_substate_key = v
                else:
                    name = v.name if hasattr(v, 'name') else None
                    if not name:
                        name = v.__name__ if hasattr(v, '__name__') else None
                    self.initial_substate_key = name if name else None
            else:
                setattr(self, k, v)

        super(State, self).__init__() # [PORT] initialize how? We have also init_state()

    def _trace(self, *l):
        key = self.statechart.statechart_trace_key
        self.trace = getattr(self.statechart, key) if hasattr(self.statechart, key) else None

    def _owner(self, *l):
        sc = self.statechart
        key = sc.statechart_owner_key if sc else None
        owner = getattr(sc, key) if sc else None
        self.owner = owner if owner else sc

    def statechart_owner_did_change(self):
        self._owner()

        for substate in self.substates:
            substate.statechart_owner_did_change()

    def _statechart_delegate(self, *l):
        self.statechart_delegate = self.statechart.statechart_delegate

    def _location(self, instance, value, *l):
        sc = self.statechart
        delegate = self.statechart_delegate
        delegate.statechart_update_location_for_state(sc, value, self if value else None)
        self.location = delegate.statechart_acquire_location_for_state(sc, self)
        
    def destroy(self):
        sc = self.statechart

        self.owner_key = sc.statechart_owner_key if sc else None
        self.trace_key = sc.statechart_owner_key if sc else None
    
        if sc is not None:
            self.unbind(owner_key=self._statechart_owner_did_change)
            self.unbind(trace_key=self._statechart_trace_did_change)

        substates = self.substates
    
        if substates is not None:
            for state in substates:
                state.destroy()
    
        self._teardown_all_state_observe_handlers()
    
        self.substates = None
        self.current_substates = None
        self.entered_substates = None
        self.parent_state = None
        self.history_state = None
        self.initial_substate_key = ''
        self.statechart = None
    
        #self.notifyPropertyChange("trace") # [PORT] Use kivy's dispatch?
        #self.notifyPropertyChange("owner")
    
        self._registered_event_handlers = None
        self._registered_string_event_handlers = None
        self._registered_reg_exp_event_handlers = None
        self._registered_state_observe_handlers = None
        self._registered_substate_paths = None
        self._registered_substates = None
    
        #sc_super()

    """
      Used to initialize this state. To only be called by the owning statechart.
    """
    def init_state(self):
        if self.state_is_initialized:
            return  
    
        self._register_with_parent_states()
        self._setup_route_handling()
    
        substates = []
        matched_initial_substate = False
        value_is_method = False
        history_state = None
    
        self.substates = substates
    
        if hasattr(self, 'InitialSubstate'):
            initial_substate_class = getattr(self, 'InitialSubstate')
            from kivy_statecharts.system.history_state import HistoryState
            if initial_substate_class is not None:
                if issubclass(initial_substate_class, HistoryState):
                    history_state = self.create_substate(initial_substate_class)
              
                    if not history_state.default_state:
                        self.state_log_error("Initial substate is invalid. History state requires the name of a default state to be set")
                        self.initial_substate_key = ''
                        history_state = None
                    else:
                        setattr(self, 'initial_substate_key', history_state.default_state)
    
        # Iterate through all this state's substates, if any, create them, and then initialize
        # them. This causes a recursive process.
        for key in dir(self):
            if key == '__class__':
                continue

            value = getattr(self, key)
            if not inspect.ismethod(value) and not inspect.isclass(value):
                continue

            value_is_method = inspect.ismethod(value)
      
            if value_is_method and hasattr(value, 'is_event_handler') and value.is_event_handler == True:
                self._register_event_handler(key, value)
                continue

            if value_is_method and hasattr(value, 'is_state_observe_handler') and value.is_state_observe_handler == True:
                self._register_state_observe_handler(key, value)
                continue

            # [PORT] Removed statePlugin system. Use import in python.

            #if inspect.isclass(value) and issubclass(value, State) and getattr(self, key) is not self.__init__: # [PORT] using inspect
            if inspect.isclass(value) and issubclass(value, State):
                state = self._add_substate(key, value, None)
                # [PORT] Added clarification in this condition to distinguish between the normal case of
                #        having a simple initial_substate_key defined, vs. the use of a HistoryState as the
                #        initial_substate.
                if key == self.initial_substate_key and history_state is None:
                    self.initial_substate_key = state if isinstance(state, basestring) else state.name # [PORT] Needs to always be a string.
                    self.initial_substate_object = state
                    matched_initial_substate = True
                elif history_state and history_state.default_state == key:
                    # [PORT] No need to do this in python version, because default_state is a key; We do not reset
                    #        default_state to be a state object -- we rely on get_substate to find it by the key
                    #        when it is accessed. default_state has already been set (See check above).
                    #history_state.default_state = state if isinstance(state, basestring) else state.name # [PORT] Needs to always be a string.
                    matched_initial_substate = True

        if self.initial_substate_key and not matched_initial_substate:
            msg = "Unable to set initial substate {0} since it did not match any of state {1}'s substates"
            self.state_log_error(msg.format(self.initial_substate_key, self))

        if len(self.substates) == 0:
            if self.initial_substate_key:
                msg = "Unable to make {0} an initial substate since state {1} has no substates"
                self.state_log_warning(msg.format(self.initial_substate_key, self))
        elif len(self.substates) > 0:
              state = self._add_empty_initial_substate_if_needed()
              if state is None and self.initial_substate_key and self.substates_are_concurrent:
                    self.initial_substate_key = ''
                    msg = "Can not use {0} as initial substate since substates are all concurrent for state {1}"
                    self.state_log_warning(msg.format(self.initial_substate_key, self))

        #self.notifyPropertyChange("substates")
        # [PORT] substates have changed. Call _current_states on statechart, which is bound to root_state_instance,
        #        and updates self.current_states = self.root_state_instance.substates. That binding won't fire if 
        #        root_state_instance.substates changes, so we manually call it in kivy.
        self.statechart._current_states()

        self.current_substates = []
        self.entered_substates = []
        self.state_is_initialized = True

    """ @private 
    
      Used to bind this state with a route this state is to represent if a route has been assigned.
      
      When invoked, the method will delegate the actual binding strategy to the statechart delegate 
      via the delegate's {@link StatechartDelegate#statechart_bind_state_to_route} method.
      
      Note that a state cannot be bound to a route if this state is a concurrent state.
      
      @see #represented_route
      @see StatechartDelegate#statechart_bind_state_to_route
    """
    def _setup_route_handling(self):
        route = self.represented_route
        sc = self.statechart
        delegate = self.statechart_delegate

        if route is None:
            return
    
        if self.is_concurrent_state():
            self.state_log_error("State {0} cannot handle route '{1}' since state is concurrent".format(self, route))
            return
    
        delegate.statechart_bind_state_to_route(sc, self, route, self.route_triggered)

    """
      Main handler that gets triggered whenever the app's location matches this state's assigned
      route. 
      
      When invoked the handler will first refer to the statechart delegate to determine if it
      should actually handle the route via the delegate's 
      {@see StatechartDelegate#statechart_should_state_handle_triggered_route} method. If the 
      delegate allows the handling of the route then the state will continue on with handling
      the triggered route by calling the state's {@link #handle_triggered_route} method, otherwise 
      the state will cancel the handling and inform the delegate through the delegate's 
      {@see StatechartDelegate#statechartStateCancelledHandlingRoute} method.
      
      The handler will create a state route context ({@link StateRouteContext}) object 
      that packages information about what is being currently handled. This context object gets 
      passed along to the delegate's invoked methods as well as the state transition process. 
      
      Note that this method is not intended to be directly called or overridden.
      
      @see #represented_route
      @see StatechartDelegate#statechartShouldStateHandleRoute
      @see StatechartDelegate#statechartStateCancelledHandlingRoute
      @see #create_state_route_handler_context
      @see #handle_triggered_route
    """
    def route_triggered(self, params):
        if self._is_entering_state:
            return

        sc = self.statechart
        delegate = self.statechart_delegate
        loc = self.location
    
        attr = {
            'state': self,
            'location': loc,
            'params': params,
            'handler': self.route_triggered
        }

        context = self.create_state_route_handler_context(attr)

        if delegate.statechart_should_state_handle_triggered_route(sc, self, context):
            if self.trace and loc:
                self.state_log_trace("will handle route '{0}'".format(loc))
            self.handle_triggered_route(context)
        else:
            delegate.statechart_state_cancelled_handling_triggered_route(sc, self, context)

    """
      Constructs a new instance of a state routing context object.
      
      @param {Hash} attr attributes to apply to the constructed object
      @return {StateRouteContext}
      
      @see #handleRoute
    """
    def create_state_route_handler_context(attr):
        return StateRouteHandlerContext.create(attr)

    """
      Invoked by this state's {@link #route_triggered} method if the state is
      actually allowed to handle the triggered route. 
      
      By default the method invokes a state transition to this state.
    """
    def handle_triggered_route(self, context):
        self.go_to_state(state=self, context=context)

    """ @private """
    def _add_empty_initial_substate_if_needed(self):
        from kivy_statecharts.system.empty_state import EmptyState

        if self.initial_substate_key or self.substates_are_concurrent:
            return None

        state = self.create_substate(EmptyState)

        self.initial_substate_key = state.name if state.name else state.__class__.__name__

        self.substates.append(state)

        setattr(self, state.name, state)

        self.initial_substate_object = state

        state.init_state()

        self.state_log_warning("state {0} has no initial substate defined. Will default to using an empty state as initial substate".format(self))

        return state

    """ @private """
    def _add_substate(self, name, state, attr):
        attr = dict.copy(attr) if attr else {}
        attr['name'] = name

        state = self.create_substate(state, attr)

        self.substates.append(state)

        setattr(self, name, state)

        state.init_state()

        return state

    """
      Used to dynamically add a substate to this state. Once added successfully you
      are then able to go to it from any other state within the owning statechart.
     
      A couple of notes when adding a substate:
      
      - If this state does not have any substates, then in addition to the 
        substate being added, an empty state will also be added and set as the 
        initial substate. To make the added substate the initial substate, set
        this object's initial_substate_key property.
         
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
    def add_substate(self, name, state=None, attr={}):
        if not name: # [PORT] this used the empty(name) function.
            self.state_log_error("Can not add substate. name required")
            return None

        if hasattr(self, name):
            self.state_log_error("Can not add substate '{0}'. Already a defined property".format(name))
            return None

        if not self.state_is_initialized:
            self.state_log_error("Can not add substate '{0}'. this state is not yet initialized".format(name))
            return None

        if state is None:
            state = State
        elif state is not None and isinstance(state, dict):
            attr = state
            state = State

        state_is_valid = inspect.isclass(state) and issubclass(state, State)

        if not state_is_valid:
            self.state_log_error("Can not add substate '{0}'. must provide a state class".format(name))
            return None

        state = self._add_substate(name, state, attr)

        self._add_empty_initial_substate_if_needed()

        # [PORT] Should there be a manual update call here?
        #self.dispatch('substates')
        #self.notifyPropertyChange("substates")

        return state

    """
      creates a substate for this state
    """
    def create_substate(self, state, attr=None):
        attr = dict.copy(attr) if attr else {}
        attr['parent_state'] = self
        attr['statechart'] = self.statechart
        return state(**attr)

    """ @private 
    
      Registers event handlers with this state. Event handlers are special
      functions on the state that are intended to handle more than one event. This
      compared to basic functions that only respond to a single event that reflects
      the name of the method.
    """
    def _register_event_handler(self, name, handler):
        self._registered_event_handlers[name] = handler

        for event in handler.events:
            if isinstance(event, basestring): # [PORT] checking for string and unicode -- need unicode? otherwise just str?
                self._registered_string_event_handlers[event] = { 'name': name, 'handler': handler }
                continue

            if isinstance(event, REGEX_TYPE):
                self._registered_reg_exp_event_handlers.append({ 'name': name, 'handler': handler, 'regexp': event })
                continue

            self.state_log_error("Invalid event {0} for event handler {1} in state {1}".format(event, name, self))

    """ @private 
    
      Registers state observe handlers with this state. State observe handlers behave just like
      when you apply observes() on a method but will only be active when the state is currently 
      entered, otherwise the handlers are inactive until the next time the state is entered
    """
    def _register_state_observe_handler(self, name, handler):
        i = 0
        args = handler.args
        number_of_args = len(args)
        arg = None
        handlers_are_valid = True

        while i < number_of_args:
            arg = args[i]
            if not isinstance(arg, basestring) or not arg: # [PORT] this used the empty(name) function.
                self.state_log_error("Invalid argument {0} for state observe handler {1} in state {2}".format(arg, name, self))
                handlers_are_valid = False
            i += 1

        if not handlers_are_valid:
            return

        self._registered_state_observe_handlers[name] = handler.args

    """ @private
      Will traverse up through this state's parent states to register
      this state with them.
    """
    def _register_with_parent_states(self):
        parent = self.parent_state
        
        while parent is not None:
            parent._register_substate(self)
            parent = parent.parent_state

    """ @private
      Will register a given state as a substate of this state
    """
    def _register_substate(self, state):
        path = state.path_relative_to(self)

        if path is None:
            return

        self._registered_substates.append(state)

        # Keep track of states based on their relative path to this state. 
        if not state.name in self._registered_substate_paths:
            self._registered_substate_paths[state.name] = {}
        
        self._registered_substate_paths[state.name][path] = state

    """
      Will generate path for a given state that is relative to this state. It is
      required that the given state is a substate of this state.
      
      If the heirarchy of the given state to this state is the following:
      A > B > C, where A is this state and C is the given state, then the 
      relative path generated will be "B.C"
    """
#    pathRelativeTo: function(state) {
#      var path = this.get('name'),
#          parent = this.get('parentState');
#
#      while (!SC.none(parent) && parent !== state) {
#        path = "%@.%@".fmt(parent.get('name'), path);
#        parent = parent.get('parentState');
#      }
#
#      if (parent !== state && state !== this) {
#        this.stateLogError('Can not generate relative path from %@ since it not a parent state of %@'.fmt(state, this));
#        return null;
#      }
#
#      return path;
#    },

    def path_relative_to(self, state):
        path = self.name
        parent = self.parent_state

        # [PORT] Bindings related problem. In the original SC, _fullPath is a
        # computed property updated when name or parent changes. Here,
        # path_relative_to() is called when the name initially changes, at
        # which time the parent_state has not yet been set, and then just
        # after is another call when the parent_state changes (See the binding
        # setup in __init__.py). So, for now, just return the path to avoid
        # the log message below.
        if parent is None:
            return path

        #while parent is not None and parent is not state and state != type(self):
        #while parent is not None and parent is not state:
        # [PORT] != versions, here and in the if below, seem to be correct,
        # because the check is against instances.
        while parent and parent != state:
            path = "{0}.{1}".format(parent.name, path)
            parent = parent.parent_state

        #if parent is not state and state is not self:
        #if parent is not state and state is not type(self):
        if parent != state and state != self:
            self.state_log_error("Can not generate relative path from {0} since it not a parent state of {1} ({2})".format(state, self, path))
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
      get_substate method will then return. The callback should have the following
      signature:
      
        function(state, value, paths) 
        
      - state: The state get_state was invoked on
      - value: The value supplied to get_state 
      - paths: An array of substate paths that matched the given value
      
      If there were no matches then `paths` is not provided to the callback. 
      
      You can also optionally provide a target that the callback is invoked on. If no
      target is provided then this state is used as the target. 
      
      @param value {State|String} used to identify a substate of this state
      @param [callback] {Function} the callback
      @param [target] {Object} the target
    """
    def get_substate(self, value, callback=None, target=None):
        if value is None:
            return None

        # If the value is an object then just check if the value is 
        # a registered substate of this state, and if so return it. 
        if not isinstance(value, basestring): # [PORT] if not a string, is an object
            return value if value in self._registered_substates else None

        if not isinstance(value, basestring):
            self.state_log_error("Can not find matching subtype. value must be a State class or string: {0}".format(value))
            return None
        
        # [PORT] In python API for history states, the history state must be called InitialSubstate.
        #        We need an explicit check for it here, otherwise the path matcher might fail if there
        #        are other substates with history states (multiple matches on 'InitialSubstate').
        if value == 'InitialSubstate' and hasattr(self, 'InitialSubstate'):
            return getattr(self, 'InitialSubstate')

        # [PORT] Considered this, but it seemed to match on what should remain ambiguous.
        #for state in self._registered_substates:
            #if value == state.name:
                #return state

        # Not found yet, so keep looking with path matcher.
        matcher = StatePathMatcher(state=self, expression=value)

        matches = []

        if len(matcher.tokens) == 0:
            return None

        # Grab the paths associated with this state name.
        paths = self._registered_substate_paths[matcher.last_part] if matcher.last_part in self._registered_substate_paths else None

        if paths is None:
            return self._notify_substate_not_found(callback=callback, target=target, value=value)

        if value in paths:
            matches.append(paths[value])
        else:
            for path in paths:
                if matcher.match(path):
                    matches.append(paths[path])

        if len(matches) == 1:
            return matches[0]

        if len(matches) > 1:
            path_keys = []
            for key in paths:
                # [PORT] Added this. Perhaps the matcher should return only the exact match, if it exists.
                #        This will catch substate A, when there are also substates X.A and B.Y.A. Otherwise,
                #        as apparently the way the javascript version works, there would be no match, because
                #        of that ambiguity. This way, state references must be explicit.
                #if path == value: 
                #    return self.get_state(paths[path])
                path_keys.append(key)

            if callback is not None:
                return self._notify_substate_not_found(callback=callback, target=target, value=value, keys=path_keys)

            msg = "Can not find substate matching '{0}' in state {1}. Ambiguous with the following: {2}"
            self.state_log_error(msg.format(value, self.full_path, ', '.join(path_keys)))

        return self._notify_substate_not_found(callback=callback, target=target, value=value)

    """ @private """
    def _notify_substate_not_found(self, callback=None, target=None, value=None, keys=None):
        if callback:
            if target and hasattr(target, callback.__name__):
                return getattr(target, callback.__name__)(self, value, keys)
            elif hasattr(self, callback.__name__):
                return getattr(self, callback.__name__)(self, value, keys)
            else:
                return callback(self, value, keys)
        else:
            return None

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
    def get_state(self, value):
        if value == self.name or value == self: # [PORT] Added the second part. See get_state tests.
            return self

        # [PORT] This doesn't make sense. It is like a protection for a wrong call.
        #
        if isinstance(value, State):
            return value

        return self.get_substate(value, self._handle_substate_not_found)

    """ @private """
    def _handle_substate_not_found(self, state, value, keys=None):
        parent_state = self.parent_state

        if parent_state is not None:
            return parent_state.get_state(value)

        if keys is not None:
            msg = "Can not find state matching '{0}'. Ambiguous with the following: {1}"
            self.state_log_error(msg.format(value, ', '.join(keys)))

        return None

    """
      Used to go to a state in the statechart either directly from this state if it is a current state,
      or from the first relative current state from this state.
      
      If the value given is a string then it is considered a state path expression. The path is then
      used to find a state relative to this state based on rules of the {@link #get_state} method.
      
      @param value {State|String} the state to go to
      @param [context] {Hash|Object} context object that will be supplied to all states that are
             exited and entered during the state transition process. Context can not be an instance of 
             State.
    """
    def go_to_state(self, value, context=None):
        state = self.get_state(value)

        if state is None:
            msg = "can not go to state {0} from state {1}. Invalid value."
            self.state_log_error(msg.format(value, self))
            return

        fromState = self.find_first_relative_current_state(state)

        self.statechart.go_to_state(state=state, from_current_state=fromState, use_history=False, context=context)

    """
      Used to go to a given state's history state in the statechart either directly from this state if it
      is a current state or from one of this state's current substates. 
      
      If the value given is a string then it is considered a state path expression. The path is then
      used to find a state relative to this state based on rules of the {@link #get_state} method.
      
      Method can be called in the following ways:
      
          // With one argument
          go_to_history_state(<value>)
      
          // With two arguments
          go_to_history_state(<value>, <boolean | hash>)
      
          // With three arguments
          go_to_history_state(<value>, <boolean>, <hash>)
      
      Where <value> is either a string or a State object and <hash> is a regular JS hash object.
      
      @param value {State|String} the state whose history state to go to
      @param [recusive] {Boolean} indicates whether to follow history states recusively starting
             from the given state
      @param [context] {Hash|Object} context object that will be supplied to all states that are exited
             entered during the state transition process. Context can not be an instance of State.
    """
    def go_to_history_state(self, value, recursive=None, context=None):
        state = self.get_state(value)

        if state is None:
            msg = "can not go to history state {0} from state {1}. Invalid value."
            self.state_log_error(msg.format(value, self))
            return

        fromState = self.find_first_relative_current_state(state)

        self.statechart.go_to_history_state(state=state, from_current_state=fromState, recursive=recursive, context=context)

    """
      Resumes an active goto state transition process that has been suspended.
    """
    def resume_go_to_state(self):
        self.statechart.resume_go_to_state()

    """
      Used to check if a given state is a current substate of this state. Mainly used in cases
      when this state is a concurrent state.
      
      @param state {State|String} either a state object or the name of a state
      @returns {Boolean} true is the given state is a current substate, otherwise False is returned
    """
    def state_is_current_substate(self, state=None):
        state_obj = None
        if isinstance(state, basestring):
            state_obj = self.statechart.get_state(state)
        else:
            state_obj = state

        if not state_obj:
            return False

        return True if state_obj in self.current_substates else False

    """
      Used to check if a given state is a current substate of this state. Mainly used in cases
      when this state is a concurrent state.
      
      @param state {State|String} either a state object or the name of a state
      @returns {Boolean} true is the given state is a current substate, otherwise False is returned
    """
    def state_is_entered_substate(self, state=None):
        state_obj = None
        if isinstance(state, basestring):
            state_obj = self.statechart.get_state(state)
        else:
            state_obj = state

        if not state_obj:
            return False

        return True if state_obj in self.entered_substates else False

    """
      Indicates if this state is the root state of the statechart.
      
      @property {Boolean}
    """
    def is_root_state(self):
        return True if self.statechart.root_state_instance is self else False

    """
      Indicates if this state is a current state of the statechart.
      
      @property {Boolean} 
    """
    def is_current_state(self):
        return True if self.state_is_current_substate(self) else False

    """
      Indicates if this state is a concurrent state
      
      @property {Boolean}
    """
    def is_concurrent_state(self):
        return True if self.parent_state.substates_are_concurrent else False

    """
      Indicates if this state is a currently entered state. 
      
      A state is currently entered if during a state transition process the
      state's enter_state method was invoked, but only after its exit_state method 
      was called, if at all.
    """
    def is_entered_state(self):
        return True if self.state_is_entered_substate(self) else False

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
    def find_first_relative_current_state(self, anchor=None):
        if self.is_current_state():
            return self

        if not self.current_substates:
            return self.parent_state.find_first_relative_current_state() if self.parent_state is not None else None

        if len(self.current_substates) > 1:
            anchor = self.get_substate(anchor)
            if anchor is not None:
                return anchor.find_first_relative_current_state()

        return self.current_substates[0]

    """
      Used to re-enter this state. Call this only when the state is a current state of
      the statechart.  
    """
    def reenter(self):
        if self.is_entered_state():
            # [PORT] Changed this from self to self.name, after str and key changes. Then, had
            #        to change it form self.go_to_state to self.statechart.go_to_state -- need to pin
            #        down that difference.
            self.statechart.go_to_state(state=self.name)
        else:
            Logger.error("Can not re-enter state {0} since it is not an entered state in the statechart".format(self))

    """
      Called by the statechart to allow a state to try and handle the given event. If the
      event is handled by the state then YES is returned, otherwise NO.
      
      There is a particular order in how an event is handled by a state:
      
       1. Basic function whose name matches the event
       2. Registered event handler that is associated with an event represented as a string
       3. Registered event handler that is associated with events matching a regular expression
       4. The unknown_event function
        
      Use of event handlers that are associated with events matching a regular expression may
      incur a performance hit, so they should be used sparingly.
      
      The unknown_event function is only invoked if the state has it, otherwise it is skipped. Note that
      you should be careful when using unknown_event since it can be either abused or cause unexpected
      behavior.
      
      Example of a state using all four event handling techniques:
      
          State.extend({
        
            // Basic function handling event 'foo'
            foo: function(arg1, arg2) { ... },
          
            // event handler that handles 'frozen' and 'canuck'
            event_handlerA: function(event, arg1, arg2) {
              ...
            }.handle_event('frozen', 'canuck'),
          
            // event handler that handles events matching the regular expression /num\d/
            //   ex. num1, num2
            event_handlerB: function(event, arg1, arg2) {
              ...
            }.handle_event(/num\d/),
          
            // Handle any event that was not handled by some other
            // method on the state
            unknown_event: function(event, arg1, arg2) {
          
            }
        
          });
    """
    def try_to_handle_event(self, event, arg1=None, arg2=None):
        trace = self.trace
        sc = self.statechart
        ret = None

        # First check if the name of the event is the same as a registered event handler. If so,
        # then do not handle the event.
        #
        # [PORT] So, this means that if you have a method called event_handler1, you need to call the
        #        associated event event1, not event_handler1. This is confusing. Methods in a state class
        #        are by definition event handlers, registerd by the method names. These are handled below.
        #        Special 'event handlers', capable of handling more than one event are the ones marked with the
        #        State.event_handler([]) decorator. And then there are plain event handlers, treated by this
        #        conditional. What are they? There probably be better terminology to differentiate,
        #        e.g., registeredMethods vs. event_handlers vs. multipleEventHanders, perhaps.
        #
        if event in self._registered_event_handlers:
            self.state_log_warning("state {0} can not handle event '{1}' since it is a registered event handler".format(self, event))
            return False

        if event in self._registered_state_observe_handlers:
            self.state_log_warning("state {0} can not handle event '{1}' since it is a registered state observe handler".format(self, event))
            return False

        # Now begin by trying a basic method on the state to respond to the event
        if hasattr(self, event) and inspect.ismethod(getattr(self, event)):
            if trace:
                self.state_log_trace("will handle event '{0}'".format(event))

            sc.state_will_try_to_handle_event(self, event, event)
            ret = getattr(self, event)(arg1, arg2) != False
            sc.state_did_try_to_handle_event(self, event, event, ret)
            return ret

        # Try an event handler that is associated with an event represented as a string
        handler = self._registered_string_event_handlers[event] if event in self._registered_string_event_handlers else None
        if handler is not None:
            if trace:
                self.state_log_trace("{0} will handle event '{1}'".format(handler['name'], event))

            sc.state_will_try_to_handle_event(self, event, handler['name'])
            ret = handler['handler'](event, arg1, arg2) != False
            sc.state_did_try_to_handle_event(self, event, handler['name'], ret)
            return ret

        # Try an event handler that is associated with events matching a regular expression
        number_of_handlers = len(self._registered_reg_exp_event_handlers)
        i = 0
        while i < number_of_handlers:
            handler = self._registered_reg_exp_event_handlers[i]
            if handler['regexp'].match(event):
                if trace:
                    self.state_log_trace("{0} will handle event '{1}'".format(handler['name'], event))

                sc.state_will_try_to_handle_event(self, event, handler['name'])
                ret = handler['handler'](event, arg1, arg2) != False
                sc.state_did_try_to_handle_event(self, event, handler['name'], ret)
                return ret
            i += 1

        # Final attempt. If the state has an unknown_event function then invoke it to 
        # handle the event
        if hasattr(self, 'unknown_event') and inspect.ismethod(getattr(self, 'unknown_event')):
            if trace:
                self.state_log_trace("unknown_event will handle event '{0}'".format(event))

            sc.state_will_try_to_handle_event(self, event, "unknown_event")
            ret = self.unknown_event(event, arg1, arg2) != False
            sc.state_did_try_to_handle_event(self, event, "unknown_event", ret)
            return ret

        # Nothing was able to handle the given event for this state
        return False

    """
      Called whenever this state is to be entered during a state transition process. This 
      is useful when you want the state to perform some initial set up procedures. 
      
      If when entering the state you want to perform some kind of asynchronous action, such
      as an animation or fetching remote data, then you need to return an asynchronous 
      action, which is done like so:
      
          enter_state: function() {
            return this.perform_async('foo');
          }
      
      After returning an action to be performed asynchronously, the statechart will suspend
      the active state transition process. In order to resume the process, you must call
      this state's resume_go_to_state method or the statechart's resume_go_to_state. If no asynchronous 
      action is to be perform, then nothing needs to be returned.
      
      When the enter_state method is called, an optional context value may be supplied if
      one was provided to the go_to_state method.
      
      In the case that the context being supplied is a state context object 
      ({@link StateRouteHandlerContext}), an optional `enter_state_by_route` method can be invoked
      on this state if the state has implemented the method. If `enter_state_by_route` is
      not part of this state then the `enter_state` method will be invoked by default. The
      `enter_state_by_route` is simply a convenience method that helps removes checks to 
      determine if the context provide is a state route context object. 
      
      @param {Hash} [context] value if one was supplied to go_to_state when invoked
      
      @see #represented_route
    """
    def enter_state(self, context=None):
        pass

    """
      Notification called just before enter_state is invoked. 
      
      Note: This is intended to be used by the owning statechart but it can be overridden if 
      you need to do something special.
      
      @param {Hash} [context] value if one was supplied to go_to_state when invoked
      @see #enter_state
    """
    def state_will_become_entered(self, context=None):
        self._is_entering_state = True

    """
      Notification called just after enter_state is invoked. 
      
      Note: This is intended to be used by the owning statechart but it can be overridden if 
      you need to do something special.
      
      @param context {Hash} Optional value if one was supplied to go_to_state when invoked
      @see #enter_state
    """
    def state_did_become_entered(self, context=None):
        self._setup_all_state_observe_handlers()
        self._is_entering_state = False

    """
      Called whenever this state is to be exited during a state transition process. This is 
      useful when you want the state to peform some clean up procedures.
      
      If when exiting the state you want to perform some kind of asynchronous action, such
      as an animation or fetching remote data, then you need to return an asynchronous 
      action, which is done like so:
      
          exit_state: function() {
            return this.perform_async('foo');
          }
      
      After returning an action to be performed asynchronously, the statechart will suspend
      the active state transition process. In order to resume the process, you must call
      this state's resume_go_to_state method or the statechart's resume_go_to_state. If no asynchronous 
      action is to be perform, then nothing needs to be returned.
      
      When the exit_state method is called, an optional context value may be supplied if
      one was provided to the go_to_state method.
      
      @param context {Hash} Optional value if one was supplied to go_to_state when invoked
    """
    def exit_state(self, context=None):
        pass

    """
      Notification called just before exit_state is invoked. 
      
      Note: This is intended to be used by the owning statechart but it can be overridden 
      if you need to do something special.
      
      @param context {Hash} Optional value if one was supplied to go_to_state when invoked
      @see #exit_state
    """
    def state_will_become_exited(self, context=None):
        self._is_exiting_state = True
        self._teardown_all_state_observe_handlers()

    """
      Notification called just after exit_state is invoked. 
      
      Note: This is intended to be used by the owning statechart but it can be overridden 
      if you need to do something special.
      
      @param context {Hash} Optional value if one was supplied to go_to_state when invoked
      @see #exit_state
    """
    def state_did_become_exited(self, context=None):
        self._is_exiting_state = False

    """ @private 
    
      Used to setup all the state observer handlers. Should be done when
      the state has been entered.
    """
    def _setup_all_state_observe_handlers(self):
        self._configure_all_state_observe_handlers("addObserver")

    """ @private 
    
      Used to teardown all the state observer handlers. Should be done when
      the state is being exited.
    """
    def _teardown_all_state_observe_handlers(self):
        self._configure_all_state_observe_handlers("removeObserver")

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
    def _configure_all_state_observe_handlers(self, action):
        values = []
        for key in self._registered_state_observe_handlers:
            values = self._registered_state_observe_handlers[key]

        i = 0
        while i < len(values):
            path = values[i]
            observer = key
            dot_index = path.find(".")

            if dot_index < 0:
                getattr(self, action)(path, self, observer)
            elif path.find("*") == 0:
                getattr(self, action)(path[1], self, observer)
            else:
                root = None
                if dot_index == 0:
                    root = this
                    path = path[1]
                elif dot_index == 4 and path[0, 5] == "self.":
                    root = self
                    path = path[5]
                elif dot_index < 0 and len(path) == 4 and path == "self":
                    root = self
                    path = ""
                Observers[action](path, self, observer, root)
            i += 1

    """
      Call when an asynchronous action need to be performed when either entering or exiting
      a state.
      
      @see enter_state
      @see exit_state
    """
    def perform_async(self, func, arg1=None, arg2=None):
        return AsyncMixin().perform(func, arg1=arg1, arg2=arg2)

    """ @override
    
      Returns YES if this state can respond to the given event, otherwise
      NO is returned
    
      @param event {String} the value to check
      @returns {Boolean}
    """
    def responds_to_event(self, event):
        if event in self._registered_event_handlers:
            return False
        if hasattr(self, event) and inspect.ismethod(getattr(self, event)):
            return True
        if event in self._registered_string_event_handlers:
            return True
        if event in self._registered_state_observe_handlers:
            return False

        for handler in self._registered_reg_exp_event_handlers:
            if handler['regexp'].match(event):
                return True

        return hasattr(self, 'unknown_event') and inspect.ismethod(getattr(self, 'unknown_event'))

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
    def _full_path(self, *l): # [PORT] Added *l
        root = self.statechart.root_state_instance if self.statechart else None
        if root is None:
            self.full_path = self.name
        else:
            self.full_path = self.path_relative_to(root)

    def toString(self):
        return self.full_path

    """ @private """
    def _entered_substates_did_change(self, *l):
        #self.notifyPropertyChange("entered_substates")
        pass

    """ @private """
    def _current_substates_did_change(self, *l):
        #self.notifyPropertyChange("current_substates")
        pass

    """ @private """
    def _statechart_trace_did_change(self, *l):
        #self.notifyPropertyChange("trace")
        pass

    """ @private """
    def _statechart_owner_did_change(self, *l):
        #self.notifyPropertyChange("owner")
        pass

    """ 
      Used to log a state trace message
    """
    def state_log_trace(self, msg):
        self.statechart.statechart_log_trace("{0}: {1}".format(self, msg))

    """ 
      Used to log a state warning message
    """
    def state_log_warning(self, msg):
        self.statechart.statechart_log_warning(msg)

    """ 
      Used to log a state error message
    """
    def state_log_error(self, msg):
        sc = self.statechart
        sc.statechart_log_error(msg)

    # [PORT] plugin() method removed in python version.

    @classmethod
    def event_handler(self, events):
        def event_handler_decorator(fn):
            fn.is_event_handler = True
            fn.events = events
            return fn
        return event_handler_decorator

    #def event_handler(events):
        #def event_handler_decorator(self, *args, **kwargs):
            #fn.is_event_handler = True
            #fn.events = events
            #return fn
        #return event_handler_decorator(self, *args, **kwargs)

