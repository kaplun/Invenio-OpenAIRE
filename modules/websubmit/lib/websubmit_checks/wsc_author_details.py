# -*- coding: utf-8 -*-
##
## $Id: wsc_author_details.py,v 1.2 2007/08/17 10:41:04 nich Exp $
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


"""This is the function "wsc_author_details". It is used to check that the
   details of authors as entered into an element of type "WSET_Author"
   meets certain validation constraints.
"""

__revision__ = "$Id: wsc_author_details.py,v 1.2 2007/08/17 10:41:04 nich Exp $"


from invenio.websubmit_elements.WSET_Author import WSET_Author

def wsc_author_details(wset_author_object,
                       forename_mandatory=0,
                       affiliation_mandatory=0):
    """Check the details entered into the author element.
       Check that:
          + The user has not entered an author's forename without the surname;
          + The user has not entered an affiliation without an author;
          + IF affiliation has been flagged as mandatory, the user has entered
            an affiliation for each author;
          + IF author-forenames have been flagged as mandatory, the user has
            entered a forename (or initials) for each author;
       @param wset_authors_object: (WSET_Author object) - this is the author
        details object. It MUST be an object of type
        invenio.websubmit_elements.WSET_Author
       @param forename_mandatory: (integer) - a flag indicating whether or
        not the forename (or initials) is mandatory for an author.
       @param affiliation_mandatory: (integer) - a flag indicating whether
        or not the affiliation is mandatory for an author.
       @return: (integer) - 0 (zero) if no error is found and the test is
        passed; 1 (one) if an error is found and the test fails.
    """
    ## Flag indicating whether an error was found:
    data_error = 0

    ## Sanity checking - ensure we are working with an object of type
    ## WSET_Author
    if not isinstance(wset_author_object, WSET_Author):
        ## Unexpected wset_author_object - raise a TypeError:
        err_msg = "wsc_author_details error: Expected an object of type " \
                  "invenio.websubmit_elements.WSET_Author to work with; " \
                  "Got %s" % str(type(wset_author_object))
        raise TypeError(err_msg)

    ## Wash forename_mandatory:
    try:
        forename_mandatory = int(forename_mandatory)
    except (TypeError, ValueError):
        ## Invalid value for the forename_mandatory flag.
        ## Give it a value of zero:
        forename_mandatory = 0
    ## Give the flag a value of True or False depending upon
    ## its integer value:
    if forename_mandatory == 0:
        forename_mandatory = False
    else:
        forename_mandatory = True

    ## Wash affiliation_mandatory:
    try:
        affiliation_mandatory = int(affiliation_mandatory)
    except (TypeError, ValueError):
        ## Invalid value for the affiliation_mandatory flag.
        ## Give it a value of zero:
        affiliation_mandatory = 0
    ## Give the flag a value of True or false depending upon
    ## its integer value:
    if affiliation_mandatory == 0:
        affiliation_mandatory = False
    else:
        affiliation_mandatory = True

    ## Now test the values held by the author element:
    ## Get the object's "value" (the author-details part of it):
    wset_author_value = wset_author_object.value["author_details"]

    ## Get the author-numbers for the authors:
    author_numbers = wset_author_value.keys()
    author_numbers.sort()

    ## Loop through the author numbers, checking each author's details:
    for author_number in author_numbers:
        ## Get the values for this author:
        au_surname     = wset_author_value[author_number]['surname']
        au_forename    = wset_author_value[author_number]['forename']
        au_affiliation = wset_author_value[author_number]['affiliation']

        ## If this author-number has no surname, ensure that both the
        ## forename and affiliation are blank:
        if au_surname == "" and \
               not (au_forename == "" and au_affiliation == ""):
            ## A forename and/or an affiliation has been given for this
            ## author, but no surname. This is illegal.
            data_error = 1
            break
        elif au_surname != "":
            ## Surname is not blank. Check the forename and affiliation,
            ## based upon whether or not they are required fields:

            ## Check forename:
            if forename_mandatory and au_forename == "":
                ## Forename is mandatory but has not been provided.
                data_error = 1
                break

            ## Check affiliation:
            if affiliation_mandatory and au_affiliation == "":
                ## Affiliation is mandatory but has not been provided.
                data_error = 1
                break

    ## Return the check's return-status code:
    return data_error

