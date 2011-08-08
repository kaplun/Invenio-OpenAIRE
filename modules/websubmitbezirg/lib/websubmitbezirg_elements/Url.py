from invenio.websubmitbezirg_elements.Checkable import CheckableTextBox
from invenio.websubmitbezirg_checks.validateUrl import validateUrl

from pyjamas.ui.Label import Label

class Url(CheckableTextBox):
    def __init__(self, Name, Check=validateUrl, Msg="Not Valid URL", Text="http://", **kwargs):
        super(Url, self).__init__(Name=Name, Check=Check, Msg=Msg, Text=Text, **kwargs)
    def load(self):
        l = Label("URL:")
        self.add(l)
        super(Url, self).load()
