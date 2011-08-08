from invenio.websubmitbezirg_elements.Checkable import CheckableTextBox
from invenio.websubmitbezirg_checks.validateEmail import validateEmail

from pyjamas.ui.Label import Label

class Email(CheckableTextBox):
    def __init__(self, Name, Check=validateEmail, Msg="Not Valid Email", **kwargs):
        super(Email, self).__init__(Name=Name, Check=Check, Msg=Msg, **kwargs)
    def load(self):
        l = Label("Email:")
        self.add(l)
        super(Email, self).load()
