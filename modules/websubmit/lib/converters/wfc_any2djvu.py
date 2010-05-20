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
OpenOffice.org wrapper (through unoconv)
"""

import os

CFG_CONVERTER_NEEDS_WORKING_DIR = True
CFG_CONVERSION_MAP = {
    'from': ['.bmp', '.djvu', '.gif', '.jpeg', '.pbm', '.pdf', '.pict', '.pnm', '.ps', '.tiff'],
    'to': ['.djvu'],
    'params': {'resolution': 400, 'ocr': True, 'input_format': 5}
}

def any2djvu(input_file, output_file, resolution=400, ocr=True, input_format=5):
    """
    Transform input_file into a .djvu file.
    @param input_file [string] the input file name
    @param output_file [string] the output_file file name, None for temporary generated
    @param resolution [int] the resolution of the output_file
    @param input_format [int] [1-9]:
        1 - DjVu Document (for verification or OCR)
        2 - PS/PS.GZ/PDF Document (default)
        3 - Photo/Picture/Icon
        4 - Scanned Document - B&W - <200 dpi
        5 - Scanned Document - B&W - 200-400 dpi
        6 - Scanned Document - B&W - >400 dpi
        7 - Scanned Document - Color/Mixed - <200 dpi
        8 - Scanned Document - Color/Mixed - 200-400 dpi
        9 - Scanned Document - Color/Mixed - >400 dpi
    @return [string] output_file input_file.
    raise InvenioWebSubmitFileConverterError in case of errors.
    Note: due to the bottleneck of using a centralized server, it is very
    slow and is not suitable for interactive usage (e.g. WebSubmit functions)
    """
    ocr = ocr and "1" or "0"

    ## Any2djvu expect to find the file in the current directory.
    execute_command(CFG_PATH_ANY2DJVU, '-a', '-c', '-r', resolution, '-o', ocr, '-f', input_format, os.path.basename(input_file), cwd=working_dir)

    ## Any2djvu doesn't let you choose the output_file file name.
    djvu_output = os.path.join(working_dir, decompose_file(input_file)[1] + '.djvu')
    return output_file
