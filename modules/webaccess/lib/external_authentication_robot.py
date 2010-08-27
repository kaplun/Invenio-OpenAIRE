# -*- coding: utf-8 -*-
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

"""External user authentication for simple robots

This implement an external authentication system suitable for robots usage.
User attributes are retrieved directly from the form dictionary of the request
object.
"""

import os
import sys
import hmac
import time

if sys.hexversion < 0x2060000:
    try:
        import simplejson as json
    except ImportError:
        # Okay, no Ajax app will be possible, but continue anyway,
        # since this package is only recommended, not mandatory.
        pass
else:
    import json

if sys.hexversion < 0x2050000:
    import sha as sha1
else:
    from hashlib import sha1

from cPickle import loads, dumps
from zlib import decompress, compress

from invenio.external_authentication import ExternalAuth, InvenioWebAccessExternalAuthError
from invenio.config import CFG_ETCDIR, CFG_SITE_URL, CFG_SITE_SECURE_URL

CFG_ROBOT_EMAIL_ATTRIBUTE_NAME = 'email'
CFG_ROBOT_NICKNAME_ATTRIBUTE_NAME = 'nickname'
CFG_ROBOT_GROUPS_ATTRIBUTE_NAME = 'groups'
CFG_ROBOT_TIMEOUT_ATTRIBUTE_NAME = '__timeout__'
CFG_ROBOT_GROUPS_SEPARATOR = ';'
CFG_ROBOT_URL_TIMEOUT = 3600

CFG_ROBOT_KEYS_PATH = os.path.join(CFG_ETCDIR, 'webaccess', 'robot_keys.dat')

class ExternalAuthRobot(ExternalAuth):
    def __init__(self, enforce_external_nicknames=False):
        ExternalAuth.__init__(self, enforce_external_nicknames=enforce_external_nicknames)
        from cPickle import loads
        from zlib import decompress
        try:
            self.__robot_keys = loads(decompress(open(CFG_ROBOT_KEYS_PATH).read()))
            if not isinstance(self.__robot_keys, dict):
                self.__robot_keys = {}
        except:
            self.__robot_keys = {}

    def __extract_attribute(self, req):
        from invenio.bibedit_utils import json_unicode_to_utf8
        from invenio.webinterface_handler import wash_urlargd
        args = wash_urlargd(req.form, {
            'assertion': (str, ''),
            'robot': (str, ''),
            'digest': (str, '')})
        assertion = args['assertion']
        digest = args['digest']
        robot = args['robot']
        shared_key = self.__robot_keys.get(robot)
        if shared_key is None:
            raise InvenioWebAccessExternalAuthError("A key does not exist for robot: %s" % robot)
        if hmac.new(shared_key, assertion, sha1).hexdigest() != digest:
            raise InvenioWebAccessExternalAuthError("The provided assertion %s does not validated against the digest %s for robot %s" % (repr(assertion), repr(digest), repr(robot)))
        data = json_unicode_to_utf8(json.loads(assertion))
        if not isinstance(data, dict):
            raise InvenioWebAccessExternalAuthError("The provided assertion %s is invalid" % (repr(assertion)))
        timeout = data[CFG_ROBOT_TIMEOUT_ATTRIBUTE_NAME]
        if timeout < time.time():
            raise InvenioWebAccessExternalAuthError("The provided assertion %s is expired" % (repr(assertion)))
        return data

    def auth_user(self, username, password, req=None):
        """Authenticate user-supplied USERNAME and PASSWORD.  Return
        None if authentication failed, or the email address of the
        person if the authentication was successful.  In order to do
        this you may perhaps have to keep a translation table between
        usernames and email addresses.
        Raise InvenioWebAccessExternalAuthError in case of external troubles.
        """
        data = self.__extract_attribute(req)
        email = data.get(CFG_ROBOT_EMAIL_ATTRIBUTE_NAME)
        if email:
            if isinstance(email, str):
                return email.strip().lower()
            else:
                raise InvenioWebAccessExternalAuthError("The email provided in the assertion is invalid: %s" % (repr(email)))
        else:
            return None

    def fetch_user_groups_membership(self, username, password=None, req=None):
        """Given a username and a password, returns a dictionary of groups
        and their description to which the user is subscribed.
        Raise InvenioWebAccessExternalAuthError in case of troubles.
        """
        if CFG_ROBOT_GROUPS_ATTRIBUTE_NAME:
            data = self.__extract_attribute(req)
            groups = data.get(CFG_ROBOT_GROUPS_ATTRIBUTE_NAME)
            if groups:
                if isinstance(groups, str):
                    groups = [group.strip() for group in groups.split(CFG_ROBOT_GROUPS_SEPARATOR)]
                    return dict(zip(groups, groups))
                else:
                    raise InvenioWebAccessExternalAuthError("The groups provided in the assertion are invalid: %s" % (repr(groups)))
        return {}

    def fetch_user_nickname(self, username, password=None, req=None):
        """Given a username and a password, returns the right nickname belonging
        to that user (username could be an email).
        """
        if CFG_ROBOT_NICKNAME_ATTRIBUTE_NAME:
            data = self.__extract_attribute(req)
            nickname = data.get(CFG_ROBOT_NICKNAME_ATTRIBUTE_NAME)
            if nickname:
                if isinstance(nickname, str):
                    return nickname.strip().lower()
                else:
                    raise InvenioWebAccessExternalAuthError("The nickname provided in the assertion is invalid: %s" % (repr(nickname)))
        return None

    def fetch_user_preferences(self, username, password=None, req=None):
        """Given a username and a password, returns a dictionary of keys and
        values, corresponding to external infos and settings.

        userprefs = {"telephone": "2392489",
                     "address": "10th Downing Street"}

        (WEBUSER WILL erase all prefs that starts by EXTERNAL_ and will
        store: "EXTERNAL_telephone"; all internal preferences can use whatever
        name but starting with EXTERNAL). If a pref begins with HIDDEN_ it will
        be ignored.
        """
        data = self.__extract_attribute(req)
        for key in (CFG_ROBOT_EMAIL_ATTRIBUTE_NAME, CFG_ROBOT_GROUPS_ATTRIBUTE_NAME, CFG_ROBOT_NICKNAME_ATTRIBUTE_NAME, CFG_ROBOT_TIMEOUT_ATTRIBUTE_NAME):
            if key and key in data:
                del data[key]
        return data

    def robot_login_method_p():
        """Return True if this method is dedicated to robots and should
        not therefore be available as a choice to regular users upon login.
        """
        return True
    robot_login_method_p = staticmethod(robot_login_method_p)


def test_create_example_url(email, assertion=None, timeout=None, referer=None, robot=None, login_method=None):
    from invenio.access_control_config import CFG_EXTERNAL_AUTHENTICATION
    from invenio.urlutils import create_url
    if assertion is None:
        assertion = {}
    assertion['email'] = email
    if timeout is None:
        timeout = time.time() + CFG_ROBOT_URL_TIMEOUT
    assertion['__timeout__'] = timeout
    if referer is None:
        referer = CFG_SITE_URL
    robot_keys = loads(decompress(open(CFG_ROBOT_KEYS_PATH).read()))
    if robot is None:
        robot = robot_keys.keys()[0]
    if login_method is None:
        for a_login_method, details in CFG_EXTERNAL_AUTHENTICATION.iteritems():
            if details[2]:
                login_method = a_login_method
                break
    assertion = json.dumps(assertion)
    shared_key = robot_keys[robot]
    digest = hmac.new(shared_key, assertion, sha1).hexdigest()
    return create_url("%s%s" % (CFG_SITE_SECURE_URL, "/youraccount/robotlogin"), {
        'assertion': assertion,
        'robot': robot,
        'login_method': login_method,
        'digest': digest,
        'referer': referer})


def update_robot_key(robot, key=None):
    try:
        robot_keys = loads(decompress(open(CFG_ROBOT_KEYS_PATH).read()))
    except:
        robot_keys = {}
    if key is None and robot in robots_keys:
        del robot_keys[robot]
    else:
        robot_keys[robot] = key
    os.makedirs(os.path.join(CFG_ETCDIR, 'webaccess'))
    open(CFG_ROBOT_KEYS_PATH, 'w').write(compress(dumps(robot_keys, -1)))

