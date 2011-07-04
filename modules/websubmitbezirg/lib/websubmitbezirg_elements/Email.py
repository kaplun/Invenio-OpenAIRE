import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.Label import Label

from invenio.websubmitbezirg_elements.Checkable import CheckableTextBox
from invenio.websubmitbezirg_checks.validateEmail import validateEmail


class Email(CheckableTextBox):
    def __init__(self, Name, CheckFunction=validateEmail, Msg="Not Valid Email", **kwargs):
        super(Email, self).__init__(Name=Name, CheckFunction=CheckFunction, Msg=Msg, **kwargs)
    def load(self):
        l = Label("Email:")
        self.add(l)
        super(Email, self).load()
