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
from datetime import datetime
from tempfile import mkdtemp
from time import strftime
from uuid import uuid4
from glob import glob
import tarfile
import os
import shutil
import fcntl
import sys
import cPickle

from invenio.textutils import encode_for_xml
from invenio.config import CFG_ETCDIR, CFG_PREFIX
from invenio.dbquery import run_sql
from invenio.configobj import ConfigObj
from websubmitng_elements import *
from websubmitng_fields import *
from websubmitng_callables import *

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
CFG_WEBSUBMITNG_VARDIR = os.path.join(CFG_PREFIX, 'var', 'data', 'submitng')
def python2xml(obj, indent=0):
    """
    <?xml version="1.0"?>
    <map>
        <key name="authors">
            <list>
                <value>
                    <list>
                        <value>Kaplun, Samuele</value>
                        <value>CERN</value>
                    </list>
                </value>
                <value>
                    <list>
                        <value>Caffaro, Jerome</value>
                        <value>CERN</value>
                    </list>
                </value
            </list>
        </key>
        <key name="abstract">
            <value>
                the foo and the bar
            </value>
        </key>
        <key name="date">
            <value>
                2000/02/32
            </value>
        </key>
    </map>
    """

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
            out += '%s<key value="%s">\n' % (" " * (indent + 4), encode_for_xml(key))
            out += python2xml(value, indent + 8)
            out += "%s</key>\n" % (" " * (indent + 4))
        out += "%s</map>\n" % (" " * indent)
        return out
    raise TypeError("%s is of type %s which can't be handled" % (repr(obj), type(obj)))

def unserializable_object(object):
    return "This object is not JSON Serializable."


class WebSubmitSession(dict):
    def __init__(self, doctype, session_id=None):
        self.__session_id = session_id
        self.__doctype = doctype
        if self.__session_id is None:
            self.create_session(doctype)
        self.__curdir = os.path.join(CFG_WEBSUBMITNG_VARDIR, doctype, str(self.__session_id))
        self.__session_json = os.path.join(self.__curdir, 'session.json')
        self.__session_pickled = os.path.join(self.__curdir, 'session.pickled')
        self.__aliases = []
        wfe = self.load()
        self.dump(wfe)

    #def __setitem__(self, key, value):
    #    wfe = self.load()
    #    dict.__setitem__(self, key, value)
    #    session = wfe.getObjects().next()[1]
    #We can get, but, how to set the session object in wfe?
    #    try:
    #        self.dump(wfe)
    #    except TypeError as err:
    #        dict.__delitem__(self, key)
    #        raise Exception("TypeError has occured in WebSubmitSession: " + str(err))

    #def __setattr__(self, name, value):
    #    dict.__dict__[name] = value
    #    if name.startswith('__'):
    #        self["%s__" % name] = value

    #session.__foo = 'bar' -> session['__foo__'] = 'bar'
    #session['foo'] = 'bar'

    def dump(self, wfe):
        """
        Method to dump the workflow engine.
        """
        if wfe != None:
            session_json_file = open(self.__session_json, 'w')
            session_pickled_file = open(self.__session_pickled, 'w')
            fcntl.lockf(session_json_file.fileno(), fcntl.LOCK_EX)
            fcntl.lockf(session_pickled_file.fileno(), fcntl.LOCK_EX)
            try:
                json.dump(wfe, session_json_file, indent=4, default=unserializable_object)
                cPickle.dump(wfe, session_pickled_file)
            finally:
                fcntl.lockf(session_json_file.fileno(), fcntl.LOCK_UN)
                fcntl.lockf(session_pickled_file.fileno(), fcntl.LOCK_UN)
                session_json_file.close()
                session_pickled_file.close()

    def load(self):
        """
        Method to load the workflow engine and return it.
        Session is updated if there is a  session object in the engine.
        """
        wfe = None
        if os.path.exists(self.__session_pickled):
            session_pickled_file = open(self.__session_pickled)
            fcntl.lockf(session_pickled_file.fileno(), fcntl.LOCK_SH)
            try:
                wfe = cPickle.load(session_pickled_file)
                self.update(wfe.getObjects().next()[1])
            except StopIteration:
                pass
            finally:
                fcntl.lockf(session_pickled_file.fileno(), fcntl.LOCK_UN)
                session_pickled_file.close()
        elif os.path.exists('%s.tar.bz2' % self.__curdir):
            raise InvenioWebSubmitNGSessionError("Session %s for doctype %s has already been closed" %
                                                 (str(self.__session_id), self.__doctype))
        return wfe

    def create_session(self, doctype):
        path = os.path.join(CFG_WEBSUBMITNG_VARDIR, doctype)
        self.__session_id = uuid4()
        self.__curdir = os.path.join(path, str(self.__session_id))
        os.makedirs(self.__curdir)

    # The two methods below are not being used currently.
    def add_alias(self, alias):
        if alias not in self.__aliases:
            self.__aliases.append(alias)
            alias_path = os.path.join(CFG_WEBSUBMITNG_VARDIR, self.doctype, '%s_%s' %
                                      (alias_path, str(self.__session_id)))
            os.symlink(self.__curdir, alias_path)

    def close_session(self):
        the_tar = tarfile.open("%s.tar.bz2" % self.__curdir, 'w:bz2', dereference=False)
        the_tar.add(self.__curdir)
        the_tar.close()
        shutil.rmtree(self.__curdir, ignore_errors=True)
        for alias in self.__aliases:
            try:
                os.remove(alias)
            except:
                register_exception(user_info=self['user_info']) #?
            alias_path = os.path.join(CFG_WEBSUBMITNG_VARDIR, self.doctype, '%s_%s' %
                                      (alias_path, str(self.__session_id)))
            os.symlink('%s.tar.bz2' % self.__curdir, '%s.tar.bz2' % alias_path)

    def get_session_id(self):
        return self.__session_id

    session_id = property(get_session_id)

#Not currently using the two classes below.
class InvenioWebSubmitValuesError(Exception):
    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return 'ERRORS: %s.' % ', '.join(errors)

class InvenioWebSubmitValueError(Exception):
    pass

class WebSubmitSubmission(object):

    def __init__(self, doctype, session):
        self.__interfaces = {}
        self.__workflows = {}
        self._load(doctype, session)

    #def get_session(self, cookie):
    #    return self.__session_loader(cookie)

    #def get_next_step(self, session):
    #    pass

    #def _load_session_loader(self, parser):
    #    session_type = parser.defaults().get('session_type', 'default')
    #    if session_type == 'default':
    #        self.__session_loader = WebSubmitSession
    #    else:
    #        raise NotImplemented

    def _load(self, doctype, session):
        """
        ConfigObj to load the .ini file corresponding to the doctype as a dictionary.
        Use the dictionary to load the sections corresponding to the
        interfaces and the workflows.

        Code corresponding to loading any other sections that can be specified
        in the .ini configuration files can be included in this method.
        """
        doctype_file = os.path.join(CFG_ETCDIR, 'websubmitng', doctype + '.ini') # doctype_file should be a .ini file.
        config = {}
        try:
            # file_error is set to true so that IOError is raised if the file is not found.
            # 'infile' parameter needn't necessarily be a file for ConfigObj. However, we are
            # dealing only with config 'files', and thus, only 'files' are accepted.
            config = ConfigObj(infile=doctype_file, file_error=True)
        except IOError as err:
            raise Exception("IOError has occured: " + str(err) +
                            "   Path: " + str(os.path.abspath('')))
        except SyntaxError as err:
            raise Exception("Syntax error: " + str(err))

        for (key, value) in config.iteritems():
            if key.startswith('interface') and isinstance(value, dict) and value:
                self.__interfaces[key] = self._load_interface(key, value, session)
            elif key.startswith('workflow') and isinstance(value, dict) and value:
                self.__workflows[key] = self._load_workflow(key, value)

    def _load_interface(self, key, interface_as_dict, session):
        interface = WebSubmitInterface('', '', key)
        for (interface_key, interface_value) in interface_as_dict.items():

            if interface_key.startswith('description') and interface_value:
                interface.description = interface_value

            elif interface_key.startswith('fields') and interface_value:
                for (field_key, field_value) in interface_value.items():

                    if field_key.startswith('table'):
                        header = None
                        rows = []
                        for (table_row_key, table_row_value) in field_value.items():
                            if table_row_key.startswith('header'):
                                header = table_row_value.values()
                            if table_row_key.startswith('row'):
                                row = []
                                for (row_element_key, row_element_value) in \
                                    table_row_value.items():
                                    row.append(self.get_element_object
                                               (row_element_key, row_element_value, session))
                                rows.append(row)
                        t = Table(rows, header)
                        interface.append(t)

                    elif field_key.startswith('fieldset'):
                        legend = ''
                        elements = []
                        for (element_key, element_value) in field_value.items():
                            if element_key == 'legend':
                                legend = element_value
                                continue
                            elements.append(self.get_element_object
                                            (element_key, element_value, session))
                        f = Fieldset(legend, elements)
                        interface.append(f)

                    else:
                        e = self.get_element_object(field_key, field_value, session)
                        interface.append(e)
            elif interface_key.startswith('checks') and interface_value:
                pass

        return interface

    def get_element_object(self, key, value, session):
        """
        Append the name of the element(key) and the session to the input string(value),
        evaluate it and return the element object.
        """
        value_string = value
        while value_string[-1] in [')',',',' ']:
            value_string = value_string[:-1]
        value_string += ", name='" + key + "', session=session)"
        obj = eval(value_string)
        return obj

    def _load_workflow(self, key, workflow_as_dict):
        for (workflow_key, workflow_value) in workflow_as_dict.items():
            self.__workflows[workflow_key] = eval(workflow_value)

    def get_interfaces(self):
        return self.__interfaces

    def get_workflows(self):
        return self.__workflows

    interfaces = property(get_interfaces)
    workflows = property(get_workflows)
