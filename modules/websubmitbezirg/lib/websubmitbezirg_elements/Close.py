import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.Button import Button
    from pyjamas.Window import setLocation
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    Button = NullClass

class Close(Button):
    def __init__(self, Value="Close"): # like <input type="submit" value=Value />
        super(Close, self).__init__(Value, listener=self) # the listener is None, it is set by the engine
    def load(self):
        pass
    def onClick(self, sender):
        setLocation("/")
