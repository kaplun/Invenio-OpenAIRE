# -*- coding: utf-8 -*-
##
## $Id: WSET_TextArea.py,v 1.10 2007/08/17 08:42:45 nich Exp $
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

"""This is the definition of the abstract WSET_TextArea (WebSubmit Element
   Type - HTML textarea) class.
"""

__revision__ = "$Id: WSET_TextArea.py,v 1.10 2007/08/17 08:42:45 nich Exp $"

## Import useful stuff:
from invenio.search_engine import encode_for_xml
import cgi


## Import the WSET (WebSubmit Element Type) base class.
from invenio.websubmit_elements.WSET import WSET, \
     CFG_WEBSUBMIT_XML_ELEMENT, \
     CFG_WEBSUBMIT_XML_VALUE, \
     CFG_WEBSUBMIT_XML_EMPTY_VALUE


CFG_WEBSUBMIT_TEXTAREA = \
          """<textarea class="%(class)s" name="%(name)s" """ \
          """rows="%(rows)s" cols="%(cols)s">%(value)s</textarea>"""


CFG_WEBSUBMIT_INPUT_STYLECLASS = "websubmit_input"
CFG_WEBSUBMIT_TEXTAREA_STYLE_CLASS = "websubmit_textarea"

class WSET_TextArea(WSET):
    """This class represents an HTML textarea in a WebSubmit form.
    """
    ## Object-inititialiser:
    def __init__(self,
                 wso,
                 elementname,
                 elementlabel,
                 outputheader="",
                 outputfooter="",
                 rows=10,
                 cols=25,
                 treatlinesasvalues=0,
                 defaultvalue="",
                 **dummy):
        """Initialise a WSET_TextArea object.
           @param wso: (WebSubmissionObject) - the Web Submission Object,
            containing the various information relating to the current
            submission, the user conducting the submission, etc.
            This object will even contain the details of all values submitted
            from the last reload of the form (and therefore the value for
            this textarea - if there was one).
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
           @param rows: (integer) - the number of rows in the textarea.
            This value defaults to 10.
           @param cols: (integer) - the number of columns in the textarea.
            This value defaults to 25.
           @param treatlinesasvalues: (integer) - A flag indicating whether
            or not the WSET_TextArea element should treat each "line" in its
            input as a distinct value. This parameter has no affect on the
            interface, but influences the way that the value(s) are marked
            up in the XML created by the element.
           @param defaultvalue: (string) - Any default value that should
            appear in the textarea when it is first drawn on the submission
            page.
           @param **dummy: - a dummy variable to catch all "garbage" parameters
            that could be passed to  __init__ from the config file.
        """
        ## Call the super-class's init, passing it the wso, the element's 
        ## name, the dictionary of element labels, and the output header and
        ## footer.
        super(WSET_TextArea, self).__init__(wso,
                                            elementname,
                                            elementlabel,
                                            outputheader,
                                            outputfooter)

        ## Sanity checking of default value:
        if type(defaultvalue) not in (str, unicode):
            ## a default value must be a string-type.
            defaultvalue = ""

        ## Treat "rows":
        try:
            ## cast it to an integer:
            rows = int(rows)
        except ValueError:
            ## Invalid value for rows.
            rows = 10

        if rows < 1:
            ## if rows is less than 1, we use the default size
            self._rows = 10
        else:
            ## use the rows provided by the user:
            self._rows = rows

        ## Treat "cols":
        try:
            ## cast it to an integer:
            cols = int(cols)
        except ValueError:
            ## Invalid value for cols.
            cols = 25

        if cols < 1:
            ## if cols is less than 1, we use the default size
            self._cols = 25
        else:
            ## use the rows provided by the user:
            self._cols = cols

        ## The "treatlinesasvalues" parameter indicates whether or not the
        ## data entered into this text area by the user should be treated
        ## as "one value-per-line". If so, it means that the XML created by the
        ## get_xml() method will mark each line up as a distinct "value".
        ## Otherwise, the entire contents of the textarea are treated as a
        ## single value.
        if treatlinesasvalues not in ("", "0", 0):
            ## This is a multi-line element
            self._treat_lines_as_values = True
        else:
            ## Distinction between data "lines" is not made:
            self._treat_lines_as_values = False


        ## Call "_retrieve_submitted_values" to get any value that may have
        ## been provided for this textarea by the user on the last visit
        ## to the page:
        self._retrieve_submitted_values()

        ## Retrieve any serialized value for this object:
        serialized_value = self._retrieve_serialized_values()

        ## If this object's value has not been set AND some kind of value was
        ## returned by the previous call to "_retrieve_serialized_values",
        ## assign the de-serialized value to self.value. Otherwise, adopt the
        ## default value:
        if self.value is None:
            if serialized_value is not None:
                ## A value had been serialized into the submission dir. Use it.
                self.value = serialized_value
            else:
                ## Since there was no value for this object in the form, nor
                ## was there a serialized value for it, use the default value:
                self.value = str(defaultvalue)

    ## Private methods:
    def _retrieve_submitted_values(self):
        """This method is responsible for reading in the submitted "data values"
           for a given select element and storing them into local member,
           "self.value".
           @return: None.
        """
        if self._wso.submitted_form_fields.has_key(self._name):
            ## A value has been provided for this textarea. Extract it and
            ## store it.
            my_value = self._wso.submitted_form_fields[self._name]
            if isinstance(my_value, str):
                ## Only one value was selected and a string was therefore
                ## received. Add it into a list and assign it to the
                ## _value member.
                self.value = my_value
            elif type(my_value) is list:
                ## Multiple values were submitted and a list has therefore
                ## been received. Assign it to the _value member.
                self.value = my_value[0]
            else:
                ## An unexpected type was received - raise a value error
                raise ValueError("Unexpected value type for WSET_TextArea.")


    ## Public Interface:
    def get_html(self):
        """This method is responsible for creating and returning an HTML
           string that will represent a textarea object in the WebSubmit
           submission page interface.
           @return: (string) - HTML representation of a select list.
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

        ## Add the "options" into the select-list definition:
        element_html += CFG_WEBSUBMIT_TEXTAREA \
                        % { 'class'    : CFG_WEBSUBMIT_TEXTAREA_STYLE_CLASS,
                            'name'     : cgi.escape(self._name, 1),
                            'rows'     : cgi.escape(str(self._rows), 1),
                            'cols'     : cgi.escape(str(self._cols), 1),
                            'value'    : cgi.escape(self.value),
                          }


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
           supplied a value for a given WSET_TextArea element during the
           submission. It will return a boolean "True" if the element has
           received some kind of value from the submission form, or "False"
           if not.
           @return: (boolean) - True if the element has a value; False if
            the element has no value;
        """
        hasvalue = True
        if len(self.value.strip()) == 0:
            ## This element does not have a value
            hasvalue = False

        ## return the flag indicating whether or not the element has a value:
        return hasvalue

    def get_xml(self):
        """Return an XML representation of the content of a WSET_TextArea element.
        This element should look something like this:
        if _treat_lines_as_values
                <wset_element_name>
                  <value id=1>xxx</value>
                  <value id=2>yyy</value>
                </wset_element_name>
        else:
                <wset_element_name>
                  <value>xxx yyy</value>
                </wset_element_name>
        The XML will later be used to create a 
        @return: (string) of XML.
        """
        ## A string to contain the XML for the values entered into this
        ## WSET_TextArea element:
        xmlstr = ""
        values = self.value
        ## If the lines must be treated as different values, split
        ## element content with "\n"
        if self._treat_lines_as_values is True:
            values = values.split("\n")
        else:
            values = [values]
        if len(values) > 0 and values!= [""]:
            ## Initialise a string containing the XML for all of the values:
            values_xml = ""
            line_number = 0
            ## Transform each of the values into its XML and add it into the
            ## XML string containing all of the values:
            for value in values:
                value = value.strip()
                if value != "":
                    value_xml = CFG_WEBSUBMIT_XML_VALUE % \
                                { 'id'     : \
                                  encode_for_xml("id=\"%d\"" % line_number),
                                  'value_content'    : \
                                  encode_for_xml(value),
                                 }
                    values_xml += value_xml
                    line_number += 1
        else:
            values_xml = CFG_WEBSUBMIT_XML_EMPTY_VALUE
        ## Now add the values-xml into the xml string:
        xmlstr = CFG_WEBSUBMIT_XML_ELEMENT % \
                 { 'name'    : self._name,
                   'content' : values_xml,
                   }

        ## Return the XML for the values:
        return xmlstr
