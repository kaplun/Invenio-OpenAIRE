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
import re
from cgi import escape

from invenio.config import CFG_SITE_LANG, CFG_SITE_URL, CFG_ETCDIR, CFG_VERSION
from invenio.messages import gettext_set_language
from invenio.htmlutils import H

CFG_OPENAIRE_PAGE_TEMPLATE = open(os.path.join(CFG_ETCDIR, 'openaire.tpl')).read()
CFG_OPENAIRE_FORM_TEMPLATE = open(os.path.join(CFG_ETCDIR, 'openaire_form.tpl')).read()

RE_PLACEMARKS = re.compile(r'%\((?P<placemark>\w+)\)s')
CFG_OPENAIRE_FORM_TEMPLATE_PLACEMARKS = dict([(placemark, '') for placemark in RE_PLACEMARKS.finditer(CFG_OPENAIRE_FORM_TEMPLATE)])
class Template:
    def tmpl_headers(self):
        return """
            <link type="text/css" href="%(site)s/css/smoothness/jquery-ui-1.8.4.custom.css" rel="Stylesheet" />
            <script type="text/javascript" src="%(site)s/js/jquery-1.4.2.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery-ui-1.8.4.custom.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery.uploadify.v2.1.0.js"></script>
            <script type="text/javascript" src="%(site)s/js/swfobject.js"></script>
            <style type="text/css" src="%(site)s/css/uploadify.css"></style>
            <style type="text/css">
            .ui-autocomplete {
                max-height: 200px;
                overflow-y: auto;
            }
            </style>
            """ % {'site': CFG_SITE_URL}

    def tmpl_dropdown_menu(self, kbname, label, name, default=''):
        return H.script(type="text/javascript")("""
            $(document).ready(function() {
                $("#%(name)s").autocomplete({
                    source: "%(site)s/kb/export?kbname=%(kbname)s&format=jquery"
                });
            });
        """ % {
            'name': name,
            'site': CFG_SITE_URL,
            'kbname': kbname
        }) + H.div(class_="ui-widget")(
                H.label(for_=name)(label + ': ') +
                H.input(size=50, id=name, value=default)
            )

    def tmpl_select_a_project(self, default_project='', action=CFG_SITE_URL+"/deposit/uploadfiles", ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        return H.h3(_('Select a Project')) + \
            H.p(escape(_('Start typing the name of the project')) + H.br() +
                H.form(action=action, method='get')(
                    self.tmpl_dropdown_menu("project_acronym", "Project", 'project', default=default_project) +
                    H.input(type='submit', name='ok', id='ok', value=_("Select"))()
                )
            )

    def tmpl_form(self, projectid, fileinfo, form=None, warnings=None, errors=None, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        values = dict(CFG_OPENAIRE_FORM_TEMPLATE_PLACEMARKS)
        values['id'] = projectid
        for key, value in form.iteritems:
            if key.endswith('_%d' % projectid):
                values['%s_value' % key[:-len('_%d' % projectid)]] = escape(value, True)
        values['fileinfo'] = fileinfo
        values['language_label'] = escape(_("Document language"))
        values['title_label'] = escape(_("Document title"))
        values['original_title_label'] = escape(_("Original language title"))
        values['author_label'] = escape(_("Author(s)"))
        values['abstract_label'] = escape(_("Abstract"))
        values['original_abstract_label'] = escape(_("Original language abstract"))
        values['journal_title_label'] = escape(_("Journal title"))
        values['volume_label'] = escape(_("Volume"))
        values['issue_label'] = escape(_("Issue"))
        values['pages_label'] = escape(_("Pages"))
        values['remove_label'] = escape(_("Remove"))
        values['status_warning_label'] = escape(_('Metadata have some warnings'))
        values['status_error_label'] = escape(_('Metadata have some errors!'))
        values['status_ok_label'] = escape(_('Metadata are OK!'))
        value['status_warning'] = ''
        value['status_error'] = ''
        value['status_ok'] = 'display: none;'
        if warnings:
            values['form_status'] = 'warning'
            value['status_warning'] = 'display: none;'
            value['status_error'] = ''
            value['status_ok'] = ''
            for key, value in warnings.iteritems():
                if key.endswith('_%d' % projectid):
                    values['warning_%s_value' % key[:-len('_%d' % projectid)]] = escape(value, True)
        if errors:
            value['status_warning'] = ''
            value['status_error'] = 'display: none;'
            value['status_ok'] = ''
            values['form_status'] = 'error'
            for key, value in errors.iteritems():
                if key.endswith('_%d' % projectid):
                    values['error_%s_value' % key[:-len('_%d' % projectid)]] = escape(value, True)

        return CFG_OPENAIRE_FORM_TEMPLATE % values

    def tmpl_upload_publications(self, projectid, session, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        return """
            <h3>%(upload_publications)s</h3>
            %(selected_project)s
            <form action="/httptest/dumpreq" method="POST">
            <noscript>
                <label for="file1">%(first_publication)s: <input type="file" id="file1" name="file" />
                <label for="file2">%(second_publication)s: <input type="file" id="file2" name="file" />
                <label for="file3">%(third_publication)s: <input type="file" id="file3" name="file" />
                <input type="hidden" name="projectid" value="%(projectid)s" />
                <input type="submit" name="Upload" value=%(upload)s" />
            </noscript>
            <input id="fileInput" name="file" type="file" />
            <input type="submit" value="%(begin_upload)s" id="begin_upload"/>
            <input type="reset" value="%(cancel_upload)s" id="cancel_upload"/>
            </form>
            <script type="text/javascript">// <![CDATA[
                $(document).ready(function() {
                    $('#fileInput').uploadify({
                    'uploader'  : '%(site)s/flash/uploadify.swf',
                    'script'    : '%(site)s/deposit/uploadifybackend',
                    'cancelImg' : '%(site)s/img/cancel.png',
                    'auto'      : true,
                    'folder'    : '/uploads',
                    'multi'     : true,
                    'buttonText': '%(buttontext)s',
                    'scriptData': {'projectid': '%(projectid)s', 'session': '%(session)s'},
                    'onAllComplete': function(){
                        window.location="%(site)s/deposit/edit_metadata";
                    }
                    });
                    $('#begin_upload').click(function(){
                        $('#fileInput').uploadifyUpload();
                        return 0;
                    });
                    $('#cancel_upload').click(function(){
                        $('#fileInput').uploadifyClearQueue();
                        return 0;
                    });
                });
            // ]]></script>""" % {
                'upload_publications': escape(_("Upload Publications")),
                'selected_project': 'bla',
                'first_publication': escape(_("First publication")),
                'second_publication': escape(_("Second publication")),
                'third_publication': escape(_("Third publication")),
                'site': CFG_SITE_URL,
                'projectid': projectid,
                'session': session,
                'upload': escape(_("Upload")),
                'begin_upload': escape(_("Begin upload")),
                'cancel_upload': escape(_("Cancel upload")),
                'buttontext': _("BROWSE"),
            }

    def tmpl_publication_form(self, index, publicationid, title="", authors="", abstract="", accessrights_type="", embargo="", language="", keyword="", errors=None, warnings=None, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)


    def tmpl_add_publication_data_and_submit(self, selected_project, publication_forms, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        return """
            <h3>%(add_publication_data_and_submit)s</h3>
            <div class="note">
                <h5>%(selected_project_title)s</h5>
                %(selected_project)s (<a href="/deposit/">%(change_project)s</a>)
                <h5>%(uploaded_publications)s</h5>
                <table width="100%%" cellspacing="0" cellpadding="0" border="0">
                    <thead>
                        <tr class="even">
                            <th width="3%%" align="right" valign="bottom" class="even">&nbsp;</th>
                            <th valign="bottom">%(title_head)s</th>
                            <th align="center" valign="bottom">%(license_type_head)s</th>
                            <th align="center" valign="bottom">%(embargo_release_date_head)s</th>
                            <th align="center" valign="bottom">&nbsp;</th>
                        </tr>
                    </thead>
                    <tbody>
                        %(publication_forms)s
                    </tbody>
                </table>
            </div>
            <p align="center"><input type="submit" name="ok" id="ok" value="Next"></p>""" % {
                'add_publication_data_and_submit': escape(_('Add Publication Data & Submit')),
                'selected_project_title': escape(_("Selected Project")),
                'selected_project': selected_project,
                'change_project': escape(_('change project')),
                'uploaded_publications': escape(_('Uploaded Publications')),
                'title_head': escape(_('Title')),
                'license_type_head': escape(_('License Type')),
                'embargo_release_date_head': escape(_('Embargo%(x_br)sRelease Date')) % ('<br />'),
                'publication_forms': publication_forms
            }


    def tmpl_page(self, title, body, headers, username, logout_key="", ln=CFG_SITE_LANG):
        return CFG_OPENAIRE_PAGE_TEMPLATE % {
            'headers': headers,
            'title': title,
            'body': body,
            'username': username,
            'logout_key': logout_key,
            'release': "Invenio %s" % CFG_VERSION}
