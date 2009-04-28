# -*- coding: utf-8 -*-
##
## $Id: WSET_RadioButton.py,v 1.7 2007/08/13 12:31:22 diane Exp $
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

"""This is the definition of the WSET_RadioButton class.
"""

__revision__ = "$Id: WSET_RadioButton.py,v 1.7 2007/08/13 12:31:22 diane Exp $"


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
CFG_WEBSUBMIT_RADIOBUTTON = \
          """<input class="%(class)s" type="radio" name="%(name)s" """ \
          """value="%(value)s" %(checked)s />"""

CFG_WEBSUBMIT_INPUT_STYLECLASS = "websubmit_input"
CFG_WEBSUBMIT_RADIOBUTTON_STYLE_CLASS = "websubmit_radiobutton"


class WSET_RadioButton(WSET_OptionList):
    """This class represents radio buttons in a WebSubmit form.
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
        """Initialise a Radio-button element with some values from the config
           template.
           @param wso: (WebSubmissionObject) - the Web Submission Object,
            containing the various information relating to the current
            submission, the user conducting the submission, etc.
            This object will even contain the details of all values submitted
            from the last reload of the form (and therefore the values for
            this radio-button if there were any).
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
            be displayed by the radio-button when it is drawn on the
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
        ## Call the super-class's init, passing it the wso, the dictionary of
        ## field-labels, the list of option-values.  The super-class will take
        ## care of initialising the options to be displayed for this radio-
        ## button and some other internal variables.
        super(WSET_RadioButton, self).__init__(wso, \
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
        """This method is responsible for reading in the submitted "data value"
           for a given radio-button element and storing it into local member,
           "self.value".
           @return: None.
        """
        if self._wso.submitted_form_fields.has_key(self._name):
            ## One of this radio-button's options was selected when this page
            ## was last submitted. Extract the value and set it into a local
            ## member:
            self.value = self._wso.submitted_form_fields[self._name]


    ## Public interface:
    def get_xml(self):
        """Create the simple XML that represents a radio-button and its
           value.
           If the element has no value, a tag is return with an empty value
           inside.
           <WSE_RadioButton>
            <value>xxx</value>
           </WSE_Radio>
           @return: (string) - XML.
        """
        if self.has_value() is not False:
            ## This element has a value - some XML should be returned/
            xml_string = CFG_WEBSUBMIT_XML_VALUE % \
                          {'id'            : "",
                           'value_content' : encode_for_xml(self.value),
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
           string that will represent a radio-button object in the WebSubmit
           submission page interface.
           @return: (string) - HTML representation of a radio-button.
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

        ## A radio-button may only have one button selected by default.
        ## Therefore, we need a flag to indicate whether or not the
        ## selected value has been printed:
        selected_button_printed = False

        ## Create a list to contain the HTML strings for the radio-button
        ## options:
        radiobuttons_html = []
        ## Loop through all of the "options"
        for idx in xrange(0, len(self._options)):
            ## The label, value and "default-selected" for this button:
            button_label    = self._options[idx][1]
            button_val      = self._options[idx][0]
            button_default_selected = self._options[idx][2]
            button_checked  = False
            ## Should this button be marked as "selected"?
            if self.value is not None:
                ## The user has selected a value for this button. Is this
                ## it? Mark it as checked if so:
                if button_val == self.value:
                    button_checked = True
                    selected_button_printed = True
            elif button_default_selected and not selected_button_printed:
                ## Although this radio-button has no value as selected by
                ## the user, it has a default value, and this option is
                ## it. Mark it as checked.
                button_checked = True
                ## Set the flag stating that the "selected button" has been
                ## printed:
                selected_button_printed = True
            
            ## Build the HTML string for this radio-button option:
            button_html = """<span>"""
            button_html += CFG_WEBSUBMIT_RADIOBUTTON % \
                       { 'class'   : CFG_WEBSUBMIT_RADIOBUTTON_STYLE_CLASS,
                         'name'    : cgi.escape(self._name, 1),
                         'value'   : cgi.escape(button_val, 1),
                         'checked' : (button_checked and "checked") or (""),
                       }
            button_html += \
                        """&nbsp;<span class="websubmit_radioinput_label">""" \
                        """%s</span></span>""" \
                        % cgi.escape(button_label, 1)
            ## Now add the HTML string into the list of radio-buttons HTML:
            radiobuttons_html.append(button_html)

        ## Now start to build the element itself:
        element_html = "<div>"
        ## Based upon the layout, build the buttons vertically,
        ## or horizonatally:
        if self._button_layout == "V":
            ## Create the radio-buttons in a vertical column of buttons:
            for radiobutton in radiobuttons_html:
                element_html += """
     %s<br />""" % radiobutton
        else:
            ## Create the radio-buttons in horizontal rows of radio-buttons,
            ## taking care to line-break when the appropriate number of
            ## buttons per row have been printed:
            buttons_printed_this_line = 0

            for radiobutton in radiobuttons_html:
                ## Add this radio-button into htmlstr
                element_html += """%s&nbsp;&nbsp;""" % radiobutton
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
        
        ## Now, concatenate the error-string and the element html:
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
           supplied a value for a given WSET_RadioButton element during the
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
