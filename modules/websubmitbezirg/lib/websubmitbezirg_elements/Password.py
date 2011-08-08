from invenio.websubmitbezirg_elements.Checkable import CheckablePasswordTextBox
from invenio.websubmitbezirg_checks.validatePassword import validatePassword

from pyjamas.ui.Label import Label

class Password(CheckablePasswordTextBox):
    def __init__(self, Name, Check=validatePassword, Msg = "Not Valid Password", **kwargs):
        super(Password, self).__init__(Name=Name, Check=Check, Msg=Msg, **kwargs)
    def load(self):
        l = Label("Password:")
        self.add(l)
        super(Password, self).load()
