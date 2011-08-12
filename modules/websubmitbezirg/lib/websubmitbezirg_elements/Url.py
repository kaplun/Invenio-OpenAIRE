import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.Label import Label

from invenio.websubmitbezirg_elements.Checkable import CheckableTextBox
from invenio.websubmitbezirg_checks.validateUrl import validateUrl

class Url(CheckableTextBox):
    def __init__(self, Name, CheckFunction=validateUrl, Msg="Not Valid URL", Text="http://", **kwargs):
        super(Url, self).__init__(Name=Name, CheckFunction=CheckFunction, Msg=Msg, Text=Text, **kwargs)
    def load(self):
        l = Label("URL:")
        self.add(l)
        super(Url, self).load()
