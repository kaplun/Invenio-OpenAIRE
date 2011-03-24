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

# pylint: disable=C0103
"""Invenio BibEdit Administrator Interface."""

__revision__ = "$Id"

__lastupdated__ = """$Date: 2008/08/12 09:26:46 $"""

import sys
if sys.hexversion < 0x2060000:
    try:
        import simplejson as json
        simplejson_available = True
    except ImportError:
        # Okay, no Ajax app will be possible, but continue anyway,
        # since this package is only recommended, not mandatory.
        simplejson_available = False
else:
    import json
    simplejson_available = True

from invenio.access_control_engine import acc_authorize_action
from invenio.bibedit_engine import perform_request_ajax, perform_request_init, \
    perform_request_newticket, perform_request_compare
from invenio.bibedit_utils import json_unicode_to_utf8
from invenio.config import CFG_SITE_LANG, CFG_SITE_URL
from invenio.messages import gettext_set_language
from invenio.search_engine import guess_primary_collection_of_a_record
from invenio.urlutils import redirect_to_url
from invenio.webinterface_handler import WebInterfaceDirectory, wash_urlargd
from invenio.webpage import page
from invenio.webuser import collect_user_info, getUid, page_not_authorized

navtrail = (' <a class="navtrail" href=\"%s/help/admin\">Admin Area</a> '
            ) % CFG_SITE_URL


class WebInterfaceEditPages(WebInterfaceDirectory):
    """Defines the set of /edit pages."""

    _exports = ['', 'new_ticket', 'compare_revisions']

    def __init__(self, recid=None):
        """Initialize."""
        self.recid = recid

    def index(self, req, form):
        """Handle all BibEdit requests.
        The responsibilities of this functions is:
        * JSON decoding and encoding.
        * Redirection, if necessary.
        * Authorization.
        * Calling the appropriate function from the engine.

        """
        uid = getUid(req)
        argd = wash_urlargd(form, {'ln': (str, CFG_SITE_LANG)})
        # Abort if the simplejson module isn't available
        if not simplejson_available:
            title = 'Record Editor'
            body = '''Sorry, the record editor cannot operate when the
                `simplejson' module is not installed.  Please see the INSTALL
                file.'''
            return page(title       = title,
                        body        = body,
                        errors      = [],
                        warnings    = [],
                        uid         = uid,
                        language    = argd['ln'],
                        navtrail    = navtrail,
                        lastupdated = __lastupdated__,
                        req         = req)

        # If it is an Ajax request, extract any JSON data.
        ajax_request, recid = False, None
        if form.has_key('jsondata'):
            json_data = json.loads(str(form['jsondata']))
            # Deunicode all strings (Invenio doesn't have unicode
            # support).
            json_data = json_unicode_to_utf8(json_data)
            ajax_request = True
            if json_data.has_key('recID'):
                recid = json_data['recID']
            json_response = {'resultCode': 0, 'ID': json_data['ID']}

        # Authorization.
        user_info = collect_user_info(req)
        if user_info['email'] == 'guest':
            # User is not logged in.
            if not ajax_request:
                # Do not display the introductory recID selection box to guest
                # users (as it used to be with v0.99.0):
                auth_code, auth_message = acc_authorize_action(req,
                                                               'runbibedit')
                referer = '/edit/'
                if self.recid:
                    referer = '/record/%s/edit/' % self.recid
                return page_not_authorized(req=req, referer=referer,
                                           text=auth_message, navtrail=navtrail)
            else:
                # Session has most likely timed out.
                json_response.update({'resultCode': 100})
                return json.dumps(json_response)

        elif self.recid:
            # Handle RESTful calls from logged in users by redirecting to
            # generic URL.
            redirect_to_url(req, '%s/record/edit/#state=edit&recid=%s&recrev=%s' % (
                    CFG_SITE_URL, self.recid, ""))

        elif recid is not None:
            json_response.update({'recID': recid})
            # Authorize access to record.
            auth_code, auth_message = acc_authorize_action(req, 'runbibedit',
                collection=guess_primary_collection_of_a_record(recid))
            if auth_code != 0:
                json_response.update({'resultCode': 101})
                return json.dumps(json_response)

        # Handle request.
        if not ajax_request:
            # Show BibEdit start page.
            body, errors, warnings = perform_request_init(uid, argd['ln'], req, __lastupdated__)
            title = 'Record Editor'
            return page(title       = title,
                        body        = body,
                        errors      = errors,
                        warnings    = warnings,
                        uid         = uid,
                        language    = argd['ln'],
                        navtrail    = navtrail,
                        lastupdated = __lastupdated__,
                        req         = req)
        else:
            # Handle AJAX request.
            json_response.update(perform_request_ajax(req, recid, uid,
                                                      json_data))
            return json.dumps(json_response)

    def compare_revisions(self, req, form):
        """Handle the compare revisions request"""
        argd = wash_urlargd(form, { \
                'ln': (str, CFG_SITE_LANG), \
                'rev1' : (str, ''), \
                'rev2' : (str, ''), \
                'recid': (int, 0)})

        ln = argd['ln']
        uid = getUid(req)
        _ = gettext_set_language(ln)

        # Checking if currently logged user has permission to perform this request

        auth_code, auth_message = acc_authorize_action(req, 'runbibedit')
        if auth_code != 0:
            return page_not_authorized(req=req, referer="/edit",
                                       text=auth_message, navtrail=navtrail)
        recid = argd['recid']
        rev1 = argd['rev1']
        rev2 = argd['rev2']
        ln = argd['ln']

        body, errors, warnings = perform_request_compare(ln, recid, rev1, rev2)

        return page(title = _("Comparing two record revisions"),
                    body =  body,
                    errors = errors,
                    warnings = warnings,
                    uid = uid,
                    language = ln,
                    navtrail    = navtrail,
                    lastupdated = __lastupdated__,
                    req         = req)

    def new_ticket(self, req, form):
        """handle a edit/new_ticket request"""
        argd = wash_urlargd(form, {'ln': (str, CFG_SITE_LANG), 'recid': (int, 0)})
        ln = argd['ln']
        _ = gettext_set_language(ln)
        auth_code, auth_message = acc_authorize_action(req, 'runbibedit')
        if auth_code != 0:
            return page_not_authorized(req=req, referer="/edit",
                                       text=auth_message, navtrail=navtrail)
        uid = getUid(req)
        if argd['recid']:
            (errmsg, url) = perform_request_newticket(argd['recid'], uid)
            if errmsg:
                return page(title       = _("Failed to create a ticket"),
                            body        = _("Error")+": "+errmsg,
                            errors      = [],
                            warnings    = [],
                            uid         = uid,
                            language    = ln,
                            navtrail    = navtrail,
                            lastupdated = __lastupdated__,
                            req         = req)
            else:
                #redirect..
                redirect_to_url(req, url)

    def __call__(self, req, form):
        """Redirect calls without final slash."""
        if self.recid:
            redirect_to_url(req, '%s/record/%s/edit/' % (CFG_SITE_URL,
                                                         self.recid))
        else:
            redirect_to_url(req, '%s/record/edit/' % CFG_SITE_URL)
