# -*- coding: utf-8 -*-
## This file is part of Invenio.
## Copyright (C) 2011 CERN.
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
oai_repository_server_ctxo.py -- utilities to implement the Knowledge Exchange
protocol to export usage statistics over OAI-PMH.
"""

if sys.hexversion < 0x2060000:
    from md5 import md5
else:
    from hashlib import md5

from invenio.config import CFG_SITE_URL, CFG_USER_CLASSIFICATION, CFG_OAI_ID_FIELD
from invenio.htmlutils import X

CFG_ROBOTSLIST_URL = "http://purl.org/robotslist/current/robotlist.xml"
_ROBOTS_REGEX_RE = re.compile(r"<regEx>(.*?)</regEx>")
_ROBOTSLIST_CACHE = os.path.join(CFG_CACHEDIR, 'robotlist.xml')
_ONE_DAY = 24 * 60 * 60

CFG_SERVICE_TYPES = ('objectFile', 'descriptiveMetadata')

_ROBOTSLIST_RE = None
def get_robotlist_re(fresh=False):
    """
    Return a compiled regular expression to match all robot user agent as per:
    <http://purl.org/robotslist/current/robotlist.xml>
    """
    global _ROBOTSLIST_RE
    if not fresh and _ROBOTSLIST_RE:
        return _ROBOTSLIST_RE
    if not os.path.exists(_ROBOTSLIST_CACHE) or (time.time() - os.path.getmtime(_ROBOTSLIST_CACHE)) > _ONE_DAY:
        try:
            robotslist = urlopen(CFG_ROBOTSLIST_URL).read()
            open(_ROBOTSLIST_CACHE, "w").write(robotslist)
        except:
            register_exception(alert_admin=True, prefix="Can't download the robot list from %s and save it into %s" % (CFG_ROBOTSLIST_URL, _ROBOTSLIST_CACHE))
    else:
        robotslist = open(_ROBOTSLIST_CACHE).read()
    agents = _ROBOTS_REGEX_RE.findall(robotslist)
    _ROBOTSLIST_RE = re.compile("|".join(agent.strip() for agent in agents))
    return _ROBOTSLIST_RE

_CFG_SALT = None
_CFG_SALT_FILE = os.path.join(CFG_ETCDIR, 'salt.txt')
def get_salt():
    global _CFG_SALT
    if CFG_SALT:
        return _CFG_SALT
    if os.path.exists(_CFG_SALT_FILE):
        _CFG_SALT = open(_CFG_SALT_FILE).read()
        return _CFG_SALT
    import uuid
    _CFG_SALT = uuid.uuid4()
    open(_CFG_SALT_FILE, "w").write(_CFG_SALT)
    return _CFG_SALT

def salt_obfuscate_ip_address(ip):
    return md5(ip + get_salt()).hexdigest()

def format_requester_identifier(ip):
    return "data:,%s" % salt_obfuscate_ip_address(ip)

def format_c_class_subnet(ip):
    subnet = '.'.join(ip.split('.')[:3] + ["0"])
    return "data:,%s" % subnet

def format_service_type(service_type):
    assert service_type in CFG_SERVICE_TYPES
    return "info:/eu-repo/semantics/" % service_type

def format_resolver_identifier():
    return CFG_SITE_URL

def format_requester_classification(uid, ip, user_agent, referer):
    from invenio.webuser import collect_user_info
    from invenio.access_control_admin import acc_is_user_in_role, acc_get_role_id
    user_info = collect_user_info(uid)
    user_info['remote_ip'] = ip
    user_info['referer'] = referer
    user_info['agent'] = user_agent
    for user_type, user_roles in CFG_USER_CLASSIFICATION:
        for role in user_roles:
            if acc_is_user_in_role(user_info, acc_get_role_id(role)):
                return user_type
    return ""

def format_requester_session(session_key):
    if session_key:
        return md5(session_key).hexdigest()
    return ""

def format_referent_identifier(recid):
    from invenio.search_engine import get_fieldvalues
    oai_ids = get_fieldvalues(recid, CFG_OAI_ID_FIELD)
    if oai_ids:
        return oai_ids[0]
    return ""

def format_timestamp(event):
    return event.strftime("%Y-%m-%dT%H:%M:%S")

def format_context_object(recid, uid, ip, session_key, user_agent, referer, url, timestamp, service_type):
    return X['context-object'](timestamp=format_timestamp(timestamp))(
        X.referent()(
            X.identifier()(url),
            X.identifier()(format_referent_identifier(recid)),
        ),
        referer and X['referring-entity']()(
            X.identifier(referer)
        ) or '',
        X.requester()(
            X['metadata-by-val']()(
                X.format()("http://dini.de/namespace/oas-requesterinfo"),
                X.metadata()(
                    X.requesterinfo(xmlns="http://dini.de/namespace/oas-requesterinfo")(
                        X["user-agent"]()(user_agent),
                        X["hashed-ip"]()(format_requester_identifier(ip)),
                        X["hashed-c"]()(format_c_class_subnet()(ip),
                        X["classification"]()(format_requester_classification(uid, ip, user_agent, referer)),
                        X["hashed-session"]()(format_requester_session(session_key)),
                    ),
                )
            )
        ),
        X['service-type'](
            X['metadata-by-val']()(
                X.format()("http://dublincore.org/documents/2008/01/14/dcmi-terms/"),
                X.metadata()(format_service_type(service_type))
            ),
            X.resolver()(
                X.identifier()(CFG_SITE_URL),
            )
        )
    )

def get_dini_requester_snippet(uid, ip, session_key, user_agent):
    formatted_ip = format_requester_identifier(ip)
    return X.requester(X.identifier()(formatted_ip))

