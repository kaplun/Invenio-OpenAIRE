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
import json

from invenio.webinterface_handler import wash_urlargd, WebInterfaceDirectory
from invenio.messages import gettext_set_language
from invenio.webuser import collect_user_info
from invenio.urlutils import redirect_to_url, make_canonical_urlargd
from invenio.session import get_session
from invenio.config import CFG_ETCDIR, CFG_VERSION, CFG_SITE_URL, CFG_SITE_SECURE_URL
from invenio.openaire_deposit_engine import page, OpenAIREPublications, OpenAIREPublication, wash_form
from invenio.access_control_engine import acc_authorize_action
import invenio.template

openaire_deposit_templates = invenio.template.load('openaire_deposit')

class WebInterfaceOpenAIREDepositPages(WebInterfaceDirectory):
    _exports = ['', 'uploadifybackend', 'sandbox', 'checkmetadata']

    def index(self, req, form):
        argd = wash_urlargd(form, {'projectid': (int, 0), 'delete': (str, '')})
        _ = gettext_set_language(argd['ln'])
        user_info = collect_user_info(req)
        auth_code, auth_message = acc_authorize_action(user_info, 'submit', doctype='OpenAIRE')
        if auth_code:
            if user_info['guest'] == '1':
                return redirect_to_url(req, "%s/youraccount/login%s" % (
                    CFG_SITE_SECURE_URL,
                        make_canonical_urlargd({
                    'referer' : "%s%s" % (
                        CFG_SITE_URL,
                        req.uri),
                    "ln" : argd['ln']}, {})))
            else:
                return page(req=req, body=_("You are not authorized to use OpenAIRE deposition."), title=_("Authorization failure"))
        projectid = argd['projectid']
        if not projectid:
            body = openaire_deposit_templates.tmpl_select_a_project(ln=argd['ln'])
            title = _("Submit New Publications")
            return page(title=title, body=body, req=req)
        else:
            uid = user_info['uid']
            publications = OpenAIREPublications(uid, projectid)
            if argd['delete']:
                publications.delete_publication(argd['delete'])
            project_data = '' ## FIXME
            fileinfo = '' ## FIXME
            selected_project = '' ## FIXME openaire_deposit_templates.tmpl_selected_project(projectid, project_data)
            forms = ""
            for index, (publicationid, publication) in enumerate(publications.iteritems()):
                publication.merge_form(form, check_required_fields=False, ln=argd['ln'])
                forms += openaire_deposit_templates.tmpl_form(projectid, publicationid, index+1, fileinfo, form=publication.metadata['__form__'], warnings=publication.warnings, errors=publication.errors, ln=argd['ln'])
            body = openaire_deposit_templates.tmpl_add_publication_data_and_submit(selected_project, forms, ln=argd['ln'])
            body += openaire_deposit_templates.tmpl_upload_publications(projectid=projectid, session=get_session(req).sid(), ln=argd['ln'])
            title = _('Edit Publications Information')
            return page(body=body, title=title, req=req)

    def uploadifybackend(self, req, form):
        argd = wash_urlargd(form, {'projectid': (int, 0), 'session': (str, '')})
        _ = gettext_set_language(argd['ln'])
        session = argd['session']
        get_session(req=req, sid=session)
        user_info = collect_user_info(req)
        if user_info['guest'] == '1':
            raise ValueError(_("This session is invalid"))
        uid = user_info['uid']
        publications = OpenAIREPublications(uid, argd['projectid'])
        publications.upload_several_files(form)
        return "1"

    def getfile(self, req, form):
        argd = wash_urlargd(form, {'projectid': (int, 0), 'publicationid': (str, ''), 'fileid': (str, '')})
        uid = collect_user_info(req)['uid']
        publicationid = argd['publicationid']
        projectid = argd['projectid']
        fileid = argd['fileid']
        publication = OpenAIREPublication(uid, projectid, publicationid)
        fulltext = publication.fulltexts[fileid]
        return fulltext.stream(req)

    def sandbox(self, req, form):
        body = """<em id="filename">pippo</em>
            <div class="tooltip">
            <h1>this is a prova</h1>
            <p>ciao mamama</p><p>come va</p>
            </div>
            <script type="text/javascript">
                $("#filename").tooltip({ effect: 'slide'});
            </script>
            <form action="%(site)s/httptest/dumpreq" method="get">
            <input type="submit" name="ciao" value="un value" title="foo"/>
            <input type="submit" name="pippolo" value="suu" title="boh" />
            </form>
        """ % {'site' : CFG_SITE_URL}
        return page(title='sandbox', body=body, req=req)

    def checkmetadata(self, req, form):
        argd = wash_urlargd(form, {'publicationid': (str, ''),
            'check_required_fields': (int, 0)
        })
        publicationid = argd['publicationid']
        check_required_fields = argd['check_required_fields']
        metadata = wash_form(form, publicationid)
        req.content_type = 'application/json'
        errors, warnings = OpenAIREPublication.check_metadata(metadata, publicationid, check_required_fields=check_required_fields, ln=argd['ln'])
        return json.dumps({'errors': errors, 'warnings': warnings})

    __call__ = index