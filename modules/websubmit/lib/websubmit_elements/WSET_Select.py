# -*- coding: utf-8 -*-
##
## $Id: WSET_Select.py,v 1.7 2007/08/13 12:31:22 diane Exp $
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

"""This is the definition of the WSET_Select class.
"""

__revision__ = "$Id: WSET_Select.py,v 1.7 2007/08/13 12:31:22 diane Exp $"


## Import the WSET (WebSubmit Element Type) base class.
from invenio.websubmit_elements.WSET_OptionList import WSET_OptionList
from invenio.search_engine import encode_for_xml
import cgi

## Import the WSET (WebSubmit Element Type) base class.
from invenio.websubmit_elements.WSET import \
     CFG_WEBSUBMIT_XML_ELEMENT, \
     CFG_WEBSUBMIT_XML_VALUE, \
     CFG_WEBSUBMIT_XML_EMPTY_VALUE

CFG_WEBSUBMIT_SELECT_OPTION = \
          """<option value="%(value)s"%(selected)s>%(label)s</option>"""

CFG_WEBSUBMIT_SELECT = \
          """<select class="%(class)s" name="%(name)s"%(multiple)s%(size)s>
%(options)s
</select>"""


CFG_WEBSUBMIT_INPUT_STYLECLASS = "websubmit_input"
CFG_WEBSUBMIT_SELECT_STYLE_CLASS = "websubmit_select"

class WSET_Select(WSET_OptionList):
    """This class represents an HTML Select list in a WebSubmit form.
    """
    ## Object-inititialiser:
    def __init__(self,
                 wso,
                 elementname,
                 elementlabel,
                 optionvalues,
                 outputheader="",
                 outputfooter="",
                 multiple=0,
                 listsize="",
                 **dummy):
        """Initialise a WSET_Select object.
           @param wso: (WebSubmissionObject) - the Web Submission Object,
            containing the various information relating to the current
            submission, the user conducting the submission, etc.
            This object will even contain the details of all values submitted
            from the last reload of the form (and therefore the values for
            this select-list if there were any).
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
            be displayed by the select-list when it is drawn on the
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
           @param multiple (integer) - flag to indicate whether ot not the
            select list is a multiple-select. Defaults to 0, meaning that it
            is not a multiple-select list. Any other value will result in
            a multiple-select list.
           @param listsize: (integer) - this parameter can be used alongside
            the "multiple" parameter to give a multiple select-list a "size".
            The size of a multiple-select list basically means the number of
            options that are shown to the user.
            The parameter defaults to the empty string. In this case, the size
            of the list will be set to 5 (or less, if there are fewer options
            than 5). Otherwise, the list expects an integer representing the
            number of options to show in the list.
            A non-int or a value of less than 1 will result in the default.
           @param **dummy: - a dummy variable to catch all "garbage" parameters
            that could be passed to __init__ from the config file.
        """
        ## Let the super-class set up the base-information for this object
        ## (including the options to be presented in the list):
        super(WSET_Select, self).__init__(wso, \
                                          elementname, \
                                          elementlabel, \
                                          optionvalues, \
                                          outputheader, \
                                          outputfooter)

        ## is this to a be a multiple-select list? Set a flag indicating this:
        try:
            multiple = int(multiple)
        except ValueError:
            ## Non-int value.
            if multiple == "":
                ## No value provided - this is a not a multiple select:
                self._multiple = False
            else:
                ## non-zero value - make this a multiple select:
                self._multiple = True
        else:
            ## If multiple is 0, set the multiple flag to false.
            if multiple == 0:
                ## This is not a multiple-select:
                self._multiple = False
            else:
                ## This is a multiple-select:
                self._multiple = True

        ## Treat "listsize":
        try:
            ## cast it to an integer:
            listsize = int(listsize)
        except ValueError:
            ## Invalid listsize.
            listsize = 0

        if listsize < 1:
            ## if the length of the list is less than 1, we use the default size
            if len(self._options) < 5:
                ## fewer options than 5 - use the number of options:
                self._listsize = len(self._options)
            else:
                ## set the list size to 5:
                self._listsize = 5
        else:
            ## use the size provided by the user:
            self._listsize = listsize
            

    ## Private methods:
    def _retrieve_submitted_values(self):
        """This method is responsible for reading in the submitted "data values"
           for a given select element and storing them into local member,
           "self.value".
           @return: None.
        """
        if self._wso.submitted_form_fields.has_key(self._name):
            ## One or more of this select's options was selected when this page
            ## was last submitted. Extract the value and set it into a local
            ## member:
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
                raise ValueError("Unexpected value type for WSET_Select.")


    ## Public methods:
    def get_xml(self):
        """Return an XML representation of the values entered into a
           WSET_Select element.  This element should look something like this:

                <wset_element_name>
                  <value>xxx</value>
                  <value>yyy</value>
                </wset_element_name>
           The XML will later be used to create a 
           @return: (string) of XML.
        """
        ## A string to contain the XML for the values entered into this
        ## WSET_Select element:
        xmlstr = ""
        if self.has_value() is not False:
            ## Initialise a string containing the XML for all of the values:
            values_xml = ""
            ## Transform each of the values into its XML and add it into the
            ## XML string containing all of the values:
            for value in self.value:
                value_xml = CFG_WEBSUBMIT_XML_VALUE % \
                            {'value_content'     : \
                             encode_for_xml(value.strip()),\
                             'id' : ""
                             }
                values_xml += value_xml
        else:
            values_xml = CFG_WEBSUBMIT_XML_EMPTY_VALUE
        ## Now add the values-xml into the xml string:
        xmlstr = CFG_WEBSUBMIT_XML_ELEMENT % \
                 { 'name'    : self._name,
                   'content' : values_xml,
                }

        ## Return the XML for the values:
        return xmlstr
       
    def get_html(self):
        """This method is responsible for creating and returning an HTML
           string that will represent a select list object in the WebSubmit
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

        ## Create a string to contain the HTML strings for the select list
        ## options:
        options_html = ""

        ## A select list that is not a multiple-select may only have one option
        ## selected at any one time. Therefore, we need a flag to indicate
        ## whether or not the selected value has been printed:
        selected_option_printed = False

        ## Loop through all of the "options"
        for idx in xrange(0, len(self._options)):
            ## The label, value and "default-selected" for this button:
            option_label    = self._options[idx][1]
            option_val      = self._options[idx][0]
            option_default_selected = self._options[idx][2]
            option_selected  = False

            ## Should this option be marked as "selected"?
            if self.value is not None:
                ## The user has selected at least one value from this select
                ## list. Is this it?

                if self._multiple or \
                   (not self._multiple and not selected_option_printed):
                    ## Either this is a multiple select-list (in which case we
                    ## don't care how many options we mark as selected), OR it
                    ## is a multiple select-list, but we haven't yet marked an
                    ## option as selected (in which case it's OK to select this
                    ## option). In any case, if this option's value is in the
                    ## internal list value, this option should be marked as
                    ## selected:
                    if option_val in self.value:
                        ## Mark it as selected:
                        option_selected = True
                        ## Now just update the flag to say that at least one
                        ## option has been marked as selected:
                        selected_option_printed = True
            elif option_default_selected:
                ## This option should be selected by default.
                if self._multiple or \
                   (not self._multiple and not selected_option_printed):
                    ## Either this is a multiple select-list (in which case we
                    ## don't care how many options we mark as selected), OR it
                    ## is a multiple select-list, but we haven't yet marked an
                    ## option as selected (in which case it's OK to select this
                    ## option).
                    ## In any case, mark this option as selected:
                    option_selected = True
                    ## Now just update the flag to say that at least one
                    ## option has been marked as selected:
                    selected_option_printed = True

            ## Build the HTML string for this select-list option:
            options_html += "\n   " + CFG_WEBSUBMIT_SELECT_OPTION \
                            % { "value"    : cgi.escape(option_val, 1),
                                "selected" : (option_selected and " selected") \
                                              or (""),
                                "label"    : cgi.escape(option_label, 1),
                              }
        ## Now start to build the element itself:
        element_html = "<div>\n"

        ## Add the "options" into the select-list definition:
        element_html += CFG_WEBSUBMIT_SELECT \
                        % { 'class'    : CFG_WEBSUBMIT_SELECT_STYLE_CLASS,
                            'name'     : cgi.escape(self._name, 1),
                            'multiple' : (self._multiple and " multiple") \
                                         or (""),
                            'size'     : (self._multiple and \
                                          " size=\"%s\"" % str(self._listsize))\
                                         or (""),
                            'options'  : options_html + "\n",
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
           supplied a value for a given WSET_Select element during the
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
