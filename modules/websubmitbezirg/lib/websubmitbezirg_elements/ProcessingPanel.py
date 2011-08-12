import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.VerticalPanel import VerticalPanel
    from pyjamas.ui.HTML import HTML
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    VerticalPanel = HTML = NullClass


from invenio.websubmitbezirg_elements.Loader import Loader
#from invenio.messages import gettext_set_language

class ProcessingPanel(VerticalPanel):
    def __init__(self, **kwargs):
        #_ = gettext_set_language(lang)
        super(ProcessingPanel, self).__init__(**kwargs)
        self.loader = Loader()
        self.label = HTML("Processing, please wait...")
        self.load()
    def load(self):
        self.add(self.loader)
        self.add(self.label)
