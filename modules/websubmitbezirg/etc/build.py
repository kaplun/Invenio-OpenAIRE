#!/usr/bin/python                                                                                                                                              

import subprocess
import os
import os.path
from imp import load_source
from shutil import copyfile

from invenio.config import CFG_WEBDIR, CFG_ETCDIR, CFG_PYLIBDIR
from invenio.websubmitbezirg_engine import Workflow


APP_NAME = "websubmitbezirg"
APP_ETC_DIR = os.path.join(CFG_ETCDIR, APP_NAME)
APP_WEB_DIR = os.path.join(CFG_WEBDIR, APP_NAME + "-static")

if __name__ == "__main__":

    # list doctypes
    doctypes =  [doctype_file[:-3] for doctype_file in os.listdir(APP_ETC_DIR) if doctype_file.endswith(".py") and not doctype_file in ["build.py", "bootstrap.py"]]

    for doctype in doctypes:
        doctype_file = os.path.join(APP_ETC_DIR, doctype+'.py')

        doctype_web_dir = os.path.join(APP_WEB_DIR, doctype)
        if not os.path.exists(doctype_web_dir):
            os.mkdir(doctype_web_dir) # create www/websubmitbezirg-static/DOCTYPE/

        doctype_module = load_source(doctype, doctype_file)

        # list workflows in the doctype
        workflows_dict = [(var, val) for var, val in vars(doctype_module).items() if isinstance(val,Workflow)]

        for workflow_var, workflow_obj in workflows_dict:

            # create www/websubmitbezirg-static/DOCTYPE/ACTION
            action_web_dir = os.path.join(APP_WEB_DIR, doctype, workflow_obj.action)
            if not os.path.exists(action_web_dir):
                os.mkdir(action_web_dir) 
            
            # create bootstrap
            copyfile(doctype_file, "bootstrap.py")
            bootstrap = open("bootstrap.py", 'a')
            bootstrap.write("\n%s.build_interface()" % (workflow_var))
            bootstrap.close()

            # compile tmp
            subprocess.check_call(["/opt/invenio/lib/pyjamas/bin/pyjsbuild",                                                                             
                                   "-d",
                                   "--print-statements",
                                   "-I", CFG_PYLIBDIR, #os.path.join(APP_ETC_DIR, doctype), # action
                                   "-o", action_web_dir,                                                                                   
                                   "bootstrap"])                                                                    
            
            print doctype, workflow_obj.action

        if not workflows_dict:
            print "Empty %s" % (doctype) # Empty DocType/                                                                                                      
        

        os.remove("bootstrap.py")
        os.remove("bootstrap.js")
