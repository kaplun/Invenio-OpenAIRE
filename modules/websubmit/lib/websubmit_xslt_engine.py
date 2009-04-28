# -*- coding: utf-8 -*-
##
## $Id: websubmit_xslt_engine.py,v 1.1 2007/08/14 12:33:15 diane Exp $
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

"""
websubmit_xslt_engine - Wrapper for an XSLT engine.

Some functions are registered in order to be used in XSL code:

Dependencies: Need one of the following XSLT processors:
              - libxml2 & libxslt
              - 4suite

Used by: websubmit_engine.py
"""

__revision__ = "$Id: websubmit_xslt_engine.py,v 1.1 2007/08/14 12:33:15 diane Exp $"

import sys
import os
import time
import string
from invenio.config import \
     weburl, \
     etcdir

from invenio.file import readfile
#FIXME this config varible must be moved to websubmit_config
CFG_WEBSUBMIT_TEMPLATES_PATH = etcdir + "/websubmit"

# The namespace used for Websubmit function
CFG_WEBSUBMIT_FUNCTION_NS = "http://cdsweb.cern.ch/websubmit/fn"

# Import one XSLT processor
#
# processor_type:
#       -1 : No processor found
#        0 : libxslt
#        1 : 4suite
processor_type = -1
try:
    # libxml2 & libxslt
    processor_type = 0
    import libxml2
    import libxslt
except ImportError:
    pass

if processor_type == -1:
    try:
        # 4suite
        processor_type = 1
        from Ft.Xml.Xslt import Processor
        from Ft.Xml import InputSource
        from xml.dom import Node
    except ImportError:
        pass

if processor_type == -1:
    # No XSLT processor found
    sys.stderr.write('No XSLT processor could be found.\n' \
                     'No output produced.\n')
    sys.exit(1)

##################################################################
# Support for formatting date, fetching file content, and looking
# into knowlegde base file.

def get_current_date_libxslt(ctx, format):
    """
    libxslt extension function:
    Bridge between Websubmit and XSL stylesheets.
    
    Can be used in that way in XSL stylesheet
    
    (provided xmlns:fn="http://cdsweb.cern.ch/websubmit/fn" has been declared):
    <xsl:value-of select="fn:current_date('%Y%V')"/> where %Y%V is the format of the date.
    The date is the current time.
        
    """
    try:
        return time.strftime(str(format))
    except Exception, err:
        sys.stderr.write("Error during formatting function evaluation: " + \
                         str(err) + \
                         '\n')
        return ''
    
def get_current_date_4suite(ctx, format):
    """
    libxslt extension function:
    Bridge between Websubmit and XSL stylesheets.
    
    Can be used in that way in XSL stylesheet
    
    (provided xmlns:fn="http://cdsweb.cern.ch/websubmit/fn" has been declared):
    (provided xmlns:fn="http://cdsweb.cern.ch/websubmit/fn" has been declared):
    <xsl:value-of select="fn:current_date('%Y%V')"/> where %Y%V is the format of the date.
    The date is the current time.
    
    """
    try:
        return time.strftime(str(format))
    except Exception, err:
        sys.stderr.write("Error during formatting function evaluation: " + \
                         str(err) + \
                         '\n')
        
        return ''

def read_file_libxslt(ctx, path):
    """
    libxslt extension function:
    Bridge between Websubmit and XSL stylesheets.
    
    Can be used in that way in XSL stylesheet
    
    (provided xmlns:fn="http://cdsweb.cern.ch/websubmit/fn" has been declared):
    <xsl:value-of select="fn:read_file('/test/')"/> where '/test' is the path to
    file to be read. If file cannot be read, return an empty string.
        
    """
    try:
        return readfile(str(path)).rstrip('\n')
    except Exception, err:
        sys.stderr.write("Error during formatting function evaluation: " + \
                         str(err) + \
                         '\n')
        return ''
    
def read_file_4suite(ctx, path):
    """
    libxslt extension function:
    Bridge between Websubmit and XSL stylesheets.
    
    Can be used in that way in XSL stylesheet
    
    (provided xmlns:fn="http://cdsweb.cern.ch/websubmit/fn" has been declared):
    <xsl:value-of select="fn:read_file('/test/')"/> where '/test' is the path to
    file to be read. If file cannot be read, return an empty string.
        
    """
    try:
        return readfile(str(path)).rstrip('\n')
    except Exception, err:
        sys.stderr.write("Error during formatting function evaluation: " + \
                         str(err) + \
                         '\n')
        
        return ''

def look_up_KB_file_libxslt(ctx, value, path, mode):
    """
    libxslt extension function:
    Bridge between Websubmit and XSL stylesheets.
    
    Can be used in that way in XSL stylesheet
    
    (provided xmlns:fn="http://cdsweb.cern.ch/websubmit/fn" has been declared):
    <xsl:value-of select="fn:look_up_KB('/test_KB/')"/> where '/test_KB' is the path to
    KB file to be read. If file cannot be read, or the pattern is not found
    return an empty string.
        
    """
    try:
        if isinstance(value, str):
            string_value = value
        elif isinstance(value, int):
            string_value = str(value)
        else:
            string_value = libxml2.xmlNode(_obj=value[0]).children.content
        return crawl_KB(str(path), string_value, mode=mode)
    except Exception, err:
        sys.stderr.write("Error during formatting function evaluation: " + \
                         str(err) + \
                         '\n')
        return ''
    
def look_up_KB_file_4suite(ctx, value, path):
    """
    libxslt extension function:
    Bridge between Websubmit and XSL stylesheets.
    
    Can be used in that way in XSL stylesheet
    
    (provided xmlns:fn="http://cdsweb.cern.ch/websubmit/fn" has been declared):
    <xsl:value-of select="fn:look_up_KB('/test_KB/')"/> where '/test_KB' is the path to
    KB file to be read. If file cannot be read, or the pattern is not found
    return an empty string.
        
    """
    try:
        if isinstance(value, str):
            string_value = value
        elif isinstance(value, int):
            string_value = str(value)
        else:
            string_value = libxml2.xmlNode(_obj=value[0]).children.content
        return crawl_KB(str(path), string_value, mode=None)
    except Exception, err:
        sys.stderr.write("Error during formatting function evaluation: " + \
                         str(err) + \
                         '\n')
        
        return ''
    
def crawl_KB(filename, value, mode=None):
    """
    look-up value in KB_file in one of following modes:
    ===========================================================
    1                           - case sensitive     / match  (default)
    2                           - not case sensitive / search
    3                           - case sensitive     / search
    4                           - not case sensitive / match
    5                           - case sensitive     / search (in KB)
    6                           - not case sensitive / search (in KB)
    7                           - case sensitive     / search (reciprocal)
    8                           - not case sensitive / search (reciprocal)
    9                           - replace by _DEFAULT_ only
    R                           - not case sensitive / search (reciprocal) (8) replace
    """

    # FIXME: Remove \n from returned value?
    if (os.path.isfile(filename)):
        file_to_read = open(filename,"r")
        file_read = file_to_read.readlines()
        for line in file_read:
            code = string.split(line, "---")
            if (mode == "2"):
                value_to_cmp   = value.lower()
                code[0]        = code[0].lower()
                if ((len(value_to_cmp.split(code[0])) > 1) \
                    or (code[0]=="_DEFAULT_")):
                    value = code[1]
                                                   
            elif ((mode == "3") or (mode == "0")):
                if ((len(value.split(code[0])) > 1) \
                    or (code[0]=="_DEFAULT_")):
                    value = code[1]
                                        
            elif (mode == "4"):
                value_to_cmp   = value.lower()
                code[0]        = code[0].lower()
                if ((code[0] == value_to_cmp) or \
                    (code[0] == "_DEFAULT_")):
                    value = code[1]
                                        
            elif (mode == "5"):
                if ((len(code[0].split(value)) > 1) \
                    or (code[0]=="_DEFAULT_")):
                    value = code[1]
                                                    
            elif (mode == "6"):
                value_to_cmp   = value.lower()
                code[0]        = code[0].lower()
                if ((len(code[0].split(value_to_cmp)) > 1) \
                    or (code[0] == "_DEFAULT_")):
                    value = code[1]
                                                    
            elif (mode == "7"):
                if ((len(code[0].split(value)) > 1) \
                    or (len(value.split(code[0])) > 1) \
                    or (code[0] == "_DEFAULT_")):
                    value = code[1]
                                                   
            elif (mode == "8"):
                value_to_cmp   = value.lower()
                code[0]        = code[0].lower()
                if ((len(code[0].split(value_to_cmp)) > 1) \
                    or (len(value_to_cmp.split(code[0])) > 1) \
                    or (code[0] == "_DEFAULT_")):
                    value = code[1]
                                
            elif (mode == "9"):
                if (code[0]=="_DEFAULT_"):
                    value = code[1]
                    
            elif (mode == "R"):
                value_to_cmp   = value.lower()
                code[0]        = code[0].lower()
                if ((len(code[0].split(value_to_cmp)) > 1) \
                    or (len(value_to_cmp.split(code[0])) > 1) \
                    or (code[0] == "_DEFAULT_")):
                    value = value.replace(code[0], code[1])
            else:
                if ((code[0] == value) or (code[0]=="_DEFAULT_")):
                    value = code[1]
        value = value.rstrip("</subfield>\n")
        value = value.lstrip('<subfield code="a">')
        file_to_read.close()
        return value
    else:
        return 'file not found'
        
# End of related functions                                  #
##################################################################

def parse(xmltext, template_filename=None, template_source=None):
    """
    Processes an XML text according to a template, and returns the result.

    The template can be given either by name (or by path) or by source.
    If source is given, name is ignored.

    websubmit_xslt_engine will look for template_filename in standard directories
    for templates. If not found, template_filename will be assumed to be a path to
    a template. If none can be found, return None.

    @param xmltext The string representation of the XML to process
    @param template_filename The name of the template to use for the processing
    @param template_source The configuration describing the processing.
    @return the transformed XML text.
    """
    if processor_type == -1:
        # No XSLT processor found
        sys.stderr.write('No XSLT processor could be found.')
        sys.exit(1)

    # Retrieve template and read it
    if template_source:
        template = template_source
    elif template_filename:
        try:
            path_to_templates = (CFG_WEBSUBMIT_TEMPLATES_PATH + os.sep +
                                 template_filename)
            if os.path.exists(path_to_templates):
                template = file(path_to_templates).read()
            elif os.path.exists(template_filename):
                template = file(template_filename).read()
            else:
                sys.stderr.write(template_filename +' does not exist.')
                return None
        except IOError:
            sys.stderr.write(template_filename +' could not be read.')
            return None
    else:
        sys.stderr.write(template_filename +' was not given.')
        return None

    result = ""
    if processor_type == 0:
        # libxml2 & libxslt
        
        # Register Websubmit functions for use in XSL
        libxslt.registerExtModuleFunction("current_date",
                                          CFG_WEBSUBMIT_FUNCTION_NS,
                                          get_current_date_libxslt)
        libxslt.registerExtModuleFunction("read_file",
                                          CFG_WEBSUBMIT_FUNCTION_NS,
                                          read_file_libxslt)
        libxslt.registerExtModuleFunction("look_up_KB",
                                          CFG_WEBSUBMIT_FUNCTION_NS,
                                          look_up_KB_file_libxslt)

        # Load template and source
        template_xml = libxml2.parseDoc(template)
        processor = libxslt.parseStylesheetDoc(template_xml)
        source = libxml2.parseDoc(xmltext)

        # Transform
        result_object = processor.applyStylesheet(source, None)
        result = processor.saveResultToString(result_object)

        # Deallocate
        processor.freeStylesheet()
        source.freeDoc()
        result_object.freeDoc()

    elif processor_type == 1:
        # 4suite

        # Init
        processor = Processor.Processor()
        
        # Register Websubmit functions for use in XSL
        processor.registerExtensionFunction(CFG_WEBSUBMIT_FUNCTION_NS,
                                            "current_date",
                                            get_current_date_4suite)
        libxslt.registerExtModuleFunction("read_file",
                                          CFG_WEBSUBMIT_FUNCTION_NS,
                                          read_file_4suite)
        libxslt.registerExtModuleFunction("look_up_KB",
                                          CFG_WEBSUBMIT_FUNCTION_NS,
                                          look_up_KB_file_4suite)


        # Load template and source
        transform = InputSource.DefaultFactory.fromString(template,
                                                       uri=weburl)
        source = InputSource.DefaultFactory.fromString(xmltext,
                                                       uri=weburl)
        processor.appendStylesheet(transform)

        # Transform
        result = processor.run(source)
    else:
        sys.stderr.write("No XSLT processor could be found")
        
    return result
    
if __name__ == "__main__":
    pass

