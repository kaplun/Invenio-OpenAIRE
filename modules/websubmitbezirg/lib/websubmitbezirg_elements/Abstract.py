import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.HorizontalPanel import HorizontalPanel
    from pyjamas.ui.Label import Label
    from pyjamas.ui.TextArea import TextArea
else:
    HorizontalPanel = object

class Abstract(HorizontalPanel):
    def load(self):
        l = Label("Abstract:")
        t = TextArea()
        self.add(l)
        self.add(t)