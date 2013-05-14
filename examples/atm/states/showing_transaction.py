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

from functools import partial

class ShowingTransactionScreen(State):
	    
            def enter_state(self, context=None):
                print 'ShowingTransactionScreen/enter_state'
		if not 'Transaction' in self.statechart.app.sm.screen_names:		

			self.app = self.statechart.app                
			
			self.view = BoxLayout(orientation='vertical', spacing=10)

            		toolbar = BoxLayout(size_hint=(1.0, None), height=50)

            		label = Label(text='Transaction', color=[.8, .8, .8, .8], bold=True)
            		toolbar.add_widget(label)

            		button = Button(text='Save and Exit')
          		button.bind(on_press=self.go_to_terminate)
            		toolbar.add_widget(button)

		

            		self.trans_option = FloatLayout(size=(600,600))
			
			terminate = Button(text='Terminate',pos_hint={'x':.79,'y':-.99},size_hint=(.2,.13),background_color=[.8,.2,.3,1])
			terminate.bind(on_press=self.Close_App) 
	
			self.Deposit = Button(text='Deposit',pos_hint={'x':.01,'y':.77},size_hint=(.33,.15))
			self.Withdraw = Button(text='Withdraw',pos_hint={'x':.34,'y':.77},size_hint=(.33,.15))
			self.Slip = Button(text='Slip',pos_hint={'x':.67,'y':.77},size_hint=(.33,.15))
			

			self.Deposit.bind(on_press=self.Deposit_Amount)
			self.Withdraw.bind(on_press=self.Withdraw_Amount)
			self.Slip.bind(on_press=self.Show_Info)			

			self.trans_option.add_widget(self.Deposit)
			self.trans_option.add_widget(terminate)
			

			self.dep_amount = FloatLayout(size=(600,600))			
			self.with_amount = FloatLayout(size=(600,600))		
			self.slip = FloatLayout(size=(600,600))		

            		self.view.add_widget(toolbar)
			self.view.add_widget(self.trans_option)
			screen = Screen(name='Transaction')
            		screen.add_widget(self.view)
            		self.app.sm.add_widget(screen)
			
			self.fetch_db_data()
			self.Deposit_Amount()

        	if self.app.sm.current != 'Transaction':
            		self.app.sm.current = 'Transaction'
            
	    def exit_state(self, context=None):
                print 'ShowingTransactionScreen/exit_state'
		self.commit_all_to_db()
           

	    def fetch_db_data(self, *args):
			self.a = ShowingATMachine()
			if (self.a.validation == 1):			
				self.get_name = str(self.a.Name.text)
				self.get_pass = str(self.a.Password.text)
			elif (self.a.available == 1):
				self.get_name = str(self.a.L_Name.text)
				self.get_pass = str(self.a.L_Password.text)
							
			conn = sqlite3.connect('./account/'+ self.get_name +'.db')
			with conn:
				c = conn.cursor()

				for row in c.execute("SELECT * from account where pass = '%s'" % self.get_pass):
					self.post_name =  row[0]   				
					self.post_type  = row[1]
					self.post_password = row[2]
    					self.post_balance = float(row[3])


	    def Deposit_Amount(self, *args):
			self.view.remove_widget(self.with_amount)
			self.view.remove_widget(self.slip)

			self.trans_option.remove_widget(self.Deposit)
			self.trans_option.remove_widget(self.Withdraw)
			self.trans_option.remove_widget(self.Slip)
			
			self.trans_option.add_widget(self.Withdraw)
			self.trans_option.add_widget(self.Slip)	
			self.dep_amount = FloatLayout(size=(600,600))		
			
			Dep_Label = Label(text='Deposit',size_hint=(.3,.15),pos_hint={'x':.01,'y':1.83},font_size="21dp")

			self.Dep_Amount = TextInput(hint_text='Enter amount to be deposited',size_hint=(.3,.15),pos_hint={'x':.01,'y':1.5},multiline=False)
			self.Dep_Amount.bind(on_text_validate=self.commit_deposit)

			self.Deposit_Label = Label(text='',size_hint=(.2,.2),pos_hint={'x':.06,'y':1.3},color=[.2,.8,.2,1],font_size="18dp")

			Dep_Commit = Button(text='Commit',size_hint=(.2,.15),pos_hint={'x':.06,'y':1.1})
			Dep_Commit.bind(on_press=self.commit_deposit)			

			self.dep_amount.add_widget(self.Dep_Amount)
			self.dep_amount.add_widget(Dep_Label)
			self.dep_amount.add_widget(Dep_Commit)
			self.dep_amount.add_widget(self.Deposit_Label)
			
			self.view.add_widget(self.dep_amount)
			return self.view

	    def Withdraw_Amount(self, *args):
			self.view.remove_widget(self.dep_amount)
			self.view.remove_widget(self.slip)

			self.trans_option.remove_widget(self.Deposit)
			self.trans_option.remove_widget(self.Withdraw)
			self.trans_option.remove_widget(self.Slip)
			
			self.trans_option.add_widget(self.Deposit)
			self.trans_option.add_widget(self.Slip)
			self.with_amount = FloatLayout(size=(600,600))	
			
			Withdraw_Label = Label(text='Withdraw',size_hint=(.3,.15),pos_hint={'x':.34,'y':1.83},font_size="21dp")

			self.Withdraw_Amount = TextInput(hint_text='Enter amount to be withdrawn',size_hint=(.3,.15),pos_hint={'x':.34,'y':1.5},multiline=False)
			self.Withdraw_Amount.bind(on_text_validate=self.commit_withdraw)			

			Withdraw_Commit = Button(text='Commit',size_hint=(.2,.15),pos_hint={'x':.4,'y':1.1})
			Withdraw_Commit.bind(on_press=self.commit_withdraw)			
			
			self.Withdraw_Label = Label(text='',size_hint=(.2,.2),pos_hint={'x':.4,'y':1.3},color=[.8,.2,.2,1],font_size="18dp")

			self.with_amount.add_widget(self.Withdraw_Amount)
			self.with_amount.add_widget(Withdraw_Label)
			self.with_amount.add_widget(Withdraw_Commit)
			self.with_amount.add_widget(self.Withdraw_Label)
			
			self.view.add_widget(self.with_amount)
			return self.view

	    def Show_Info(self, *args):
			self.view.remove_widget(self.dep_amount)
			self.view.remove_widget(self.with_amount)

			self.trans_option.remove_widget(self.Deposit)
			self.trans_option.remove_widget(self.Withdraw)
			self.trans_option.remove_widget(self.Slip)

			self.trans_option.add_widget(self.Deposit)
			self.trans_option.add_widget(self.Withdraw)

			self.slip = FloatLayout(size=(600,600))

			show_info_Label = Label(text='Show_Info',size_hint=(.3,.15),pos_hint={'x':.67,'y':1.83},font_size="21dp")
			show_info = Label(text="HI",pos_hint={'x':.64,'y':1.0},size_hint=(.3,.5),color=[.2,.2,.8,1],font_size="21dp")
			self.slip.add_widget(show_info)
			self.slip.add_widget(show_info_Label)

			self.view.add_widget(self.slip) 
			show_info.text = 'Name : ' + str(self.post_name) + '\n\nType : ' + str(self.post_type) + '\n\nPassword : ' + str(self.post_password) + '\n\nBalance : ' + str(self.post_balance) + '\n\nPin : Hidden'
			
			
			return self.view

	    def commit_deposit(self, *args):
			if (self.Dep_Amount.text!=''):
				self.post_balance = str(float(self.post_balance) + float(self.Dep_Amount.text))
				self.Dep_Amount.text = ''
				self.Deposit_Label.text = 'Amount Deposited'
			else:
				self.Deposit_Label.text = 'Please enter the amount'
			return self.Dep_Amount.text

	    def commit_withdraw(self, *args):
			if (self.Withdraw_Amount.text!=''):
				self.post_balance = str(float(self.post_balance) - float(self.Withdraw_Amount.text))
				self.Withdraw_Amount.text =''
				self.Withdraw_Label.text = 'Amount Withdrawn'
			else:
				self.Withdraw_Label.text = 'Please enter the amount'
			return self.Withdraw_Amount.text

	    def commit_all_to_db(self, *args):
			
			conn = sqlite3.connect('./account/'+ self.get_name + '.db')
			
			with conn:
				c = conn.cursor()
				c.execute("UPDATE account SET bal='%s'" % self.post_balance)
				conn.commit()
			conn.close()			

            def go_to_terminate(self, *args):
        	        self.go_to_state('ShowingTerminationScreen') 		
			

	    def Close_App(self, *args):
			#ATMApp().stop() something like this might end the App
	    		pass
    	    
