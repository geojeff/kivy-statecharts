from kivy.lang import Builder

Builder.load_string('''
#:import math math
#:import itertools itertools

[PolygonBubbleButton@BubbleButton]:

    background_down: 'atlas://data/images/defaulttheme/bubble_btn'
    background_normal: 'atlas://data/images/defaulttheme/bubble_btn_pressed'
    group: 'drawing_menu_root'
    size_hint: ctx.size_hint if hasattr(ctx, 'size_hint') else (1, 1)
    width: ctx.width if hasattr(ctx, 'width') else 1
    height: ctx.height if hasattr(ctx, 'height') else 1
    on_release: app.statechart.send_event( \
            ctx.action, self, None)
    action: ctx.action
    text: ctx.text if hasattr(ctx, 'text') else ''
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Mesh:
            vertices: list(itertools.chain(*[ \
                       ((self.center[0]) \
                            + math.cos(i * ((2 * math.pi) / ctx.sides)) \
                                * ctx.radius, \
                        (self.center[1]) \
                            + math.sin(i * ((2 * math.pi) / ctx.sides)) \
                                * ctx.radius, \
                        math.cos(i * ((2 * math.pi) / ctx.sides)), \
                        math.sin(i * ((2 * math.pi) / ctx.sides))) \
                            for i in xrange(ctx.sides)]))
            indices: range(ctx.sides)
            mode: 'triangle_fan'
    Scatter:
        do_scale: False
        do_translation: False
        do_rotation: False
        auto_bring_to_front: False
''')
