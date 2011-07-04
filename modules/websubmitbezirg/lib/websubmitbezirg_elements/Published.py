from invenio.websubmitbezirg_elements.Checkable import CheckableDateField

class Published(CheckableDateField):
    def __init__(self, Name, Title="Published:", **kwargs):
        super(Published,self).__init__(Name=Name, Title=Title, **kwargs)
