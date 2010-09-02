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

import os
import shutil
import tempfile
import json

from datetime import datetime

from invenio.bibedit import json_unicode_to_utf8
from invenio.webpage import page as invenio_page
from invenio.webinterface_handler import wash_urlargd
from invenio.webuser import session_param_set, session_param_get, session_param_list, collect_user_info
from invenio import template
from invenio.config import CFG_SITE_LANG, CFG_SITE_URL, CFG_WEBSUBMIT_STORAGEDIR

CFG_OPENAIRE_DEPOSIT_PATH = os.path.join(CFG_WEBSUBMIT_STORAGEDIR, 'OpenAIRE')

openaire_deposit_templates = template.load('openaire_deposit')

def portal_page(title, body, navtrail="", description="", keywords="",
         metaheaderadd="", uid=None,
         cdspageheaderadd="", cdspageboxlefttopadd="",
         cdspageboxleftbottomadd="", cdspageboxrighttopadd="",
         cdspageboxrightbottomadd="", cdspagefooteradd="", lastupdated="",
         language=CFG_SITE_LANG, verbose=1, titleprologue="",
         titleepilogue="", secure_page_p=0, req=None, errors=[], warnings=[], navmenuid="admin",
         navtrail_append_title_p=1, of="", rssurl=CFG_SITE_URL+"/rss", show_title_p=True,
         body_css_classes=None):
    if req is not None:
        user_info = collect_user_info(req)
        username = user_info.get('EXTERNAL_username', user_info['email'])
        logout_key = user_info.get('EXTERNAL_logout_key', '')
    else:
        username = 'Guest'
        logout_key = ''
    return openaire_deposit_templates.tmpl_page(title=title, body=body, headers=metaheaderadd, username=username, logout_key=logout_key, ln=language)

def page(title, body, navtrail="", description="", keywords="",
         metaheaderadd="", uid=None,
         cdspageheaderadd="", cdspageboxlefttopadd="",
         cdspageboxleftbottomadd="", cdspageboxrighttopadd="",
         cdspageboxrightbottomadd="", cdspagefooteradd="", lastupdated="",
         language=CFG_SITE_LANG, verbose=1, titleprologue="",
         titleepilogue="", secure_page_p=0, req=None, errors=[], warnings=[], navmenuid="admin",
         navtrail_append_title_p=1, of="", rssurl=CFG_SITE_URL+"/rss", show_title_p=True,
         body_css_classes=None):
    if req is not None:
        form = req.form
        argd = wash_urlargd(form, {'style': (str, '')})
        style = argd['style']
        if style in ('portal', 'invenio'):
            session_param_set(req, 'style', style)
        else:
            try:
                style = session_param_get(req, 'style')
            except KeyError:
                style = 'invenio'
                session_param_set(req, 'style', 'invenio')
    else:
        style = 'invenio'
    if not metaheaderadd:
        metaheaderadd = openaire_deposit_templates.tmpl_headers()
    body = """<noscript>
            <strong>WARNING: You must enable Javascript in your browser (or you must whitelist this website in the Firefox NoScript plugin) in order to properly deposit a publication into the OpenAIRE Orphan Record Repository.</strong>
        </noscript>
        """ + body
    if style == 'portal':
        return portal_page(title, body, navtrail, description, keywords,
            metaheaderadd, uid,
            cdspageheaderadd, cdspageboxlefttopadd,
            cdspageboxleftbottomadd, cdspageboxrighttopadd,
            cdspageboxrightbottomadd, cdspagefooteradd, lastupdated,
            language, verbose, titleprologue,
            titleepilogue, secure_page_p, req, errors, warnings, navmenuid,
            navtrail_append_title_p, of, rssurl, show_title_p,
            body_css_classes)
    else:
        return invenio_page(title, body, navtrail, description, keywords,
            metaheaderadd, uid,
            cdspageheaderadd, cdspageboxlefttopadd,
            cdspageboxleftbottomadd, cdspageboxrighttopadd,
            cdspageboxrightbottomadd, cdspagefooteradd, lastupdated,
            language, verbose, titleprologue,
            titleepilogue, secure_page_p, req, errors, warnings, navmenuid,
            navtrail_append_title_p, of, rssurl, show_title_p,
            body_css_classes)

class OpenAIREPublications(dict):
    def __init__(self, uid, projectid):
        super.__init__(self)
        self.uid = uid
        self.projectid = projectid
        self.path = os.path.join(CFG_OPENAIRE_DEPOSIT_PATH, str(uid), str(projectid))
        self.errors = []
        self.warnings = []
        self._initialize_storage()
        self._load()

    def _initialize_storage(self):
        os.makedirs(self.path)

    def _load(self):
        for publicationid in os.listdir(self.path):
            self[publicationid] = OpenAIREPublication(self.uid, self.projectid, publicationid)
            if self[publicationid].errors:
                self.errors.append(publicationid)
            if self[publicationid].warnings:
                self.warnings.append(publicationid)

    def upload_several_files(self, form):
        for afile in form[files]:
            the_directory = tempfile.mkdtemp(dir=self.path, prefix='')
            publicationid = os.path.basename(the_directory)
            publication = self[publicationid] = OpenAIREPublication(self.uid, self.projectid, publicationid)
            publication.add_a_fulltext(afile.file.name, afile.filename)
            if publication.warnings:
                self.warnings.append(publicationid)
            if publication.errors:
                self.errors.append(publicationid)

class OpenAIREPublication(object):
    def __init__(self, uid, projectid, publicationid):
        self.uid = uid
        self.projectid = projectid
        self.publicationid = publicationid
        self.path = os.path.join(CFG_OPENAIRE_DEPOSIT_PATH, str(uid), str(projectid), str(publicationid))
        self.fulltext_path = os.path.join(self.path, 'files')
        self.metadata_path = os.path.join(self.path, 'metadata')
        self._initialize_storage()
        self.fulltexts = {}
        self.warnings = []
        self.errors = []
        self._load()

    def __del__(self):
        self._dump()

    def _initialize_storage(self):
        os.makedirs(os.path.join(self.path, 'files'))

    def _load(self):
        self._load_metadata()
        self._load_fulltext_info()

    def _load_metadata(self):
        try:
            self.metadata = json_unicode_to_utf8(json.load(open(os.path.join(self.path, 'metadata'))))
            self.md = datetime.fromtimestamp(os.path.getmtime(os.path.join(self.path, 'metadata')))
            try:
                self.cd = datetime.fromtimestamp(os.path.getctime(os.path.join(self.path, 'metadata')))
            except OSError:
                self.cd = self.md
        except:
            self.metadata = {}
            self._dump_metadata()
            self._load_metadata()

    def _load_fulltexts():
        for fulltextid in os.listdir(self.fulltext_path):
            if not fulltextid.startswith('.') and os.path.isdir(os.path.join(self.fulltext_path, fulltextid)):
                for filename in os.listdir(os.path.join(self.fulltext_path, fulltextid)):
                    if not filename.startswith('.'):
                        self.fulltexts[fulltextid] = generic_path2bidocfile(os.path.join(self.fulltext_path, fulltextid, filename))

    def add_a_fulltext(self, original_path, filename):
        the_directory = tempfile.mkdtemp(prefix='', dir=self.fulltext_path)
        fulltextid = os.path.basename(the_directory)
        final_path = os.path.join(the_directory, os.path.basename(filename))
        shutil.copy2(original_path, final_path)
        self.fulltexts[fulltextid] = generic_path2bidocfile(final_path)
        return fulltextid

    def _dump(self):
        self._dump_metadata()

    def _dump_metadata(self):
        json.dump(self.metadata, open(os.path.join(self.path, 'metadata'), 'w'), indent=4)

    def merge_form(form):
        self.metadata['__form__'] = {}
        for key, values in form.iteritems():
            if key.startswith('%s_' % self.publicationid):
                key = key[len('%s_' % self.publicationid):]
                ## We consider only form elements related to this publication
                self.metadata['__form__'][key] = []
                for value in values:
                    if value.filename is not None:
                        ## we are handling a file
                        fulltextid = self.add_a_fulltext(value.file.name, value.filename)
                        self.metadata['__form__'][key].append(fulltextid)
                    else:
                        self.metadata['__form__'][key].append(value)




