import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.HorizontalPanel import HorizontalPanel
    from pyjamas.ui.Label import Label
    from pyjamas.ui.FileUpload import FileUpload
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    HorizontalPanel = Label = FileUpload =  NullClass

class File(HorizontalPanel):
    def __init__(self, *args, **kwargs):
        super(File,self).__init__()
        self.l = Label("Upload a file:")
        self.t = FileUpload(*args, **kwargs)
    def load(self):
        self.add(self.l)
        self.add(self.t)
