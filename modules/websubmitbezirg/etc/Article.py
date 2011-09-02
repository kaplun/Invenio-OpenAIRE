import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.CheckBox import CheckBox
    from pyjamas.ui.ListBox import ListBox
    from pyjamas.ui.RadioButton import RadioButton
    from pyjamas.ui.Label import Label
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    CheckBox = Label = ListBox = RadioButton = NullClass 


# import interface engine
from invenio.websubmitbezirg_engine import Page, Workflow

# import basic elements
from invenio.websubmitbezirg_elements.Title import Title
from invenio.websubmitbezirg_elements.Author import Author
from invenio.websubmitbezirg_elements.Abstract import Abstract
from invenio.websubmitbezirg_elements.NoPages import NoPages
from invenio.websubmitbezirg_elements.Language import Language
from invenio.websubmitbezirg_elements.Published import Published
from invenio.websubmitbezirg_elements.File import File
from invenio.websubmitbezirg_elements.RefNumber import RefNumber
from invenio.websubmitbezirg_elements.Submit import Submit
from invenio.websubmitbezirg_elements.Close import Close


# import basic workflow processes
from invenio.websubmitbezirg_processes.show_page import show_page
from invenio.websubmitbezirg_processes.make_record import make_record
from invenio.websubmitbezirg_processes.insert_record import insert_record
from invenio.websubmitbezirg_processes.mailto import mailto
from invenio.websubmitbezirg_processes.get_report_number import get_report_number
from invenio.websubmitbezirg_processes.explode_records import explode_records

submitPage = Page("Submit Page",
                  Title("ti1"),
                  Author("au1"),
                  Abstract("ab1"),
                  NoPages("no1"),
                  Language("ln1"),
                  Published("p1", Required=True),
                  File("f1"),
                  Submit()
                  )

modifyPage = Page("Modify Page",
                  RefNumber("ref1"),
                  Submit()
)

donePage = Page("DonePage",
                Label("Thank you. Your document has been submitted."),
                Close()
                )

w1 = Workflow("Submit",
              show_page(submitPage),
              make_record(),
              insert_record(),
              show_page(donePage)
              )

w2 = Workflow("Modify",
              show_page(modifyPage),
              get_report_number(),
              explode_records(),
              show_page(submitPage),
              make_record(),
              insert_record(),
              mailto("foo@cern.ch", "bar@cern.ch"),
              show_page(donePage)
              )
