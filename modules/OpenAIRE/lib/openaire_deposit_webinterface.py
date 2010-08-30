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
from invenio.webpage import page
from invenio.messages import gettext_set_language
from invenio.webuser import collect_user_info
from invenio.config import CFG_ETCDIR, CFG_VERSION, CFG_SITE_URL

CFG_OPENAIRE_TEMPLATE = open(os.path.join(CFG_ETCDIR, 'openaire.tpl')).read()

class WebInterfaceOpenAIREDepositPages(WebInterfaceDirectory):
    _exports = ['']

    def index(self, req, form):
        argd = wash_urlargd(form, {'style': (str, 'referer')})
        if argd['style'] == 'referer':
            referer = req.headers_in['referer']
            if referer:
                if referer.startswith('http://www.openaire.eu/'):
                    argd['style'] = 'portal'
                else:
                    argd['style'] = 'invenio'
            else:
                argd['style'] = 'invenio'
        _ = gettext_set_language(argd['ln'])
        values = {}
        values['title'] = _('OpenAIRE Orphan Record Repository')
        values['headers'] = """
<link type="text/css" href="%(site)s/css/smoothness/jquery-ui-1.8.4.custom.css" rel="Stylesheet" />
<script type="text/javascript" src="%(site)s/js/jquery-1.4.2.min.js"></script>
<script type="text/javascript" src="%(site)s/js/jquery-ui-1.8.4.custom.min.js"></script>
""" % {'site': CFG_SITE_URL}
        values['body'] = """<script type="text/javascript">
    $(document).ready(function() {
        $("#test").autocomplete({
            source: "%(site)s/kb/export?kbname=project_acronym&format=jquery"
        });
    });
    </script>
    <div class="ui-widget"><label for="test">Test: </label><input id="test"/></div>""" % {'site': CFG_SITE_URL}
        user_info = collect_user_info(req)
        values['username'] = user_info.get('EXTERNAL_username', user_info['email'])
        values['logout_key'] = user_info.get('EXTERNAL_logout_key', '')
        values['release'] = "Invenio %s" % CFG_VERSION
        if argd['style'] == 'portal':
            return CFG_OPENAIRE_TEMPLATE % values
        else:
            return page(values['title'], values['body'], metaheaderadd=values['headers'])
