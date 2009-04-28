# -*- coding: utf-8 -*-
##
## $Id: WSET.py,v 1.9 2007/08/17 08:35:45 nich Exp $
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

"""This is the definition of the abstract WSET (WebSubmit Element Type) class.
   This class should be extended by all WSET_* element classes.
"""

__revision__ = "$Id: WSET.py,v 1.9 2007/08/17 08:35:45 nich Exp $"

## Import useful stuff:
from invenio.config import cdslang

from cPickle import load, dump, UnpicklingError, PicklingError
import os

## Config variables for get_xml function
CFG_WEBSUBMIT_XML_ELEMENT = """<%(name)s>%(content)s</%(name)s>"""

CFG_WEBSUBMIT_XML_VALUE = """<value %(id)s>%(value_content)s</value>"""

CFG_WEBSUBMIT_XML_EMPTY_VALUE = """<value/>"""

CFG_WEBSUBMIT_XML_COMPOUND_OF_VALUE = """<%(node_name)s>%(node_value)s</%(node_name)s>"""

CFG_WEBSUBMIT_XML_EMPTY_COMPOUND_OF_VALUE = """<%(node_name)s/>"""

## --
## A function to raise a "NotImplementedError" when abstract methods are
## called.

def abstract_method_call():
    """When called, this function raises a "NotImplementedError" with a
       message string that the "caller" method must be implemented by
       subclasses.
       Based on an example at <http://norvig.com/python-iaq.html>.
    """
    ## Library to retrieve information about stack frames:
    import inspect
    ## Get references to the caller stack frames:
    currentframe = inspect.currentframe()
    outerframes = inspect.getouterframes(currentframe)
    ## Get the name of the method that called this function from the frames:
    caller = outerframes[1][3]
    ## Delete the references to the frames:
    del currentframe
    del outerframes
    ## Raise the exception:
    raise NotImplementedError("The " + caller + " method must be implemented " \
                              "by subclasses.")

## --
## The Abstract WSET class.

class WSET(object):
    """This ABSTRACT class represents an interface that should be implemented
       by all WSET_* classes.
       It is not supposed to be instantiated, but all WSET_* classes should
       extend it and implement ALL of its abstract methods.
    """

    def __init__(self,
                 wso,
                 elementname,
                 elementlabel,
                 outputheader="",
                 outputfooter=""):
        """Initialise a WSET object.
           @param wso: (WebSubmissionObject) - an object containing
            various information about a submission (such as interface language,
            etc).
           @param elementname: (string) - the name of this WebSubmit element.
            This value is important, as it will be used for naming the element
            in its XML, etc.
            It is a requirement that the name of a WSET element begin with
            "WSE_". E.g.: "WSE_publisher". Failure to name WSETs according to
            this convention will result in a "ValueError" being raised.
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
        """
        ## Sanity checking for elementname:
        if type(elementname) not in (str, unicode):
            ## Illegal type for element name. Must be a string.
            msg = """A WSET element's name (elementname) must be a string """ \
                  """with a length of at least 1."""
            raise TypeError(msg)
        elif len(elementname.strip()) < 1:
            ## Illegal element name. Raise Value Error.
            msg = """A WSET element's name (elementname) must be a string """ \
                  """with a length of at least 1."""
            raise ValueError(msg)
        elif not elementname.startswith("WSE_"):
            ## It is a requirement that a WSET element's name begin with
            ## "WSE_" (e.g. "WSE_publisher"):
            msg = """A WSET element's name (elementname) must be a string """ \
                  """beginning with "WSE_". E.g.: "WSE_publisher"."""
            raise ValueError(msg)

        ## Store "elementname" locally:
        self._name = elementname

        ## Store the element's header locally:
        if type(outputheader) not in (str, unicode):
            ## Illegal element "header"
            msg = """The header supplied for a WSET must be a string."""
            raise TypeError(msg)
        self._elementheader = outputheader

        ## Store the element's footer locally:
        if type(outputfooter) not in (str, unicode):
            ## Illegal element "footer"
            msg = """The footer supplied for a WSET must be a string."""
            raise TypeError(msg)
        self._elementfooter = outputfooter

        ## reset the internal error flag:
        self.error = False

        ## Store the wso as a local member:
        self._wso = wso

        ## Using self._wso.ln, try to get the correct label for this element:
        if self._wso.ln in elementlabel:
            ## Use the label appropriate to the interface language:
            label = elementlabel[self._wso.ln]
        elif cdslang in elementlabel:
            ## Since there was no label for the interface language,
            ## use the label created for the language specified in
            ## "cdslang":
            label = elementlabel[cdslang]
        else:
            ## There was no label for the interface language and no
            ## label for the language specified in cdslang.
            ## If there are any labels for this element at all, use the first
            ## one that we find - no matter which language it is written in:
            label_languages = elementlabel.keys()
            if len(label_languages) > 0:
                ## Take the first label:
                label = elementlabel[label_languages[0]]
            else:
                ## Couldn't find a label for this element. Give up - don't
                ## use a label at all:
                label = ""
        ## record the element's label into a local member:
        self._label = label

        ## Set the element's initial value to None:
        self.value = None

    ## Private method that should be used by a WSET object to read its
    ## own data values from the WSO, and store them into its internal data-
    ## members.
    def _retrieve_submitted_values(self):
        """This method is responsible for reading in the submitted "data values"
           for a given WSET and storing them into local members.
           Given that a WSET is responsible for knowing the names of its
           own fields, it should be able to search for them in the
           self._wso object, (which contains the details of all submitted
           fields - the field-names and their values), extract the values
           and assign them to its own local members.
           @param wso: (WebSubmissionObject) - the Web Submission Object.
           @return: None.
        """
        ## This method must be implemented in the subclass. A NotImplementedError
        ## will be raised if this method is not overridden and is called.
        abstract_method_call()

    def _retrieve_serialized_values(self):
        """This method enables a WSET instance to read its submitted value(s)
           back from the disc and to assign them to the local "value" member.
           It should only be used when no values were found in the form.
           @return: the serialized value object, or None if there wasn't one.
        """
        serialized_value = None
        ## The filename of the serialized value file:
        serialized_file_name = "%s/%s.SERIALIZED" \
                               % (self._wso.WebSubmit_submissiondir, \
                                  self._name)
        ## Does a serialized "value" exist for this WSET?
        if os.path.exists(serialized_file_name):
            ## A serialized representation of this object's value has been
            ## stored in the current submission's working directory.
            ## Retrieve it and assign it to the "value" member:
            try:
                fh_val = open(serialized_file_name, "r")
                serialized_value = load(fh_val)
                fh_val.close()
            except IOError, err:
                ## There was a problem with the value file
                raise InvenioWebSubmitInternalError(str(err))
            except UnpicklingError, err:
                ## There was a problem unpickling the data value:
                raise InvenioWebSubmitInternalError(str(err))

            ## Now unlink the serialized value file:
            os.unlink(serialized_file_name)

        ## Return the serialized value
        return serialized_value

    def serialize_values_to_submission_dir(self):
        """This function is used to tell a WSET instance to serialize its value
           into the current submission's working directory.
        """
        ## The filename of the serialized value file:
        serialized_file_name = "%s/%s.SERIALIZED" \
                            % (self._wso.WebSubmit_submissiondir, \
                               self._name)
        ## Open the serialized value file for writing (truncating any file that
        ## already exists) and serialize self.value into it.
        try:
            fh_val = open(serialized_file_name, "w+")
            dump(self.value, fh_val)
            fh_val.close()
        except IOError, err:
            ## There was a problem writing to the value file
            raise InvenioWebSubmitInternalError(str(err))
        except PicklingError, err:
            ## There was a problem pickling the data value:
            raise InvenioWebSubmitInternalError(str(err))

    ## Public interface:
    def get_html(self):
        """Return the HTML representation of a WSET to be included as an input
           field in a WebSubmit form.
           @return: (string) of HTML.
        """
        ## This method must be implemented in the subclass. A NotImplementedError
        ## will be raised if this method is not overridden and is called.
        abstract_method_call()

    def get_xml(self):
        """Return an XML representation of the data input via this element.
           The XML will later be used to create a 
           @return: (string) of XML.
        """
        ## This method must be implemented in the subclass. A NotImplementedError
        ## will be raised if this method is not overridden and is called.
        abstract_method_call()

    def has_value(self):
        """This method is used for the purpose of checking whether the user
           supplied a value for a given element during the submission.
           It will return a boolean "True" if the element has received some
           kind of value from the submission form, or "False" if not.
           @return: (boolean) - True if the element has a value; False if
            the element has no value;
        """
        ## This method must be implemented in the subclass. A NotImplementedError
        ## will be raised if this method is not overridden and is called.
        abstract_method_call()
