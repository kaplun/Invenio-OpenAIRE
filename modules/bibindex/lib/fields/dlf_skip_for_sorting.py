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

"""
Derived logical fields to put toghether some subfields into a given string
using a format string.
"""

from invenio.bibrecord import record_get_field_values

def get_values(recid, record, tags, special_char='*', separator=", "):
    ret = []
    for tag in tags:
        values = record_get_field_values(record, tag[:4], tag[4:5] or ' ', tag[5:6] or ' ', tag[6:7] or '')
        for value in values:
            split_value = value.split(special_char, 1)
            if len(split_value) == 2:
                ret.append('%s%s%s' % (split_value[1], separator, split_value[0]))
    return ret