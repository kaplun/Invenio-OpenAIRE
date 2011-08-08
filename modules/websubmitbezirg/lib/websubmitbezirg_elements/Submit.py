from pyjamas.ui.Button import Button

class Submit(Button):
    def __init__(self, Value="Submit"): # like <input type="submit" value=Value />
        super(Submit, self).__init__(Value) # the listener is None, it is set by the engine
    def load(self):
        pass
