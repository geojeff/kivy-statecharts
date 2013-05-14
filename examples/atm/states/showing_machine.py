import os
import sqlite3

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.listview import ListView

from kivy.uix.screenmanager import Screen

from kivy_statecharts.system.state import State
from kivy.properties import ObjectProperty

from kivy_statecharts.system.statechart import StatechartManager

from functools import partial

class ShowingATMachine(State):
            root = ObjectProperty(None)
	    L_Name = TextInput(text='',hint_text='Enter Name',pos_hint={'x':.55,'y':1.5},multiline=False,size_hint=(.4,.13))
	    L_Password =TextInput(hint_text='Enter password',pos_hint={'x':.55,'y':1.2},multiline=False,size_hint=(.4,.13),password=True)	    
	    
	    Pin = TextInput(text='',hint_text='Enter valid pin here (digits only)',pos_hint={'x':.1,'y':.9},multiline=False,size_hint=(.4,.13),password=True)	    

	    Name = TextInput(text='',hint_text='Enter Name',pos_hint={'x':.1,'y':1.5},multiline=False,size_hint=(.4,.13))
	    Password = TextInput(hint_text='Enter password',pos_hint={'x':.1,'y':1.2},multiline=False,size_hint=(.4,.13),password=True)
	    def __init__(self, **kwargs):
		self.validation = 0		
		self.available = 0
				
		self.update_info()
		self.update_login()
        	super(ShowingATMachine, self).__init__(**kwargs)

            def enter_state(self, context=None):
                print 'ShowingATMachine/enter_state'
		if not 'Machine' in self.statechart.app.sm.screen_names:		
			self.validation = 1
			self.app = self.statechart.app                
			
			self.view = BoxLayout(orientation='vertical', spacing=10)

            		toolbar = BoxLayout(size_hint=(1.0, None), height=50)

            		label = Label(text='Machine', color=[.8, .8, .8, .8], bold=True)
            		toolbar.add_widget(label)

            		button = Button(text='Help',size_hint=(0.3,1.0))
          		button.bind(on_press=self.go_to_help)
            		toolbar.add_widget(button)

            		self.reading_card = FloatLayout(size=(600,600))
			self.write_card_info = Button(text='FILL',pos_hint={'x':.01,'y':.67},size_hint=(.5,.17))
			self.write_card_info.bind(on_press=self.fill_cardinfo)
			self.have_account = Button(text='Login',pos_hint={'x':.5,'y':.67},size_hint=(.5,.17))
			self.have_account.bind(on_press=self.login_account)
		

			self.signup = FloatLayout(size=(600,600))			
			self.login = FloatLayout(size=(600,600))			

            		self.view.add_widget(toolbar)
			self.view.add_widget(self.reading_card)
			screen = Screen(name='Machine')
            		screen.add_widget(self.view)
            		self.app.sm.add_widget(screen)
	
			self.fill_cardinfo()

        	if self.app.sm.current != 'Machine':
            		self.app.sm.current = 'Machine'
            
	    def exit_state(self, context=None):
                print 'ShowingATMachine/exit_state'

            
            def go_to_help(self, *args):
        	        self.go_to_state('ShowingHelpScreen')
	    def got_to_pin(self,*args):
			self.go_to_state('ShowingPinScreen')
	    def fill_cardinfo(self, *args):
			
			self.view.remove_widget(self.login)
			self.reading_card.remove_widget(self.write_card_info)
			self.login.remove_widget(self.L_Name)
			self.login.remove_widget(self.L_Password)

			self.reading_card.add_widget(self.have_account)
			self.signup = FloatLayout(size=(600,600))

			fill_Label = Label(text='Fill',pos_hint={'x':.01,'y':1.73},size_hint=(.5,.17),font_size="21dp")
			
			Type = TextInput(hint_text='Enter Account Type',pos_hint={'x':.1,'y':1.35},multiline=False,size_hint=(.4,.13))
			
			Balance = TextInput(hint_text='Enter current Balance (must be integar/float)',pos_hint={'x':.1,'y':1.05},multiline=False,size_hint=(.4,.13))

			Proceed = Button(text="Proceed",background_color=[0.2,0.2,0.8,1],pos_hint={'x':.1,'y':.5},size_hint=(.2,.13))
			Proceed.bind(on_press=partial(self.check_validation,self.Name,Type,self.Password,Balance,self.Pin))
			
			self.signup.add_widget(self.Name)
			self.signup.add_widget(Type)
			self.signup.add_widget(self.Password)
			self.signup.add_widget(self.Pin)
			self.signup.add_widget(Balance)
			self.signup.add_widget(Proceed)	
			self.signup.add_widget(fill_Label)
		
			self.view.add_widget(self.signup)
			
			return self.view
	    def login_account(self, *args):

			self.view.remove_widget(self.signup)
			self.reading_card.remove_widget(self.have_account)
			self.reading_card.add_widget(self.write_card_info)
			self.signup.remove_widget(self.Name)
			self.signup.remove_widget(self.Password)
			self.signup.remove_widget(self.Pin)
			
			
			login_Label = Label(text='Login',pos_hint={'x':.5,'y':1.73},size_hint=(.5,.17),font_size="21dp")

			
			self.L_Name.bind(on_text_validation=self.update_info)
			

			_Proceed = Button(text="Proceed",background_color=[0.2,0.2,0.8,1],pos_hint={'x':.55,'y':1.0},size_hint=(.2,.13))
			_Proceed.bind(on_press=partial(self.check_user_availability,self.L_Name,self.L_Password))			
			
			self.login.add_widget(self.L_Name)
			self.login.add_widget(self.L_Password)
			self.login.add_widget(_Proceed)
			self.login.add_widget(login_Label)

			self.view.add_widget(self.login)
			return self.view

	    def check_validation(self, name, typ, pas, bal, pin,*args):
			self.update_info()
			if (name.text !="" and typ.text!="" and pas.text!="" and bal.text!=""):
				
				file = name.text
				file = file + '.db'
				if not os.path.exists('account'):
					os.makedirs('account')
				conn = sqlite3.connect('./account/'+file)
				with conn:
					c = conn.cursor()

					c.execute('''CREATE TABLE account (name text,type text,pass text,bal real,pin integar)''')

					c.execute("INSERT INTO account values (?,?,?,?,?)",(name.text,typ.text,pas.text,bal.text,pin.text))
				
					conn.commit()
				conn.close()
				self.go_to_state('ShowingPinScreen')

	    def check_user_availability(self,name,pas, *args):
			self.update_login()
			if (name.text !="" and pas.text!=""):
				conn = sqlite3.connect('./account/'+ name.text +'.db')
				with conn:
					c = conn.cursor()

					for row in c.execute("SELECT * from account"):
    						r  =row[0]
    						q = row[2]
    						if (name.text==r and pas.text==q):
							self.go_to_state('ShowingPinScreen')
							break

	    def update_info(self, *args):
			
			if (self.Name.text!=''):
				self.validation = 1
				

	    def update_login(self, *args):
			
			if (self.L_Name.text!=''):
				self.available = 1
				
