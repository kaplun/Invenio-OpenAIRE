import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.Button import Button
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    Button = NullClass

class Submit(Button):
    def __init__(self, Value="Submit"): # like <input type="submit" value=Value />
        super(Submit, self).__init__(Value) # the listener is None, it is set by the engine
    def load(self):
        pass
