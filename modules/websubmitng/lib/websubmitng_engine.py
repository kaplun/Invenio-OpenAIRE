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

from cgi import escape
import os

from invenio.textutils import encode_for_xml
from invenio.webpage import page
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

class WebSubmitInterface(list):
    def __init__(self, user_info, session, title=None, description=None):
        self.user_info = user_info
        self.session = session

    def get_full_page(self, req):
        return page(req=req, title=self.title, description=self.description)

    def get_html(self):
        out = '<table class="websubmitng_form"><tbody>\n'
        for element in self:
            out += '  <tr>\n'
            if element.expects_default_label_usage():
                out += '    <td class="websubmitng_label">\n'
                element_name = element.get_name()
                label = element.get_label()
                out += '      <label for="%s">%s</label>\n' % (escape(element_name, True), label)
                out += '    </td>\n'
                out += '    <td class="websubmitng_element">\n'
                out += element.get_html()
                out += '    </td>\n'
            else:
                out += '    <td class="websubmitng_element" colspan="2">\n'
                out += element.get_html()
                out += '    </td>\n'
            out += '  <tr>\n'
        out += '</tbody></table>\n'
        return out

    def get_js(self):
        out = ""
        classes = []
        for element in self:
            element_class = type(element)
            if element_class not in classes:
                out += element.get_js()
                classes.append(element_class)
        return out

    def get_css(self):
        out = ""
        classes = []
        for element in self:
            element_class = type(element)
            if element_class not in classes:
                out += element.get_css()
                classes.append(element_class)
        return out

