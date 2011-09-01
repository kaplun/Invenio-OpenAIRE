"""
The WebController (the C part of the MVC) for the WebSubmission module.

An overview of the URL scheme and the dispatching:

GET       /websubmitbezirg/                     -------> list_doctypes()
GET       /websubmitbezirg/DOCTYPE              -------> list_actions()
GET       /websubmitbezirg/DOCTYPE/ACTION       -------> init_submission()
GET,POST  /websubmitbezirg/DOCTYPE/ACTION/UUID  -------> resume_submission()

"""


from invenio.webinterface_handler import wash_urlargd, WebInterfaceDirectory
from invenio.webpage import page, pageheaderonly, pagefooteronly
from invenio.urlutils import redirect_to_url
from invenio.workflow_engine import GenericWorkflowEngine, HaltProcessing

import os
import os.path
import json
import sys
import re
import fcntl
import cPickle
import cStringIO

from invenio.websubmitbezirg_engine import Interface, Workflow
from invenio.websubmitbezirg_config import APP_NAME, APP_URL, APP_ETC_DIR, APP_WEB_DIR, APP_DATA_DIR

from imp import load_source

from uuid import uuid4, UUID

# The bzip2 compression of the pickled files is commented out
# from shutil import copyfileobj
# from bz2 import BZ2File

class WebInterfaceBezirgSubmitPages(WebInterfaceDirectory):
    _exports = ['']

    def list_doctypes(self, req, form):
        """
        The main page of the module.

        Dispatched from http://INVENIO_ROOT/websubmitbezirg

        Reads the configuration file (config.json)
        and returns all enabled DOCTYPEs.
        """

        title = "Choose Doctype"
        html = ""

        config_file = open(os.path.join(APP_ETC_DIR, "config.json"), 'r')
        config = json.load(config_file)

        for category_ in config:
            category = category_.encode('ascii')
            html += '<h2>%s</h2><ul>' % (category) # hardcoded html; a template would be nicer
            for doctype_, enabled in config[category].items():
                doctype = doctype_.encode('ascii')
                if enabled:
                    doctype_url = APP_URL + '/' + doctype
                    html += '<li><a href="%s">%s</a></li>' % (doctype_url, doctype) # hardcoded html
            html += "</ul>"
        return page(title, html)

    def _lookup(self, component, path):

        # ugly hack to the broken _lookup method
        # treats trailing slashes to the path as supposed to
        while path and path[-1] == '':
            path = path[:-1]


        def list_actions(req, form, component, path):
            """
            The page of a specified DOCTYPE.

            Dispatched from http://INVENIO_ROOT/websubmitbezirg/DOCTYPE

            Returns a list with all the ACTIONs of the DOCTYPE.

            """

            title = "Choose Action"
            html = ""

            
            doctype = component
            doctype_file = os.path.join(APP_ETC_DIR, doctype+".py")
           
            if os.path.exists(doctype_file):

                doctype_module = load_source(doctype, doctype_file) # dynamically load the DOCTYPE.py specification to extract the actions

                # each Workflow inside the DOCTYPE.py has each own name.
                # An action corresponds to a specific Workflow. So the name of the action is the name of the Workflow
                actions = [val.action for var, val in vars(doctype_module).items() if isinstance(val,Workflow)]

                for action in actions:
                    action_url = req.uri.rstrip('/') + '/' + action
                    html += '<a href="%s">%s</a><br>' % (action_url, action)
                if not actions: # no actions in the doctype
                    html = "Empty doctype, no actions"
            else: # no doctype dir in etc
                html = "No such doctype"

            return page(title, html)
   

        def init_submission(req, form, component, path):
            """
            Initialize the submission page.

            Dispatched from http://INVENIO_ROOT/websubmitbezirg/DOCTYPE/ACTION

            1. Creates a new UUID.
            2. Starts the workflow engine and maybe execute some initial processes that come before the 1st page in the workflow.
            3. Halts the engine, pickles it and dumps it.
            4. Redirects the user to http://INVENIO_ROOT/websubmitbezirg/DOCTYPE/ACTION/UUID, which is a new unique session for the user.
            """

            doctype = component
            doctype_file = os.path.join(APP_ETC_DIR, doctype+".py")
            action = path[0]

            if os.path.exists(doctype_file):

                # workflows indexed by action name
                doctype_module = load_source(doctype, doctype_file)
                workflows = {}
                for var,val in vars(doctype_module).items():
                    if isinstance(val, Workflow):
                        workflows[val.action] = val

                if action in workflows:
                    # create a new UUID
                    uuid = uuid4()

                    pickled_engine_path = os.path.join(APP_DATA_DIR, str(uuid), str(uuid) + ".pickled") # the pickled filename
                    os.mkdir(os.path.join(APP_DATA_DIR, str(uuid))) # the directory containing the pickled file

                    # spawn a new workflow engine instance
                    wfe = GenericWorkflowEngine()
                    # wfe.addManyCallbacks('*', workflows[action].processes)
                    wfe.setWorkflow(workflows[action].processes)
                    wfe.setVar('uuid', uuid)
                    wfe.setVar('status', 'Running')
                    
                    try:
                        # Run the initial processes before the 1st page
                        pickled_engine_file = open(pickled_engine_path, 'w')
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_EX)
                        wfe.start() # start the workflow
                    except HaltProcessing:
                        # dump
                        cPickle.dump(wfe, pickled_engine_file)
                    finally:
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_UN)
                        pickled_engine_file.close()


                    # redirect to UUID
                    redirect_to_url(req, req.uri.rstrip('/') + '/' + str(uuid))
                else:
                    html = "No such doctype/action"
            else:
                html = "No such doctype"

            return page(title, html)


        def resume_submission(req, form, component, path):
            """
            The actual submission page that corresponds to a unique session.

            Dispatched from http://INVENIO_ROOT/websubmitbezirg/DOCTYPE/ACTION/UUID

            GET requests: Show the current page to the user
            POST requests: Deal with input by the user

            1. Resume the engine marked with the UUID
            2. Do stuff to the engine and dump it.
            """
            
            doctype = component
            doctype_file = os.path.join(APP_ETC_DIR, doctype+".py")
            action = path[0]
            uuid = path[1]

            # check for the validity of the uuid
            try:
                UUID(uuid)
            except:
                return "Invalid uuid"

            pickled_engine_path = os.path.join(APP_DATA_DIR, str(uuid), str(uuid) + ".pickled")

            if os.path.exists(pickled_engine_path):
                doctype_module = load_source(doctype, doctype_file)
            else:
                return "Session/engine does not exist"
            
            ## Workflow from the submit file

            # workflows indexed by action name
            workflows = {}
            for var,val in vars(doctype_module).items():
                if isinstance(val, Workflow):
                    workflows[val.action] = val

            if action in workflows:
                workflow = workflows[action]
            else:
                title = "Error"
                html = "No such doctype/action"
                return page(title, html)


            req_method = req.get_method()


            if req_method == 'GET':
                ##### GET
                # A user asks for the submission page
                # A somewhat "static" html file is returned
                # The html file wraps the corresponding bootstrap.js and puts the invenio header and footer
                
                title = "Submission Form"
                html = ""
                
                app_static_url = "/%s-static" % (APP_NAME)
                
                submission_static_url = "/%s-static/%s/%s" % (APP_NAME, doctype, action)
                    
                metaheaderadd = '<link rel="stylesheet" href="%(app_static_url)s/bootstrap.css" type="text/css" /> <meta name="pygwt:module" content="%(url)s/bootstrap">' % {"app_static_url": app_static_url, "url": submission_static_url}

                html += '<script language="javascript" src="%s/bootstrap.js"></script> <div id="bootstrap"></div>' % (submission_static_url)

                return page(title, html, metaheaderadd= metaheaderadd)

            elif req_method == 'POST':
                # the POST response is JSON encoded
                # Similar interface to a JSON-RPC call:  {'method': STR, 'params': JSON}
                # extract the keys
                method = form['method']
                params = json.loads(form['params'])


                ##### POST
                # 4 different "JSON-RPC" calls by the user
                # A 'submit_form' that contaitns the filled form by the user
                # A 'validate' AJAX call by the user to validate a specific element of a Submission Page
                # A 'validate_all' AJAX call by the user to validate all elements of a Submission Page
                # A 'current_page' AJAX call by the user asking for the next page to show


                ##### 'current_page' call
                if method == 'current_page':
                    pickled_engine_file = open(pickled_engine_path, 'r+')
                    try:
                        # the response is blocking. it returns when the engine halts
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_EX)
                        wfe = cPickle.load(pickled_engine_file)
                        __current_page_name = wfe.getVar('__current_page_name')
                        output_form = wfe.getVar('output_form')
                    except:
                        result = "error"
                    else:
                        result = {'__current_page_name': __current_page_name, 'output_form': output_form}
                    finally:
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_UN)
                        pickled_engine_file.close()



                ##### 'submit_form' call
                elif method == 'submit_form':
                    pickled_engine_file = open(pickled_engine_path, 'r+')
                    try:
                        # the response is non-blocking. if the engine runs when the form is submitted return error
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                        wfe = cPickle.load(pickled_engine_file)

                        wfe.setWorkflow(workflow.processes)

                        # convert form from FieldStorage to dict
                        # FieldStorage contains cStringIO instances, that are not pickle-serializable 
                        form_dict = {}
                        for k,v in form.items():
                            form_dict[k] = v.value


                        wfe.setVar("input_form", form_dict)

                        wfe.resume()

                        
                        if wfe.hasVar("__finished"):
                            # the engine/processing  is done
                            cPickle.dump(wfe, pickled_engine_file)
                            # BZIP2 Compression of the engine
                            # commented out
                            # pickled_engine_compressed_file = BZ2File(pickled_engine_path+".bz2", 'w')
                            # copyfileobj(pickled_engine_file, pickled_engine_compressed_file)
                            # pickled_engine_compressed_file.close()
                            # os.remove(pickled_engine_path)
                            result = "ok"
                    except IOError:
                        # the engine is running
                        result = "error"
                    except HaltProcessing:
                        # dump
                        pickled_engine_file.close()
                        pickled_engine_file = open(pickled_engine_path, 'r+')                        
                        cPickle.dump(wfe, pickled_engine_file)
                        result = "ok"
                    finally:
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_UN)
                        pickled_engine_file.close()



                ##### 'validate' call
                elif method == 'validate':
                    element_name = params['element_name']
                    element_input = params['element_input']

                    pickled_engine_file = open(pickled_engine_path, 'r+')
                    try:
                        # the response is blocking. it returns when the engine halts
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_EX)
                        wfe = cPickle.load(pickled_engine_file)
                        __current_page_name = wfe.getVar('__current_page_name')
                    except:
                        result = "error"
                    else:
                        current_page = [p for p in workflow.pages if p.name==__current_page_name][0]
                        element = [e for e in current_page.elements if hasattr(e,'getName') and e.getName() == element_name][0]
                        result = element.checkFunction(element_input)
                    finally:
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_UN)
                        pickled_engine_file.close()
                        



                ##### 'validate_all' call                        
                elif method == 'validate_all':
                    pickled_engine_file = open(pickled_engine_path, 'r+')
                    try:
                        # the response is blocking. it returns when the engine halts
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_EX)
                        wfe = cPickle.load(pickled_engine_file)
                        __current_page_name = wfe.getVar('__current_page_name')
                    except:
                        result = "error"
                    else:
                        current_page = [p for p in workflow.pages if p.name==__current_page_name][0]
                        elements = current_page.elements
                        for k,v in form.items():
                            for element in elements:
                                if hasattr(element, 'checkFunction') and hasattr(element, 'getName') and element.getName() == k:
                                    if not element.checkFunction(v):
                                        return json.dumps({'method': method, 'result': False}) # server-side validation failed, exit
                        result = True # server-side validation suceeded for all elements
                # the response is of the form {'method': STR, 'result': JSON}
                return json.dumps({'method': method, 'result': result})


        def dispatcher(req, form):
            """
            The request dispatcher.
            It is not a regexp dispatcher. It is based on incremental path levels.
            """

            dispatch_table = [list_actions,          # GET       /websubmitbezirg/DOCTYPE
                              init_submission,       # GET       /websubmitbezirg/DOCTYPE/ACTION
                              resume_submission,     # GET,POST  /websubmitbezirg/DOCTYPE/ACTION/UUID
                              ]
            return dispatch_table[len(path)](req, form, component, path)

        return dispatcher, []

    __call__ = index = list_doctypes # the main page of the module


