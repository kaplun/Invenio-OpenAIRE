from pyjamas.ui.RootPanel import *
from pyjamas.DOM import getElementById, getInnerText
from pyjamas.ui.FormPanel import FormPanel
from pyjamas.ui.Button import Button
from pyjamas.ui.Hidden import Hidden
from pyjamas import Window


from elements import *

class Interface(object):
    def __init__(self, *args):
        self.elements = args

        self.root = RootPanel("bootstrap")

        self.form = FormPanel()
        self.form.setAction("/websubmitbezirg/submit/")
        

        # Because we're going to add a FileUpload widget, we'll need to set the
        # form to use the POST method, and multipart MIME encoding.
        self.form.setEncoding(FormPanel.ENCODING_MULTIPART)
        self.form.setMethod(FormPanel.METHOD_POST)

        # Add an event handler to the form.
        self.form.addFormHandler(self)

        # Create a panel to hold all of the form widgets.
        self.panel = VerticalPanel()
        self.form.setWidget(self.panel)

        self.root.add(self.form)

        for element in self.elements:
            self.panel.add(element)

        self.doctype = Hidden(Name="doctype", Value="")
        self.action = Hidden(Name="action", Value="")
        self.panel.add(self.doctype)
        self.panel.add(self.action)
        
        self.submitButton = Button("Submit", self)
        self.submitMsg = Label("The form contains errors")
        self.submitMsg.setVisible(False)
        self.panel.add(self.submitButton)
        self.panel.add(self.submitMsg)



    def onClick(self, sender):
        for element in self.elements:
            if isinstance(element, Checkable): # checkable panel
                subelements = element.getChildren()
                for subelement in subelements:
                    if isinstance(subelement, TextBox) or isinstance(subelement, TextArea): # checkable textarea or textbox
                        if subelement.getID() == "invalid":
                            self.submitMsg.setVisible(True)
                            return "Validation failed" # just for exiting the function

        # if the function has been validated, the form will be POSTed 
        self.submitMsg.setVisible(False)
        
        self.doctype.setValue(getInnerText(getElementById("_doctype")))
        self.action.setValue(getInnerText(getElementById("_action")))


        #self.form.submit()

    def onSubmitComplete(self, event):
        # When the form submission is successfully completed, this event is
        # fired. Assuming the service returned a response of type text/plain,
        # we can get the result text here (see the FormPanel documentation for
        # further explanation).
        pass

    def onSubmit(self, event):
        pass


class Workflow(object):
    def __init__(self):
        pass
