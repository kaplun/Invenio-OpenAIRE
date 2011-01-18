# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2006, 2007, 2008, 2009, 2010, 2011 CERN.
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

"""WebAccess Regression Test Suite."""

__revision__ = "$Id$"

import unittest
import socket
import time
import cgi

from urlparse import urlparse, urlunparse
from urllib import urlopen, urlencode

from invenio.access_control_admin import acc_add_role, acc_delete_role, \
    acc_get_role_definition
from invenio.access_control_firerole import compile_role_definition, \
    serialize, deserialize
from invenio.config import CFG_SITE_URL, CFG_SITE_SECURE_URL, CFG_DEVEL_SITE
from invenio.testutils import make_test_suite, run_test_suite, \
                              test_web_page_content, merge_error_messages

class WebAccessWebPagesAvailabilityTest(unittest.TestCase):
    """Check WebAccess web pages whether they are up or not."""

    def test_webaccess_admin_interface_availability(self):
        """webaccess - availability of WebAccess Admin interface pages"""

        baseurl = CFG_SITE_URL + '/admin/webaccess/webaccessadmin.py/'

        _exports = ['', 'delegate_startarea', 'manageaccounts']

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

    def test_webaccess_admin_guide_availability(self):
        """webaccess - availability of WebAccess Admin guide pages"""

        url = CFG_SITE_URL + '/help/admin/webaccess-admin-guide'
        error_messages = test_web_page_content(url,
                                               expected_text="WebAccess Admin Guide")
        if error_messages:
            self.fail(merge_error_messages(error_messages))
        return

class WebAccessFireRoleTest(unittest.TestCase):
    """Check WebAccess behaviour WRT FireRole."""

    def setUp(self):
        """Create a fake role."""
        self.role_name = 'test'
        self.role_description = 'test role'
        self.role_definition = 'allow email /.*@cern.ch/'
        self.role_id, dummy, dummy, dummy = acc_add_role(self.role_name,
            self.role_description,
            serialize(compile_role_definition(self.role_definition)),
            self.role_definition)

    def tearDown(self):
        """Drop the fake role."""
        acc_delete_role(self.role_id)

    def test_webaccess_firerole_serialization(self):
        """webaccess - firerole role definition correctly serialized"""
        def_ser = compile_role_definition(self.role_definition)
        tmp_def_ser = acc_get_role_definition(self.role_id)
        self.assertEqual(def_ser, deserialize(tmp_def_ser))

class WebAccessUseBasketsTest(unittest.TestCase):
    """
    Check WebAccess behaviour WRT enabling/disabling web modules such
    as baskets.
    """

    def test_precached_area_authorization(self):
        """webaccess - login-time precached authorizations for usebaskets"""
        error_messages = test_web_page_content(CFG_SITE_SECURE_URL + '/youraccount/display?ln=en', username='jekyll', password='j123ekyll', expected_text='Your Baskets')
        error_messages.extend(test_web_page_content(CFG_SITE_SECURE_URL + '/youraccount/display?ln=en', username='hyde', password='h123yde', unexpected_text='Your Baskets'))

        if error_messages:
            self.fail(merge_error_messages(error_messages))

if CFG_DEVEL_SITE:
    class WebAccessRobotLoginTest(unittest.TestCase):
        """
        Check whether robot login functionality is OK.
        """
        def _erase_example_user_and_groups(self):
            from invenio.dbquery import run_sql
            uid = run_sql("SELECT id FROM user WHERE email=%s", (self.a_email, ))
            if uid:
                run_sql("DELETE FROM user WHERE id=%s", (uid[0][0], ))
                run_sql("DELETE FROM user_usergroup WHERE id_user=%s", (uid[0][0], ))
            for method_name in self.robot_login_methods:
                for group in self.some_groups:
                    run_sql("DELETE FROM usergroup WHERE name=%s", ("%s [%s]" % (group, method_name), ))

        def setUp(self):
            from invenio.access_control_config import CFG_EXTERNAL_AUTHENTICATION
            self.robot_login_methods = dict([(method_name, CFG_EXTERNAL_AUTHENTICATION[method_name]) for method_name in CFG_EXTERNAL_AUTHENTICATION if CFG_EXTERNAL_AUTHENTICATION[method_name] and CFG_EXTERNAL_AUTHENTICATION[method_name].robot_login_method_p()])
            self.a_robot = "regression-test"
            self.a_password = "123"
            self.a_email = "foo.bar@example.org"
            self.a_nickname = "foo-bar"
            self.some_groups = ["a group for regression test", "another group for regression test"]
            self.myip = urlopen(CFG_SITE_URL + "/httptest/whatismyip").read()
            from invenio.external_authentication_robot import update_robot_key
            for method_name in self.robot_login_methods:
                update_robot_key(method_name, self.a_robot, self.a_password)
            from invenio.external_authentication_robot import load_robot_keys

        def tearDown(self):
            from invenio.external_authentication_robot import update_robot_key
            #for method_name in self.robot_login_methods:
                #update_robot_key(method_name, self.a_robot)
            from invenio.external_authentication_robot import load_robot_keys
            self._erase_example_user_and_groups()

        def test_normal_robot_login_method(self):
            """webaccess - robot login method"""
            for method_name, method in self.robot_login_methods.iteritems():
                url = method.test_create_example_url(self.a_email, method_name, self.a_robot, self.myip)
                try:
                    error_messages = test_web_page_content(url, expected_text=self.a_email)
                    if error_messages:
                        self.fail(merge_error_messages(error_messages))
                finally:
                    self._erase_example_user_and_groups()

        def test_robot_login_method_with_nickname(self):
            """webaccess - robot login method with nickname"""
            for method_name, method in self.robot_login_methods.iteritems():
                if method.enforce_external_nicknames:
                    url = method.test_create_example_url(self.a_email, method_name, self.a_robot, self.myip, nickname=self.a_nickname)
                    try:
                        error_messages = test_web_page_content(url, expected_text=self.a_nickname)
                        if error_messages:
                            self.fail(merge_error_messages(error_messages))
                    finally:
                        self._erase_example_user_and_groups()

        def test_robot_login_method_with_groups(self):
            """webaccess - robot login method with groups"""
            for method_name, method in self.robot_login_methods.iteritems():
                url = method.test_create_example_url(self.a_email, method_name, self.a_robot, self.myip, groups=self.some_groups, referer=CFG_SITE_SECURE_URL + "/yourgroups/display")
                try:
                    for group in self.some_groups:
                        error_messages = test_web_page_content(url, expected_text="%s [%s]" % (group, method_name))
                    if error_messages:
                        self.fail(merge_error_messages(error_messages))
                finally:
                    self._erase_example_user_and_groups()

        def test_robot_login_method_wrong_ip(self):
            """webaccess - robot login method wrong IP"""
            for method_name, method in self.robot_login_methods.iteritems():
                url = method.test_create_example_url(self.a_email, method_name, self.a_robot, '123.123.123.123')
                try:
                    error_messages = test_web_page_content(url, expected_text="The provided assertion has been issued for a different IP address")
                    if error_messages:
                        self.fail(merge_error_messages(error_messages))
                finally:
                    self._erase_example_user_and_groups()

        def test_robot_login_method_expired_assertion(self):
            """webaccess - robot login method with expired assertion"""
            for method_name, method in self.robot_login_methods.iteritems():
                url = method.test_create_example_url(self.a_email, method_name, self.a_robot, self.myip, timeout=time.time())
                time.sleep(1)
                try:
                    error_messages = test_web_page_content(url, expected_text="The provided assertion is expired")
                    if error_messages:
                        self.fail(merge_error_messages(error_messages))
                finally:
                    self._erase_example_user_and_groups()

        def test_robot_login_method_with_invalid_signature(self):
            """webaccess - robot login method with invalid signature"""
            for method_name, method in self.robot_login_methods.iteritems():
                url = method.test_create_example_url(self.a_email, method_name, self.a_robot, self.myip)
                url = list(urlparse(url))
                query = cgi.parse_qs(url[4])
                for key, value in query.items():
                    query[key] = value[0]
                digest = query['digest']
                digest0 = digest[0]
                if digest0 == '0':
                    digest0 = '1'
                else:
                    digest0 = '0'
                digest = digest0 + digest[1:]
                query['digest'] = digest
                url[4] = urlencode(query)
                url = urlunparse(url)
                try:
                    error_messages = test_web_page_content(url, expected_text="does not validate against the digest")
                    if error_messages:
                        self.fail(merge_error_messages(error_messages))
                finally:
                    self._erase_example_user_and_groups()


    TEST_SUITE = make_test_suite(WebAccessWebPagesAvailabilityTest,
                                WebAccessFireRoleTest,
                                WebAccessUseBasketsTest,
                                WebAccessRobotLoginTest)
else:
    TEST_SUITE = make_test_suite(WebAccessWebPagesAvailabilityTest,
                                WebAccessFireRoleTest,
                                WebAccessUseBasketsTest)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE, warn_user=True)
