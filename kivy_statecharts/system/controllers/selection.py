'''
ObjectSelection
=================

.. versionadded:: 1.8

.. warning::

    This code is still experimental, and its API is subject to change in a
    future version.

:class:`Selection` provides selection operations for controllers.

Elements that control selection behaviour:

* *selection*, a list of selected items.

* *selection_mode*, 'single', 'multiple', 'none'

* *allow_empty_selection*, a boolean -- If False, a selection is forced. If
  True, and only user or programmatic action will change selection, it can
  be empty.

Users of this class dispatch the *on_selection_change* event.

    :Events:
        `on_selection_change`: (view, view list )
            Fired when selection changes

.. versionchanged:: 1.8.0

    Broke out of :class:`ListAdapter` into a mixin class. Adapted for
    controllers.

'''

__all__ = ('ObjectSelection', )

import inspect

from kivy.event import EventDispatcher

from kivy.adapters.models import SelectableDataItem

from kivy.properties import BooleanProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import OpObservableList
from kivy.properties import OptionProperty


class ObjectSelection(EventDispatcher):
    '''
    A base class for controllers interfacing with lists, dictionaries or other
    collection type data.
    '''

    selection = ListProperty([], cls=OpObservableList)
    '''The selection list property is the container for selected items.

    :data:`selection` is a :class:`~kivy.properties.ListProperty` and defaults
    to [].
    '''

    selection_mode = OptionProperty('single',
            options=('none', 'single', 'multiple'))
    '''Selection modes:

       * *none*, use the list as a simple list (no select action). This option
         is here so that selection can be turned off, momentarily or
         permanently, for an existing list controller.

       * *single*, multi-touch/click ignored. Single item selection only.

       * *multiple*, multi-touch / incremental addition to selection allowed;
         may be limited to a count by selection_limit

    :data:`selection_mode` is an :class:`~kivy.properties.OptionProperty` and
    defaults to 'single'.
    '''

    propagate_selection_to_data = BooleanProperty(False)
    '''Data items are required to have an is_selected boolean property.

    NOTE: This would probably be better named as sync_selection_with_data().

    :data:`propagate_selection_to_data` is a
    :class:`~kivy.properties.BooleanProperty` and defaults to False.
    '''

    allow_empty_selection = BooleanProperty(True)
    '''The allow_empty_selection may be used for cascading selection between
    several controllers. Such automatic maintenance of the selection is
    important for all but simple apps.  Set allow_empty_selection to False and
    the selection is auto-initialized and always maintained, so any observing
    objects may likewise be updated to stay in sync.

    :data:`allow_empty_selection` is a
    :class:`~kivy.properties.BooleanProperty` and defaults to True.
    '''

    selection_limit = NumericProperty(-1)
    '''When the selection_mode is multiple and the selection_limit is
    non-negative, this number will limit the number of selected items. It can
    be set to 1, which is equivalent to single selection. If selection_limit is
    not set, the default value is -1, meaning that no limit will be enforced.

    :data:`selection_limit` is a :class:`~kivy.properties.NumericProperty` and
    defaults to -1 (no limit).
    '''

    __events__ = ('on_selection_change', )

    def __init__(self, **kwargs):
        super(ObjectSelection, self).__init__(**kwargs)

        self.bind(selection_mode=self.selection_mode_changed,
                  allow_empty_selection=self.check_for_empty_selection)

        self.initialize_selection()

    def get_count(self):
        return len(self.content)

    def get_content_item(self, index):
        if index < 0 or index >= len(self.content):
            return None
        return self.content[index]

    def selection_mode_changed(self, *args):
        if self.selection_mode == 'none':
            for selected_item in self.selection:
                self.deselect_item(selected_item)
        else:
            self.check_for_empty_selection()

    def on_selection_change(self, *args):
        '''on_selection_change() is the default handler for the
        on_selection_change event.
        '''
        pass

    def get_selection(self):
        '''A convenience method.
        '''
        return self.selection

    def get_first_selected_item(self):
        '''A convenience method.
        '''
        return self.selection[0] if self.selection else None

    def handle_selection(self, item, hold_dispatch=False, *args):
        if item not in self.selection:
            if self.selection_mode in ['none', 'single'] and \
                    len(self.selection) > 0:
                for selected_item in self.selection:
                    self.deselect_item(selected_item)
            if self.selection_mode != 'none':
                if self.selection_mode == 'multiple':
                    if self.allow_empty_selection:
                        # If < 0, selection_limit is not active.
                        if self.selection_limit < 0:
                            self.select_item(item)
                        else:
                            if len(self.selection) < self.selection_limit:
                                self.select_item(item)
                    else:
                        self.select_item(item)
                else:
                    self.select_item(item)
        else:
            self.deselect_item(item)
            if self.selection_mode != 'none':
                #
                # If the deselection makes selection empty, the following call
                # will check allows_empty_selection, and if False, will
                # select the first item. If item happens to be the first item,
                # this will be a reselection.
                #
                self.check_for_empty_selection()

        if not hold_dispatch:
            self.dispatch('on_selection_change')

    def select_item(self, item):
        self.set_content_item_selection(item, True)
        self.selection.append(item)

    def deselect_item(self, item):
        self.set_content_item_selection(item, False)
        self.selection.remove(item)

    def set_content_item_selection(self, item, value):
        if isinstance(item, SelectableDataItem):
            item.is_selected = value
        elif type(item) == dict:
            if 'is_selected' in item:
                item['is_selected'] = value
        elif hasattr(item, 'is_selected'):
            # TODO: Change this to use callable().
            if (inspect.isfunction(item.is_selected)
                    or inspect.ismethod(item.is_selected)):
                item.is_selected()
            else:
                item.is_selected = value

    def initialize_selection(self, *args):
        if len(self.selection) > 0:
            self.selection = []
            self.dispatch('on_selection_change')

        self.check_for_empty_selection()

    def check_for_empty_selection(self, *args):
        if not self.allow_empty_selection:
            if len(self.selection) == 0:
                # Select the first item if we have it.
                item = self.get_content_item(0)
                if item is not None:
                    self.handle_selection(item)
