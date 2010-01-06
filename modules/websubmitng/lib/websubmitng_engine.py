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
from ConfigParser import SafeConfigParser
from datetime import datetime
from tempfile import mkdtemp
from time import strftime
from uuid import uuid4
from glob import glob
import tarfile
import os
import shutil
import fcntl

from invenio.textutils import encode_for_xml
from invenio.webpage import page
from invenio.config import CFG_ETCDIR
from invenio.dbquery import run_sql

if sys.hexversion < 0x2060000:
    try:
        import simplejson as json
    except ImportError:
        # Okay, no Ajax app will be possible, but continue anyway,
        # since this package is only recommended, not mandatory.
        pass
else:
    import json

CFG_WEBSUBMITNG_ETCDIR = os.path.join(CFG_ETCDIR, 'websubmitng')

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

class WebSubmitSession(dict):
    def __init__(self, doctype, session_id=None):
        self.__session_id = session_id
        self.__doctype = doctype
        if self.__session is None:
            self.create_session()
        self.__curdir = os.path.join(CFG_WEBSUBMITNG_DIR, doctype, self.__session_id)
        self.__session_path = os.path.join(self.__curdir, 'session.json')
        self.__aliases = []
        self.load()
        self.dump()

    def __setitem__(self, key, value):
        super.__setitem__(self, key, value)
        try:
            self.dump()
        except TypeError, err:
            super.__deitem__(self, key)
            raise

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if name.startswith('__'):
            self["%s__" % name] = value

    def dump(self):
        if self.__status == 'PACKED':
            raise InvenioWebSubmitNGSessionError("Session %s for doctype %s has already been packed" % (self.__session_id, self.__doctype))
        else:
            session_file = open(self.__session_path), 'w')
            fcntl.lockf(session_file.fileno(), fcntl.LOCK_EX)
            try:
                json.dump(self, session_file, indent=4)
            finally:
                fcntl.lockf(session_file.fileno(), fcntl.LOCK_UN)

    def load(self):
        if os.path.exists(self.__session_path):
            session_file = open(self.__session_path)
            fcntl.lockf(session_file.fileno(), fcntl.LOCK_SH)
            try:
                self.update(json.load(session_file.read()))
            finally:
                fcntl.lockf(session_file.fileno(), fcntl.LOCK_UN)
        elif os.path.exists('%s.tar.bz2' % self.__curdir):
            raise InvenioWebSubmitNGSessionError("Session %s for doctype %s has already been closed" % (self.__session_id, self.__doctype))

    def create_session(self, doctype):
        path = os.path.join(CFG_WEBSUBMIT_DIR, doctype)
        self.__session_id = uuid.uuid4()
        self.__curdir = os.path.join(path, self.__session_id)
        os.makedirs(path)
        self.__status = 'NEW'

    def get_status(self):
        return self.__status

    def add_alias(self, alias):
        if alias not in self.__aliases:
            self.__aliases.append(alias)
            alias_path = os.path.join(CFG_WEBSUBMITNG_DIR, self.doctype, '%s_%s' % (alias_path, self.__session_id))
            os.symlink(self.__curdir, alias_path)

    def close_session(self):
        self.__status = 'CLOSED'
        the_tar = tarfile.open("%s.tar.bz2" % self.__curdir, 'w:bz2', dereference=False)
        the_tar.add(self.__curdir)
        the_tar.close()
        shutil.rmtree(self.__curdir, ignore_errors=True)
        for alias in self.__aliases:
            try:
                os.remove(alias)
            except:
                register_exception(user_info=self['user_info'])
            alias_path = os.path.join(CFG_WEBSUBMITNG_DIR, self.doctype, '%s_%s' % (alias_path, self.__session_id))
            os.symlink('%s.tar.bz2' % self.__curdir, '%s.tar.bz2' % alias_path)
        self.__status = 'PACKED'

    status = property(get_status)

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
                element_name = element.name
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

    def check_values(self):
        errors = []
        for element in self:
            try:
                element.check_value()
            except InvenioWebSubmitValueError, err:
                errors.append(err)
        if errors:
            raise InvenioWebSubmitValuesError(errors)
        return True

    def get_recstruct(self):
        recstruct = {}
        for element in self:
            recstruct.update(element.get_recstruct())
        return recstruct

    def get_simple_xml(self):
        out = '<?xml version="1.0"?>\n'



class InvenioWebSubmitValuesError(Exception):
    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return 'ERRORS: %s.' % ', '.join(errors)

class InvenioWebSubmitValueError(Exception):
    pass

class WebSubmitInterfaceElement(object):
    def __init__(self, name, session):
        self.__name = name,
        self.__user_info = session['user_info']
        self.__session = session
        self.__value = None
        self.__marc_field = marc_field

    def get_html(self):
        raise NotImplemented()

    def get_js():
        raise NotImplemented()
    get_js = staticmethod(get_js)

    def get_css():
        raise NotImplemented()
    get_css = staticmethod(get_css)

    def get_value(self):
        return self.__value

    def get_name(self):
        return self.__name

    def get_recstruct(self):
        return {}

    def check_value(self):
        return true

    def get_value_as_xml_snippet(self):
        return python2xml(self.__value, indent=8)

    value = property(get_value)
    name = property(get_name)

class WebSubmitSubmission(object):
    def __init__(self, doctype):
        self.__doctype = doctype
        self.__interfaces = {}
        self.__worflows = {}
        self.__parser = None
        self._load()

    def get_session(self, cookie):
        return self.__session_loader(cookie)

    def get_next_step(self, session):


    def _load(self):
        parser = SafeConfigParser()
        parser.read(os.path.join(CFG_WEBSUBMITNG_ETCDIR, '%s.conf' % self.doctype))
        if parser.has_section('include'):
            self._load_includes(parser)
        if 'session_type' in parser.defaults():
            self._load_session_loader(parser)
        for section in parser.sections():
            if section.startswith('interface'):
                self._load_interface(parser, section)
            elif section.startswith('worflow'):
                self._load_workflow(parser, section)

    def _load_includes(self, parser):
        for field, value in parser.items('include'):
            if field == 'file':
                path = os.path.join(CFG_WEBSUBMITNG_ETCDIR, '%s.conf' % value)
                if path != os.path.abspath(path) or not os.path.exists(path):
                    raise ConfigParser('value %s specified for field "file" in section "include" does not correspond to a valid name under %s' % (repr(value), CFG_WEBSUBMITNG_ETCDIR))
                parser.read(path)

    def _load_session_loader(self, parser):
        session_type = parser.defaults().get('session_type', 'default')
        if session_type == 'default':
            self.__session_loader = WebSubmitSession
        else:
            raise NotImplemented

    def _load_interface(self, parser, section):
        try:
            interface_type = parser.get(section, 'type')
        except NoOptionError:
            interface_type = 'default'
        if interface_type == 'default':
            self.__interfaces[section] = WebSubmitInterface(parser, section)
        else:
            raise NotImplemented

    def _load_workflow(self, parser, section):
        try:
            worflow_type = parser.get(section, 'type')
        except NoOptionError:
            worflow_type = 'default'
        if worflow_type == 'default':
            self.__workflows[section] = WebSubmitWorkflow(parser, section)
        else:
            raise NotImplemented

class WebSubmitConfigParser(SafeConfigParser):
