from invenio.webinterface_handler import wash_urlargd, WebInterfaceDirectory
from invenio.webpage import page, pageheaderonly, pagefooteronly
from invenio.urlutils import redirect_to_url
from invenio.config import CFG_ETCDIR, CFG_WEBDIR, CFG_SITE_URL

import os
import os.path
import sys
import re
from uuid import uuid4


APP_NAME = "websubmitbezirg"
APP_URL = CFG_SITE_URL + '/' + APP_NAME
APP_ETC_DIR = os.path.join(CFG_ETCDIR, APP_NAME)
APP_WEB_DIR = os.path.join(CFG_WEBDIR, APP_NAME + "-static")


sys.path.append(APP_ETC_DIR)
from checks import *
from elements import *

class WebInterfaceBezirgSubmitPages(WebInterfaceDirectory):
    _exports = ['']

    def index(self, req, form):
        redirect_to_url(req, APP_URL + '/submit')


            
    def _lookup(self, component, path):

        def list_doctypes(req, form, component, path):
            title = "Choose Doctype"
            html = ""

            for doctype in filter(lambda d: os.path.isdir(os.path.join(APP_WEB_DIR,d)), os.listdir(APP_WEB_DIR)):
                doctype_url = APP_URL + '/submit/'+ doctype
                html += '<a href="%s">%s</a><br>' % (doctype_url, doctype)        
            if not html:
                html = "No doctype"

            return page(title, html)
        

        def list_actions(req, form, component, path):
            title = "Choose Action"
            html = ""

            doctype = path[0]

            doctype_dir = os.path.join(APP_ETC_DIR, doctype)
            if os.path.exists(doctype_dir):
                for action in filter(lambda d: os.path.isdir(os.path.join(doctype_dir, d)), os.listdir(doctype_dir)):
                    action_url = req.uri.rstrip('/') + '/' + action
                    html += '<a href="%s">%s</a><br>' % (action_url, action)
                if not html: # no actions in the doctype
                    html = "Empty doctype, no actions"
            else: # no doctype dir in etc
                html = "No such doctype"

            return page(title, html)
   

        def init_submission(req, form, component, path):
            doctype = path[0]
            action = path[1]
            if os.path.exists(os.path.join(APP_WEB_DIR, doctype, action, "bootstrap.js")):
                uuid = uuid4()
                redirect_to_url(req, req.uri.rstrip('/') + '/' + str(uuid))
            elif os.path.exists(os.path.join(APP_WEB_DIR, doctype, action)):
                title = "Error"
                html = "Empty action, no submission"
                return page(title, html)
            else:
                title = "Error"
                html = "No such doctype/action"
                return page(title, html)


        def resume_submission(req, form, component, path):
            
            doctype = path[0]
            action = path[1]

            if os.path.exists(os.path.join(APP_WEB_DIR, doctype, action)):
                title = "Submission Form"
                html = ""
                uuid = path[2]

                submission_url = "/%s-static/%s/%s" % (APP_NAME, doctype, action)

                metaheaderadd = '<link rel="stylesheet" href="%(url)s/bootstrap.css" type="text/css" /> <meta name="pygwt:module" content="%(url)s/bootstrap">' % {"url": submission_url}

                html += '<script language="javascript" src="%s/bootstrap.js"></script> <div id="bootstrap"></div><div style="display:none" id="_doctype">%s</div><div style="display:none" id="_action">%s</div>' % (submission_url, doctype, action)

                return page(title, html, metaheaderadd= metaheaderadd)
            else:
                title = "Error"
                html = "No such doctype/action"
                return page(title, html)


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
                return "The form contains errors (server-side)"
            else:
                return "The form is valid"


        def dispatcher(req, form):
            dispatch_table = {('submit',0): list_doctypes,         # GET /websubmitbezirg/submit
                              ('submit',1): list_actions,          # GET /websubmitbezirg/submit/DOCTYPE
                              ('submit',2): init_submission,       # GET /websubmitbezirg/submit/ACTION
                              ('submit',3): resume_submission,     # GET /websubmitbezirg/submit/ACTION/UUID
                              ('validate', 0): validate_submission # POST /websubmitbezirg/validate
                              }
            for url,callback in dispatch_table.iteritems():
                if url[0] == component and url[1] == len(path):
                    return callback(req, form, component, path)


        return dispatcher, []

    __call__ = index


