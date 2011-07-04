import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.Label import Label

from invenio.websubmitbezirg_elements.Checkable import CheckablePasswordTextBox
from invenio.websubmitbezirg_checks.validatePassword import validatePassword



class Password(CheckablePasswordTextBox):
    def __init__(self, Name, CheckFunction=validatePassword, Msg = "Not Valid Password", **kwargs):
        super(Password, self).__init__(Name=Name, CheckFunction=CheckFunction, Msg=Msg, **kwargs)
    def load(self):
        l = Label("Password:")
        self.add(l)
        super(Password, self).load()
