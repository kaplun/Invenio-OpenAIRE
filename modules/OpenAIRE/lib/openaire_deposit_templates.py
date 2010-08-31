# -*- coding: utf-8 -*-
##
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
from cgi import escape

from invenio.config import CFG_SITE_LANG, CFG_SITE_URL, CFG_ETCDIR, CFG_VERSION

CFG_OPENAIRE_TEMPLATE = open(os.path.join(CFG_ETCDIR, 'openaire.tpl')).read()

class Template:
    def tmpl_headers(self):
        return """
            <link type="text/css" href="%(site)s/css/smoothness/jquery-ui-1.8.4.custom.css" rel="Stylesheet" />
            <script type="text/javascript" src="%(site)s/js/jquery-1.4.2.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery-ui-1.8.4.custom.min.js"></script>
            <style type="text/css">
            .ui-autocomplete {
                max-height: 200px;
                overflow-y: auto;
            }
            </style>
            """ % {'site': CFG_SITE_URL}

    def tmpl_dropdown_menu(self, kbname, label, name, default=''):
        return """
            <script type="text/javascript">
            $(document).ready(function() {
                $("#%(name)s").autocomplete({
                    source: "%(site)s/kb/export?kbname=%(kbname)s&format=jquery"
                });
            });
            </script>
            <div class="ui-widget"><label for="%(name)s">%(label)s: </label><input size="50" id="%(name)s" name=%(name)s value="%(value)s" /></div>""" % {
                'site': escape(CFG_SITE_URL, True),
                'kbname': escape(kbname, True),
                'name': escape(name, True),
                'label': escape(label),
                'value': escape(default)}

    def tmpl_select_a_project(self, default_project='', action=CFG_SITE_URL+"/deposit/uploadfiles", ln=CFG_SITE_LANG):
        return """
            <h2>&nbsp;</h2>
            <h3>Step 1: Select a Project</h3>
            <p>Start typing the name of the project.<br />
            <br />
            <form action="%(action)s" method="get">
            %(menu)s
            <input type="submit" name="ok" id="ok" value="Select" />
            </p>
            </form>
            <p>&nbsp;</p>
            """ % {
                'action': escape(action, True),
                'menu': self.tmpl_dropdown_menu("project_acronym", "Project", 'project', default=default_project)}

    def tmpl_page(self, title, body, headers, username, logout_key="", ln=CFG_SITE_LANG):
        return CFG_OPENAIRE_TEMPLATE % {
            'headers': headers,
            'title': title,
            'body': body,
            'username': username,
            'logout_key': logout_key,
            'release': "Invenio %s" % CFG_VERSION}