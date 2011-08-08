from pyjamas.ui.HorizontalPanel import HorizontalPanel

class Abstract(HorizontalPanel):
    def load(self):
        l = Label("Abstract:")
        t = TextArea()
        self.add(l)
        self.add(t)
