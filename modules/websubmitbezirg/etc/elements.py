from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.Label import Label
from pyjamas.ui.FileUpload import FileUpload
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.Button import Button
from pyjamas.ui.Calendar import DateField, Calendar, CalendarPopup


class Title(HorizontalPanel):
    def __init__(self):
        super(Title,self).__init__()
        l = Label("Title")
        t = TextArea()
        self.add(l)
        self.add(t)

class Author(HorizontalPanel):
    def __init__(self):
        super(Author,self).__init__()
        l = Label("Author")
        t = TextArea()
        self.add(l)
        self.add(t)

class Abstract(HorizontalPanel):
    def __init__(self):
        super(Abstract,self).__init__()
        l = Label("Abstract")
        t = TextArea()
        self.add(l)
        self.add(t)

class NoPages(VerticalPanel):
    def __init__(self):
        super(NoPages,self).__init__()
        l = Label("NoPages")
        t = TextBox()
        self.add(l)
        self.add(t)
        
    
class Language(VerticalPanel):
    def __init__(self):
        super(Language,self).__init__()
        l = Label("Language")
        c = ListBox()
        c.addItem("English")
        c.addItem("French")
        f = FileUpload()
        self.add(l)
        self.add(c)
        self.add(f)

class Submit(Button):
    def __init__(self, **kwargs):
        super(Submit,self).__init__("submit", **kwargs)

        
class Published(HorizontalPanel):
    def __init__(self):
        super(Published,self).__init__()
        l = Label("Published")
        df = DateField()
        self.add(l)
        self.add(df)

class Checkable(HorizontalPanel):
    def __init__(self, check, text = None):
        self.check = check
        self.check_label = Label("")
        self.text = None

    def onModuleLoad(self):
        self.addKeyboardListener = CheckableListener
        self.add(check_label)

    class CheckableListener:
         def onKeyUp(self, sender, keyCode, modifiers):
             self.updateText(self.textBox, self.echo)
         def onKeyDown(self, sender, keyCode, modifiers):
             pass
         def onKeyPress(self, sender, keyCode, modifiers):
             pass

class CTextArea(Checkable):
    def __init__(self, Name = name, Check = check, **kwargs):
        super(CTextArea, self).__init__(check)
        self.text = TextArea(Name = name, **kwargs)
        self.onModuleLoad()

    def onModuleLoad(self):
        self.add(text)
        super(CTextArea, self).onModuleLoad()
