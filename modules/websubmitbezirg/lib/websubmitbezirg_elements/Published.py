from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Label import Label
from invenio.websubmitbezirg_elements.DateField import DateField

class Published(HorizontalPanel):
    def load(self):
        l = Label("Published:")
        df = DateField()
        self.add(l)
        self.add(df)
