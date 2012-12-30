# ================================================================================
# Project: kivy-statecharts - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

import inspect

class AsyncMixin:
    '''Singleton.'''

    def perform(self, func, arg1=None, arg2=None):
        '''Call in either a state's enter_state or exit_state method when you
           want a state to perform an asynchronous action, such as an
           animation.

           Parameters:

           * func {String|Function} the function to be invoked on a state
           * arg1 Optional. An argument to pass to the given function
           * arg2 Optional. An argument to pass to the given function

           Returns {Async} a new instance of an Async call instance.
        '''
        return Async(func, arg1=arg1, arg2=arg2)

class Async(AsyncMixin):
    '''Represents a call that is intended to be asynchronous. This is
       used during a state transition process when either entering or exiting a
       state.
    '''
    def __init__(self, func, arg1=None, arg2=None):
        self.func = func
        self.arg1 = arg1
        self.arg2 = arg2

    def try_to_perform(self, state):
        '''Called by the statechart.'''
        if isinstance(self.func, basestring):
            if hasattr(state, self.func):
              getattr(state, self.func)(self.arg1, self.arg2)
        # [PORT] Either one, same call sig?
        elif inspect.isfunction(self.func) or inspect.ismethod(self.func):
            self.func(state, self.arg1, self.arg2)
