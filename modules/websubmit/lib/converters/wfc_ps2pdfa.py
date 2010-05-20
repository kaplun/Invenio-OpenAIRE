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
Postscript to PDF/A converter
"""

import shutil
import os

from invenio.config import CFG_PATH_GS, CFG_ETCDIR
from invenio.websubmit_file_converter_utils import execute_command
from invenio.websubmit_config import InvenioWebSubmitFileConverterError
from invenio.shellutils import is_executable

def ps2pdfa(input_file, output_file, working_dir, title="No title"):
    """
    Transform any PS into a PDF/A (see: <http://www.pdfa.org/>)
    @param title [string] the title of the document.
    @param pdfopt [bool] whether to linearize the pdf, too.
    @return [string] output_file input_file
    raise InvenioWebSubmitFileConverterError in case of errors.
    """
    shutil.copy(os.path.join(CFG_ETCDIR, 'websubmit', 'file_converter_templates', 'ISOCoatedsb.icc'), working_dir)
    pdfa_header = open(os.path.join(CFG_ETCDIR, 'websubmit', 'file_converter_templates', 'PDFA_def.ps')).read()
    pdfa_header = pdfa_header.replace('<<<<TITLEMARKER>>>>', title)
    outputpdf = os.path.join(working_dir, 'output_file.pdf')
    open(os.path.join(working_dir, 'PDFA_def.ps'), 'w').write(pdfa_header)
    execute_command(CFG_PATH_GS, '-sProcessColorModel=DeviceCMYK', '-dPDFA', '-dBATCH', '-dNOPAUSE', '-dNOOUTERSAVE', '-dUseCIEColor', '-sDEVICE=pdfwrite', '-sOutputFile=output_file.pdf', 'PDFA_def.ps', input_file, cwd=working_dir)
    shutil.move(outputpdf, output_file)
    return output_file

def check_prerequisities(input_format, output_format, working_dir, title="No title"):
    if not is_executable(CFG_PATH_GS):
        raise InvenioWebSubmitFileConverterError("CFG_PATH_GS is set to %s, which either does not exists or is not executable" % (repr(CFG_PATH_GS)))

