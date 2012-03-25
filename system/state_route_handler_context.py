# ================================================================================
# Project:   Kivy.Statechart - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

import inspect

"""
  @class

  Represents contextual information for whenever a state handles a triggered
  route. In additional to retaining contextual information, you can also
  use the object to retry trigging the state's route handler. Useful in cases
  where you need to defer the handling of the route for a later time. 
  
  @see State

  @extends Object
  @author Michael Cohen
"""
class StateRouteHandlerContext:
    """
      The state that constructed this context object.
    
      @property {State}
    """
    state = ObjectProperty(None)
    
    """
      The location that caused the state's route to be
      triggered. 
    
      @property {String}
    """
    location = StringProperty(None)
    
    """
      The parameters that were supplied to the state's
      handler when the state's route was triggered.
    
      @property {Hash}
    """
    params = DictProperty({})
    
    """
      The handler that got invoked when the state's
      route was triggered. This can either be a reference
      to the actual method or a name of the method.
    
       [PORT] treated here as String

      @property {Function|String}
    """
    handler = StringProperty(None)

    """
      Used to retry invoking the state's handler for when
      the state's route gets triggered. When called this will
      essentially perform the same call as when the handler 
      was originally triggered on state. 
    """
    def retry(self):
        if isinstance(self.handler, basestring):
            self.handler = self.state[self.handler]
  
        if inspect.isfunction(self.handler):
            self.handler(self.state, [self.params])
