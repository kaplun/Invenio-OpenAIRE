# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2010, 2011 CERN.
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

"""Unit tests for the invenio_connector script."""

__revision__ = "$Id$"

import os
import unittest

from invenio.invenio_connector import InvenioConnector
from invenio.config import CFG_SITE_URL
from invenio.testutils import make_test_suite, run_test_suite

class InvenioConnectorTest(unittest.TestCase):
    """Test function to get default values."""

    def test_local_search(self):
        """InvenioConnector - local search"""
        server = InvenioConnector(CFG_SITE_URL)
        result = server.search(p='ellis', of='id')
        self.assertTrue(len(result) > 0, \
                        'did not get local search results.')

    def test_remote_search(self):
        """InvenioConnector - remote search"""
        server = InvenioConnector("http://inspirebeta.net")
        result = server.search(p='ellis', of='id')
        self.assertTrue(len(result) > 0, \
                        'did not get remote search results from http://inspirebeta.net.')

    def test_search_collections(self):
        """InvenioConnector - collection search"""
        server = InvenioConnector(CFG_SITE_URL)
        result = server.search(p='', c=['Books'], of='id')
        self.assertTrue(len(result) > 0, \
                        'did not get collection search results.')

TEST_SUITE = make_test_suite(InvenioConnectorTest)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE, warn_user=True)
