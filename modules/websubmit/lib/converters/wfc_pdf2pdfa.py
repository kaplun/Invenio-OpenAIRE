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
PDF to PDF/A converter
"""

import os
import re
import shutil
from logging import debug

from invenio.config import CFG_PATH_PDFINFO, CFG_PATH_PDFTOPS, CFG_PATH_GS, CFG_ETCDIR
from invenio.websubmit_config import InvenioWebSubmitFileConverterError
from invenio.websubmit_file_converter_utils import execute_command

_RE_FIND_TITLE = re.compile(r'^Title:\s*(.*?)\s*$')
def pdf2pdfa(input_file, output_file, working_dir, title=None):
    """
    Transform any PDF into a PDF/A (see: <http://www.pdfa.org/>)
    @param title [string] the title of the document. None for autodiscovery.
    """
    if title is None:
        stdout = execute_command(CFG_PATH_PDFINFO, input_file)
        for line in stdout.split('\n'):
            g = _RE_FIND_TITLE.match(line)
            if g:
                title = g.group(1)
                break
    if not title:
        raise InvenioWebSubmitFileConverterError("It's impossible to automatically discover the title. Please specify it as a parameter")

    debug("Extracted title is %s" % title)

    shutil.copy(os.path.join(CFG_ETCDIR, 'websubmit', 'file_converter_templates', 'ISOCoatedsb.icc'), working_dir)
    pdfa_header = open(os.path.join(CFG_ETCDIR, 'websubmit', 'file_converter_templates', 'PDFA_def.ps')).read()
    pdfa_header = pdfa_header.replace('<<<<TITLEMARKER>>>>', title)
    inputps = os.path.join(working_dir, 'input.ps')
    outputpdf = os.path.join(working_dir, 'output_file.pdf')
    open(os.path.join(working_dir, 'PDFA_def.ps'), 'w').write(pdfa_header)
    execute_command(CFG_PATH_PDFTOPS, '-level3', input_file, inputps)
    execute_command(CFG_PATH_GS, '-sProcessColorModel=DeviceCMYK', '-dPDFA', '-dBATCH', '-dNOPAUSE', '-dNOOUTERSAVE', '-dUseCIEColor', '-sDEVICE=pdfwrite', '-sOutputFile=output_file.pdf', 'PDFA_def.ps', 'input.ps', cwd=working_dir)
    shutil.move(outputpdf, output_file)

def check_prerequisities(input_format, output_format, working_dir, title=None):
    if not is_executable(CFG_PATH_GS):
        raise InvenioWebSubmitFileConverterError("CFG_PATH_GS is set to %s, which either does not exists or is not executable" % (repr(CFG_PATH_GS)))
    if not is_executable(CFG_PATH_PDFINFO):
        raise InvenioWebSubmitFileConverterError("CFG_PATH_PDFINFO is set to %s, which either does not exists or is not executable" % (repr(CFG_PATH_PDFINFO)))
    if not is_executable(CFG_PATH_PDFTOPS):
        raise InvenioWebSubmitFileConverterError("CFG_PATH_PDFTOPS is set to %s, which either does not exists or is not executable" % (repr(CFG_PATH_PDFTOPS)))
