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

"""CDS Invenio Search Engine config parameters."""

__revision__ = \
    "$Id$"

## Note: many interesting search engine config variables are defined
## in the global config.py.  This file should define locally
## interesting variables only.

## do we want experimental features? (0=no, 1=yes)
CFG_EXPERIMENTAL_FEATURES = 0

## Magic name used to store and retrieve the hitset of *all* the restricted
## records.
CFG_SCHBAG_RESTRICTED_RECIDS_NAME = 'restricted_recids'


class InvenioWebSearchUnknownCollectionError(Exception):
    """Exception for bad collection."""
    def __init__(self, colname):
        """Initialisation."""
        self.colname = colname
    def __str__(self):
        """String representation."""
        return repr(self.colname)
