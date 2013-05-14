from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.listview import ListView

from help import help_attr

from kivy.uix.screenmanager import Screen

from kivy_statecharts.system.state import State
from kivy.properties import ObjectProperty

from kivy_statecharts.system.statechart import StatechartManager

class ShowingHelpScreen(State):
            #root = ObjectProperty(None)

            def enter_state(self, context=None):
                print 'ShowingHelpScreen/enter_state'
		if not 'Help' in self.statechart.app.sm.screen_names:		

			self.app = self.statechart.app                
			#self.root = self.statechart.app.root
			view = BoxLayout(orientation='vertical', spacing=10)

            		toolbar = BoxLayout(size_hint=(1.0, None), height=50)

            		label = Label(text='Help', color=[.8, .8, .8, .8], bold=True)
            		toolbar.add_widget(label)
			
			Help = FloatLayout(size=(600,600))
			help_content = Label(color=[.6,.3,.1,1],font_size="18sp")
			help_content.text = help_attr			
			
			
			Help.add_widget(help_content)			            		

			button = Button(text='Machine')
          		button.bind(on_press=self.go_to_machine)
            		toolbar.add_widget(button)

            		

            		view.add_widget(toolbar)
			view.add_widget(Help)
			screen = Screen(name='Help')
            		screen.add_widget(view)
            		self.app.sm.add_widget(screen)

        	if self.app.sm.current != 'Help':
            		self.app.sm.current = 'Help'
            
		
	    def exit_state(self, context=None):
                print 'ShowingHelpScreen/exit_state'

            # Utility method:
            #
            def go_to_machine(self, *args):
        	        self.go_to_state('ShowingATMachine')

    	    
