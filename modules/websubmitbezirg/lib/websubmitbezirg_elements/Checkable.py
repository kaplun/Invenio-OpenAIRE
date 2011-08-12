import sys
from time import strptime
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.HorizontalPanel import HorizontalPanel
    from pyjamas.ui.Label import Label
    from pyjamas.ui.TextArea import TextArea
    from pyjamas.ui.TextBox import TextBox
    from pyjamas.ui.PasswordTextBox import PasswordTextBox
    from pyjamas.ui.RootPanel import get
    from pyjamas.JSONParser import JSONParser

    import urllib
    from pyjamas.HTTPRequest import HTTPRequest
    from pyjamas.Window import getLocation
    from pyjamas.JSONParser import JSONParser
    def ajax(method, params, handler):
        jsonParams = JSONParser().toJSONString(params) 

        data = urllib.urlencode({'method': method, 'params': jsonParams})
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        
        currentURL = getLocation().getPageHref()
        HTTPRequest().asyncPost(currentURL, data, handler=handler, headers=header)

else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    Label = TextArea = TextBox = HorizontalPanel = PasswordTextBox = NullClass

from invenio.websubmitbezirg_elements.DateField import DateField


class Checkable(HorizontalPanel):
    def __init__(self, Name, CheckFunction, Msg, Element=None, Check=True, Required=False, CheckOnClient=True, **kwargs):
        super(Checkable, self).__init__() 

        self.name = Name
        self.Check = Check
        self.CheckOnClient = CheckOnClient


        # Required
        self.required = Required
        if self.required:
            # wrap required and check
            self.checkFunction = lambda input: input.strip()!='' and CheckFunction(input)   # wraps and input must be not an empty string
        else:
            # wrap optional and check
            self.checkFunction = lambda input: input.strip()=='' or CheckFunction(input)  # wraps and input can be an empty string

        self.checkLabel = Label(Msg, StyleName="emph")
        self.checkElement = Element(Name=Name, **kwargs)

    # Methods to make Checkable behave like an Element
    def getName(self):
        return self.name
    def setText(self,txt):
        self.checkElement.setText(txt)
    def getText(self):
        return self.checkElement.getText()

    # self.getName = self.checkElement.getName
    # self.setText = self.checkElement.setText
    # self.getText = self.checkElement.getText

    def load(self): 
        self.checkLabel.setVisible(False)
        self.checkElement.addFocusListener(self)

        self.add(self.checkElement)
        self.add(self.checkLabel)

        if self.required:
            l = Label("*", StyleName="emph")
            self.insert(l,0)

    def runCheck(self, sender):
        get("submit-label").setVisible(False)
        try:
            if not self.CheckOnClient:
                raise Exception
            valid = self.checkFunction(self.checkElement.getText())
            if valid:
                self.checkElement.setID("valid")
                self.checkLabel.setVisible(False)
            else:
                self.checkElement.setID("invalid")
                self.checkLabel.setVisible(True)
            return valid
        except:
            # client check failed
            # make server check
            ajax("validate", {"element_name": self.getName(), "element_input": self.getText()}, self)
            return True
    def onFocus(self, sender):
        pass
    def onLostFocus(self, sender):
        if self.Check:
            valid = self.runCheck(sender)
            if not valid:
                self.checkElement.addKeyboardListener(self) 
            return valid
    def onKeyUp(self, sender, keyCode, modifiers):
        valid = self.runCheck(sender)
        return valid
    def onKeyDown(self, sender, keyCode, modifiers):
        pass
    def onKeyPress(self, sender, keyCode, modifiers):
        pass

    # server check listener
    def onCompletion(self, text):
        pyText = JSONParser().decodeAsObject(text)
        method = pyText['method']
        result = pyText['result']
        
        if method == "validate":
            if result == True:
                # the element is valid
                self.checkElement.setID("valid")
                self.checkLabel.setVisible(False)
            else:
                self.checkElement.setID("invalid")
                self.checkLabel.setVisible(True)
    def onError(self, text, code):
        pass
    def onTimeOut(self, text):
        pass


class CheckableTextArea(Checkable):
    def __init__(self, Name, CheckFunction, Msg, **kwargs):
        super(CheckableTextArea, self).__init__(Name=Name, CheckFunction=CheckFunction, Msg=Msg, Element=TextArea, **kwargs)

class CheckableTextBox(Checkable):
    def __init__(self, Name, CheckFunction, Msg, **kwargs):
        super(CheckableTextBox, self).__init__(Name=Name, CheckFunction=CheckFunction, Msg=Msg, Element=TextBox, **kwargs)

class CheckablePasswordTextBox(Checkable):
    def __init__(self, Name, CheckFunction, Msg, **kwargs):
        super(CheckablePasswordTextBox, self).__init__(Name=Name, CheckFunction=CheckFunction, Msg=Msg, Element=PasswordTextBox, **kwargs)


class CheckableDateField(HorizontalPanel):
    def __init__(self, Name, Title, Msg="Not Valid Date", CheckOnClient=True, Required=False, **kwargs):
        super(CheckableDateField, self).__init__()
        self.CheckOnClient=CheckOnClient
        self.l = Label(Title)
        self.name = Name
        self.d = DateField(**kwargs)
        self.checkLabel = Label(Msg, StyleName="emph")

        # Required
        self.required = Required
        if self.required:
            # wrap required and check
            self.checkFunction = lambda input: strptime(input, self.d.format)   # wraps and input must be not an empty string
        else:
            # wrap optional and check
            self.checkFunction = lambda input: input.strip()=='' or strptime(input, self.d.format)  # wraps and input can be an empty string

    def load(self):
        self.checkLabel.setVisible(False)
        self.checkElement = self.d.getTextBox()
        self.checkElement.setName(self.name)
        self.checkElement.addFocusListener(self)

        if self.required:
            l_ = Label("*", StyleName="emph")
            self.add(l_)

        self.add(self.l)
        self.add(self.d)
        self.add(self.checkLabel)
        
    def getName(self):
        return self.checkElement.getName()

    def getText(self):
        return self.checkElement.getText()

    def setText(self, text):
        self.checkElement.setText(text)

    def onLostFocus(self, sender):
        get("submit-label").setVisible(False)
        if not self.CheckOnClient:
            ajax("validate", {"element_name": self.getName(), "element_input": self.getText()}, self)
        else:
            try:
                self.checkFunction(self.checkElement.getText())
            except:
                self.checkElement.setID("invalid")
                self.checkLabel.setVisible(True)
            else:
                self.checkElement.setID("valid")
                self.checkLabel.setVisible(False)
        
    def onFocus(self, sender):
        pass

    # server check listener
    def onCompletion(self, text):
        pyText = JSONParser().decodeAsObject(text)
        method = pyText['method']
        result = pyText['result']
        
        if method == "validate":
            if result == True:
                # the element is valid
                self.checkElement.setID("valid")
                self.checkLabel.setVisible(False)
            else:
                self.checkElement.setID("invalid")
                self.checkLabel.setVisible(True)
    def onError(self, text, code):
        pass
    def onTimeOut(self, text):
        pass
