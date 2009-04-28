## $Id: websubmit_engine.py,v 1.9 2007/07/30 14:00:58 diane Exp $

## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007 CERN.
##
## CDS Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## CDS Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with CDS Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""WebSubmit: the mechanism for the submission of new records into CDS Invenio
   via a Web interface.
"""

__revision__ = "$Id: websubmit_engine.py,v 1.9 2007/07/30 14:00:58 diane Exp $"

## import interesting modules:
import string
import os
import sys
import time
import types
import re
import shutil
from mod_python import apache

from invenio.config import \
     bibconvert, \
     cdslang, \
     cdsname, \
     images, \
     pylibdir, \
     storage, \
     urlpath, \
     version, \
     weburl
from invenio.dbquery import run_sql, Error
from invenio.access_control_engine import acc_authorize_action
from invenio.access_control_admin import acc_is_role
from invenio.webpage import page, create_error_box
from invenio.webuser import getUid, get_email, collect_user_info
from invenio.websubmit_config import *
from invenio.file import *
from invenio.messages import gettext_set_language, wash_language

from websubmit_dblayer import \
     get_storage_directory_of_action, \
     get_longname_of_doctype, \
     get_longname_of_action, \
     get_num_pages_of_submission, \
     get_parameter_value_for_doctype, \
     submission_exists_in_log, \
     log_new_pending_submission, \
     log_new_completed_submission, \
     update_submission_modified_date_in_log, \
     update_submission_reference_in_log, \
     update_submission_reference_and_status_in_log, \
     get_form_fields_on_submission_page, \
     get_element_description, \
     get_element_check_description, \
     get_form_fields_not_on_submission_page, \
     function_step_is_last, \
     get_collection_children_of_submission_collection, \
     get_submission_collection_name, \
     get_doctype_children_of_submission_collection, \
     get_categories_of_doctype, \
     get_doctype_details, \
     get_actions_on_submission_page_for_doctype, \
     get_action_details, \
     get_parameters_of_function, \
     get_details_of_submission, \
     get_functions_for_submission_step, \
     get_submissions_at_level_X_with_score_above_N, \
     submission_is_finished

import invenio.template
websubmit_templates = invenio.template.load('websubmit')
## -------- NEW STUFF FOLLOWS ---- NEW STUFF FOLLOWS --------------
import invenio.miniparser
from websubmit_elements.WSET_RadioButton import WSET_RadioButton
import cgi
from xml.dom.minidom import parseString
#from xml.sax import parseString, ContentHandler, SAXParseException
from invenio.config import etcdir
CFG_WEBSUBMIT_ELEMENTS_IMPORT_PATH = "invenio.websubmit_elements"
CFG_WEBSUBMIT_ELEMENTS_LIBRARY = etcdir + "/websubmit/element_library.xml"
CFG_WEBSUBMIT_CHECKS_IMPORT_PATH = "invenio.websubmit_checks"
CFG_WEBSUBMIT_SUBMISSION_TEMPLATES = etcdir + "/websubmit"
CFG_WEBSUBMIT_COLLECTION_NUMBER_OF_LEVEL = 5
CFG_WEBSUBMIT_CATEGORY_NUMBER_OF_LEVEL = 5
from invenio.websubmit_templates import *
#put CFG_BIBRECORD_PARSERS_AVAILABLE in config.py ??? 
from invenio.bibrecord_config import *
import pyRXP
# find out about the best usable parser:
def warnCB(s):
    print s

## WSC calls:
def perform_form_input_checking(wsc_requests, wse_objects, interface_language):
    """Given a set of WSET elements, and a list of checks that are to be
       performed upon various elements, perform the checks upon the relevant
       elements, recording whether or not any checks are failed, and in the
       event of any failures, building up a list of error-messages to be
       returned to WebSubmit core for display.

       @param wsc_requests: (list) - each index in the list is actually
        another list in the following structure:
            [ <reference to wsc function>,
              "param1, param2, param3, ...",
              { "en" : "Failure message in English",
                "fr" : "Failure message in French",
                "de" : "Failure messahe in German",
                "ru" : "Failure message in Russian",
                ...,
              }
            ]
        Basically, the first cell contains a reference to the executable
        function; the second cell is a string that represents the parameters
        that are to be passed to the function; and the third cell is a
        dictionary containing the error message to be displayed upon the
        check's failure in the various supported languages.
        So, for example, the wsc_requests parameter list may look something
        like this:

            [ [ <reference to wsc_string_length>,
                "wse_buildingname, 4, 30,",
                { "en" : "Building name must be between 4 and 30 characters in
                          length.",
                }
              ]
              [ <reference to wsc_string_length>,
                "wse_surname, 0, 100",
                { "en" : "The maximum length of surname is 110 characters.",
                }
              ]
            ]
        NOTE: When treating the "parameters" string for a WSC, any items
        beginning with the prefix "wse_" (e.g. "wse_startdate") will be treated
        as WSET objects. This means WSET fields MUST be named with a "wse_"
        prefix.
       @param wse_objects: (dictionary) - contains the WSE objects that
        appear on the interface, keyed by their names. For example:
           { "author"   : <WSET_Author instance>,
             "title"    : <WSET_TextArea instance>,
             "keywords" : <WSET_TextArea instance>,
             "subject"  : <WSET_Select instance>,
           }
       @param interface_language: (string) -  the code for the language of the
        interface. This is used to choose the correct language for any error-
        messages that are generated.
       @return: (list) - containing 2 cells: (boolean, list).
        The first cell of the tuple, the boolean value, is a flag indicating
        whether or not any checks failed. A boolean True value indicates that at
        least one check failed, and WebSubmit should act appropriately; A
        boolean False indicates that no checks failed.
        The second cell of the tuple contains a list of strings, with each
        string being an error message created by a failed check.
    """
    ## Flag to indicate whether or not one of the checks failed:
    check_failure = False

    ## A list in which to keep any error-messages that are to be displayed as a
    ## result of the failure of wsc checks:
    encountered_error_messages = []

    ## Loop through all WSC requests, get the function, treat the parameters
    for checking_request in wsc_requests:
        ## get a reference to the WSC:
        wsc_function = checking_request[0]
        ## Get the arguments to be passed to the function in their raw
        ## "string" form:
        wsc_args_string = checking_request[1]
        ## Get the error-messages dictionary:
        error_messages = checking_request[2]
        
        ## Now parse the arguments string into a tuple:
        argstring_parser = invenio.miniparser.Parser(wsc_args_string, wse_objects)
        args_tuple = argstring_parser.parse()

        ## Call the wsc, passing it the arguments tuple:
        check_status = wsc_function(*args_tuple)

        ## Did the check fail?
        if check_status != 0:
            ## Yes - a non-zero status code was returned by this check.
            ## Set the check-failure flag:
            check_failure = True

            ## Now add the error-message for this check-failure in the
            ## language appropriate to the interface:
            if interface_language in error_messages:
                ## This check has an error message in the interface
                ## language: use it:
                error_string = error_messages[interface_language]
            elif cdslang in error_messages:
                ## This check didn't have an error message in the interface
                ## language. Did it have an error message written in the
                ## default language "cdslang"? If so, use it:
                error_string = error_messages[cdslang]
            elif len(error_messages.keys()) > 0:
                ## Although this check didn't have an error message in either
                ## the interface language or the default "cdslang" language,
                ## it did have an error message in at least one language.
                ## Therefore, we simply take the first error message that we
                ## find in the dictionary and use that:
                error_string = error_messages.values()[0]
            else:
                ## The Admin hasn't provided an error message. Make a default
                ## Unknown error message:
                error_string = "An unidentified problem was encountered with" \
                               " the data enterted into one of the form " \
                               "fields. Please check and try again."

            ## Now append the error string into the list of error messages:
            encountered_error_messages.append(error_string)

    ## return the check-failed flag, and the error-messages:
    return (check_failure, encountered_error_messages)




#replace get_WSET_class_reference to be able to retrieve either a class or a function
#from a given module
def get_reference_from_name(name,
                            import_path=CFG_WEBSUBMIT_ELEMENTS_IMPORT_PATH):
    """Given parameter name, get and return a reference to a class or function.
       Note. It is assumed that each name will exist as a class or function in
       the module having the same name
       E.g. the element 'WSET_Text', should exist as a class in the file
       'WSET_Text.py', in the directory designated by import_path 'CFG_WEBSUBMIT_ELEMENTS_IMPORT_PATH'.

       @param name: (string) - the name of the function or class which should be retrieved
       @param import_path: (string) - the base of the path to the module assigned by param name 
       @return: (class-type/function) - the reference to the class/function named by the name parameter.
    """
    try:
        ## Build the path to the module:
        module_path = import_path + "." + name
        ## Import that module:
        module = __import__(module_path)
        ## Loop through all of the components in the path to the imported
        ## module and obtain a reference to that component's module:
        components = module_path.split(".")
        for comp in components[1:]:
            module = getattr(module, comp)
    except Exception, err:
        ## If there was an exception while doing this, propagate it upwards:
        ## FIXME
        raise err
    else:
        ## From the reference to the module designated by name, get a reference to the
        ## class/function itself:
        try:
            ## Store the reference to the class in a local variable:
            built_in_object = module.__dict__['%s' % name]
        except KeyError, err:
            ## The class/function did not exist in its module!
            raise err
        else:
            ## Return the reference to the class/function itself:
            return built_in_object
        

## HERE IS A TEMPORARY FAKE WSO CLASS DEFINITION:
class InvenioWebSubmitSubmissionObject(object):
    def __init__(self, req, lang):
        """Initialise a wso.
           @param req: (mod_python.Request object) - the Apache request object.
            This req object also contains a member "form", which is a
            mod_python.util.FieldStorage object and contains all of the data
            submitted to the server on the last visit to the page.
        """
        ## Keep a local reference to the request object:
        self.req = req
        ## Store the language:
        self.lang = lang
        ## Extract the WSET fields from the request object's form object:
        self.submitted_form_fields = get_wset_fields_from_form(req.form)


def get_wset_fields_from_form(form):
    """From a submitted FORM, capture all of the fields whose names begin with
       "WSET".  Return a dictionary containing these WSET* fields.

       Note:
        A WSET element object re-creates itself with the values that the user
        entered into its fields on the last visit to the page, and to do this
        it must have access to the form so that it can retrieve its own values.
        Since it needs access to all of the form values in order to retrieve its
        own values, it's nicer if it only has access to the WSET fields. That
        way, it can't do anything with system-specific fields.
        This function is used to produce the dictionary of WSET fields before
        WSET-object creation, then.
       @param form: (mod_python.util.FieldStorage) - the CGI "form".
        It is treated as though it were a dictionary.
       @return: (dictionary) - of mod_python.util.Field items keyed by their
        (WSET) field names.
    """
    ## A dictionary to store all of the WSET* fields in:
    wset_fields = {}
    ## A list of all of the variables passed into the "form" (i.e. all of
    ## the fieldnames):
    form_fieldnames = form.keys()

    ## Loop through all of the form fields. If a field whose name starts with
    ## "WSET" is found, add it into dictionary of "WSET" fields.
    for field_name in form_fieldnames:
        if field_name.startswith("WSE_"):
            ## This is a WSET field. Take a reference to it:
            wset_fields[field_name] = form[field_name]

    ## Return the dictionary of WSET fields
    return wset_fields


def read_library(xmltext=""):
    """
    @param xmltext: xml based text containing the library of the elements
    This function builds a dictionnary where the key are the name of the
    elements and the values are the element node
    @return the dictionnary
    """
    dom = parseString(xmltext)
    elements_by_name = {}
    for element in dom.getElementsByTagName("element"):
        try:
            elements_by_name[element.getAttribute("name").encode("utf-8")] = element
        except AttributeError, err:
            #FIXME
            #Attribute name is mandatory
            raise err
    return elements_by_name

#parse the library - FIXME need to user data cacher
library = read_library(open(CFG_WEBSUBMIT_ELEMENTS_LIBRARY, "r").read())

def create_submission(wso,
                      parser = "dom", 
                      templates=[CFG_WEBSUBMIT_SUBMISSION_TEMPLATES + "/CTH.xml"]):
    submission = []
    for template in templates:
        if os.access(template, os.F_OK|os.R_OK):
            ## Parse Template:
            try:
                if parser == "dom":
                    submission.append(create_interface_minidom(open(template).read(), wso))
                #FIXME rxp parser is not up to date
                #else:
                    #wse_elements.append(create_interface_RXP(open(template).read(), wso))
            except Exception, err:
                ## Problem parsing the XML - FIXME
                raise err
        else:
            ## Fatal error - can't read template - FIXME
            raise Exception()
    ## Do something with our objects
    #return websubmit_templates.tmpl_create_page(wse_elements)
    #return create_interface_html(wse_elements)
    #FIXME: at the time beeing we consider only the submission for the first template
    return submission[0]

def preform_request_end_submission(req, lang=cdslang):
    body = ""
    ## create a WebSubmitSubmissionObject:
    wso = InvenioWebSubmitSubmissionObject(req, lang)
    ## on this submission page:
    interface, checker, wse_objects = create_submission(wso)

    (check_failure, error_messages) = \
                   perform_form_input_checking(checker, wse_objects, lang)

    if check_failure:
        ## Something went wrong - redraw interface
        body += create_submission_form(lang, interface, wse_objects, error_messages)
    else:
        body += "Now I would do the functions here"

    return body
        

def perform_request_create_submission_interface(req, lang=cdslang):
    """This function creates the submission-form that the user sees and uses
       to submit new records into CDS Invenio via WebSubmit.
       @param req: (mod_python.Request object) - the Apache request object.
        This req object also contains a member "form", which is a
        mod_python.util.FieldStorage object and contains all of the data
        submitted to the server on the last visit to the page.
       @param lang: (string) - the language of the interface. Defaults to
        cdslang if not provided.
       @return: (string) - the HTML page-body.
    """
    ## A string to hold the page-body:
    body = ""

    ## create a WebSubmitSubmissionObject:
    wso = InvenioWebSubmitSubmissionObject(req, lang)

    ## on this submission page:
    interface, checker, wse_objects = create_submission(wso)
    body += create_submission_form(lang, interface, wse_objects)

##    body += "There is a form here. Click the button to submit it."
##     body += """<br /><br />

##     <form action="/submit" method="post">"""
    
##     #create html for containers and corresponding elements
##     for items in interface:
##         container = items["container_label"]
##         elements = items["elements"]
##         element_html = ""
##         for element_name in elements:
##             element_html += Template().tmpl_element(wse_objects[element_name].get_html(), cgi.escape(lang, 1))
##         body +=  Template().tmpl_comtainer(container, elements, cgi.escape(lang, 1)) % {'elements' : element_html}

##     body += """
##     <input type="hidden" name="ln" value="%s" />
##     <input type="submit" name="WebSubmitFormSubmit" value="Finish Submission" />
##     </form>""" % cgi.escape(lang, 1)

    return body

def create_submission_form(lang,
                           interface,
                           wse_objects,
                           error_messages=None):
    ## Sanity check for errors:
    if error_messages is None:
        error_messages = []
    
    body = ""
    body += "There is a form here. Click the button to submit it."
    body += """<br /><br />"""

    for error_message in error_messages:
        body += "%s<br />" % error_message

    body += """
    <form action="/submit" method="post">"""
    
    #create html for containers and corresponding elements
    for items in interface:
        container = items["container_label"]
        elements = items["elements"]
        element_html = ""
        for element_name in elements:
            element_html += Template().tmpl_element(wse_objects[element_name].get_html(), cgi.escape(lang, 1))
        body +=  Template().tmpl_comtainer(container, elements, cgi.escape(lang, 1)) % {'elements' : element_html}

    body += """
    <input type="hidden" name="ln" value="%s" />
    <input type="submit" name="WebSubmitFormSubmit" value="Finish Submission" />
    </form>""" % cgi.escape(lang, 1)

    return body


def get_wset_objects_for_submission(wso):
    """FIXME: THIS METHOD IS A TEST DRIVER MAKING A DUMMY LIST OF
              WSET_* OBJECTS.
    """
    wset_list = []

    el1_lab = { "fr" : "Animaux",
                "en" : "Animals",
                "de" : "Tiele",
              }

    el1_opt = [
                { "value"    : "BIRD",
                  "label"    : { "fr" : "un oiseau",
                                 "en" : "a bird",
                                 "de" : "ein Vogel",
                               },
                  "selected" : "NO",
                },
                { "value"    : "HORSE",
                  "label"    : { "fr" : "un cheval",
                                 "en" : "a horse",
                                 "de" : "ein Pferd",
                               },
                  "selected" : "YES",
                },
                { "value"    : "CAT",
                  "label"    : { "fr" : "un chat",
                                 "en" : "a cat",
                                 "de" : "eine Katze",
                               },
                  "selected" : "NO",
                }
              ]

    obj1 = WSET_RadioButton(wso,
                            "animals",
                            el1_lab,
                            el1_opt)

    el2_lab = { "fr" : "La nourriture",
                "en" : "Food",
                "de" : "Nahrungsmitteln",
              }

    el2_opt = [
                { "value"    : "FRUIT",
                  "label"    : { "fr" : "Le fruit",
                                 "en" : "Fruit",
                                 "de" : "Fruchte",
                               },
                  "selected" : "NO",
                },
                { "value"    : "MEAT",
                  "label"    : { "fr" : "La viande",
                                 "en" : "Meat",
                                 "de" : "Fleisch",
                               },
                  "selected" : "NO",
                },
                { "value"    : "BREAD",
                  "label"    : { "fr" : "Le pain",
                                 "en" : "Bread",
                                 "de" : "Brot",
                               },
                  "selected" : "NO",
                }
              ]

    obj2 = WSET_RadioButton(wso=wso,
                            elementname="food",
                            elementlabel=el2_lab,
                            optionvalues=el2_opt,
                            buttonlayout="H",
                            numbuttonsperline=2,
                            mandatory=1)

    wset_list.append(obj1)
    wset_list.append(obj2)

    return wset_list

def create_interface_minidom(xmltext,
                             wso,
                             verbose=CFG_BIBRECORD_DEFAULT_VERBOSE_LEVEL,
                             correct=CFG_BIBRECORD_DEFAULT_CORRECT):
    
    """
    Uses xml.dom.minidom parser to creates a tuple (interface, checker, dictionnary of objects)
    +interface:
        List of dictionnaries with 2 keys:
         "container-label" : dictionnary of pairs of language/value
         "elements" : list of names of websubmit element
         example:
         [{'container_label': {'fr': 'Zone de texte'},
           'elements': ['abstract', 'Title']},
          {'container_label': {'fr': 'Bouton Radio', 'en': 'RadioButton'},
           'elements': ['keyword']}
    +checker:
        List of tuples of 3 elements:
        -reference to a wsc_function
        -string containing the parameters for this function
        -dictionnary where items are pairs of language/value
        example:
         [(<function wsc_string_length at 0x42b28d4c>,
           '(abstract, 20)',
           {'en': 'The size of the abstract must be more than 20 characters'}),
          (<function wsc_string_length at 0x42b28d4c>,
           '(title, 30)',
           {'en': 'The size of the title must be more than 30 characters'
            'fr:  'La taille du titre doit etre superieure a 30 caracteres'}),
         ]
    +elements:
        Dictionnary of websubmit elements objects used for the current submission
        -keys: name of the element
        -values: instance of WSET class
        example:
        {'PublicationJournal': <invenio.websubmit_elements.WSET_Select.WSET_Select object at 0x42b24cec>,
         'Title': <invenio.websubmit_elements.WSET_TextArea.WSET_TextArea object at 0x427e18cc>,
         'abstract': <invenio.websubmit_elements.WSET_TextArea.WSET_TextArea object at 0x427e1aac>,
        }
    @param xmltext: (string) xml template for a the interface of a given submission
    @param wso: () current websubmit object
    @param verbose & correct : #FIXME put config variable in a unique place for websubmit and bibrecord

    @return a tuple (interface, checker, elements) see description above.
    """
    
    interface = []
    elements = {}
    checker = []
    dom = parseString(xmltext)
    root = dom.childNodes[0]
    
    #build interface & elements dictionnary
    for cont in root.getElementsByTagName("container"):
        container = {"container_label":{}, "elements" :[]}
        list_of_elements = []
        container_label = {}
        for c_label in cont.getElementsByTagName("container-label"):
            if c_label.hasAttribute("ln") and c_label.hasChildNodes():
                container_label[c_label.getAttribute("ln").encode("utf-8")] = c_label.firstChild.nodeValue.encode("utf-8")
            else:
                raise Exception
                    #FIXME xml template not correct
                    #If container-label exists,it must have an attribute "ln" and a node Value
        for element in cont.getElementsByTagName("element"):
            element_label = {}
            option_values = []
            default_value = ""
            attrs = {}
            element_name = element.getAttribute("name").encode("utf-8")
            if element_name == "":
              raise Exception
              #FIXME
            if not element.hasAttribute("type"):
                #Pick up the element node from the library
                if library.has_key(element_name):
                    current_element = library[element_name]
                else:
                    #FIXME: xml template not correct
                    #Element must have an attribute type
                    # of must be defined in the library
                    raise Exception
            else:
                current_element = element
            #Encode key value
            for (key, value) in current_element.attributes.items():
                attrs[key.encode("utf-8")] = value.encode("utf-8")
            #Get element type
            try:
                element_type = attrs["type"]
            except KeyError, err:
                 #FIXME: xml template not correct
                 #Element must have an attribute type
                 raise Exception
            del attrs["type"]
            if current_element.getElementsByTagName("default-value"):
                try:
                    default_value = current_element.getElementsByTagName("default-value")[0].firstChild.nodeValue.encode("utf-8")
                except AttributeError, err:
                    #FIXME
                    #If default_value exists it must have a node value
                    raise err
            for el_label in current_element.getElementsByTagName("element-label"):
                if el_label.hasAttribute("ln") and el_label.hasChildNodes():
                    element_label[el_label.getAttribute("ln")] = el_label.firstChild.nodeValue.encode("utf-8")
                else:
                    raise Exception
                    #FIXME xml template not correct
                    #If element-label exists,it must have an attribute "ln" and a node Value
            for opt in current_element.getElementsByTagName("option"):
                #Get the value. Value is mandatory for a option tag
                if opt.hasAttribute("value"):
                    option = {"value":opt.getAttribute("value").encode("utf-8"), "label":{}}
                else:
                    raise Exception 
                    #FIXME xml template not correct
                    #If option exists it must have and attribut 'value'
                #Set the selected attribute yes/no
                if opt.hasAttribute("selected"):
                    option["selected"] = opt.getAttribute("selected").encode("utf-8")
                    #FIXME need to check if selected is something else than yes/no???
                else:
                    option["selected"] ="no"
                for opt_label in opt.getElementsByTagName("option-label"):
                    if opt_label.hasAttribute("ln") and opt_label.hasChildNodes():
                        option["label"][opt_label.getAttribute("ln")] = opt_label.firstChild.nodeValue.encode("utf-8")
                    else:
                        raise Exception
                        #FIXME xml template not correct
                        #If option-label exists,it must have an attribute "ln" and a node Value
                option_values.append(option)

            element_class = get_reference_from_name(element_type)
            attrs["elementname"] = element_name
            attrs["optionvalues"] = option_values
            attrs["wso"] = wso
            attrs["elementlabel"] = element_label
            attrs["defaultvalue"] = default_value
            try:
                element_object = element_class(**attrs)
            except TypeError, err:
                ##FIXME
                raise err
            list_of_elements.append(element_name)
            elements[element_name] = element_object
            current_element = None
        container["elements"] = list_of_elements
        container["container_label"] = container_label
        interface.append(container)
        
    #Build Checker
    for check in root.getElementsByTagName("check"):
        error_label = {}
        if check.hasAttribute("test"):
            test = check.getAttribute("test").encode("utf-8")
        else:
            #FIXME check must have an attribute test
            raise Exception
        try:
            wsc_function_ref, params = test.split("(", 1)
            params = "(" + params
        except ValueError, err:
            #FIXME attribute test must be of the form "function(param1, param2....)"
            raise err
        wsc_function_ref = get_reference_from_name(wsc_function_ref, CFG_WEBSUBMIT_CHECKS_IMPORT_PATH)
        for err_label in check.getElementsByTagName("error-label"):
            if err_label.hasAttribute("ln") and err_label.hasChildNodes():
                error_label[err_label.getAttribute("ln").encode("utf-8")] = err_label.firstChild.nodeValue.encode("utf-8")
            else:
                raise Exception
                #FIXME xml template not correct
                #If error-label exists,it must have an attribute "ln" and a node Value
        checker.append((wsc_function_ref, params, error_label))
        
    return (interface, checker, elements)


def create_submission_collection_page_minidom(xmltext,
                                              verbose=CFG_BIBRECORD_DEFAULT_VERBOSE_LEVEL,
                                              correct=CFG_BIBRECORD_DEFAULT_CORRECT):
    
    """
    Parse the main submission config file containing the submission tree
    @param xmltext: (string) xml template for creating the submission collection page
    @return a list of collections
    +collection: dictionnaries of the following form
                 {"label":{},
                  "doctypes" :[],
                  "collections"=[collection]
                 }
        +doctypes: list of dictionnaries of the following form:
                   {"id":"",
                    "label":{},
                    "template": None,
                    "categories":[],
                    "access_rules":""
                   }
            +categories: list of dictionnaries of the following form:
                   {"id":"",
                    "label":{},
                    "template": None,
                    "categories":[],
                    "access_rules":""
                   }
    """
    dom = parseString(xmltext)
    root = dom.childNodes[0]
    collection_level = 0
    collections = recursive_collection_node(root, collection_level, [])
    #take the first element of the root collection
    #return collections[0]["collections"]
    return collections

def recursive_collection_node(node, collection_level, collections):
    """
    Create the collection and sub-collections recursively
    @param node: instance of DOM Element of type collection 
    @collection_level: (int) level in the tree of the collections limit
                       by CFG_WEBSUBMIT_COLLECTION_NUMBER_OF_LEVEL variable
    @collections: current list of collection
    @return the list of collections extended with the current collection
    """
    collection = {"label":{},
                  "collections":[],
                  "doctypes" :[]}
    for coll_child in node.childNodes:
        ## collection label
        if coll_child.nodeName.encode("utf-8") == "collection-label":
            if coll_child.hasAttribute("ln") and coll_child.hasChildNodes():
                collection["label"][coll_child.getAttribute("ln").encode("utf-8")] = coll_child.firstChild.nodeValue.encode("utf-8")
            else:
                raise Exception
                #FIXME xml template not correct
                #If collection-label exists,it must have an attribute "ln" and a node Value                
        ## doctype
        if coll_child.nodeName.encode("utf-8") == "doctype":
            doctype = {"id":"",
                       "label":{},
                       "template":None,
                       "categories":[],
                       "access_rules":""
                       }
            for child in coll_child.childNodes:
                ## doctype label
                if child.nodeName.encode("utf-8") == "doctype-label":
                        if child.hasAttribute("ln") and child.hasChildNodes():
                            doctype["label"][child.getAttribute("ln")] = child.firstChild.nodeValue.encode("utf-8")
                        else:
                            raise Exception
                            #FIXME xml template not correct
                            #If doctype-label exists,it must have an attribute "ln" and a node Value
                elif child.nodeName.encode("utf-8") == "category":
                    category_level = 0
                    doctype["categories"] = recursive_category_node(child, category_level, [])
                elif child.nodeName.encode("utf-8") == "access-restriction":
                    for rule in child.getElementsByTagName("rule"):
                        doctype["access_rules"] += "%s\n" % rule.firstChild.nodeValue.encode("utf-8")
            if coll_child.hasAttribute("template"):
                doctype["template"] = coll_child.getAttribute("template").encode("utf-8")
            if coll_child.hasAttribute("id"):
                doctype["id"] = coll_child.getAttribute("id").encode("utf-8")
            else:
                raise Exception
            collection["doctypes"].append(doctype)
        #####sub-collections#####
        if coll_child.nodeName.encode("utf-8") == "collection":
            collection_level += 1
            if collection_level < CFG_WEBSUBMIT_COLLECTION_NUMBER_OF_LEVEL:
                recursive_collection_node(coll_child, collection_level, collection["collections"])
    collections.append(collection)
    return collections
    
def recursive_category_node(node, category_level, categories):
    category = {"id":"",
                "label":{},
                "template":None,
                "categories":[],
                "access_rules":""
                }
    if node.hasAttribute("id"):
        category["id"] = node.getAttribute("id").encode("utf-8")
    else:
        raise Exception
    if node.hasAttribute("template"):
        category["template"] = node.getAttribute("template").encode("utf-8")
    for categ_child in node.childNodes:
        ######categ label########
        if categ_child.nodeName.encode("utf-8") == "category-label":
            if categ_child.hasAttribute("ln") and categ_child.hasChildNodes():
                category["label"][categ_child.getAttribute("ln").encode("utf-8")] = categ_child.firstChild.nodeValue.encode("utf-8")
            else:
                raise Exception
                #FIXME xml template not correct
                #If category-label exists,it must have an attribute "ln" and a node Value                
            
        elif categ_child.nodeName.encode("utf-8") == "category":
            category_level += 1
            if category_level < CFG_WEBSUBMIT_CATEGORY_NUMBER_OF_LEVEL:
                recursive_category_node(categ_child, category_level, category["categories"])
        elif categ_child.nodeName.encode("utf-8") == "access-restriction":
            for rule in categ_child.getElementsByTagName("rule"):
                category["access_rules"] += "%s\n" % rule.firstChild.nodeValue.encode("utf-8")
            if categ_child.hasAttribute("template"):
                category["template"] = categ_child.getAttribute("template").encode("utf-8")
    categories.append(category)
    return categories

    
##FIXME: need to be updated as for minidom parser, don't want to keep the two parsers
##up to date during development
##def create_interface_RXP(xmltext,
##                          wso,
##                          verbose=CFG_BIBRECORD_DEFAULT_VERBOSE_LEVEL,
##                          correct=CFG_BIBRECORD_DEFAULT_CORRECT):
##     #FIXME put config variable in a unique place for websubmit and bibrecord
##     """
##     Creates a list of websubmit container object and returns it
##     Uses the RXP parser
    
##     If verbose>3 then the parser will be strict and will stop in case of well-formedness errors
##     or DTD errors
##     If verbose=0, the parser will not give warnings
##     If 0<verbose<=3, the parser will not give errors, but will warn the user about possible mistakes

##     correct != 0 -> We will try to correct errors such as missing attributtes
##     correct = 0 -> there will not be any attempt to correct errors
    
##     """
    
##     TAG, ATTRS, CHILD_LIST = range(3)
    
##     if verbose > 3:
##         p = pyRXP.Parser(ErrorOnValidityErrors=1,
##                          ProcessDTD=1,
##                          ErrorOnUnquotedAttributeValues=1,
##                          warnCB = warnCB,
##                          srcName='string input')
##     else:
##         p = pyRXP.Parser(ErrorOnValidityErrors=0,
##                          ProcessDTD=1,
##                          ErrorOnUnquotedAttributeValues=0,
##                          warnCB = warnCB,
##                          srcName='string input')

##     #FIXME
##     ## if correct:
## ##         (rec, e) = wash(xmltext)
## ##         err.extend(e)
## ##         return (rec, e)

    
##     root1 = p(xmltext) #root = (tagname, attr_dict, child_list, reserved)

##     interface = []
##     for tc in root1[CHILD_LIST]:
##         #tc --> container
##         if type(tc).__name__ == 'tuple' and tc[TAG] == "container":
##             container = {"container_label":{}, "elements" :[]}
##             list_of_elements = []
##             #te --> element or container-label
##             for te in tc[CHILD_LIST]:
##                 if type(te).__name__ == 'tuple' and te[TAG] == "container-label":
##                     try:
##                         label = {te[ATTRS].values()[0].encode("utf-8"): te[CHILD_LIST][0].encode("utf-8")}
##                         container["container_label"].update(label)
##                     except IndexError, err:
##                         #FIXME xml template not correct
##                         #If container-label exists,it must have an attribute "ln" and a node Value
##                         raise err
##                 if type(te).__name__ == 'tuple' and te[TAG] == "element":
##                     element_label = {}
##                     option_values = []
##                     default_value = ""
##                     for tel in te[CHILD_LIST]:
##                         if type(tel).__name__ == 'tuple' and tel[TAG] == "default-value":
##                             try:
##                                 default_value = tel[CHILD_LIST][0].encode("utf-8")
##                             except KeyError, err:
##                                 #FIXME
##                                 #If default_value exists it must have a node value
##                                 raise err
##                         if type(tel).__name__ == 'tuple' and tel[TAG] == "element-label":
##                             try:
##                                 label = {tel[ATTRS].values()[0].encode("utf-8"): tel[CHILD_LIST][0].encode("utf-8")}
##                                 element_label.update(label)
##                             except IndexError, err:
##                                 #FIXME xml template not correct
##                                 #If element-label exists,it must have an attribute "ln" and a node Value
##                                 raise err
##                         if type(tel).__name__ == 'tuple' and tel[TAG] == "option":
##                             try:
##                                 option = {"value":tel[ATTRS]["value"].encode("utf-8"),
##                                           "label":{}}
##                             except KeyError, err:
##                                 #FIXME xml template not correct
##                                 #If option exists it must have and attribut 'value'
##                                 raise err
##                             #Set the selected attribute yes/no
##                             #FIXME need to check if selected is something else than yes/no???
##                             if tel[ATTRS].has_key("selected"):
##                                 option["selected"] = tel[ATTRS]["selected"].encode("utf-8")
##                             else:
##                                 option["selected"] ="no"
##                             for teo in tel[CHILD_LIST]:
##                                 #option-label
##                                 if type(teo).__name__ == 'tuple' and teo[TAG] == "option-label":
##                                     try:
##                                         label = {teo[ATTRS].values()[0].encode("utf-8"): teo[CHILD_LIST][0].encode("utf-8")}
##                                         option["label"].update(label)
##                                     except IndexError, err:
##                                         #FIXME xml template not correct
##                                         #If option-label exists,it must have an attribute "ln" and a node Value
##                                         raise err
##                             option_values.append(option)
                    
##                     try:
##                         attrs = te[ATTRS]
##                         element_type = attrs["type"]
##                         del attrs["type"]
##                         element_name = attrs["name"]
##                         del attrs["name"]
##                         element_name = element_name.encode("utf-8")
##                     except KeyError, err:
##                         ##FIXME mandatory attributes are missing
##                         raise err
##                     for (key, value) in attrs.items():
##                         attrs[key.encode("utf-8")] = value.encode("utf-8")
##                     element_class = get_WSET_class_reference(element_type)
##                     attrs["optionvalues"] = option_values
##                     attrs["wso"] = wso
##                     attrs["elementname"] = element_name
##                     attrs["elementlabel"] = element_label
##                     attrs["defaultvalue"] = default_value
##                     try:
##                         element_object = element_class(**attrs)
##                     except TypeError, err:
##                         ##FIXME
##                         raise err
##                     list_of_elements.append(element_object)
##             container["elements"] = list_of_elements
##             interface.append(container)          
##     return interface










## -------- OLD STUFF FOLLOWS ---- OLD STUFF FOLLOWS --------------
def interface(req,
              c=cdsname,
              ln=cdslang,
              doctype="",
              act="",
              startPg=1,
              indir="",
              access="",
              mainmenu="",
              fromdir="",
              file="",
              nextPg="",
              nbPg="",
              curpage=1):
    """This function is called after a user has visited a document type's
       "homepage" and selected the type of "action" to perform. Having
       clicked an action-button (e.g. "Submit a New Record"), this function
       will be called . It performs the task of initialising a new submission
       session (retrieving information about the submission, creating a
       working submission-directory, etc), and "drawing" a submission page
       containing the WebSubmit form that the user uses to input the metadata
       to be submitted.
       When a user moves between pages in the submission interface, this
       function is recalled so that it can save the metadata entered into the
       previous page by the user, and draw the current submission-page.

       Note: During a submission, for each page refresh, this function will be
       called while the variable "step" (a form variable, seen by
       websubmit_webinterface, which calls this function) is 0 (ZERO).

       In other words, this function handles the FRONT-END phase of a
       submission, BEFORE the WebSubmit functions are called.

       @param req: (apache request object) *** NOTE: Added into this object, is
        a variable called "form" (req.form). This is added into the object in
        the index function of websubmit_webinterface. It contains a
        "mod_python.util.FieldStorage" instance, that contains the form-fields
        found on the previous submission page.
       @param c: (string), defaulted to cdsname. The name of the CDS Invenio
        installation.
       @param ln: (string), defaulted to cdslang. The language in which to
        display the pages.
       @param doctype: (string) - the doctype ID of the doctype for which the
        submission is being made.
       @param act: (string) - The ID of the action being performed (e.g.
        submission of bibliographic information; modification of bibliographic
        information, etc).
       @param startPg: (integer) - Starting page for the submission? Defaults
        to 1.
       @param indir: (string) - the directory used to store all submissions
        of the given "type" of this submission. For example, if the submission
        is of the type "modify bibliographic information", this variable would
        contain "modify".
       @param access: (string) - the "access" number for the submission
        (e.g. 1174062451_7010). This number is also used as the name for the
        current working submission directory.
       @param mainmenu: (string) - contains the URL (minus the CDS Invenio
        home stem) for the submission's home-page. (E.g. If this submission
        is "PICT", the "mainmenu" file would contain "/submit?doctype=PICT".
       @param fromdir: (integer)
       @param file: (string)
       @param nextPg: (string)
       @param nbPg: (string)
       @param curpage: (integer) - the current submission page number. Defaults
        to 1.
    """

    ln = wash_language(ln)

    # load the right message language
    _ = gettext_set_language(ln)

    sys.stdout = req
    # get user ID:
    try:
        uid = getUid(req)
        uid_email = get_email(uid)
    except Error, e:
        return errorMsg(e, req, c, ln)
    # variable initialisation
    t = ""
    field = []
    fieldhtml = []
    level = []
    fullDesc = []
    text = []
    check = []
    select = []
    radio = []
    upload = []
    txt = []
    noPage = []
    # Preliminary tasks
    # check that the user is logged in
    if uid_email == "" or uid_email == "guest":
        return warningMsg(websubmit_templates.tmpl_warning_message(
                           ln = ln,
                           msg = _("Sorry, you must log in to perform this action.")
                         ), req, ln)
        # warningMsg("""<center><font color="red"></font></center>""",req, ln)
    # check we have minimum fields
    if "" in (doctype, act, access):
        ## We don't have all the necessary information to go ahead
        ## with this submission:
        return errorMsg(_("Invalid parameter"), req, c, ln)


    ## Before continuing to display the submission form interface,
    ## verify that this submission has not already been completed:
    if submission_is_finished(doctype, act, access, uid_email):
        ## This submission has already been completed.
        ## This situation can arise when, having completed a submission,
        ## the user uses the browser's back-button to go back to the form
        ## stage of the submission and then tries to submit once more.
        ## This is unsafe and should not be allowed. Instead of re-displaying
        ## the submission forms, display an error message to the user:
        wrnmsg = """<b>This submission has been completed. Please go to the""" \
                 """ <a href="/submit?doctype=%(doctype)s&amp;ln=%(ln)s">""" \
                 """main menu</a> to start a new submission.</b>""" \
                 % { 'doctype' : doctype, 'ln' : ln }
        return warningMsg(wrnmsg, req)


    ## retrieve the action and doctype data:

    ## Concatenate action ID and doctype ID to make the submission ID:
    subname = "%s%s" % (act, doctype)

    if indir == "":
        ## Get the submission storage directory from the DB:
        submission_dir = get_storage_directory_of_action(act)
        if submission_dir not in ("", None):
            indir = submission_dir
        else:
            ## Unable to determine the submission-directory:
            return errorMsg(_("Unable to find the submission directory."), req, c, ln)

    ## get the document type's long-name:
    doctype_lname = get_longname_of_doctype(doctype)
    if doctype_lname is not None:
        ## Got the doctype long-name: replace spaces with HTML chars:
        docname = doctype_lname.replace(" ", "&nbsp;")
    else:
        ## Unknown document type:
        return errorMsg(_("Unknown document type"), req, c, ln)

    ## get the action's long-name:
    action_lname = get_longname_of_action(act)
    if action_lname is not None:
        ## Got the action long-name: replace spaces with HTML chars:
        actname = action_lname.replace(" ", "&nbsp;")
    else:
        ## Unknown action:
        return errorMsg(_("Unknown action"), req, c, ln)

    ## Get the number of pages for this submission:
    num_submission_pages = get_num_pages_of_submission(subname)
    if num_submission_pages is not None:
        nbpages = num_submission_pages
    else:
        ## Unable to determine the number of pages for this submission:
        return errorMsg(_("Unable to determine the number of submission pages."), req, c, ln)

    ## If unknown, get the current page of submission:
    if startPg != "" and curpage in ("", 0):
        curpage = startPg

    ## retrieve the name of the file in which the reference of
    ## the submitted document will be stored
    rn_filename = get_parameter_value_for_doctype(doctype, "edsrn")
    if rn_filename is not None:
        edsrn = rn_filename
    else:
        ## Unknown value for edsrn - set it to an empty string:
        edsrn = ""

    ## This defines the path to the directory containing the action data
    curdir = "%s/%s/%s/%s" % (storage, indir, doctype, access)

    ## if this submission comes from another one (fromdir is then set)
    ## We retrieve the previous submission directory and put it in the proper one
    if fromdir != "":
        olddir = "%s/%s/%s/%s" % (storage, fromdir, doctype, access)
        if os.path.exists(olddir):
            os.rename(olddir, curdir)
    ## If the submission directory still does not exist, we create it
    if not os.path.exists(curdir):
        try:
            os.makedirs(curdir)
        except:
            return errorMsg(_("Unable to create a directory for this submission."), req, c, ln)
    # retrieve the original main menu url and save it in the "mainmenu" file
    if mainmenu != "":
        fp = open("%s/mainmenu" % curdir, "w")
        fp.write(mainmenu)
        fp.close()
    # and if the file containing the URL to the main menu exists
    # we retrieve it and store it in the $mainmenu variable
    if os.path.exists("%s/mainmenu" % curdir):
        fp = open("%s/mainmenu" % curdir, "r");
        mainmenu = fp.read()
        fp.close()
    else:
        mainmenu = "%s/submit" % (urlpath,)
    # various authentication related tasks...
    if uid_email != "guest" and uid_email != "":
        #First save the username (email address) in the SuE file. This way bibconvert will be able to use it if needed
        fp = open("%s/SuE" % curdir, "w")
        fp.write(uid_email)
        fp.close()
    # is user authorized to perform this action?
    (auth_code, auth_message) = acc_authorize_action(req, "submit", verbose=0, doctype=doctype, act=act)
    if acc_is_role("submit", doctype=doctype, act=act) and auth_code != 0:
        return warningMsg("""<center><font color="red">%s</font></center>""" % auth_message, req)

    ## update the "journal of submission":
    ## Does the submission already exist in the log?
    submission_exists = \
         submission_exists_in_log(doctype, act, access, uid_email)
    if submission_exists == 1:
        ## update the modification-date of this submission in the log:
        update_submission_modified_date_in_log(doctype, act, access, uid_email)
    else:
        ## Submission doesn't exist in log - create it:
        log_new_pending_submission(doctype, act, access, uid_email)

    # Save the form fields entered in the previous submission page
    # If the form was sent with the GET method
    form = req.form
    value = ""
    # we parse all the form variables
    for key in form.keys():
        formfields = form[key]
        if re.search("\[\]", key):
            filename = key.replace("[]", "")
        else:
            filename = key
        # the field is an array
        if isinstance(formfields, types.ListType):
            fp = open("%s/%s" % (curdir, filename), "w")
            for formfield in formfields:
                #stripslashes(value)
                value = specialchars(formfield)
                fp.write(value+"\n")
            fp.close()
        # the field is a normal string
        elif isinstance(formfields, types.StringTypes) and formfields != "":
            value = formfields
            fp = open("%s/%s" % (curdir, filename), "w")
            fp.write(specialchars(value))
            fp.close()
        # the field is a file
        elif hasattr(formfields,"filename") and formfields.filename is not None:
            if not os.path.exists("%s/files/%s" % (curdir, key)):
                try:
                    os.makedirs("%s/files/%s" % (curdir, key))
                except:
                    return errorMsg(_("Cannot create submission directory."), req, c, ln)
            filename = formfields.filename
            if filename != "":
                # This may be dangerous if the file size is bigger than the available memory
                data = formfields.file.read()
                fp = open("%s/files/%s/%s" % (curdir, key, filename), "w")
                fp.write(data)
                fp.close()
                fp = open("%s/lastuploadedfile" % curdir, "w")
                fp.write(filename)
                fp.close()
                fp = open("%s/%s" % (curdir, key), "w")
                fp.write(filename)
                fp.close()

        ## if the found field is the reference of the document,
        ## save this value in the "journal of submissions":
        if uid_email != "" and uid_email != "guest":
            if key == edsrn:
                update_submission_reference_in_log(doctype, access, uid_email, value)

    ## create the interface:
    subname = "%s%s" % (act, doctype)

    ## Get all of the form fields that appear on this page, ordered by fieldnum:
    form_fields = get_form_fields_on_submission_page(subname, curpage)

    full_fields = []
    values = []

    for field_instance in form_fields:
        full_field = {}
        ## Retrieve the field's description:
        element_descr = get_element_description(field_instance[3])
        if element_descr is None:
            ## The form field doesn't seem to exist - return with error message:
            return \
             errorMsg(_("Unknown form field found on submission page."), \
                      req, c, ln)

        if element_descr[8] is None:
            val = ""
        else:
            val = element_descr[8]

        ## we also retrieve and add the javascript code of the checking function, if needed
        ## Set it to empty string to begin with:
        full_field['javascript'] = ''
        if field_instance[7] != '':
            check_descr = get_element_check_description(field_instance[7])
            if check_descr is not None:
                ## Retrieved the check description:
                full_field['javascript'] = check_descr

        full_field['type'] = element_descr[3]
        full_field['name'] = field_instance[3]
        full_field['rows'] = element_descr[5]
        full_field['cols'] = element_descr[6]
        full_field['val'] = val
        full_field['size'] = element_descr[4]
        full_field['maxlength'] = element_descr[7]
        full_field['htmlcode'] = element_descr[9]
        full_field['typename'] = field_instance[1]  ## TODO: Investigate this, Not used?
                                                    ## It also seems to refer to pagenum.

        # The 'R' fields must be executed in the engine's environment,
        # as the runtime functions access some global and local
        # variables.
        if full_field ['type'] == 'R':
            co = compile (full_field ['htmlcode'].replace("\r\n","\n"), "<string>", "exec")
            exec(co)
        else:
            text = websubmit_templates.tmpl_submit_field (ln = ln, field = full_field)

        # we now determine the exact type of the created field
        if full_field['type'] not in [ 'D','R']:
            field.append(full_field['name'])
            level.append(field_instance[5])
            fullDesc.append(field_instance[4])
            txt.append(field_instance[6])
            check.append(field_instance[7])
            # If the field is not user-defined, we try to determine its type
            # (select, radio, file upload...)
            # check whether it is a select field or not
            if re.search("SELECT", text, re.IGNORECASE) is not None:
                select.append(1)
            else:
                select.append(0)
            # checks whether it is a radio field or not
            if re.search(r"TYPE=[\"']?radio", text, re.IGNORECASE) is not None:
                radio.append(1)
            else:
                radio.append(0)
            # checks whether it is a file upload or not
            if re.search(r"TYPE=[\"']?file", text, re.IGNORECASE) is not None:
                upload.append(1)
            else:
                upload.append(0)
            # if the field description contains the "<COMBO>" string, replace
            # it by the category selected on the document page submission page
            combofile = "combo%s" % doctype
            if os.path.exists("%s/%s" % (curdir, combofile)):
                f = open("%s/%s" % (curdir, combofile), "r")
                combo = f.read()
                f.close()
            else:
                combo=""
            text = text.replace("<COMBO>", combo)
            # if there is a <YYYY> tag in it, replace it by the current year
            year = time.strftime("%Y");
            text = text.replace("<YYYY>", year)
            # if there is a <TODAY> tag in it, replace it by the current year
            today = time.strftime("%d/%m/%Y");
            text = text.replace("<TODAY>", today)
            fieldhtml.append(text)
        else:
            select.append(0)
            radio.append(0)
            upload.append(0)
            # field.append(value) - initial version, not working with JS, taking a submitted value
            field.append(field_instance[3])
            level.append(field_instance[5])
            txt.append(field_instance[6])
            fullDesc.append(field_instance[4])
            check.append(field_instance[7])
            fieldhtml.append(text)
        full_field['fullDesc'] = field_instance[4]
        full_field['text'] = text

        # If a file exists with the name of the field we extract the saved value
        text = ''
        if os.path.exists("%s/%s" % (curdir, full_field['name'])):
            file = open("%s/%s" % (curdir, full_field['name']), "r");
            text = file.read()
            text = re.compile("[\n\r]*$").sub("", text)
            text = re.compile("\n").sub("\\n", text)
            text = re.compile("\r").sub("", text)
            file.close()

        values.append(text)

        full_fields.append(full_field)

    returnto = {}
    if int(curpage) == int(nbpages):
        subname = "%s%s" % (act, doctype)
        other_form_fields = \
              get_form_fields_not_on_submission_page(subname, curpage)
        nbFields = 0
        message = ""
        fullcheck_select = []
        fullcheck_radio = []
        fullcheck_upload = []
        fullcheck_field = []
        fullcheck_level = []
        fullcheck_txt = []
        fullcheck_noPage = []
        fullcheck_check = []
        for field_instance in other_form_fields:
            if field_instance[5] == "M":
                ## If this field is mandatory, get its description:
                element_descr = get_element_description(field_instance[3])
                if element_descr is None:
                    ## The form field doesn't seem to exist - return with error message:
                    return \
                     errorMsg(_("Unknown form field found on one of the submission pages."), \
                              req, c, ln)
                if element_descr[3] in ['D', 'R']:
                    if element_descr[3] == "D":
                        text = element_descr[9]
                    else:
                        text = eval(element_descr[9])
                    formfields = text.split(">")
                    for formfield in formfields:
                        match = re.match("name=([^ <>]+)", formfield, re.IGNORECASE)
                        if match is not None:
                            names = match.groups
                            for value in names:
                                if value != "":
                                    value = re.compile("[\"']+").sub("", value)
                                    fullcheck_field.append(value)
                                    fullcheck_level.append(field_instance[5])
                                    fullcheck_txt.append(field_instance[6])
                                    fullcheck_noPage.append(field_instance[1])
                                    fullcheck_check.append(field_instance[7])
                                    nbFields = nbFields + 1
                else:
                    fullcheck_noPage.append(field_instance[1])
                    fullcheck_field.append(field_instance[3])
                    fullcheck_level.append(field_instance[5])
                    fullcheck_txt.append(field_instance[6])
                    fullcheck_check.append(field_instance[7])
                    nbFields = nbFields+1
        # tests each mandatory field
        fld = 0
        res = 1
        for i in range (0, nbFields):
            res = 1
            if not os.path.exists("%s/%s" % (curdir, fullcheck_field[i])):
                res=0
            else:
                file = open("%s/%s" % (curdir, fullcheck_field[i]), "r")
                text = file.read()
                if text == '':
                    res=0
                else:
                    if text == "Select:":
                        res=0
            if res == 0:
                fld = i
                break
        if not res:
            returnto = {
                         'field' : fullcheck_txt[fld],
                         'page'  : fullcheck_noPage[fld],
                       }

    t += websubmit_templates.tmpl_page_interface(
          ln = ln,
          docname = docname,
          actname = actname,
          curpage = curpage,
          nbpages = nbpages,
          file = file,
          nextPg = nextPg,
          access = access,
          nbPg = nbPg,
          doctype = doctype,
          act = act,
          indir = indir,
          fields = full_fields,
          javascript = websubmit_templates.tmpl_page_interface_js(
                         ln = ln,
                         upload = upload,
                         field = field,
                         fieldhtml = fieldhtml,
                         txt = txt,
                         check = check,
                         level = level,
                         curdir = curdir,
                         values = values,
                         select = select,
                         radio = radio,
                         curpage = curpage,
                         nbpages = nbpages,
                         images = images,
                         returnto = returnto,
                       ),
          images = images,
          mainmenu = mainmenu,
         )

    # start display:
    req.content_type = "text/html"
    req.send_http_header()
    p_navtrail = """<a href="/submit">%(submit)s</a>&nbsp;>&nbsp;<a href="/submit?doctype=%(doctype)s\">%(docname)s</a>&nbsp;""" % {
                   'submit'  : _("Submit"),
                   'doctype' : doctype,
                   'docname' : docname,
                 }
    return page(title= actname,
                body = t,
                navtrail = p_navtrail,
                description = "submit documents",
                keywords = "submit",
                uid = uid,
                language = ln,
                req = req,
                navmenuid='submit')


def endaction(req,
              c=cdsname,
              ln=cdslang,
              doctype="",
              act="",
              startPg=1,
              indir="",
              access="",
              mainmenu="",
              fromdir="",
              file="",
              nextPg="",
              nbPg="",
              curpage=1,
              step=1,
              mode="U"):
    """Having filled-in the WebSubmit form created for metadata by the interface
       function, the user clicks a button to either "finish the submission" or
       to "proceed" to the next stage of the submission. At this point, a
       variable called "step" will be given a value of 1 or above, which means
       that this function is called by websubmit_webinterface.
       So, during all non-zero steps of the submission, this function is called.

       In other words, this function is called during the BACK-END phase of a
       submission, in which WebSubmit *functions* are being called.

       The function first ensures that all of the WebSubmit form field values
       have been saved in the current working submission directory, in text-
       files with the same name as the field elements have. It then determines
       the functions to be called for the given step of the submission, and
       executes them.
       Following this, if this is the last step of the submission, it logs the
       submission as "finished" in the journal of submissions.

       @param req: (apache request object) *** NOTE: Added into this object, is
        a variable called "form" (req.form). This is added into the object in
        the index function of websubmit_webinterface. It contains a
        "mod_python.util.FieldStorage" instance, that contains the form-fields
        found on the previous submission page.
       @param c: (string), defaulted to cdsname. The name of the CDS Invenio
        installation.
       @param ln: (string), defaulted to cdslang. The language in which to
        display the pages.
       @param doctype: (string) - the doctype ID of the doctype for which the
        submission is being made.
       @param act: (string) - The ID of the action being performed (e.g.
        submission of bibliographic information; modification of bibliographic
        information, etc).
       @param startPg: (integer) - Starting page for the submission? Defaults
        to 1.
       @param indir: (string) - the directory used to store all submissions
        of the given "type" of this submission. For example, if the submission
        is of the type "modify bibliographic information", this variable would
        contain "modify".
       @param access: (string) - the "access" number for the submission
        (e.g. 1174062451_7010). This number is also used as the name for the
        current working submission directory.
       @param mainmenu: (string) - contains the URL (minus the CDS Invenio
        home stem) for the submission's home-page. (E.g. If this submission
        is "PICT", the "mainmenu" file would contain "/submit?doctype=PICT".
       @param fromdir:
       @param file:
       @param nextPg:
       @param nbPg:
       @param curpage: (integer) - the current submission page number. Defaults
        to 1.
       @param step: (integer) - the current step of the submission. Defaults to
        1.
       @param mode:
    """

    global rn, sysno, dismode, curdir, uid, uid_email, last_step, action_score

    # load the right message language
    _ = gettext_set_language(ln)

    try:
        rn
    except NameError:
        rn = ""
    dismode = mode
    ln = wash_language(ln)
    sys.stdout = req
    t = ""
    # get user ID:
    try:
        uid = getUid(req)
        uid_email = get_email(uid)
    except Error, e:
        return errorMsg(e, req, c, ln)
    # Preliminary tasks
    # check that the user is logged in
    if uid_email == "" or uid_email == "guest":
        return warningMsg(websubmit_templates.tmpl_warning_message(
                           ln = ln,
                           msg = _("Sorry, you must log in to perform this action.")
                         ), req, ln)

    ## check we have minimum fields
    if "" in (doctype, act, access):
        ## We don't have all the necessary information to go ahead
        ## with this submission:
        return errorMsg(_("Invalid parameter"), req, c, ln)


    ## Before continuing to process the submitted data, verify that
    ## this submission has not already been completed:
    if submission_is_finished(doctype, act, access, uid_email):
        ## This submission has already been completed.
        ## This situation can arise when, having completed a submission,
        ## the user uses the browser's back-button to go back to the form
        ## stage of the submission and then tries to submit once more.
        ## This is unsafe and should not be allowed. Instead of re-processing
        ## the submitted data, display an error message to the user:
        wrnmsg = """<b>This submission has been completed. Please go to the""" \
                 """ <a href="/submit?doctype=%(doctype)s&amp;ln=%(ln)s">""" \
                 """main menu</a> to start a new submission.</b>""" \
                 % { 'doctype' : doctype, 'ln' : ln }
        return warningMsg(wrnmsg, req)

    ## retrieve the action and doctype data
    if indir == "":
        ## Get the submission storage directory from the DB:
        submission_dir = get_storage_directory_of_action(act)
        if submission_dir not in ("", None):
            indir = submission_dir
        else:
            ## Unable to determine the submission-directory:
            return errorMsg(_("Unable to find the submission directory."), \
                            req, c, ln)

    # The following words are reserved and should not be used as field names
    reserved_words = ["stop", "file", "nextPg", "startPg", "access", "curpage", "nbPg", "act", \
                      "indir", "doctype", "mode", "step", "deleted", "file_path", "userfile_name"]
    # This defines the path to the directory containing the action data
    curdir = "%s/%s/%s/%s" % (storage, indir, doctype, access)
    # If the submission directory still does not exist, we create it
    if not os.path.exists(curdir):
        try:
            os.makedirs(curdir)
        except:
            return errorMsg(_("Cannot create submission directory."), req, c, ln)
    # retrieve the original main menu url ans save it in the "mainmenu" file
    if mainmenu != "":
        fp = open("%s/mainmenu" % curdir, "w")
        fp.write(mainmenu)
        fp.close()
    # and if the file containing the URL to the main menu exists
    # we retrieve it and store it in the $mainmenu variable
    if os.path.exists("%s/mainmenu" % curdir):
        fp = open("%s/mainmenu" % curdir, "r");
        mainmenu = fp.read()
        fp.close()
    else:
        mainmenu = "%s/submit" % (urlpath,)

    ## retrieve the name of the file in which the reference of
    ## the submitted document will be stored
    rn_filename = get_parameter_value_for_doctype(doctype, "edsrn")
    if rn_filename is not None:
        edsrn = rn_filename
    else:
        ## Unknown value for edsrn - set it to an empty string:
        edsrn = ""

    ## Determine whether the action is finished
    ## (ie there are no other steps after the current one):
    finished = function_step_is_last(doctype, act, step)

    # Save the form fields entered in the previous submission page
    # If the form was sent with the GET method
    form = req.form
    value = ""
    # we parse all the form variables
    for key in form.keys():
        formfields = form[key]
        if re.search("\[\]", key):
            filename = key.replace("[]", "")
        else:
            filename = key
        # the field is an array
        if isinstance(formfields,types.ListType):
            fp = open("%s/%s" % (curdir, filename), "w")
            for formfield in formfields:
                #stripslashes(value)
                value = specialchars(formfield)
                fp.write(value+"\n")
            fp.close()
        # the field is a normal string
        elif isinstance(formfields, types.StringTypes) and formfields != "":
            value = formfields
            fp = open("%s/%s" % (curdir, filename), "w")
            fp.write(specialchars(value))
            fp.close()
        # the field is a file
        elif hasattr(formfields, "filename") and formfields.filename is not None:
            if not os.path.exists("%s/files/%s" % (curdir, key)):
                try:
                    os.makedirs("%s/files/%s" % (curdir, key))
                except:
                    return errorMsg("can't create submission directory", req, cdsname, ln)
            filename = formfields.filename
            if filename != "":
                # This may be dangerous if the file size is bigger than the available memory
                data = formfields.file.read()
                fp = open("%s/files/%s/%s" % (curdir, key, filename), "w")
                fp.write(data)
                fp.close()
                fp = open("%s/lastuploadedfile" % curdir, "w")
                fp.write(filename)
                fp.close()
                fp = open("%s/%s" % (curdir, key), "w")
                fp.write(filename)
                fp.close()
        ## if the found field is the reference of the document
        ## we save this value in the "journal of submissions"
        if uid_email != "" and uid_email != "guest":
            if key == edsrn:
                update_submission_reference_in_log(doctype, access, uid_email, value)

    ## get the document type's long-name:
    doctype_lname = get_longname_of_doctype(doctype)
    if doctype_lname is not None:
        ## Got the doctype long-name: replace spaces with HTML chars:
        docname = doctype_lname.replace(" ", "&nbsp;")
    else:
        ## Unknown document type:
        return errorMsg(_("Unknown document type"), req, c, ln)

    ## get the action's long-name:
    action_lname = get_longname_of_action(act)
    if action_lname is not None:
        ## Got the action long-name: replace spaces with HTML chars:
        actname = action_lname.replace(" ", "&nbsp;")
    else:
        ## Unknown action:
        return errorMsg(_("Unknown action"), req, c, ln)

    ## Get the number of pages for this submission:
    subname = "%s%s" % (act, doctype)
    num_submission_pages = get_num_pages_of_submission(subname)
    if num_submission_pages is not None:
        nbpages = num_submission_pages
    else:
        ## Unable to determine the number of pages for this submission:
        return errorMsg(_("Unable to determine the number of submission pages."), \
                        req, cdsname, ln)

    ## Determine whether the action is finished
    ## (ie there are no other steps after the current one):
    last_step = function_step_is_last(doctype, act, step)

    next_action = '' ## The next action to be proposed to the user

    # Prints the action details, returning the mandatory score
    action_score = action_details(doctype, act)
    current_level = get_level(doctype, act)

    # Calls all the function's actions
    function_content = ''
    try:
        ## Handle the execution of the functions for this
        ## submission/step:
        start_time = time.time()
        function_content = print_function_calls(req=req, doctype=doctype,
                                                action=act,
                                                step=step,
                                                form=form,
                                                start_time=start_time,
                                                ln=ln)
    except InvenioWebSubmitFunctionError, e:
        ## There was a serious function-error. Execution ends.
        return errorMsg(e.value, req, c, ln)
    except InvenioWebSubmitFunctionStop, e:
        ## For one reason or another, one of the functions has determined that
        ## the data-processing phase (i.e. the functions execution) should be
        ## halted and the user should be returned to the form interface once
        ## more. (NOTE: Redirecting the user to the Web-form interface is
        ## currently done using JavaScript. The "InvenioWebSubmitFunctionStop"
        ## exception contains a "value" string, which is effectively JavaScript
        ## - probably an alert box and a form that is submitted). **THIS WILL
        ## CHANGE IN THE FUTURE WHEN JavaScript IS REMOVED!**
        if e.value is not None:
            function_content = e.value
        else:
            function_content = e
    else:
        ## No function exceptions (InvenioWebSubmitFunctionStop,
        ## InvenioWebSubmitFunctionError) were raised by the functions. Propose
        ## the next action (if applicable), and log the submission as finished:

        ## If the action was mandatory we propose the next
        ## mandatory action (if any)
        if action_score != -1 and last_step == 1:
            next_action = Propose_Next_Action(doctype, \
                                              action_score, \
                                              access, \
                                              current_level, \
                                              indir)

        ## If we are in the last step of an action, we can update
        ## the "journal of submissions"
        if last_step == 1:
            if uid_email != "" and uid_email != "guest" and rn != "":
                ## update the "journal of submission":
                ## Does the submission already exist in the log?
                submission_exists = \
                     submission_exists_in_log(doctype, act, access, uid_email)
                if submission_exists == 1:
                    ## update the rn and status to finished for this submission
                    ## in the log:
                    update_submission_reference_and_status_in_log(doctype, \
                                                                  act, \
                                                                  access, \
                                                                  uid_email, \
                                                                  rn, \
                                                                  "finished")
                else:
                    ## Submission doesn't exist in log - create it:
                    log_new_completed_submission(doctype, \
                                                 act, \
                                                 access, \
                                                 uid_email, \
                                                 rn)

    ## Having executed the functions, create the page that will be displayed
    ## to the user:
    t = websubmit_templates.tmpl_page_endaction(
          ln = ln,
          weburl = weburl,
          # these fields are necessary for the navigation
          file = file,
          nextPg = nextPg,
          startPg = startPg,
          access = access,
          curpage = curpage,
          nbPg = nbPg,
          nbpages = nbpages,
          doctype = doctype,
          act = act,
          docname = docname,
          actname = actname,
          indir = indir,
          mainmenu = mainmenu,
          finished = finished,
          images = images,
          function_content = function_content,
          next_action = next_action,
        )

    # start display:
    req.content_type = "text/html"
    req.send_http_header()

    p_navtrail = """<a href="/submit">""" + _("Submit") +\
                 """</a>&nbsp;>&nbsp;<a href="/submit?doctype=%(doctype)s">%(docname)s</a>""" % {
                   'doctype' : doctype,
                   'docname' : docname,
                 }
    return page(title= actname,
                body = t,
                navtrail = p_navtrail,
                description="submit documents",
                keywords="submit",
                uid = uid,
                language = ln,
                req = req,
                navmenuid='submit')

def home(req, c=cdsname, ln=cdslang):
    """This function generates the WebSubmit "home page".
       Basically, this page contains a list of submission-collections
       in WebSubmit, and gives links to the various document-type
       submissions.
       Document-types only appear on this page when they have been
       connected to a submission-collection in WebSubmit.
       @param req: (apache request object)
       @param c: (string) - defaults to cdsname
       @param ln: (string) - The CDS Invenio interface language of choice.
        Defaults to cdslang (the default language of the installation).
       @return: (string) - the Web page to be displayed.
    """
    ln = wash_language(ln)
    # get user ID:
    try:
        uid = getUid(req)
    except Error, e:
        return errorMsg(e, req, c, ln)
    # start display:
    req.content_type = "text/html"
    req.send_http_header()

    # load the right message language
    _ = gettext_set_language(ln)

    finaltext = websubmit_templates.tmpl_submit_home_page(
                    ln = ln,
                    catalogues = makeCataloguesTable(ln)
                )

    return page(title=_("Submit"),
               body=finaltext,
               navtrail=[],
               description="submit documents",
               keywords="submit",
               uid=uid,
               language=ln,
               req=req,
               navmenuid='submit'
               )

def makeCataloguesTable(ln=cdslang):
    """Build the 'catalogues' (submission-collections) tree for
       the WebSubmit home-page. This tree contains the links to
       the various document types in WebSubmit.
       @param ln: (string) - the language of the interface.
        (defaults to 'cdslang').
       @return: (string) - the submission-collections tree.
    """
    text = ""
    catalogues = []

    ## Get the submission-collections attached at the top level
    ## of the submission-collection tree:
    top_level_collctns = get_collection_children_of_submission_collection(0)
    if len(top_level_collctns) != 0:
        ## There are submission-collections attatched to the top level.
        ## retrieve their details for displaying:
        for child_collctn in top_level_collctns:
            catalogues.append(getCatalogueBranch(child_collctn[0], 1))

        text = websubmit_templates.tmpl_submit_home_catalogs(
                 ln=ln,
                 catalogs=catalogues
               )
    else:
        text = websubmit_templates.tmpl_submit_home_catalog_no_content(ln=ln)
    return text

def getCatalogueBranch(id_father, level):
    """Build up a given branch of the submission-collection
       tree. I.e. given a parent submission-collection ID,
       build up the tree below it. This tree will include
       doctype-children, as well as other submission-
       collections and their children.
       Finally, return the branch as a dictionary.
       @param id_father: (integer) - the ID of the submission-collection
        from which to begin building the branch.
       @param level: (integer) - the level of the current submission-
        collection branch.
       @return: (dictionary) - the branch and its sub-branches.
    """
    elem = {} ## The dictionary to contain this branch of the tree.
    ## First, get the submission-collection-details:
    collctn_name = get_submission_collection_name(id_father)
    if collctn_name is not None:
        ## Got the submission-collection's name:
        elem['name'] = collctn_name
    else:
        ## The submission-collection is unknown to the DB
        ## set its name as empty:
        elem['name'] = ""
    elem['id']    = id_father
    elem['level'] = level

    ## Now get details of the doctype-children of this
    ## submission-collection:
    elem['docs'] = []  ## List to hold the doctype-children
                       ## of the submission-collection
    doctype_children = \
       get_doctype_children_of_submission_collection(id_father)
    for child_doctype in doctype_children:
        elem['docs'].append(getDoctypeBranch(child_doctype[0]))

    ## Now, get the collection-children of this submission-collection:
    elem['sons'] = []
    collctn_children = \
         get_collection_children_of_submission_collection(id_father)
    for child_collctn in collctn_children:
        elem['sons'].append(getCatalogueBranch(child_collctn[0], level + 1))

    ## Now return this branch of the built-up 'collection-tree':
    return elem

def getDoctypeBranch(doctype):
    """Create a document-type 'leaf-node' for the submission-collections
       tree. Basically, this leaf is a dictionary containing the name
       and ID of the document-type submission to which it links.
       @param doctype: (string) - the ID of the document type.
       @return: (dictionary) - the document-type 'leaf node'. Contains
        the following values:
          + id:   (string) - the document-type ID.
          + name: (string) - the (long) name of the document-type.
    """
    ldocname = get_longname_of_doctype(doctype)
    if ldocname is None:
        ldocname = "Unknown Document Type"
    return { 'id' : doctype, 'name' : ldocname, }

def displayCatalogueBranch(id_father, level, catalogues):
    text = ""
    collctn_name = get_submission_collection_name(id_father)
    if collctn_name is None:
        ## If this submission-collection wasn't known in the DB,
        ## give it the name "Unknown Submission-Collection" to
        ## avoid errors:
        collctn_name = "Unknown Submission-Collection"

    ## Now, create the display for this submission-collection:
    if level == 1:
        text = "<LI><font size=\"+1\"><strong>%s</strong></font>\n" \
               % collctn_name
    else:
        ## TODO: These are the same (and the if is ugly.) Why?
        if level == 2:
            text = "<LI>%s\n" % collctn_name
        else:
            if level > 2:
                text = "<LI>%s\n" % collctn_name

    ## Now display the children document-types that are attached
    ## to this submission-collection:
    ## First, get the children:
    doctype_children = get_doctype_children_of_submission_collection(id_father)
    collctn_children = get_collection_children_of_submission_collection(id_father)

    if len(doctype_children) > 0 or len(collctn_children) > 0:
        ## There is something to display, so open a list:
        text = text + "<UL>\n"
    ## First, add the doctype leaves of this branch:
    for child_doctype in doctype_children:
        ## Add the doctype 'leaf-node':
        text = text + displayDoctypeBranch(child_doctype[0], catalogues)

    ## Now add the submission-collection sub-branches:
    for child_collctn in collctn_children:
        catalogues.append(child_collctn[0])
        text = text + displayCatalogueBranch(child_collctn[0], level+1, catalogues)

    ## Finally, close up the list if there were nodes to display
    ## at this branch:
    if len(doctype_children) > 0 or len(collctn_children) > 0:
        text = text + "</UL>\n"

    return text

def displayDoctypeBranch(doctype, catalogues):
    text = ""
    ldocname = get_longname_of_doctype(doctype)
    if ldocname is None:
        ldocname = "Unknown Document Type"
    text = "<LI><a href=\"\" onmouseover=\"javascript:" \
           "popUpTextWindow('%s',true,event);\" onmouseout" \
           "=\"javascript:popUpTextWindow('%s',false,event);\" " \
           "onClick=\"document.forms[0].doctype.value='%s';" \
           "document.forms[0].submit();return false;\">%s</a>\n" \
           % (doctype, doctype, doctype, ldocname)
    return text


def action(req, c=cdsname, ln=cdslang, doctype=""):
    # load the right message language
    _ = gettext_set_language(ln)

    nbCateg = 0
    snameCateg = []
    lnameCateg = []
    actionShortDesc = []
    indir = []
    actionbutton = []
    statustext = []
    t = ""
    ln = wash_language(ln)
    # get user ID:
    try:
        uid = getUid(req)
        uid_email = get_email(uid)
    except Error, e:
        return errorMsg(e, req, c, ln)
    #parses database to get all data
    ## first, get the list of categories
    doctype_categs = get_categories_of_doctype(doctype)
    for doctype_categ in doctype_categs:
        nbCateg = nbCateg+1
        snameCateg.append(doctype_categ[0])
        lnameCateg.append(doctype_categ[1])

    ## Now get the details of the document type:
    doctype_details = get_doctype_details(doctype)
    if doctype_details is None:
        ## Doctype doesn't exist - raise error:
        return errorMsg (_("Unable to find document type.") + str(doctype), req)
    else:
        docFullDesc  = doctype_details[0]
        docShortDesc = doctype_details[1]
        description  = doctype_details[4]

    ## Get the details of the actions supported by this document-type:
    doctype_actions = get_actions_on_submission_page_for_doctype(doctype)
    for doctype_action in doctype_actions:
        ## Get the details of this action:
        action_details = get_action_details(doctype_action[0])
        if action_details is not None:
            actionShortDesc.append(doctype_action[0])
            indir.append(action_details[1])
            actionbutton.append(action_details[4])
            statustext.append(action_details[5])

    ## Send the gathered information to the template so that the doctype's
    ## home-page can be displayed:
    t = websubmit_templates.tmpl_action_page(
          ln=ln,
          uid=uid, guest=(uid_email == "" or uid_email == "guest"),
          pid = os.getpid(),
          now = time.time(),
          doctype = doctype,
          description = description,
          docfulldesc = docFullDesc,
          snameCateg = snameCateg,
          lnameCateg = lnameCateg,
          actionShortDesc = actionShortDesc,
          indir = indir,
          # actionbutton = actionbutton,
          statustext = statustext,
        )

    p_navtrail = """<a href="/submit">%(submit)s</a>""" % {'submit' : _("Submit")}

    return page(title = docFullDesc,
                body=t,
                navtrail=p_navtrail,
                description="submit documents",
                keywords="submit",
                uid=uid,
                language=ln,
                req=req,
                navmenuid='submit'
               )

def Request_Print(m, txt):
    """The argumemts to this function are the display mode (m) and the text
       to be displayed (txt).
       If the argument mode is 'ALL' then the text is unconditionally echoed
       m can also take values S (Supervisor Mode) and U (User Mode). In these
       circumstances txt is only echoed if the argument mode is the same as
       the current mode
    """
    global dismode
    if m == "A" or m == dismode:
        return txt
    else:
        return ""

def Evaluate_Parameter (field, doctype):
    # Returns the literal value of the parameter. Assumes that the value is
    # uniquely determined by the doctype, i.e. doctype is the primary key in
    # the table
    # If the table name is not null, evaluate the parameter

    ## TODO: The above comment looks like nonesense? This
    ## function only seems to get the values of parameters
    ## from the db...

    ## Get the value for the parameter:
    param_val = get_parameter_value_for_doctype(doctype, field)
    if param_val is None:
        ## Couldn't find a value for this parameter for this doctype.
        ## Instead, try with the default doctype (DEF):
        param_val = get_parameter_value_for_doctype("DEF", field)
    if param_val is None:
        ## There was no value for the parameter for the default doctype.
        ## Nothing can be done about it - return an empty string:
        return ""
    else:
        ## There was some kind of value for the parameter; return it:
        return param_val


def Get_Parameters (function, doctype):
    """For a given function of a given document type, a dictionary
       of the parameter names and values are returned.
       @param function: (string) - the name of the function for which the
        parameters are to be retrieved.
       @param doctype: (string) - the ID of the document type.
       @return: (dictionary) - of the parameters of the function.
        Keyed by the parameter name, values are of course the parameter
        values.
    """
    parray = {}
    ## Get the names of the parameters expected by this function:
    func_params = get_parameters_of_function(function)
    for func_param in func_params:
        ## For each of the parameters, get its value for this document-
        ## type and add it into the dictionary of parameters:
        parameter = func_param[0]
        parray[parameter] = Evaluate_Parameter (parameter, doctype)
    return parray

def get_level(doctype, action):
    """Get the level of a given submission. If unknown, return 0
       as the level.
       @param doctype: (string) - the ID of the document type.
       @param action: (string) - the ID of the action.
       @return: (integer) - the level of the submission; 0 otherwise.
    """
    subm_details = get_details_of_submission(doctype, action)
    if subm_details is not None:
        ## Return the level of this action
        subm_level = subm_details[9]
        try:
            int(subm_level)
        except ValueError:
            return 0
        else:
            return subm_level
    else:
        return 0

def action_details (doctype, action):
    # Prints whether the action is mandatory or optional. The score of the
    # action is returned (-1 if the action was optional)
    subm_details = get_details_of_submission(doctype, action)
    if subm_details is not None:
        if subm_details[9] != "0":
            ## This action is mandatory; return the score:
            return subm_details[10]
        else:
            return -1
    else:
        return -1

def print_function_calls (req, doctype, action, step, form, start_time, ln=cdslang):
    # Calls the functions required by an "action" action on a "doctype" document
    # In supervisor mode, a table of the function calls is produced
    global htdocsdir,storage,access,pylibdir,dismode,user_info
    user_info = collect_user_info(req)
    # load the right message language
    _ = gettext_set_language(ln)
    t = ""

    ## Get the list of functions to be called
    funcs_to_call = get_functions_for_submission_step(doctype, action, step)

    ## If no functions are found at this step for this doctype,
    ## get the functions for the DEF(ault) doctype:
    if len(funcs_to_call) == 0:
        funcs_to_call = get_functions_for_submission_step("DEF", action, step)
    if len(funcs_to_call) > 0:
        # while there are functions left...
        functions = []
        for function in funcs_to_call:
            function_name = function[0]
            function_score = function[1]
            currfunction = {
              'name' : function_name,
              'score' : function_score,
              'error' : 0,
              'text' : '',
            }
            if os.path.exists("%s/invenio/websubmit_functions/%s.py" % (pylibdir, function_name)):
                # import the function itself
                #function = getattr(invenio.websubmit_functions, function_name)
                execfile("%s/invenio/websubmit_functions/%s.py" % (pylibdir, function_name), globals())
                if not globals().has_key(function_name):
                    currfunction['error'] = 1
                else:
                    function = globals()[function_name]
                    # Evaluate the parameters, and place them in an array
                    parameters = Get_Parameters(function_name, doctype)
                    # Call function:
                    log_function(curdir, "Start %s" % function_name, start_time)
                    try:
                        func_returnval = function(parameters, curdir, form)
                    except InvenioWebSubmitFunctionWarning, err:
                        ## There was an unexpected behaviour during the execution.
                        ## Log the message into function's log and go to next function
                        log_function(curdir, "***Warning*** from %s: %s" % (function_name, str(err)), start_time)
                    log_function(curdir, "End %s" % function_name, start_time)
                    if func_returnval is not None:
                        ## Append the returned value as a string:
                        currfunction['text'] = str(func_returnval)
                    else:
                        ## The function the NoneType. Don't keep that value as
                        ## the currfunction->text. Replace it with the empty
                        ## string.
                        currfunction['text'] = ""
            else:
                currfunction['error'] = 1
            functions.append(currfunction)

        t = websubmit_templates.tmpl_function_output(
              ln = ln,
              display_on = (dismode == 'S'),
              action = action,
              doctype = doctype,
              step = step,
              functions = functions,
            )
    else :
        if dismode == 'S':
            t = "<br /><br /><b>" + _("The chosen action is not supported by the document type.") + "</b>"
    return t


def Propose_Next_Action (doctype, action_score, access, currentlevel, indir, ln=cdslang):
    global machine, storage, act, rn
    t = ""
    next_submissions = \
         get_submissions_at_level_X_with_score_above_N(doctype, currentlevel, action_score)

    if len(next_submissions) > 0:
        actions = []
        first_score = next_submissions[0][10]
        for action in next_submissions:
            if action[10] == first_score:
                ## Get the submission directory of this action:
                nextdir = get_storage_directory_of_action(action[1])
                if nextdir is None:
                    nextdir = ""
                curraction = {
                  'page' : action[11],
                  'action' : action[1],
                  'doctype' : doctype,
                  'nextdir' : nextdir,
                  'access' : access,
                  'indir' : indir,
                  'name' : action[12],
                }
                actions.append(curraction)

        t = websubmit_templates.tmpl_next_action(
              ln = ln,
              actions = actions,
            )
    return t

def errorMsg(title, req, c=cdsname, ln=cdslang):
    # load the right message language
    _ = gettext_set_language(ln)

    return page(title = _("Error"),
                body = create_error_box(req, title=title, verbose=0, ln=ln),
                description="%s - Internal Error" % c,
                keywords="%s, Internal Error" % c,
                language=ln,
                req=req,
                navmenuid='submit')

def warningMsg(title, req, c=cdsname, ln=cdslang):
    # load the right message language
    _ = gettext_set_language(ln)

    return page(title = _("Warning"),
                body = title,
                description="%s - Internal Error" % c,
                keywords="%s, Internal Error" % c,
                language=ln,
                req=req,
                navmenuid='submit')

def specialchars(text):
    text = string.replace(text, "&#147;", "\042");
    text = string.replace(text, "&#148;", "\042");
    text = string.replace(text, "&#146;", "\047");
    text = string.replace(text, "&#151;", "\055");
    text = string.replace(text, "&#133;", "\056\056\056");
    return text

def log_function(curdir, message, start_time, filename="function_log"):
    """Write into file the message and the difference of time
    between starttime and current time
    @param curdir:(string) path to the destination dir
    @param message: (string) message to write into the file
    @param starttime: (float) time to compute from
    @param filname: (string) name of log file
    """
    time_lap = "%.3f" % (time.time() - start_time)
    if os.access(curdir, os.F_OK|os.W_OK):
        fd = open("%s/%s" % (curdir, filename), "a+")
        fd.write("""%s --- %s\n""" % (message, time_lap))
        fd.close()

