# -*- coding: utf-8 -*-
##
## $Id: websube2.py,v 1.12 2007/08/17 10:47:37 nich Exp $
##
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
__revision__ = "$Id: websube2.py,v 1.12 2007/08/17 10:47:37 nich Exp $"

from invenio.config import cdslang, storage, etcdir
from invenio.messages import gettext_set_language, wash_language
from invenio.webuser import collect_user_info
from invenio.dbquery import run_sql
from invenio.data_cacher import DataCacher
from invenio.websubmit_xslt_engine import parse
from invenio.bibformat import format_record

import invenio.template
websubmit_templates = invenio.template.load('websubmit')

import types
import os
import cgi
import time
import xml
from xml.dom.minidom import parseString

## Some config constants:
CFG_WEBSUBMIT_SUBMISSION_TEMPLATES = etcdir + "/websubmit"
CFG_WEBSUBMIT_ELEMENTS_LIBRARY = etcdir + "/websubmit/element_library.xml"
CFG_WEBSUBMIT_ELEMENTS_IMPORT_PATH = "invenio.websubmit_elements"
CFG_WEBSUBMIT_CHECKS_IMPORT_PATH = "invenio.websubmit_checks"
CFG_WEBSUBMIT_MAX_UPLOADED_FILE_SIZE = 500*(2**20) ## 500Mbytes

## A data-cacher class to cache the library of WSEs DOM:

class WSELibraryDomDataCacher(DataCacher):
    """A class to build and cache the DOM "element" nodes of the
       WSE "elements" Library so that the library file doesn't need
       to be parsed on every visit to the submission page.
    """
    def __init__(self):
        """Initialize a cache of the WSE Library DOM."""
        def cache_filler():
            """A method to fill the WSE_Library_DOM cache file on disc.
               Basically, the WSE Library XML is parsed into a DOM, the
               interesting element nodes are referenced in a dictionary by
               WSE-name, and the resulting dictionary is serialized to a cache-
               file on disc. The DOM is then unlinked.
               When the various WebSubmit functions want to use the Library DOM
               elements, they will read the cached dictionary back data from the
               cache-file and treat it as if it were any normal dictionary.
               @return: (dictionary) - DOM "element" nodes, keyed by their WSE
                names (e.g. WSE_Title).
            """
            ## Initialise a dictionary of DOM "element" nodes,
            ## keyed by WSE name: 
            dom_elements_by_name = {}

            ## Now read in the WSE Library XML config file:
            ## (Note: it may not exist. If it doesn't exist, we just pass
            ## over this quietly and return an empty cache):
            if os.path.exists(CFG_WEBSUBMIT_ELEMENTS_LIBRARY):
                try:
                    xml_fh = open(CFG_WEBSUBMIT_ELEMENTS_LIBRARY, "r")
                    xml_file_body = xml_fh.read()
                    xml_fh.close()
                except IOError, err:
                    ## Unable to read the WSE Library config file.
                    ## There isn't much that we can do here, just re-raise
                    ## this error:
                    raise err

                ## Parse the WSE Library XML into a DOM:
                try:
                    dom = parseString(xml_file_body)
                except xml.parsers.expat.ExpatError, err:
                    ## Some kind of error occurred when we tried to parse the
                    ## XML file. There isn't much that we can do here,
                    ## just re-raise this error:
                    msg = "There was a problem parsing the WSE Library file: " \
                          "(%s)" % str(err)
                    raise InvenioWebSubmitConfigFileError(msg)
                else:
                    ## We now have the DOM.
                    ## Extract all of the element nodes and put them into the
                    ## "dom_elements_by_name" dictionary:
                    for element in dom.getElementsByTagName("element"):
                        try:
                            dom_elements_by_name[\
                             element.getAttribute("name").encode("utf-8")] \
                              = element
                        except AttributeError, err:
                            ## This element doesn't seem to have a name
                            ## attribute, but name is mandatory for a library
                            ## element. The Library XML is therefore not valid
                            ## and we cannot continue:
                            msg = "There was a problem parsing the WSE Library"\
                                  " file. All elements must have a name " \
                                  "attribute."
                            raise InvenioWebSubmitConfigFileError(msg)
                    ## Now return the elements dictionary:
                    return dom_elements_by_name
        
        def timestamp_getter():
            """Return the last update time of the WSE Library XML file as a
               (string) timestamp of the following format:
                  2007-08-13 13:58:13
               @return: (string) - timestamp.
            """
            ## Get the time of the last modification of the WSE Library
            ## XML file (in seconds past the epoch):
            time_last_modification = \
                            os.stat(CFG_WEBSUBMIT_ELEMENTS_LIBRARY).st_mtime
            ## Convert the last-modification time to a 9-sequence tuple and
            ## then into a timestamp string of a format like
            ## "2007-08-13 13:58:13":
            last_modified_timestamp = time.strftime("%Y-%m-%d %H:%M:%S", \
                                        time.localtime(time_last_modification))
            return last_modified_timestamp

        ## Call the 
        DataCacher.__init__(self, cache_filler, timestamp_getter)

## Now check to see whether the cached elements library exists and is OK.
## If not, re-create it:
try:
    DUMMY = WSE_LIBRARY_DOM_CACHE.is_ok_p
except NameError:
    ## It isn't OK - re-create it:
    WSE_LIBRARY_DOM_CACHE = WSELibraryDomDataCacher()



## Definition of WebSubmit Exceptions:

class InvenioWebSubmitConfigFileError(Exception):
    """This exception is used to signal that there was an unresolvable
       problem with one of the configuration files used by WebSubmit and that
       as a result the submission had to be halted.
       An example could be that a mandatory attribute was missing from one
       of the elements in a config file.  E.g.:
         Expected something like this:
           <element-label ln="en">Abstract</element-label>
         Got something like this:
           <element-label>Abstract</element-label>
         Since the "ln" (language) attribute was considered mandatory for the
         element-label tag, WebSubmit may raise this exception.
       Extends: Exception.
    """
    def __init__(self, value):
        """Set the internal "value" attribute to that of the passed "value"
           parameter.
           @param value: (string) - a string to display to the user.
        """
        Exception.__init__(self)
        self.value = value
    def __str__(self):
        """Return oneself as a string (actually, return the contents of
           self.value).
           @return: (string)
        """
        return str(self.value)


class InvenioWebSubmitInternalError(Exception):
    """This exception should be raised and caught within WebSubmit itself.
       It is used to signal that there was some kind of internal problem that
       prevented normal operation. An example of this could be some kind of
       disk space problem that prevented files from being written.
       Extends: Exception.
    """
    def __init__(self, value):
        """Set the internal "value" attribute to that of the passed "value"
           parameter.
           @param value: (string) - a string to display to the user.
        """
        Exception.__init__(self)
        self.value = value
    def __str__(self):
        """Return oneself as a string (actually, return the contents of
           self.value).
           @return: (string)
        """
        return str(self.value)

class InvenioWebSubmitAuthenticationError(Exception):
    """This exception should be raised and caught within WebSubmit itself.
       It is used to signal that the user was not authenticated to perform
       a given action relating to a submission.
       Extends: Exception.
    """
    def __init__(self, value):
        """Set the internal "value" attribute to that of the passed "value"
           parameter.
           @param value: (string) - a string to display to the user.
        """
        Exception.__init__(self)
        self.value = value
    def __str__(self):
        """Return oneself as a string (actually, return the contents of
           self.value).
           @return: (string)
        """
        return str(self.value)

class InvenioWebSubmitFormArgumentError(Exception):
    """This exception should be raised and caught within WebSubmit itself.
       It is used to signal that there was a problem with one or more of
       the arguments passed via the WebSubmit submission form, which
       prevented normal operation. An example of this could be that the
       document-type was missing, making it impossible to build the
       submission page.
       Extends: Exception.
    """
    def __init__(self, value):
        """Set the internal "value" attribute to that of the passed "value"
           parameter.
           @param value: (string) - a string to display to the user.
        """
        Exception.__init__(self)
        self.value = value
    def __str__(self):
        """Return oneself as a string (actually, return the contents of
           self.value).
           @return: (string)
        """
        return str(self.value)

## Definition of WebSubmit Submission Object:

class InvenioWebSubmitSubmissionObject(object):
    """This class represents a WebSubmit "submission" object.
       It contains all information relevant to a submission that is being made
       at any given time.
    """
    def __init__(self, req, ln=cdslang):
        """Initialise a wso.
           @param req: (mod_python.Request object) - the Apache request object.
            This req object also contains a member "form", which is a
            mod_python.util.FieldStorage object and contains all of the data
            submitted to the server on the last visit to the page.
           @param ln: (string) - the interface language code (defaults to the
            cds-invenio installation's default language).
        """
        ## Keep a local reference to the request object:
        self.req = req
        ## Wash and store the interface language:
        self.ln = wash_language(ln)
        ## Extract the WSET fields from the request object's form object:
        self.submitted_form_fields = get_wset_fields_from_form(req.form)
        ## Get information about the user and store it in the local
        ## "user_info" (dictionary) member:
        self.user_info = collect_user_info(req)

        ## If the form had a field "WebSubmit_document_type", extract it and
        ## store it:
        try:
            self.WebSubmit_document_type = \
                                   self.req.form["WebSubmit_document_type"]
        except KeyError:
            ## "WebSubmit_document_type" was not referred to in the form.
            self.WebSubmit_document_type = ""

        ## If the form had a field "WebSubmit_action", extract it and
        ## store it:
        try:
            self.WebSubmit_action = self.req.form["WebSubmit_action"]
        except KeyError:
            ## "WebSubmit_action" was not referred to in the form - use the
            ## default action (submit bibliographic information):
            self.WebSubmit_action = "submit"

        ## If the form had a field "WebSubmit_category", extract it and
        ## store it:
        if "WebSubmit_category" in self.req.form.keys():
            category = self.req.form["WebSubmit_category"]
            if isinstance(category, types.ListType):
                self.WebSubmit_category = category
            else:
                ## Since there is only one category, put it into a list:
                self.WebSubmit_category = [category]
        else:
            ## "WebSubmit_category" was not referred to in the form.
            self.WebSubmit_category = []

        ## If the form had a field "WebSubmit_Submission_Config", extract it
        ## and store it:
        try:
            self.WebSubmit_Submission_Config = \
                         self.req.form["WebSubmit_Submission_Config"]
        except KeyError:
            ## "WebSubmit_Submission_Config" was not referred to in the form
            ## Set it as blank.
            self.WebSubmit_Submission_Config = ""


        ## A local reference to the submission's ID:
        self.WebSubmit_submissionid = ""
        if "WebSubmit_submissionid" in self.req.form.keys():
            ## The submission form contains a "submission id", store it:
            self.WebSubmit_submissionid =  \
                                 self.req.form["WebSubmit_submissionid"]


## Database functions - FIXME (Move into DB Layer)

def register_new_submission(userid,
                            documenttype,
                            category,
                            action,
                            reportnum=""):
    """Register a new submission in the WebSubmit submission-log table.
       The database will allocate a submission-id to the submission. This
       submission-id will be returned for use in the submission process.
       @param userid: (integer) - the userid of the logged-in user (i.e.
        the owner of the submission.)
       @param documenttype: (string) - the code identifying the document-
        type to which the submission refers.
       @param category: (string) - the string containing the category/ies
        of the document type that the submission refers to.
       @param action: (string) the action performed for the submission (e.g.
        SBI, MBI, etc).
       @param reportnum: (string) - the report number of the record that is
        created or referred to (in the case of MBI) by the submission. The
        report number defaults to an empty string (because for new submissions,
        the report number is unknown when the submission is initialised -
        it's even possible that records referred to by a submission have no
        report number.)
       @return: (integer) - the "submission id".
    """
    ## Create the query string used to insert the new submission into
    ## the submission-log:
    qstr = """INSERT INTO sbmSUBMISSIONLOG """ \
           """(id_submitter, reference, document_type, """ \
           """category, action, date_creation, date_modification) VALUES """ \
           """(%s, %s, %s, %s, %s, NOW(), NOW())"""
    ## Log the new submission in the submission log table:
    submissionid = run_sql(qstr, \
                           (userid,
                            reportnum,
                            documenttype,
                            category,
                            action))
    ## submission_id contains the id number that was allocated to the
    ## submission in the log. Return it as an integer:
    return int(submissionid)

def update_submission_modificaton_date(submissionid):
    """Update the modification date for a given submission in the
       submission log table.
       @param submissionid: (integer) - the ID of the submission for which the
        modification date is to be updated.
       @return: None.
    """
    qstr = """UPDATE sbmSUBMISSIONLOG SET date_modification=NOW() """ \
           """WHERE id_submitter=%s"""
    run_sql(qstr, (submissionid,))

def submission_belongs_to_user(submissionid, userid):
    """This function queries the submission log table to see whether a
       given submission belongs to a given user. If it does, an integer value
       of 1 is returned. If it doesn't, an integer value of 0 is returned.
       @param submissionid: (integer) - the submission ID.
       @param userid: (integer) - the user ID.
       @return: (integer) 1 if the submission belongs to the user; 0 if not.
    """
    ## Reset a flag indicating whether or not the submission exists
    ## for the user:
    subm_exists = 0
    qstr = """SELECT COUNT(id) from sbmSUBMISSIONLOG """ \
           """WHERE id=%s AND id_submitter=%s"""
    qres = run_sql(qstr, (submissionid, userid))
    if len(qres) > 0:
        num_submissions = qres[0][0]
        try:
            num_submissions = int(num_submissions)
        except (ValueError, TypeError):
            ## Bad value for number of submissions, set as 0
            num_submissions = 0
        if num_submissions > 0:
            ## The submission exists in the log for this user:
            subm_exists = 1
    ## return submission-exists flag:
    return subm_exists

## Functions to obtain references to WebSubmit modules and objects:

def get_symbol_reference_from_symbol_name(symbol_name,
                                          import_module_path):
    """Obtain a reference to a given symbol in a given module, as dictated by
       the import_module_path and symbol_name parameters.
       Basically, from the name of the symbol, it obtains and returns a
       reference to the symbol itself.
       @param symbol_name: (string) - the name of the symbol for which a
        reference is to be retrieved.
       @param import_path: (string) - the path to the module containing the
        symbol to be retrieved.
       @return: (a symbol reference/None) - If the symbol could be retrieved,
        it will be returned to the caller. If there was an error retrieving it,
        the function will return None.
    """
    try:
        ## Import the module:
        module = __import__(import_module_path)
        ## Loop through all of the components in the path to the imported
        ## module and obtain a reference to that component's module. We move
        ## through all modules in the path, down to the target module:
        components = import_module_path.split(".")
        for comp in components[1:]:
            module = getattr(module, comp)
    except (AttributeError, ImportError):
        ## Either couldn't import the target module using the import path,
        ## or there was a problem traversing the imported modules.
        ## Anyway, it's not possible to obtain the desired symbol's
        ## reference.
        return None
    
    ## The "module" variable should now contain a reference to the module
    ## containing our symbol of interest. From this "target" module, get a
    ## reference to the symbol itself:
    try:
        ## Store the reference to the class in a local variable:
        symbol_reference = module.__dict__['%s' % symbol_name]
    except KeyError, err:
        ## The requested symbol did not exist in the target module.
        return None
    else:
        ## Return the reference to the class/function itself:
        return symbol_reference




## Submission session initialization:

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


def initialize_submission_session(wso):
    """When a new submission is started, it must be initialised. This means
       giving it a submission-id, storing basic information about it in
       the database (in the sbmSUBMISSIONLOG table), and creating a submission
       directory for it.
       Thereafter, upon every refresh of the page during the submission, the
       details of the submission must be checked (does it belong to the current
       user? does the submission directory exist? Etc.)
       This function performs those tasks. It checks:
        + User is logged in;
        + Document type has been supplied;
        + Action has been supplied;
        + If there is a submission ID:
           -- Make sure the user owns that submission by checking in the
              submission log table;
           -- Update the modification time for the submission in the
              submission log table;
           -- Check that the submission directory exists;
        + If there is no submission ID:
           -- Create a record for the submission in the submission log table,
              acquiring the submission ID and storing it in
              wso.WebSubmit_submissionid;
           -- Create the submission directory;
       This function may raise exceptions if any of the checks fail.
       @param wso: (WebSubmitSubmissionObject) - the object containing
        information about the current submission. It's used when checking
        details about the submission.
       @return: None
    """
    ## Ensure that there is a doctype stored in the WSO:
    if wso.WebSubmit_document_type == "":
        ## No doctype found - it's not possible to process a submission for
        ## an unknown doctype.
        msg = websubmit_templates.tmpl_error_unresolvable_doctype(wso.ln)
        raise InvenioWebSubmitFormArgumentError(msg)

    ## Ensure that there is an action stored in the WSO:
    if wso.WebSubmit_action == "":
        ## No action found - it's not possible to process a submission for
        ## an unknown action.
        msg = websubmit_templates.tmpl_error_unresolvable_action(wso.ln)
        raise InvenioWebSubmitFormArgumentError(msg)

    ## Test to see whether there is a submission-id stored in WSO:
    if wso.WebSubmit_submissionid != "":
        ## This is a visit to an existing "submission session".
        ## Check that the current user actually owns this submission session:
        user_owns_submission = \
             submission_belongs_to_user(wso.WebSubmit_submissionid, \
                                        wso.user_info["uid"])
        if not user_owns_submission:
            ## The current user doesn't have the permission to work with the
            ## current submission. Raise an exception with a message explaining
            ## this.
            msg = websubmit_templates.\
            tmpl_error_permission_denied_for_user_access_to_submission(\
                wso.user_info["nickname"], \
                wso.WebSubmit_submissionid, \
                wso.ln)
            raise InvenioWebSubmitAuthenticationError(msg)

        ## Update the modification time of this visit to the submission in the
        ## submission log table:
        update_submission_modificaton_date(wso.WebSubmit_submissionid)

        ## Check that the "submission directory" for this submission exists:
        submission_dir = "%s/%s/%s/%s" % (storage, \
                                          wso.WebSubmit_action, \
                                          wso.WebSubmit_document_type, \
                                          wso.WebSubmit_submissionid)
        ## Store the submission directory path in the WSO:
        wso.WebSubmit_submissiondir = submission_dir
        if not os.path.exists(submission_dir):
            ## Submission directory doesn't exist. This is an unexpected error
            ## and the submission cannot continue. The error should be logged
            ## and the user alerted.
            msg = websubmit_templates.\
            tmpl_error_submission_directory_not_found(\
                wso.WebSubmit_submissionid, \
                wso.ln)
            raise InvenioWebSubmitInternalError(msg)
    else:
        ## This is a new "submission-session".
        ## Obtain a submission 'id':
        submissionid = \
                  register_new_submission(\
                    wso.user_info["uid"], \
                    wso.WebSubmit_document_type, \
                    "[+]".join(wso.WebSubmit_category), \
                    wso.WebSubmit_action)
        ## Add the new submission's ID into WSO:
        wso.WebSubmit_submissionid = submissionid

        ## Create the "submission directory" for this submission:
        submission_dir = "%s/%s/%s/%s" % (storage, \
                                          wso.WebSubmit_action, \
                                          wso.WebSubmit_document_type, \
                                          wso.WebSubmit_submissionid)
        ## Store the submission directory path in the WSO:
        wso.WebSubmit_submissiondir = submission_dir
        ## Check to ensure that the submission directory does NOT already
        ## exist:
        if os.path.exists(submission_dir):
            ## Somehow the current submission dir exists. This shouldn't
            ## happen - the submission cannot continue.
            ## The error should be logged and the user alerted.
            msg = websubmit_templates.\
            tmpl_error_submission_directory_already_existed(\
                wso.WebSubmit_submissionid, \
                wso.ln)
            raise InvenioWebSubmitInternalError(msg)
        else:
            ## Create the submission directory:
            try:
                os.makedirs(submission_dir)
            except OSError, err:
                ## Unable to make the current submission directory.
                ## Permissions problem? The submission cannot continue.
                ## The user should be warned and the error should be logged.
                msg = websubmit_templates.\
                tmpl_error_couldnt_create_submission_directory(\
                    wso.WebSubmit_submissionid, \
                    str(err), \
                    wso.ln)
                raise InvenioWebSubmitInternalError(msg)


## ----- Submission Config Template XML File Parsing ------

def get_submission_components(wso):
    """This function serves as the interface between:
         (a) the XML parser that actually parses the XML submission
             configuration template in order to create the various structures
             and objects that make up a given submission;

          - and -

         (b) The functions that make use of these objects and structures in
             order to process the submission (e.g. the functions that create the
             submission forms, those that check input values, etc).

       From the data held in the WSO, the function determines which submission-
       configuration template should be used during the given submission,
       asks a parser to parse it and to return a tuple of 3 groups of elements
       that make up a submission's inner-workings.  The tuple returned by the
       parser is of the following structure:
          (submission-form-structure, data-checkers, interface-field-objects)

       The 3 items in this tuple are as follows:
          + submission-form-structure:
            This is a list of 2-element dictionaries, each of which represents
            a section on the submission form that is to be created. Each
            dictionary contains two members:
              + "container-label" (dictionary) - essentially the label that is
                to be displayed for a given form-section. The dictionary
                contains the label in various different languages, each of which
                is keyed by the language code;
              + "elements" (list) - a list of the NAMES of each of the WSET
                elements appearing within that particular section on the
                submission page.
            As an example, the submission-form-structure item could be something
            like this:

              [
                { 'container-label' : { 'fr' : 'Informations personnelles',
                                        'en' : 'Personal details',
                                      },
                  'elements'        : [ 'WSE_Surname',
                                        'WSE_First_Name',
                                        'WSE_Date_Of_Birth',
                                      ],
                },
                {
                  'container_label' : {
                                        'fr' : 'Adresse',
                                        'en' : 'Address',
                                      },
                  'elements'        : [
                                        'WSE_House_Number',
                                        'WSE_Street_Name',
                                        'WSE_Town',
                                        'WSE_Post_Code',
                                      ],
                }
              ]

          + data-checkers:
            This is a list of 3-cell tuples. The 3 members of each tuple are:
              + An internal reference to a WebSubmit Checking Function (WSC);
              + A string representing the arguments to be passed to the WSC
                when it is called;
              + A dictionary containing the error message (to be used when the
                data value is deemed invalid by the function) in various
                different languages - keyed by each language's code;
            The data-checkers list may therefore look something like this:
                [
                  ( <function wsc_string_length at 0x42b28d4c>,
                    '(abstract, 20)',
                    {
                      'en' : 'The abstract must be more than 20 characters in length',
                      'fr' : 'La taille du resume doit etre superieure a 20 caracteres',
                    }
                  ),
                  ( <function wsc_string_length at 0x42b28d4c>,
                    '(title, 30)',
                    {
                      'en' : 'The title must be more than 30 characters in length',
                      'fr' :  'La taille du titre doit etre superieure a 30 caracteres',
                    }
                  ),
                ]
          + wset_instances:
            This is a dictionary containing references to the WSET objects that
            make up the submission form.
            Each object in the dictionary is keyed by its name as a string. The
            dictionary could look something like this:
                {
                  'WSE_PublicationJournal' :
                    <invenio.websubmit_elements.WSET_Select.WSET_Select object at 0x42b24cec>,
                  'WSE_Title' :
                    <invenio.websubmit_elements.WSET_TextArea.WSET_TextArea object at 0x427e18cc>,
                  'WSE_Abstract' :
                    <invenio.websubmit_elements.WSET_TextArea.WSET_TextArea object at 0x427e1aac>,
                }
       @param wso: (WebSubmitSubmissionObject instance) - the object that
        represents the current submission and stores data relating to it.
       @return: (tuple) - 3 elements as described above:
         (submission-form-structure, data-checkers, wset_instances)
    """
    ## Get the template name from the WSO:
    templatename = os.path.basename(wso.WebSubmit_Submission_Config).strip()

    ## Check that the templatename isn't empty:
    if templatename == "":
        ## there is no template-name. This value should have been passed in the
        ## submission form and its presence should have been checked earlier.
        ## Therefore, if it's not here, there was an unexpected problem.
        msg = websubmit_templates.\
            tmpl_error_unresolvable_submission_config_template(wso.ln)
        raise InvenioWebSubmitInternalError(msg)

    ## Build the full path to the submission configuration template:
    templatepath = """%(template-path)s/%(template-name)s.xml""" \
                   % {
                       'template-path' : CFG_WEBSUBMIT_SUBMISSION_TEMPLATES,
                       'template-name' : templatename,
                     }

    ## If the template file exists, parse it to obtain the submission objects:
    if not os.access(templatepath, os.F_OK|os.R_OK):
        ## The submission configuration template file doesn't seem to
        ## be readable. The submission can't continue - raise an error:
        msg = websubmit_templates.\
            tmpl_error_couldnt_access_submission_config_template(templatename, \
                                                                 wso.ln)
        raise InvenioWebSubmitInternalError(msg)

    ## Read in the submission config-file:
    try:
        config_fh = open(templatepath, "r")
        config_file_body = config_fh.read()
        config_fh.close()
    except IOError, err:
        ## Unable to read the template file - cant continue:
        msg = websubmit_templates.\
           tmpl_error_couldnt_read_submission_config_template(templatename,
                                                              str(err),
                                                              wso.ln)
        raise InvenioWebSubmitInternalError(msg)

    ## Now parse the config file:
    ## Note that the "create_submission_components_minidom" function could
    ## raise one of the following exceptions:
    ## (InvenioWebSubmitConfigFileError,
    ##  InvenioWebSubmitInternalError)
    ## This function won't handle them - rather let them propagate up to
    ## the caller for proper handling.
    submission_components = \
          create_submission_components_minidom(wso, config_file_body)

    ## Return the internal objects making up the submission:
    return submission_components


def create_submission_components_minidom(wso, xmltext):
    """This method accepts the contents of a submission configuration template
       in the form of an XML string and parses it in order to create the
       various components that are used during the course of the submission.

       The xml.dom.minidom parser is used to parse the XML string into a
       document tree that is used to create the submission objects.

       This function creates and returns a tuple containing 3 elements:
        (submission-form-structure, data-checkers, interface-field-objects)

       The 3 items in this tuple are as follows:
          + submission-form-structure:
            This is a list of 2-element dictionaries, each of which represents
            a section on the submission form that is to be created. Each
            dictionary contains two members:
              + "container-label" (dictionary) - essentially the label that is
                to be displayed for a given form-section. The dictionary
                contains the label in various different languages, each of which
                is keyed by the language code;
              + "elements" (list) - a list of the NAMES of each of the WSET
                elements appearing within that particular section on the
                submission page.
            As an example, the submission-form-structure item could be something
            like this:

              [
                { 'container-label' : { 'fr' : 'Informations personnelles',
                                        'en' : 'Personal details',
                                      },
                  'elements'        : [ 'WSE_Surname',
                                        'WSE_First_Name',
                                        'WSE_Date_Of_Birth',
                                      ],
                },
                {
                  'container_label' : {
                                        'fr' : 'Adresse',
                                        'en' : 'Address',
                                      },
                  'elements'        : [
                                        'WSE_House_Number',
                                        'WSE_Street_Name',
                                        'WSE_Town',
                                        'WSE_Post_Code',
                                      ],
                }
              ]

          + data-checkers:
            This is a list of 3-cell tuples. The 3 members of each tuple are:
              + An internal reference to a WebSubmit Checking Function (WSC);
              + A string representing the arguments to be passed to the WSC
                when it is called;
              + A dictionary containing the error message (to be used when the
                data value is deemed invalid by the function) in various
                different languages - keyed by each language's code;
            The data-checkers list may therefore look something like this:
                [
                  ( <function wsc_string_length at 0x42b28d4c>,
                    '(abstract, 20)',
                    {
                      'en' : 'The abstract must be more than 20 characters in length',
                      'fr' : 'La taille du resume doit etre superieure a 20 caracteres',
                    }
                  ),
                  ( <function wsc_string_length at 0x42b28d4c>,
                    '(title, 30)',
                    {
                      'en' : 'The title must be more than 30 characters in length',
                      'fr' :  'La taille du titre doit etre superieure a 30 caracteres',
                    }
                  ),
                ]
          + wset_instances:
            This is a dictionary containing references to the WSET objects that
            make up the submission form.
            Each object in the dictionary is keyed by its name as a string. The
            dictionary could look something like this:
                {
                  'WSE_PublicationJournal' :
                    <invenio.websubmit_elements.WSET_Select.WSET_Select object at 0x42b24cec>,
                  'WSE_Title' :
                    <invenio.websubmit_elements.WSET_TextArea.WSET_TextArea object at 0x427e18cc>,
                  'WSE_Abstract' :
                    <invenio.websubmit_elements.WSET_TextArea.WSET_TextArea object at 0x427e1aac>,
                }
       @param wso: (WebSubmitSubmissionObject instance) - the object that
        represents the current submission and stores data relating to it.
       @param xmltext: (string) - the contents of the submission's XML
        configuration template as a string of XML that is to be parsed by the
        minidom parser.
       @return: (tuple) - 3 elements as described above:
         (submission-form-structure, data-checkers, wset_instances)
    """
    ## A list of "data checkers" (WebSubimt Checking Functions and their
    ## associated arguments and error-messages):
    checkers = []
    ## A list of dictionaries, each of which represents a distinct section
    ## of the form:
    form_sections = []
    ## A dictionary containing the wset instances that will be used on the
    ## submission form, each of which is keyed by its name as a string:
    wset_instances = {}

    ## Parse the XML text:
    try:
        dom = parseString(xmltext)
    except xml.parsers.expat.ExpatError, err:
        ## There was an error parsing the XML file.
        ## Unable to continue - report the error by raising the
        ## relevant exception:
        templatename = wso.WebSubmit_Submission_Config.strip()
        msg = websubmit_templates.\
              tmpl_error_xml_submission_template_unparsable(templatename,
                                                            str(err),
                                                            wso.ln)
        raise InvenioWebSubmitConfigFileError(msg)

    ## Get the root of the document tree representing all components in
    ## this submission:
    root = dom.childNodes[0]
    
    ## #########################################################################
    ## Handle content relating to the interface creation (the elements that
    ## should appear on the submission form and their "containers", etc.
    ## #########################################################################

    ## Obtain all "container" elements from the submission config dom tree.
    ## A "cointainer" element effectively represents a given "section" on the
    ## submission page and will contain "WSET" elements.
    ## For each container node, get its labels and the elements contained
    ## within it so that they can be added as a unit into the list of form-
    ## sections:
    for container_node in root.getElementsByTagName("container"):
        ## A list of the names of the WSETs that appear on the current page
        ## section:
        element_names = []
        ## A dictionary of the page-section's label in various languages (keyed
        ## by the language code):
        section_label = {}

        ## Obtain this page-section's label in its various language
        ## translations and store them in the "section_label" dictionary:
        for c_label in container_node.getElementsByTagName("container-label"):
            if c_label.hasAttribute("ln") and c_label.hasChildNodes():
                ## Store the label (keyed by the value of "ln" in the section-
                ## label dictionary:
                label_lang = c_label.getAttribute("ln").encode("utf-8")
                label_text = c_label.firstChild.nodeValue.encode("utf-8")
                section_label[label_lang] = label_text
            else:
                ## Oops. This label seems to be missing either its "ln"
                ## (language) attribute, or its message value. Both are
                ## mandatory. Halt the submission and report an error:
                templatename = wso.WebSubmit_Submission_Config.strip()
                msg = websubmit_templates.\
                   tmpl_error_xml_submission_template_container_label_invalid(\
                    templatename,
                    wso.ln)
                ## Cleanup the DOM:
                dom.unlink()
                ## Raise the exception:
                raise InvenioWebSubmitConfigFileError(msg)

        ## For each of the elements below this container node, get its details,
        ## and instantiate the element.
        for element_node in container_node.getElementsByTagName("element"):
            element_label = {} ## Dictionary containing the label to be
                               ## associated with the element, in its various
                               ## different languages
            option_values = [] ## If the element is some kind of option-list,
                               ## "options" to be displayed in the list may
                               ## be supplied in the config file.
            default_value = "" ## A default value may be supplied for the
                               ## element.
            attrs = {}         ## Attributes that are taken from the config
                               ## will be kept in the "attrs" dictionary and
                               ## then passed to the relevant WSET's
                               ## __init__ method.

            ## Get the name of this element:
            element_name = element_node.getAttribute("name").encode("utf-8")

            ## Check that the name is not empty. (Element-name is mandatory.)
            if element_name == "":
                ## Oops. The name attrbute seems to be missing. Halt the
                ## submission with an appropriate error message.
                templatename = wso.WebSubmit_Submission_Config.strip()
                msg = websubmit_templates.\
                      tmpl_error_xml_submission_template_element_name_missing(\
                       templatename,
                       wso.ln)
                ## Cleanup the DOM:
                dom.unlink()
                ## Raise the exception:
                raise InvenioWebSubmitConfigFileError(msg)

            ## Does the element node have a "type" attribute? If not, then it
            ## should be present in a "common elements library" config file.
            if not element_node.hasAttribute("type"):
                ## Check for the element by name in the elements library:
                wse_library = WSE_LIBRARY_DOM_CACHE.get_cache()
                if wse_library.has_key(element_name):
                    ## The element is in the wse library - get it directly from
                    ## there:
                    current_element = wse_library[element_name]
                else:
                    ## The element does not have an entry in the library.
                    ## If an element node doesn't have a "type" attribute,
                    ## it's madatory that it be in the library. Since it's not
                    ## in this case, we can assume that the element tag in the
                    ## config file was missing the mandatory "type" attribute.
                    ## Raise an exception containing an appropriate error
                    ## message:
                    templatename = wso.WebSubmit_Submission_Config.strip()
                    msg = websubmit_templates.\
                      tmpl_error_xml_submission_template_element_type_missing(\
                        templatename,
                        element_name,
                        wso.ln)
                    ## Cleanup the DOM:
                    dom.unlink()
                    ## Raise the exception:
                    raise InvenioWebSubmitConfigFileError(msg)
            else:
                ## Since this element had a type, don't look in the library,
                ## take the description from this config file:
                current_element = element_node

            ## Store the various attributes of this element tag into the attrs
            ## dictionary as UTF-8 encoded byte strings of key->value pairs
            ## (attribute-name ---> attribute-value):
            for (key, value) in current_element.attributes.items():
                attrs[key.encode("utf-8")] = value.encode("utf-8")

            ## OK, now extract the element type from the attributes dictionary:
            try:
                element_type = attrs["type"]
            except KeyError, err:
                ## Oops. It has no type. Is it possible that the element if we
                ## took this element information from the common elements
                ## library file, 
                templatename = wso.WebSubmit_Submission_Config.strip()
                msg = websubmit_templates.\
                  tmpl_error_xml_submission_template_element_type_missing(\
                    templatename,
                    element_name,
                    wso.ln)
                ## Cleanup the DOM:
                dom.unlink()
                ## Raise the exception:
                raise InvenioWebSubmitConfigFileError(msg)

            ## Having extracted the "type" of this element, remove it from the
            ## attributes dictionary:
            del attrs["type"]

            ## Does this element have a "default value" node?
            ## If so, it represents the default value that is to be
            ## assigned to the element. Get it.
            if current_element.getElementsByTagName("default-value"):
                ## There is a default value. Get and store it:
                try:
                    default_value = \
                       current_element.\
                       getElementsByTagName("default-value")[0].\
                       firstChild.nodeValue.encode("utf-8")
                except AttributeError:
                    ## Despite having a default-value node, there is no actual
                    ## value for this element's "default value"! If the default-
                    ## value node is present, it must have a value.
                    templatename = wso.WebSubmit_Submission_Config.strip()
                    msg = websubmit_templates.\
                      tmpl_error_xml_submission_template_node_value_missing(\
                        templatename,
                        "default-value",
                        wso.ln)
                    ## Cleanup the DOM:
                    dom.unlink()
                    ## Raise the exception:
                    raise InvenioWebSubmitConfigFileError(msg)

            ## This WSET element may have a label, which may be represented in
            ## various languages. Get and store each translation of the label:
            for el_label in \
                    current_element.getElementsByTagName("element-label"):
                ## It is mandatory for this element-label node to have a
                ## "ln" (language) attribute and a value:
                if el_label.hasAttribute("ln") \
                       and el_label.hasChildNodes():
                    ## Get the label text and store it into the element_label
                    ## dictionary under its language code:
                    element_label[el_label.getAttribute("ln")] = \
                                   el_label.firstChild.nodeValue.encode("utf-8")
                else:
                    ## This element label was missing either its "ln" attribute,
                    ## or its value. Since they are both mandatory, this is
                    ## considered to be an error in the template.
                    templatename = wso.WebSubmit_Submission_Config.strip()
                    msg = websubmit_templates.\
                      tmpl_error_xml_submission_template_invalid_element_label(
                          templatename,
                          element_name,
                          wso.ln)
                    ## Cleanup the DOM:
                    dom.unlink()
                    ## Raise the exception:
                    raise InvenioWebSubmitConfigFileError(msg)

            ## If this element is some kind of option-list, various "options"
            ## may have been supplied for it. If they are present, retrieve
            ## them and store their details in the "option_values" list:
            for opt in current_element.getElementsByTagName("option"):
                ## Initialise a dictionary to contain the details of the option:
                option = { 'value'    : "",
                           'label'    : {},
                           'selected' : "no",
                         }
                
                ## Get the (MANDATORY) value attribute:
                if opt.hasAttribute("value"):
                    ## Save the value for this option:
                    option['value'] = opt.getAttribute("value").encode("utf-8")
                else:
                    ## The option seems to be missing its mandatory value
                    ## attribute. This is a template error.
                    templatename = wso.WebSubmit_Submission_Config.strip()
                    msg = websubmit_templates.\
                     tmpl_error_xml_submission_template_invalid_element_option(\
                         templatename,
                         element_name,
                         wso.ln)
                    ## Cleanup the DOM:
                    dom.unlink()
                    ## Raise the exception:
                    raise InvenioWebSubmitConfigFileError(msg)

                ## Does this option have a selected attibute?
                if opt.hasAttribute("selected"):
                    ## The option has a selected attribute.
                    ## It should be set to either "yes" or "no". By default,
                    ## when the "option" structure was created above, "selected"
                    ## was set to "no", so if the value of the attribute is not
                    ## "yes", it will be ignored.
                    selected_value = \
                      opt.getAttribute("selected").encode("utf-8").lower()
                    if selected_value == "yes":
                        ## Mark this option as selected:
                        option['selected'] = selected_value

                ## If this option has option-labels, get them:
                for opt_label in opt.getElementsByTagName("option-label"):
                    ## The "ln" (language) attribute is mandatory for an
                    ## option-label, as is the node's value:
                    if opt_label.hasAttribute("ln") \
                           and opt_label.hasChildNodes():
                        ## Both ln and node-value are present - record them:
                        option['label'][opt_label.getAttribute("ln")] = \
                              opt_label.firstChild.nodeValue.encode("utf-8")
                    else:
                        ## There was a problem with the option. It's missing
                        ## the ln attribute, a value, or both.
                        templatename = wso.WebSubmit_Submission_Config.strip()
                        msg = websubmit_templates.\
                         tmpl_error_xml_submission_template_invalid_element_option(\
                             templatename,
                             element_name,
                             wso.ln)
                        ## Cleanup the DOM:
                        dom.unlink()
                        ## Raise the exception:
                        raise InvenioWebSubmitConfigFileError(msg)

                ## Append the structure representing this option into the
                ## list of options for this element:
                option_values.append(option)

            ## Try to get a reference to the class-type of the current element:
            element_import_path = "%s.%s" % \
                                    (CFG_WEBSUBMIT_ELEMENTS_IMPORT_PATH, \
                                     element_type)
            element_class_ref = \
                     get_symbol_reference_from_symbol_name(element_type,
                                                           element_import_path)
            ## Test the symbol reference for the element. If it's None, there
            ## was a problem importing the element's class reference and the
            ## submission should be halted.
            if element_class_ref is None:
                ## Oops. We don't have the element's class reference:
                msg = websubmit_templates.\
                 tmpl_error_unable_to_retrieve_WSET_class_reference(\
                     element_type, \
                     wso.ln)
                ## Cleanup the DOM:
                dom.unlink()
                ## Raise the exception:
                raise InvenioWebSubmitInternalError(msg)
                
            ## Now, add the element's name, values list, labels, and default-
            ## value into the dictionary of attributes that are to be passed
            ## to the class' __init__ method:
            attrs["wso"] = wso
            attrs["elementname"] = element_name
            attrs["optionvalues"] = option_values
            attrs["elementlabel"] = element_label
            attrs["defaultvalue"] = default_value

            ## Attempt to create an instance of the WSET from its class
            ## reference. Pass the attributes harvested from the config
            ## file to its __init__ method:
            try:
                element_instance = element_class_ref(**attrs)
            except TypeError, err:
                ## For some reason, it was not possible to instantiate the
                ## WSET class. Perhaps some mandatory arguments were missing?
                ## The submission must be halted.
                msg = websubmit_templates.\
                 tmpl_error_unable_to_instantiate_WSET_object(element_type,
                                                              str(err),
                                                              wso.ln)
                ## Cleanup the DOM:
                dom.unlink()
                ## Raise the exception:
                raise InvenioWebSubmitInternalError(msg)

            ## Append the name of the newly-created WSET into the list of
            ## element names:
            element_names.append(element_name)
            ## Store a reference to the newly-created WSET along with any
            ## others, keyed by its name:
            wset_instances[element_name] = element_instance

            ## Reset the place-holder for the current XML element node:
            current_element = None

        ## Create a dictionary to contain the labels and a list of the names of
        ## the WSET elements that are to be found in the page section
        ## represented by the current "container" node:
        form_section = {
                         "container_label" : {}, ## Dictionary of the page
                                                 ## Section's labels (keyed
                                                 ## by message language).
                         "elements"        : [], ## List of the names of the
                                                 ## WSET elements found in this
                                                 ## page section.
                       }
        ## Add the label and element names list into this form-section
        ## structure:
        form_section["container_label"] = section_label
        form_section["elements"] = element_names
        ## Add this section into the list of form sections:
        form_sections.append(form_section)


    ## #########################################################################
    ## Handle content relating to the data-input checks:
    ## #########################################################################

    ## Obtain all "check" elements from the submission config dom tree.
    ## A "check" element effectively represents a call to a WSC (WebSubmit
    ## checking function) that should be made for a given element or elements.
    for check in root.getElementsByTagName("check"):
        ## A dictionary to contain the error label that is to be associated
        ## with a given checking function call. This error label will be used
        ## in the event that the conditions imposed by the WSC were not met.
        ## Error labels may be present in various different languages.
        error_label = {}

        ## Check for the mandatory "test" attribute:
        if check.hasAttribute("test"):
            ## "test" is effectively the python call to the WSC. It is written
            ## in pretty much the same way to calling a function in python.
            ## It could look something like this, for example:
            ## wsc_string_length(WSE_publisher, &quot;30&quot;, &quot;10&quot;)
            ## Get this call as a string and store it:
            test = check.getAttribute("test").encode("utf-8")
        else:
            ## The "test" attribute is madatory (without it, it would be
            ## impossible to know which WSC to call or even how to call it).
            ## This is a template config error and the submission should
            ## be halted.
            msg = websubmit_templates.\
                   tmpl_error_xml_submission_template_invalid_check_node(\
                       templatename,
                       wso.ln)
            ## Cleanup the DOM:
            dom.unlink()
            ## Raise the exception:
            raise InvenioWebSubmitConfigFileError(msg)

        ## Split the "test" string into the WSC name and the parameters to be
        ## passed to it:
        try:
            ## Split this kind of thing: wsc_xyx(1, 2)
            ## ...into...
            ## wsc_xyx and (1, 2)
            (wsc_name, wsc_params) = test.split("(", 1)
            wsc_params = "(" + wsc_params
        except ValueError, err:
            ## Invalid format for "test" - this is a config template error and
            ## the submission should be halted:
            msg = websubmit_templates.\
                   tmpl_error_xml_submission_template_invalid_check_string(\
                       templatename,
                       wso.ln)
            ## Cleanup the DOM:
            dom.unlink()
            ## Raise the exception:
            raise InvenioWebSubmitConfigFileError(msg)

        ## Try to get a reference to the WSC:
        wsc_import_path = "%s.%s" % \
                                    (CFG_WEBSUBMIT_CHECKS_IMPORT_PATH, \
                                     wsc_name)
        wsc_ref = get_symbol_reference_from_symbol_name(wsc_name, \
                                                        wsc_import_path)

        ## Test the symbol reference for the WSC. If it's None, there
        ## was a problem importing the WSC function reference and the
        ## submission should be halted.
        if wsc_ref is None:
            ## Oops. We don't have the WSC's function reference:
            msg = websubmit_templates.\
             tmpl_error_unable_to_retrieve_WSC_function_reference(wsc_name, \
                                                                  wso.ln)
            ## Cleanup the DOM:
            dom.unlink()
            ## Raise the exception:
            raise InvenioWebSubmitInternalError(msg)

        ## Get any error labels belonging to this check:
        for err_label in check.getElementsByTagName("error-label"):
            if err_label.hasAttribute("ln") and err_label.hasChildNodes():
                error_label[err_label.getAttribute("ln").encode("utf-8")] = \
                                 err_label.firstChild.nodeValue.encode("utf-8")
            else:
                ## Oops. If error labels are present for a check, both the "ln"
                ## attribute and a message value are mandatory.
                msg = websubmit_templates.\
                   tmpl_error_xml_submission_template_invalid_check_node(\
                       templatename,
                       wso.ln)
                ## Cleanup the DOM:
                dom.unlink()
                ## Raise the exception:
                raise InvenioWebSubmitConfigFileError(msg)

        ## Now append the details of this check into the checkers list, as a
        ## tuple of (check-reference, check-parameters, error-label):
        checkers.append((wsc_ref, wsc_params, error_label))

    ## Finally, return a tuple of the submission components:
    return (form_sections, checkers, wset_instances)

## -------------- Page creation functions --------------------------------------


def get_submission_form(document_type,
                        action,
                        submission_config,
                        submission_id,
                        category,
                        ln,
                        form_sections,
                        wse_objects,
                        error_messages=None):
    """This function calls the relevant template methods to convert the
       submission data and WSEs belonging to a given submission into a HTML
       form that can be sent to the client.
       @param document_type: (string) - the submission's document type.
       @param action: (string) - the submission's "action".
       @param submission_config: (string) - the name of the config file used
        to create the submission interface.
       @param submission_id: (string) - the submission's identification code.
       @param category: (string) - the submission category.
       @param ln: (string) - the interface language.
       @param form_sections: (list) - of dictionaries, each of which
        represents a "form section" (a container of WSEs, appearing on
        the submission form).
       @param wse_objects: (dictionary) - WSET instances in a dictionary,
        keyed by their WSE fieldnames. Each of them is asked to return
        its HTML representation so that it can be included in the
        submission form.
       @param error_messages: (list) - the error messages that should be
        included in the submission form.
    """
    ## A buffer for the HTML representation of the form sections and WSEs:
    form_sections_html = ""
    
    ## loop through all of the form sections. For each of them, get the
    ## HTML for the container itself, and request the HTML for all of the
    ## WSET elements inside of it.
    ## Once we have all of the HTML for the components that make up the
    ## submission form, we can pass it to the relevant template method
    ## for inclusion in the submission form:
    for section in form_sections:
        ## The dictionary containing this section's label in its various
        ## translations:
        form_section_label    = section["container_label"]
        ## The list of the names of all of the elements in this form section:
        form_section_elements = section["elements"]
        ## A buffer to hold the HTML that represents the elements in this
        ## form section:
        section_elements_html = ""

        ## Now loop through the names of all of the elements in this form
        ## section.  For each, ask its WSET instance to return its
        ## HTML representation and pass this to the template method concerned
        ## with the representation of an element.
        ## Finally, concatenate the returned HTML to the end of the HTML buffer:
        for element_name in form_section_elements:
            section_elements_html += websubmit_templates.\
               tmpl_wse_html_instance(\
                wse_objects[element_name].get_html())

        ## Having retrieved the HTML for all of the WSEs in this form section,
        ## include that HTML into the HTML returned from the form-section
        ## template for the current form section:
        current_section_html = \
          websubmit_templates.tmpl_wse_group_container(form_section_label, \
                                                       cgi.escape(ln, 1)) \
                                                       % { 'elements' : \
                                                           section_elements_html
                                                         }
        ## Now append the HTML for the current form section to the HTML for
        ## all form sections:
        form_sections_html += current_section_html

    ## We now have the HTML for all sections of the submission form for the
    ## current submission. It can be passed to the template responsible for
    ## the creation of the HTML for the entire submission form:
    form_html = websubmit_templates.\
                  tmpl_submission_form_body(document_type,
                                            action,
                                            submission_config,
                                            submission_id,
                                            category.split("[+]"),
                                            form_sections_html,
                                            error_messages,
                                            ln)

    ## Finally, return the HTML for the submission form:
    return form_html

## ------ Data Checking Functions: ---------------------------------------------

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

## --------- Functions for XML record creation: --------------------------------

def create_simple_WSE_xml_record_file(wso):
    """This function retrieves the simple XML representation of each of the WSE
       objects that appears in the current submission and writes it to a simple
       XML record file ("simple_wse_record.xml") in the current submission
       directory.
       @param wso: (WebSubmitSubmissionObject) - the object representing the
        current submission. It contains the current submission's working
        directory and the WSE objects themselves.
       @return: (string) - the simple XML record.
       Exceptions raised: InvenioWebSubmitInternalError in the event that the
        XML file cannot be written.
    """
    ## Open a buffer string to contain the simple XML returned by the WSE
    ## objects (initialized with the opening "record" tag):
    xml_buffer = "<record>\n"
    ## Loop through the list of WSE instances. For each, request its simple XML
    ## representation and append it to the XML buffer:
    for wse in wso.wse_objects.values():
        xml_buffer += wse.get_xml()

    ## Now append a closing "record" tag to the simple XML record in the buffer:
    xml_buffer += "</record>\n"

    ## The simple XML record should now be written to disc in the current
    ## submission's working directory. Note that if it already exists
    ## (perhaps one of the WebSubmit functions previously sent the client
    ## back to the form for some reason), it will be truncated:
    try:
        xml_fh = open("%s/simple_wse_record.xml" \
                      % wso.WebSubmit_submissiondir, "w+")
        xml_fh.write(xml_buffer)
        xml_fh.close()
    except IOError, err:
        ## Oh dear, there was some kind of problem writing the simple WSE XML
        ## file. The submission cannot continue.
        msg = websubmit_templates.\
              tmpl_error_unable_to_create_simple_WSE_XML_record(\
                        str(err),
                        wso.ln)
        raise InvenioWebSubmitInternalError(msg)

    ## return the simple XML record as a string:
    return xml_buffer


def create_MARCXML_record_file_from_simple_XML(wso, simple_xml):
    """This function is responsible for the creation of the MARCXML record
       resulting from the submitted data.
       The function uses XSLT to transform the "simple" XML record
       (simple_wse_record.xml) that is created by concatenating the XML
       produced by calling the "get_xml" method of all of the WSE instances
       belonging to the given submission into a MARCXML record. This MARCXML
       record is then saved under the name "marcxml_record.xml" in the
       submission's working directory.
       @param wso: (WebSubmitSubmissionObject) - the object representing the
        current submission. Items encapsulated within it that are of
        interest to this function:
           + WebSubmit_submissiondir     - the current submission's working
                                           directory;
           + WebSubmit_Submission_Config - the name of the config template
                                           used by the current submission.
       @param simple_xml: (string) - the simple XML record that is to be
        transformed into a MARCXML record.
       @return: None.
       Exceptions raised:
        + InvenioWebSubmitInternalError in the event that the
          XML record file cannot be written or there is a problem during the
          XSLT translation.
    """
    ## First, ensure that the simple XML is not an empty string.
    if simple_xml.strip() != "":
        ## Translate the simple XML record.
        ## Read in the XSL template:
        try:
            xsl_template_fh = open(etcdir + "/websubmit/%s.xsl" \
                                   % wso.WebSubmit_Submission_Config, "r")
            xsl_template = xsl_template_fh.read()
            xsl_template_fh.close()
        except IOError, err:
            ## There was a problem retrieving the contents of the XSL template.
            ## The submission must be halted.
            msg = websubmit_templates.\
                  tmpl_error_unable_to_create_MARCXML_record(str(err), \
                                                             wso.ln)
            raise InvenioWebSubmitInternalError(msg)

        ## Now parse the simple XML against the XSL template using XSLT in order
        ## to obtain the new MARCXML record:
        try:
            marcxml_record = parse(xmltext=simple_xml, \
                                   template_source=xsl_template)
        except Exception, err:
            ## FIXME - some exceptions to catch here, but not yet sure which :-)
            msg = websubmit_templates.\
                  tmpl_error_unable_to_create_MARCXML_record(str(err), \
                                                             wso.ln)
            raise InvenioWebSubmitInternalError(msg)

        ## Now write the newly created MARCXML record to an XML file in the
        ## current submission's working directory:
        try:
            marcxml_rec_fh = open("%s/marcxml_record.xml" \
                                   % wso.WebSubmit_submissiondir, "w+")
            marcxml_rec_fh.write(marcxml_record)
            marcxml_rec_fh.close()
        except IOError, err:
            ## There was a problem writing the newly created MARCXML record to
            ## disc in the current submission's working directory.
            ## The submission must be halted.
            msg = websubmit_templates.\
                  tmpl_error_unable_to_create_MARCXML_record(str(err), \
                                                             wso.ln)
            raise InvenioWebSubmitInternalError(msg)


def create_XML_records(wso):
    """Glue function to handle the creation of both the simple XML and the
       MARCXML records.
       @param wso: (WebSubmitSubmissionObject) - the object representing the
        current submission.
    """
    ## First, create the simple XML record (both writing it to disc
    ## and retrieving the contents as an XML string):
    simple_xml = create_simple_WSE_xml_record_file(wso)
    ## Use the simple XML to create the MARCXML record; write it to disc:
    create_MARCXML_record_file_from_simple_XML(wso, simple_xml)


## ------ Functions to display a preview of the record: ------------------------

def get_record_preview(submission_dir, ln):
    """Use the MARCXML record created from the submitted data (i.e. saved as
       a file called "marcxml_record.xml" in the current submission's working
       directory) in order to obtain a preview of the submitted record's HTML-
       detailed output in the CDS Invenio repository. Return this preview
       as a string.
       @param submission_dir: (string) - the current submission's working
        directory.
       @param ln: (string) - the interface language.
       @return: (string) - the record preview, ready to be included in the
        page.
    """
    ## Read the saved record into a buffer:
    try:
        marcxml_rec_fh = open("%s/marcxml_record.xml" \
                               % submission_dir, "r")
        xml_buffer = marcxml_rec_fh.read()
        marcxml_rec_fh.close()
    except IOError, err:
        ## Unable to read the MARCXML record. Halt.
        msg = websubmit_templates.\
              tmpl_error_unable_to_read_MARCXML_record(str(err), \
                                                       ln)
        raise InvenioWebSubmitInternalError(msg)

    ## For some reason bibformat doesn't seem to like this line:
    ## <?xml version="1.0" encoding="UTF-8"?>
    ## If it's present at the beginning of the record, remove it.
    if xml_buffer.lstrip().startswith(\
        """<?xml version="1.0" encoding="UTF-8"?>"""):
        xml_buffer = xml_buffer.lstrip()[\
            len("""<?xml version="1.0" encoding="UTF-8"?>"""):]

    ## OK, get and return the formatted record preview:
    formatted_rec = format_record(-1, "hd", xml_record=xml_buffer, ln=ln)
    return formatted_rec.strip()

def create_preview_page_new_submission(submission_dir, ln):
    """From the newly created MARCXML record in the current submission's
       working directory, create a "preview page" that essentially asks the
       user to confirm that the submitted data looks OK and gives them a
       choice: finish the submission; edit the submitted data;
       @param submission_dir: (string) - the current submission's working
        directory.
       @param ln: (string) - the interface language.
       @return: (string) - the record preview confirmation page.
    """

## ----- Helper Functions ------------------------------------------------------

def serialize_wse_submitted_values(wse_objects):
    """Loop through all of the WSE Instances and ask each of them to pickle its
       value into the submission's working directory.
       @param wse_objects: (list) - contains the WSET instances found on the
        submission form.
    """
    ## Loop through all objects, asking them to serialize themselves to the
    ## current submission's working directory.
    for wse in wse_objects:
        ## Ask this wse to serialize itself:
        wse.serialize_values_to_submission_dir()


################################################################################
##
## *** Page request handling functions ***
##
################################################################################


def perform_request_create_submission_form(req, ln=cdslang):
    """This function creates the submission-form that the user sees and uses
       to submit metadata into CDS Invenio via WebSubmit.
       @param req: (mod_python.Request object) - the Apache request object.
        This req object also contains a member "form", which is a
        mod_python.util.FieldStorage object and contains all of the data
        submitted to the server on the last visit to the page.
       @param ln: (string) - the language of the interface. Defaults to
        cdslang if not provided.
       @return: (string) - the HTML page-body.
    """
    ## Initialize a string in which to hold the page-body:
    body = ""

    ## Using the mod-python request object, create a WebSubmit
    ## Submission Object to store details about the current submission:
    wso = InvenioWebSubmitSubmissionObject(req, ln)

    ## Prepare gettext according to the chosen language:
    _ = gettext_set_language(wso.ln)

    ## Guests are not allowed to use WebSubmit to submit into the
    ## repository. Is this user a guest?
    if wso.user_info["guest"]:
        ## The current user is a guest user. Do not allow the submission
        ## to continue - return a 'login' message instead:
        title = _("WebSubmit Authentication Error")
        body = websubmit_templates.tmpl_warning_guest_user_must_login(wso.ln)
        return (title, body)

    ## Perform some initialisation and checking tasks for the submission:
    try:
        initialize_submission_session(wso)
    except InvenioWebSubmitInternalError, err:
        ## An unexpected internal error ocurred making it impossible for this
        ## submission to continue.
        ## Display an error message to the user, log the error and possibly
        ## alert the admin. (FIXME - LOGGING)
        title = _("WebSubmit Internal Error")
        body = str(err)
        return (title, body)
    except InvenioWebSubmitAuthenticationError, err:
        ## It seems that the user tried to manipulate a submission that didn't
        ## belong to them. Halt the submission and display an "access denied"
        ## message. (FIXME - LOGGING)
        title = _("WebSubmit Authentication Error")
        body = str(err)
        return (title, body)
    except InvenioWebSubmitFormArgumentError, err:
        ## The submission form was missing some information (such as the doctype
        ## for the submission or the action). Halt the submission and send the
        ## user to the submission home-page with a message explaining that
        ## there was not enough information for the submission to be processed.
        ## (FIXME - LOGGING)
        title = _("WebSubmit Form Error")
        body = str(err)
        return (title, body)
    else:
        ## Given that we have a document type, intitialize a title string
        ## that contains it, for the submission page:
        title = _("Submit Details for %(x_doctype)s.") \
                % { 'x_doctype' : wso.WebSubmit_document_type }

    ## Get the compents that make up the submission page for the
    ## current submission:
    try:
        ## + form_sections contains the details of the items that appear on
        ##   the submission page itself;
        ## + checks contains the details of the checks that are to be called
        ##   for given input fields;
        ## + wse_objects contains the WSET instances that have been created
        ##   and will be used on the submission form;
        (form_sections, checks, wse_objects) = get_submission_components(wso)
    except InvenioWebSubmitConfigFileError, err:
        ## Oops. There was a problem with the submission's config file.
        ## Return the error message to the user:
        ## (FIXME - LOGGING)
        title = _("WebSubmit Submission Configuration File Error")
        body = str(err)
        return (title, body)
    except InvenioWebSubmitInternalError, err:
        ## There was some kind of unforeseen internal error.
        ## Return the error message to the user:
        ## (FIXME - LOGGING)
        title = _("WebSubmit Internal Error")
        body = str(err)
        return (title, body)

    ## Insert the WSE Objects dictionary into WSO:
    wso.wse_objects = wse_objects

    ## Pass the relevant data and objects to the method responsible for the
    ## creation of the submission form:
    title = _("Submit Metadata")
    body += get_submission_form(wso.WebSubmit_document_type,
                                wso.WebSubmit_action,
                                wso.WebSubmit_Submission_Config,
                                wso.WebSubmit_submissionid,
                                "[+]".join(wso.WebSubmit_category),
                                wso.ln,
                                form_sections,
                                wse_objects)

    ## Serialize the values of all WSE Instances:
    serialize_wse_submitted_values(wso.wse_objects.values())

    ## return the page title and body:
    return (title, body)


def perform_request_process_submitted_form(req, ln=cdslang):
    """Once a user has filled in the "submission form" in order to submit
       some metadata into CDS Invenio via WebSubmit, they click on the
       "finish submission" button and this function is called.
       The function basically has the job of requesting that checks be
       performed on the input-data as necessary (determined by WSCs configured
       at the submission-template level), and then either triggering the
       functions that process the submission-data or re-displaying the
       submission form, depending upon whether or not the data checks were
       successful.
       @param req: (mod_python.Request object) - the Apache request object.
        This req object also contains a member "form", which is a
        mod_python.util.FieldStorage object and contains all of the data
        submitted to the server on the last visit to the page.
       @param ln: (string) - the language of the interface. Defaults to
        cdslang if not provided.
       @return: (string) - the HTML page-body.
    """
    ## Initialize a string in which to hold the page-body:
    body = ""

    ## Using the mod-python request object, create a WebSubmit
    ## Submission Object to store details about the current submission:
    wso = InvenioWebSubmitSubmissionObject(req, ln)

    ## Prepare gettext according to the chosen language:
    _ = gettext_set_language(wso.ln)

    ## Guests are not allowed to use WebSubmit to submit into the
    ## repository. Is this user a guest?
    if wso.user_info["guest"]:
        ## The current user is a guest user. Do not allow the submission
        ## to continue - return a 'login' message instead:
        title = _("WebSubmit Authentication Error")
        body = websubmit_templates.tmpl_warning_guest_user_must_login(wso.ln)
        return (title, body)

    ## Flag to indicate that there was an error during the submission and
    ## the submission process should be halted:
    submission_error = False

    ## Perform some initialisation and checking tasks for the submission:
    try:
        initialize_submission_session(wso)
    except InvenioWebSubmitInternalError, err:
        ## An unexpected internal error ocurred making it impossible for this
        ## submission to continue.
        ## Display an error message to the user, log the error and possibly
        ## alert the admin. (FIXME - LOGGING)
        title = _("WebSubmit Internal Error")
        body = str(err)
        return (title, body)
    except InvenioWebSubmitAuthenticationError, err:
        ## It seems that the user tried to manipulate a submission that didn't
        ## belong to them. Halt the submission and display an "access denied"
        ## message. (FIXME - LOGGING)
        title = _("WebSubmit Authentication Error")
        body = str(err)
        submission_error = True
    except InvenioWebSubmitFormArgumentError, err:
        ## The submission form was missing some information (such as the doctype
        ## for the submission or the action). Halt the submission and send the
        ## user to the submission home-page with a message explaining that
        ## there was not enough information for the submission to be processed.
        ## (FIXME - LOGGING)
        title = _("WebSubmit Form Error")
        body = str(err)
        submission_error = True

    ## If there was an error while initializing this submission session,
    ## return now:
    if submission_error:
        return (title, body)

    ## Get the compents that make up the submission page for the
    ## current submission:
    try:
        ## + form_sections contains the details of the items that appear on
        ##   the submission page itself;
        ## + checks contains the details of the checks that are to be called
        ##   for given input fields;
        ## + wse_objects contains the WSET instances that have been created
        ##   and will be used on the submission form;
        (form_sections, checks, wse_objects) = get_submission_components(wso)
    except InvenioWebSubmitConfigFileError, err:
        ## Oops. There was a problem with the submission's config file.
        ## Return the error message to the user:
        ## (FIXME - LOGGING)
        title = _("WebSubmit Submission Configuration File Error")
        body = str(err)
        submission_error = True
    except InvenioWebSubmitInternalError, err:
        ## There was some kind of unforeseen internal error.
        ## Return the error message to the user:
        ## (FIXME - LOGGING)
        title = _("WebSubmit Internal Error")
        body = str(err)
        submission_error = True

    ## If there was an error while getting this submission's components,
    ## return now:
    if submission_error:
        return (title, body)

    ## Insert the WSE Objects dictionary into WSO:
    wso.wse_objects = wse_objects

    ## Perform the checking with the WSCs:
    (check_failure, error_messages) = \
                   perform_form_input_checking(checks, wse_objects, ln)

    ## Was the check successful?
    if check_failure:
        ## One or more data items failed to validate.
        ## The interface should be redrawn and the error messages as returned
        ## by the checks that failed passed to the page to be displayed:
        title = _("Submit Metadata")
        body += get_submission_form(wso.WebSubmit_document_type,
                                    wso.WebSubmit_action,
                                    wso.WebSubmit_Submission_Config,
                                    wso.WebSubmit_submissionid,
                                    "[+]".join(wso.WebSubmit_category),
                                    wso.ln,
                                    form_sections,
                                    wse_objects,
                                    error_messages)
    else:
        ## The checks all ended without error, meaning that all input data
        ## was correctly validated.
        ## At this point, the submission processing phase can begin.

        ## Create the MARCXML record for this submission in the current
        ## submission's working directory:
        try:
            create_XML_records(wso)
        except InvenioWebSubmitInternalError, err:
            title = _("WebSubmit MARCXML Record Creation Error")
            body = str(err)
        else:
            ## Now execute the WebSubmit functions:
            if True:
                ## Present a page-preview to the user.
                title = _("Submitted Data - A Preview")
                record_preview = \
                        get_record_preview(wso.WebSubmit_submissiondir, wso.ln)
                body = websubmit_templates.tmpl_new_record_preview_page(\
                         wso.WebSubmit_document_type,
                         wso.WebSubmit_action,
                         wso.WebSubmit_Submission_Config,
                         wso.WebSubmit_submissionid,
                         "[+]".join(wso.WebSubmit_category),
                         record_preview,
                         wso.ln)

                ## Serialize the values of all WSE Instances, ready for the
                ## next visit to the page:
                serialize_wse_submitted_values(wso.wse_objects.values())

    ## return the page title and body:
    return (title, body)
































































## Junk:

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
#from invenio.access_control_admin import acc_isRole
from invenio.webpage import page, create_error_box
from invenio.webuser import getUid, isGuestUser, get_email, collect_user_info
from invenio.websubmit_config import *
from invenio.file import *
from invenio.messages import gettext_set_language, wash_language

import invenio.miniparser

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
    if acc_isRole("submit", doctype=doctype, act=act) and auth_code != 0:
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
        function_content = print_function_calls(req=req, doctype=doctype,
                                                action=act,
                                                step=step,
                                                form=form,
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

def print_function_calls (req, doctype, action, step, form, ln=cdslang):
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
                    func_returnval = function(parameters, curdir, form)
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
