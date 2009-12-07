# -*- coding: utf-8 -*-
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
WebSubmit NG Report Number Engine module.
"""

from datetime import datetime

from invenio.dbquery import run_sql

def default_partial_expand_pattern(session, pattern, counter_pattern):
    elements = dict(session)
    if 'year' not in elements:
        elements['year'] = datetime.today().year
    elements['counter'] = counter_pattern
    return pattern % elements

def create_report_number(session, pattern, counter_pattern, partial_expand_pattern=default_partial_expand_pattern):
    pattern = partial_expand_pattern(session, pattern, counter_pattern)
    try:
        run_sql("LOCK TABLES sbmRNCOUNTERS WRITE")
        res = run_sql("SELECT counter FROM sbmRNCOUNTERS WHERE pattern=%s", (pattern, ))
        if res:
            counter = res[0][0]
            run_sql("UPDATE sbmRNCOUNTERS SET counter=%s, last_modification=NOW() WHERE pattern=%s" % (counter + 1, pattern))
        else:
            counter = 1
            run_sql("INSERT INTO sbmRNCOUNTERS(counter, pattern, last_modification) VALUES(%s, %s, NOW())" % (counter + 1, pattern))
    finally:
        run_sql("UNLOCK TABLES")
    report_number = pattern % counter
    return report_number

