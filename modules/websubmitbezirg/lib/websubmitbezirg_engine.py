"""
This module includes the basic widgets: Interface, Page and Workflow.

A thing to mention is that this module is is being processed both:
1. statically by the pyjamas, to create the client-side interface, its core logic and a basic display formatting.
2. dynamically by the invenio instance, to create the server-side logic of the interface (extracting processes, checks that belong to a DOCTYPE spec).

"""


import sys
if sys.version_info[3] == 'pyjamas':
    # modules to load if this module is being processed by the Pyjamas Compiler
    from pyjamas.ui.RootPanel import RootPanel
    from pyjamas.ui.Label import Label
    from pyjamas.ui.FormPanel import FormPanel
    from pyjamas.ui.Panel import Panel
    from pyjamas.ui.VerticalPanel import VerticalPanel
    from pyjamas.ui.HorizontalPanel import HorizontalPanel
    from pyjamas.ui.Button import Button
    from pyjamas.ui.Hidden import Hidden

    from invenio.websubmitbezirg_elements.ProcessingPanel import ProcessingPanel as ProcessingPage
    from invenio.websubmitbezirg_elements.Submit import Submit
    from invenio.websubmitbezirg_elements.Checkable import Checkable, CheckableDateField


    import urllib
    from pyjamas.HTTPRequest import HTTPRequest
    from pyjamas.Window import getLocation
    from pyjamas.JSONParser import JSONParser

    from pyjamas.ui.CheckBox import CheckBox
    from pyjamas.ui.ListBox import ListBox
    from pyjamas.ui.TextBoxBase import TextBoxBase

    from pyjamas.ui.HTML import HTML

    from pyjamas import DOM

    def ajax(method, params, handler):
        """
        Make an AJAX JSON-RPC-like call
        """

        # this method parameter is different
        # than the http request method.
        # the http request method is POST (async)
        
        # the ajax request is of the form {'method': STR, 'params': JSON}

        # the params are python expressions
        # converts them to json
        jsonParams = JSONParser().toJSONString(params) 

        data = urllib.urlencode({'method': method, 'params': jsonParams})
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        
        currentURL = getLocation().getPageHref()
        HTTPRequest().asyncPost(currentURL, data, handler=handler, headers=header)

else:
    # code to create if this module is being processed by Invenio 
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    VerticalPanel = NullClass

class Page(VerticalPanel):
    def __init__(self, name, *args, **kwargs):
        # The Main Panel
        super(Page,self).__init__(StyleName="main-panel", **kwargs)

        self.elements = args
        self.name = name

        if sys.version_info[3] == 'pyjamas':
            self.setSpacing(10)

            # Some extra elements
            self.submitLabel = Label("The form contains errors", StyleName="emph", ID="submit-label")
            self.submitLabel.setVisible(False)

            self.method = Hidden(Name="method", Value="submit_form")
            self.params = Hidden(Name="params", Value="{}")

            self.load()

    def load(self):
        """
        Addes each element of the Page and formats it according to some rules.

        The page is a VerticalPanel
        Most of the elements are Horizontal Panels
        Each element is added vertically-wise, essentially forming a Grid.
        3 rules apply to the formatting
        """

        for element in self.elements:
            
            if isinstance(element, Panel):
                # Rule 1: panels or builtin elements
                if hasattr(element, 'load'):
                    element.load()
                self.add(element)
            else:
                wrapper_element = HorizontalPanel()
                if isinstance(element, tuple) or isinstance(element, list):
                    # Rule 2: a list of elements wrap them inside a horizontal panel
                    for element_ in element:
                        if hasattr(element_, 'load'):
                            e.load()
                        wrapper_element.add(element_)
                else:
                    # Rule 3: a single "simple" element, wrap it inside a horizontal panel
                    wrapper_element.add(element)
                self.add(wrapper_element)

        self.add(self.submitLabel)
        self.add(self.method)
        self.add(self.params)

    def fill(self, form):
        """
        The form contains data to fill the elements.
        The method to fill them is different for each element type.
        The fill function dispatches element-wise:
        TextBoxBase().setText()
        CheckBox().setChecked()
        ListBox().selectValue()
        """

        for element in self.elements:
            if isinstance(element, CheckBox): 
                if element.getName() in form:
                    element.setChecked(form[element.getName()])
            elif isinstance(element, ListBox):
                if element.getName() in form:
                    element.selectValue(form[element.getName()])
            elif isinstance(element, TextBoxBase) or isinstance(element,Checkable) or isinstance(element, CheckableDateField):
                if element.getName() in form:
                    element.setText(form[element.getName()])
            elif isinstance(element, Panel):
                for element_ in element:
                    if isinstance(element_, CheckBox): 
                        if element_.getName() in form:
                            element_.setChecked(form[element_.getName()])
                    elif isinstance(element_, ListBox):
                        if element_.getName() in form:
                            element_.selectValue(form[element_.getName()])
                    elif isinstance(element_, TextBoxBase) or isinstance(element_,Checkable):
                        if element_.getName() in form:
                            element_.setText(form[element_.getName()])


class Interface(object):
    """
    The Interface can be thought as the Page Manager.

    It makes the actual AJAX calls to the server and listens for Form events.
    
    According to this feedback and data received, it makes the transition between pages.

    The interface contains also the Main Form and submits it on completion.

    """
    def __init__(self, *args):

        self.pages = args

        self.root = RootPanel("bootstrap")

        self.location = getLocation().getHref()
        
        # Create The Main Form
        self.form = FormPanel(Encoding = FormPanel.ENCODING_MULTIPART, Method=FormPanel.METHOD_POST)
        self.form.setAction(self.location) # should be set to the document.URL
        self.form.addFormHandler(self) # sets the form listener

        # adds the form to the rootpanel
        self.root.add(self.form)


        # adds ClickListeners to all the Submit buttons of the Pages
        for page in self.pages:
            for element in page.elements:
                if isinstance(element, Submit):
                    element.addClickListener(self)

        # show the processing page
        self.processingPage = ProcessingPage()
        self.setCurrentPage(self.processingPage)

        # Ask for the current page to show
        ajax("current_page", params={}, handler=self)


    def setCurrentPage(self, page):
        self._current_page = page
        self.form.setWidget(page)


    def getCurrentPage(self):
        return self._current_page

    # The Form Listener
    #
    def onClick(self, sender):
        
        # if an element is marked as invalid then the whole client-side validation is False
        if DOM.getElementById("invalid"):
            client_side_validation = False  
        else: 
            client_side_validation = True

        if client_side_validation: 
            # the client-side validation succeeded
            # transition to server-side validation

            # hide that the form contains errors
            self.getCurrentPage().submitLabel.setVisible(False)

            # server-side-validation
            self.getCurrentPage().method.setValue("validate_all")
            self.form.submit()

        else:
            # show that the form contains errors
            self.getCurrentPage().submitLabel.setVisible(True)

    def onSubmitComplete(self, event):
        # the rsp is retrieved
        # pass it to the next page

        # Ask for the current page

        rsp = event.getResults()
        rsp_html = HTML(rsp)
        rsp_json = rsp_html.getText()
        rsp_py = JSONParser().decodeAsObject(rsp_json)

        method = rsp_py['method']
        result = rsp_py['result']

        if method == "submit_form":
            if result == "ok": 
                ajax("current_page", params={}, handler=self)
        elif method == "validate_all":
            if result == True:
                # hide that the form contains errors
                self.getCurrentPage().submitLabel.setVisible(False)

                # make the button a <input type="submit" />, submit the form
                self.getCurrentPage().method.setValue("submit_form")
                self.form.submit()

                # show the processing page
                self.processingPage = ProcessingPage()
                self.setCurrentPage(self.processingPage)
                self.processingPage.label.setHTML("Processing form...")
            else:
                # show that the form contains errors
                self.getCurrentPage().submitLabel.setVisible(True)



    def onSubmit(self, event):
        pass
    

    # The AJAX handler
    #
    def onCompletion(self, text):
        # responses are of the form {'method': STR, 'result': JSON}
        
        pyText = JSONParser().decodeAsObject(text)
        method = pyText['method']
        result = pyText['result']
        if method == 'current_page':
            # the nextpage's name is returned inside the response
            next_page_name = result['__current_page_name']
            next_page = [p for p in self.pages if p.name==next_page_name][0]

            # the data to fill in the next page
            output_form = result['output_form']

            if output_form:
                next_page.fill(output_form)

            self.setCurrentPage(next_page)


    def onError(self, text, code):
        pass
    def onTimeOut(self, text):
        # self.submitLabel.setText = "mpli"
        # self.submitLabel.setVisibile(true)
        pass

class Workflow(object):
    def __init__(self, action_name, *args):
        """
        The workflow takes an action_name
        and a list of processes to run.

        A workflow also contains a list of pages that it should sequentially display,
        according to calls to the special process "show_page".
        """

        self.action = action_name
        self.processes = list(args)

        def end_process(obj, engine):
            engine.setVar("result", "finished")
            engine.setVar("__finished", True)

        self.processes.append(end_process)


        self.pages = [process.__page__ for process in self.processes if getattr(process,'__page__', False)]

    def build_interface(self):
        """
        A function that is called by the build.py script to construct the Interface, based on the pages of the Workflow.
        """
        if sys.version_info[3] == 'pyjamas':
            Interface(*self.pages)
