# -*- coding: utf-8 -*-
##
## $Id: WSET_Date.py,v 1.4 2007/08/17 08:37:17 nich Exp $
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

"""This is the definition of the abstract WSET_Date (WebSubmit Element
   Type) class.
"""

__revision__ = "$Id: WSET_Date.py,v 1.4 2007/08/17 08:37:17 nich Exp $"

## Import useful stuff:
from invenio.search_engine import encode_for_xml, create_inputdate_box
import cgi, re


## Import the WSET (WebSubmit Element Type) base class.
from invenio.websubmit_elements.WSET import WSET, \
     CFG_WEBSUBMIT_XML_ELEMENT, \
     CFG_WEBSUBMIT_XML_VALUE, \
     CFG_WEBSUBMIT_XML_EMPTY_VALUE, \
     CFG_WEBSUBMIT_XML_COMPOUND_OF_VALUE, \
     CFG_WEBSUBMIT_XML_EMPTY_COMPOUND_OF_VALUE


CFG_WEBSUBMIT_INPUT_STYLECLASS = "websubmit_input"

CFG_WEBSUBMIT_DATE_TABLE_ROW = """
  <table>
   <tr>
    <td><select class=%(day)s</td>
    <td><input type="select" size="15" name="%(forename)s" value="%(value-forename)s" /></td>
    <td><input type="text" size="25" name="%(affiliation)s" value="%(value-affiliation)s" /></td>
   </tr>
  </table>"""

class WSET_Date(WSET):
    """This class represents a "Date" field in a WebSubmit form.
       A Date field consists of one date in the form of three
       select-box fields:
        + day;
        + month;
        + year;
    """
    ## Object-inititialiser:
    def __init__(self,
                 wso,
                 elementname,
                 elementlabel,
                 outputheader="",
                 outputfooter="",
                 **dummy):
        """Initialise a WSET_Date object.
           @param wso: (WebSubmissionObject) - the Web Submission Object,
            containing the various information relating to the current
            submission, the user conducting the submission, etc.
            This object will even contain the details of all values submitted
            from the last reload of the form (and therefore the value for
            the values for a date entered - if there were any).
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
        super(WSET_Date, self).__init__(wso,
                                        elementname,
                                        elementlabel,
                                        outputheader, 
                                        outputfooter)
        
        ## Retrieve any submitted values:
        self._retrieve_submitted_values()

        ## Retrieve any serialized value for this object:
        serialized_value = self._retrieve_serialized_values()

        ## If this object's value has not been set AND some kind of value was
        ## returned by the previous call to "_retrieve_serialized_values",
        ## assign the de-serialized value to self.value.
        if "".join([str(val).strip() for val in self.value.values()]) == "" \
                    and serialized_value is not None:
            ## A value had been serialized into the submission dir. Use it.
            self.value = serialized_value

    ## Private methods:
    def _retrieve_submitted_values(self):
        """This method is responsible for reading in the submitted "data values"
           for a given WSET_Date element and storing them into local member,
           "self.value".
           @return: None.
        """
        date_submitted = {"d": "",
                          "m": "",
                          "y": ""}

        for part in date_submitted.keys():
            if self._wso.submitted_form_fields.has_key("%s_%s" % (self._name, part)):
                part_value =  self._wso.submitted_form_fields["%s_%s" % (self._name, part)]
                if isinstance(part_value, str):
                    ## Only one value was selected and a string was therefore
                    ## received.
                    try:
                        date_submitted[part] = int(part_value)
                    except ValueError:
                        pass
                elif type(part_value) is list:
                    ## Multiple values were submitted and a list has therefore
                    ## been received.
                    try:
                        date_submitted[part] = int(part_value[0])
                    except ValueError:
                        pass
                else:
                    ## An unexpected type was received - raise a value error
                    raise ValueError("Unexpected value type for WSET_Date.")
        ## Now, assign the details of the date to the value member:
        self.value = date_submitted


    ## Public Interface:
    def get_html(self):
        """This method is responsible for creating and returning an HTML
           string that will represent a date-fields object in the WebSubmit
           submission page interface.
           @return: (string) - HTML representation of date fields.
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
        element_html += create_inputdate_box(name=self._name + "_", \
                                             selected_year=self.value["y"], \
                                             selected_month=self.value["m"], \
                                             selected_day=self.value["d"], \
                                             ln=self._wso.ln)
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
           supplied a value for a given WSET_Date element during the
           submission.
           It will return a boolean "True" if the element has received some
           kind of value from the submission form, or "False" if not.
           @return: (boolean) - True if the element has a value; False if
            the element has no value;
        """
        hasvalue = True
        if "" in self.value.values():
            ## This element does not have a value for day&month&year
            hasvalue = False

        ## return the flag indicating whether or not the element has a value:
        return hasvalue

    def get_xml(self):
        """Return an XML representation of the date entered into a
           WSET_DATE element.  This element should look something like this:

                <wset_element_name>
                  <value>
                    <day>02</day>
                    <month>12</month>
                    <year>2007</year>
                  </value>
                </wset_element_name>

           The XML will later be used to create a 
           @return: (string) of XML.
        """
        ## A string to contain the XML for the date's values entered into this
        ## WSET_DATE element:
        xmlstr = ""
        ## String containing the XML for date
        date_xml = ""
        if self.has_value() is not False:
            for key, val in self.value.items():
                if val:
                    date_xml += CFG_WEBSUBMIT_XML_COMPOUND_OF_VALUE % \
                                {'node_name' : encode_for_xml(key),
                                 'node_value'     : \
                                 encode_for_xml(str(val))}
                else:
                    date_xml += CFG_WEBSUBMIT_XML_EMPTY_COMPOUND_OF_VALUE % \
                                {'node_name' : encode_for_xml(key)}

            date_xml = CFG_WEBSUBMIT_XML_VALUE % {'value_content':date_xml, \
                                                  'id'           :""}
        else:
            date_xml = CFG_WEBSUBMIT_XML_EMPTY_VALUE
        ## Now add the date-xml into the xml string:
        xmlstr = CFG_WEBSUBMIT_XML_ELEMENT % \
                 { 'name'    : self._name,
                   'content' : date_xml
                   }

        ## Return the XML for the date:
        return xmlstr
