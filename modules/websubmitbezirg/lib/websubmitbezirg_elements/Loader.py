import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.Image import Image
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    Image = NullClass


class Loader(Image):
    def __init__(self, url="/websubmitbezirg-static/ajax-loader.gif", **kwargs):
        super(Loader,self).__init__(url=url, **kwargs)
    def load(self):
        pass
