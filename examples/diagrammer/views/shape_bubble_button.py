from kivy.lang import Builder
from kivy.uix.bubble import BubbleButton


Builder.load_string('''
<ShapeBubbleButton>:

    background_down: 'atlas://data/images/defaulttheme/bubble_btn'
    background_normal: 'atlas://data/images/defaulttheme/bubble_btn_pressed'
    group: 'state_drawing_menu_root'
    size_hint: self.size_hint if hasattr(self, 'size_hint') else (1, 1)
    width: self.width if hasattr(self, 'width') else 1
    height: self.height if hasattr(self, 'height') else 1
    on_release: app.statechart.send_event( \
            self.action, self, None)
    action: self.action
    text: self.text if hasattr(self, 'text') else ''
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Mesh:
            vertices: self.shape.vertices()
            indices: self.shape.indices()
            mode: 'triangle_fan'
    Scatter:
        do_scale: False
        do_translation: False
        do_rotation: False
        auto_bring_to_front: False
''')


class ShapeBubbleButton(BubbleButton):
    pass
