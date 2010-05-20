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
Simple wrapper (through unoconv)
"""

import os
from invenio.shellutils import escape_shell_arg, is_executable
from invenio.websubmit_config import InvenioWebSubmitFileConverterError

def converter(input_file, output_file, executable, pattern):
    command = pattern % {'executable' : escape_shell_arg(executable), 'input': escape_shell_arg(input_file), 'output_file': escape_shell_arg(output_file)}
    if is_executable(executable):
        execute_command(command)
    else:
        InvenioWebSubmitFileConverterError("It is not possible to execute %s: %s does not exist or is not executable" % (command, executable))

def check_prerequisities(input_format, output_format, executable, pattern):
    if not is_executable(executable):
        raise InvenioWebSubmitFileConverterError("%s does not exist or is not executable." % executable)