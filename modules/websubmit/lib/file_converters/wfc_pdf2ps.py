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
"""

from invenio.config import CFG_PATH_PDFTOPS
from invenio.websubmit_file_converter_utils import execute_command, InvenioWebSubmitFileConverterError

CFG_CONVERTER_NEEDS_WORKING_DIR = False

def converter(input_file, output_file, working_dir, level=2, **dummy):
    """
    Convert from Pdf to Postscript.
    """
    level = str(level).strip()
    if level not in ("1", "2", "3"):
        raise InvenioWebSubmitFileConverterError("Invalid Postscript level: %s" % level)
    execute_command(CFG_PATH_PDFTOPS, '-level%s' % level, input_file, output_file)

def check_prerequisities():
    return bool(CFG_PATH_PDFTOPS)

def get_conversion_map():
    return {'.pdf' : {'.ps' : {}}}