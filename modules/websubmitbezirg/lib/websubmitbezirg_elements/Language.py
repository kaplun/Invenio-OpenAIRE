import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.VerticalPanel import VerticalPanel
    from pyjamas.ui.Label import Label
    from pyjamas.ui.ListBox import ListBox
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    Label = ListBox = VerticalPanel = NullClass


class Language(VerticalPanel):
    def __init__(self, **kwargs):
        super(Language, self).__init__()
        self.l = Label("Language:")
        self.c = ListBox(**kwargs)
        
    def load(self):
        self.c.addItem("English", "en")
        self.c.addItem("French", "fr")
        self.add(self.l)
        self.add(self.c)
