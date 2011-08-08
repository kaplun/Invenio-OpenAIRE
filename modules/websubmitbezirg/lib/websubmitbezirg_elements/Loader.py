from pyjamas.ui.Image import Image

class Loader(Image):
    def __init__(self, url="/websubmitbezirg-static/ajax-loader.gif", **kwargs):
        super(Loader,self).__init__(url=url, **kwargs)
    def load(self):
        pass
