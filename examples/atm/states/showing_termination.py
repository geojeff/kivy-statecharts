
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from help import terminate_msg

from kivy.uix.screenmanager import Screen

from kivy_statecharts.system.state import State


from kivy_statecharts.system.statechart import StatechartManager


from kivy.core.image import Image
class ShowingTerminationScreen(State):
          
	    
            def enter_state(self, context=None):
                print 'ShowingTerminationScreen/enter_state'
	        
		if not 'Termination' in self.statechart.app.sm.screen_names:		

			self.app = self.statechart.app                
			
			view = BoxLayout(orientation='vertical', spacing=10)

            		toolbar = BoxLayout(size_hint=(1.0, None), height=50)

            		label = Label(text='Terminating Screen', color=[.8, .8, .8, .8], bold=True)
            		toolbar.add_widget(label)

            		button = Button(text='Return to Main Menu')
          		button.bind(on_press=self.return_to_main)
            		toolbar.add_widget(button)
		
            		label = Label(color=[.8,.1,.1,0.7],size_hint=(.3,.3),font_size="20sp",pos_hint={'x':.41,'y':.34})
			label.text = terminate_msg            		
			view.add_widget(toolbar)
			view.add_widget(label)
			
			screen = Screen(name='Termination')
            		screen.add_widget(view)
            		self.app.sm.add_widget(screen)

        	if self.app.sm.current != 'Termination':
            		self.app.sm.current = 'Termination'
            
	    def exit_state(self, context=None):
                print 'ShowingTerminationScreen/exit_state'

            
            def return_to_main(self, *args):
			       	        
			self.go_to_state('ShowingATMachine')
	    		pass
	    
    	    
