# -*- coding: utf-8 -*-
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
PDF to PostScript WebSubmit File Converter.
If available this plugin will exploit the wfc_pdf2ocr plugin
"""

import os

from invenio.config import CFG_PATH_PDFTOTEXT
from invenio.websubmit_file_convert_utils import execute_command

CFG_CONVERTER_NEEDS_WORKING_DIR = False

def converter(input_file, output_file, working_dir, perform_ocr=True, ln='en', **dummy):
    """
    Return the text content in input_file.
    """
    execute_command(CFG_PATH_PDFTOTEXT, '-enc', 'UTF-8', '-eol', 'unix', '-nopgbrk', input_file, output_file)
    if perform_ocr:
        from invenio.websubmit_file_convert import convert, can_convert
        if can_convert('.pdf', '.txt;ocr'):
            ocred_output = convert(input_file, output_format='.txt;ocr', ln=ln)
        open(output_file, 'a').write(open(ocred_output).read())
        os.remove(ocred_output)

def check_prerequisities():
    return bool(CFG_PATH_PDFTOTEXT)

def get_conversion_map():
    from invenio.websubmit_file_convert import can_convert
    ret = {'.pdf' : {'.txt' : {'perform_ocr' : False}}
    if can_convert('.pdf', '.txt;ocr'):
        ret['.pdf']['.txt;+ocr'] = {'perform_ocr' : True}
    return ret
