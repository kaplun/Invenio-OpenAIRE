from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Label import Label
from pyjamas.ui.TextArea import TextArea

class Author(HorizontalPanel):
    def load(self):
        l = Label("Author:")
        t = TextArea()
        self.add(l)
        self.add(t)
