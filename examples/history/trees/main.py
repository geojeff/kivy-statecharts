import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.treeview import TreeView, TreeViewNode, TreeViewLabel
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scatter import ScatterPlane
from kivy.config import Config 

from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import Statechart
from kivy_statechart.system.statechart import StatechartManager

# TreesApp shows several trees in tab panels, for use in testing history states.

##############################
#
#  User Interface components.
#

# Viewport is from wiki.kivy.org snippets
#
class Viewport(ScatterPlane):
    def __init__(self, **kwargs):
        kwargs.setdefault('size', (700, 774))
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


############################
#
#  Application Statechart
#

# Utility method for constructing state name from cosmetic label text
# of tab headers.
#
def state_name(text):
    return 'Showing{0}'.format(text.replace(' ', ''))

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
            kwargs['initialSubstateKey'] = 'ShowingMain'
            super(AppStatechart.RootState, self).__init__(**kwargs)
        
        def enterState(self, context=None):
            print 'RootState/enterState'
                            
        def exitState(self, context=None):
            print 'RootState/exitState'

        ##############################
        # ShowingMain
        #
        class ShowingMain(State):
            def __init__(self, **kwargs):
                kwargs['initialSubstateKey'] = 'ShowingInstructions' # Initial system startup
                super(AppStatechart.RootState.ShowingMain, self).__init__(**kwargs)
        
            def enterState(self, context=None):
                print 'ShowingMain/enterState'
                        
            def exitState(self, context=None):
                print 'ShowingMain/exitState'

            def tab_selection_did_change(self, tab_header=None, context=None):
                self.gotoState(state_name(tab_header.text))

            ######################################
            # ShowingInstructions (default tab)
            #
            class ShowingInstructions(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingMain.ShowingInstructions, self).__init__(**kwargs)
            
                def enterState(self, context=None):
                    print 'ShowingInstructions/enterState'
                            
                def exitState(self, context=None):
                    print 'ShowingInstructions/exitState'
    
            ##############################
            # ShowingTreeOne
            #
            class ShowingTreeOne(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingMain.ShowingTreeOne, self).__init__(**kwargs)
            
                def enterState(self, context=None):
                    print 'ShowingTreeOne/enterState'
                            
                def exitState(self, context=None):
                    print 'ShowingTreeOne/exitState'
    
                def node_clicked(self, node_id=None, touch=None):
                    print 'node clicked - tree one', node_id, touch
    
            ##############################
            # ShowingTreeTwo
            #
            class ShowingTreeTwo(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingMain.ShowingTreeTwo, self).__init__(**kwargs)
            
                def enterState(self, context=None):
                    print 'ShowingTreeTwo/enterState'
                            
                def exitState(self, context=None):
                    print 'ShowingTreeTwo/exitState'
    
                def node_clicked(self, node_id=None, touch=None):
                    print 'node clicked - tree two', node_id, touch
    
    
# See kivy/examples/widgets/tabbed_panel_showcase.py for the original code
# for how to subclass TabbedPanel for animation.
#
class MainTabbedPanel(TabbedPanel):
    app = ObjectProperty(None)

    # Override tab switching method to animate on tab switch,
    # and to fire tab actions to the statechart.
    #
    def switch_to(self, header):
        if header.content is None:
            return
        anim = Animation(color=(1, 1, 1, 0), d =.24, t = 'in_out_quad')

        def start_anim(_anim, child, in_complete, *lt):
            if hasattr(child, 'color'):
                _anim.start(child)
            elif not in_complete:
                _on_complete()

        def _on_complete(*lt):
            if hasattr(header.content, 'color'):
                header.content.color = (0, 0, 0, 0)
                anim = Animation(color = (1, 1, 1, 1), d =.23, t = 'in_out_quad')
                start_anim(anim, header.content, True)

            # Guard for early firing, when the TabbedPanel will switch_to the default_tab
            # on instantiation, which the statechart matches by its default state setup.
            #
            # So, at app startup, the UI and the statechart will be in sync on the default tab,
            # but here we dispatch later tab changes to stay in sync.
            #
            if self.app.statechart: 
                self.app.statechart.sendEvent('tab_selection_did_change', header)

            super(MainTabbedPanel, self).switch_to(header)

        anim.bind(on_complete = _on_complete)
        if self.content and self.content.children:
            start_anim(anim, self.content.children[0], False)
        else:
            _on_complete()


class TreeNodeButton(Button, TreeViewLabel):
    app = ObjectProperty(None)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.app.statechart.sendEvent('node_clicked', self.text, touch)
            return True


#################
#
#  Application 
#
class TreesApp(App):
    statechart = ObjectProperty(None)
    main_view = ObjectProperty(None)

    def build(self):
        Config.set('graphics', 'width', '800') # not working, must be set from command line
        Config.set('graphics', 'height', '600') # not working, must be set from command line

        self.root = Viewport(size=(800,600))

        tp = MainTabbedPanel(app=self, default_tab_text='Instructions', default_tab_content=Label(text='Click on tree nodes in trees one and two.'))

        # Recursive utility function for adding nodes to the tree view.
        #
        # The custom tree node type, TreeNodeButton, has an app property, giving access to
        # the statechart for sending node click events to the statechart.
        #
        def populate_tree_nodes(tree_view, parent, node):
            if parent is None:
                tree_node_button = tree_view.add_node(TreeNodeButton(app=self, text=node['node_id'], is_open=True))
            else:
                tree_node_button = tree_view.add_node(TreeNodeButton(app=self, text=node['node_id'], is_open=True), parent)
    
            for child_node in node['children']:
                populate_tree_nodes(tree_view, tree_node_button, child_node)
        
        # Add tree one.
        #
        tree = {'node_id': '1',
                'children': [{'node_id': '1.1',
                              'children': [{'node_id': '1.1.1',
                                            'children': [{'node_id': '1.1.1.1',
                                                          'children': []}]},
                                           {'node_id': '1.1.2',
                                            'children': []},
                                           {'node_id': '1.1.3',
                                            'children': []}]},
                              {'node_id': '1.2',
                               'children': []}]}
        tph = TabbedPanelHeader(text='Tree One')
        tree_one = TreeView(root_options=dict(text='Tree One'), hide_root=False, indent_level=4)
        populate_tree_nodes(tree_one, None, tree)
        tph.content = tree_one
        tp.add_widget(tph)

        # Add tree two.
        #
        tree = {'node_id': '2',
                'children': [{'node_id': '2.1',
                              'children': [{'node_id': '2.1.1',
                                            'children': [{'node_id': '2.1.1.1',
                                                          'children': []}]},
                                           {'node_id': '2.1.2',
                                            'children': []},
                                           {'node_id': '2.1.3',
                                            'children': []}]},
                              {'node_id': '2.2',
                               'children': []}]}
        tph = TabbedPanelHeader(text='Tree Two')
        tree_two = TreeView(root_options=dict(text='Tree Two'), hide_root=False, indent_level=4)
        populate_tree_nodes(tree_two, None, tree)
        tph.content = tree_two
        tp.add_widget(tph)

        self.root.add_widget(tp)

        return self.root

    def on_start(self):
        self.statechart = AppStatechart(app=self)
        self.statechart.initStatechart()


##########
#
#  Main
#
if __name__ in ('__android__', '__main__'):
    app = TreesApp()
    app.run()


