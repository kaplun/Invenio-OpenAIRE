# -*- coding: utf-8 -*-
##
## $Id: WSET_OptionList.py,v 1.8 2007/08/17 08:38:12 nich Exp $
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

"""This is the definition of the WSET_OptionList class.
   This is an abstract class and should be extended by concrete "option list"
   classes like "radio buttons", "check-buttons", etc.
"""

__revision__ = "$Id: WSET_OptionList.py,v 1.8 2007/08/17 08:38:12 nich Exp $"

## Import useful stuff:
from invenio.config import cdslang

## Import the WSET (WebSubmit Element Type) base class.
from invenio.websubmit_elements.WSET import WSET



class WSET_OptionList(WSET):
    """This ABSTRACT class should be extended by all concrete "option lists".
       Examples of such concrete option-lists are HTML select lists, check-
       boxes and radio-buttons.
       It is not supposed to be instantiated.
    """
    ## Object-inititialiser:
    def __init__(self,
                 wso,
                 elementname,
                 elementlabel,
                 optionvalues,
                 outputheader="",
                 outputfooter=""):
        """Initialise a WSET_OptionList object.
           @param wso: (WebSubmissionObject type) - an object containing
            various information about a submission (such as interface language,
            etc).
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
            be displayed by the option-list element when it is drawn on the
            page. For each "option", there is a VALUE, a LABELand a flag
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
            That is to say, it is a list of dictionaries - whereby each
            dictionary represents one of the options and its label. It is
            expected to have a member called "value" (a string, which is used
            as the value of that option). It is also expected to have a
            member "label", which must be either NoneType (in which case the
            value will be used directly as the label) or a dictionary of
            possible label values, keyed by their language. Finally, it is\
            expected to have a member called "selected" with a value of
            either "YES" or "NO".
           @param outputheader: (string) - a string that is to be displayed
            before an element. This can contain HTML markup.
           @param outputfooter: (string) - a string that is to be displayed
            after an element. This can contain HTML markup.
        """
        ## Call the super-class's init, passing it the wso, the element's
        ## name, the dictionary of element labels, the element's header
        ## and the element's footer:
        super(WSET_OptionList, self).__init__(wso,
                                              elementname,
                                              elementlabel,
                                              outputheader,
                                              outputfooter)

        ## Sanity checking:
        ## Check that optionvalues is of the correct type:
        if type(optionvalues) not in (list, tuple):
            ## invalid "optionvalues" list. Raise a TypeError.
            msg = """Unexpected Type for "optionvalues" - expected list."""
            raise TypeError(msg)

        ## Initialise an empty list of options:
        self._options = []

        ## Call "_retrieve_submitted_values" to get any value that may have
        ## been provided for this option-list by the user on the last visit
        ## to the page:
        ## ATTENTION: OVERRIDE THIS METHOD IN THE SUBCLASS OR THINGS WILL
        ## BREAK!
        self._retrieve_submitted_values()

        ## Retrieve any serialized value for this object:
        serialized_value = self._retrieve_serialized_values()

        ## If this object's value has not been set AND some kind of value was
        ## returned by the previous call to "_retrieve_serialized_values",
        ## assign the de-serialized value to self.value.
        if self.value is None and serialized_value is not None:
            ## A value had been serialized into the submission dir. Use it.
            self.value = serialized_value

        ## Finally, initialise the options for this list:
        self._initialise_options(optionvalues)


    ## Private interface:
    def _initialise_options(self, optionvalues):
        """Given the list of options dictionaries (descibed in the docstring
           for the __init__ method, initialise the self._options member,
           a list of tuples containing the element value, its label, and
           a flag indicating whether or not it should be selected by default:
             [ (val, label, selected), ... ]
           @param optionvalues: (list) - of dictionaries, each of which
            describes an option, its label in various languages, and
            whether it should be marked as selected by default.
           @return: None.
        """
        for option in optionvalues:
            ## get the value of this option:
            try:
                optn_val = option["value"]
            except KeyError:
                ## Invalid option - there is no "value".
                msg = """Unexpected Type for "optionvalues" - options """ \
                      """without values are not allowed."""
                raise TypeError(msg)

            ## Get the label for this option:
            try:
                optn_labels = option["label"]
            except KeyError:
                ## Invalid option. There should be a label. However, since
                ## labels are optional as a value can be used directly as
                ## an option label, this can just be set as an empty
                ## dictionary:
                optn_labels = {}
            else:
                ## If the value of label was not a dictionary, replace it
                ## with an empty dictionary:
                if type(optn_labels) is not dict:
                    optn_labels = {}

            ## Get the "selected" value for this option:
            try:
                optn_selected = option["selected"]
            except KeyError:
                ## No value for "selected". Set it to False.
                optn_selected = False
            else:
                ## If optn_selected contains "YES, set it to True; else,
                ## set it to False.
                if optn_selected.upper() == "YES":
                    optn_selected = True
                else:
                    optn_selected = False


            ## Now set the details for this option into a 3-cell tuple
            ## consisting of the option's value first, then the label,
            ## then the "selected" flag value:
            ## Based on lang, get the correct label:
            if self._wso.ln in optn_labels:
                ## Use the label appropriate to the interface language:
                label = optn_labels[self._wso.ln]
            elif cdslang in optn_labels:
                ## Since there was no label for the interface language,
                ## use the label created for the language specified in
                ## "cdslang":
                label = optn_labels[cdslang]
            elif "default-label" in optn_labels:
                ## Since there was no label for the interface language
                ## and no label for the language specified in cdslang,
                ## use the default-label:
                label = optn_labels["default-label"]
            else:
                ## There was no label for the interface language, no
                ## label for the language specified in cdslang and no
                ## default label. Use the value directly as a label:
                label = optn_val

            ## Now add this option's value and label into the list of
            ## options:
            self._options.append((optn_val, label, optn_selected))

