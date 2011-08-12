import sys
if sys.version_info[3] == 'pyjamas':
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
        # this method parameter is different
        # than the http request method.
        # the http request method is POST (async)
        
        # the ajax request is of the form {'method': STR, 'params': JSON}

        # the params are python expressions
        # convert them to json
        jsonParams = JSONParser().toJSONString(params) 

        data = urllib.urlencode({'method': method, 'params': jsonParams})
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        
        currentURL = getLocation().getPageHref()
        HTTPRequest().asyncPost(currentURL, data, handler=handler, headers=header)

else:
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
        for element in self.elements:
            if isinstance(element, Panel):
                # panels
                # or basic elements
                if hasattr(element, 'load'):
                    element.load()
                self.add(element)
            else:
                wrapper_element = HorizontalPanel()
                if isinstance(element, tuple) or isinstance(element, list):
                    # a list of elements
                    # wrap them inside a horizontal panel
                    for element_ in element:
                        if hasattr(element_, 'load'):
                            e.load()
                        wrapper_element.add(element_)
                else:
                    # single "simple" element
                    # wrap it inside a horizontal panel
                    wrapper_element.add(element)
                self.add(wrapper_element)

        self.add(self.submitLabel)
        self.add(self.method)
        self.add(self.params)

    def fill(self, form):
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
    def __init__(self, *args):
        self.pages = args

        # 
        #self.doctype = Hidden(Name="doctype", Value="") # hidden elements 
        #self.action = Hidden(Name="action", Value="")   # for passing the doctype&action to the form 

        self.root = RootPanel("bootstrap")

        self.location = getLocation().getHref()
        
        # The Form
        #
        self.form = FormPanel(Encoding = FormPanel.ENCODING_MULTIPART, Method=FormPanel.METHOD_POST)
        self.form.setAction(self.location) # should be set to the document.URL
        self.form.addFormHandler(self) # sets the form listener
        # added to the rootpanel
        self.root.add(self.form)

        for page in self.pages:
            for element in page.elements:
                if isinstance(element, Submit):
                    element.addClickListener(self)

        # show the processing page
        self.processingPage = ProcessingPage()
        self.setCurrentPage(self.processingPage)

        # Ask for the current page
        ajax("current_page", params={}, handler=self)


    def setCurrentPage(self, page):
        self._current_page = page
        self.form.setWidget(page)


    def getCurrentPage(self):
        return self._current_page

    # The Form Listener
    #
    def onClick(self, sender):
        
        client_side_validation = server_side_validation = True
        
        if client_side_validation and server_side_validation: # short-circuit so it won't hit the server if client-side fails
            # hide that the form contains errors
            self.getCurrentPage().submitLabel.setVisible(False)

            # make the button a <input type="submit" />, submit the form
            self.form.submit()

            # show the processing page
            self.processingPage = ProcessingPage()
            self.setCurrentPage(self.processingPage)
            self.processingPage.label.setHTML("Processing form...")
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

        if result == "ok": 
            ajax("current_page", params={}, handler=self)


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
            next_page_name = result['current_page_name']
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
    def __init__(self, action, *args):
        self.action = action
        self.processes = list(args)

        def end_process(obj, engine):
            engine.setVar("result", "finished")
            engine.setVar("__finished", True)

        self.processes.append(end_process)


        self.pages = [process.__page__ for process in self.processes if getattr(process,'__page__', False)]

    def build_interface(self):
        if sys.version_info[3] == 'pyjamas':
            Interface(*self.pages)




