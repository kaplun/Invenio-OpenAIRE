#!/usr/bin/python                                                                                                                                              

import subprocess
import os
import os.path

from invenio.config import CFG_WEBDIR, CFG_ETCDIR

APP_NAME = "websubmitbezirg"
APP_ETCDIR = os.path.join(CFG_ETCDIR, APP_NAME)
APP_WEBDIR = os.path.join(CFG_WEBDIR, APP_NAME + "-static")

if __name__ == "__main__":
    doctypes =  filter(os.path.isdir, os.listdir(APP_ETCDIR))
    for doctype in doctypes:
        doctype_etc_dir = doctype
        doctype_web_dir = os.path.join(APP_WEBDIR, doctype)
        if not os.path.exists(doctype_web_dir):
            os.mkdir(doctype_web_dir)
        actions = filter(os.path.isdir, [os.path.join(doctype_etc_dir,subdir) for subdir in os.listdir(doctype_etc_dir)])
        if not actions:
            print "Empty %s" % (doctype) # Empty DocType/                                                                                                      
        for action in actions:
            action_etc_dir = os.path.join(action)
            action_web_dir = os.path.join(APP_WEBDIR, action)
            if not os.path.exists(action_web_dir):
                os.mkdir(action_web_dir)
            if os.path.exists(os.path.join(action_etc_dir, "bootstrap.py")):
                subprocess.check_call(["/opt/invenio/lib/pyjamas/bin/pyjsbuild",                                                                             
                                       "-d",
                                       "--print-statements",
                                       "-I", action,
                                       "-o", action_web_dir,                                                                                   
                                       "bootstrap"])                                                                    
                print os.path.join(action, "bootstrap.py")
            else:
                print "Empty %s" % (action) # Empty DocType/Action/
