from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.Label import Label
from pyjamas.ui.ListBox import ListBox

class Language(VerticalPanel):
    def __init__(self, **kwargs):
        super(Language, self).__init__()
        self.l = Label("Language:")
        self.c = ListBox(**kwargs)
        self.c.addItem("English", "en")
        self.c.addItem("French", "fr")
        
    def load(self):
        self.add(self.l)
        self.add(self.c)
