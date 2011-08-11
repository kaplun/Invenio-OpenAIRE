# import interface engine
from invenio.websubmitbezirg_engine import Page, Workflow

# import basic elements
import sys
if sys.version_info[3] == 'pyjamas':
    from invenio.websubmitbezirg_elements.Author import Author
    from invenio.websubmitbezirg_elements.NoPages import NoPages
    from invenio.websubmitbezirg_elements.Url import Url
    from invenio.websubmitbezirg_elements.Email import Email
    from invenio.websubmitbezirg_elements.Password import Password
    from invenio.websubmitbezirg_elements.Submit import Submit
    from invenio.websubmitbezirg_elements.Published import Published
    from invenio.websubmitbezirg_elements.Language import Language
    from pyjamas.ui.CheckBox import CheckBox
    from pyjamas.ui.ListBox import ListBox
    from pyjamas.ui.RadioButton import RadioButton
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    NoPages = Url = ProcessingPage = Language = ListBox = RadioButton = CheckBox = Submit =  Published = Email = Password = Author = NullClass 


# import basic workflow processes
from invenio.websubmitbezirg_processes.show_page import show_page
from invenio.websubmitbezirg_processes.test_test import test_test
from invenio.websubmitbezirg_processes.explode_records import explode_records

p1 = Page("Page1",
          NoPages(Name="nopages1"),
          Url(Name="url1"),
          Published(),
          CheckBox(Name="checkbox_a1", Text="Mplo", Checked=True),
          CheckBox(Name="checkbox_b1", Text="Mpli"),
          RadioButton("rb1", "e1"),
          RadioButton("rb1", "e2"),
          RadioButton("rb1", "e3"),
          Language(Name="language1"),
          Submit()
          )

p2 = Page("Page2",
          NoPages(Name="nopages2"),
          Url(Name="url2"),
          CheckBox(Name="checkbox_a2", Text="Mplo", Checked=True),
          CheckBox(Name="checkbox_b2", Text="Mpli"),
          Language(Name="language2"),
          Submit()
          )

w1 = Workflow("Submit",
              show_page(p1),
              test_test(),
              explode_records(),
              show_page(p2)
              )

w2 = Workflow("Modify",
              show_page(p2),
              show_page(p1)
              )


