from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.Label import Label
from pyjamas.ui.FileUpload import FileUpload
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.Button import Button
from pyjamas.ui.Calendar import DateField, Calendar, CalendarPopup

from checks import *

class Title(HorizontalPanel):
    def __init__(self):
        super(Title,self).__init__()
        l = Label("Title:")
        t = TextArea()
        self.add(l)
        self.add(t)

class Author(HorizontalPanel):
    def __init__(self):
        super(Author,self).__init__()
        l = Label("Author:")
        t = TextArea()
        self.add(l)
        self.add(t)

class Abstract(HorizontalPanel):
    def __init__(self):
        super(Abstract,self).__init__()
        l = Label("Abstract:")
        t = TextArea()
        self.add(l)
        self.add(t)

class NoPages(VerticalPanel):
    def __init__(self):
        super(NoPages,self).__init__()
        l = Label("NoPages:")
        t = TextBox()
        self.add(l)
        self.add(t)
        
    
class Language(VerticalPanel):
    def __init__(self):
        super(Language,self).__init__()
        l = Label("Language:")
        c = ListBox()
        c.addItem("English")
        c.addItem("French")
        f = FileUpload()
        self.add(l)
        self.add(c)
        self.add(f)

class Published(HorizontalPanel):
    def __init__(self):
        super(Published,self).__init__()
        l = Label("Published:")
        df = DateField()
        self.add(l)
        self.add(df)


class Checkable(HorizontalPanel):
    def __init__(self, Name, Check, Msg, Element=None, **kwargs):
        super(Checkable, self).__init__()
        check = Check

        element = Element(Name=Name, **kwargs)
        check_label = Label(Msg)
        check_label.setVisible(False)

        class CheckableListener:
            def runCheck(self, sender):
                valid = check(element.getText())
                if valid:
                    element.setID("valid")
                    check_label.setVisible(False)
                else:
                    element.setID("invalid")
                    check_label.setVisible(True)
                return valid
            def onFocus(self, sender):
                pass
            def onLostFocus(self, sender):
                valid = self.runCheck(sender)
                if not valid:
                    element.addKeyboardListener(self) 
                return valid
            def onKeyUp(self, sender, keyCode, modifiers):
                valid = self.runCheck(sender)
                return valid
            def onKeyDown(self, sender, keyCode, modifiers):
                pass
            def onKeyPress(self, sender, keyCode, modifiers):
                pass
        element.addFocusListener(CheckableListener())

        self.add(element)
        self.add(check_label)

class CheckableTextArea(Checkable):
    def __init__(self, Name, Check, Msg, **kwargs):
        super(CheckableTextArea, self).__init__(Name, Check, Msg, TextArea, **kwargs)

class CheckableTextBox(Checkable):
    def __init__(self, Name, Check, Msg, **kwargs):
        super(CheckableTextBox, self).__init__(Name, Check, Msg, TextBox, **kwargs)

class Email(CheckableTextBox):
    def __init__(self, Name, Check=validateEmail, Msg="Not Valid Email", **kwargs):
        super(Email, self).__init__(Name=Name, Check=Check, Msg=Msg, **kwargs )
        l = Label("Email:")
        self.insert(l,0)

class Url(CheckableTextBox):
    def __init__(self, Name, Check=validateUrl, Msg="Not Valid URL", **kwargs):
        super(Url, self).__init__(Name=Name, Check=Check, Msg=Msg, **kwargs )
        l = Label("URL:")
        self.insert(l,0)
