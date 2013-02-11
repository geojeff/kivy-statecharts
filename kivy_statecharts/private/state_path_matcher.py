# ================================================================================
# Project: kivy-statecharts - A Statechart Framework for Kivy
# Copyright: (c) 2010, 2011 Michael Cohen, and contributors.
# Python Port: Jeff Pittman, ported from SproutCore, SC.Statechart
# ================================================================================

from kivy.event import EventDispatcher
from kivy.properties import ListProperty, StringProperty, ObjectProperty

'''
  Authorship Details
  ------------------

  Michael Cohen wrote the javascript version in 2010-2011 as Ki:

      https://github.com/FrozenCanuck/Ki/

  which became SC.Statechart in 2011:

      https://github.com/sproutcore/sproutcore/tree/master/frameworks/statechart

  Jeff Pittman wrote the Python port in 2012, porting directly from
  SC.Statechart, and prepared for incorporation into the Kivy project.

  kivy-statecharts became part of the Kivy project in [TODO].

  StatePathMatcher
  ----------------

  The `StatePathMatcher` is used to match a given state path match expression
  against state paths. A state path is a basic dot-notion consisting of
  one or more state names joined using '.'. Ex: 'foo', 'foo.bar'.

  The state path match expression language provides a way of expressing a state path.
  The expression is matched against a state path from the end of the state path
  to the beginning of the state path. A match is true if the expression has been
  satisfied by the given path.

  Syntax:

    expression -> <self> <subpath> | <path>

    path -> <part> <subpath>

    subpath -> '.' <part> <subpath> | empty

    self -> 'self'

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
'''
class StatePathMatcher(EventDispatcher):
    tokens = ListProperty([])
    '''A parsed set of tokens from the matcher's given expression.'''

    last_part = StringProperty(None)

    def __init__(self, state=None, expression=None):
        self.state = state
        '''The state that is used to represent 'self' for the
           matcher's given expression.
        '''

        self.expression = expression
        '''The expression used by this matcher to match against
           given state paths.
        '''

        self.bind(tokens=self._last_part)

        self._parse_expression()

    def _parse_expression(self):
        '''Will parse the matcher's given expession by creating tokens and
           chaining them together.

           .. Note:: Because the DSL for state path expressions is tiny, a
                     simple hand-crafted parser is being used. However, if the
                     DSL becomes any more complex, then it will probably be
                     necessary to refactor the logic in order follow a more
                     conventional type of parser.
        '''
        parts = self.expression.split('.') if self.expression else []
        tokens = []

        index = 0
        for part in parts:
            if '~' in part:
                part = part.split('~')
                if len(part) > 2:
                    raise Exception("Invalid use of '~' at part {0}".format(index))
                token = _ExpandToken(start=part[0], end=part[1])
            elif part == 'self':
                if len(tokens) > 0:
                    raise Exception("Invalid use of 'self' at part {0}".format(index))
                token = _ThisToken()
            else:
                token = _BasicToken(value=part)

            token.owning_matcher = self
            tokens.append(token)
            index += 1

        self.tokens = tokens

        stack = list(tokens)
        chain = stack.pop() if stack else None
        self._chain = chain
        token = stack.pop() if stack else None
        while token:
            chain.next_token = token
            chain = token
            token = stack.pop() if stack else None

    def _last_part(self, *l):
        '''Returns the last part of the expression. So if the
           expression is 'foo.bar' or 'foo~bar' then 'bar' is returned in both
           cases. If the expression is 'self' then 'self' is returned.
        '''
        self.last_part = self.tokens[-1].last_part if self.tokens else None

    def match(self, path):
        '''Will make a state path against this matcher's expression.

           The path provided must follow a basic dot-notation path containing
           one or more dots '.'. Ex: 'foo', 'foo.bar'.

           Return True if there is a match, otherwise False.
        '''
        # Bug out if path is None or is '' or if path is not a string.
        if path is None or not path or not isinstance(path, basestring):
            return False

        # When this matcher starts a match run, set self._stack. For example,
        # for path A.B.C, the stack witll be [ A, B, C ]. The related _pop method
        # will pop them off as C, then B, then A, during match operations.
        #
        # Set self._stack to None if path is None.
        #
        self._stack = path.split('.') if path else None

        # self._chain is the head of a linked-list of chained tokens. Kick off a
        # traversal of the tokens by firing on the head.
        return self._chain.match()

    def _pop(self):
        self._last_popped = self._stack.pop() if self._stack else None
        return self._last_popped

class _Token(EventDispatcher):
    '''Base class used to represent a token the expression.'''

    last_part = StringProperty(None)
    '''The last part the token represents, which is either a valid state
       name or representation of a state
    '''

    owning_matcher = ObjectProperty(None)
    '''The state path matcher that owns this token.'''

    next_token = ObjectProperty(None)
    '''The next token in the matching chain.'''

    def __init__(self, token_type):
        self.token_type = token_type
        super(_Token, self).__init__()

    def match(self):  #pragma: no cover
        '''Used to match against what is currently on the owning_matcher's
           current path stack
        '''
        raise NotImplementedError

class _BasicToken(_Token):
    '''Represents a basic name of a state in the expression. Ex 'foo'.

       A match is true if the matcher's current path stack is popped and the
       result matches this token's value.
    '''

    value = StringProperty(None)

    def __init__(self, value):
        self.bind(value=self._last_part)

        self.value = value

        super(_BasicToken, self).__init__(token_type='basic')

    def _last_part(self, *l):
        self.last_part = self.value

    def match(self):
        # Pop the next available part of the owning_matcher's expression part stack.
        # So that if we start with path A.B.C, we will first pop C, then B, then A.
        part = self.owning_matcher._pop() if self.owning_matcher else None

        # This is a bottom-up procedure, working from leaf toward root, such that
        # if value of this token doesn't match the last popped expression part, we
        # return back up the chain with False.
        if self.value != part:
            return False

        # self.value matches part, but if there are other parts, try to match them.
        return self.next_token.match() if self.next_token else True

class _ExpandToken(_Token):
    '''Represents an expanding path based on the use of the '<start>~<end>'
       syntax.  <start> represents the start and <end> represents the end.

       A match is True if the matcher's current path stack is first popped to
       match <end> and eventually is popped to match <start>. If neither <end>
       nor <start> are satisfied then False is returned.
    '''

    start = StringProperty(None)
    end = StringProperty(None)

    def __init__(self, start=None, end=None):
        self.bind(end=self._last_part)

        self.start = start
        self.end = end

        super(_ExpandToken, self).__init__(token_type='expand')

    def _last_part(self, *l):
        self.last_part = self.end

    def match(self):
        part = self.owning_matcher._pop() if self.owning_matcher else None
        if part != self.end:
            return False

        while part:
            if part == self.start:
                return self.next_token.match() if self.next_token else True
            part = self.owning_matcher._pop() if self.owning_matcher else None

        return False

class _ThisToken(_Token):
    '''Represents a this token, which is used to represent the owning_matcher's
       `state` property.

       A match is true if the last path part popped from the owning_matcher's
       current path stack is an immediate substate of the state this token
       represents.
    '''

    def __init__(self):
        self.last_part = 'self'

        super(_ThisToken, self).__init__(token_type='this')

    def match(self):
        part = self.owning_matcher._last_popped

        if part is None or len(self.owning_matcher._stack) != 0:
            return False

        for substate in self.owning_matcher.state.substates:
            if substate.name == part:
                return True

        return False
