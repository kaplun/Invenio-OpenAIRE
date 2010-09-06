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

from invenio.webinterface_handler import wash_urlargd, WebInterfaceDirectory
from invenio.messages import gettext_set_language
from invenio.webuser import collect_user_info
from invenio.session import get_session
from invenio.config import CFG_ETCDIR, CFG_VERSION, CFG_SITE_URL
from invenio.openaire_deposit_engine import page, OpenAIREPublications
import invenio.template

openaire_deposit_templates = invenio.template.load('openaire_deposit')

class WebInterfaceOpenAIREDepositPages(WebInterfaceDirectory):
    _exports = ['', 'uploadpublications', 'uploadifybackend']

    def index(self, req, form):
        argd = wash_urlargd(form, {})
        _ = gettext_set_language(argd['ln'])
        body = openaire_deposit_templates.tmpl_select_a_project(ln=argd['ln'])
        title = _("Submit New Publications")
        return page(title=title, body=body, req=req)

    def uploadpublications(self, req, form):
        argd = wash_urlargd(form, {'projectid': (int, 0)})
        _ = gettext_set_language(argd['ln'])
        uid = collect_user_info(req)
        projectid = argd['projectid']
        body = openaire_deposit_templates.tmpl_upload_publications(projectid=projectid, session=get_session(req).sid(), ln=argd['ln'])
        title = _("Upload Publications")
        return page(title=title, body=body, req=req)

    def uploadifybackend(self, req, form):
        argd = wash_urlargd(form, {'projectid': (int, 0), 'session': (str, '')})
        session = argd['session']
        get_session(req=req, sid=session)
        uid = collect_user_info(req)
        publications = OpenAIREPublications(uid, argd['projectid'])
        open('/tmp/uploadify.log', 'a').write('%s %s %s\n' %(uid, session, form['Filedata'].filename))
        return "1"

    def checkmetadata(self, req, form):
        pass

    __call__ = index