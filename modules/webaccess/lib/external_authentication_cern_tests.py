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

"""Unit tests for the user handling library."""

__revision__ = "$Id$"

import unittest

from invenio.config import CFG_CERN_SITE
from invenio.testutils import make_test_suite, run_test_suite

class ExternalAuthenticationCernTest(unittest.TestCase):
    """Test functions related to the CERN authentication."""

    def setUp(self):
        # pylint: disable=C0103
        """setting up helper variables for tests"""
        from invenio import external_authentication_cern as cern
        self.username, self.userpwd, self.useremail = \
                open('demopwd.cfg', 'r').readline().strip().split(':', 2)
        self.cern = cern.ExternalAuthCern()

    def test_auth_user_ok(self):
        """external authentication CERN - authorizing user through CERN system: should pass"""
        self.assertEqual(self.cern.auth_user(self.username, self.userpwd), \
                self.useremail)

    def test_auth_user_fail(self):
        """external authentication CERN - authorizing user through CERN system: should fail"""
        self.assertEqual(self.cern.auth_user('patata', 'patata'), None)

    def test_fetch_user_groups_membership(self):
        """external authentication CERN - fetching user group membership at CERN"""
        self.assertNotEqual(self.cern.fetch_user_groups_membership(self.useremail, self.userpwd), 0)
        self.assertEqual(self.cern.fetch_user_groups_membership('patata', 'patata'), {})

    def test_fetch_user_preferences(self):
        """external authentication CERN - fetching user setting from CERN"""
        self.assertEqual(self.cern.fetch_user_preferences(self.username, self.userpwd)['email'], self.useremail)
        #self.assertRaises(KeyError, self.cern.fetch_user_preferences('patata', 'patata')['email'])

if CFG_CERN_SITE:
    TEST_SUITE = make_test_suite(ExternalAuthenticationCernTest,)
else:
    TEST_SUITE = make_test_suite()

if __name__ == "__main__":
    run_test_suite(TEST_SUITE)


