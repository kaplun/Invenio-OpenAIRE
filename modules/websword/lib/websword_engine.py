# -*- coding: utf-8 -*-

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

import tempfile
import time
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

from invenio.config import CFG_TMPDIR
from invenio.datetime

def is_dry_run_request(req):
    """
    @return: True if the current request is a dry_run (or No-Op) request.
    @see: section 3.1 in http://www.swordapp.org/docs/sword-profile-1.3.html
    """
    return req.headers_in.get("X-No-Op", "false").lower() == 'true'

def is_verbose_request(req):
    """
    @return: True if the current request should be handled verbosely.
    @see: section 3.2 in http://www.swordapp.org/docs/sword-profile-1.3.html
    """
    return req.headers_in.get("X-Verbose", "false").lower() == 'true'

def get_on_behalf_of(req):
    """
    @return: uid of the user on behalf of which this deposition is performed.
    @see: section 2 in http://www.swordapp.org/docs/sword-profile-1.3.html
    @raise: ValueError if the user is not known.
    """
    user = req.headers_in.get("X-On-Behalf-Of", None)
    if user is None:
        return
    elif user.isdigit() and run_sql("SELECT id FROM user WHERE id=%s", (user, )):
        return int(user)
    uid = run_sql("SELECT id FROM user WHERE email=%s OR nickname=%s" % (user, user))
    if uid:
        return uid[0][0]
    raise ValueError("Unknown user %s specified in X-On-Behalf-Of header" % repr(user))

def sword_session_gc():
    run_sql()

class SwordSession(object):
    def __init__(self):


def create_sword_session(info):
    session = tempfile.mkdtemp(dir=CFG_TMPDIR, prefix="sword-session-%s" % time.strftime("%Y-%m-%d_%H:%M:%S"))
    open(os.path.join(session, '.info'), 'w').write()


def get_sword_service_description(req):

def create_error_document()