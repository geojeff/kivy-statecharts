from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

from kivy.properties import ListProperty, ObjectProperty

from kivy_statecharts.system.state import State
from kivy.uix.screenmanager import Screen



class ShowingDrawingAreaScreen(State):
    ''' App's drawing area'''

    points = ListProperty()
    shapes = ListProperty()
    connections = ListProperty()
    
    connecting_shape = ObjectProperty(None, allownone=True)
    moving_shape = ObjectProperty(None, allownone=True)
	
    def enter_state(self, context=None):

        if not 'DrawingArea' in self.statechart.app.sm.screen_names:
            
			# Convenience references:
            self.app = self.statechart.app
            view = BoxLayout(orientation='vertical', spacing=10)

            toolbar = BoxLayout(size_hint=(1.0, None), height=50)

            button = Button(text='Main')
            button.bind(on_press=self.go_to_main)
            toolbar.add_widget(button)

            label = Label(text='Drawing Area', color=[.8, .8, .8, .8], bold=True)
            toolbar.add_widget(label)
            drawing_area = FloatLayout(size=(800,800))
            draw_label = Label(text='drawing goes here',color=[.8,.2,.2,1])
            drawing_area.add_widget(draw_label)
            
            view.add_widget(toolbar)
            view.add_widget(drawing_area)
            #self.statechart.go_to_state(self.DrawingArea)
			
            screen = Screen(name='DrawingArea')
            screen.add_widget(view)
            self.app.sm.add_widget(screen)

        if self.app.sm.current != 'DrawingArea':
            self.app.sm.current = 'DrawingArea'
			
    def exit_state(self, context=None):
        pass
		
    def go_to_main(self, *args):
        self.go_to_state('ShowingMainScreen')
		