# -*- coding: utf-8 -*-
##
## $Id: WSET_CheckBox.py,v 1.7 2007/08/13 12:31:22 diane Exp $
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

"""This is the definition of the WSET_CheckBox class.
"""

__revision__ = "$Id: WSET_CheckBox.py,v 1.7 2007/08/13 12:31:22 diane Exp $"


## Import the WSET (WebSubmit Element Type) base class.
from invenio.websubmit_elements.WSET_OptionList import WSET_OptionList
## Import the WSET (WebSubmit Element Type) config variables needed for get_xml
from invenio.websubmit_elements.WSET import \
     CFG_WEBSUBMIT_XML_VALUE, \
     CFG_WEBSUBMIT_XML_EMPTY_VALUE, \
     CFG_WEBSUBMIT_XML_ELEMENT

from invenio.search_engine import encode_for_xml
import cgi

## Some config variables:
CFG_WEBSUBMIT_CHECKBOX = \
          """<input class="%(class)s" type="checkbox" name="%(name)s" """ \
          """value="%(value)s" %(checked)s />"""

CFG_WEBSUBMIT_INPUT_STYLECLASS = "websubmit_input"
CFG_WEBSUBMIT_CHECKBOX_STYLE_CLASS = "websubmit_checkbox"

CFG_WEBSUBMIT_WSE_ERROR_MSG = """<span>%s</span>"""


class WSET_CheckBox(WSET_OptionList):
    """This class represents a check-box in a WebSubmit form.
    """
    ## Object-inititialiser:
    def __init__(self,
                 wso,
                 elementname,
                 elementlabel,
                 optionvalues,
                 outputheader="",
                 outputfooter="",
                 buttonlayout="V",
                 numbuttonsperline=5,
                 **dummy):
        """Initialise a WSET_CheckBox object.
           @param wso: (WebSubmissionObject) - the Web Submission Object,
            containing the various information relating to the current
            submission, the user conducting the submission, etc.
            This object will even contain the details of all values submitted
            from the last reload of the form (and therefore the values for
            this check-box if there were any).
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
           @param optionvalues: (list) - these are the options that will
            be displayed by the check-box when it is drawn on the
            page. For each "option", there is a VALUE, a LABEL and a flag
            indicating whether or not the option is to be SELECTED by
            default. There may be different labels to choose from - a function
            of the language parameter "lang". Value however is not dependent
            upon language.
            The "optionvalues" list should have the following structure:
              [
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
           @param outputheader: (string) - a string that is to be displayed
            before an element. This can contain HTML markup.
           @param outputfooter: (string) - a string that is to be displayed
            after an element. This can contain HTML markup.
           @param buttonlayout: (character) - a configuration parameter
            indicating the layout that the radio-buttons should take.
            There are 2 options:
             "V" (== vertical - there will be one veritcal "column" of radio-
              buttons);
             "H" (== horizontal - there will be several radio-buttons per line.
              The number of buttons per line is determined by the
              "numbuttonsperline" parameter);
              Any incorrect value that is passed will be converted into "V".
           @param numbuttonsperline: (integer) - If the radio-button layout is
            "rows", this parameter contains the number of buttons to disaplay
            "per row". It defaults to 5.
           @param **dummy: - a dummy variable to catch all "garbage" parameters
            that could be passed to a WSE_Radio's __init__ from the config
            file.
        """
        ## Let the super-class set up the base-information for this object
        ## (including the options to be presented in the list):
        super(WSET_CheckBox, self).__init__(wso, \
                                            elementname, \
                                            elementlabel, \
                                            optionvalues, \
                                            outputheader, \
                                            outputfooter)

        ## Are the buttons to be laid out horizontally or vertically?
        buttonlayout = buttonlayout.upper()
        if buttonlayout not in ("H", "V"):
            ## Invalid value for buttonlayout is replaced with "V":
            buttonlayout = "V"
        self._button_layout = buttonlayout
        
        ## If the buttons are to be laid out horizontally, how many
        ## should be found on a line?
        numbuttonsperline = int(numbuttonsperline)
        if numbuttonsperline < 1:
            ## 0 or negative values are not allowed - set to 5:
            numbuttonsperline = 5
        self._num_buttons_per_line = numbuttonsperline


    ## Private methods:
    def _retrieve_submitted_values(self):
        """This method is responsible for reading in the submitted "data values"
           for a given check-box element and storing them into local member,
           "self.value".
           @return: None.
        """
        if self._wso.submitted_form_fields.has_key(self._name):
            ## One or more of this check-box's options was selected when this
            ## page was last submitted. Extract the value and set it into a
            ## local member:
            self.value = []
            my_value = self._wso.submitted_form_fields[self._name]
            if type(my_value) is list:
                ## Multiple values were submitted and a list has therefore
                ## been received. Assign it to the value member.
                self.value = my_value
            elif isinstance(my_value, str):
                ## Only one value was selected and a string was therefore
                ## received. Add it into a list and assign it to the
                ## value member.
                self.value = [my_value]
            else:
                ## An unexpected type was received - raise a value error
                raise ValueError("Unexpected value type for WSET_CheckBox.")


    ## Public methods:
    def get_xml(self):
        """Create the simple XML that represents checkboxes and its
           value.
           If the element has no value, a tag is return with an empty value
           inside.
           <WSE_CheckBox>
            <value>xxx</value>
           </WSE_CheckBox>
           @return: (string) - XML.
        """
        xml_string = ""
        if self.has_value() is not False:
            for val in self.value:
                xml_string += CFG_WEBSUBMIT_XML_VALUE % \
                              {'id'            : encode_for_xml('id="%s"' % str(self.value.index(val))),
                               'value_content' : encode_for_xml(val),
                               }
        else:
            xml_string = CFG_WEBSUBMIT_XML_EMPTY_VALUE
            
        ## Now add the file-xml into the xml string:
        xmlstr = CFG_WEBSUBMIT_XML_ELEMENT % \
                 { 'name'    : self._name,
                   'content' : xml_string,
                   }

        ## Return the XML for the files:
        return xmlstr
        

    def get_html(self):
        """This method is responsible for creating and returning an HTML
           string that will represent a checkbox object in the WebSubmit
           submission page interface.
           @return: (string) - HTML representation of a checkbox.
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

        ## Create a list to contain the HTML strings for the check-box
        ## options:
        checkboxes_html = []
        ## Loop through all of the "options"
        for idx in xrange(0, len(self._options)):
            ## The label, value and "default-selected" for this button:
            button_label    = self._options[idx][1]
            button_val      = self._options[idx][0]
            button_default_selected = self._options[idx][2]
            button_checked  = False
            ## Should this button be marked as "selected"?
            if self.value is not None:
                ## The user has selected at least one value for this button. Is
                ## this one of them? Mark it as checked if so:
                if button_val in self.value:
                    button_checked = True
            elif button_default_selected:
                ## Although this check-box has no value as selected by
                ## the user, it has default value(s) and this option is
                ## one of them. Mark it as checked.
                button_checked = True

            ## Build the HTML string for this check-box option:
            button_html = """<span>"""
            button_html += CFG_WEBSUBMIT_CHECKBOX % \
                       { 'class'   : CFG_WEBSUBMIT_CHECKBOX_STYLE_CLASS,
                         'name'    : cgi.escape(self._name, 1),
                         'value'   : cgi.escape(button_val, 1),
                         'checked' : (button_checked and "checked") or (""),
                       }
            button_html += \
                     """&nbsp;<span class="websubmit_checkboxinput_label">""" \
                     """%s</span></span>""" \
                     % cgi.escape(button_label, 1)
            ## Now add the HTML string into the list of check-boxes HTML:
            checkboxes_html.append(button_html)

        ## Now start to build the element itself:
        element_html = "<div>"
        ## Based upon the layout, build the buttons vertically,
        ## or horizonatally:
        if self._button_layout == "V":
            ## Create the check-box buttons in a vertical column of buttons:
            for checkbox in checkboxes_html:
                element_html += """
     %s<br />""" % checkbox
        else:
            ## Create the check-boxes in horizontal rows of buttons,
            ## taking care to line-break when the appropriate number of
            ## buttons per row have been printed:
            buttons_printed_this_line = 0

            for checkbox in checkboxes_html:
                ## Add this radio-button into htmlstr
                element_html += """%s&nbsp;&nbsp;""" % checkbox
                ## increment the counter detailing the number of buttons
                ## printed on this line:
                buttons_printed_this_line += 1

                ## Check whether a new line should be started:
                if buttons_printed_this_line == self._num_buttons_per_line:
                    ## The maximum premissable number of buttons has been
                    ## printed on this line. Start a new line.
                    element_html += "<br />"
                    buttons_printed_this_line = 0

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
           supplied a value for a given WSET_CheckBox element during the
           submission.
           It will return a boolean "True" if the element has received some
           kind of value from the submission form, or "False" if not.
           @return: (boolean) - True if the element has a value; False if
            the element has no value;
        """
        hasvalue = True
        if self.value is None:
            ## This element does not have a value
            hasvalue = False

        ## return the flag indicating whether or not the element has a value:
        return hasvalue

