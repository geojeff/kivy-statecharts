from kivy.uix.screenmanager import Screen

from kivy.lang import Builder


Builder.load_string('''
#:import DrawingMenu views.drawing_menus.DrawingMenu
#:import DrawingArea views.drawing_area.DrawingArea

<DrawingAreaScreen>
    drawing_menu: drawing_menu
    drawing_area: drawing_area

    BoxLayout:
        orientation: 'vertical'
        spacing: 2

        BoxLayout:
            size_hint: 1, None
            height: 30

            ToggleButton:
                text: 'Help'
                group: 'screen manager buttons'
                on_press: app.statechart.send_event('go_to_help')

            ToggleButton:
                text: 'Drawing Area'
                color: [1.0, 1.0, 1.0, .9]
                bold: True
                group: 'screen manager buttons'
                state: 'down'

        BoxLayout:

            DrawingMenu:
                id: drawing_menu

            DrawingArea:
                id: drawing_area
''')


class DrawingAreaScreen(Screen):
    pass
