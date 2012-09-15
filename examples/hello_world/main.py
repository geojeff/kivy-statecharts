from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.core.window import Window

from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager

import random


class HelloWorldView(Widget):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(HelloWorldView, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if text == 'h':
            self.app.statechart.sendEvent('h')
        elif text == 'e':
            self.app.statechart.sendEvent('e')
        elif text == 'l':
            self.app.statechart.sendEvent('l')
        elif text == 'o':
            self.app.statechart.sendEvent('o')
        elif text == 'w':
            self.app.statechart.sendEvent('w')
        elif text == 'r':
            self.app.statechart.sendEvent('r')
        elif text == 'd':
            self.app.statechart.sendEvent('d')

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        return True


class LetterButton(Button):
    statechart = ObjectProperty(None)

    def __init__(self, letter, statechart, **kwargs):
        self.letter = letter
        self.statechart = statechart
        super(LetterButton, self).__init__(**kwargs)
        self.bind(on_press=self.letter_clicked)

    def letter_clicked(self, *args):
        self.statechart.sendEvent(self.letter)


class AppStatechart(StatechartManager):
    app = ObjectProperty(None)

    def __init__(self, **kw):
        self.trace = True
        self.rootStateClass = self.RootState
        super(AppStatechart, self).__init__(**kw)

    class RootState(State):
        initialSubstateKey = 'ShowingHelloWorld'

        class ShowingHelloWorld(State):
            root = ObjectProperty(None)

            def enterState(self, context=None):
                print 'ShowingHelloWorld/enterState'
                self.root = self.statechart.app.root

            def exitState(self, context=None):
                print 'ShowingHelloWorld/exitState'

            # Utility method:
            #
            def add_label(self, letter):
                width, height = self.statechart.app.hello_world_view.size
                margin = 40

                x = random.randint(0, width - margin)
                y = random.randint(margin, height )

                self.root.add_widget(Button(pos=(x, y),
                                            size=(20, 20),
                                            text=letter))

            # Action methods:
            #
            def h(self, *args):
                self.add_label('h')

            def e(self, *args):
                self.add_label('e')

            def l(self, *args):
                self.add_label('l')

            def o(self, *args):
                self.add_label('o')

            def w(self, *args):
                self.add_label('w')

            def r(self, *args):
                self.add_label('r')

            def d(self, *args):
                self.add_label('d')


class HelloWorldApp(App):
    statechart = ObjectProperty(None)
    hello_world_view = ObjectProperty(None)

    def build(self):
        self.hello_world_view = HelloWorldView(app=self)
        return self.hello_world_view

    def on_start(self):
        self.statechart = AppStatechart(app=self)
        self.statechart.initStatechart()


if __name__ in ('__android__', '__main__'):
    HelloWorldApp().run()
