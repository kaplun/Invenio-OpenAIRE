# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010 CERN.
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

"""
BibIndex indexing engine configuration parameters.
"""

__revision__ = \
    "$Id$"

## configuration parameters read from the general config file:
from invenio.config import CFG_VERSION
## version number:
BIBINDEX_ENGINE_VERSION = "Invenio/%s bibindex/%s" % (CFG_VERSION, CFG_VERSION)

## safety parameters concerning DB thread-multiplication problem:
CFG_CHECK_MYSQL_THREADS = 0 # to check or not to check the problem?
CFG_MAX_MYSQL_THREADS = 50 # how many threads (connections) we
                           # consider as still safe
CFG_MYSQL_THREAD_TIMEOUT = 20 # we'll kill threads that were sleeping
                              # for more than X seconds
