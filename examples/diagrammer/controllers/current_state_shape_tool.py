from kivy.controllers.objectcontroller import ObjectController
from kivy.enums import binding_transforms
from kivy.properties import TransformProperty

from models.shape_tool import ShapeTool

class CurrentStateShapeToolController(ObjectController):

    shape_tool_item = TransformProperty(
            subject='data',
            op=binding_transforms.TRANSFORM,
            func=lambda data_item: ShapeTool(
                shape=data_item.shape,
                action='show_submenu_state_shape_tool'))

    def __init__(self, **kwargs):

        super(CurrentStateShapeToolController, self).__init__(**kwargs)
