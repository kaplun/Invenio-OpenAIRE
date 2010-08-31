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
from invenio.config import CFG_ETCDIR, CFG_VERSION, CFG_SITE_URL
from invenio.openaire_deposit_engine import page, openaire_deposit_templates

class WebInterfaceOpenAIREDepositPages(WebInterfaceDirectory):
    _exports = ['']

    def index(self, req, form):
        argd = wash_urlargd(form, {})
        _ = gettext_set_language(argd['ln'])
        body = openaire_deposit_templates.tmpl_select_a_project(ln=argd['ln'])
        title = _("Submit New Publications")
        return page(title=title, body=body, req=req)

    __call__ = index