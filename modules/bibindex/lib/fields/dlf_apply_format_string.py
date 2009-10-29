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

from invenio.bibrecord import record_get_field_instances, field_get_subfield_values

def get_values(recid, record, format_string, tag, subfields):
    instances = record_get_field_instances(record, tag[:4], tag[4:5] or ' ', tag[5:6] or ' ')
    ret = []
    for instance in instances:
        mapping = {}
        for code in subfields:
            values = field_get_subfield_values(instance, code)
            if values:
                mapping[code] = values[0]
            else:
                mapping[code] = ''
        ret.append(format_string % mapping)
    return ret

