from invenio.websubmitbezirg_elements.Checkable import CheckableTextBox
from invenio.websubmitbezirg_checks.validateNoPages import validateNoPages

from pyjamas.ui.Label import Label

class NoPages(CheckableTextBox):
    def __init__(self, Name, Check=validateNoPages, Msg="Must be digits", **kwargs):
        super(NoPages, self).__init__(Name=Name, Check=Check, Msg=Msg, **kwargs)
    def load(self):
        l = Label("NoPages:")
        self.add(l)
        super(NoPages,self).load()
