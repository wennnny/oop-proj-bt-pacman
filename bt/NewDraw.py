import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf, Gdk, GLib

import xdot
from NodeStatus import *
from threading import RLock
from BehaviorTree import *
from gi.repository import GObject
from ActionTest import ActionTest
from ConditionTest import ConditionTest


import random
from time import sleep


class MyDotWindow(xdot.DotWindow):

    def __init__(self):
        xdot.DotWindow.__init__(self)

    dotcode = """
    digraph G {
        World[label=\"*\n?\" penwidth=\"2\"  shape=\"box\" color=\"black\" ]
        Hello -> World
        Ciao -> World
        Ciao2 -> World
        Ciao3 -> World
    }
    """


class BTWindow(xdot.DotWindow):
    def __init__(self):
        xdot.DotWindow.__init__(self)
        self.dotcode = None
        self.node_names = []


    def get_dot_code(self):

        return self.dotcode

    def get_dot_for_node(self, node):
        type = node.nodeType
        alias = node.name
        while alias in self.node_names:
            alias = alias + 'x' #manages aliases (nodes with the same name)
        self.node_names.append(alias)

        dotcode = alias
        if type == 'Sequence':
            dotcode += """[label=\"->\" penwidth=\"2\"  shape=\"box\" color=\"black\" ]; \n """
        elif type == 'Selector':
                dotcode += """[label=\"?\" penwidth=\"2\"  shape=\"box\" color=\"black\" ]; \n """
        elif type == 'Action':
            dotcode += "[label= """ + node.name + """ penwidth=\"2\"  shape=\"box\" color=\"black\"  ];\n """
        elif type == 'Condition':
            dotcode += "[label=""" + node.name + """ penwidth=\"2\"  shape=\"ellipse\" color=\"black\" ]; \n"""
        else:
            raise ('Node type not parsed')
        return (dotcode,alias)


    def get_dot_for_tree(self,tree):
        dot_code, alias = self.get_dot_for_node(tree)
        if tree.nodeClass != 'Leaf':
            #is a non leaf node. Need to draw the children as well.
            for c in tree.Children:
                code, new_alias = self.get_dot_for_tree(c)
                dot_code += code
                dot_code += tree.name + """ -> """ + new_alias + """; \n"""
        return dot_code, alias



    def update_widget(self,tree):
        symbols = ['black', 'red', 'yellow']
        random.seed
        symbol = random.choice(symbols)
        self.dotcode = """ digraph G {
         """ + self.get_dot_for_tree(tree)[0] + """ } """ #finalization


        print(self.dotcode)
        # GLib.timeout_add(100, self.update_widget)
        self.set_dotcode(self.dotcode)
        pass


def new_draw_tree(tree):

    window = BTWindow()
    window.update_widget(tree)
    window.connect('delete-event', Gtk.main_quit)
    Gtk.main()



# def main():
#     window = MyDotWindow()
#     window.set_dotcode(dotcode)
#     window.connect('delete-event', Gtk.main_quit)
#     Gtk.main()


if __name__ == '__main__':
    fallback_1 = FallbackNode('f1')
    sequence_1 = SequenceNode('s1')
    sequence_2 = SequenceNode('s2')
    action_1 = ActionTest('Action')
    condition_1 = ActionTest('Action')

    sequence_1.AddChild(action_1)
    sequence_1.AddChild(condition_1)

    new_draw_tree(sequence_1)
