import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, ListProperty, BooleanProperty, OptionProperty
from kivy.vector import Vector
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
from kivy.uix.scatter import ScatterPlane
from kivy.uix.switch import Switch
from kivy.config import Config 
from random import randint, random

from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import Statechart
from kivy_statechart.system.statechart import StatechartManager

import inspect


#################
#
#  Data models
#

# Thruster model.

class Thruster(Widget):
    thruster_id = StringProperty('')
    thruster_group_id = NumericProperty(0)
    thruster_grid_label = ObjectProperty(None)
    thruster_list_label = ObjectProperty(None)
    pulsation = NumericProperty(0)

    def __init__(self, thruster_id, group_id, grid_label, list_label):
        self.thruster_id = thruster_id
        self.thruster_group_id = group_id
        self.thruster_grid_label = grid_label
        self.thruster_list_label = list_label


# Thruster data reference dict -- [region][thruster_group][thruster_id] = thruster instance
 
thrusters = { 'forward':   {  1: { 'F1F': None, 'F2F': None, 'F3F': None },
                              2: { 'F1L': None, 'F3L': None },
                              3: { 'F2R': None, 'F4R': None },
                              4: { 'F1U': None, 'F2U': None, 'F3U': None },
                              5: { 'F5R': None, 'F2D': None, 'F4D': None },
                              6: { 'F1D': None, 'F3D': None, 'F5L': None }},
              'aft-left':  {  8: { 'L1A': None, 'L3A': None },
                              9: { 'L1L': None, 'L2L': None, 'L3L': None, 'L4L': None },
                             11: { 'L1U': None, 'L2U': None, 'L4U': None },
                             13: { 'L2D': None, 'L3D': None, 'L4D': None, 'L5D': None }},
              'aft-right': {  7: { 'R1A': None, 'R3A': None },
                             10: { 'R1R': None, 'R2R': None, 'R3R': None, 'R4R': None },
                             12: { 'R1U': None, 'R2U': None, 'R4U': None },
                             14: { 'R2D': None, 'R3D': None, 'R4D': None, 'R5D': None }}}

##############################
#
#  User Interface components.
#

class ThrusterControlModeSwitch(Switch):
    pass


class ThrustersListView(BoxLayout):
    item_template = StringProperty('ThrustersItem')
    items = ListProperty([])

    def __init__ (self, **kwargs):
        super(ThrustersListView, self).__init__(**kwargs)
        Clock.schedule_once(self.update_width)

    def on_items(self, *args):
        self.clear_widgets()
        for item in self.items:
            w = Builder.template(self.item_template, **item)
            self.add_widget(w)

    def update_width(self, dt):
        self.width = 100


class ThrustersGridView(BoxLayout):
    pass


class ForwardThrustersView(BoxLayout):
    pass
 

class AftLeftThrustersView(BoxLayout):
    pass
 

class AftRightThrustersView(BoxLayout):
    pass
 

# Viewport is from wiki.kivy.org snippets
#
class Viewport(ScatterPlane):
    def __init__(self, **kwargs):
        kwargs.setdefault('size', (700, 714))
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('do_scale', False)
        kwargs.setdefault('do_translation', False)
        kwargs.setdefault('do_rotation', False)
        super(Viewport, self).__init__( **kwargs)
        Window.bind(system_size=self.on_window_resize)
        Clock.schedule_once(self.fit_to_window, -1)

    def on_window_resize(self, window, size):
        self.fit_to_window()

    def fit_to_window(self, *args):
        if self.width < self.height: #portrait
            if Window.width < Window.height: #so is window
                self.scale = Window.width/float(self.width)
            else: #window is landscape..so rotate viewport
                self.scale = Window.height/float(self.width)
                self.rotation = -90
        else: #landscape
            if Window.width > Window.height: #so is window
                self.scale = Window.width/float(self.width)
            else: #window is portrait..so rotate viewport
                self.scale = Window.height/float(self.width)
                self.rotation = -90

        self.center = Window.center
        for c in self.children:
            c.size = self.size

    def add_widget(self, w, *args, **kwargs):
        super(Viewport, self).add_widget(w, *args, **kwargs)
        w.size = self.size


class ThrusterGroupControl(Widget):
    location_x = NumericProperty(0)
    location_y = NumericProperty(0)

    # The region of the space shuttle: forward, aft-left, or aft-right
    region = StringProperty('')

    # For pulsation, we alternate between the original size and the pulsation size.
    alternator = BooleanProperty(False)
    
    # The pulsation is the amount of size (radius) increase over the normal size. When off,
    # a thruster's pulsation is zero, and it paints as normal.
    pulsation = NumericProperty(10)
    
    def pulsate(self):
        if self.alternator:
            self.pos = (self.location_x+self.size[0]/2-self.pulsation/2, self.location_y+self.size[1]/2-self.pulsation/2)
            self.size = (self.pulsation, self.pulsation)
            self.alternator = False
        else:
            self.size = (10,10)
            self.pos = (self.location_x, self.location_y)
            self.alternator = True

    def adjust_pulsation(self, mode, thruster_group_id):
        if mode == 'increasing':
            self.pulsation = self.pulsation+1
        else:
            self.pulsation = self.pulsation-1 if self.pulsation > self.size[0] else self.size[0]

        for thruster_id in thrusters[self.region][thruster_group_id]:
            new_pulsation = self.pulsation - self.size[0]
            thrusters[self.region][thruster_group_id][thruster_id].pulsation = new_pulsation
            thrusters[self.region][thruster_group_id][thruster_id].thruster_grid_label.text = "{0}:{1}".format(thruster_id[1:], str(new_pulsation))
            thrusters[self.region][thruster_group_id][thruster_id].thruster_list_label.pulsation.text = str(new_pulsation)


class MotionControlWidget(Widget):
    statechart = ObjectProperty(None)
    control_id = StringProperty('')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
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

    thrusters_list_view = ObjectProperty(None)
    thrusters_grid_view = ObjectProperty(None)

    # 'increasing' and 'decreasing' are mapped to 'more' and 'less' in the UI, for brevity.
    thruster_control_mode = OptionProperty('increasing', options=('increasing', 'decreasing'))

    # The 14 group controls, which represent 44 individiual thrusters, fired in these groups.
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

    # Rotational motion controls:
    yaw_plus = ObjectProperty(None)
    yaw_minus = ObjectProperty(None)
    pitch_plus = ObjectProperty(None)
    pitch_minus = ObjectProperty(None)
    roll_plus = ObjectProperty(None)
    roll_minus = ObjectProperty(None)
    
    # Translational motion controls:
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

    def initialize_thruster_mode(self):
        # Without this set, the initial mode would be 'decreasing'.
        setattr(self.thruster_control_mode_switch, 'active', False)

    def initialize_thruster_groups(self, pulsation=10):
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

    def thruster_mode_control_changed(self):
        if self.thruster_control_mode_switch.active_norm_pos: 
            self.thruster_control_mode = 'increasing'
        else:
            self.thruster_control_mode = 'decreasing'

    def update(self, *args):
        # Pulsate thruster_groups by their pulsate amounts.
        for thruster_group in (self.thruster_group_1, self.thruster_group_2, self.thruster_group_3, self.thruster_group_4, self.thruster_group_5, self.thruster_group_6, self.thruster_group_7, self.thruster_group_8, self.thruster_group_9, self.thruster_group_10, self.thruster_group_11, self.thruster_group_12, self.thruster_group_13, self.thruster_group_14):
            thruster_group.pulsate()
        

#######################################################
#
#  Registration of UI Components with kv View System
#
Factory.register("ThrusterControlModeSwitch", ThrusterControlModeSwitch)
Factory.register("ThrustersGridView", ThrustersGridView)
Factory.register("ThrustersListView", ThrustersListView)
Factory.register("ForwardThrustersView", ForwardThrustersView)
Factory.register("AftLeftThrustersView", AftLeftThrustersView)
Factory.register("AftRightThrustersView", AftRightThrustersView)
Factory.register("RotationalMotionControl", RotationalMotionControl)
Factory.register("TranslationalMotionControl", TranslationalMotionControl)
Factory.register("ThrusterGroupControl", ThrusterGroupControl)
Factory.register("ShuttleControlView", ShuttleControlView)


############################
#
#  Application Statechart
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
            #self.statechart.app.mainView.initialize_thruster_mode()
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

            class AdjustingThrusterGroup_1(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_1, self).__init__(**kwargs)
                    self.group = 1
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def translate_x_minus(self, arg1=None, arg2=None):
                    #import pudb; pudb.set_trace()
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

            class AdjustingThrusterGroup_2(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_2, self).__init__(**kwargs)
                    self.group = 2
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def yaw_plus(self, arg1=None, arg2=None):
                    print 'yaw_plus firing', self.statechart.app.mainView.thruster_control_mode
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def translate_y_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

            class AdjustingThrusterGroup_3(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_3, self).__init__(**kwargs)
                    self.group = 3
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def yaw_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def translate_y_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

            class AdjustingThrusterGroup_4(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_4, self).__init__(**kwargs)
                    self.group = 4
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def pitch_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def translate_z_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

            class AdjustingThrusterGroup_5(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_5, self).__init__(**kwargs)
                    self.group = 5
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def pitch_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def translate_z_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

            class AdjustingThrusterGroup_6(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_6, self).__init__(**kwargs)
                    self.group = 6
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def roll_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def translate_z_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

            class AdjustingThrusterGroup_7(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_7, self).__init__(**kwargs)
                    self.group = 7
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def pitch_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def translate_x_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

            class AdjustingThrusterGroup_8(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_8, self).__init__(**kwargs)
                    self.group = 8
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def pitch_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def translate_x_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

            class AdjustingThrusterGroup_9(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_9, self).__init__(**kwargs)
                    self.group = 9
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def yaw_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def translate_y_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

            class AdjustingThrusterGroup_10(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_10, self).__init__(**kwargs)
                    self.group = 10
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def yaw_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def translate_y_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

            class AdjustingThrusterGroup_11(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_11, self).__init__(**kwargs)
                    self.group = 11
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def pitch_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def roll_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def translate_z_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

            class AdjustingThrusterGroup_12(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_12, self).__init__(**kwargs)
                    self.group = 12
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def pitch_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def roll_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def translate_z_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

            class AdjustingThrusterGroup_13(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_13, self).__init__(**kwargs)
                    self.group = 13
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def pitch_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def roll_plus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def translate_z_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

            class AdjustingThrusterGroup_14(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingThrusterControls.AdjustingThrusterGroup_14, self).__init__(**kwargs)
                    self.group = 14
                    self.thruster_group = getattr(self.statechart.app.mainView, 'thruster_group_%s' % self.group)

                def pitch_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def roll_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)

                def translate_z_minus(self, arg1=None, arg2=None):
                    self.thruster_group.adjust_pulsation(self.statechart.app.mainView.thruster_control_mode, self.group)


#################
#
#  Application 
#
class ShuttleControlApp(App):
    statechart = ObjectProperty(None)
    thrustersListView = ObjectProperty(None)
    mainView = ObjectProperty(None)
    thruster_ids_sorted = ListProperty([])

    def build(self):
        Config.set('graphics', 'width', '700') # not working, must be set from command line
        Config.set('graphics', 'height', '714') # not working, must be set from command line
        self.root = Viewport(size=(700,714))

        self.mainView = ShuttleControlView(app=self)
        self.root.add_widget(self.mainView)

        self.statechart = AppStatechart(app=self)
        self.statechart.initStatechart()

        Clock.schedule_once(self.create_thrusters, 5)

        thruster_ids = []
        for region in thrusters:
            for thruster_group_id in thrusters[region]:
                for thruster_id in thrusters[region][thruster_group_id]:
                    thruster_ids.append(thruster_id)
        self.thruster_ids_sorted = sorted(thruster_ids)

        # Initialize list items.
        self.mainView.thrusters_list_view.items = [{ 'thruster_id': t_id, 'pulsation': '0' } for t_id in self.thruster_ids_sorted]

        return self.root

    def create_thrusters(self, dt):
        # A sorted list of thruster ids is needed for setting grid items.
        region_widgets = { 'forward': self.mainView.thrusters_grid_view.forward_thrusters,
                           'aft-left': self.mainView.thrusters_grid_view.aft_left_thrusters,
                           'aft-right': self.mainView.thrusters_grid_view.aft_right_thrusters }

        # Create the 44 thruster data objects, setting them in the global reference data dict.
        for region in thrusters:
            for group_id in thrusters[region]:
                for thruster_id in thrusters[region][group_id]:
                    grid_label = getattr(region_widgets[region], thruster_id.lower())
                    list_label = self.mainView.thrusters_list_view.children[self.thruster_ids_sorted.index(thruster_id)]
                    thrusters[region][group_id][thruster_id] = Thruster(thruster_id, group_id, grid_label, list_label)

##########
#
#  Main
#
if __name__ in ('__android__', '__main__'):
    app = ShuttleControlApp()
    app.run()

