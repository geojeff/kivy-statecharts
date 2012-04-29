import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, ListProperty, BooleanProperty
from kivy.vector import Vector
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse

from random import randint, random

from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import Statechart
from kivy_statechart.system.statechart import StatechartManager

import inspect


class ThrusterGroupControl(Widget):
    # The control location is set in the kv file initially. The pos value is set based
    # on this and the pulsation (ellipse size) value, so that the control stays centered.
    location_x = NumericProperty(0)
    location_y = NumericProperty(0)
    location = ReferenceListProperty(location_x, location_y)

    # For pulsation, we alternate between the original size and the pulsation size.
    alternator = BooleanProperty(False)
    
    # The pulsation is the amount of size increase over the normal size. When off,
    # a thruster's pulsation is zero, and it paints as normal.
    pulsation_x = NumericProperty(10)
    pulsation_y = NumericProperty(10)
    pulsation = ReferenceListProperty(pulsation_x, pulsation_y)
    
    def pulsate(self):
        if self.alternator:
            self.pos = (self.location_x+self.size[0]/2-self.pulsation_x/2, self.location_y+self.size[1]/2-self.pulsation_y/2)
            self.size = (self.pulsation_x, self.pulsation_y)
            self.alternator = False
        else:
            self.size = (10,10)
            self.pos = (self.location_x, self.location_y)
            self.alternator = True

    def pulsate_more(self):
        self.pulsation_x = self.pulsation_x+1
        self.pulsation_y = self.pulsation_y+1

    def pulsate_less(self):
        self.pulsation_x = self.pulsation_x-1 if self.pulsation_x > 1 else 1
        self.pulsation_y = self.pulsation_y-1 if self.pulsation_y > 1 else 1

    def slide_back_and_forth_more(self):
        self.pulsate_more()

    def slide_back_and_forth_less(self):
        self.pulsate_less()

    def slide_in_and_out_more(self):
        self.pulsate_more()

    def slide_in_and_out_less(self):
        self.pulsate_less()

    def slide_up_and_down_more(self):
        self.pulsate_more()

    def slide_up_and_down_less(self):
        self.pulsate_less()

class MotionControlWidget(Widget):
    statechart = ObjectProperty(None)
    control_id = StringProperty('')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # if the touch is colliding to our widget, let's grab it.
            touch.grab(self)
        
            #with self.canvas:
                #Color(1, 1, 0)
                #d = 10.
                #Ellipse(pos=(touch.x - d/2, touch.y - d/2), size=(d, d))
    
            return True

    def on_touch_up(self, touch):
        if touch.grab_current is self:
    
            touch.ungrab(self)

            self.statechart.sendEvent(self.control_id)
    
            return True

class RotationalMotionControl(MotionControlWidget):
    pass

class TranslationalMotionControl(MotionControlWidget):
    pass


class ShuttleControlView(Widget):
    app = ObjectProperty(None)
    background_image = ObjectProperty(None)

    thruster_group_1 = ObjectProperty(None)
    thruster_group_2 = ObjectProperty(None)
    thruster_group_3 = ObjectProperty(None)
    thruster_group_4 = ObjectProperty(None)
    thruster_group_5 = ObjectProperty(None)
    thruster_group_6 = ObjectProperty(None)
    thruster_group_7 = ObjectProperty(None)
    thruster_group_8 = ObjectProperty(None)
    thruster_group_9 = ObjectProperty(None)
    thruster_group_10 = ObjectProperty(None)
    thruster_group_11 = ObjectProperty(None)
    thruster_group_12 = ObjectProperty(None)
    thruster_group_13 = ObjectProperty(None)
    thruster_group_14 = ObjectProperty(None)

    yaw_plus = ObjectProperty(None)
    yaw_minus = ObjectProperty(None)
    pitch_plus = ObjectProperty(None)
    pitch_minus = ObjectProperty(None)
    roll_plus = ObjectProperty(None)
    roll_minus = ObjectProperty(None)
    
    translate_x_plus = ObjectProperty(None)
    translate_x_minus = ObjectProperty(None)
    translate_y_plus = ObjectProperty(None)
    translate_y_minus = ObjectProperty(None)
    translate_z_plus = ObjectProperty(None)
    translate_z_minus = ObjectProperty(None)

    def __init__(self, app, **kwargs):
        self.app = app
        super(ShuttleControlView, self).__init__(**kwargs) 
        #self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        #self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print 'My keyboard has been closed!'
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print 'The key', keycode, 'has been pressed'
        print ' - text is %r' % text
        print ' - modifiers are %r' % modifiers

        if keycode[1] == 's':
            self.app.statechart.sendEvent('pulsate')
        elif keycode[1] == 'escape':
            # Keycode is composed of an integer + a string
            # If we hit escape, release the keyboard
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def initialize_thruster_groups(self, pulsation=(10,10)):
        for thruster_group in (self.thruster_group_1, self.thruster_group_2, self.thruster_group_3, self.thruster_group_4, self.thruster_group_5, self.thruster_group_6, self.thruster_group_7, self.thruster_group_8, self.thruster_group_9, self.thruster_group_10, self.thruster_group_11, self.thruster_group_12, self.thruster_group_13, self.thruster_group_14):
            # Set a default pulsation value.
            thruster_group.pulsation = pulsation

            # The initial value of location_x and location_y are taken from the pos set in the kv file.
            thruster_group.location_x = thruster_group.pos[0] - thruster_group.size[0]/2
            thruster_group.location_y = thruster_group.pos[1] - thruster_group.size[1]/2

    def set_statechart_in_motion_controls(self, statechart):
        controls = { 'yaw_plus': self.yaw_plus, 
                     'yaw_minus': self.yaw_minus, 
                     'pitch_plus': self.pitch_plus, 
                     'pitch_minus': self.pitch_minus, 
                     'roll_plus': self.roll_plus, 
                     'roll_minus': self.roll_minus, 
                     'translate_x_plus': self.translate_x_plus, 
                     'translate_x_minus': self.translate_x_minus, 
                     'translate_y_plus': self.translate_y_plus, 
                     'translate_y_minus': self.translate_y_minus, 
                     'translate_z_plus': self.translate_z_plus, 
                     'translate_z_minus': self.translate_z_minus }
        for control_id in controls:
            setattr(controls[control_id], 'control_id', control_id)
            setattr(controls[control_id], 'statechart', statechart)

    def update(self, *args):
        # Wiggle thruster_groups by their pulsate amounts.
        for thruster_group in (self.thruster_group_1, self.thruster_group_2, self.thruster_group_3, self.thruster_group_4, self.thruster_group_5, self.thruster_group_6, self.thruster_group_7, self.thruster_group_8, self.thruster_group_9, self.thruster_group_10, self.thruster_group_11, self.thruster_group_12, self.thruster_group_13, self.thruster_group_14):
            thruster_group.pulsate()
        

class ThrusterControlState(State):
    thruster_group = ObjectProperty(None)
    thruster_ids = ListProperty([])

    def enterState(self, context=None):
        pass
            
    def exitState(self, context=None):
        pass

    def setThrusterCount(self):
        thruster_ids = []
        for item in dir(self):
            if inspect.isclass(item) and issubclass(State) and item.__name__.startswith('AdjustingThruster_'):
                thruster_ids.append(item.__name__[-3:])
        self.thruster_ids = thruster_ids

    def speed_up(self, arg1=None, arg2=None):
        self.thruster_group.pulsation_x += len(self.thrusters)
        self.thruster_group.pulsation_y += len(self.thrusters)

    def slow_down(self, arg1=None, arg2=None):
        self.thruster_group.pulsation_x -= len(self.thrusters)
        self.thruster_group.pulsation_y -= len(self.thrusters)

    def zero_out(self, arg1=None, arg2=None):
        self.thruster_group.pulsation_x = 0
        self.thruster_group.pulsation_y = 0


##############
# Statechart
#
class AppStatechart(StatechartManager):
    def __init__(self, app, **kw):
        self.app = app
        self.trace = True
        self.rootStateClass = self.RootState
        super(AppStatechart, self).__init__(**kw)

    ###########################
    # RootState of statechart
    #
    class RootState(State):
        def __init__(self, **kwargs):
            kwargs['initialSubstateKey'] = 'ShowingThrusterControls'
            super(AppStatechart.RootState, self).__init__(**kwargs)
        
        def enterState(self, context=None):
            print 'RootState/enterState'
            self.statechart.app.mainView.initialize_thruster_groups()
            self.statechart.app.mainView.set_statechart_in_motion_controls(self.statechart)
            Clock.schedule_interval(self.statechart.app.mainView.update, 1.0/60.0)
                        
        def exitState(self, context=None):
            print 'RootState/exitState'

        ##############################
        # ShowingThrusterControls
        #
        class ShowingThrusterControls(State):
            def __init__(self, **kwargs):
                kwargs['substatesAreConcurrent'] = True
                super(AppStatechart.RootState.ShowingThrusterControls, self).__init__(**kwargs)
        
            def enterState(self, context=None):
                print 'ShowingThrusterControls/enterState'
                        
            def exitState(self, context=None):
                print 'ShowingThrusterControls/exitState'

            class AdjustingThrusterGroup_1(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_1, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_1'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def translate_x_minus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_back_and_forth_less()

                class AdjustingThruster_F1F(State):
                    pass

                class AdjustingThruster_F2F(State):
                    pass

                class AdjustingThruster_F3F(State):
                    pass

            class AdjustingThrusterGroup_2(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_2, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_2'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def yaw_plus(self, arg1=None, arg2=None):
                    print 'yaw_plus firing'
                    self.thruster_group.pulsate_more()

                def translate_y_plus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_up_and_down_more()

                class AdjustingThruster_F1L(State):
                    pass

                class AdjustingThruster_F3L(State):
                    pass

            class AdjustingThrusterGroup_3(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_3, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_3'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def yaw_minus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_less()

                def translate_y_minus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_up_and_down_less()

                class AdjustingThruster_F2R(State):
                    pass

                class AdjustingThruster_F4R(State):
                    pass

            class AdjustingThrusterGroup_4(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_4, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_4'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def pitch_minus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_less()

                def translate_z_plus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_in_and_out_more()

                class AdjustingThruster_F1U(State):
                    pass

                class AdjustingThruster_F2U(State):
                    pass

                class AdjustingThruster_F3U(State):
                    pass

            class AdjustingThrusterGroup_5(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_5, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_5'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def pitch_plus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_more()

                def translate_z_minus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_in_and_out_less()

                class AdjustingThruster_F5R(State):
                    pass

                class AdjustingThruster_F2D(State):
                    pass

                class AdjustingThruster_F4D(State):
                    pass

            class AdjustingThrusterGroup_6(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_6, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_6'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def roll_plus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_more()

                def translate_z_minus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_in_and_out_less()

                class AdjustingThruster_F1D(State):
                    pass

                class AdjustingThruster_F3D(State):
                    pass

                class AdjustingThruster_F5L(State):
                    pass

            class AdjustingThrusterGroup_7(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_7, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_7'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def pitch_minus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_less()

                def translate_x_plus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_back_and_forth_more()

                class AdjustingThruster_R1A(State):
                    pass

                class AdjustingThruster_R3A(State):
                    pass

            class AdjustingThrusterGroup_8(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_8, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_8'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def pitch_plus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_more()

                def translate_x_plus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_back_and_forth_more()

                class AdjustingThruster_L1A(State):
                    pass

                class AdjustingThruster_L3A(State):
                    pass

            class AdjustingThrusterGroup_9(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_9, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_9'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def yaw_minus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_less()

                def translate_y_plus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_up_and_down_more()

                class AdjustingThruster_L1L(State):
                    pass

                class AdjustingThruster_L2L(State):
                    pass

                class AdjustingThruster_L3L(State):
                    pass

                class AdjustingThruster_L4L(State):
                    pass

            class AdjustingThrusterGroup_10(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_10, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_10'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def yaw_plus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_more()

                def translate_y_minus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_up_and_down_less()

                class AdjustingThruster_R1R(State):
                    pass

                class AdjustingThruster_R2R(State):
                    pass

                class AdjustingThruster_R3R(State):
                    pass

                class AdjustingThruster_R4R(State):
                    pass

            class AdjustingThrusterGroup_11(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_11, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_11'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def pitch_plus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_more()

                def roll_minus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_less()

                def translate_z_plus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_in_and_out_more()

                class AdjustingThruster_L1U(State):
                    pass

                class AdjustingThruster_L2U(State):
                    pass

                class AdjustingThruster_L4U(State):
                    pass

            class AdjustingThrusterGroup_12(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_12, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_12'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def pitch_plus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_more()

                def roll_plus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_more()

                def translate_z_plus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_in_and_out_more()

                class AdjustingThruster_R1U(State):
                    pass

                class AdjustingThruster_R2U(State):
                    pass

                class AdjustingThruster_R4U(State):
                    pass

            class AdjustingThrusterGroup_13(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_13, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_13'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def pitch_minus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_less()

                def roll_plus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_more()

                def translate_z_minus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_in_and_out_less()

                class AdjustingThruster_L2D(State):
                    pass

                class AdjustingThruster_L3D(State):
                    pass

                class AdjustingThruster_L4D(State):
                    pass

                class AdjustingThruster_L5D(State):
                    pass

            class AdjustingThrusterGroup_14(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_14, self).__init__(**kwargs)
                    self.tgKey = 'thruster_group_14'
                    self.thruster_group = getattr(self.statechart.app.mainView, self.tgKey)
                    self.setThrusterCount()

                def pitch_minus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_less()

                def roll_minus(self, arg1=None, arg2=None):
                    self.thruster_group.pulsate_less()

                def translate_z_minus(self, arg1=None, arg2=None):
                    self.thruster_group.slide_in_and_out_less()

                class AdjustingThruster_R2D(State):
                    pass

                class AdjustingThruster_R3D(State):
                    pass

                class AdjustingThruster_R4D(State):
                    pass

                class AdjustingThruster_R5D(State):
                    pass


Factory.register("RotationalMotionControl", RotationalMotionControl)
Factory.register("TranslationalMotionControl", TranslationalMotionControl)
Factory.register("ThrusterGroupControl", ThrusterGroupControl)
Factory.register("ShuttleControlView", ShuttleControlView)

class ShuttleControlApp(App):
    statechart = ObjectProperty(None)
    mainView = ObjectProperty(None)

    def build(self):
        print 'BUILDING'
        layout = FloatLayout(size=(1000,1000), size_hint=(1,1))
        self.mainView = ShuttleControlView(app=self)
        layout.add_widget(self.mainView)
        self.statechart = AppStatechart(app=self)
        self.statechart.initStatechart()
        return layout

if __name__ in ('__android__', '__main__'):
    app = ShuttleControlApp()
    app.run()

