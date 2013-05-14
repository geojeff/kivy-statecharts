import sqlite3
from states.showing_machine import ShowingATMachine


from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.listview import ListView

from kivy.uix.screenmanager import Screen

from kivy_statecharts.system.state import State
from kivy.properties import ObjectProperty


from kivy_statecharts.system.statechart import StatechartManager

class ShowingPinScreen(State):
            

            def enter_state(self, context=None):
                print 'ShowingPinScreen/enter_state'
		if not 'Pin' in self.statechart.app.sm.screen_names:		

			self.app = self.statechart.app                
			
			view = BoxLayout(orientation='vertical', spacing=10)

            		toolbar = BoxLayout(size_hint=(1.0, None), height=50)

            		label = Label(text='Pin', color=[.8, .8, .8, .8], bold=True)
            		toolbar.add_widget(label)

            		button = Button(text='Back_to_Machine')
          		button.bind(on_press=self.go_to_machine)
            		toolbar.add_widget(button)

            		Pin_read = FloatLayout(size=(600,600))
			self.pin_input = TextInput(hint_text='Enter your valid pin here __should be digits to proceed__',size_hint=(.6,.1),pos_hint={'x':.2,'y':.65},multiline=False)
			Proceed_button = Button(text='Proceed',background_color=[0.18,0.8,0.18,1],pos_hint={'x':.44,'y':.2},size_hint=(.14,.1))			
			
			
			self.invalid_pin = Label(text='',color=[.6,.3,.5,1],size_hint=(.2,.2),pos_hint={'x':.4,'y':.44},font_size="19sp")
			
			self.pin_input.bind(on_text_validate=self.check_validation)
			Proceed_button.bind(on_press=self.check_validation)
					

			Pin_read.add_widget(Proceed_button)
			
			Pin_read.add_widget(self.pin_input)
			Pin_read.add_widget(self.invalid_pin)

            		view.add_widget(toolbar)
			view.add_widget(Pin_read)
			screen = Screen(name='Pin')
            		screen.add_widget(view)
            		self.app.sm.add_widget(screen)

        	if self.app.sm.current != 'Pin':
            		self.app.sm.current = 'Pin'
            
	    def exit_state(self, context=None):
                print 'ShowingPinScreen/exit_state'

           
            def go_to_machine(self, *args):
        	        self.go_to_state('ShowingATMachine')
	    def check_validation(self, *args):
			if (self.pin_input.text!='' and self.pin_input.text.isdigit()):
				obj = ShowingATMachine()
				if (obj.validation == 1 and self.pin_input.text==obj.Pin.text):
					self.go_to_state('ShowingTransactionScreen')
				elif (obj.available == 1):
					conn = sqlite3.connect('./account/'+ obj.L_Name.text + '.db')
			
					with conn:
						c = conn.cursor()
						for r in c.execute("SELECT pin from account where name='%s' and pass='%s'" % (obj.L_Name.text, obj.L_Password.text)):
							get_pin = r[0]
						
							if (self.pin_input.text==str(get_pin)):
								self.invalid_pin.text = ''
								self.pin_input.text = ''
								self.go_to_state('ShowingTransactionScreen')
								break
							else:
								self.invalid_pin.text= 'Invalid Pin'
				else:
					self.invalid_pin.text= 'Invalid Pin'

	    
    	    
