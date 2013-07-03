from kivy.uix.widget import Widget

from kivy.lang import Builder


Builder.load_string('''
<DrawingArea>:
    canvas:
        Color:
            rgba: .3, .3, .3, .3
        Rectangle:
            size: self.size
            pos: self.pos
    on_touch_down: app.statechart.send_event( \
            'drawing_area_touch_down', args[1]) \
            if self.collide_point(*args[1].pos) else None
    on_touch_move: app.statechart.send_event( \
            'drawing_area_touch_move', args[1]) \
            if self.collide_point(*args[1].pos) else None
    on_touch_up: app.statechart.send_event( \
            'drawing_area_touch_up', args[1]) \
            if self.collide_point(*args[1].pos) else None
''')


class DrawingArea(Widget):
    pass
