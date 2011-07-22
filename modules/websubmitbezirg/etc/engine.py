from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.HTML import HTML

from elements import *

class Interface(object):
    def __init__(self, *args):
        root = RootPanel("bootstrap")
        for element in args:
            root.add(element)


class Workflow(object):
    def __init__(self):
        pass
