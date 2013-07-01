from kivy.lang import Builder
from kivy.uix.bubble import BubbleButton
from kivy.uix.listview import ListItemButton
from kivy.properties import ObjectProperty


Builder.load_string('''
<PolygonBubbleButton>:

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
            rgba: 1, 1, 1, 1
        Mesh:
            vertices: self.shape.vertices(origin=self.center)
            indices: self.shape.indices()
            mode: 'triangle_fan'
    Scatter:
        do_scale: False
        do_translation: False
        do_rotation: False
        auto_bring_to_front: False
''')


class PolygonBubbleButton(BubbleButton, ListItemButton):

    shape = ObjectProperty(None)

    def __init__(self, **kwargs):

        self.shape = kwargs['shape_cls'](radius=kwargs['radius'],
                                         sides=kwargs['sides'])

        self.value = kwargs['value']

        if 'action' in kwargs:
            self.action = kwargs['action']

        super(PolygonBubbleButton, self).__init__(**kwargs)
