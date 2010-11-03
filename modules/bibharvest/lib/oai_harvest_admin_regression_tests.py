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

"""BibHarvest Admin Regression Test Suite."""

__revision__ = "$Id$"

import unittest

from invenio.config import CFG_SITE_URL
from invenio.testutils import make_test_suite, run_test_suite, \
                              test_web_page_content, merge_error_messages

class BibHarvestAdminWebPagesAvailabilityTest(unittest.TestCase):
    """Check BibHarvest Admin web pages whether they are up or not."""

    def test_oaiharvestadmin_interface_pages_availability(self):
        """oaiharvestadmin - availability of OAI Harvest Admin interface pages"""

        baseurl = CFG_SITE_URL + '/admin/bibharvest/oaiharvestadmin.py/'

        _exports = ['', 'editsource', 'addsource', 'delsource']

        error_messages = []
        for url in [baseurl + page for page in _exports]:
            # first try as guest:
            error_messages.extend(test_web_page_content(url,
                                                        username='guest',
                                                        expected_text=
                                                        'Authorization failure'))
            # then try as admin:
            error_messages.extend(test_web_page_content(url,
                                                        username='admin'))
        if error_messages:
            self.fail(merge_error_messages(error_messages))
        return

    def test_oai_admin_guide_availability(self):
        """oaiharvestadmin - availability of OAI Admin Guide"""

        url = CFG_SITE_URL + '/help/admin/oai-admin-guide'
        error_messages = test_web_page_content(url,
                                               expected_text="OAI Admin Guide")
        if error_messages:
            self.fail(merge_error_messages(error_messages))
        return

TEST_SUITE = make_test_suite(BibHarvestAdminWebPagesAvailabilityTest)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE, warn_user=True)
