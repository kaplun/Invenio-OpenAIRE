import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.VerticalPanel import VerticalPanel
    from pyjamas.ui.HTML import HTML
    from pyjamas.Timer import Timer
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    VerticalPanel = HTML = NullClass


from invenio.websubmitbezirg_elements.Loader import Loader

class ProcessingPanel(VerticalPanel):
    def __init__(self, **kwargs):
        super(ProcessingPanel, self).__init__(**kwargs)
        self.loader = Loader()
        self.label = HTML("Loading...")
        self.load()
        self.t = Timer(10000, notify=self)
    def load(self):
        self.add(self.loader)
        self.add(self.label)
    def onTimer(self, timer):
        self.label.setHTML("""
        It seems that Processing takes too long. <br /> 
        You can try to hit <a href="">Refresh</a> or bookmark the page and come back later. <br />
        An e-mail notification will be automatically sent to you when the Processing is complete.""")
