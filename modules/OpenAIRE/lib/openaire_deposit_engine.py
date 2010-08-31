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

from invenio.webpage import page as invenio_page
from invenio.webinterface_handler import wash_urlargd
from invenio.webuser import session_param_set, session_param_get, session_param_list, collect_user_info
from invenio import template
from invenio.config import CFG_SITE_LANG, CFG_SITE_URL

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




