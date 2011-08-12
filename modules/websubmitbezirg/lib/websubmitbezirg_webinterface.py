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

from shutil import copyfileobj
from bz2 import BZ2File

class WebInterfaceBezirgSubmitPages(WebInterfaceDirectory):
    _exports = ['']

    def list_doctypes(self, req, form):
        title = "Choose Doctype"
        html = ""

        config_file = open(os.path.join(APP_ETC_DIR, "config.json"), 'r')
        config = json.load(config_file)

        for category_ in config:
            category = category_.encode('ascii')
            html += '<h2>%s</h2><ul>' % (category)
            for doctype_, enabled in config[category].items():
                doctype = doctype_.encode('ascii')
                if enabled:
                    doctype_url = APP_URL + '/' + doctype
                    html += '<li><a href="%s">%s</a></li>' % (doctype_url, doctype)
            html += "</ul>"
        return page(title, html)

    def _lookup(self, component, path):

        while path and path[-1] == '':
            path = path[:-1]


        def list_actions(req, form, component, path):
            title = "Choose Action"
            html = ""

            doctype = component
            doctype_file = os.path.join(APP_ETC_DIR, doctype+".py")
           
            if os.path.exists(doctype_file):

                doctype_module = load_source(doctype, doctype_file)
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

                    pickled_engine_path = os.path.join(APP_DATA_DIR, str(uuid) + ".pickled")

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
            
            doctype = component
            doctype_file = os.path.join(APP_ETC_DIR, doctype+".py")
            action = path[0]
            uuid = path[1]

            # check for the validity of the uuid
            try:
                UUID(uuid)
            except:
                return "Invalid uuid"

            pickled_engine_path = os.path.join(APP_DATA_DIR, str(uuid) + ".pickled")

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


                # Wrap the 
                # pyjamas bootstrap.js
                # and return it
                title = "Submission Form"
                html = ""
                
                app_static_url = "/%s-static" % (APP_NAME)
                
                submission_static_url = "/%s-static/%s/%s" % (APP_NAME, doctype, action)
                    
                metaheaderadd = '<link rel="stylesheet" href="%(app_static_url)s/bootstrap.css" type="text/css" /> <meta name="pygwt:module" content="%(url)s/bootstrap">' % {"app_static_url": app_static_url, "url": submission_static_url}

                html += '<script language="javascript" src="%s/bootstrap.js"></script> <div id="bootstrap"></div>' % (submission_static_url)

                return page(title, html, metaheaderadd= metaheaderadd)

            elif req_method == 'POST':
                # the request is a form {'method': STR, 'params': JSON}
                method = form['method']
                params = json.loads(form['params'])

                if method == 'current_page':
                    pickled_engine_file = open(pickled_engine_path, 'r+')
                    try:
                        # the response is blocking. it returns when the engine halts
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_EX)
                        wfe = cPickle.load(pickled_engine_file)
                        current_page_name = wfe.getVar('current_page_name')
                        output_form = wfe.getVar('output_form')
                    except:
                        result = "error"
                    else:
                        result = {'current_page_name': current_page_name, 'output_form': output_form}
                    finally:
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_UN)
                        pickled_engine_file.close()


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
                            pickled_engine_compressed_file = BZ2File(pickled_engine_path+".bz2", 'w')
                            copyfileobj(pickled_engine_file, pickled_engine_compressed_file)
                            pickled_engine_compressed_file.close()
                            os.remove(pickled_engine_path)
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

                elif method == 'validate':
                    element_name = params['element_name']
                    element_input = params['element_input']

                    pickled_engine_file = open(pickled_engine_path, 'r+')
                    try:
                        # the response is blocking. it returns when the engine halts
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_EX)
                        wfe = cPickle.load(pickled_engine_file)
                        current_page_name = wfe.getVar('current_page_name')
                    except:
                        result = "error"
                    else:
                        current_page = [p for p in workflow.pages if p.name==current_page_name][0]
                        element = [e for e in current_page.elements if hasattr(e,'getName') and e.getName() == element_name][0]
                        result = element.checkFunction(element_input)
                    finally:
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_UN)
                        pickled_engine_file.close()
                elif method == 'validate_all':
                    pickled_engine_file = open(pickled_engine_path, 'r+')
                    try:
                        # the response is blocking. it returns when the engine halts
                        fcntl.lockf(pickled_engine_file.fileno(), fcntl.LOCK_EX)
                        wfe = cPickle.load(pickled_engine_file)
                        current_page_name = wfe.getVar('current_page_name')
                    except:
                        result = "error"
                    else:
                        current_page = [p for p in workflow.pages if p.name==current_page_name][0]
                        elements = current_page.elements
                        for k,v in form.items():
                            for element in elements:
                                if hasattr(element, 'checkFunction') and hasattr(element, 'getName') and element.getName() == k:
                                    if not element.checkFunction(v):
                                        return json.dumps({'method': method, 'result': False}) # server-side validation failed, exit
                        result = True # server-side validation suceeded for all elements
                # the response is of the form {'method': STR, 'result': JSON}
                return json.dumps({'method': method, 'result': result})

            




        def validate_submission(req, form, component, path):
            doctype = form['doctype']
            action = form['action']
            action_etc_dir = os.path.join(APP_ETC_DIR, doctype, action)

            class ValidationError(Exception):
                pass

            class Interface(object):
                def __init__(self, *args):
                    self.elements = args
                    for inputName, inputValue in form.items():
                        for element in self.elements:
                            if inputName == element.getName() and isinstance(element, Checkable):
                                if not element.checkFunction(inputValue):
                                    raise ValidationError # validation failed

            class Workflow(object):
                pass

            try:
                execfile(os.path.join(action_etc_dir,"bootstrap.py"))
            except ValidationError:
                #req.content_type = "text/plain"
                return json.dumps({'valid': False})
            else:
                return json.dumps({'valid': True})


        def dispatcher(req, form):
            # incrementing the path
            dispatch_table = [list_actions,          # GET /websubmitbezirg/DOCTYPE
                              init_submission,       # GET /websubmitbezirg/DOCTYPE/ACTION
                              resume_submission,     # GET /websubmitbezirg/DOCTYPE/ACTION/UUID
                              ]
            return dispatch_table[len(path)](req, form, component, path)

        return dispatcher, []

    __call__ = index = list_doctypes


