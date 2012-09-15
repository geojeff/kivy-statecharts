from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty,
    ReferenceListProperty,
    ObjectProperty,
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.graphics.vertex_instructions import Rectangle, Ellipse
from kivy.uix.floatlayout import FloatLayout

from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager


class Paddle(Widget):
    parent = ObjectProperty(None)
    score = NumericProperty(0)
    x = NumericProperty(0)
    y = NumericProperty(0)

    def __init__(self):
        super(Paddle, self).__init__(size=(25, 200))
        with self.canvas:
            Rectangle(pos=self.pos, size=self.size)

    def initBindings(self):
        self.bind(parent=self._x)
        self.bind(parent=self._center_y)

    def _x(self, *l):
        pass

    def _center_y(self, *l):
        pass

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class LeftPlayerPaddle(Paddle):
    def __init__(self, **kwargs):
        super(LeftPlayerPaddle, self).__init__(**kwargs)

    def _x(self, *l):
        self.x = self.parent.x

    def _center_y(self, *l):
        self.center_y = self.parent.center_y


class RightPlayerPaddle(Paddle):
    def __init__(self, **kwargs):
        super(RightPlayerPaddle, self).__init__(**kwargs)

    def _x(self, *l):
        self.x = self.parent.width - self.width

    def _center_y(self, *l):
        self.center_y = self.parent.center_y


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def __init__(self):
        super(PongBall, self).__init__(size=(50, 50))
        with self.canvas:
            Ellipse(pos=self.pos, size=self.size)
        self.bind(parent=self._center)

    def _center(self, *l):
        self.center = self.parent.center

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    playerLeft = ObjectProperty(None)
    playerRight = ObjectProperty(None)

    def __init__(self):
        super(PongGame, self).__init__()

        self.ball = PongBall()
        self.playerLeft = LeftPlayerPaddle()
        self.playerRight = RightPlayerPaddle()

        with self.canvas:
            Rectangle(pos=(self.center_x - 5, 0), size=(10, self.height))

        self.add_widget(self.ball)
        self.add_widget(self.playerLeft)
        self.add_widget(self.playerRight)

        self.playerLeft.initBindings()
        self.playerRight.initBindings()

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, *args):
        self.ball.move()

        #bounce of paddles
        self.playerLeft.bounce_ball(self.ball)
        self.playerRight.bounce_ball(self.ball)

        #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        #went of to a side to score point?
        if self.ball.x < self.x:
            self.playerRight.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.playerLeft.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.playerLeft.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.playerRight.center_y = touch.y


class MainView(FloatLayout):
    game = ObjectProperty(None)

    def __init__(self, game):
        super(MainView, self).__init__()
        self.game = game
        self.add_widget(self.game)


##############
# Statechart
#
class AppStatechart(StatechartManager):
    app = ObjectProperty(None)

    def __init__(self, **kw):
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

        initialSubstateKey = 'PongGame'

        ###################
        # PongGame
        #
        class PongGame(State):
            mainView = ObjectProperty(None)
            game = ObjectProperty(None)

            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'InitializingGame'
                super(AppStatechart.
                      RootState.
                      PongGame, self).__init__(**kwargs)

            def enterState(self, context=None):
                print 'PongGame/enterState'
                self.game = PongGame()
                self.mainView = MainView(self.game)

            def exitState(self, context=None):
                print 'PongGame/exitState'

            class InitializingGame(State):
                def __init__(self, **kwargs):
                    kwargs['initialSubstateKey'] = 'ShowingGame'
                    super(AppStatechart.
                          RootState.
                          PongGame.
                          InitializingGame, self).__init__(**kwargs)

                def enterState(self, context=None):
                    print 'InitializingGame/enterState'
                    app = PongApp(self.parentState.mainView)
                    self.statechart.app = app

                def exitState(self, context=None):
                    print 'InitializingGame/exitState'

                class ShowingGame(State):
                    def __init__(self, **kwargs):
                        super(AppStatechart.
                              RootState.
                              PongGame.
                              InitializingGame.
                              ShowingGame, self).__init__(**kwargs)

                    def enterState(self, context=None):
                        print 'ShowingGame/enterState'
                        self.statechart.app.run()

                    def exitState(self, context=None):
                        print 'ShowingGame/exitState'


class PongApp(App):
    mainView = ObjectProperty(None)

    def __init__(self, mainView):
        self.mainView = mainView
        super(PongApp, self).__init__()

    def build(self):
        self.mainView.game.serve_ball()
        Clock.schedule_interval(self.mainView.game.update, 1.0 / 60.0)
        return self.mainView.game

if __name__ in ('__android__', '__main__'):
    statechart = AppStatechart()
    statechart.initStatechart()
