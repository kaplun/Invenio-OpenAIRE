import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.VerticalPanel import VerticalPanel
    from pyjamas.ui.HorizontalPanel import HorizontalPanel
    from pyjamas.ui.TextArea import TextArea
    from pyjamas.ui.TextBox import TextBox
    from pyjamas.ui.Label import Label
    from pyjamas.ui.FileUpload import FileUpload
    from pyjamas.ui.ListBox import ListBox
    from pyjamas.ui.Button import Button
    from pyjamas.ui.Calendar import DateField, Calendar, CalendarPopup
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            if 'Name' in kwargs:
                self.__name = kwargs['Name']
            else:
                self.__name = None
        def getName(self):
            return self.__name
    VerticalPanel=HorizontalPanel=TextArea=TextBox=Label=FileUpload=ListBox=Button=DateField=NullClass

from checks import *

class Title(HorizontalPanel):
    def onModuleLoad(self):
        l = Label("Title:")
        t = TextArea()
        self.add(l)
        self.add(t)

class Author(HorizontalPanel):
    def onModuleLoad(self):
        l = Label("Author:")
        t = TextArea()
        self.add(l)
        self.add(t)

class Abstract(HorizontalPanel):
    def onModuleLoad(self):
        l = Label("Abstract:")
        t = TextArea()
        self.add(l)
        self.add(t)

class NoPages(VerticalPanel):
    def onModuleLoad(self):
        l = Label("NoPages:")
        t = TextBox()
        self.add(l)
        self.add(t)
        
    
class Language(VerticalPanel):
    def onModuleLoad(self):
        l = Label("Language:")
        c = ListBox()
        c.addItem("English")
        c.addItem("French")
        f = FileUpload()
        self.add(l)
        self.add(c)
        self.add(f)

class Published(HorizontalPanel):
    def onModuleLoad(self):
        l = Label("Published:")
        df = DateField()
        self.add(l)
        self.add(df)


class Checkable(HorizontalPanel):
    def __init__(self, Name, Check, Msg, Element=None, **kwargs):
        if sys.version_info[3] == 'pyjamas':
            super(Checkable, self).__init__()
        else:
            super(Checkable, self).__init__(Name=Name, **kwargs)
        self.checkFunction = checkFunction = Check
        self.checkLabel = checkLabel = Label(Msg)
        self.checkElement = checkElement = Element(Name=Name, **kwargs)

        class CheckableListener:
            def runCheck(self, sender):
                valid = checkFunction(checkElement.getText())
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

    def onModuleLoad(self): 
        self.checkLabel.setVisible(False)
        self.checkElement.addFocusListener(self.checkListener)

        self.add(self.checkElement)
        self.add(self.checkLabel)



class CheckableTextArea(Checkable):
    def __init__(self, Name, Check, Msg, **kwargs):
        super(CheckableTextArea, self).__init__(Name=Name, Check=Check, Msg=Msg, Element=TextArea, **kwargs)

class CheckableTextBox(Checkable):
    def __init__(self, Name, Check, Msg, **kwargs):
        super(CheckableTextBox, self).__init__(Name=Name, Check=Check, Msg=Msg, Element=TextBox, **kwargs)

class Email(CheckableTextBox):
    def __init__(self, Name, Check=validateEmail, Msg="Not Valid Email", **kwargs):
        super(Email, self).__init__(Name=Name, Check=Check, Msg=Msg, **kwargs )
    def onModuleLoad(self):
        #getattr(Checkable,"onModuleLoad")(self)
        l = Label("Email:")
        self.add(l)
        super(Email, self).onModuleLoad()

class Url(CheckableTextBox):
    def __init__(self, Name, Check=validateUrl, Msg="Not Valid URL", Text="http://", **kwargs):
        super(Url, self).__init__(Name=Name, Check=Check, Msg=Msg, Text=Text, **kwargs )
    def onModuleLoad(self):
        #getattr(Checkable,"onModuleLoad")(self)
        l = Label("URL:")
        self.add(l)
        super(Url, self).onModuleLoad()



