from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty,
    ReferenceListProperty,
    ObjectProperty,
)
from kivy.vector import Vector
from kivy.factory import Factory
from kivy.clock import Clock
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    app = ObjectProperty(None)
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, app):
        self.app = app
        super(PongGame, self).__init__()

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, *args):
        self.ball.move()

        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        #went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


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
        def __init__(self, **kwargs):
            super(AppStatechart.
                  RootState, self).__init__(**kwargs)

        initialSubstateKey = 'ShowingPongGame'

        ###################
        # ShowingPongGame
        #
        class ShowingPongGame(State):
            def __init__(self, **kwargs):
                kwargs['name'] = 'ShowingPongGame'
                super(AppStatechart.
                      RootState.
                      ShowingPongGame, self).__init__(**kwargs)

            def enterState(self, context=None):
                print 'ShowingPongGame/enterState'
                self.statechart.app.run()

            def exitState(self, context=None):
                print 'ShowingPongGame/exitState'

Factory.register("PongBall", PongBall)
Factory.register("PongPaddle", PongPaddle)
Factory.register("PongGame", PongGame)


class PongApp(App):
    statechart = ObjectProperty(None)
    game = ObjectProperty(None)

    def build(self):
        print 'BUILDING'
        self.game = PongGame(app=self)
        self.game.serve_ball()
        Clock.schedule_interval(self.game.update, 1.0 / 60.0)
        return self.game


if __name__ in ('__android__', '__main__'):
    app = PongApp()

    # The app will be started from the statechart.
    statechart = AppStatechart(app=app)
    statechart.initStatechart()
