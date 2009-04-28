# -*- coding: utf-8 -*-
##
## $Id: WSET_Author.py,v 1.15 2007/08/17 10:43:43 nich Exp $
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

"""This is the definition of the abstract WSET_Author (WebSubmit Element
   Type) class.
"""

__revision__ = "$Id: WSET_Author.py,v 1.15 2007/08/17 10:43:43 nich Exp $"

## Import useful stuff:
from invenio.search_engine import encode_for_xml
import cgi, re


## Import the WSET (WebSubmit Element Type) base class.
from invenio.websubmit_elements.WSET import WSET, \
     CFG_WEBSUBMIT_XML_COMPOUND_OF_VALUE, \
     CFG_WEBSUBMIT_XML_EMPTY_COMPOUND_OF_VALUE, \
     CFG_WEBSUBMIT_XML_VALUE, \
     CFG_WEBSUBMIT_XML_EMPTY_VALUE, \
     CFG_WEBSUBMIT_XML_ELEMENT


CFG_WSET_AUTHOR_DEFAULT_NUM_AUTHORS_DISPLAYED = 4



CFG_WEBSUBMIT_INPUT_STYLECLASS = "websubmit_input"


CFG_WEBSUBMIT_AUTHOR_TABLE_HEADER = """
 <table>
  <tr>
   <td><span>Surname</span></td>
   <td><span>Forename/Initials</span></td>
   <td><span>Affiliation</span></td>
  </tr>"""


CFG_WEBSUBMIT_AUTHOR_TABLE_FOOTER = """
 </table>"""


CFG_WEBSUBMIT_AUTHOR_TABLE_ROW = """
  <tr>
   <td><input type="text" size="30" name="%(surname)s" value="%(value-surname)s" /></td>
   <td><input type="text" size="15" name="%(forename)s" value="%(value-forename)s" /></td>
   <td><input type="text" size="25" name="%(affiliation)s" value="%(value-affiliation)s" /></td>
  </tr>"""

CFG_WEBSUBMIT_MORE_AUTHORS_BUTTON_ROW = """
  <tr>
   <td colspan="3" style="text-align: right;"> Show&nbsp;
    <input type="text" size="3" name="%(num-authors-name)s" value="%(num-authors-val)s" />
    &nbsp;lines&nbsp;
    <input type="submit" name="%(button-name)s" value="Update" />
   </td>
  </tr>"""

class WSET_Author(WSET):
    """This class represents an "Author(s)" field in a WebSubmit form.
       An author(s) field consists of one or more authors in the form of three
       data-entry fields:
        + Surname;
        + Forename;
        + Affiliation;
       The three fields above relate to a single author, but it is possible to
       to enter information about multiple authors.
    """
    ## Object-inititialiser:
    def __init__(self,
                 wso,
                 elementname,
                 elementlabel,
                 outputheader="",
                 outputfooter="",
                 **dummy):
        """Initialise a WSET_Author object.
           @param wso: (WebSubmissionObject) - the Web Submission Object,
            containing the various information relating to the current
            submission, the user conducting the submission, etc.
            This object will even contain the details of all values submitted
            from the last reload of the form (and therefore the value for
            the authors entered - if there were any).
           @param elementname: (string) - the name of this WebSubmit element.
           @param elementlabel: (dictionary) - If the element is to have a
            label, it will be found in this dictionary. The dictionary should
            contain the label for the element in various different languages.
            The correct label will be chosen based upon the interface language
            (found in the wso), or if a label is not provided in that language,
            the label for cdslang will be used. If a label is not provided in
            that language, the element's label will be left empty.
            The expected structure of elementlabel is:
              { "fr" : "Titre",
                "en" : "Title",
                "de" : "Titel",
              }
           @param outputheader: (string) - a string that is to be displayed
            before an element. This can contain HTML markup.
           @param outputfooter: (string) - a string that is to be displayed
            after an element. This can contain HTML markup.
           @param **dummy: - a dummy variable to catch all "garbage" parameters
            that could be passed to  __init__ from the config file.
        """
        ## Call the super-class's init, passing it the wso, the element's 
        ## name, and the dictionary of element labels:
        super(WSET_Author, self).__init__(wso,
                                          elementname,
                                          elementlabel,
                                          outputheader,
                                          outputfooter)

        ## Set some local fieldname skeletons:
        self._name_surname_field = """%s_surname_""" % self._name
        self._name_forename_field = """%s_forename_""" % self._name
        self._name_affiliation_field = \
                                 """%s_affiliation_""" % self._name

        ## Initialize the value member with the default number of authors to
        ## be displayed in the form and an empty list of author details:
        self.value = {
                       ## The number of author fields to be displayed:
                       'num_author_fields' : \
                         CFG_WSET_AUTHOR_DEFAULT_NUM_AUTHORS_DISPLAYED,
                       ## The details of all authors:
                       'author_details'    : {},
                     }

        ## Retrieve any submitted values:
        self._retrieve_submitted_values()

        ## Retrieve any serialized value for this object:
        serialized_value = self._retrieve_serialized_values()

        ## If this object's value has not been set AND some kind of value was
        ## returned by the previous call to "_retrieve_serialized_values",
        ## assign the de-serialized value to self.value.
        if not self.value["author_details"] and serialized_value is not None:
            ## A value had been serialized into the submission dir. Use it.
            self.value = serialized_value

    ## Private methods:
    def _retrieve_submitted_values(self):
        """This method is responsible for reading in the submitted "data values"
           for a given WSET_Author element and storing them into local member,
           "self.value".
           @return: None.
        """
        ## User wishes to update the number of authors displayed in the
        ## submission form:
        ## First, check that a valid number of authors to display has been
        ## passed:
        if self._wso.submitted_form_fields.has_key(self._name \
                                                   + "_num_authors"):
            num_authors = \
                 self._wso.submitted_form_fields[self._name \
                                                 + "_num_authors"]
        else:
            ## There was no "num_authors" passed - use the default:
            num_authors = CFG_WSET_AUTHOR_DEFAULT_NUM_AUTHORS_DISPLAYED

        ## Now, ensure that "num-authors" is an integer and greater than 0:
        try:
            num_authors = int(num_authors)
        except ValueError:
            ## Oops - not an integer - use default.
            num_authors = CFG_WSET_AUTHOR_DEFAULT_NUM_AUTHORS_DISPLAYED

        if num_authors < 1:
            ## less than 1 author is not allowed!
            num_authors = CFG_WSET_AUTHOR_DEFAULT_NUM_AUTHORS_DISPLAYED

        ## Now, set the internal _num_author_fields member:
        self.value["num_author_fields"] = num_authors

        ## Now, if there are any values for authors, retrieve them:
        ptn_fieldname_surname = re.compile("^%s(?P<authornum>\d+)$" \
                                % self._name_surname_field)
        ptn_fieldname_forename = re.compile("^%s(?P<authornum>\d+)$" \
                                 % self._name_forename_field)
        ptn_fieldname_affiliation = re.compile("^%s(?P<authornum>\d+)$" \
                                    % self._name_affiliation_field)

        ## Get the names of the submitted form fields:
        wse_field_names = self._wso.submitted_form_fields.keys()

        ## Loop through all WSR form fields and search for those that belong
        ## to this WSET_Author element. For each field found (be it an author's
        ## forename, surname, or affiliation), extract the "author number",
        ## create a dictionary for that author and add it into a dictionary
        ## containing the details of all authors, keyed by the author number:
        authors_submitted = {}
        for field in wse_field_names:
            ## Is this a WSET_Author "surname" field for this author object?
            m_fieldname_surname = ptn_fieldname_surname.match(field)
            if m_fieldname_surname is not None:
                ## Yes it is. Get its number, extract the value for this field,
                ## and save it in "authors_submitted" under the "surname"
                ## field for this author-number:
                author_num = int(m_fieldname_surname.group('authornum'))
                ## Have we already seen a field belonging to this author?
                if not authors_submitted.has_key(author_num):
                    ## NO - create a dictionary for this author and insert it
                    ## into the authors_submitted dictionary:
                    authors_submitted[author_num] = \
                                { "surname"     : "",
                                  "forename"    : "",
                                  "affiliation" : "",
                                }

                ## Now assign this surname into the dictionary for this author:
                authors_submitted[author_num]["surname"] = \
                            self._wso.submitted_form_fields[field]
                ## Move on to check the next submitted field:
                continue

            ## Is this a WSET_Author "forename" for this author object?
            m_fieldname_forename = ptn_fieldname_forename.match(field)
            if m_fieldname_forename is not None:
                ## Yes it is. Get its number, extract the value for this field,
                ## and save it in "authors_submitted" under the "forename"
                ## field for this author-number:
                author_num = int(m_fieldname_forename.group('authornum'))
                ## Have we already seen a field belonging to this author?
                if not authors_submitted.has_key(author_num):
                    ## NO - create a dictionary for this author and insert it
                    ## into the authors_submitted dictionary:
                    authors_submitted[author_num] = \
                                { "surname"     : "",
                                  "forename"    : "",
                                  "affiliation" : "",
                                }

                ## Now assign this forename into the dictionary for this author:
                authors_submitted[author_num]["forename"] = \
                            self._wso.submitted_form_fields[field]
                ## Move on to check the next submitted field:
                continue

            ## Is this a WSET_Author "affiliation" for this author object?
            m_fieldname_affiliation = ptn_fieldname_affiliation.match(field)
            if m_fieldname_affiliation is not None:
                ## Yes it is. Get its number, extract the value for this field,
                ## and save it in "authors_submitted" under the "affiliation"
                ## field for this author-number:
                author_num = int(m_fieldname_affiliation.group('authornum'))
                ## Have we already seen a field belonging to this author?
                if not authors_submitted.has_key(author_num):
                    ## NO - create a dictionary for this author and insert it
                    ## into the authors_submitted dictionary:
                    authors_submitted[author_num] = \
                                { "surname"     : "",
                                  "forename"    : "",
                                  "affiliation" : "",
                                }

                ## Now assign this affiliation into the dictionary for this
		## author:
                authors_submitted[author_num]["affiliation"] = \
                            self._wso.submitted_form_fields[field]
                ## Move on to check the next submitted field:
                continue

        ## Given all of the submitted "author values", eliminate the "holes"
        ## (i.e. the author lines with no values):
        treated_author_fields = {}
        next_author_num = 1
        submitted_au_nums = authors_submitted.keys()
        submitted_au_nums.sort()
        for submitted_au_num in submitted_au_nums:
            if not \
               (authors_submitted[submitted_au_num]["surname"].strip() \
                == "" \
               and authors_submitted[submitted_au_num]["forename"].strip() \
                == "" \
               and authors_submitted[submitted_au_num]["affiliation"].strip() \
                == ""):
                ## This author line has a value - add the details into the
                ## treated dictionary of authors - that without blank author
                ## rows:
                treated_author_fields[next_author_num] = \
                                           authors_submitted[submitted_au_num]
                next_author_num += 1

        ## Now, assign the details of the authors to the value member:
        self.value["author_details"] = treated_author_fields


    ## Public Interface:
    def get_html(self):
        """This method is responsible for creating and returning an HTML
           string that will represent a author-fields object in the WebSubmit
           submission page interface.
           @return: (string) - HTML representation of author fields.
        """
        ## Initialise the html string to be returned.
        htmlstr = """
  <div>"""

        ## Add the label into the html string:
        htmlstr += """
  <div>%s</div>
""" \
        % cgi.escape(self._label, 1)

        ## Add the element's "header":
        htmlstr += """<div>%s</div>""" % self._elementheader

        ## Create the HTML for the element itself:
        element_html = "<div>\n"

        ## Open a table to hold the authors:
        element_html += CFG_WEBSUBMIT_AUTHOR_TABLE_HEADER

        ## Display the appropriate number of authors fields:
        for count in xrange(1, self.value["num_author_fields"] + 1):
            element_html += CFG_WEBSUBMIT_AUTHOR_TABLE_ROW % \
              { 'surname'           : \
                      self._name_surname_field + str(count),
                'forename'          : \
                      self._name_forename_field + str(count),
                'affiliation'       : \
                      self._name_affiliation_field + str(count),
                'value-surname'     : \
                      (self.value["author_details"].has_key(count) and \
                       cgi.escape(\
                        self.value["author_details"][count]["surname"], 1)) \
                      or (""),
                'value-forename'    : \
                      (self.value["author_details"].has_key(count) and \
                       cgi.escape(\
                        self.value["author_details"][count]["forename"], 1)) \
                      or (""),
                'value-affiliation' : \
                      (self.value["author_details"].has_key(count) and \
                       cgi.escape(\
                        self.value["author_details"][count]["affiliation"], 1))\
                      or (""),
              }

        ## Add a row enabling the user to alter the number of authors displayed:
        element_html += CFG_WEBSUBMIT_MORE_AUTHORS_BUTTON_ROW \
	   % { 'num-authors-name' : self._name + "_num_authors",
	       'num-authors-val'  : \
                   cgi.escape(str(self.value["num_author_fields"]), 1),
	       'button-name'      : self._name + "_update_authors",
	     }


        ## Close the authors table:
        element_html += CFG_WEBSUBMIT_AUTHOR_TABLE_FOOTER

        ## Close the div for the element itself:
        element_html += "</div>"
        htmlstr += element_html

        ## Add the element's "footer":
        htmlstr += """<div>%s</div>""" % self._elementfooter

        ## Close up the DIV containing this element:
        htmlstr += """
  </div>
"""
        ## return the built HTML string:
        return htmlstr

    def has_value(self):
        """This method is used for the purpose of checking whether the user
           has entered the details of (an) author(s) into a WSET_Author
           element on the submission form.
           It will return a boolean "True" if the element contains the
           details of at least one author, or "False" if not.
           @return: (boolean) - True if an author is present; False if
            not;
        """
        hasvalue = True
        if len(self.value["author_details"].keys()) == 0:
            ## No author details were submitted:
            hasvalue = False

        ## return the flag indicating whether or not the author element
        ## has a value:
        return hasvalue

    def get_xml(self):
        """Return an XML representation of the authors entered into a
           WSET_Author element.  This element should look something like this:

                <wset_element_name>
                  <value id=1>
                    <surname>WXYZ</surname>
                    <forename>A</forename>
                    <affiliation>CERN</affiliation>
                  </value>
                  <value id=2>
                    <surname>LMNO</surname>
                    <forename>B</forename>
                    <affiliation>CERN</affiliation>
                  </value>
                </wset_element_name>

           The XML will later be used to create a 
           @return: (string) of XML.
        """
        ## A string to contain the XML for the authors entered into this
        ## WSET_Author element:
        xmlstr = ""
        ## Get a list of the different authors' ID numbers (the keys for each
        ## of the authors):
        au_numbers = self.value["author_details"].keys()

        if self.has_value() is not False:
            ## Initialise a string containing the XML for all of the authors:
            authors_xml = ""

            ## Transform each of the authors into its XML and add it into the
            ## XML string containing all of the authors:
            au_numbers.sort()
            for au_num in au_numbers:
                author_xml = ""
                for key, val in self.value["author_details"][au_num].items():
                    if val.strip() != "":
                        author_xml += CFG_WEBSUBMIT_XML_COMPOUND_OF_VALUE % \
                                    { 'node_name'  : encode_for_xml(key),
                                      'node_value' : \
                                               encode_for_xml(val.strip())
                                    }
                    else:
                        author_xml += CFG_WEBSUBMIT_XML_EMPTY_COMPOUND_OF_VALUE 
                authors_xml += CFG_WEBSUBMIT_XML_VALUE % \
                   { 'id'            : "id=\"" + \
                                       encode_for_xml(str(au_num)) + \
                                       "\"", \
                     'value_content' : author_xml,
                   }
        else:
            authors_xml = CFG_WEBSUBMIT_XML_EMPTY_VALUE
        ## Now add the author-xml into the xml string:
        xmlstr = CFG_WEBSUBMIT_XML_ELEMENT % \
                     { 'name'    : self._name,
                       'content' : authors_xml,
                     }

        ## Return the XML for the authors:
        return xmlstr
