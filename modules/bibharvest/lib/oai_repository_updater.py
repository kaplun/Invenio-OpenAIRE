## This file is part of Invenio.
## Copyright (C) 2009, 2010, 2011 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""OAI Repository administration tool -

   Updates the metadata of the records to include OAI identifiers and
   OAI SetSpec according to the settings defined in OAI Repository
   admin interface

"""

from invenio.dbquery import run_sql
from invenio.config import CFG_OAI_ID_FIELD, CFG_OAI_SET_FIELD, \
    CFG_OAI_SET_FIELD, CFG_OAI_ID_PREFIX
from invenio.search_engine import search_pattern


def build_oai_id(recid):
    """
    Return the oai_id corresponding to a given recid.
    """
    return "oai:%s:%s" % (CFG_OAI_ID_PREFIX, recid)

def get_all_set_specs():
    """
    Return all the defined set_specs
    """
    res = run_sql("SELECT DISTINCT(setSpec) FROM oaiREPOSITORY")
    return [row[0] for row in res]

def get_all_modified_recid(since):

