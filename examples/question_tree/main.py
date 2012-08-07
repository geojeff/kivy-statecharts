import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.treeview import TreeView, TreeViewNode, TreeViewLabel
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatter import ScatterPlane
from kivy.config import Config 
#from listview import ListAdapter, ListView

from kivy_statechart.system.state import State
from kivy_statechart.system.statechart import Statechart
from kivy_statechart.system.statechart import StatechartManager

# TreesApp shows several trees in tab panels.

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
                self.gotoState('ShowingTree')

            #####################################
            # ShowingInstructions (default tab)
            #
            class ShowingInstructions(State):
                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingMain.ShowingInstructions, self).__init__(**kwargs)
            
                def enterState(self, context=None):
                    print 'ShowingInstructions/enterState'
                            
                def exitState(self, context=None):
                    print 'ShowingInstructions/exitState'
    
            ######################################################
            # ShowingTree -- designed for reuse for tree states
            #
            # [TODO] In reuse, the states are each unique objects, but do not have unique names.
            #        Will this work?
            #
            class ShowingTree(State):
                selected_node = ObjectProperty(None)

                def __init__(self, **kwargs):
                    super(AppStatechart.RootState.ShowingMain.ShowingTree, self).__init__(**kwargs)

                def enterState(self, context=None):
                    print 'ShowingTree/enterState'
                            
                def exitState(self, context=None):
                    print 'ShowingTree/exitState'

                def node_clicked(self, node_id=None, touch=None):
                    print 'node clicked - tree one', node_id, touch
                    self.selected_node = self.statechart.app.tabbed_panel.current_tab.content.tree_view.selected_node

                    print 'clicked on TreeNodeLabel', self.selected_node.text, self.selected_node.level

                    if self.selected_node.is_answered is True:
                        self.gotoState('ShowingNodeAlreadyCompletePopup')
                    elif type(self.selected_node.parent_node) is TreeViewLabel or self.selected_node.parent_node.is_answered is True:
                        # This node is root or a node whose parent is_answered, so is eligible.
                        self.gotoState('ShowingNodeQuestion')
                    else:
                        self.gotoState('ShowingIneligibleNodePopup')

                class ShowingNodeQuestion(State):
                    selected_node = ObjectProperty(None) # [TODO] Better to get from parentState?
                    current_tab_content = ObjectProperty(None)
                    content_answer_input = ObjectProperty(None)

                    def __init__(self, **kwargs):
                        super(AppStatechart.RootState.ShowingMain.ShowingTree.ShowingNodeQuestion, self).__init__(**kwargs)
                
                    def enterState(self, context=None):
                        print 'ShowingNodeQuestion/enterstate'

                        self.current_tab_content = self.statechart.app.tabbed_panel.current_tab.content
                        self.selected_node = self.current_tab_content.tree_view.selected_node

                        content = GridLayout(cols=1)

                        content_question_label = Label(text=self.selected_node.question, text_size=(200, None))
                        self.content_answer_input = TextInput(text=self.selected_node.answer)
                        content_ok = Button(text='OK', size_hint_y=None, height=40)
                        content_cancel = Button(text='Cancel', size_hint_y=None, height=40)

                        content_ok.bind(on_release=self.evaluate_answer)
                        content_cancel.bind(on_release=self.cancel)

                        content.add_widget(content_question_label)
                        content.add_widget(self.content_answer_input)
                        content.add_widget(content_ok)
                        content.add_widget(content_cancel)

                        self.popup = Popup(title="Node: {0}".format(self.selected_node.text), size_hint=(None, None), size=(400, 400), content=content, auto_dismiss=False)

                        self.popup.open()
                                
                    def exitState(self, context=None):
                        print 'ShowingNodeQuestion/exitState'
                        self.popup.dismiss()

                    def evaluate_answer(self, context):
                        print 'evaluate_answer', self.content_answer_input.text.lower(), self.selected_node.answer
                        if self.content_answer_input.text.lower() == self.selected_node.answer:
                            self.selected_node.background_color = [0., 1., 0., 1.]
                            self.selected_node.is_answered = True

                            # Are there any unanswered questions in this tree? If not, mark the entire tree of questions as complete.
                            # Otherwise, update the score.
                            num_correct = len([1 for node_button in self.current_tab_content.tree_view.iterate_all_nodes() 
                                                   if type(node_button) == TreeNodeButton and node_button.is_answered is True])
                            num_questions = len(self.current_tab_content.tree_view.children)-1 # - 1 for the root TreeViewLabel

                            if num_correct == num_questions:
                                self.current_tab_content.is_completed = True 
                                self.current_tab_content.completion_status_label.text = "All questions were answered correctly!"
                            else:
                                self.current_tab_content.completion_status_label.text = "Score: {0}/{1}".format(num_correct, num_questions)

                            self.gotoState(self.parentState)
                        else:
                            self.selected_node.background_color = [1., 0., 0., 1.]
                            self.selected_node.is_answered = False
                            self.gotoState('ShowingWrongAnswerPopup')

                    def cancel(self, context):
                        # Note: Parent class is the name of the class in the actual statechart, 
                        # not ShowingTreeState -- this is the superclass. So, we know in this
                        # case that we can just go up to parent.
                        self.gotoState(self.parentState)

                class ShowingNodeAlreadyCompletedPopup(State):
                    popup = ObjectProperty(None)

                    def __init__(self, **kwargs):
                        super(AppStatechart.RootState.ShowingMain.ShowingTree.ShowingNodeAlreadyCompletedPopup, self).__init__(**kwargs)
                
                    def enterState(self, context=None):
                        print 'ShowingNodeAlreadyCompletedPopup/enterState'
                        content = GridLayout(cols=1)

                        content_label = Label(text="Your correct answer: {0}.".format(self.statechart.app.tabbed_panel.current_tab.content.selected_node.answer), text_size=(200, None))
                        content_ok_button = Button(text='OK', size_hint_y=None, height=40)

                        content_ok_button.bind(on_release=self.cancel)

                        content.add_widget(content_label)
                        content.add_widget(content_ok_button)

                        self.popup = Popup(title="Already Answered Correctly", size_hint=(None, None), size=(400, 400), content=content, auto_dismiss=False)

                        self.popup.open()
                                
                    def exitState(self, context=None):
                        print 'ShowingNodeAlreadyCompletedPopup/exitState'
                        self.popup.dismiss()

                    def cancel(self, context):
                        self.gotoState(self.parentState)

                class ShowingIneligibleNodePopup(State):
                    popup = ObjectProperty(None)

                    def __init__(self, **kwargs):
                        super(AppStatechart.RootState.ShowingMain.ShowingTree.ShowingIneligibleNodePopup, self).__init__(**kwargs)
                
                    def enterState(self, context=None):
                        print 'ShowingIneligibleNodePopup/enterState'
                        selected_node = self.statechart.app.tabbed_panel.current_tab.content.tree_view.selected_node
                        content = GridLayout(cols=1)

                        content_label = Label(text="(You skipped one or more parents).".format(selected_node.text), text_size=(200, None))
                        content_ok_button = Button(text='OK', size_hint_y=None, height=40)

                        content_ok_button.bind(on_release=self.cancel)

                        content.add_widget(content_label)
                        content.add_widget(content_ok_button)

                        self.popup = Popup(title="Sorry, ineligible node: {0}".format(selected_node.text), size_hint=(None, None), size=(400, 400), content=content, auto_dismiss=False)

                        self.popup.open()
                                
                    def exitState(self, context=None):
                        print 'ShowingIneligibleNodePopup/exitState'
                        self.popup.dismiss()

                    def cancel(self, context):
                        self.gotoState(self.parentState)

                class ShowingWrongAnswerPopup(State):
                    popup = ObjectProperty(None)

                    def __init__(self, **kwargs):
                        super(AppStatechart.RootState.ShowingMain.ShowingTree.ShowingWrongAnswerPopup, self).__init__(**kwargs)
                
                    def enterState(self, context=None):
                        print 'ShowingWrongAnswerPopup/enterState'
                        content = GridLayout(cols=1)

                        content_label = Label(text=self.statechart.app.tabbed_panel.current_tab.content.tree_view.selected_node.question, text_size=(200, None))
                        content_give_up_button = Button(text='I give up for now', size_hint_y=None, height=40)
                        content_try_again_button = Button(text='Try Again', size_hint_y=None, height=40)

                        content_try_again_button.bind(on_release=self.try_again)
                        content_give_up_button.bind(on_release=self.cancel)

                        content.add_widget(content_label)
                        content.add_widget(content_try_again_button)
                        content.add_widget(content_give_up_button)

                        self.popup = Popup(title="Sorry, wrong answer", size_hint=(None, None), size=(400, 400), content=content, auto_dismiss=False)

                        self.popup.open()
                                
                    def exitState(self, context=None):
                        print 'ShowingWrongAnswerPopup/exitState'
                        self.popup.dismiss()

                    def try_again(self, context):
                        self.gotoState('ShowingNodeQuestion')

                    def cancel(self, context):
                        self.gotoState(self.parentState)


            
    
# See kivy/examples/widgets/tabbed_panel_showcase.py for the original code
# for how to subclass TabbedPanel for animation.
#
class MainTabbedPanel(TabbedPanel):
    app = ObjectProperty(None)

    # Override tab switching method to animate on tab switch,
    # and to fire tab actions to the statechart.
    #
    def switch_to(self, header, *args):
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
    question = StringProperty(None)
    answer = StringProperty(None)
    is_answered = BooleanProperty(False)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.app.statechart.sendEvent('node_clicked', self.text, touch)
            return True


##################
#
#  TabBoxLayout
#
class TabBoxLayout(BoxLayout):
    tree_view = ObjectProperty(None)
    completion_status_label = ObjectProperty(None)
    is_complete = BooleanProperty(False)
    num_questions = NumericProperty(0)

    def __init__(self, tree_view=None, completion_status_label=None, num_questions=0, **kwargs):
        self.tree_view = tree_view
        self.completion_status_label = completion_status_label
        self.num_questions = num_questions

        super(TabBoxLayout, self).__init__(**kwargs)

        self.add_widget(tree_view)
        self.add_widget(completion_status_label)


#################
#
#  Application 
#
class TreesApp(App):
    statechart = ObjectProperty(None)
    tabbed_panel = ObjectProperty(None)

    def build(self):
        Config.set('graphics', 'width', '800') # not working, must be set from command line
        Config.set('graphics', 'height', '600') # not working, must be set from command line

        self.root = Viewport(size=(800,600))

        self.tabbed_panel = MainTabbedPanel(app=self, default_tab_text='Instructions', default_tab_content=Label(text='Click on tree nodes in trees one and two, and answer qeuestions that pop up. You are forced to answer the root question first, and you will not be able to answer the question for a node unless all of the node\'s parents have already been answered successfully. As questions for nodes are answered, the nodes are colored green. If answered incorrectly, nodes are marked as red. The goal to "solve" a tree of questions is to paint all nodes green.', text_size=(200, None)))

        # Recursive utility function for adding nodes to the tree view.
        #
        # The custom tree node type, TreeNodeButton, has an app property, giving access to
        # the statechart for sending node click events to the statechart.
        #
        # Leverage this recursion for counting the questions.
        #
        def populate_tree_nodes(tree_view, parent, node):
            if parent is None:
                tree_node_button = tree_view.add_node(TreeNodeButton(app=self, question=node['question'], answer=node['answer'], text=node['node_id'], is_open=True))
            else:
                tree_node_button = tree_view.add_node(TreeNodeButton(app=self, question=node['question'], answer=node['answer'], text=node['node_id'], is_open=True), parent)
    
            for child_node in node['children']:
                populate_tree_nodes(tree_view, tree_node_button, child_node)
        
        # Add tree one.
        #
        tree = {'node_id': '1',
                'question': 'What is 2 + 2?',
                'answer': '4',
                'children': [{'node_id': '1.1',
                              'question': 'What continent holds Ethiopia?',
                              'answer': 'africa',
                              'children': [{'node_id': '1.1.1',
                                            'question': 'The cat drank the milk. Which word in that sentence is the verb?',
                                            'answer': 'drank',
                                            'children': [{'node_id': '1.1.1.1',
                                                          'question': 'How many degrees for a right angle?',
                                                          'answer': '90',
                                                          'children': []}]},
                                           {'node_id': '1.1.2',
                                            'question': 'Which ocean is the largest?',
                                            'answer': 'pacific',
                                            'children': []},
                                           {'node_id': '1.1.3',
                                            'question': 'Tiny negatively charged particles around an atomic nucleus are called?',
                                            'answer': 'electrons',
                                            'children': []}]},
                              {'node_id': '1.2',
                               'question': 'What is the last name of the king of rock and roll?',
                               'answer': 'presley',
                               'children': []}]}

        tph = TabbedPanelHeader(text='Tree One')
        tree_one = TreeView(root_options=dict(text='Tree One'), hide_root=False, indent_level=4)
        populate_tree_nodes(tree_one, None, tree)
        tab_content = TabBoxLayout(tree_view=tree_one, completion_status_label=Label(text='Not started'), orientation='vertical')
        tph.content = tab_content
        self.tabbed_panel.add_widget(tph)

        # Add tree two.
        #
        tree = {'node_id': '2',
                'question': 'How many Earth planets are recognized in 2012?',
                'answer': '8',
                'children': [{'node_id': '2.1',
                              'question': 'Which planet got knocked off?',
                              'answer': 'pluto',
                              'children': [{'node_id': '2.1.1',
                                            'question': 'Which planet is the largest?',
                                            'answer': 'jupiter',
                                            'children': [{'node_id': '2.1.1.1',
                                                          'question': 'Which planet is known for its rings?',
                                                          'answer': 'saturn',
                                                          'children': []}]},
                                           {'node_id': '2.1.2',
                                            'question': 'The second planet from the Sun, with a rich carbon dioxide atmosphere, is?',
                                            'answer': 'venus',
                                            'children': []},
                                           {'node_id': '2.1.3',
                                            'question': 'Mars is known for its giant volcano, ______________ Mons.',
                                            'answer': 'olympus',
                                            'children': []}]},
                             {'node_id': '2.2',
                              'question': 'Io is a moon of which planet?',
                              'answer': 'jupiter',
                              'children': []}]}

        tph = TabbedPanelHeader(text='Tree Two')
        tree_two = TreeView(root_options=dict(text='Tree Two'), hide_root=False, indent_level=4)
        populate_tree_nodes(tree_two, None, tree)
        tph.content = TabBoxLayout(tree_view=tree_two, completion_status_label=Label(text='Not started'), orientation='vertical')
        self.tabbed_panel.add_widget(tph)

        self.root.add_widget(self.tabbed_panel)

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



