import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.HorizontalPanel import HorizontalPanel
    from pyjamas.ui.Label import Label
    from pyjamas.ui.TextArea import TextArea
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass

    HorizontalPanel = Label = TextArea = NullClass

class Title(HorizontalPanel):
    def __init__(self, Name, **kwargs):
        super(Title,self).__init__()
        self.l = Label("Title:")
        self.t = TextArea(Name, **kwargs)

    def load(self):
        self.add(self.l)
        self.add(self.t)
