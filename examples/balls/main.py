from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty,
    ReferenceListProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.vector import Vector
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.core.window import Window
from kivy_statecharts.system.state import State
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

        self.balls = (self.ball_1,
                      self.ball_2,
                      self.ball_3,
                      self.ball_4,
                      self.ball_5)

    def _keyboard_closed(self):
        print 'My keyboard has been closed!'
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print 'The key', keycode, 'has been pressed'
        print ' - text is %r' % text
        print ' - modifiers are %r' % modifiers

        if text == 'u':
            self.app.statechart.send_event('speed_up')
        elif text == 'd':
            self.app.statechart.send_event('slow_down')
        elif keycode[1] == 'escape':
            # Keycode is composed of an integer + a string
            # If we hit escape, release the keyboard
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def serve_balls(self, vel=(4, 0)):
        for ball in self.balls:
            ball.center = self.center
            ball.velocity = vel

    def update(self, *args):
        # Move balls by their velocities.
        for ball in self.balls:
            ball.move()

        # Bounce balls off sides.
        for ball in self.balls:
            if (ball.y < self.y) or (ball.top > self.top):
                ball.velocity_y *= -1
            if (ball.x < self.x) or (ball.x > self.right):
                ball.velocity_x *= -1


class MovingBall(State):
    ball_key = StringProperty(None)
    ball = ObjectProperty(None)
    velocity_x_factor = NumericProperty(1)
    velocity_y_factor = NumericProperty(1)

    def enter_state(self, context=None):
        self.ball = getattr(self.statechart.app.mainView, self.ball_key)
        self.ball.velocity_x += self.velocity_x_factor
        self.ball.velocity_y += self.velocity_y_factor

    def exit_state(self, context=None):
        pass

    def speed_up(self, arg1=None, arg2=None):
        self.velocity_x_factor += 1
        self.velocity_y_factor += 1
        self.ball.velocity_x *= self.velocity_x_factor
        self.ball.velocity_y *= self.velocity_y_factor

    def slow_down(self, arg1=None, arg2=None):
        self.velocity_x_factor -= 1
        self.velocity_y_factor -= 1
        if self.velocity_x_factor > 0:
            self.ball.velocity_x /= self.velocity_x_factor
        if self.velocity_y_factor > 0:
            self.ball.velocity_y /= self.velocity_y_factor


##############
# Statechart
#
class AppStatechart(StatechartManager):
    def __init__(self, app, **kw):
        self.app = app
        self.trace = True
        self.root_state_class = self.RootState
        super(AppStatechart, self).__init__(**kw)

    ###########################
    # RootState of statechart
    #
    class RootState(State):
        initial_substate_key = 'ShowingBalls'

        def enter_state(self, context=None):
            print 'RootState/enter_state'
            self.statechart.app.mainView.serve_balls()
            Clock.schedule_interval(self.statechart.app.mainView.update,
                                    1.0 / 60.0)

        def exit_state(self, context=None):
            print 'RootState/exit_state'

        ##############################
        # ShowingBalls
        #
        class ShowingBalls(State):
            substates_are_concurrent = True

            def enter_state(self, context=None):
                print 'ShowingBalls/enter_state'

            def exit_state(self, context=None):
                print 'ShowingBalls/exit_state'

            class MovingBall_1(MovingBall):
                def __init__(self, **kwargs):
                    self.ball_key = 'ball_1'
                    self.velocity_x_factor = 1
                    self.velocity_y_factor = 1
                    super(AppStatechart.
                          RootState.
                          ShowingBalls.
                          MovingBall_1, self).__init__(**kwargs)

            class MovingBall_2(MovingBall):
                def __init__(self, **kwargs):
                    self.ball_key = 'ball_2'
                    self.velocity_x_factor = 2
                    self.velocity_y_factor = 2
                    super(AppStatechart.
                          RootState.
                          ShowingBalls.
                          MovingBall_2, self).__init__(**kwargs)

            class MovingBall_3(MovingBall):
                def __init__(self, **kwargs):
                    self.ball_key = 'ball_3'
                    self.velocity_x_factor = 3
                    self.velocity_y_factor = 3
                    super(AppStatechart.
                          RootState.
                          ShowingBalls.
                          MovingBall_3, self).__init__(**kwargs)

            class MovingBall_4(MovingBall):
                def __init__(self, **kwargs):
                    self.ball_key = 'ball_4'
                    self.velocity_x_factor = 4
                    self.velocity_y_factor = 4
                    super(AppStatechart.
                          RootState.
                          ShowingBalls.
                          MovingBall_4, self).__init__(**kwargs)

            class MovingBall_5(MovingBall):
                def __init__(self, **kwargs):
                    self.ball_key = 'ball_5'
                    self.velocity_x_factor = 5
                    self.velocity_y_factor = 5
                    super(AppStatechart.
                          RootState.
                          ShowingBalls.
                          MovingBall_5, self).__init__(**kwargs)


Factory.register("Ball", Ball)
Factory.register("BallsView", BallsView)


class BallsApp(App):
    statechart = ObjectProperty(None)
    mainView = ObjectProperty(None)

    def build(self):
        self.mainView = BallsView(app=self)
        return self.mainView

    def on_start(self):
        self.statechart = AppStatechart(app=self)
        self.statechart.init_statechart()


if __name__ in ('__android__', '__main__'):
    app = BallsApp()
    app.run()
