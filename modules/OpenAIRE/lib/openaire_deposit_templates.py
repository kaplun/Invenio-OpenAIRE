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
from invenio.htmlutils import H, EscapedString
from invenio.textutils import nice_size

CFG_OPENAIRE_PAGE_TEMPLATE = open(os.path.join(CFG_ETCDIR, 'openaire_page.tpl')).read()
CFG_OPENAIRE_FORM_TEMPLATE = open(os.path.join(CFG_ETCDIR, 'openaire_form.tpl')).read()

RE_PLACEMARKS = re.compile(r'%\((?P<placemark>\w+)\)s')
CFG_OPENAIRE_FORM_TEMPLATE_PLACEMARKS = dict((placemark, '') for placemark in RE_PLACEMARKS.findall(CFG_OPENAIRE_FORM_TEMPLATE))
class Template:
    def tmpl_headers(self):
        return """
            <script type="text/javascript">
                var gSite = "%(site)s";
            </script>
            <link type="text/css" href="%(site)s/css/jquery-ui-1.8.4.custom.css" rel="Stylesheet" />
            <link type="text/css" href="%(site)s/css/uploadify.css" rel="Stylesheet" />
            <link type="text/css" href="%(site)s/css/openaire.css" rel="Stylesheet" />
            <script type="text/javascript" src="%(site)s/js/jquery-1.4.2.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery-ui-1.8.4.custom.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery.uploadify.v2.1.0.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/swfobject.js"></script>
            <script type="text/javascript" src="http://cdn.jquerytools.org/1.2.4/all/jquery.tools.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery.elastic.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery.qtip-1.0.0-rc3.js"></script>
            <script type="text/javascript" src="%(site)s/js/openaire_deposit_engine.js"></script>
            """ % {'site': CFG_SITE_URL}

    def tmpl_choose_project(self, default='', existing_projects=None, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        if existing_projects is None:
            existing_projects = {}
        body = ""
        for existing_projectid, existing_project in existing_projects.iteritems():
            body += self.tmpl_project_information(existing_projectid, existing_project['grant_agreement_number'], existing_project['ec_project_website'], existing_project['acronym'], existing_project['call_identifier'], existing_project['end_date'], existing_project['start_date'], existing_project['title'], existing_project['fundedby'], project_selection=True, ln=ln)

        script = """
            $(document).ready(function() {
                $("#project").autocomplete({
                    source: "%(site)s/kb/export?kbname=projects&amp;format=jquery&amp;ln=%(ln)s",
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
            })""" % {'site': CFG_SITE_URL, 'ln': ln}
        return H.script(script, escape_body=False, type="text/javascript") + \
            H.div(class_="note")(EscapedString(body, escape_nothing=True)) + H.div(class_="ui-widget")(
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

    def tmpl_select_a_project(self, existing_projects=None, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        return """
            <h3>%(select_a_project_label)s</h3>
            <form method="get">
                %(choose_a_project)s
                <input type="submit" name="ok" id="ok" value="%(select_label)s" />
            </form>
            """ % {
                'select_a_project_label': escape(_("Your projects")),
                'choose_a_project': self.tmpl_choose_project(existing_projects=existing_projects, ln=ln),
                'select_label': escape(_("Select"), True),
            }

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
        values['authors_tooltip'] = escape(_("<p>Please enter one author per line in the form: <pre>Surname, First Names: Institution</pre> Note that the <em>institution</em> is optional although recommended.</p><p>Example of valid entries are:<ul><li>John, Doe: Example institution</li><li>Jane Doe</li></ul></p>"), True)
        values['abstract_label'] = escape(_("English abstract"))
        values['english_language_label'] = escape(_("English information"))
        values['original_language_label'] = escape(_("Original language information"))
        values['original_abstract_label'] = escape(_("Original language abstract"))
        values['journal_title_label'] = escape(_("Journal title"))
        values['publication_date_label'] = escape(_("Publication date"))
        values['volume_label'] = escape(_("Volume"))
        values['issue_label'] = escape(_("Issue"))
        values['pages_label'] = escape(_("Pages"))
        values['remove_label'] = escape(_("Remove"))
        values['remove_confirm'] = escape(_("Are you sure you want to permanently remove this publication?"))
        values['status_warning_label'] = escape(_('Metadata have some warnings'))
        values['status_error_label'] = escape(_('Metadata have some errors!'))
        values['status_ok_label'] = escape(_('Metadata are OK!'))
        values['submit_label'] = escape(_('Submit this publication'))
        values['form_status'] = 'error' ## FIXME metadata_status
        values['access_rights_options'] = self.tmpl_access_rights_options(values.get('access_rights_value', ''), ln=ln)
        values['language_options'] = self.tmpl_language_options(values.get('language_value', ), ln)
        values['save_label'] = escape(_('Save publication'))
        values['submit_label'] = escape(_('Submit publication'))
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
            <form action="%(site)s/deposit" method="POST">
                <input id="fileInput" name="file" type="file" />
                <input type="reset" value="%(cancel_upload)s" id="cancel_upload"/>
                <input type="hidden" value="%(projectid)s" name="projectid" />
                <input type="hidden" value="%(session)s" name="session" />
            </form>
            <script type="text/javascript">// <![CDATA[
                $(document).ready(function() {
                    $('#cancel_upload').hide();
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
                        $('input.save').trigger('click');
                        window.location="%(site)s/deposit?projectid=%(projectid)s";
                    },
                    'onOpen': function(){
                        $('#cancel_upload').show();
                    }
                    });
                    $('#cancel_upload').click(function(){
                        $('#fileInput').uploadifyClearQueue();
                        return 0;
                    });
                });
            // ]]></script>""" % {
                'upload_publications': escape(_("Upload Publications")),
                'projectid': 'bla',
                'site': CFG_SITE_URL,
                'projectid': projectid,
                'session': session,
                'upload': escape(_("Upload")),
                'begin_upload': escape(_("Begin upload")),
                'cancel_upload': escape(_("Cancel upload")),
                'buttontext': _("BROWSE"),
            }



    def tmpl_project_information(self, projectid, grant_agreement_number, ec_project_website, acronym, call_identifier, end_date, start_date, title, fundedby, project_selection=False, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        data = {
                'selected_project_label': escape(_("Selected Project")),
                'acronym': escape(acronym, True),
                'site': escape(CFG_SITE_URL, True),
                'change_project_label': escape(_("change project")),
                'acronym_label': escape(_("Acronym"), True),
                'title_label': escape(_("Title"), True),
                'title': escape(title, True),
                'grant_agreement_number_label': escape(_("Grant Agreement Number"), True),
                'grant_agreement_number': escape(str(grant_agreement_number), True),
                'ec_project_website_label': escape(_("EC Project Website"), True),
                'ec_project_website': escape(ec_project_website, True),
                'start_date_label': escape(_("Start Date"), True),
                'start_date': escape(start_date, True),
                'end_date_label': escape(_("End Date"), True),
                'end_date': escape(end_date, True),
                'fundedby_label': escape(_("Funded By"), True),
                'fundedby': escape(fundedby, True),
                'call_identifier_label': escape(_("Call Identifier"), True),
                'call_identifier': escape(call_identifier, True),
                'id': escape(projectid, True),
                'ln': escape(ln, True),
                'selected_project_label': escape(_("Selected project"))
            }
        if project_selection:
            data['acronym_body'] = """<a href="%(site)s/deposit?projectid=%(id)s&amp;ln=%(ln)s" class="selectedproject" id="selectedproject_%(id)s">%(acronym)s</a>""" % data
        else:
            data['acronym_body'] = """<div class="note"><h5>%(selected_project_label)s</h5>
<div class="selectedproject" id="selectedproject_%(id)s">%(acronym)s</div> (<a href="%(site)s/deposit">%(change_project_label)s</a>)</div>""" % data
        return """
            %(acronym_body)s
            <script type="text/javascript">// <![CDATA[
                $(document).ready(function(){
                    var tooltip = clone(gTipDefault);
                    tooltip.content = {'text': '<table><tbody><tr><td align="right"><strong>%(acronym_label)s:<strong></td><td align="left">%(acronym)s</td></tr><tr><td align="right"><strong>%(title_label)s:<strong></td><td align="left">%(title)s</td></tr><tr><td align="right"><strong>%(grant_agreement_number_label)s:<strong></td><td align="left">%(grant_agreement_number)s</td></tr><tr><td align="right"><strong>%(ec_project_website_label)s:<strong></td><td align="left"><a href="%(ec_project_website)s" target="_blank">%(ec_project_website_label)s</a></td></tr><tr><td align="right"><strong>%(start_date_label)s:<strong></td><td align="left">%(start_date)s</td></tr><tr><td align="right"><strong>%(end_date_label)s:<strong></td><td align="left">%(end_date)s</td></tr><tr><td align="right"><strong>%(fundedby_label)s:<strong></td><td align="left">%(fundedby)s</td></tr><tr><td align="right"><strong>%(call_identifier_label)s:<strong></td><td align="left">%(call_identifier)s</td></tr><tbody></table>'}
                    $('#selectedproject_%(id)s').qtip(tooltip);
                });
            // ]]></script>""" % data

    def tmpl_add_publication_data_and_submit(self, projectid, project_information, publication_forms, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        return """
            <h3>%(add_publication_data_and_submit)s</h3>
            <form method="POST" id="publication_forms">
            %(project_information)s
            %(publication_forms)s
            </form>
            <script type="text/javascript">//<![CDATA[
                var gProjectid = %(projectid)s;
                jQuery(document).ready(function(){
                    $('.accordion .head').click(function() {
                        $(this).next().toggle('slow');
                        return false;
                    }).next().hide();
                    $('input.datepicker').datepicker({dateFormat: 'yy-mm-dd'});
                    $('textarea').elastic();
                    $('#publication_forms').submit(function(event){
                        event.stopPropagation();
                        return false;
                    });
                    $('a.deletepublication').click(function(){
                        return confirm("%(confirm_delete_publication)s");
                    })
                    });
            //]]></script>
            """ % {
                'project_information': project_information,
                'add_publication_data_and_submit': escape(_('Add Publication Data & Submit')),
                'selected_project_title': escape(_("Selected Project")),
                'projectid': projectid,
                'change_project': escape(_('change project')),
                'uploaded_publications': escape(_('Uploaded Publications')),
                'title_head': escape(_('Title')),
                'license_type_head': escape(_('License Type')),
                'embargo_release_date_head': escape(_('Embargo%(x_br)sRelease Date')) % {'x_br': '<br />'},
                'publication_forms': publication_forms,
                'confirm_delete_publication': _("Are you sure you want to delete this publication?"),
                'ln': ln,
                'projectid': projectid
            }


    def tmpl_file(self, filename, publicationid, download_url, md5, mimetype, format, size, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        return """
            %(file_label)s: <div class="file" id="file_%(id)s"><em>%(filename)s</em></div>
            <script type="text/javascript">//<![CDATA[
                $(document).ready(function(){
                    var tooltip = clone(gTipDefault);
                    tooltip.content = {'text': '<table><tbody><tr><td align="right"><strong>%(filename_label)s:<strong></td><td align="left"><a href="%(download_url)s" target="_blank" type="%(mimetype)s">%(filename)s</a></td></tr><tr><td align="right"><strong>%(checksum_label)s:<strong></td><td align="left">%(md5)s</td></tr><tr><td align="right"><strong>%(mimetype_label)s:<strong></td><td align="left">%(mimetype)s</td></tr><tr><td align="right"><strong>%(format_label)s:<strong></td><td align="left">%(format)s</td></tr><tr><td align="right"><strong>%(size_label)s:<strong></td><td align="left">%(size)s</td></tr><tbody></table>'}
                    $('#file_%(id)s').qtip(tooltip);
                });
            //]]></script>""" % {
                'file_label': escape(_('file')),
                'id': escape(publicationid, True),
                'filename': escape(filename),
                'filename_label': escape(_("Name")),
                'download_url': escape(download_url, True),
                'mimetype': escape(mimetype, True),
                'mimetype_label': escape(_("Mimetype")),
                'format': escape(format),
                'format_label': escape(_("Format")),
                'size_label': escape(_("Size")),
                'size': escape(nice_size(size)),
                'checksum_label': escape(_("MD5 Checksum")),
                'md5': escape(md5),
            }

    def tmpl_page(self, title, body, headers, username, logout_key="", ln=CFG_SITE_LANG):
        return CFG_OPENAIRE_PAGE_TEMPLATE % {
            'headers': headers,
            'title': title,
            'body': body,
            'username': username,
            'logout_key': logout_key,
            'site': CFG_SITE_URL,
            'release': "Invenio %s" % CFG_VERSION}