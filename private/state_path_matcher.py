# ================================================================================
# Project:   Kivy.Statechart - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

from kivy.event import EventDispatcher
from kivy.properties import ListProperty, StringProperty

""" @class

  The `StatePathMatcher` is used to match a given state path match expression 
  against state paths. A state path is a basic dot-notion consisting of
  one or more state names joined using '.'. Ex: 'foo', 'foo.bar'. 
  
  The state path match expression language provides a way of expressing a state path.
  The expression is matched against a state path from the end of the state path
  to the beginning of the state path. A match is true if the expression has been
  satisfied by the given path. 
  
  Syntax:
  
    expression -> <this> <subpath> | <path>
    
    path -> <part> <subpath>
    
    subpath -> '.' <part> <subpath> | empty
  
    this -> 'this'
    
    part -> <name> | <expansion>
    
    expansion -> <name> '~' <name>
    
    name -> [a-z_][\w]*
    
  Expression examples:
  
    foo
    
    foo.bar
    
    foo.bar.mah
    
    foo~mah
    
    self.foo
    
    self.foo.bar
    
    self.foo~mah
    
    foo.bar~mah
    
    foo~bar.mah

  @extends Object
  @author Michael Cohen
"""
class StatePathMatcher(EventDispatcher):
    """
      A parsed set of tokens from the matcher's given expression
      
      @field {Array}
      @see #expression
    """
    tokens = ListProperty([])
  
    lastPart = StringProperty(None)

    def __init__(self, state=None, expression=None):
        """
          The state that is used to represent 'self' for the
          matcher's given expression.
          
          @field {State}
          @see #expression
        """
        self.state = state

        """
          The expression used by this matcher to match against
          given state paths
              
          @field {String}
        """
        self.expression = expression
          
        self.bind(tokens=self._lastPart)

        self._parseExpression()
  
    """ @private 
  
      Will parse the matcher's given expession by creating tokens and chaining them
      together.
      
      Note: Because the DSL for state path expressions is tiny, a simple hand-crafted 
      parser is being used. However, if the DSL becomes any more complex, then it will 
      probably be necessary to refactor the logic in order follow a more conventional 
      type of parser.
      
      @see #expression
    """
    def _parseExpression(self):
        parts = self.expression.split('.') if self.expression else []
        part = ''
        chain = None
        token = ''
        tokens = []
      
        for part in parts:
            if '~' in part:
                part = part.split('~')
                if len(part) > 2:
                    raise "Invalid use of '~' at part {0}".format(i)
                token = _ExpandToken(start=part[0], end=part[1])
            elif part == 'self':
                if len(tokens) > 0:
                    raise "Invalid use of 'self' at part {0}".format(i)
                token = _ThisToken()
            else:
                token = _BasicToken(value=part)
            
            token.owningMatcher = self
            tokens.append(token)
      
        self.tokens = tokens
      
        stack = tokens[:]
        chain = stack.pop() if stack else None
        self._chain = chain
        while chain:
            chain.nextToken = stack.pop() if stack else None
            chain = chain.nextToken

        # If the path expression is A.B.C, self.tokens is [ A, B, C ], and self._chain is C -> B -> A
        c = self._chain
        while c:
            c = c.nextToken
  
    """
      Returns the last part of the expression. So if the
      expression is 'foo.bar' or 'foo~bar' then 'bar' is returned
      in both cases. If the expression is 'self' then 'self' is
      returned. 
    """
    def _lastPart(self, *l):
        self.lastPart = self.tokens[-1].lastPart if self.tokens else None

    """
      Will make a state path against this matcher's expression. 
      
      The path provided must follow a basic dot-notation path containing
      one or dots '.'. Ex: 'foo', 'foo.bar'
      
      @param path {String} a dot-notation path
      @return {Boolean} true if there is a match, otherwise false
    """
    def match(self, path):
        # When this matcher starts a match run, set self._stack. For example,
        # for path A.B.C, the stack witll be [ A, B, C ]. The related _pop method
        # will pop them off as C, then B, then A, during match operations.
        #
        # Set self._stack to None if path is None.
        #
        self._stack = path.split('.') if path else None

        # Bug out is path is None or if path is not a string.
        if path is None or not isinstance(path, basestring):
            return False

        # self._chain is the head of a linked-list of chained tokens. Kick off a
        # traversal of the tokens by firing on the head.
        return self._chain.match()
  
    """ @private """
    def _pop(self):
        self._lastPopped = self._stack.pop() if self._stack else None
        return self._lastPopped

""" @private @class

  Base class used to represent a token the expression
"""
class _Token(EventDispatcher):
    """ 
      The last part the token represents, which is either a valid state
      name or representation of a state
    """
    lastPart = StringProperty(None)

    def __init__(self): 
        """ The type of this token """
        self.tokenType = None
  
        """ The state path matcher that owns this token """
        self.owningMatcher = None
  
        """ The next token in the matching chain """
        self.nextToken = None
        
        super(_Token, self).__init__() 
  
    """ 
      Used to match against what is currently on the owningMatcher's
      current path stack
    """
    def match(self):
        return False

""" @private @class

  Represents a basic name of a state in the expression. Ex 'foo'. 
  
  A match is true if the matcher's current path stack is popped and the
  result matches this token's value.
"""
class _BasicToken(_Token):
    value = StringProperty(None)

    def __init__(self, value):
        self.bind(value=self._lastPart)

        self.tokenType = 'basic'
        self.value = value

        super(_BasicToken, self).__init__() 

    def _lastPart(self, *l):
        self.lastPart = self.value
    
    def match(self):
        # Pop the next available part of the owningMatcher's expression part stack.
        # So that if we start with path A.B.C, we will first pop C, then B, then A.
        part = self.owningMatcher._pop() if self.owningMatcher else None

        # This is a bottom-up procedure, working from leaf toward root, such that
        # if value of this token doesn't match the last popped expression part, we 
        # return back up the chain with False.
        if self.value != part:
            return False
    
        # self.value matches part, but if there are other parts, try to match them.
        return self.nextToken.match() if self.nextToken else True
  
""" @private @class

  Represents an expanding path based on the use of the '<start>~<end>' syntax.
  <start> represents the start and <end> represents the end. 
  
  A match is True if the matcher's current path stack is first popped to match 
  <end> and eventually is popped to match <start>. If neither <end> nor <start>
  are satisfied then False is returned.
"""
class _ExpandToken(_Token):
    end = StringProperty(None)

    def __init__(self, start=None, end=None):
        self.bind(end=self._lastPart)

        self.tokenType = 'expand'
        self.start = start
        self.end = end

        super(_ExpandToken, self).__init__() 

    def _lastPart(self, *l):
        self.lastPart = self.end

    def match(self):
        start = self.start
        end = self.end
        part = ''
        token = self.nextToken
          
        part = self.owningMatcher._pop() if self.owningMatcher else None
        if part != end:
            return False
      
        while part:
            if part == start:
                return token.match() if token else True
            part = self.owningMatcher._pop() if self.owningMatcher else None
      
        return False

""" @private @class
  
  Represents a this token, which is used to represent the owningMatcher's
  `state` property.
  
  A match is true if the last path part popped from the owningMatcher's
  current path stack is an immediate substate of the state this
  token represents.
"""
class _ThisToken(_Token):
    def __init__(self):
        self.tokenType = 'self'
        self.lastPart = 'self'

        super(_ThisToken, self).__init__() 
  
    def match(self):
        state = self.owningMatcher.state
        substates = state.substates
        
        part = self.owningMatcher._lastPopped

        if part is None or len(self.owningMatcher._stack) != 0:
            return False
    
        for i in range(len(self.substates)):
            if substates[i]['name'] == part:
                return True
    
        return False
