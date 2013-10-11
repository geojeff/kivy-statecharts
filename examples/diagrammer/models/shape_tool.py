from kivy.models import SelectableDataItem
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty


class ShapeTool(SelectableDataItem):
    shape = ObjectProperty(None)
    action = StringProperty('')
