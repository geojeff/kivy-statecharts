import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, ListProperty
from kivy.vector import Vector
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint, random
from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import Statechart
from kivy_statechart.system.statechart import StatechartManager

import inspect


class ThrustersImage(Image):
    def __init__(self, source):
        super(ThrustersImage, self).__init__(source=source)


class ThrusterGroupControl(Widget):
    vibration_x = NumericProperty(0)
    vibration_y = NumericProperty(0)
    vibration = ReferenceListProperty(vibration_x, vibration_y)
    
    def vibrate(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_back_and_forth_more(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_back_and_forth_less(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_in_and_out_more(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_in_and_out_less(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_in_and_out_more(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_in_and_out_less(self):
        self.pos = Vector(*self.vibration) + self.pos


class RotationalMotionControl(Widget):
    vibration_x = NumericProperty(0)
    vibration_y = NumericProperty(0)
    vibration = ReferenceListProperty(vibration_x, vibration_y)
    
    def vibrate(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_back_and_forth_more(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_back_and_forth_less(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_in_and_out_more(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_in_and_out_less(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_in_and_out_more(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_in_and_out_less(self):
        self.pos = Vector(*self.vibration) + self.pos


class TranslationalMotionControl(Widget):
    vibration_x = NumericProperty(0)
    vibration_y = NumericProperty(0)
    vibration = ReferenceListProperty(vibration_x, vibration_y)
    
    def vibrate(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_back_and_forth_more(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_back_and_forth_less(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_in_and_out_more(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_in_and_out_less(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_in_and_out_more(self):
        self.pos = Vector(*self.vibration) + self.pos

    def slide_in_and_out_less(self):
        self.pos = Vector(*self.vibration) + self.pos


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

    def __init__(self, app, background_image):
        self.app = app
        self.background_image = background_image
        print background_image
        super(ShuttleControlView, self).__init__() 
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        print 'My keyboard has been closed!'
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print 'The key', keycode, 'has been pressed'
        print ' - text is %r' % text
        print ' - modifiers are %r' % modifiers

        if keycode[1] == 's':
            self.app.statechart.sendEvent('vibrate')
        elif keycode[1] == 'escape':
            # Keycode is composed of an integer + a string
            # If we hit escape, release the keyboard
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def place_thruster_groups(self, vibration=(4,0)):
        for thruster_group in (self.thruster_group_1, self.thruster_group_2, self.thruster_group_3, self.thruster_group_4, self.thruster_group_5, self.thruster_group_6, self.thruster_group_7, self.thruster_group_8, self.thruster_group_9, self.thruster_group_10, self.thruster_group_11, self.thruster_group_12, self.thruster_group_13, self.thruster_group_14):
            thruster_group.vibration = vibration
        
    def update(self, *args):
        # Wiggle thruster_groups by their vibrate amounts.
        for thruster_group in (self.thruster_group_1, self.thruster_group_2, self.thruster_group_3, self.thruster_group_4, self.thruster_group_5, self.thruster_group_6, self.thruster_group_7, self.thruster_group_8, self.thruster_group_9, self.thruster_group_10, self.thruster_group_11, self.thruster_group_12, self.thruster_group_13, self.thruster_group_14):
            thruster_group.vibrate()
        

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
        self.thruster_group.vibration_x += len(self.thrusters)
        self.thruster_group.vibration_y += len(self.thrusters)

    def slow_down(self, arg1=None, arg2=None):
        self.thruster_group.vibration_x -= len(self.thrusters)
        self.thruster_group.vibration_y -= len(self.thrusters)

    def zero_out(self, arg1=None, arg2=None):
        self.thruster_group.vibration_x = 0
        self.thruster_group.vibration_y = 0


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
            #self.statechart.app.mainView.place_thruster_groups()
            #Clock.schedule_interval(self.statechart.app.mainView.update, 1.0/60.0)
                        
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

                def translate_x_minus(self):
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
                    self.tgKey = 'thruster_group_2'
                    self.vibration_x = 2
                    self.vibration_y = 2
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_2, self).__init__(**kwargs)

                def yaw_plus(self):
                    self.thruster_group.rotate_more()

                def translate_y_plus(self):
                    self.thruster_group.slide_up_and_down_more()

                class AdjustingThruster_F1L(State):
                    pass

                class AdjustingThruster_F3L(State):
                    pass

            class AdjustingThrusterGroup_3(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    self.tgKey = 'thruster_group_3'
                    self.vibration_x = 3
                    self.vibration_y = 3
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_3, self).__init__(**kwargs)

                def yaw_minus(self):
                    self.thruster_group.rotate_less()

                def translate_y_minus(self):
                    self.thruster_group.slide_up_and_down_less()

                class AdjustingThruster_F2R(State):
                    pass

                class AdjustingThruster_F4R(State):
                    pass

            class AdjustingThrusterGroup_4(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    self.tgKey = 'thruster_group_4'
                    self.vibration_x = 4
                    self.vibration_y = 4
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_4, self).__init__(**kwargs)

                def pitch_minus(self):
                    self.thruster_group.rotate_less()

                def translate_z_plus(self):
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
                    self.tgKey = 'thruster_group_5'
                    self.vibration_x = 5
                    self.vibration_y = 5
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_5, self).__init__(**kwargs)

                def pitch_plus(self):
                    self.thruster_group.rotate_more()

                def translate_z_minus(self):
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
                    self.tgKey = 'thruster_group_6'
                    self.vibration_x = 5
                    self.vibration_y = 5
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_6, self).__init__(**kwargs)

                def roll_plus(self):
                    self.thruster_group.rotate_more()

                def translate_z_minus(self):
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
                    self.tgKey = 'thruster_group_7'
                    self.vibration_x = 5
                    self.vibration_y = 5
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_7, self).__init__(**kwargs)

                def pitch_minus(self):
                    self.thruster_group.rotate_less()

                def translate_x_plus(self):
                    self.thruster_group.slide_back_and_forth_more()

                class AdjustingThruster_R1A(State):
                    pass

                class AdjustingThruster_R3A(State):
                    pass

            class AdjustingThrusterGroup_8(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    self.tgKey = 'thruster_group_8'
                    self.vibration_x = 5
                    self.vibration_y = 5
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_8, self).__init__(**kwargs)

                def pitch_plus(self):
                    self.thruster_group.rotate_more()

                def translate_x_plus(self):
                    self.thruster_group.slide_back_and_forth_more()

                class AdjustingThruster_L1A(State):
                    pass

                class AdjustingThruster_L3A(State):
                    pass

            class AdjustingThrusterGroup_9(ThrusterControlState):
                def __init__(self, **kwargs):
                    kwargs['substatesAreConcurrent'] = True
                    self.tgKey = 'thruster_group_9'
                    self.vibration_x = 5
                    self.vibration_y = 5
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_9, self).__init__(**kwargs)

                def yaw_minus(self):
                    self.thruster_group.rotate_less()

                def translate_y_plus(self):
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
                    self.tgKey = 'thruster_group_10'
                    self.vibration_x = 5
                    self.vibration_y = 5
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_10, self).__init__(**kwargs)

                def yaw_plus(self):
                    self.thruster_group.rotate_more()

                def translate_y_minus(self):
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
                    self.tgKey = 'thruster_group_11'
                    self.vibration_x = 5
                    self.vibration_y = 5
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_11, self).__init__(**kwargs)

                def pitch_plus(self):
                    self.thruster_group.rotate_more()

                def roll_minus(self):
                    self.thruster_group.rotate_less()

                def translate_z_plus(self):
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
                    self.tgKey = 'thruster_group_12'
                    self.vibration_x = 5
                    self.vibration_y = 5
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_12, self).__init__(**kwargs)

                def pitch_plus(self):
                    self.thruster_group.rotate_more()

                def roll_plus(self):
                    self.thruster_group.rotate_more()

                def translate_z_plus(self):
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
                    self.tgKey = 'thruster_group_13'
                    self.vibration_x = 5
                    self.vibration_y = 5
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_13, self).__init__(**kwargs)

                def pitch_minus(self):
                    self.thruster_group.rotate_less()

                def roll_plus(self):
                    self.thruster_group.rotate_more()

                def translate_z_minus(self):
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
                    self.tgKey = 'thruster_group_14'
                    self.vibration_x = 5
                    self.vibration_y = 5
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_14, self).__init__(**kwargs)

                def pitch_minus(self):
                    self.thruster_group.rotate_less()

                def roll_minus(self):
                    self.thruster_group.rotate_less()

                def translate_z_minus(self):
                    self.thruster_group.slide_in_and_out_less()

                class AdjustingThruster_R2D(State):
                    pass

                class AdjustingThruster_R3D(State):
                    pass

                class AdjustingThruster_R4D(State):
                    pass

                class AdjustingThruster_R5D(State):
                    pass


Factory.register("ThrustersImage", ThrustersImage)
Factory.register("RotationalMotionControl", RotationalMotionControl)
Factory.register("TranslationalMotionControl", TranslationalMotionControl)
Factory.register("ThrusterGroupControl", ThrusterGroupControl)
Factory.register("ShuttleControlView", ShuttleControlView)

class ShuttleControlApp(App):
    statechart = ObjectProperty(None)
    mainView = ObjectProperty(None)

    def build(self):
        print 'BUILDING'
        self.mainView = ShuttleControlView(app=self, background_image=ThrustersImage("RCSJetCode.png"))
        self.statechart = AppStatechart(app=self)
        self.statechart.initStatechart()
        return self.mainView

if __name__ in ('__android__', '__main__'):
    app = ShuttleControlApp()
    app.run()

