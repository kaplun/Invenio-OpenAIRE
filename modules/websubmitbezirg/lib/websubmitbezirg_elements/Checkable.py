from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Label import Label
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.PasswordTextBox import PasswordTextBox

class Checkable(HorizontalPanel):
    def __init__(self, Name, Check, Msg, Element=None, Required=False, **kwargs):
        if sys.version_info[3] == 'pyjamas':
            super(Checkable, self).__init__()
        else:
            super(Checkable, self).__init__(Name=Name, **kwargs)

        self.required = Required
        if self.required:
            # wrap required and check
            self.checkFunction = checkFunction = lambda input: Check(input) and input.strip() # wraps and input must be not an empty string
        else:
            # wrap optional and check
            self.checkFunction = checkFunction = lambda input: Check(input) or not input.strip() # wraps and input can be an empty string
        self.checkLabel = checkLabel = Label(Msg, StyleName="emph")
        self.checkElement = checkElement = Element(Name=Name, **kwargs)

        self.getName = self.checkElement.getName
        self.setText = self.checkElement.setText
        self.getText = self.checkElement.getText


        class CheckableListener:
            def runCheck(self, sender):
                valid = checkFunction(checkElement.getText())
                get("submit-label").setVisible(False)
                if valid:
                    checkElement.setID("valid")
                    checkLabel.setVisible(False)
                else:
                    checkElement.setID("invalid")
                    checkLabel.setVisible(True)
                return valid
            def onFocus(self, sender):
                pass
            def onLostFocus(self, sender):
                valid = self.runCheck(sender)
                if not valid:
                    checkElement.addKeyboardListener(self) 
                return valid
            def onKeyUp(self, sender, keyCode, modifiers):
                valid = self.runCheck(sender)
                return valid
            def onKeyDown(self, sender, keyCode, modifiers):
                pass
            def onKeyPress(self, sender, keyCode, modifiers):
                pass

        self.checkListener = CheckableListener()

    def load(self): 
        self.checkLabel.setVisible(False)
        #self.checkElement.addFocusListener(self.checkListener)

        self.add(self.checkElement)
        self.add(self.checkLabel)
        if self.required:
            l = Label("*", StyleName="emph")
            self.insert(l,0)

    
class CheckableTextArea(Checkable):
    def __init__(self, Name, Check, Msg, **kwargs):
        super(CheckableTextArea, self).__init__(Name=Name, Check=Check, Msg=Msg, Element=TextArea, **kwargs)

class CheckableTextBox(Checkable):
    def __init__(self, Name, Check, Msg, **kwargs):
        super(CheckableTextBox, self).__init__(Name=Name, Check=Check, Msg=Msg, Element=TextBox, **kwargs)

class CheckablePasswordTextBox(Checkable):
    def __init__(self, Name, Check, Msg, **kwargs):
        super(CheckablePasswordTextBox, self).__init__(Name=Name, Check=Check, Msg=Msg, Element=PasswordTextBox, **kwargs)
