# -*- coding: utf-8 -*-
##
## $Id: WSET_File.py,v 1.2 2007/08/17 08:37:45 nich Exp $
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

"""This is the definition of the abstract WSET_File (WebSubmit Element
   Type) class.
"""

__revision__ = "$Id: WSET_File.py,v 1.2 2007/08/17 08:37:45 nich Exp $"

## Import useful stuff:
from invenio.search_engine import encode_for_xml
from invenio.config import tmpdir, \
     images
import cgi, os

## Max file size
from invenio.websubmit_engine import CFG_WEBSUBMIT_MAX_UPLOADED_FILE_SIZE

## Import the WSET (WebSubmit Element Type) base class.
from invenio.websubmit_elements.WSET import WSET, \
     CFG_WEBSUBMIT_XML_VALUE, \
     CFG_WEBSUBMIT_XML_EMPTY_VALUE, \
     CFG_WEBSUBMIT_XML_ELEMENT


CFG_WEBSUBMIT_FILE_TABLE_HEADER = """
 <table cellpadding="4">
 """

CFG_WEBSUBMIT_FILE_TABLE_FOOTER = """
 </table>"""


CFG_WEBSUBMIT_FILE_TABLE_ROW_EMPTY = """
  <tr>
   <td><input type="file" size="30" name="%(file)s" /></td>
  </tr>"""

CFG_WEBSUBMIT_FILE_TABLE_ROW_FILLED = """
  <tr>
   <td><img src="%(img_src)s"/>
   <td><strong>%(value-filename)s</strong> [%(value-filesize)s bytes]</td>
   <td><input type="submit" name="%(delete)s" value="Delete_File" />
  </tr>"""
   
class WSET_File(WSET):
    """This class represents an "File" field in a WebSubmit form.
       An file(s) field consists of the following data-entry fields:
        + file;
    """
    ## Object-inititialiser:
    def __init__(self,
                 wso,
                 elementname,
                 elementlabel,
                 outputheader="",
                 outputfooter="",
                 **dummy):
        """Initialise a WSET_File object.
           @param wso: (WebSubmissionObject) - the Web Submission Object,
            containing the various information relating to the current
            submission, the user conducting the submission, etc.
            This object will even contain the details of all values submitted
            from the last reload of the form (and therefore the value for
            the file entered - if there were any).
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
        super(WSET_File, self).__init__(wso,
                                        elementname,
                                        elementlabel,
                                        outputheader,
                                        outputfooter)
        
        ## Set some local fieldname skeletons:
        self._name_file_field = """%s_file""" % self._name
        self._name_delete_field = """%s_delete""" % self._name

        ## Retrieve any submitted values:
        self._retrieve_submitted_values()

        ## Retrieve any serialized value for this object:
        serialized_value = self._retrieve_serialized_values()

        ## If this object's value has not been set AND some kind of value was
        ## returned by the previous call to "_retrieve_serialized_values",
        ## assign the de-serialized value to self.value.
        if "".join([str(val).strip() for val in self.value.values()]) == "" \
                    and not self._name_delete_field in \
                                     self._wso.submitted_form_fields.keys() \
                    and serialized_value is not None:
            ## There was no value for the file passed in the form and the file
            ## hasn't been deleted this call, BUT there is a serialised value
            ## for the file (name) in the submission directory. Use the
            ## serialised value.
            self.value = serialized_value

    ## Private methods:
    def _retrieve_submitted_values(self):
        """This method is responsible for reading in the submitted "data values"
           for a given WSET_File element and storing them into local member,
           "self.value".
           @return: None.
        """
        ## Get the names of the submitted form fields:
        wse_field_names = self._wso.submitted_form_fields.keys()


        ## Loop through all WSO form fields and search for those that belong
        ## to this WSET_File element. For each field found (be it an file's
        ## filename) add it into a dictionary containing the details 

        files_submitted = {}
        dir_path = "%s/files/%s" % (self._wso.WebSubmit_submissiondir, \
                                    self._name_file_field)

        ## Test if the file was uploaded before in order to display file's details 
        ## when the page is reloaded for other fields
        
        if os.path.exists(dir_path):
            path_content = os.listdir(dir_path)
            if path_content != []:
                files_submitted["name"] = "%s/%s" % (dir_path, path_content[0])
                files_submitted["size"] = str(os.stat("%s/%s" %(dir_path, path_content[0])).st_size)  

        for field in wse_field_names:
            ## Is this a WSET_File "file" field for this file object?
            if field == self._name_file_field:
                ## Yes it is. 
                field_value = self._wso.submitted_form_fields[field]

                ## Test if the field contains attributes related to the file,
                ## that means that a file has been uploaded
                if hasattr(field_value, "filename") and field_value.filename is not None\
                       and field_value.filename != "":
                    filename = field_value.filename
                    ## Create a directory if it does not exist with the same name 
                    ## as the file input field to store the file
                    if not os.path.exists("%s/files/%s" % (self._wso.WebSubmit_submissiondir, field)):
                        try:
                            os.makedirs("%s/files/%s" % (self._wso.WebSubmit_submissiondir, field))
                        except IOError, err:
                            raise ValueError(str(err) + \
                                             "Cannot create file directory in submission directory.")
                    ## Read the file content from form file object UP TO limit size
                    file_content = field_value.file.read(CFG_WEBSUBMIT_MAX_UPLOADED_FILE_SIZE)
                    file_path = "%s/files/%s/%s" % (self._wso.WebSubmit_submissiondir, field, filename)
                    ## Write the content into the destination file
                    fp = open(file_path, "w")
                    fp.write(file_content)
                    fp.close()
                    files_submitted["name"] = file_path
                    ## Get the size of the file uploaded
                    files_submitted["size"] = str(os.stat(file_path).st_size)                  

            ## Is this a WSET_File "delete" field for this file object?
            if field == self._name_delete_field:
                ## Yes it is.
                ## Delete first file in the directory designated by the name of the
                ## file input field, assuming that there is only one file inside this dir
                ## as at this step the name of the file submitted previously is not
                ## into WSO.
                if os.path.exists(dir_path):
                    path_content = os.listdir(dir_path)
                    if path_content != []:
                        os.unlink("%s/%s" %(dir_path, path_content[0]))
                        files_submitted = {}
                
        ## Now, assign the details of the files to the value member:
        self.value = files_submitted

    ## Public Interface:
    def get_html(self):
        """This method is responsible for creating and returning an HTML
           string that will represent a file-fields object in the WebSubmit
           submission page interface.
           @return: (string) - HTML representation of file fields.
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

        ## Open a table to hold the files:
        element_html += CFG_WEBSUBMIT_FILE_TABLE_HEADER

        #If the file has not yet been uploaded
        if self.value == {}:
            element_html += CFG_WEBSUBMIT_FILE_TABLE_ROW_EMPTY % \
                            {"file"         : self._name_file_field}
        #The file exists
        else:
            element_html += CFG_WEBSUBMIT_FILE_TABLE_ROW_FILLED % \
                            {"value-filename" : os.path.basename(self.value.get("name", "Name not available")), \
                             "value-filesize" : self.value.get("size", ""), \
                             "delete"         : self._name_delete_field, \
                             "img_src"        : "%s/file-icon-text-15x20.gif" % images, \
                             }
                    

        ## Close the files table:
        element_html += CFG_WEBSUBMIT_FILE_TABLE_FOOTER

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
           has entered the details of (an) file(s) into a WSET_File
           element on the submission form.
           It will return a boolean "True" if the element contains the
           details of at least one file, or "False" if not.
           @return: (boolean) - True if an file is present; False if
            not;
        """
        hasvalue = True
        if self.value == {}:
            ## No file details were submitted:
            hasvalue = False

        ## return the flag indicating whether or not the file element
        ## has a value:
        return hasvalue

    def get_xml(self):
        """Return an XML representation of the files entered into a
           WSET_File element.  This element should look something like this:

                <wset_element_name>
                  <value >
                  file path
                  </value>
                </wset_element_name>

           The XML will later be used to create a 
           @return: (string) of XML.
        """
        ## Test the value
        if self.has_value() is not False:
            file_xml = CFG_WEBSUBMIT_XML_VALUE % \
                       {'id'            : "",
                        'value_content' : encode_for_xml(self.value.get("name", "")),
                        }
        else:
            file_xml = CFG_WEBSUBMIT_XML_EMPTY_VALUE
        ## Now add the file-xml into the xml string:
        xmlstr = CFG_WEBSUBMIT_XML_ELEMENT % \
                     { 'name'    : self._name,
                       'content' : file_xml,
                     }

        ## Return the XML for the files:
        return xmlstr
