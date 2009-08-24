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
Gzip WebSubmit File Converter.
"""

import os

from invenio.config import CFG_PATH_GZIP
from invenio.websubmit_file_converter_utils import execute_command, \
    InvenioWebSubmitFileConverterError, normalize_format

CFG_CONVERTER_NEEDS_WORKING_DIR = False

def converter(input_file, output_file, working_dir, **argd):
    execute_command(CFG_PATH_GZIP, input_file, '-c', filename_out=output_file)

def check_prerequisities():
    """Return True if OpenOffice tmpdir do exists and OpenOffice can
    successfully create file there."""
    return bool(CFG_PATH_GZIP)

def get_conversion_map():
    return {'' : {'.gz' : ()}}
