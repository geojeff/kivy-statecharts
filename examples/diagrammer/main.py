import kivy
kivy.require('1.6.0')

from kivy.app import App

from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import OptionProperty

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.animation import Animation

from statechart.statechart import AppStatechart


class RootWidget(GridLayout):

    bg = ObjectProperty(None)
    connector = ObjectProperty(None)
    connector_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.bg.bind(points=self.points_added)

    def points_added(self, *args):
        #print self.bg.points
        pass


class MainScreen(FloatLayout):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class DiagrammerApp(App):
    '''An app for drawing statechart diagrams, serving to illustrate lower
    level graphics operations and statecharts, as well as the normal higher
    level states.
    '''

    statechart = ObjectProperty(None)
    screen_manager = ObjectProperty(None)
    main_screen = ObjectProperty(None)

    drawing_area = ObjectProperty(None, allownone=True)

    points = ListProperty()
    shapes = ListProperty()
    connections = ListProperty()

    current_shape = ObjectProperty(None, allownone=True)
    current_connection = ObjectProperty(None, allownone=True)

    drawing_mode = OptionProperty('select_pick',
                                   options=('select_pick',
                                            'select_marquee',
                                            'select_node',
                                            'text_large',
                                            'text_medium',
                                            'text_small',
                                            'line_straight',
                                            'line_arc',
                                            'line_bezier',
                                            'shape_rectangle',
                                            'shape_ellipse',
                                            'shape_polygon',
                                            'state_triangle',
                                            'state_rectangle',
                                            'state_pentagon',
                                            'state_ellipse'))

    def build(self):

        self.screen_manager = ScreenManager()
        return self.screen_manager

        self.root = MainScreen(app=self)
        self.main_screen = self.root

    def on_start(self):
        self.statechart = AppStatechart(app=self)
        self.statechart.init_statechart()

    def swap_in_submenu(self, context, submenu):

        scrollview = context.parent.parent.parent
        boxlayout = context.parent.parent

        # Add the submenu to the BoxLayout in the menu scrollview. First check
        # to see if a submenu is present, and remove it, before adding the
        # submenu to swap in.

        if len(boxlayout.children) == 2:
            boxlayout.remove_widget(boxlayout.children[0])

        boxlayout.add_widget(submenu)

        Animation(scroll_x=1, d=.5).start(scrollview)


if __name__ in ('__main__'):
    DiagrammerApp().run()
