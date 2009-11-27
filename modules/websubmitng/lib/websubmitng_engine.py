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

"""
WebSubmit NG Engine module.
"""

from invenio.textutils import encode_for_xml
import os

from invenio.config import CFG_ETCDIR

if sys.hexversion < 0x2060000:
    try:
        import simplejson as json
    except ImportError:
        # Okay, no Ajax app will be possible, but continue anyway,
        # since this package is only recommended, not mandatory.
        pass
else:
    import json

class WebSubmitStatus(object):
    INIT = 'INIT'
    INTERFACE = 'INTERFACE'
    WORKFLOW = 'WORKFLOW'
    ERROR = 'ERROR'
    DONE = 'DONE'

def python2xml(obj, indent=0):
    if not indent:
        out = '<?xml version="1.0"?>\n'
    else:
        out = ''
    if isinstance(obj, (str, int, long, float, bool, type(None))):
        out += "%s<value>\n" % (" " * indent)
        out += "%s%s\n" % (" " * (indent + 4), encode_for_xml(str(obj)))
        out += "%s</value>\n" % (" " * indent)
        return out
    elif isinstance(obj, (tuple, list)):
        out += "%s<list>\n" % (" " * indent)
        for value in obj:
            out += python2xml(value, indent + 4)
        out += "%s</list>\n" % (" " * indent)
        return out
    elif isinstance(obj, dict):
        out += "%s<map>\n" % (" " * indent)
        for key, value in obj.iteritems():
            out += '%s<key value="%s">\n' % (" " * (indent + 4), encode_for_xml(key, quote=True))
            out += python2xml(value, indent + 8)
            out += "%s</key>\n" % (" " * (indent + 4))
        out += "%s</map>\n" % (" " * indent)
        return out
    raise TypeError("%s is of type %s which can't be handled" % (repr(obj), type(obj)))

class WebSubmitSubmission(object):
    def __init__(self, session):
        self.__session = session
        pass

    def get

class WebSubmitSession(dict):
    def __init__(self, path):
        self.path = path
        self.curdir = os.path.dirname(path)
        self.session = os.path.basename(path)
        os.makedirs(self.__curdir)
        self.load()
        super.__setitem__(self, '__curdir__', self.curdir)
        super.__setitem__(self, '__session__', self.session)
        self.dump()

    def __setitem__(self, key, value):
        super.__setitem__(self, key, value)
        try:
            self.dump()
        except TypeError, err:
            super.__deitem__(self, key)
            raise

    def dump(self):
        json.dump(self, open(self.path, 'w'), indent=4)

    def load(self):
        if os.path.exists(self.path):
            self.update(json.load(open(self.path)))

    def export_to_xml(self):
        out = """<?xml version="1.0"?>
<!DOCTYPE map SYSTEM "%s">
""" % (os.path.join(CFG_ETCDIR, "websubmitng", "session.dtd"))