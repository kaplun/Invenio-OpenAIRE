import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.Label import Label

from invenio.websubmitbezirg_elements.Checkable import CheckableTextBox
from invenio.websubmitbezirg_checks.validateNoPages import validateNoPages


class NoPages(CheckableTextBox):
    def __init__(self, Name, CheckFunction=validateNoPages, Msg="Must be digits", **kwargs):
        super(NoPages, self).__init__(Name=Name, CheckFunction=CheckFunction, Msg=Msg, **kwargs)
    def load(self):
        l = Label("NoPages:")
        self.add(l)
        super(NoPages,self).load()
