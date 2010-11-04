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

from invenio.webinterface_handler import wash_urlargd, WebInterfaceDirectory
from invenio.messages import gettext_set_language
from invenio.webuser import collect_user_info, session_param_get, session_param_set
from invenio.urlutils import redirect_to_url, make_canonical_urlargd
from invenio.session import get_session
from invenio.config import CFG_SITE_URL, CFG_SITE_SECURE_URL
from invenio.openaire_deposit_engine import page, get_project_information, \
    OpenAIREPublication, wash_form, get_exisiting_projectids_for_uid, \
    get_all_projectsids, get_favourite_authorships_for_user, \
    get_all_publications_for_project, upload_file
from invenio.openaire_deposit_utils import simple_metadata2namespaced_metadata
from invenio.access_control_engine import acc_authorize_action
from invenio.bibknowledge import get_kbr_keys
from invenio.urlutils import create_url
from invenio.webinterface_handler_config import SERVER_RETURN, HTTP_BAD_REQUEST, HTTP_UNAUTHORIZED
import invenio.template

openaire_deposit_templates = invenio.template.load('openaire_deposit')

class WebInterfaceOpenAIREDepositPages(WebInterfaceDirectory):
    _exports = ['', 'uploadifybackend', 'sandbox', 'checkmetadata', 'ajaxgateway', 'checksinglefield', 'getfile', 'authorships']

    def index(self, req, form):
        argd = wash_urlargd(form, {'projectid': (int, -1), 'delete': (str, ''), 'publicationid': (str, ''), 'plus': (int, -1), 'linkproject': (int, -1), 'unlinkproject': (int, -1)})
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
                        req.unparsed_uri),
                    "ln" : argd['ln']}, {})))
            else:
                return page(req=req, body=_("You are not authorized to use OpenAIRE deposition."), title=_("Authorization failure"))
        projectid = argd['projectid']
        plus = argd['plus']
        if plus == -1:
            try:
                plus = bool(session_param_get(req, 'plus'))
            except KeyError:
                plus = False
                session_param_set(req, 'plus', plus)
        else:
            plus = bool(plus)
            session_param_set(req, 'plus', plus)

        all_project_ids = get_all_projectsids()

        if projectid not in all_project_ids:
            projectid = -1
        uid = user_info['uid']
        ## No project selected
        ## Then let's display all the existing projects for the given user.
        ## And lets let the user to choose a project.
        projects = [get_project_information(uid, projectid_, deletable=False, ln=argd['ln'], linked=True) for projectid_ in get_exisiting_projectids_for_uid(user_info['uid']) if projectid_ != projectid]
        if projectid < 0:
            selected_project = None
        else:
            selected_project = get_project_information(uid, projectid, deletable=False, linked=False, ln=argd['ln'])
        body = openaire_deposit_templates.tmpl_choose_project(existing_projects=projects, selected_project=selected_project, ln=argd['ln'])
        body += openaire_deposit_templates.tmpl_upload_publications(projectid=projectid, session=get_session(req).sid(), ln=argd['ln'])

        if projectid >= 0:
            ## There is a project on which we are working good!
            publications = get_all_publications_for_project(uid, projectid, ln=argd['ln'])
            if argd['publicationid'] in publications:
                if argd['addproject'] in all_project_ids:
                    publications[argd['publicationid']].link_project(argd['linkproject'])
                if argd['delproject'] in all_project_ids:
                    publications[argd['publicationid']].unlink_project(argd['unlinkproject'])
                if argd['delete']:
                    ## there was a request to delete a publication
                    publications[argd['publicationid']].delete()
                    del publications[argd['publicationid']]

            forms = ""
            submitted_publications = ""
            for index, (publicationid, publication) in enumerate(publications.iteritems()):
                if req.method.upper() == 'POST':
                    publication.merge_form(form, ln=argd['ln'])
                if publication.status == 'edited':
                    publication.check_metadata()
                    if 'submit_%s' % publicationid in form:
                        ## i.e. if the button submit for the corresponding publication has been pressed...
                        publication.upload_record()
                if publication.status in ('initialized', 'edited'):
                    forms += publication.get_publication_form()
                else:
                    submitted_publications += publication.get_publication_preview()
            body += openaire_deposit_templates.tmpl_add_publication_data_and_submit(projectid, forms, submitted_publications, ln=argd['ln'])
        title = _('Manage Your Publications')
        return page(body=body, title=title, req=req)

    def uploadifybackend(self, req, form):
        argd = wash_urlargd(form, {'session': (str, ''), 'projectid': (int, -1)})
        _ = gettext_set_language(argd['ln'])
        session = argd['session']
        get_session(req=req, sid=session)
        user_info = collect_user_info(req)
        if user_info['guest'] == '1':
            raise ValueError(_("This session is invalid"))
        projectid = argd['projectid']
        if projectid < 0:
            raise ValueError(_("Invalid project ID: %s") % projectid)
        uid = user_info['uid']
        upload_file(form, uid, projectid)
        return "1"

    def getfile(self, req, form):
        argd = wash_urlargd(form, {'publicationid': (str, ''), 'fileid': (str, '')})
        uid = collect_user_info(req)['uid']
        publicationid = argd['publicationid']
        fileid = argd['fileid']
        publication = OpenAIREPublication(uid, publicationid, ln=argd['ln'])
        fulltext = publication.fulltexts[fileid]
        return fulltext.stream(req)

    def sandbox(self, req, form):
        body = """
<div id="projects_%(publicationid)s">

</div>
"""
        return page(title='sandbox', body=body, req=req)

    def authorships(self, req, form):
        argd = wash_urlargd(form, {'projectid': (str, ''), 'term': (str, '')})
        user_info = collect_user_info(req)
        uid = user_info['uid']
        req.content_type = 'application/json'
        term = argd['term']
        projectid = argd['projectid']
        ret = get_favourite_authorships_for_user(uid, projectid, term)
        if ret:
            return json.dumps(ret)
        if ':' in term:
            ## an institution is being typed
            name, institute = term.split(':', 1)
            institute = institute.strip()
            if len(institute) > 1:
                institutes = [row[0] for row in get_kbr_keys('institutes', searchkey=institute, searchtype='s')]
                institutes.sort()
                return json.dumps(["%s: %s" % (name, institute) for institute in institutes[:100]])
        return json.dumps([])

    def ajaxgateway(self, req, form):
        argd = wash_urlargd(form, {'projectid': (str, ''), 'publicationid': (str, ''), 'action': (str, ''), 'current_field': (str, '')})
        action = argd['action']
        publicationid = argd['publicationid']
        projectid = argd['projectid']
        assert(action in ('save', 'verify_field', 'submit', 'unlinkproject', 'linkproject'))
        out = {
            'errors': {},
            'warnings': {},
            'addclasses': {},
            'delclasses': {},
            'substitutions': {},
            'appends': {},
            'hiddens': [],
            'showns': [],
        }
        if action == 'verify_field':
            current_field = argd['current_field']
            assert(current_field)
            metadata = wash_form(form, publicationid)
            out["errors"], out["warnings"] = OpenAIREPublication.static_check_metadata(metadata, publicationid, check_only_field=current_field, ln=argd['ln'])
        else:
            user_info = collect_user_info(req)
            auth_code, auth_message = acc_authorize_action(user_info, 'submit', doctype='OpenAIRE')
            assert(auth_code == 0)
            uid = user_info['uid']
            publication = OpenAIREPublication(uid, publicationid, ln=argd['ln'])
            if action == 'unlinkproject':
                publication.unlink_project(projectid)
                out["substitutions"]["#projectsbox_%s" % publicationid] = publication.get_projects_information()
            elif action == 'linkproject':
                publication.link_project(projectid)
                out["substitutions"]["#projectsbox_%s" % publicationid] = publication.get_projects_information()
            else:
                publication.merge_form(form)
                publication.check_metadata()
                out["errors"], out["warnings"] = simple_metadata2namespaced_metadata(publication.errors, publicationid), simple_metadata2namespaced_metadata(publication.warnings, publicationid)
                if "".join(out["errors"].values()).strip(): #FIXME bad hack, we need a cleaner way to discover if there are errors
                    out['addclasses']['#status_%s' % publicationid] = 'error'
                    out['delclasses']['#status_%s' % publicationid] = 'warning ok empty'
                elif "".join(out["warnings"].values()).strip():
                    out['addclasses']['#status_%s' % publicationid] = 'warning'
                    out['delclasses']['#status_%s' % publicationid] = 'error ok empty'
                else:
                    out['addclasses']['#status_%s' % publicationid] = 'ok'
                    out['delclasses']['#status_%s' % publicationid] = 'warning error empty'

                if action == 'save':
                    out["substitutions"]['#publication_information_%s' % publicationid] = publication.get_publication_information()
                elif action == 'submit':
                    if not "".join(out["errors"].values()).strip():
                        publication.upload_record()
                        out["appends"]['#submitted_publications'] = publication.get_publication_preview()
                        out["showns"].append('#submitted_publications')
                        out["hiddens"].append('#header_row_%s' % publicationid)
                        out["hiddens"].append('#body_row_%s' % publicationid)
        req.content_type = 'application/json'
        return json.dumps(out)

    __call__ = index
