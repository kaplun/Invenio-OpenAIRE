import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.HorizontalPanel import HorizontalPanel
    from pyjamas.ui.Label import Label
    from pyjamas.ui.TextBox import TextBox
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    HorizontalPanel = Label = TextBox = NullClass

class RefNumber(HorizontalPanel):
    def __init__(self, Required=False, **kwargs):
        super(RefNumber, self).__init__()
        self.l = Label("Specify Ref Number:")
        self.t = TextBox(**kwargs)
    def load(self):
        self.add(self.l)
        self.add(self.t)
