# ================================================================================
# Project: kivy-statecharts - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

from kivy.event import EventDispatcher
from kivy_statecharts.private.state_path_matcher import StatePathMatcher
from kivy_statecharts.system.async import AsyncMixin
from kivy.properties import BooleanProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from collections import deque

import inspect, re

REGEX_TYPE = type(re.compile(''))

'''Authorship Details
   ------------------

   Michael Cohen wrote the javascript version in 2010-2011 as Ki:

       https://github.com/FrozenCanuck/Ki/

   which became SC.Statechart in 2011:

       https://github.com/sproutcore/sproutcore/tree/master/frameworks/statechart

   Jeff Pittman wrote the Python port in 2012, porting directly from
   SC.Statechart, and prepared for incorporation into the Kivy project.

   kivy-statecharts became part of the Kivy project in [TODO].
'''

class State(EventDispatcher):
    '''Represents a state within a statechart.

       The statechart actively manages all states belonging to it. When a state
       is created, it immediately registers itself with it parent states.

       You do not create an instance of a state itself. The statechart manager
       will go through its state heirarchy and create the states itself.

       For more information on using statecharts, see StatechartManager.
    '''

    trace = BooleanProperty(False)
    '''Indicates if this state should trace actions. Useful for debugging
       purposes. Managed by the statechart.

       :data:`trace` is a :class:`~kivy.properties.BooleanProperty`, default is
       False.
    '''

    owner = ObjectProperty(None, allownone=True)
    '''Indicates the owner of this state. If not set on the statechart
       then the owner is the statechart, otherwise it is the assigned object.
       Managed by the statechart.

       :data:`owner` is a :class:`~kivy.properties.ObjectProperty`, default is
       None.
    '''

    owner_key = StringProperty(None)
    '''[PORT] Added owner_key as property

       :data:`owner_key` is a :class:`~kivy.properties.StringProperty`, default
       is None.
    '''

    full_path = StringProperty(None)
    '''The relative path to the root state.

       :data:`full_path` is a :class:`~kivy.properties.StringProperty`, default
       is None.
    '''

    name = StringProperty(None)
    '''The name of the state.

       :data:`name` is a :class:`~kivy.properties.StringProperty`, default
       is None.
    '''

    parent_state = ObjectProperty(None, allownone=True)
    '''This state's parent state. Managed by the statechart.

       :data:`parent_state` is a :class:`~kivy.properties.ObjectProperty`,
       default is None.
    '''

    history_state = ObjectProperty(None, allownone=True)
    '''This state's history state. Can be null. Managed by the statechart.

       :data:`history_state` is a :class:`~kivy.properties.ObjectProperty`,
       default is None.
    '''

    initial_substate_key = StringProperty(None, allownone=True)
    '''Used to indicate the initial substate of this state.

       You assign the value with the name of the state. Upon creation of the
       state, the statechart will automatically change the property to be a
       corresponding state object

       The substate is only to be this state's immediate substates. If no
       initial substate is assigned then this states initial substate will be
       an instance of an empty state (EmptyState).

       Note that a statechart's root state must always have an explicity
       initial substate value assigned else an error will be thrown.

       :data:`initial_substate_key` is a
       :class:`~kivy.properties.StringProperty`, default is None.
    '''

    initial_substate_object = ObjectProperty(None, allownone=True)
    '''The state class object, as determined from initial_substate_key.

       :data:`initial_substate_object` is a
       :class:`~kivy.properties.ObjectProperty`, default is None.
    '''

    substates_are_concurrent = BooleanProperty(False)
    '''Used to indicates if this state's immediate substates are to be
       concurrent (orthogonal) to each other.

       :data:`substates_are_concurrent` is a
       :class:`~kivy.properties.BooleanProperty`, default is False.
    '''

    substates = ListProperty([])
    '''The immediate substates of this state. Managed by the statechart.

       :data:`substates` is a :class:`~kivy.properties.ListProperty`, default
       is [].
    '''

    statechart = ObjectProperty(None, allownone=True)
    '''The statechart that this state belongs to. Assigned by the owning
       statechart.

       :data:`statechart` is a :class:`~kivy.properties.ObjectProperty`,
       default is None.
    '''

    state_is_initialized = BooleanProperty(False)
    '''Indicates if this state has been initialized by the statechart

       :data:`state_is_initialized` is a
       :class:`~kivy.properties.BooleanProperty`, default is False.
    '''

    current_substates = ListProperty([])
    '''A list of this state's current substates. Managed by the statechart.

       :data:`current_substates` is a :class:`~kivy.properties.ListProperty`,
       default is [].
    '''

    entered_substates = ListProperty([])
    '''An array of this state's substates that are currently entered. Managed
       by the statechart.

       :data:`entered_substates` is a :class:`~kivy.properties.ListProperty`,
       default is [].
    '''

    def __init__(self, **kwargs):
        self.bind(name=self._full_path)
        self.bind(parent_state=self._full_path)

        self.bind(statechart=self._trace)
        self.bind(statechart=self._owner)

        self._registered_event_handlers = {}
        self._registered_string_event_handlers = {}
        self._registered_reg_exp_event_handlers = []
        self._registered_substate_paths = {}
        self._registered_substates = []
        self._is_entering_state = False
        self._is_exiting_state = False

        sc = self.statechart

        self.owner_key = sc.statechart_owner_key if sc else None

        # [PORT] Changed to bind to self, to try to do it from here...
        self.bind(owner_key=self._statechart_owner_did_change)

        for k,v in kwargs.items():
            if k == 'initial_substate_key':
                # [PORT] Force initial_substate_key to always be string.
                if isinstance(v, basestring):
                    self.initial_substate_key = v
                else:
                    name = v.name if hasattr(v, 'name') else None
                    if name:
                        self.initial_substate_key = name
                    else:
                        self.initial_substate_object = v
            else:
                setattr(self, k, v)

        # [PORT] initialize how? We have also init_state()
        super(State, self).__init__()

    def _trace(self, *l):
        if self.statechart:
            self.trace = self.statechart.trace

    def _owner(self, *l):
        sc = self.statechart
        key = sc.statechart_owner_key if sc else None
        owner = getattr(sc, key) if sc else None
        self.owner = owner if owner else sc

    def statechart_owner_did_change(self):
        self._owner()

        for substate in self.substates:
            substate.statechart_owner_did_change()

    def destroy(self):
        sc = self.statechart

        # [PORT] What about destroying owner_key
        self.owner_key = sc.statechart_owner_key if sc else None

        self.unbind(owner_key=self._statechart_owner_did_change)

        [state.destroy() for state in self.substates]

        self.substates = []
        self.current_substates = []
        self.entered_substates = []
        self.parent_state = None
        self.history_state = None
        self.initial_substate_key = None
        self.initial_substate_object = None
        self.statechart = None

        #self.notifyPropertyChange("owner")

        self._registered_event_handlers = []
        self._registered_string_event_handlers = []
        self._registered_reg_exp_event_handlers = []
        self._registered_substate_paths = []
        self._registered_substates = []

    def init_state(self):
        '''Used to initialize this state. To only be called by the owning
           statechart.
        '''
        if self.state_is_initialized:
            self.state_log_warning("Cannot init_state() -- already init'ed.")
            return

        if not self.name:
            self.state_log_error("Cannot init_state() an unnamed state.")
            raise Exception("Cannot init_state() an unnamed state.")

        self._register_with_parent_states()

        matched_initial_substate = False
        value_is_method = False
        history_state = None

        self.substates = []

        if hasattr(self, 'InitialSubstate'):
            from kivy_statecharts.system.history_state import HistoryState

            initial_substate_class = getattr(self, 'InitialSubstate')

            if (initial_substate_class is not None and
                inspect.isclass(initial_substate_class) and
                issubclass(initial_substate_class, HistoryState)):

                history_state = self.create_substate(initial_substate_class)

                if history_state.default_state:
                    setattr(self,
                            'initial_substate_key',
                            history_state.default_state)
                else:
                    msg = ("Initial substate is invalid. History state "
                           "requires the name of a default state to be set.")
                    self.state_log_error(msg)
                    raise Exception(msg)

        # Iterate through all this state's substates, if any, create them, and
        # then initialize them. This causes a recursive process.
        for key in dir(self):
            if key == '__class__':
                continue

            value = getattr(self, key)
            if not inspect.ismethod(value) and not inspect.isclass(value):
                continue

            value_is_method = inspect.ismethod(value)

            if (value_is_method and hasattr(value, 'is_event_handler')
                    and value.is_event_handler == True):
                self._register_event_handler(key, value)
                continue

            if inspect.isclass(value) and issubclass(value, State):
                state = self._add_substate(key, value, None)
                # [PORT] Added clarification in this condition to distinguish
                #        between the normal case of having a simple
                #        initial_substate_key defined, vs. the use of a
                #        HistoryState as the initial_substate.
                if key == self.initial_substate_key and history_state is None:
                    # [PORT] Needs to always be a string.
                    self.initial_substate_key = \
                            state if isinstance(state, basestring) else state.name
                    self.initial_substate_object = state
                    matched_initial_substate = True
                elif history_state and history_state.default_state == key:
                    # [PORT] No need to do this in python version, because
                    #        default_state is a key; We do not reset
                    #        default_state to be a state object -- we rely on
                    #        get_substate to find it by the key when it is
                    #        accessed. default_state has already been set (See
                    #        check above).
                    # [PORT] Needs to always be a string.
                    #history_state.default_state = \
                    #       state if isinstance(state, basestring) else state.name
                    matched_initial_substate = True

        if self.initial_substate_key and not matched_initial_substate:
            if len(self.substates) == 0:
                if self.initial_substate_key:
                    msg = ("Unable to make {0} an initial substate since state "
                           "{1} has no substates").format(
                                   self.initial_substate_key, self)
                    self.state_log_error(msg)
                    raise Exception(msg)
            elif len(self.substates) > 0:
                msg = ("Unable to set initial substate {0} since it did "
                       "not match any of state {1}'s substates").format(
                               self.initial_substate_key, self)
                self.state_log_error(msg)
                raise Exception(msg)

        if len(self.substates) > 0:
            state = self._add_empty_initial_substate_if_needed()
            if (state is None
                      and self.initial_substate_key
                      and self.substates_are_concurrent):
                msg = ("Cannot use {0} as initial substate since "
                       "substates are all concurrent for state "
                       "{1}").format(self.initial_substate_key, self)
                self.state_log_error(msg)
                raise Exception(msg)

        #self.notifyPropertyChange("substates")
        # [PORT] substates have changed. Call _current_states on statechart,
        #        which is bound to root_state_instance, and updates
        #        self.current_states = self.root_state_instance.substates.
        #        That binding won't fire if root_state_instance.substates
        #        changes, so we manually call it in kivy.
        if self.statechart:
            self.statechart._current_states()

        self.current_substates = []
        self.entered_substates = []
        self.state_is_initialized = True

    def _add_empty_initial_substate_if_needed(self):
        from kivy_statecharts.system.empty_state import EmptyState

        if self.initial_substate_key or self.substates_are_concurrent:
            return None

        state = self.create_substate(EmptyState)

        # EmptyState has name set to "__EMPTY_STATE__"
        self.initial_substate_key = state.name

        # The EmptyState's name, "__EMPTY_STATE__" is used as a
        # property name, whose value is the empty state object
        setattr(self, state.name, state)

        # [PORT] Why would this be set, if initial_substate_key is set?
        self.initial_substate_object = state

        self.substates.append(state)

        state.init_state()

        msg = ("state {0} has no initial substate defined. Will default to "
               "using an empty state as initial substate")
        self.state_log_warning(msg.format(self))

        return state

    def _add_substate(self, name, state, attr):
        attr = dict.copy(attr) if attr else {}
        attr['name'] = name

        state = self.create_substate(state, attr)

        self.substates.append(state)

        setattr(self, name, state)

        state.init_state()

        return state

    def add_substate(self, name, state=None, attr={}):
        '''Used to dynamically add a substate to this state. Once added
           successfully you are then able to go to it from any other state
           within the owning statechart.

           A couple of notes when adding a substate:

           * If this state does not have any substates, then in addition to the
             substate being added, an empty state will also be added and set as
             the initial substate. To make the added substate the initial
             substate, set this object's initial_substate_key property.
           * If this state is a current state, the added substate will not be
             entered.
           * If this state is entered and its substates are concurrent, the added
             substate will not be entered.

           If this state is either entered or current and you'd like the added
           substate to take affect, you will need to explicitly reenter this
           state by calling its `reenter` method.

           Be aware that the name of the state you are adding must not conflict
           with the name of a property on this state or else you will get an
           error.  In addition, this state must be initialized to add
           substates.

           Parameters:

           * name {String} - A unique name for the given substate.
           * state {State} - A class that derives from `State`.
           * attr {dict} - args dict to be applied to the substate.

           Returns an instance of the given state class.
        '''
        if not name: # [PORT] this used the empty(name) function.
            msg = "Cannot add substate. name required"
            self.state_log_error(msg)
            raise Exception(msg)

        if hasattr(self, name):
            msg = ("Cannot add substate '{0}'. Already a defined "
                   "property").format(name)
            self.state_log_error(msg)
            raise Exception(msg)

        if not self.state_is_initialized:
            msg = ("Cannot add substate '{0}'. Parent state is not yet "
                   "initialized").format(name)
            self.state_log_error(msg)
            raise Exception(msg)

        if state is None:
            state = State
        elif state is not None and isinstance(state, dict):
            attr = state
            state = State

        state_is_valid = inspect.isclass(state) and issubclass(state, State)

        if not state_is_valid:
            msg = ("Cannot add substate '{0}'. Must provide a state "
                   "class").format(name)
            self.state_log_error(msg)
            raise Exception(msg)

        state = self._add_substate(name, state, attr)

        self._add_empty_initial_substate_if_needed()

        # [PORT] Should there be a manual update call here?
        #self.dispatch('substates')
        #self.notifyPropertyChange("substates")

        return state

    def create_substate(self, state, attr=None):
        attr = dict.copy(attr) if attr else {}
        attr['parent_state'] = self
        attr['statechart'] = self.statechart
        return state(**attr)

    def _register_event_handler(self, name, handler):
        '''Registers event handlers with this state. Event handlers are special
           functions on the state that are intended to handle more than one
           event.  This compared to basic functions that only respond to a
           single event that reflects the name of the method.
        '''
        self._registered_event_handlers[name] = handler

        for event in handler.events:
            # [PORT] checking for string and unicode -- need unicode? otherwise just str?
            if isinstance(event, basestring):
                self._registered_string_event_handlers[event] = \
                        { 'name': name, 'handler': handler }
                continue

            if isinstance(event, REGEX_TYPE):
                self._registered_reg_exp_event_handlers.append(
                        { 'name': name, 'handler': handler, 'regexp': event })
                continue

            msg = ("Invalid event {0} for event handler {1} in "
                   "state {1}").format(event, name, self)
            self.state_log_error(msg)
            raise Exception(msg)

    def _register_with_parent_states(self):
        '''Traverse up through this state's parent states to register this
           state with them.
        '''
        parent = self.parent_state

        while parent is not None:
            parent._register_substate(self)
            parent = parent.parent_state

    def _register_substate(self, state):
        '''Registers a given state as a substate of this state.'''
        path = state.path_relative_to(self)

        self._registered_substates.append(state)

        # Keep track of states based on their relative path to this state.
        if not state.name in self._registered_substate_paths:
            self._registered_substate_paths[state.name] = {}

        self._registered_substate_paths[state.name][path] = state

    def path_relative_to(self, state):
        '''Will generate path for a given state that is relative to this state.
           It is required that the given state is a substate of this state.

           If the heirarchy of the given state to this state is the following:
           A > B > C, where A is this state and C is the given state, then the
           relative path generated will be "B.C"
        '''
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

        while parent and parent != state:
            path = "{0}.{1}".format(parent.name, path)
            parent = parent.parent_state

        if parent != state and state != self:
            msg = ("Cannot generate relative path from {0} since it is not a "
                   "parent state of {1}").format(state, self)
            self.state_log_error(msg)
            raise Exception(msg)

        return path

    def get_substate(self, value, callback=None):
        '''Used to get a substate of this state that matches a given value.

           If the value is a state object, then the value will be returned if
           it is indeed a substate of this state, otherwise null is returned.

           If the given value is a string, then the string is assumed to be a
           path expression to a substate. The value is then parsed to find the
           closest match. For path expression syntax, refer to the {@link
           StatePathMatcher} class.

           If there is no match then null is returned. If there is more than
           one match then null is returned and an error is generated indicating
           ambiguity of the given value.

           An optional callback can be provided to handle the scenario when
           either no substate is found or there is more than one match. The
           callback is then given the opportunity to further handle the outcome
           and return a result which the get_substate method will then return.
           The callback should have the following signature::

               function(state, value, paths)

               state: The state on which get_state() was invokedon.
               value: The value supplied to get_state().
               paths: An array of substate paths that matched the given value.

           If there were no matches then `paths` is not provided to the
           callback.

           Parameters:

           * value {State|String} - Used to identify a substate of this state.
           * callback {Function} - Optional callback.
        '''

        if value is None:
            return None

        if not isinstance(value, basestring):
            if value in self._registered_substates:
                return value
            elif isinstance(value, State):
                return None
            else:
                msg = ("Cannot find matching substate. value must be a State "
                       "class or string, not type: {0}").format(type(value))
                self.state_log_error(msg)
                raise Exception(msg)

        # [PORT] Considered this, but it seemed to match on what should
        #        remain ambiguous.
        #for state in self._registered_substates:
            #if value == state.name:
                #return state

        # Not found yet, so keep looking with path matcher.
        matcher = StatePathMatcher(state=self, expression=value)

        matches = []

        # Grab the paths associated with this state name.
        paths = self._registered_substate_paths[matcher.last_part] \
                if matcher.last_part in self._registered_substate_paths \
                else None

        if paths is None:
            return self._notify_substate_not_found(callback=callback,
                                                   value=value)

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
                path_keys.append(key)

            if callback is not None:
                return self._notify_substate_not_found(callback=callback,
                                                       value=value,
                                                       keys=path_keys)

            msg = ("Cannot find substate matching '{0}' in state {1}. "
                   "Ambiguous with "
                   "the following: {2}").format(value, self.full_path,
                                                ', '.join(path_keys))
            self.state_log_error(msg)
            raise Exception(msg)

        return self._notify_substate_not_found(callback=callback,
                                               value=value)

    def _notify_substate_not_found(self, callback=None,
                                   value=None, keys=None):
        if callback:
            # This, and an even more complicated system involving an optional
            # target argument, was in the javascript version. Removed here,
            # until it is deemed necessary for some reason.
            #if hasattr(self, callback.__name__):
            #    return getattr(self, callback.__name__)(self, value, keys)
            #else:
            return callback(self, value, keys)
        else:
            return None

    def get_state(self, value):
        '''Will attempt to get a state relative to this state.

           A state is returned based on the following:

           1. First check this state's substates for a match; and
           2. If no matching substate then attempt to get the state from
              this state's parent state.

           Therefore states are recursively traversed up to the root state to
           identify a match, and if found is ultimately returned, otherwise
           null is returned. In the case that the value supplied is ambiguous
           an error message is returned.

           The value provided can either be a state object or a state path
           expression. For path expression syntax, refer to the {@link
           StatePathMatcher} class.
        '''
        # [PORT] Added the second part. See get_state tests.
        if value == self.name or value == self:
            return self

        # [PORT] This doesn't make sense. It is like a protection for a wrong
        #        call.
        if isinstance(value, State):
            return value

        return self.get_substate(value, self._handle_substate_not_found)

    def _handle_substate_not_found(self, state, value, keys=None):
        parent_state = self.parent_state

        if parent_state is not None:
            return parent_state.get_state(value)

        if keys is not None:
            msg = ("Cannot find state matching '{0}'. "
                   "Ambiguous with the following: {1}.")
            self.state_log_error(msg.format(value, ', '.join(keys)))

        return None

    def go_to_state(self, value, context=None):
        '''Used to go to a state in the statechart either directly from this
           state if it is a current state, or from the first relative current
           state from this state.

           If the value given is a string then it is considered a state path
           expression. The path is then used to find a state relative to this
           state based on rules of the {@link #get_state} method.

           Parameters:

           * value {State|String} - The state to go to.
           * context {dict|Object} - Optional dict that will be supplied to
                 all states that are exited and entered during the state
                 transition process. Context can not be an instance of State.
        '''
        state = self.get_state(value)

        if state is None:
            msg = ("Cannot go to state {0} from state {1}. Invalid "
                   "value.").format(value, self)
            self.state_log_error(msg)
            raise Exception(msg)

        fromState = self.find_first_relative_current_state(state)

        self.statechart.go_to_state(state=state,
                                    from_current_state=fromState,
                                    use_history=False,
                                    context=context)

    def go_to_history_state(self, value, recursive=None, context=None):
        '''Used to go to a given state's history state in the statechart either
           directly from this state if it is a current state or from one of
           this state's current substates.

           If the value given is a string then it is considered a state path
           expression. The path is then used to find a state relative to this
           state based on rules of the get_state() method.

           * value {State|String} - The state whose history state to go to.
           * recursive {Boolean} indicates whether to follow history states
                 recusively starting from the given state
           * context {Hash|Object} - Optional dict that will be supplied to
                 all states that are exited entered during the state transition
                 process. Context can not be an instance of State.
        '''
        state = self.get_state(value)

        if state is None:
            msg = ("Cannot go to history state {0} from state {1}. "
                   "Invalid value.").format(value, self)
            self.state_log_error(msg)
            raise Exception(msg)

        fromState = self.find_first_relative_current_state(state)

        self.statechart.go_to_history_state(state=state,
                                            from_current_state=fromState,
                                            recursive=recursive,
                                            context=context)

    def resume_go_to_state(self):
        '''Resumes an active goto state transition process that has been
           suspended.
        '''
        self.statechart.resume_go_to_state()

    def state_is_current_substate(self, state=None):
        '''Checks if a given state is a current substate of this state.
           Mainly used in cases when this state is a concurrent state.

           Returns True if the given state is a current substate, otherwise
           False.
        '''
        state_obj = None
        if isinstance(state, basestring):
            state_obj = self.statechart.get_state(state)
        else:
            state_obj = state

        if not state_obj:
            return False

        return True if state_obj in self.current_substates else False

    def state_is_entered_substate(self, state=None):
        '''Used to check if a given state is a current substate of this state.
           Mainly used in cases when this state is a concurrent state.

           Returns True if the given state is a current substate, otherwise
           False.
        '''
        state_obj = None
        if isinstance(state, basestring):
            state_obj = self.statechart.get_state(state)
        else:
            state_obj = state

        if not state_obj:
            return False

        return True if state_obj in self.entered_substates else False

    def is_root_state(self):
        return True if self.statechart.root_state_instance is self else False

    def is_current_state(self):
        return True if self.state_is_current_substate(self) else False

    def is_concurrent_state(self):
        return True if self.parent_state.substates_are_concurrent else False

    def is_entered_state(self):
        '''A state is currently entered if during a state transition process
           the state's enter_state method was invoked, but only after its
           exit_state method was called, if at all.
        '''
        return True if self.state_is_entered_substate(self) else False

    def find_first_relative_current_state(self, anchor=None):
        '''Will attempt to find a current state in the statechart that is
           relative to this state.

           Ordered set of rules to find a relative current state:

             1. If this state is a current state then it will be returned

             2. If this state has no current states and this state has a parent
                state then return parent state's first relative current state,
                otherwise return null

             3. If this state has more than one current state then use the
                given anchor state to get a corresponding substate that can be
                used to find a current state relative to the substate, if a
                substate was found.

             4. If (3) did not find a relative current state then default to
                returning this state's first current substate.

           The anchor param {State|String} is optional. It is a substate of
           this state used to help direct finding a current state.
        '''
        if self.is_current_state():
            return self

        if not self.current_substates:
            return self.parent_state.find_first_relative_current_state() \
                   if self.parent_state is not None \
                   else None

        if len(self.current_substates) > 1:
            anchor = self.get_substate(anchor)
            if anchor is not None:
                return anchor.find_first_relative_current_state()

        return self.current_substates[0]

    def reenter(self):
        '''Used to re-enter this state. Call this only when the state is a
           current state of the statechart.
        '''
        if self.is_entered_state():
            # [PORT] Changed this from self to self.name, after str and key
            #        changes. Then, had to change it from self.go_to_state to
            #        self.statechart.go_to_state -- need to pin down that
            #        difference.
            self.statechart.go_to_state(state=self.name)
        else:
            msg = ("Cannot re-enter state {0} since it is not an entered "
                   "state in the statechart").format(self)
            self.state_log_error(msg)
            raise Exception(msg)

    def try_to_handle_event(self, event, arg1=None, arg2=None):
        '''Called by the statechart to allow a state to try and handle the
           given event. If the event is handled by the state then YES is
           returned, otherwise NO.

           There is a particular order in how an event is handled by a state:

           1. Basic function whose name matches the event.
           2. Registered event handler that is associated with an event
              represented as a string.
           3. Registered event handler that is associated with events matching
              a regular expression.
           4. The unknown_event function.

           Use of event handlers that are associated with events matching a
           regular expression may incur a performance hit, so they should be
           used sparingly.

           The unknown_event function is only invoked if the state has it,
           otherwise it is skipped. Note that you should be careful when using
           unknown_event since it can be either abused or cause unexpected
           behavior.
        '''
        sc = self.statechart
        ret = None

        # First check if the name of the event is the same as a registered
        # event handler. If so, then do not handle the event.
        #
        # [PORT] So, this means that if you have a method called
        #        event_handler1, you need to call the associated event
        #        event1, not event_handler1. This is confusing. Methods in a
        #        state class are by definition event handlers, registerd by
        #        the method names. These are handled below. Special 'event
        #        handlers', capable of handling more than one event are the
        #        ones marked with the State.event_handler([]) decorator. And
        #        then there are plain event handlers, treated by this
        #        conditional. What are they? There probably be better
        #        terminology to differentiate, e.g., registeredMethods vs.
        #        event_handlers vs. multipleEventHanders, perhaps.
        #
        if event in self._registered_event_handlers:
            msg = ("state {0} can not handle event '{1}' since it is a "
                   "registered event handler").format(self, event)
            self.state_log_warning(msg)
            raise Exception(msg)

        # Now begin by trying a basic method on the state to respond to the
        # event
        if hasattr(self, event) and inspect.ismethod(getattr(self, event)):
            if self.trace:
                self.state_log_trace("will handle event '{0}'".format(event))

            sc.state_will_try_to_handle_event(self, event, event)
            ret = getattr(self, event)(arg1, arg2) != False
            sc.state_did_try_to_handle_event(self, event, event, ret)
            return ret

        # Try an event handler that is associated with an event represented
        # as a string
        handler = self._registered_string_event_handlers[event] \
                  if event in self._registered_string_event_handlers \
                  else None
        if handler is not None:
            if self.trace:
                msg = ("{0} will handle event '{1}'").format(handler['name'],
                                                             event)
                self.state_log_trace(msg)

            sc.state_will_try_to_handle_event(self, event, handler['name'])
            ret = handler['handler'](event, arg1, arg2) != False
            sc.state_did_try_to_handle_event(
                    self, event, handler['name'], ret)
            return ret

        # Try an event handler that is associated with events matching a
        # regular expression
        number_of_handlers = len(self._registered_reg_exp_event_handlers)
        i = 0
        while i < number_of_handlers:
            handler = self._registered_reg_exp_event_handlers[i]
            if handler['regexp'].match(event):
                if self.trace:
                    msg = "{0} will handle event '{1}'".format(
                            handler['name'], event)
                    self.state_log_trace(msg)

                sc.state_will_try_to_handle_event(
                        self, event, handler['name'])
                ret = handler['handler'](event, arg1, arg2) != False
                sc.state_did_try_to_handle_event(
                        self, event, handler['name'], ret)
                return ret
            i += 1

        # Final attempt. If the state has an unknown_event function then
        # invoke it to handle the event
        if (hasattr(self, 'unknown_event') and
                inspect.ismethod(getattr(self, 'unknown_event'))):
            if self.trace:
                msg = "unknown_event will handle event '{0}'".format(event)
                self.state_log_trace(msg)

            sc.state_will_try_to_handle_event(
                self, event, "unknown_event")
            ret = self.unknown_event(event, arg1, arg2) != False
            sc.state_did_try_to_handle_event(
                self, event, "unknown_event", ret)
            return ret

        # Nothing was able to handle the given event for this state
        return False

    def enter_state(self, context=None):
        '''Called whenever this state is to be entered during a state
           transition process. This is useful when you want the state to
           perform some initial set up procedures.

           If when entering the state you want to perform some kind of
           asynchronous action, such as an animation or fetching remote data,
           then you need to return an asynchronous action, which is done like
           so:

                def enter_state():
                     return self.perform_async('foo')

           After returning an action to be performed asynchronously, the
           statechart will suspend the active state transition process. In
           order to resume the process, you must call this state's
           resume_go_to_state method or the statechart's resume_go_to_state. If
           no asynchronous action is to be performed, then nothing needs to be
           returned.

           When the enter_state method is called, an optional context value may
           be supplied if one was provided to the go_to_state method.

           The context param {dict} is used if one was supplied to go_to_state
           when invoked.
        '''
        pass

    def state_will_become_entered(self, context=None):
        '''Notification called just before enter_state is invoked.

           .. Note:: This is intended to be used by the owning statechart but
                     it can be overridden if you need to do something special.

          The context param {dict} is used if one was supplied to go_to_state
          when invoked.
        '''
        self._is_entering_state = True

    def state_did_become_entered(self, context=None):
        '''Notification called just after enter_state is invoked.

           .. Note:: This is intended to be used by the owning statechart but
                     it can be overridden if you need to do something special.

           The context param {dict} is used if one was supplied to go_to_state
           when invoked.
        '''
        self._is_entering_state = False

    def exit_state(self, context=None):
        '''Called whenever this state is to be exited during a state transition
           process. This is useful when you want the state to peform some clean
           up procedures.

           If when exiting the state you want to perform some kind of
           asynchronous action, such as an animation or fetching remote data,
           then you need to return an asynchronous action, which is done like
           so:

               def exit_state():
                   return self.perform_async('foo')

           After returning an action to be performed asynchronously, the
           statechart will suspend the active state transition process. In
           order to resume the process, you must call this state's
           resume_go_to_state method or the statechart's resume_go_to_state. If
           no asynchronous action is to be performed, then nothing needs to be
           returned.

           When the exit_state method is called, an optional context value may
           be supplied if one was provided to the go_to_state method.

           The context param {dict} is used if one was supplied to go_to_state
           when invoked.
        '''
        pass

    def state_will_become_exited(self, context=None):
        '''Notification called just before exit_state is invoked.

           .. Note:: This is intended to be used by the owning statechart but it
                     can be overridden if you need to do something special.

           The context param {dict} is used if one was supplied to go_to_state
           when invoked.
        '''
        self._is_exiting_state = True

    def state_did_become_exited(self, context=None):
        '''Notification called just after exit_state is invoked.

           .. Note:: This is intended to be used by the owning statechart but
                     it can be overridden if you need to do something special.

           The context param {dict} is used if one was supplied to go_to_state
           when invoked.
        '''
        self._is_exiting_state = False

    def perform_async(self, func, arg1=None, arg2=None):
        '''Call when an asynchronous action need to be performed when either
           entering or exiting a state.
        '''
        return AsyncMixin().perform(func, arg1=arg1, arg2=arg2)

    def responds_to_event(self, event):
        '''Override as needed.

           Returns True if this state can respond to the given event, otherwise
           False is returned.

           The event {String} parm is the value to check.
        '''
        if event in self._registered_event_handlers:
            return False
        if hasattr(self, event) and inspect.ismethod(getattr(self, event)):
            return True
        if event in self._registered_string_event_handlers:
            return True

        for handler in self._registered_reg_exp_event_handlers:
            if handler['regexp'].match(event):
                return True

        return (hasattr(self, 'unknown_event') and
                inspect.ismethod(getattr(self, 'unknown_event')))

    def _full_path(self, *l): # [PORT] Added *l
        '''Returns the path for this state relative to the statechart's
           root state.

           The path is a dot-notation string representing the path from this
           state to the statechart's root state, but without including the root
           state in the path. For instance, if the name of this state if "foo"
           and the parent state's name is "bar" where bar's parent state is the
           root state, then the full path is "Bar.foo"
        '''
        root = self.statechart.root_state_instance \
                if self.statechart \
                else None
        if root is None:
            self.full_path = self.name
        else:
            self.full_path = self.path_relative_to(root)

    def __str__(self):
        return self.full_path

    def _entered_substates_did_change(self, *l):  #pragma: no cover
        #self.notifyPropertyChange("entered_substates")
        pass

    def _current_substates_did_change(self, *l):  #pragma: no cover
        #self.notifyPropertyChange("current_substates")
        pass

    def _statechart_owner_did_change(self, *l):  #pragma: no cover
        #self.notifyPropertyChange("owner")
        pass

    def state_log_trace(self, msg):
        '''Used to log a state trace message.'''
        if self.statechart:
            self.statechart.statechart_log_trace("{0}: {1}".format(self, msg))

    def state_log_warning(self, msg):
        '''Used to log a state warning message.'''
        if self.statechart:
            self.statechart.statechart_log_warning(msg)

    def state_log_error(self, msg):
        '''Used to log a state error message.'''
        if self.statechart:
            self.statechart.statechart_log_error(msg)

    @classmethod
    def event_handler(self, events):
        def event_handler_decorator(fn):
            fn.is_event_handler = True
            fn.events = events
            return fn
        return event_handler_decorator
