# -*- coding: utf-8 -*-
##
## $Id: WSET_Text.py,v 1.9 2007/08/17 08:43:07 nich Exp $
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

"""This is the definition of the abstract WSET_Text (WebSubmit Element
   Type - HTML text input) class.
"""

__revision__ = "$Id: WSET_Text.py,v 1.9 2007/08/17 08:43:07 nich Exp $"

## Import useful stuff:
from invenio.search_engine import encode_for_xml
import cgi


## Import the WSET (WebSubmit Element Type) base class.
from invenio.websubmit_elements.WSET import WSET, \
     CFG_WEBSUBMIT_XML_ELEMENT, \
     CFG_WEBSUBMIT_XML_VALUE, \
     CFG_WEBSUBMIT_XML_EMPTY_VALUE


CFG_WEBSUBMIT_TEXT = \
          """<input type="text" class="%(class)s" name="%(name)s" """ \
          """size="%(size)s" value="%(value)s"%(maxlength)s />"""


CFG_WEBSUBMIT_INPUT_STYLECLASS = "websubmit_input"
CFG_WEBSUBMIT_TEXT_STYLE_CLASS = "websubmit_textinput"

## Default "size" of a WSET_Text input:
CFG_DEFAULT_WSET_TEXT_SIZE = 15

class WSET_Text(WSET):
    """This class represents an HTML text (input) in a WebSubmit form.
    """
    ## Object-inititialiser:
    def __init__(self,
                 wso,
                 elementname,
                 elementlabel,
                 outputheader="",
                 outputfooter="",
                 size=CFG_DEFAULT_WSET_TEXT_SIZE,
                 maxlength=None,
                 defaultvalue="",
                 **dummy):
        """Initialise a WSET_Text object.
           @param wso: (WebSubmissionObject) - the Web Submission Object,
            containing the various information relating to the current
            submission, the user conducting the submission, etc.
            This object will even contain the details of all values submitted
            from the last reload of the form (and therefore the value for
            this text input - if there was one).
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
           @param size: (integer) - the size (i.e. length) of the text input
            field.
           @param maxlength: (integer) - the maximum length of input permitted
            in the text input field.
           @param defaultvalue: (string) - Any default value that should
            appear in the text input when it is first drawn on the submission
            page.
           @param **dummy: - a dummy variable to catch all "garbage" parameters
            that could be passed to  __init__ from the config file.
        """
        ## Call the super-class's init, passing it the wso, the element's
        ## name, the dictionary of element labels, and any header/footer
        ## that should be displayed in the interface, alongside the element:
        super(WSET_Text, self).__init__(wso,
                                        elementname,
                                        elementlabel,
                                        outputheader,
                                        outputfooter)

        ## Handle maxlength argument:
        try:
            maxlength = int(maxlength)
        except (TypeError, ValueError):
            ## Non-integer supplied for maxlength - ignore it:
            maxlength = None
        else:
            ## Check to ensure that maxlength >= 0. If not, don't use it.
            if maxlength < 0:
                maxlength = None

        ## Now store maxlength as a member:
        self._maxlength = str(maxlength)

        ## Handle size argument:
        try:
            size = int(size)
        except (TypeError, ValueError):
            ## Non-integer supplied for size - set it to the default:
            size = str(CFG_DEFAULT_WSET_TEXT_SIZE)
        else:
            ## Check to ensure that size > 0. If not, use the default size:
            if size < 1:
                size = str(CFG_DEFAULT_WSET_TEXT_SIZE)

        ## Now store size as a member:
        self._size = str(size)

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
                ## value member.
                self.value = my_value
            elif type(my_value) is list:
                ## Multiple values were submitted and a list has therefore
                ## been received. Assign it to the value member.
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
        element_html += CFG_WEBSUBMIT_TEXT \
                        % { 'class'     : CFG_WEBSUBMIT_TEXT_STYLE_CLASS,
                            'name'      : cgi.escape(self._name, 1),
                            'size'      : cgi.escape(self._size, 1),
                            'maxlength' : (self._maxlength is not None and \
                                           " maxlength=\"" \
                                           + cgi.escape(self._maxlength, 1) \
                                           + "\"") or (""),
                            'value'     : cgi.escape(str(self.value), 1),
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
           supplied a value for a given WSET_Text element during the submission.
           It will return a boolean "True" if the element has received some
           kind of value from the submission form, or "False" if not.
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
        """Return an XML representation of the content of a WSET_Text element.
        This element should look something like this:
                <wset_element_name>
                  <value>xxx</value>
                </wset_element_name>
        The XML will later be used to create a 
        @return: (string) of XML.
        """
        ## A string to contain the XML for the values entered into this
        ## WSET_Text element:
        xmlstr = ""
        value = self.value.strip()
        if self.has_value() is not False:
            value_xml = CFG_WEBSUBMIT_XML_VALUE % \
                        { 'value_content' : encode_for_xml(value),\
                          'id'            : ""    
                        }
        else:
            value_xml = CFG_WEBSUBMIT_XML_EMPTY_VALUE
        ## Now add the values-xml into the xml string:
        xmlstr = CFG_WEBSUBMIT_XML_ELEMENT % \
                 { 'name'    : self._name,
                   'content' : value_xml,
                 }

        ## Return the XML for the values:
        return xmlstr
