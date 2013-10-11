from kivy.lang import Builder
from kivy.uix.bubble import BubbleButton
from kivy.uix.listview import ListItemButton
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty


Builder.load_string('''
<ShapeBubbleButton>:

    background_down: 'atlas://data/images/defaulttheme/bubble_btn'
    background_normal: 'atlas://data/images/defaulttheme/bubble_btn_pressed'
    group: 'state_drawing_menu_root'
    size_hint: self.size_hint if hasattr(self, 'size_hint') else (1, 1)
    width: self.width if hasattr(self, 'width') else 1
    height: self.height if hasattr(self, 'height') else 1
    on_release: app.statechart.send_event( \
            self.action, self, None) if hasattr(self, 'action') else None
    text: self.text if hasattr(self, 'text') else ''
    canvas:
        Color:
            rgba: self.shape.fill_color
        Mesh:
            #vertices: self.shape.vertices(origin=self.shape.center)
            vertices: self.shape._vertices(origin=self.center)
            indices: self.shape.indices
            mode: 'triangle_fan'
        Color:
            rgba: self.shape.stroke_color
        Line:
            id: perimeter
            points: self.shape.points
            width: self.shape.stroke_width
            joint: 'round'
            close: True
#    canvas:
#        Color:
#            rgba: 1, 1, 1, 1
#        Mesh:
#            vertices: self.shape.vertices
#            indices: self.shape.indices
#            mode: 'triangle_fan'
    Scatter:
        do_scale: False
        do_translation: False
        do_rotation: False
        auto_bring_to_front: False
''')


class ShapeBubbleButton(BubbleButton, ListItemButton):

    shape = ObjectProperty(None)
    action = StringProperty('')

    def __init__(self, **kwargs):
        super(ShapeBubbleButton, self).__init__(**kwargs)
