from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.core.window import Window


from kivy.uix.screenmanager import ScreenManager, SlideTransition

from states.showing_machine import ShowingATMachine
from states.showing_help import ShowingHelpScreen
from states.showing_pin import ShowingPinScreen
from states.showing_transaction import ShowingTransactionScreen
from states.showing_termination import ShowingTerminationScreen
from kivy_statecharts.system.state import State
from kivy_statecharts.system.statechart import StatechartManager


class AppStatechart(StatechartManager):
    app = ObjectProperty(None)

    def __init__(self, **kwargs):
        kwargs['trace'] = True
        kwargs['root_state_class'] = self.RootState
        
        super(AppStatechart, self).__init__(**kwargs)

    class RootState(State):
	
	def __init__(self, **kwargs):
            kwargs['initial_substate_key'] = 'ShowingATMachine'

            kwargs['ShowingATMachine'] = ShowingATMachine
            kwargs['ShowingHelpScreen'] = ShowingHelpScreen
	    kwargs['ShowingPinScreen'] = ShowingPinScreen
	    kwargs['ShowingTransactionScreen'] = ShowingTransactionScreen            
	    kwargs['ShowingTerminationScreen'] = ShowingTerminationScreen

	    
            super(AppStatechart.RootState, self).__init__(**kwargs)



class ATMApp(App):
    statechart = ObjectProperty(None)
    sm = ObjectProperty(None)

    def build(self):
        self.sm = ScreenManager(transition=SlideTransition())
        return self.sm

    def on_start(self):
        self.statechart = AppStatechart(app=self)
        self.statechart.init_statechart()

    def on_stop(self):
	print '\nHave a nice day !\n'
	


if __name__ in ('__android__', '__main__'):
    ATMApp().run()
