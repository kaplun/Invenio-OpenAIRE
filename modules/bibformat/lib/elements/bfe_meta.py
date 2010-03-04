# -*- coding: utf-8 -*-
##
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008 CERN.
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
"""BibFormat element - Prints a custom field in a way suitable to be used
   in HTML META tags.
"""
__revision__ = "$Id$"

from invenio.bibformat_utils import parse_tag
from invenio.bibformat_elements.bfe_field import format as field_format
from invenio.htmlutils import create_html_tag

def format(bfo, tag, name, escape=4):
    values = bfo.fields(tag, escape=escape)
    out = []
    for value in values:
        if isinstance(value, list):
            out += value
        elif isinstance(value, dict):
            out += value.values()
        else:
            out.append(value)
    return '\n'.join([create_html_tag('meta', name=name, content=value) for value in out])

def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
