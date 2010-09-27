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
import time
import sys
if sys.hexversion < 0x2060000:
    try:
        import simplejson as json
    except ImportError:
        # Okay, no Ajax app will be possible, but continue anyway,
        # since this package is only recommended, not mandatory.
        pass
else:
    import json
import re
import copy

from invenio.bibdocfile import generic_path2bidocfile
from invenio.bibedit_utils import json_unicode_to_utf8
from invenio.webpage import page as invenio_page
from invenio.webinterface_handler import wash_urlargd
from invenio.webuser import session_param_set, session_param_get, collect_user_info, get_email
from invenio import template
from invenio.messages import gettext_set_language
from invenio.config import CFG_SITE_LANG, CFG_SITE_URL, CFG_WEBSUBMIT_STORAGEDIR
from invenio.websearch_webcoll import mymkdir
from invenio.dbquery import run_sql
from invenio.bibtask import task_low_level_submission
from invenio.bibrecord import record_add_field, record_xml_output
from invenio.bibknowledge import get_kb_mapping, get_kbr_keys
from invenio.search_engine import record_empty
from invenio.openaire_deposit_utils import wash_form, simple_metadata2namespaced_metadata, namespaced_metadata2simple_metadata, strip_publicationid
from invenio.urlutils import create_url
from invenio.bibformat import format_record

CFG_OPENAIRE_PROJECT_INFORMATION_KB = 'json_projects'
CFG_OPENAIRE_DEPOSIT_PATH = os.path.join(CFG_WEBSUBMIT_STORAGEDIR, 'OpenAIRE')
RE_AUTHOR_ROW = re.compile(u'^\w{2,}(\s+\w{2,})*,\s*\w{2,}\s*(:\s*\w{2,}.*)?$')
RE_PAGES = re.compile('\d+(-\d+)?')

def _(foo):
    return foo

def CFG_ACCESS_RIGHTS(ln):
    _ = gettext_set_language(ln)
    return {
        'closedAccess': _("Closed access"),
        'embargoedAccess': _("Embargoed access"),
        'restrictedAccess': _("Restricted access"),
        'openAccess': _("Open access")}

CFG_METADATA_FIELDS = ('title', 'original_title', 'authors', 'abstract',
    'original_abstract', 'language', 'access_rights', 'embargo_date',
    'publication_date', 'journal_title', 'volume', 'pages', 'issue', 'keywords')

CFG_METADATA_STATES = ('ok', 'error', 'warning', 'empty')
CFG_PUBLICATION_STATES = ('initialized', 'edited', 'submitted', 'pendingapproval', 'approved', 'rejected')

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
        username = user_info.get('nickname', user_info['email'])
        logout_key = user_info.get('EXTERNAL_logout_key', '')
    else:
        username = 'Guest'
        logout_key = ''
    return openaire_deposit_templates.tmpl_page(title=title, body=body, headers=metaheaderadd, username=username, logout_key=logout_key, ln=language)

def get_project_information_from_projectid(projectid):
    info = get_kb_mapping(CFG_OPENAIRE_PROJECT_INFORMATION_KB, str(projectid))
    if info:
        return json_unicode_to_utf8(json.loads(info['value']))
    else:
        return {}

def get_favourite_authorships_for_user(uid, projectid, term=''):
    if uid is None:
        return [row[0] for row in run_sql("SELECT DISTINCT authorship FROM OpenAIREauthorships WHERE projectid=%s and authorship LIKE %s ORDER BY authorship", (projectid, '%%%s%%' % term))]
    return [row[0] for row in run_sql("SELECT DISTINCT authorship FROM OpenAIREauthorships WHERE uid=%s and projectid=%s and authorship LIKE %s ORDER BY authorship", (uid, projectid, '%%%s%%' % term))]

def update_favourite_authorships_for_user(uid, projectid, publicationid, authorships):
    run_sql("DELETE FROM OpenAIREauthorships WHERE uid=%s AND projectid=%s and publicationid=%s", (uid, projectid, publicationid))
    for authorship in authorships.splitlines():
        run_sql("INSERT INTO OpenAIREauthorships(uid, projectid, publicationid, authorship) VALUES(%s, %s, %s, %s)", (uid, projectid, publicationid, authorship))

def normalize_authorships(authorships):
    ret = []
    for authorship in authorships.splitlines():
        authorship = authorship.split(':', 1)
        if len(authorship) == 2:
            name, affiliation = authorship
            name = ', '.join(item.strip() for item in name.split(','))
            affiliation = affiliation.strip()
            authorship = '%s: %s' % (name, affiliation)
        else:
            authorship = authorship.strip()
        ret.append(authorship)
    return '\n'.join(ret)

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
        metaheaderadd = openaire_deposit_templates.tmpl_headers(argd['ln'])
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

class OpenAIREProject(dict):
    def __init__(self, uid, projectid, ln=CFG_SITE_LANG):
        self.uid = uid
        self.projectid = projectid
        self.path = os.path.join(CFG_OPENAIRE_DEPOSIT_PATH, str(uid), str(projectid))
        self.errors = []
        self.warnings = []
        self.__ln = ln
        self._initialize_storage()
        self._load()

    def _initialize_storage(self):
        mymkdir(self.path)

    def _load(self):
        for publicationid in os.listdir(self.path):
            self[publicationid] = OpenAIREPublication(self.uid, self.projectid, publicationid)
            if self[publicationid].errors:
                self.errors.append(publicationid)
            if self[publicationid].warnings:
                self.warnings.append(publicationid)

    def delete_publication(self, publicationid):
        if publicationid in self:
            self[publicationid].delete()
            del self[publicationid]

    def upload_several_files(self, form, field='Filedata'):
        afile = form[field]
        publication = OpenAIREPublication(self.uid, self.projectid)
        publicationid = publication.publicationid
        self[publicationid] = publication
        publication.add_a_fulltext(afile.file.name, afile.filename)
        if publication.warnings:
            self.warnings.append(publicationid)
        if publication.errors:
            self.errors.append(publicationid)

    def get_project_information(self, linked=True):
        project_information = get_project_information_from_projectid(self.projectid)
        return openaire_deposit_templates.tmpl_project_information(projectid=self.projectid, ln=self.ln, existing_publications=len(self), linked=linked, **project_information)

    def get_ln(self):
        return self.__ln
    ln = property(get_ln)

def get_all_projectsids():
    """
    @return: the set of all the valid projects IDs
    @rtype: set of string
    """
    return set(project[0] for project in get_kbr_keys("projects"))

def get_exisiting_projectids_for_uid(uid):
    valid_projectsid = get_all_projectsids()
    try:
        return [name for name in os.listdir(os.path.join(CFG_OPENAIRE_DEPOSIT_PATH, str(uid))) if name in valid_projectsid]
    except OSError:
        return []

class OpenAIREPublication(object):
    def __init__(self, uid, projectid, publicationid=None, ln=CFG_SITE_LANG):
        self._metadata = {}
        self._metadata['__uid__'] = uid
        self._metadata['__projectid__'] = projectid
        self._metadata['__publicationid__'] = publicationid
        self.__ln = ln
        if publicationid is None:
            self.status = 'initialized'
            while True:
                self.path = tempfile.mkdtemp(dir=os.path.join(CFG_OPENAIRE_DEPOSIT_PATH, str(uid), str(projectid)), prefix='')
                self._metadata['__publicationid__'] = os.path.basename(self.path)
                if '_' not in self.publicationid:
                    ## We don't want '_' at all in publicationid!
                    break
                os.rmdir(self.path)
            self._metadata['__cd__'] = self._metadata['__md__'] = time.time()
            self.__touched = True
        else:
            self.__touched = False
            self.path = os.path.join(CFG_OPENAIRE_DEPOSIT_PATH, str(uid), str(projectid), str(publicationid))
            if not os.path.exists(self.path):
                raise ValueError("publicationid %s for projectid %s does not exist for user %s" % (publicationid, projectid, uid))
        self.fulltext_path = os.path.join(self.path, 'files')
        self.metadata_path = os.path.join(self.path, 'metadata')
        self.fulltexts = {}
        self.warnings = {}
        self.errors = {}
        self._initialize_storage()
        self._load()
        self.__deleted = False

    def __del__(self):
        if not self.__deleted and self.__touched:
            self._dump()

    def delete(self):
        self.__deleted = True
        shutil.rmtree(self.path)

    def _initialize_storage(self):
        mymkdir(os.path.join(self.path, 'files'))

    def _load(self):
        self._load_metadata()
        self._load_fulltexts()

    def _load_metadata(self):
        try:
            self._metadata.update(json_unicode_to_utf8(json.load(open(self.metadata_path))))
        except:
            self._dump_metadata()
            self._load_metadata()

    def _load_fulltexts(self):
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
        if os.path.exists(self.metadata_path):
            backup_fd, backup_name = tempfile.mkstemp(prefix='metadata-%s-' % time.strftime("%Y%m%d%H%M%S"), suffix='', dir=self.path)
            os.write(backup_fd, open(self.metadata_path).read())
            os.close(backup_fd)
        json.dump(self._metadata, open(self.metadata_path, 'w'), indent=4)

    def merge_form(self, form, ln=CFG_SITE_LANG):
        if self.status in ('initialized', 'edited'):
            if self.status == 'initialized':
                self.status = 'edited'
            self.touch()
            self._metadata['__form__'] = wash_form(form, self.publicationid)
            self._metadata.update(namespaced_metadata2simple_metadata(self._metadata['__form__'], self.publicationid))

    def touch(self):
        self._metadata['__md__'] = time.time()
        self.__touched = True

    def get_metadata_status(self):
        if self.errors:
            return 'error'
        if self.warnings:
            return 'warning'
        for field in CFG_METADATA_FIELDS:
            if field in self._metadata and self._metadata[field]:
                ## There is at least one field filled. Since there are no
                ## warnings or errors, that means it's OK :-)
                return 'ok'
        return 'empty'

    def upload_record(self):
        marcxml_path = os.path.join(self.path, 'marcxml')
        open(marcxml_path, 'w').write(self.marcxml)
        task_low_level_submission('bibupload', 'openaire', '-r', marcxml_path, '-P5')
        self.status = 'submitted'

    def get_publication_information(self):
        return openaire_deposit_templates.tmpl_publication_information(publicationid=self.publicationid, title=self._metadata.get('title', ""), authors=self._metadata.get('authors', ""), abstract=self._metadata.get('abstract', ""), ln=self.ln)

    def get_fulltext_information(self):
        out = ""
        for fulltextid, fulltext in self.fulltexts.iteritems():
            out += openaire_deposit_templates.tmpl_fulltext_information(filename=fulltext.fullname, publicationid=self.publicationid, download_url=create_url("%s/deposit/getfile" % CFG_SITE_URL, {'projectid': self.projectid, 'publicationid': self.publicationid, 'fileid': fulltextid}), md5=fulltext.checksum, mimetype=fulltext.mime, format=fulltext.format, size=fulltext.size, ln=self.ln)
        return out

    def get_publication_form(self):
        fileinfo = self.get_fulltext_information()
        publication_information = self.get_publication_information()
        return openaire_deposit_templates.tmpl_form(projectid=self.projectid, publicationid=self.publicationid, publication_information=publication_information, fileinfo=fileinfo, form=self._metadata.get("__form__"), metadata_status=self.metadata_status, warnings=simple_metadata2namespaced_metadata(self.warnings, self.publicationid), errors=simple_metadata2namespaced_metadata(self.errors, self.publicationid), ln=self.ln)

    def get_publication_preview(self):
        body = format_record(recID=self.recid, xml_record=self.marcxml, ln=self.ln, of='hd')
        return openaire_deposit_templates.tmpl_publication_preview(body, self.recid, ln=self.ln)


    def check_metadata(self):
        self.errors, self.warnings = self.static_check_metadata(self._metadata, ln=self.ln)
        if self._metadata.get('authors') and not self.errors.get('authors'):
            self._metadata['authors'] = normalize_authorships(self._metadata['authors'])
            update_favourite_authorships_for_user(self.uid, self.projectid, self.publicationid, self._metadata['authors'])

    def static_check_metadata(metadata, publicationid=None, check_only_field=None, ln=CFG_SITE_LANG):
        """
        Given a mapping in metadata.
        Check that all the required metadata are properly set.
        """
        _ = gettext_set_language(ln)

        if publicationid:
            metadata = namespaced_metadata2simple_metadata(metadata, publicationid)


        if check_only_field:
            ## Just one check, if it actually exist for the given field
            fieldname = strip_publicationid(check_only_field, publicationid)
            if fieldname in CFG_METADATA_FIELDS_CHECKS:
                checks = [CFG_METADATA_FIELDS_CHECKS[fieldname]]
                errors = {fieldname: []}
                warnings = {fieldname: []}
            else:
                checks = []
                errors = {}
                warnings = {}
        else:
            checks = CFG_METADATA_FIELDS_CHECKS.values()
            errors = dict((field, []) for field in CFG_METADATA_FIELDS_CHECKS)
            warnings = dict((field, []) for field in CFG_METADATA_FIELDS_CHECKS)

        for check in checks:
            ret = check(metadata, ln, _)
            if ret:
                assert(ret[1] in ('error', 'warning'))
                assert(ret[0]) in CFG_METADATA_FIELDS
                if ret[1] == 'error':
                    if ret[0] not in errors:
                        errors[ret[0]] = [ret[2]]
                    else:
                        errors[ret[0]].append(ret[2])
                elif ret[1] == 'warning':
                    if ret[0] not in warnings:
                        warnings[ret[0]] = [ret[2]]
                    else:
                        warnings[ret[0]].append(ret[2])
        for errorid, error_lines in errors.items():
            errors[errorid] = '<br />'.join(error_lines)
        for warningid, warning_lines in warnings.items():
            warnings[warningid] = '<br />'.join(warning_lines)
        if publicationid:
            errors = simple_metadata2namespaced_metadata(errors, publicationid)
            warnings = simple_metadata2namespaced_metadata(warnings, publicationid)
        return errors, warnings
    static_check_metadata = staticmethod(static_check_metadata)

    def get_ln(self):
        return self.__ln
    def get_status(self):
        if self._metadata['__status__'] == 'submitted':
            ## The record has been submitted into Invenio. Let's poll to see if it's actually there:
            if not record_empty(self.recid):
                ## FIXME: change this to pendingapproval once
                ## approval workflow is implemented.
                self._metadata['__status__'] = 'approved'
        return self._metadata['__status__']
    def set_status(self, new_status):
        assert(new_status in CFG_PUBLICATION_STATES)
        self._metadata['__status__'] = new_status
    def get_md(self):
        return self._metadata['__md__']
    def get_cd(self):
        return self._metadata['__cd__']
    def get_uid(self):
        return self._metadata['__uid__']
    def get_projectid(self):
        return self._metadata['__projectid__']
    def get_publicationid(self):
        return self._metadata['__publicationid__']
    def get_recid(self):
        if '__recid__' not in self._metadata:
            self._metadata['__recid__'] = run_sql("INSERT INTO bibrec(creation_date, modification_date) values(NOW(), NOW())")
        return self._metadata['__recid__']
    def get_metadata(self):
        return copy.deepcopy(self._metadata)
    def get_marcxml(self):
        rec = {}
        record_add_field(rec, '001', controlfield_value=str(self.recid))
        authors = [author.strip() for author in self._metadata['authors'].split('\n') if author.strip()]
        if authors:
            if ':' in authors[0]:
                name, affil = authors[0].split(':', 1)
                name = name.strip()
                affil = affil.strip()
                record_add_field(rec, '100', subfields=[('a', name), ('u', affil)])
            else:
                name = name.strip()
                record_add_field(rec, '100', subfields=[('a', name)])
            for author in authors[1:]:
                if ':' in author:
                    name, affil = author.split(':', 1)
                    name = name.strip()
                    affil = affil.strip()
                    record_add_field(rec, '700', subfields=[('a', name), ('u', affil)])
                else:
                    name = name.strip()
                    record_add_field(rec, '700', subfields=[('a', name)])
        record_add_field(rec, '041', subfields=[('a', self._metadata['language'])])
        record_add_field(rec, '245', subfields=[('a', self._metadata['title'])])
        if self._metadata['original_title']:
            record_add_field(rec, '246', subfields=[('a', self._metadata['original_title'])])
        record_add_field(rec, '520', subfields=[('a', self._metadata['abstract'])])
        if self._metadata['original_abstract']:
            record_add_field(rec, '560', subfields=[('a', self._metadata['original_abstract'])])
        if self._metadata['note']:
            record_add_field(rec, '500', subfields=[('a', self._metadata['note'])])
        record_add_field(rec, '980', subfields=[('a', 'OPENAIRE')])
        if self._metadata['publication_date']:
            record_add_field(rec, '260', subfields=[('c', self._metadata['publication_date'])])
        record_add_field(rec, '536', subfields=[('c', str(self.projectid))])
        record_add_field(rec, '856', ind1='0', subfields=[('f', get_email(self.uid))])
        if self._metadata['embargo_date']:
            record_add_field(rec, '942', subfields=[('a', self._metadata['embargo_date'])])
        for key, fulltext in self.fulltexts.iteritems():
            record_add_field(rec, 'FFT', subfields=[('a', fulltext.fullpath)])
        subfields = []
        if self._metadata['journal_title']:
            subfields.append(('p', self._metadata['journal_title']))
        if self._metadata['publication_date']:
            year = self._metadata['publication_date'][:4]
            subfields.append(('y', year))
        if self._metadata['issue']:
            subfields.append(('n', self._metadata['issue']))
        if self._metadata['pages']:
            subfields.append(('c', self._metadata['pages']))
        if subfields:
            record_add_field(rec, '909', 'C', '4', subfields=subfields)
        return record_xml_output(rec)

    ln = property(get_ln)
    status = property(get_status, set_status)
    md = property(get_md)
    cd = property(get_cd)
    uid = property(get_uid)
    projectid = property(get_projectid)
    publicationid = property(get_publicationid)
    recid = property(get_recid)
    metadata = property(get_metadata)
    metadata_status = property(get_metadata_status)
    marcxml = property(get_marcxml)


def _check_title(metadata, ln, _):
    title = metadata.get('title', '')
    title = title.strip()
    if not title:
        return ('title', 'error', _('The title field of the Publication is mandatory but is currently empty'))
    elif title:
        title = title.decode('UTF8')
        uppers = 0
        for c in title:
            if c.isupper():
                uppers += 1
        if 1.0 * uppers / len(title) > 0.75:
            return ('title', 'warning', _('The title field of the Publication seems to be written all in UPPERCASE'))

def _check_original_title(metadata, ln, _):
    title = metadata.get('original_title', '')
    title = title.decode('UTF8')
    if title:
        uppers = 0
        for c in title:
            if c.isupper():
                uppers += 1
        if 1.0 * uppers / len(title) > 0.75:
            return ('original_title', 'warning', _('The original title field of the Publication seems to be written all in UPPERCASE'))

def _check_authors(metadata, ln, _):
    authors = metadata.get('authors', '')
    authors = authors.decode('UTF8')
    if not authors.strip():
        return ('authors', 'error', _('The authorship of the Publication is a mandatory field but is currently empty'))
    for row in authors.split('\n'):
        row = row.strip()
        if row:
            if not RE_AUTHOR_ROW.match(row):
                return ('authors', 'error', _('"%(row)s" is not a well formatted authorship') % {"row": row})

def _check_abstract(metadata, ln, _):
    abstract = metadata.get('abstract', '')
    if not abstract.strip():
        return ('abstract', 'error', _('The abstract of the Publication is a mandatory field but is currently empty'))

def _check_language(metadata, ln, _):
    language = metadata.get('language', '')
    if not language.strip():
        return ('language', 'error', _('The language of the Publication is a mandatory field but is currently empty'))

def _check_access_rights(metadata, ln, _):
    access_rights = metadata.get('access_rights', '')
    if not access_rights in CFG_ACCESS_RIGHTS(ln):
        return ('access_rights', 'error', _('The access rights field of the Publication is not set to one of the expected values'))

def _check_embargo_date(metadata, ln, _):
    access_rights = metadata.get('access_rights', '')
    embargo_date = metadata.get('embargo_date', '')
    if access_rights == 'embargoedAccess':
        if not embargo_date:
            return ('embargo_date', 'error', _('The embargo end date is mandatory when the Access rights field of the Publication is set to Embargo access'))
        try:
            time.strptime(embargo_date, '%Y-%m-%d')
        except ValueError:
            return ('embargo_date', 'error', _('The access rights of the Publication is set to Embargo access but a valid embargo end date is not set'))

def _check_publication_date(metadata, ln, _):
    publication_date = metadata.get('publication_date', '')
    if not publication_date.strip():
        return ('publication_date', 'error', _('The publication date is mandatory'))
    try:
        time.strptime(publication_date, '%Y-%m-%d')
    except ValueError:
        return ('publication_date', 'error', _('The publication date is not correctly typed'))

def _check_pages(metadata, ln, _):
    pages = metadata.get('pages', '').strip()
    if pages and not RE_PAGES.match(pages):
        return ('pages', 'error', _("The pages are not specified correctly"))

CFG_METADATA_FIELDS_CHECKS = {
    'title': _check_title,
    'original_title': _check_original_title,
    'authors': _check_authors,
    'abstract': _check_abstract,
    'language': _check_language,
    'access_rights': _check_access_rights,
    'embargo_date': _check_embargo_date,
    'publication_date': _check_publication_date,
    'pages': _check_pages
}

