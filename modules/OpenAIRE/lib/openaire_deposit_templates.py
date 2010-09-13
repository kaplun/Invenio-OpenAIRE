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

CFG_OPENAIRE_PAGE_TEMPLATE = open(os.path.join(CFG_ETCDIR, 'openaire_page.tpl')).read()
CFG_OPENAIRE_FORM_TEMPLATE = open(os.path.join(CFG_ETCDIR, 'openaire_form.tpl')).read()

RE_PLACEMARKS = re.compile(r'%\((?P<placemark>\w+)\)s')
CFG_OPENAIRE_FORM_TEMPLATE_PLACEMARKS = dict((placemark, '') for placemark in RE_PLACEMARKS.findall(CFG_OPENAIRE_FORM_TEMPLATE))
class Template:
    def tmpl_headers(self):
        return """
            <script type="text/javascript">
                var OpenAIREURL = "%(site)s";
            </script>
            <link type="text/css" href="%(site)s/css/smoothness/jquery-ui-1.8.4.custom.css" rel="Stylesheet" />
            <link type="text/css" href="%(site)s/css/uploadify.css" rel="Stylesheet" />
            <link type="text/css" href="%(site)s/css/jquery.tooltip.css" rel="Stylesheet" />
            <link type="text/css" href="%(site)s/css/openaire.css" rel="Stylesheet" />
            <script type="text/javascript" src="%(site)s/js/jquery-1.4.2.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery-ui-1.8.4.custom.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery.uploadify.v2.1.0.js"></script>
            <script type="text/javascript" src="%(site)s/js/swfobject.js"></script>
            <script type="text/javascript" src="%(site)s/js/openaire_deposit_engine.js"></script>
            <script type="text/javascript" src="http://cdn.jquerytools.org/1.2.4/all/jquery.tools.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery.elastic.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery.form.js"></script>
            """ % {'site': CFG_SITE_URL}

    def tmpl_choose_project(self, default='', ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        script = """
            $(document).ready(function() {
                $("#project").autocomplete({
                    source: "%(site)s/kb/export?kbname=projects&format=jquery",
                    focus: function(event, ui) {
                        $('#projectid').val(ui.item.label);
                        return false;
                    },
                    select: function(event, ui) {
                        $('#project').val(ui.item.label);
                        $('#projectid').val(ui.item.value);
                        return false;
                    }
                }).focus();
            })""" % {'site': CFG_SITE_URL}
        return H.script(script, escape_body=False, type="text/javascript") + \
            H.div(class_="ui-widget")(
                H.label(for_='project')(_("Start typing the project title or the acronym or the grant agreement number")),
                H.input(id='project', name='project', type="text"),
                H.input(type='hidden', name='projectid', id='projectid')
            )

    def tmpl_dropdown_menu(self, kbname, label, name, id, default=''):
        script = """
            $(document).ready(function() {
                $("#%(name)s").autocomplete({
                    source: "%(site)s/kb/export?kbname=%(kbname)s&format=jquery"
                });
            });
        """ % {
            'name': name,
            'site': CFG_SITE_URL,
            'kbname': kbname
        }
        return H.script(script, escape_body=False, type="text/javascript") + H.div(class_="ui-widget")(
                H.label(for_=name)(label + ': '),
                H.input(size=50, id=id, name=name, value=default)
            )

    def tmpl_select_a_project(self, default_project='', ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        return H.h3(_('Select a Project')) + \
            H.p()(
                _('Start typing the name of the project'),
                H.br(),
                H.form(method='get')(
                    self.tmpl_choose_project(ln=ln),
                    H.input(type='submit', name='ok', id='ok', value=_("Select"))
                )
            )

    def tmpl_form(self, projectid, publicationid, index, fileinfo, form=None, metadata_status='empty', warnings=None, errors=None, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        values = dict(CFG_OPENAIRE_FORM_TEMPLATE_PLACEMARKS)
        values['id'] = publicationid
        values['index'] = index
        values['class'] = index % 2 and 'even' or 'odd'
        for key, value in form.iteritems():
            if key.endswith('_%s' % publicationid):
                values['%s_value' % key[:-len('_%s' % publicationid)]] = escape(value, True)
        if not values['title_value']:
            values['title_value'] = _('unknown')
        values['fileinfo'] = fileinfo
        values['projectid'] = projectid
        values['site'] = CFG_SITE_URL
        values['language_label'] = escape(_("Document language"))
        values['title_label'] = escape(_("English title"))
        values['original_title_label'] = escape(_("Original language title"))
        values['authors_label'] = escape(_("Author(s)"))
        values['abstract_label'] = escape(_("English abstract"))
        values['original_abstract_label'] = escape(_("Original language abstract"))
        values['journal_title_label'] = escape(_("Journal title"))
        values['publication_date_label'] = escape(_("Publication date"))
        values['volume_label'] = escape(_("Volume"))
        values['issue_label'] = escape(_("Issue"))
        values['pages_label'] = escape(_("Pages"))
        values['remove_label'] = escape(_("Remove"))
        values['status_warning_label'] = escape(_('Metadata have some warnings'))
        values['status_error_label'] = escape(_('Metadata have some errors!'))
        values['status_ok_label'] = escape(_('Metadata are OK!'))
        values['submit_label'] = escape(_('Submit this publication'))
        values['form_status'] = 'error' ## FIXME metadata_status
        values['access_rights_options'] = self.tmpl_access_rights_options(values.get('access_rights_value', ''), ln=ln)
        values['language_options'] = self.tmpl_language_options(values.get('language_value', ), ln)
        if warnings:
            for key, value in warnings.iteritems():
                if key.endswith('_%s' % publicationid):
                    values['warning_%s_value' % key[:-len('_%s' % publicationid)]] = escape(value, True)
        if errors:
            for key, value in errors.iteritems():
                if key.endswith('_%s' % publicationid):
                    values['error_%s_value' % key[:-len('_%s' % publicationid)]] = escape(value, True)

        return CFG_OPENAIRE_FORM_TEMPLATE % values

    def tmpl_access_rights_options(self, selected_access_right, ln=CFG_SITE_LANG):
        from invenio.openaire_deposit_engine import CFG_ACCESS_RIGHTS
        access_rights = CFG_ACCESS_RIGHTS(ln)
        _ = gettext_set_language(ln)
        out = '<option disabled="disabled">%s</option>' % (_("Select one"))
        for key, value in access_rights.iteritems():
            if key == selected_access_right:
                out += H.option(value=key, selected='selected')(value)
            else:
                out += H.option(value=key)(value)
        return out

    def tmpl_language_options(self, selected_language='eng', ln=CFG_SITE_LANG):
        from invenio.bibknowledge import get_kb_mappings
        languages = get_kb_mappings('languages')
        _ = gettext_set_language(ln)
        out = '<option disabled="disabled">%s</option>' % (_("Select one"))
        for mapping in languages:
            key = mapping['key']
            value = mapping['value']
            if key == selected_language:
                out += '<option value="%(key)s" selected="selected">%(value)s</option>' % {
                    'key': escape(key, True),
                    'value': escape(value)
                }
            else:
                out += '<option value="%(key)s">%(value)s</option>' % {
                    'key': escape(key, True),
                    'value': escape(value)
                }
        return out

    def tmpl_upload_publications(self, projectid, session, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        return """
            <h3>%(upload_publications)s</h3>
            %(selected_project)s
            <form action="%(site)s/deposit/editmetadata" method="POST">
            <input id="fileInput" name="file" type="file" />
            <input type="reset" value="%(cancel_upload)s" id="cancel_upload"/>
            <input type="submit" value="%(begin_upload)s" id="begin_upload"/>
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
                    'simUploadLimit': '2',
                    'scriptData': {'projectid': '%(projectid)s', 'session': '%(session)s'},
                    'onAllComplete': function(){
                        window.location="%(site)s/deposit?projectid=%(projectid)s";
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
                'site': CFG_SITE_URL,
                'projectid': projectid,
                'session': session,
                'upload': escape(_("Upload")),
                'begin_upload': escape(_("Begin upload")),
                'cancel_upload': escape(_("Cancel upload")),
                'buttontext': _("BROWSE"),
            }

    def tmpl_add_publication_data_and_submit(self, selected_project, publication_forms, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        return """
            <h3>%(add_publication_data_and_submit)s</h3>
            <form method="POST" id="publication_forms">
            <div class="note">
                <h5>%(selected_project_title)s</h5>
                %(selected_project)s (<a href="/deposit/">%(change_project)s</a>)
                <h5>%(uploaded_publications)s</h5>
                %(publication_forms)s
            </div>
            </form>
            <script type="text/javascript">
                jQuery(document).ready(function(){
                    $('.accordion .head').click(function() {
                        $(this).next().toggle('slow');
                        return false;
                    }).next().hide();
                    $('input.datepicker').datepicker({dateFormat: 'yy-mm-dd'});
                    $('textarea').elastic();
                    // bind 'myForm' and provide a simple callback function
                    $('#publication_forms').ajaxForm(function() {
                        alert("Thank you for your comment!");
                    });
                    $('a.deletepublication').click(function(){
                        return confirm("%(confirm_delete_publication)s");
                    })
                    });
            </script>
            """ % {
                'add_publication_data_and_submit': escape(_('Add Publication Data & Submit')),
                'selected_project_title': escape(_("Selected Project")),
                'selected_project': selected_project,
                'change_project': escape(_('change project')),
                'uploaded_publications': escape(_('Uploaded Publications')),
                'title_head': escape(_('Title')),
                'license_type_head': escape(_('License Type')),
                'embargo_release_date_head': escape(_('Embargo%(x_br)sRelease Date')) % {'x_br': '<br />'},
                'publication_forms': publication_forms,
                'confirm_delete_publication': _("Are you sure you want to delete this publication?"),
                'ln': ln
            }

    def tmpl_file(self, filename, download_url, md5, mimetype, format, size):
        pass

    def tmpl_page(self, title, body, headers, username, logout_key="", ln=CFG_SITE_LANG):
        return CFG_OPENAIRE_PAGE_TEMPLATE % {
            'headers': headers,
            'title': title,
            'body': body,
            'username': username,
            'logout_key': logout_key,
            'release': "Invenio %s" % CFG_VERSION}
