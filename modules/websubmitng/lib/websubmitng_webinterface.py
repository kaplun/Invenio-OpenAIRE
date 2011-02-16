"""
This is the webinterface handler module for the websubmit NG.
"""
from uuid import UUID

from invenio.webinterface_handler import WebInterfaceDirectory
from invenio.webpage import page
from invenio.webuser import collect_user_info, getUid
from invenio.config import CFG_SITE_URL
from invenio.urlutils import redirect_to_url

from invenio.websubmitng_engine import WebSubmitSession, WebSubmitSubmission
from invenio.engine import GenericWorkflowEngine, HaltProcessing


def check_access_user(req, wfe):
    """
    Checking user access.
    """
    if ((wfe.hasVar('next_user') and req._session['uid'] in wfe.getVar('next_user'))
        or not wfe.hasVar('next_user')): return True
    else: return False
    
def resume_workflow(req, wfe, session, submission, component, action):
    wfe._i[0] -= 1
    wfe._i[1][-1] += 1
    start_workflow(req, wfe, session, submission, component, action)

def start_workflow(req, wfe, session, submission, component, action):
    """
    Set the callbacks and start the workflow by passing the session object and
    calling the 'process' method of the engine.
 
    In case the exception "HaltProcessing" is raised, dump the session.
    In addition, if the variable 'interface_id' is set by some callable,
    redirect to the url corresponding to the interface which will render 
    the interface.
    """
    try:
        wfe.addManyCallbacks('*', submission.workflows[action])
        wfe.setVar('status', 'Running')
        wfe.process([session])
    except HaltProcessing:
        session.dump(wfe)
        if wfe.hasVar('interface_id'): 
            if check_access_user(req, wfe):
                interface_id = wfe.getVar('interface_id')
                redirect_to_url(req, CFG_SITE_URL + '/submitng/%s/%s/%s/'
                                % (component, action, session.session_id) + interface_id)
            else:
                return page("Access denied.", "This user is not authorized to execute the action.")
    

def processData(req, form, wfe, session, submission):
    """
    Assign the form data to the session.
    """
    # trim 'submitted' from the uri.
    session['uri'] = CFG_SITE_URL + req.uri[:-10]
    interface_id = wfe.getVar('interface_id')
    for element in submission.interfaces[interface_id]:
        element_names = element.get_name()
        if type(element_names) != list: element_names = [element_names]
        for name in element_names:
            if form.has_key(name):
                value = str(form[name])
                #if hasattr(value, 'file'):
                ## in value.file you have an opened file, that you can read, and hence 
                ## write somewhere.
                ## moreover in value.filename you have a hint on the filename.
                ## Don't trust it
                ## It's a file. Do whatever is necessary
                    #pass
                #else:
                    #value = str(value)
                #element.set_value(value)
                session[name] = value


class WebInterfaceNGSubmit(WebInterfaceDirectory):

    _export = [''] 

    def __init__(self):
        #Initialize the list of available doctypes 
        #and the list of actions for a chosen doctype.
        self._doctypes = ['Journals', 'Papers']
        self._doctype_actions = []

    def _lookup(self, component, path):
                        
        def _handler(req, form):
            return self.websubmit_handler(req, form, component, path)

        return _handler, []


    def index(self, req, form):
        #Compose the html and display the list of doctypes.
        html = ''
        for i in range(len(self._doctypes)):
            html += '<html><body><a href="%s/submitng/%s">%s</a></body></html> <br/>' \
                     % (CFG_SITE_URL, self._doctypes[i], self._doctypes[i]) 
        return page('Choose Doctype: ', html)

    def websubmit_handler(self, req, form, component, path):
        if component == '':
            redirect_to_url(req, CFG_SITE_URL + '/submitng')
        if component in self._doctypes:
            #list of actions for a chosen doctype.
            self._doctype_actions = ['submit']
            if not path:
                #Compose the html and display the avaiable actions(workflows)
                html = '<a href="%s/submitng/%s/submit">Submit</a>' % (CFG_SITE_URL, component)
                return page(component + '-' + 'Submit', html )
            elif path[0] in self._doctype_actions:
                action = path[0]
                #remove any trailing '/'s
                while path and path[-1] == '':
                    path = path[:-1]
                if len(path) == 1:
                #Create a session, a workflow engine and a submission.
                #Then, start the workflow corresponding to the action and the doctype.
                    session = WebSubmitSession(component)
                    wfe = GenericWorkflowEngine()
                    wfe.setVar('doctype', component)
                    wfe.setVar('status', 'Started.')
                    submission = WebSubmitSubmission(component, session) 
                    start_workflow(req, wfe, session, submission, component, action)

                else:
                #length of the path is grater than 1. 
                #Check if the session_id is valid.
                    try:
                        UUID(path[1])
                    except ValueError:
                        return page("Improper Path. Session number not valid.", '')
                    session_id = path[1]
                    session = WebSubmitSession(component, session_id)
                    wfe = session.load()
                    
                    if len(path) == 2 or wfe.getVar('status') in ['Completed', 'completed']:
                        return page("Status", 
                                    "Work Flow Status for the submission: %s" % wfe.getVar('status'))
                        
                    elif check_access_user(req, wfe):
                        if len(path) == 3 and wfe.hasVar('interface_id'):
                            submission = WebSubmitSubmission(component, session)
                             
                            if submission.interfaces.has_key(path[2]):
                            #A form must be displayed.
                                return page(component + " - " + action, 
                                            submission.interfaces[path[2]].get_html())
                                
                            elif path[2] == "submitted":
                            #A form has been submitted.
                                processData(req, form, wfe, session, submission)
                                resume_workflow(req, wfe, session, submission, component, action)
                                session.dump(wfe)
                                return page("Thank You.", 
                                            "The status of this submission work flow: %s" % wfe.getVar('status'))
                    
                    else:
                        return page("Authorization failed.", 
                                    "The user is denied access to this url.")
 
    #req.write("Namaskaaram Rajavaaru. Itlu, Invenio. " + str(user_info))
    #redirect_to_url(req, '%s/submitng?%s' % (CFG_SITE_URL, req.args))

    __call__ = index
