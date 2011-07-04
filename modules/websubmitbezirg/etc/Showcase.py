import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.CheckBox import CheckBox
    from pyjamas.ui.ListBox import ListBox
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    CheckBox = ListBox = NullClass 

# import interface engine
from invenio.websubmitbezirg_engine import Page, Workflow

# import basic elements
from invenio.websubmitbezirg_elements.NoPages import NoPages
from invenio.websubmitbezirg_elements.Url import Url
from invenio.websubmitbezirg_elements.Email import Email
from invenio.websubmitbezirg_elements.Password import Password
from invenio.websubmitbezirg_elements.Published import Published
from invenio.websubmitbezirg_elements.Language import Language
from invenio.websubmitbezirg_elements.Submit import Submit

# import basic workflow processes
from invenio.websubmitbezirg_processes.show_page import show_page
from invenio.websubmitbezirg_processes.fill_test import fill_test


p1 = Page("Page1",
          NoPages("nopages1"),
          Url("url1", Required=True), 
          Email("email1", Required=True),
          Password("p1", Required=True),          
          [CheckBox("ca1", Text="Mplo", Checked=True), CheckBox("cb1", Text="Mpli")] ,
          Published("published1", Required=True),
          Language("language1"),
          Submit()
          )

w1 = Workflow("Test",
              show_page(p1),
              fill_test(),
              show_page(p1)
              )
