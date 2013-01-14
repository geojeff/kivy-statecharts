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
        if text in ['h', 'e', 'l', 'o', 'w', 'r', 'd']:
            self.app.statechart.send_event(text)

        if keycode[1] == 'escape':
            keyboard.release()

        return True


class LetterButton(Button):
    statechart = ObjectProperty(None)

    def __init__(self, statechart, letter, **kwargs):
        super(LetterButton, self).__init__(**kwargs)
        self.statechart = statechart
        self.letter = letter
        self.bind(on_press=self.letter_clicked)

    def letter_clicked(self, *args):
        print 'letter clicked', self.letter
        self.statechart.send_event(self.letter)


class AppStatechart(StatechartManager):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['trace'] = True
        kwargs['root_state_class'] = self.RootState
        super(AppStatechart, self).__init__(**kwargs)

    class RootState(State):
        initial_substate_key = 'ShowingHelloWorld'

        class ShowingHelloWorld(State):
            root = ObjectProperty(None)

            def enter_state(self, context=None):
                print 'ShowingHelloWorld/enter_state'
                self.root = self.statechart.app.root

            def exit_state(self, context=None):
                print 'ShowingHelloWorld/exit_state'

            # Utility method:
            #
            def add_label(self, letter):
                width, height = self.statechart.app.hello_world_view.size
                button_size = (20, 20)

                x = random.randint(0, width - button_size[0])
                y = random.randint(0, height - button_size[0])

                self.root.add_widget(LetterButton(self.statechart, letter,
                                                  pos=(x, y),
                                                  size=button_size,
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
        self.statechart.init_statechart()


if __name__ in ('__android__', '__main__'):
    HelloWorldApp().run()
