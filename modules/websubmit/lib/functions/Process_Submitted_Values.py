 ## $Id: Process_Submitted_Values.py,v 1.8 2009/11/26 14:22:04 kaplun Exp $

## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008 CERN.
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

"""This is Process_Submitted_Values. Its job is to process the
   values submitted for a tipical document.
   This includes separating author names from affiliations, checking that
   they are valid, etc.
"""

__revision__ = "$Id: $"

from invenio.errorlib import register_exception
from invenio.websubmit_config import InvenioWebSubmitFunctionError, \
                                     InvenioWebSubmitFunctionStop
from invenio.websubmit_functions.Shared_Functions import ParamFromFile
import os, cgi, re, time


CFG_JS_BACK_TO_START = """
<SCRIPT LANGUAGE="JavaScript1.1"  TYPE="text/javascript">
    alert("%(alert-message)s");
    document.forms[0].action="/submit";
    document.forms[0].curpage.value = 1;
    document.forms[0].step.value = 0;
    document.forms[0].submit();
</SCRIPT>
"""

CFG_JS_BACK_TO_STEP_1 = """
<SCRIPT LANGUAGE="JavaScript1.1"  TYPE="text/javascript">
    alert("%(alert-message)s");
    document.forms[0].action="/submit";
    document.forms[0].curpage.value = 1;
    document.forms[0].step.value = 1;
    document.forms[0].submit();
 </SCRIPT>
 """


def split_authors_and_affiliations(curdir,
                                   original_author_file,
                                   separate_author_file,
                                   separate_affiliation_file,
                                   authors_mandatory=False,
                                   affiliations_mandatory=False):
    """Split an author file (that can contain both authors and affiliations)
       into a separate authors and affiliations files.
       It's expected that the format of the author file be as follows:
         Authorname : Affiliation
         Authorname : Affiliation
       A split will be made on the colon. If no affiliation is present, a
       ";" will be used in its place. This will allow bibconvert to handle a
       one to one mapping of author to affiliation without going crazy.
       @param curdir: (string) - the current submission's working directory.
       @param original_author_file: (string) - the name of the original authors/
        affiliations file, as filled by the user in the WebSubmit form. It
        should exist in curdir.
       @param separate_author_file: (string) - the name to be given to the
        file containing the authors after they have been separated from their
        affiliations.
       @param separate_affiliation_file: (string) - the name to be given to
        the file containing the affiliations after they have been separated
        from their authors.
       @param authors_mandatory: (boolean) - a flag to indicate whether authors
        were mandatory for this submission.
       @param affiliations_mandatory: (boolean) - a flag to indicate whether
        author-affiliations were mandatory in this submission.
       @return: (tuple) - taking this form:
          (error_flag, error_msg)
        error_flag is a boolean value.
        If the error_flag is False, the author/affiliations file has not
        passed its tests. If True, the authors/affiliations file was OK.
        Error message is a string containing a message for the user,
        explaining why the authors/affiliations have not been considered to be
        valid.
       @Exceptions raised: InvenioWebSubmitFunctionError - when an unexpected
        error has been encountered, such as the function being unable to
        write a file to curdir.
    """
    ## A message string to be returned to the caller.
    msg = ""
    authors_ok = True

    ## Make sure that we have valid names for the author and affiliation files:
    original_author_file = os.path.basename(original_author_file).strip()
    separate_author_file = os.path.basename(separate_author_file).strip()
    separate_affiliation_file = os.path.basename(separate_affiliation_file)
    if "" in (original_author_file, \
              separate_author_file, \
              separate_affiliation_file):
        err_msg = """Error in split_authors_and_affiliations: """ \
                  """the original_author_file, separate_author_file and """ \
                  """separate_affiliation_file values are madatory, but """ \
                  """either one or all of them were missing. Please """ \
                  """report this problem to the administrator."""
        raise InvenioWebSubmitFunctionError(err_msg)

    ## If the author file doesn't exist, just return quietly because
    ## in any case it's possible that this is a modification submission
    ## in which case there may be no authors:
    if not os.access("%s/%s" % (curdir, original_author_file), os.F_OK):
        return (authors_ok, msg)

    num_valid_authors = 0
    num_valid_affiliations = 0
    separated_authors = []
    separated_affiliations = []
    ## OK, get a list of authors from the author file:
    authors_affiliations = ParamFromFile("%s/%s" % (curdir, \
                                                    original_author_file))
    authors_affiliations_list = authors_affiliations.split('\n')

    for author_and_affiliation in authors_affiliations_list:
        author_and_affiliation = author_and_affiliation.strip()
        if author_and_affiliation == "":
            ## Author line was blank. Skip past it:
            continue
        if author_and_affiliation.find(":") != -1:
            ## The presence of a colon in this author line suggests the
            ## presence of affiliation information. Split the author line
            ## on this colon into "author" and "affiliation" components.
            (author_string, affiliation_string) = \
                            author_and_affiliation.split(":", 1)
            ## Clean whitespace from these values:
            author_string = author_string.strip()
            affiliation_string = affiliation_string.strip()
            ## Now check the values:
            if author_string == "" and affiliation_string != "":
                ## The author is empty, yet has an affiliation. This is
                ## invalid.
                msg = """The format of at least one author was """ \
                      """invalid: although there was an affiliation, """ \
                      """there was no author name. Line: {%s}.""" \
                      % author_and_affiliation.strip()
                authors_ok = False
                break
            elif author_string == "" and affiliation_string == "":
                ## Both the author and the affiliation were empty.
                ## Skip past this line.
                continue
            else:
                ## There must be an author.
                if len(affiliation_string) > 0 and len(affiliation_string) < 2:
                    ## There is an affiliation, but it is only 1 character in
                    ## length. Sounds like nonsense - reject it.
                    msg = """At least one author had an invalid """ \
                          """affiliation: {%s}""" \
                          % author_and_affiliation.strip()
                    authors_ok = False
                    break
                elif len(affiliation_string) == 0:
                    ## This author has no affiliation. Unfortunately though,
                    ## bibconvert will need a 1->1 mapping of authors and
                    ## affiliations, so we will need to make a "fake"
                    ## affiliation which we can tell bibconvert to ignore
                    ## in the templates later. Use ";":
                    separated_authors.append(author_string)
                    separated_affiliations.append(";")
                    num_valid_authors += 1
                else:
                    ## Both the author and the affiliation appear to be valid.
                    ## Keep them both:
                    separated_authors.append(author_string)
                    separated_affiliations.append(affiliation_string)
                    num_valid_authors += 1
                    num_valid_affiliations += 1
        else:
            ## There was no ":" present in the line.
            ## This effectively means that there was no affiliation and the
            ## line should be taken entirely as an "author".
            separated_authors.append(author_and_affiliation)
            separated_affiliations.append(";")
            num_valid_authors += 1
    ## All authors and affiliations have been separated into lists.
    ## Check for problems:
    if not authors_ok:
        if authors_mandatory and num_valid_authors == 0:
            ## Oh dear, the author field is mandatory, but NO valid authors were
            ## encountered.
            msg = """Author is mandatory, but NO valid authors were found. """ \
                  """Please correct this problem."""
            authors_ok = False
        elif affiliations_mandatory and num_valid_authors \
                                        != num_valid_affiliations:
            ## Oh dear, the affiliation field is mandatory, but we don't have
            ## the same number of affiliations as we do authors.
            msg = """Author-affiliation is mandatory, but the number of """ \
                  """valid authors found did not match the number of """ \
                  """affiliations found. Please correct this problem."""
            authors_ok = False

    ## If there were no problems, write out the "authors" and "affiliations"
    ## files:
    if authors_ok:
        ## Open files in which to write the new authors and affiliations:
        try:
            ## Open the new authors file for writing:
            fh_separate_author_file = open("%s/%s" \
                                           % (curdir, \
                                              separate_author_file), "w")
            for author in separated_authors:
                fh_separate_author_file.write("%s\n" % author)
                fh_separate_author_file.flush()
            fh_separate_author_file.close()
        except IOError:
            ## Unable to open the new author file:
            err_msg = """Error in split_authors_and_affiliations: Unable """ \
                      """to write to the new authors file [%s]. Please """ \
                      """report this problem to the administrator.""" \
                      % separate_author_file
            register_exception(prefix=err_msg)
            raise InvenioWebSubmitFunctionError(err_msg)
        ##
        try:
            ## Open the new affiliations file for writing:
            fh_separate_affiliation_file = open("%s/%s" \
                                                % (curdir, \
                                                   separate_affiliation_file), \
                                                "w")
            for affiliation in separated_affiliations:
                fh_separate_affiliation_file.write("%s\n" % affiliation)
                fh_separate_affiliation_file.flush()
            fh_separate_affiliation_file.close()
        except IOError:
            ## Unable to open the new affiliation file:
            err_msg = """Error in split_authors_and_affiliations: Unable """ \
                      """to write to the new affiliations file [%s]. """ \
                      """Please report this problem to the administrator.""" \
                      % separate_affiliation_file
            register_exception(prefix=err_msg)
            raise InvenioWebSubmitFunctionError(err_msg)
    ##
    ## Finally, return the error status flag and the message as a tuple:
    return (authors_ok, msg)


def check_authors(curdir, author_file):
    """Given an author file, test it to ensure that each author name fits
       a valid format.  That format is:
         Surname, Forename/Initial(s)
       For example:
         Bloggs, J
       @param curdir: (string) - the current submission's working directory.
        The author_file should exist in here.
       @param author_file: (string) - the name of the author file to be
        checked.
       @return: (tuple) - taking this form:
          (error_flag, error_msg)
        error_flag is a boolean value.
        If the error_flag is False, the author file has not passed its
        tests. If True, the author file is OK.
        Error message is a string containing a message for the user,
        explaining why the author names have not been considered to be
        valid.
    """
    ## A message string to be returned to the caller.
    msg = ""
    ## A flag to indicate whether the author names are deemed valid:
    authors_ok = True
    ## If the author file doesn't exist, just return quietly because
    ## in any case it's possible that this is a modification submission
    ## in which case there may be no authors:
    if not os.access("%s/%s" % (curdir, author_file), os.F_OK):
        return (authors_ok, msg)

    ## OK, get a list of authors from the author file:
    authors = ParamFromFile("%s/%s" % (curdir, author_file))
    author_list = authors.split('\n')
    ## A counter to indicate the number of good author names found:
    num_good_authors = 0

    ## OK - check each author:
    for current_author in author_list:
        ## Keep the original value for this author for use when reporting
        ## a problem with it:
        rawval_current_author = current_author.rstrip()
        ## Get a working author value:
        workingval_current_author = current_author.strip()
        if workingval_current_author in ('', None):
            ## If this author value is empty, pass by:
            continue
        else:
            ## Test for the number of commas in this author's name.
            ## The valid format for an author's name is:
            ##      "Surname, Forename/Initials". E.g.: Osborne, T
            ## Therefore, if there is not exactly 1 comma in the string,
            ## something is wrong.
            split_authorname = workingval_current_author.split(",")
            if len(split_authorname) == 2:
                ## Splitting the author's name on a comma resulted in only two
                ## components. The first can be considered as the surname, the
                ## second as the name/initials.
                ## Test them to ensure that they actually HAVE values and aren't
                ## just empty strings or whitespace:
                ## Rule: The author's surname should be at least two characters
                ## long and the forename/initials at least 1:
                if len(split_authorname[0].strip()) < 2 \
                   or len(split_authorname[1].strip()) < 1:
                    ## Surname and/or forename invalid.
                    ## Flag the error and break from this loop:
                    authors_ok = False
                    break
                elif split_authorname[1].find(".") != -1:
                    ## A period has been found in the author's
                    ## firstname/initials. Example, Robinson, N.A.
                    ## This isn't allowed so flag the error and break from this
                    ## loop:
                    authors_ok = False
                    break
                else:
                    ## This author line was good. Increment the counter for
                    ## the number of good author names found:
                    num_good_authors += 1
            else:
                ## Either (a) more than two commas were found (perhaps there
                ## were several authors in the line?) or (b) no commas were
                ## found. Either way, this is invalid for an author.
                authors_ok = False
                break

    ## If everything was not OK, set an appropriate error message:
    if not authors_ok:
        ## Oh dear. At least one author failed the test. Set the message string
        ## to indicate this:
        msg = """The format of at least one author name was not valid: """ \
              """[%s]. Author names must be written in the format """ \
              """Lastname, Initials (or firstname). There must only be """ \
              """ONE author name per line. Use 1 space after the comma. """ \
              """DO NOT use periods (.) in the initials/firstname.""" \
              % rawval_current_author
    elif num_good_authors == 0:
        ## No good author lines were found.
        msg = """NO valid author names were found. The author field is """ \
              """mandatory so at least one must be present. Author names """ \
              """must be written in the format Lastname, Initials (or """ \
              """firstname). There must only be ONE author name per line. """ \
              """Use 1 space after the comma. DO NOT use periods (.) in """ \
              """the initials/firstname."""
        authors_ok = False

    ## Return the error condition flag and the error message:
    return (authors_ok, msg)


def date_is_valid(date_string, date_format='%d/%m/%Y'):
    """Check that a date is valid in the format dd/mm/yyyy.
       @param date_string: (string) - the date to be checked.
       @return: (boolean) - True if the date is valid; False if the date is
        not valid.
    """
    date_valid = True
    ## Check the date:
    try:
        time.strptime(date_string, date_format)
    except ValueError:
        ## Date was invalid:
        date_valid = False
    return date_valid

def cleanup_websubmit_filedir(curdir, file_element_dirname):
    """WebSubmit presents users with "file" elements on the submission form.
       These file elements each have a name, e.g. FILE.
       The way that WebSubmit handles uploaded files is as follows:
       There is a common folder called "files" under which all files.
       The name of any "file" element on the submission interface is used to
       create a directory, under which the actual files, as uploaded via that
       element, are stored.
       For example, if the submission interface has a file element "FILE",
       and a file "paper.pdf" is uploaded via it, the directory structure will
       be as follows:
             <curdir>/
                |
                ----> files/
                        |
                        ----> FILE/
                                  |
                                  ----> paper.pdf
       The purpose of this function is to take the name of one file element,
       and to clean it up, unlinking any files within it before unlinking the
       directory itself.
       Assumption: There will only ever be NORMAL FILES in the file element's
       directory - never directories, etc. This is because WebSubmit should
       be responisble for creating everything under that directory and should
       only allow files to be uploaded there.
       @param curdir: (string) - the current submission's working directory.
       @param file_element_dirname: (string) - the name of the file element
        directory to be cleaned up.
       @Exceptions raised: An OSError may occur if files cannot be removed
        for some reason. This function however will not attempt to catch it,
        instead preferring to propagate it up to the caller.
    """
    if os.path.exists("%s/files/%s" % (curdir, file_element_dirname)):
        ## The "file element" exists. Go ahead and try to clean it:
        files_in_element_dir = os.listdir("%s/files/%s" \
                                          % (curdir, file_element_dirname))
        for filename in files_in_element_dir:
            ## Remove the file:
            os.unlink("%s/files/%s/%s" % (curdir, \
                                          file_element_dirname, \
                                          filename))
        ## Now remove the file element directory itself:
        os.rmdir("%s/files/%s" % (curdir, file_element_dirname))


def cleanup_submission_files(curdir, data_files=None, fulltext_files=None):
    """The purpose of this function is to clean away any unwanted files from
       a submission's working directory.
       The function can clean away two types of file:
         + simple data files found directly in curdir. These would normally
           be things like straight forward "value files" like form fields or
           more likely, values generated by WebSubmit functions.
         + "fulltext files" - i.e. files uploaded by the user and thus stored
           in curdir/files/FILE_FIELDNAME
       The names of the "unwanted" files are passed to this function as
       arguments.
       @param curdir: (string) - the current submission's working directory.
       @param data_files: (list) - containing the names of the "unwanted" data
        files (as strings) that are to be unlinked.
       @param fulltext_files: (list) - containing the names of the "unwanted"
        fulltext file field elements from the form.
       @return: None
       @Exceptions raised: InvenioWebSubmitFunctionError - when the function
        fails to carry out its work.
    """
    ## Sanity checking - ensure that we're working with valid list arguments:
    if data_files is None:
        data_files = []
    elif type(data_files) is str:
        data_files = [data_files]
    if fulltext_files is None:
        fulltext_files = []
    elif type(fulltext_files) is str:
        fulltext_files = [fulltext_files]

    ## First, clean-up the unwanted "full-text" files:
    for fulltext_filename in fulltext_files:
        ## Ensure that we're working with a basename:
        fulltext_filename = os.path.basename(fulltext_filename).strip()
        try:
            cleanup_websubmit_filedir(curdir, fulltext_filename)
        except OSError:
            ## An error was encountered when attempting to clean up the full-
            ## text files directory. Cannot continue.
            err_msg = "When cleaning up unwanted files in the submission's " \
                      "working directory, an error was encountered when " \
                      "trying to clean up the full-text files directory. " \
                      "Please report this problem to the administrator."
            register_exception(prefix=err_msg)
            raise InvenioWebSubmitFunctionError(err_msg)
    ## Now cleanup the "unwanted" data files:
    for data_filename in data_files:
        ## Ensure that we're working with a basename:
        data_filename = os.path.basename(data_filename).strip()
        ## If it exists, unlink the file:
        if os.path.exists("%s/%s" % (curdir, data_filename)):
            try:
                os.unlink("%s/%s" % (curdir, data_filename))
            except OSError:
                ## Unable to unlink the separate author file.
                err_msg = "When cleaning up unwanted files in the " \
                          "submission's working directory, an unexpected " \
                          "error was encountered when trying to unlink " \
                          "the data file [%s]. Please report this problem " \
                          "to the administrator." % data_filename
                register_exception(prefix=err_msg)
                raise InvenioWebSubmitFunctionError(err_msg)




def Process_Submitted_Values(parameters, \
                                       curdir, \
                                       form, \
                                       user_info=None):
    """This is Process_submitted_Values. Its job is to process the
       values submitted for an EuCARD document.
       Tasks handled:
        * Split authors and affiliations, checking them. (Author names must
          be in the format "Name, Initials/forename", affiliations must be
          separated from authors with ":", etc.
       @param: parameters: (dictionary) - the parameters to be passed to the
        function by WebSubmit. This function expects the following keys:
          * orig_aufile --> (string) the name of the original author file -
                             i.e. that in the EuCARD form.
          * separate_aufile --> (string) the name of the separate file
                                 containing the authors that is to be created.
          * separate_affile --> (string) the name of the separate file
                                 containing the affiliations that is to be
                                 created.
          * fulltext_file   --> (string) the name of the "file" element in
                                 the submission form that enables a user to
                                 upload a full-text file.
       @param curdir: (string) - the current submission's working directory.
       @param form: (dictionary) - the fields in the WebSubmit form.
       @param user_info: (dictionary) - information about the submitter.
    """
    ## Get the names of the original author/affiliation file, the separated
    ## authors file, and the separated affiliations file from the list of
    ## parameters:
    try:
        ## Authors/Affiliations files:
        author_affiliation_file   = parameters["orig_aufile"]
        separate_author_file      = parameters["separate_aufile"]
        separate_affiliation_file = parameters["separate_affile"]
        ## Main File name:
        file_element_dirname      = parameters["fulltext_file"]
    except KeyError:
        ## One of the author/affiliation file parameters was not supplied to
        ## the function by WebSubmit. This is a configuration error - the
        ## parameter has probably not been declared in the DB for this
        ## function.
        msg = """Error in Process_submitted_Values: The """ \
              """function was not configured correctly - it was not """ \
              """called with the correct arguments. """ \
              """Please report this problem to the administrator."""
        register_exception(prefix=msg)
        raise InvenioWebSubmitFunctionError(msg)
    else:
        author_affiliation_file = \
             os.path.basename(author_affiliation_file).strip()
        separate_author_file = \
             os.path.basename(separate_author_file).strip()
        separate_affiliation_file = \
             os.path.basename(separate_affiliation_file).strip()
        if "" in (author_affiliation_file, \
                  separate_author_file, \
                  separate_affiliation_file, \
                  file_element_dirname):
            ## Oops. These arguments were mandatory and at least one of them
            ## was empty.
            msg = """Error in Process_submitted_Values: The """ \
                  """function was not configured correctly - it was not """ \
                  """called with the correct arguments. """ \
                  """Please report this problem to the administrator."""
            raise InvenioWebSubmitFunctionError(msg)

    ## Now get the "action" of this submission:
    action = ParamFromFile("%s/act" % curdir)
    if action.upper() not in ('SBI', 'MBI'):
        ## This function should not be called with any actions other than
        ## SBI or MBI:
        msg = """Error in Process_submitted_Values: This """ \
              """function is designed for use only with the submission """ \
              """of new bibliographic information (the SBI action) or the """ \
              """modification of existing records (the MBI action). """ \
              """Please report this problem to the administrator."""
        raise InvenioWebSubmitFunctionError(msg)

    ## Split the authors and affiliations into two files:
    (authors_and_affiliations_valid, \
     authors_error_msg) = \
            split_authors_and_affiliations(curdir,
                                           author_affiliation_file,
                                           separate_author_file,
                                           separate_affiliation_file,
                                           True,
                                           True)
    if not authors_and_affiliations_valid:
        ## There was a problem with the authors/affiliations. The user should
        ## be redirected to the form once more so that the mistake can be
        ## corrected:
        ##
        cleanup_submission_files(curdir, fulltext_files=file_element_dirname)
        if action == 'MBI':
            ## If this is a modification, return to the page containing the
            ## fields to be modified:
            raise InvenioWebSubmitFunctionStop(CFG_JS_BACK_TO_STEP_1 \
                         % { 'alert-message' : \
                              cgi.escape(authors_error_msg, \
                                         1).replace('\n', '\\\\n'),
                           } )
        else:
            ## If this is a new submission, return to the page containing the
            ## fields:
            raise InvenioWebSubmitFunctionStop(CFG_JS_BACK_TO_START \
                         % { 'alert-message' : \
                              cgi.escape(authors_error_msg, \
                                         1).replace('\n', '\\\\n'),
                           } )
    ##
    ## Validate the authors:
    (authors_valid, authors_error_msg) = \
                                 check_authors(curdir, separate_author_file)
    if not authors_valid:
        ## At least one author name was invalid. The user should
        ## be redirected to the form once more so that the mistake can be
        ## corrected:
        data_files_to_clean = [separate_author_file, separate_affiliation_file]
        cleanup_submission_files(curdir, \
                                 data_files=data_files_to_clean, \
                                 fulltext_files=file_element_dirname)
        if action == 'MBI':
            ## If this is a modification, return to the page containing the
            ## fields to be modified:
            raise InvenioWebSubmitFunctionStop(CFG_JS_BACK_TO_STEP_1 \
                         % { 'alert-message' : \
                              cgi.escape(authors_error_msg, \
                                         1).replace('\n', '\\\\n'),
                           } )
        else:
            ## If this is a new submission, return to the page containing the
            ## fields:
            raise InvenioWebSubmitFunctionStop(CFG_JS_BACK_TO_START \
                         % { 'alert-message' : \
                              cgi.escape(authors_error_msg, \
                                         1).replace('\n', '\\\\n'),
                           } )


    ## End of checking.
    return ""
