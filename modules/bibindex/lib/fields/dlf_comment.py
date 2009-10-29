# -*- coding: utf-8 -*-
## BibIndxes bibliographic data, reference and fulltext indexing utility.
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
Derived logical fields to extract comments and reviews from a record.
"""

from invenio.webcomment import query_retrieve_comments_or_remarks
from invenio.intbitset import intbitset
from invenio.dbquery import run_sql
from invenio.bibrecord import record_get_field_value

def get_values(record):
    recid = record_get_field_value(record, "001")
    ret = []
    comments = query_retrieve_comments_or_remarks(recid, ranking=False)
    reviews = query_retrieve_comments_or_remarks(recid, ranking=True)
    if comments:
        for comment in comments:
            ret += comment[4] # The body
    if reviews:
        for review in reviews:
            ret += reviews[4] # The body
            ret += reviews[8] # The title
    return

def get_updated_recids(date):
    return intbitset(run_sql('SELECT id_bibrec FROM cmtRECORDCOMMENT WHERE date_creation >= %s', (date, )))