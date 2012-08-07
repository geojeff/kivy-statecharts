import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint, random
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import Statechart
from kivy_statecharts.system.statechart import StatechartManager


class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class BallsView(Widget):
    app = ObjectProperty(None)
    ball_1 = ObjectProperty(None)
    ball_2 = ObjectProperty(None)
    ball_3 = ObjectProperty(None)
    ball_4 = ObjectProperty(None)
    ball_5 = ObjectProperty(None)

    def __init__(self, app):
        self.app = app
        super(BallsView, self).__init__() 
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print 'My keyboard has been closed!'
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print 'The key', keycode, 'has been pressed'
        print ' - text is %r' % text
        print ' - modifiers are %r' % modifiers

        if keycode[1] == 's':
            self.app.statechart.sendEvent('speed_up')
        elif keycode[1] == 'escape':
            # Keycode is composed of an integer + a string
            # If we hit escape, release the keyboard
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def serve_balls(self, vel=(4,0)):
        for ball in (self.ball_1, self.ball_2, self.ball_3, self.ball_4, self.ball_5):
            ball.center = self.center
            ball.velocity = vel
        
    def update(self, *args):
        # Move balls by their velocities.
        for ball in (self.ball_1, self.ball_2, self.ball_3, self.ball_4, self.ball_5):
            ball.move()
        
        # Bounce balls off sides.
        for ball in (self.ball_1, self.ball_2, self.ball_3, self.ball_4, self.ball_5):
            if (ball.y < self.y) or (ball.top > self.top):
                ball.velocity_y *= -1
            if (ball.x < self.x) or (ball.x > self.right):
                ball.velocity_x *= -1


class MovingBallState(State):
    ballKey = StringProperty(None)
    ball = ObjectProperty(None)
    velocity_x = NumericProperty(1)
    velocity_y = NumericProperty(1)

    def enterState(self, context=None):
        self.ball = getattr(self.statechart.app.mainView, self.ballKey)
        self.ball.velocity_x += self.velocity_x
        self.ball.velocity_y += self.velocity_y
            
    def exitState(self, context=None):
        pass

    def speed_up(self, arg1=None, arg2=None):
        self.velocity_x += 1
        self.velocity_y += 1
        self.ball.velocity_x += self.velocity_x
        self.ball.velocity_y += self.velocity_y

    def slow_down(self, arg1=None, arg2=None):
        self.velocity_x -= 1
        self.velocity_y -= 1
        self.ball.velocity_x += self.velocity_x
        self.ball.velocity_y += self.velocity_y


##############
# Statechart
#
class AppStatechart(StatechartManager):
    def __init__(self, app, **kw):
        self.app = app
        self.trace = True
        self.rootStateClass = self.RootState
        super(AppStatechart, self).__init__(**kw)

    ###########################
    # RootState of statechart
    #
    class RootState(State):
        velocity_x = NumericProperty(1)
        velocity_y = NumericProperty(1)

        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'ShowingBalls'
            super(AppStatechart.RootState, self).__init__(**kwargs)
        
        def enterState(self, context=None):
            print 'RootState/enterState'
            self.statechart.app.mainView.serve_balls()
            Clock.schedule_interval(self.statechart.app.mainView.update, 1.0/60.0)
                        
        def exitState(self, context=None):
            print 'RootState/exitState'

        ##############################
        # ShowingBalls
        #
        class ShowingBalls(State):
            def __init__(self, **kwargs):
                kwargs['substatesAreConcurrent'] = True
                super(AppStatechart.RootState.ShowingBalls, self).__init__(**kwargs)
        
            def enterState(self, context=None):
                print 'ShowingBalls/enterState'
                        
            def exitState(self, context=None):
                print 'ShowingBalls/exitState'

            class Moving_Ball_1(MovingBallState):
                def __init__(self, **kwargs):
                    self.ballKey = 'ball_1'
                    self.velocity_x = 1
                    self.velocity_y = 1
                    super(AppStatechart.RootState.ShowingBalls.Moving_Ball_1, self).__init__(**kwargs)

            class Moving_Ball_2(MovingBallState):
                def __init__(self, **kwargs):
                    self.ballKey = 'ball_2'
                    self.velocity_x = 2
                    self.velocity_y = 2
                    super(AppStatechart.RootState.ShowingBalls.Moving_Ball_2, self).__init__(**kwargs)

            class Moving_Ball_3(MovingBallState):
                def __init__(self, **kwargs):
                    self.ballKey = 'ball_3'
                    self.velocity_x = 3
                    self.velocity_y = 3
                    super(AppStatechart.RootState.ShowingBalls.Moving_Ball_3, self).__init__(**kwargs)

            class Moving_Ball_4(MovingBallState):
                def __init__(self, **kwargs):
                    self.ballKey = 'ball_4'
                    self.velocity_x = 4
                    self.velocity_y = 4
                    super(AppStatechart.RootState.ShowingBalls.Moving_Ball_4, self).__init__(**kwargs)

            class Moving_Ball_5(MovingBallState):
                def __init__(self, **kwargs):
                    self.ballKey = 'ball_5'
                    self.velocity_x = 5
                    self.velocity_y = 5
                    super(AppStatechart.RootState.ShowingBalls.Moving_Ball_5, self).__init__(**kwargs)


Factory.register("Ball", Ball)
Factory.register("BallsView", BallsView)

class BallsApp(App):
    statechart = ObjectProperty(None)
    mainView = ObjectProperty(None)

    def build(self):
        print 'BUILDING'
        self.mainView = BallsView(app=self)
        self.statechart = AppStatechart(app=self)
        self.statechart.initStatechart()
        return self.mainView

if __name__ in ('__android__', '__main__'):
    app = BallsApp()
    app.run()

