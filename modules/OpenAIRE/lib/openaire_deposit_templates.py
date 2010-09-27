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
from cgi import escape as cgi_escape

from invenio.config import CFG_SITE_LANG, CFG_SITE_URL, CFG_ETCDIR, CFG_VERSION
from invenio.messages import gettext_set_language
from invenio.htmlutils import H, EscapedString
from invenio.textutils import nice_size

CFG_OPENAIRE_PAGE_TEMPLATE = open(os.path.join(CFG_ETCDIR, 'openaire_page.tpl')).read()
CFG_OPENAIRE_FORM_TEMPLATE = open(os.path.join(CFG_ETCDIR, 'openaire_form.tpl')).read()

def escape(value, *args, **argd):
    """Always cast to string as to avoid None values."""
    if value is None:
        value = ''
    return cgi_escape(str(value), *args, **argd)

RE_PLACEMARKS = re.compile(r'%\((?P<placemark>\w+)\)s')
CFG_OPENAIRE_FORM_TEMPLATE_PLACEMARKS = dict((placemark, '') for placemark in RE_PLACEMARKS.findall(CFG_OPENAIRE_FORM_TEMPLATE))
class Template:
    def tmpl_headers(self, ln):
        return """
            <script type="text/javascript">// <![CDATA[
                var gSite = "%(site)s";
                var gLn = "%(ln)s";
            // ]]></script>
            <link type="text/css" href="%(site)s/css/jquery-ui-1.8.5.custom.css" rel="Stylesheet" />
            <link type="text/css" href="%(site)s/css/uploadify.css" rel="Stylesheet" />
            <link type="text/css" href="%(site)s/css/openaire.css" rel="Stylesheet" />
            <script type="text/javascript" src="%(site)s/js/jquery-1.4.2.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery-ui-1.8.5.custom.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery.uploadify.v2.1.0.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/swfobject.js"></script>
            <script type="text/javascript" src="http://cdn.jquerytools.org/1.2.4/all/jquery.tools.min.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery.elastic.js"></script>
            <script type="text/javascript" src="%(site)s/js/jquery.qtip-1.0.0-rc3.js"></script>
            <script type="text/javascript" src="%(site)s/js/openaire_deposit_engine.js"></script>
            """ % {'site': CFG_SITE_URL, 'ln': ln}

    def tmpl_choose_project(self, default='', existing_projects=None, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        if existing_projects is None:
            existing_projects = []
        body = ' '.join(existing_projects)
        return  H.div(class_="note")(EscapedString(body, escape_nothing=True)) + H.div(class_="ui-widget")(
                H.label(for_='project')(_("Start typing the project title or the acronym or the grant agreement number")),
                H.input(id='project', name='project', type="text"),
                H.input(type='hidden', name='projectid', id='projectid')
            )

    def tmpl_select_a_project(self, existing_projects=None, plus=False, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        if plus:
            openaire_plus = """
                <p>%(explanation)s<br />
                <form method="POST">
                    <input type="hidden" name="projectid" value="000000" />
                    <input type="submit" value="%(no_project)s" />
                </form>
            """ % {
                'explanation': escape(_("If the publications you wish to deposit do not belong"
                    " to any FP7 EU Project, just click the following button.")),
                'no_project': escape(_("No project"), True),
            }
        else:
            openaire_plus = ''
        return """
            <h3>%(select_a_project_label)s</h3>
            <form method="POST">
                %(choose_a_project)s
                <input type="submit" name="ok" id="ok" value="%(select_label)s" />
            </form>
            %(openaire_plus)s
            """ % {
                'select_a_project_label': escape(_("Your projects")),
                'choose_a_project': self.tmpl_choose_project(existing_projects=existing_projects, ln=ln),
                'select_label': escape(_("Select"), True),
                'openaire_plus': openaire_plus
            }

    def tmpl_publication_preview(self, body, recid, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        return """
            <p>%(description)s</p>
            <div class="note">%(body)s</div>
            """ % {
                'description': escape(_("This is a preview of the submitted publication. It will be available at %(url)s.")) % {
                    "url": """<a href="%(site)s/record/%(recid)s" alt="%(the_record)s">%(site)s/record/%(recid)s</a>""" % {
                        'site': escape(CFG_SITE_URL, True),
                        'recid': recid,
                        'the_record': escape(_("The record"), True),
                    },
                },
                'body': body,
            }


    def tmpl_form(self, projectid, publicationid, publication_information, fileinfo, form=None, metadata_status='empty', warnings=None, errors=None, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        values = dict(CFG_OPENAIRE_FORM_TEMPLATE_PLACEMARKS)
        values['id'] = publicationid
        if form:
            for key, value in form.iteritems():
                if key.endswith('_%s' % publicationid):
                    values['%s_value' % key[:-len('_%s' % publicationid)]] = escape(value, True)
        values['edit_metadata_label'] = escape(_("Edit"))
        values['fileinfo'] = fileinfo
        values['projectid'] = projectid
        values['site'] = CFG_SITE_URL
        values['mandatory_label'] = escape(_("The symbol %(x_asterisk)s means the field is mandatory.")) % {"x_asterisk": """<img src="%s/img/asterisk.png" alt="mandatory" />""" % CFG_SITE_URL}
        values['language_label'] = escape(_("Document language"))
        values['title_label'] = escape(_("English title"))
        values['original_title_label'] = escape(_("Original language title"))
        values['authors_label'] = escape(_("Author(s)"))
        values['authors_tooltip'] = escape(_("<p>Please enter one author per line in the form: <pre>Surname, First Names: Institution</pre> Note that the <em>institution</em> is optional although recommended.</p><p>Example of valid entries are:<ul><li>John, Doe: Example institution</li><li>Jane Doe</li></ul></p>"), True)
        values['authors_hint'] = escape(_("Doe, John: Example institution"))
        values['abstract_label'] = escape(_("English abstract"))
        values['english_language_label'] = escape(_("English information"))
        values['original_language_label'] = escape(_("Original language information"))
        values['original_abstract_label'] = escape(_("Original language abstract"))
        values["journal_title_tooltip"] = escape(_("""<p>Start typing part of the name of the journal where you published your publication, and, when possible, it will be automatically completed against a list of known journal titles.</p><p><em>Note that the journal title list has been retrieved from the freely available resource in the <a href="http://www.ncbi.nlm.nih.gov/entrez/citmatch_help.html#JournalLists" target="_blank"><strong>Entrez</strong></a> database.</p>"""), True)
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
        values['embargo_date_hint'] = escape(_("End of the embargo"), True)
        values['embargo_date_tooltip'] = escape(_("Enter here the date when the embargo period for this publication will be over."), True)
        values['language_options'] = self.tmpl_language_options(values.get('language_value', 'eng'), ln)
        values['save_label'] = escape(_('Save publication'))
        values['submit_label'] = escape(_('Submit publication'))
        values['embargo_date_size'] = len(values['embargo_date_hint'])
        values['publication_information'] = publication_information
        values['status'] = metadata_status
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
        out = '<option disabled="disabled">%s</option>' % (_("Select access rights"))
        for key, value in access_rights.iteritems():
            if key == selected_access_right:
                out += H.option(value=key, selected='selected')(value)
            else:
                out += H.option(value=key)(value)
        return out

    def tmpl_language_options(self, selected_language='eng', ln=CFG_SITE_LANG):
        from invenio.bibknowledge import get_kb_mappings
        if not selected_language:
            selected_language = 'eng'
        languages = get_kb_mappings('languages')
        _ = gettext_set_language(ln)
        out = ""
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
            <form action="%(site)s/deposit?ln=%(ln)s" method="POST">
                <h3>%(upload_publications)s</h3>
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
                'upload_publications': escape(_("Upload New Publications")),
                'projectid': 'bla',
                'site': CFG_SITE_URL,
                'projectid': projectid,
                'session': session,
                'upload': escape(_("Upload")),
                'begin_upload': escape(_("Begin upload")),
                'cancel_upload': escape(_("Cancel upload")),
                'buttontext': _("Upload"),
                'ln': ln,
            }


    def tmpl_publication_information(self, publicationid, title, authors, abstract, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        authors = authors.strip().splitlines()
        if not title:
            title = _("Title not yet defined")
        data = {
                'title_label': escape(_("Title")),
                'authors_label': len(authors) != 1 and escape(_("Author(s)")) or escape(_("Author")),
                'abstract_label': escape(_("Abstract")),
                'title': escape(title),
                'authors': "<br />".join([escape(author) for author in authors]),
                'abstract': escape(abstract).replace('\n', '<br />'),
                'id': escape(publicationid, True)
            }
        data['body'] = """<div id="publication_information_%(id)s" class="publication_information">%(title)s</div>""" % data
        return """
            %(body)s
            <script type="text/javascript">// <![CDATA[
                $(document).ready(function(){
                    var tooltip = clone(gTipDefault);
                    tooltip.content = {
                        'text': '<table><tbody><tr><td align="right"><strong>%(title_label)s:<strong></td><td align="left">%(title)s</td></tr><tr><td align="right"><strong>%(authors_label)s:<strong></td><td align="left">%(authors)s</td></tr><tr><td align="right"><strong>%(abstract_label)s:<strong></td><td align="left">%(abstract)s</td></tr><tbody></table>'
                    };
                    $('#publication_information_%(id)s').qtip(tooltip);
                });
            // ]]></script>""" % data


    def tmpl_project_information(self, projectid, existing_publications, grant_agreement_number='', ec_project_website='', acronym='', call_identifier='', end_date='', start_date='', title='', fundedby='', linked=True, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        if projectid == '000000':
            data = {
                    'selected_project_label': escape(_("Selected Project")),
                    'acronym': escape(_('NO PROJECT'), True),
                    'site': escape(CFG_SITE_URL, True),
                    'id': escape(projectid, True),
                    'ln': escape(ln, True),
                    'existing_publications': existing_publications,
                }
            if linked:
                data['acronym'] = """<a href="%(site)s/deposit?projectid=%(id)s&amp;ln=%(ln)s">%(acronym)s</a>""" % data
            return """
                <div class="selectedproject" id="selectedproject_%(id)s">%(acronym)s (%(existing_publications)d)</div>""" % data
        else:
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
                    'existing_publications': existing_publications,
                }
            if linked:
                data['acronym'] = """<a href="%(site)s/deposit?projectid=%(id)s&amp;ln=%(ln)s">%(acronym)s</a>""" % data
            return """
                <div class="selectedproject" id="selectedproject_%(id)s">%(acronym)s (%(existing_publications)d)</div>
                <script type="text/javascript">// <![CDATA[
                    $(document).ready(function(){
                        var tooltip = clone(gTipDefault);
                        tooltip.content = {
                            'text': '<table><tbody><tr><td align="right"><strong>%(acronym_label)s:<strong></td><td align="left">%(acronym)s</td></tr><tr><td align="right"><strong>%(title_label)s:<strong></td><td align="left">%(title)s</td></tr><tr><td align="right"><strong>%(grant_agreement_number_label)s:<strong></td><td align="left">%(grant_agreement_number)s</td></tr><tr><td align="right"><strong>%(ec_project_website_label)s:<strong></td><td align="left"><a href="%(ec_project_website)s" target="_blank">%(ec_project_website_label)s</a></td></tr><tr><td align="right"><strong>%(start_date_label)s:<strong></td><td align="left">%(start_date)s</td></tr><tr><td align="right"><strong>%(end_date_label)s:<strong></td><td align="left">%(end_date)s</td></tr><tr><td align="right"><strong>%(fundedby_label)s:<strong></td><td align="left">%(fundedby)s</td></tr><tr><td align="right"><strong>%(call_identifier_label)s:<strong></td><td align="left">%(call_identifier)s</td></tr><tbody></table>'
                        };
                        $('#selectedproject_%(id)s').qtip(tooltip);
                    });
                // ]]></script>""" % data

    def tmpl_add_publication_data_and_submit(self, projectid, project_information, publication_forms, submitted_publications, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)

        if publication_forms:
            publication_forms = """<form method="POST" id="publication_forms">
            <div class="note OpenAIRE">
            <table>
            %(publication_forms)s
            </table>
            </div>
            </form>""" % {'publication_forms': publication_forms}
        else:
            publication_forms = ''

        return """
            <h3>%(title)s</h3>
            <div class="note">
            %(project_information)s (<a href="%(site)s/deposit?ln=%(ln)s" alt="%(change_project_label)s">%(change_project_label)s</a>)
            </div>
            %(publication_forms)s
            <div id="submitted_publications">
            <h3>%(submitted_publications_title)s</h3>
            %(submitted_publications)s
            </div>
            <script type="text/javascript">//<![CDATA[
                var gProjectid = "%(projectid)s";
                $(document).ready(function(){
                    $('input.datepicker').datepicker({
                        dateFormat: 'yy-mm-dd',
                        showOn: 'both',
                        onClose: function(){
                            $(this).focus();
                        },
                        showButtonPanel: true
                    });
                    $('textarea').elastic();
                    $('#publication_forms').submit(function(event){
                        event.preventDefault();
                        return false;
                    });
                    $('a.deletepublication').click(function(){
                        return confirm("%(confirm_delete_publication)s");
                    });
                    %(hide_submitted_publications)s
                });
            //]]></script>
            """ % {
                'submitted_publications_title': escape(_("Successfully submitted publications")),
                'project_information': project_information,
                'title': escape(_('Your Current Publications')),
                'selected_project_title': escape(_("Selected Project")),
                'projectid': projectid,
                'change_project_label': escape(_('change project'), True),
                'uploaded_publications': escape(_('Uploaded Publications')),
                'title_head': escape(_('Title')),
                'license_type_head': escape(_('License Type')),
                'embargo_release_date_head': escape(_('Embargo%(x_br)sRelease Date')) % {'x_br': '<br />'},
                'publication_forms': publication_forms,
                'confirm_delete_publication': _("Are you sure you want to delete this publication?"),
                'submitted_publications': submitted_publications,
                'hide_submitted_publications': not submitted_publications and \
                    """$("#submitted_publications").hide();""" or '',
                'ln': ln,
                'projectid': projectid,
                'done': escape(_("Done"), True),
                'today': escape(_("Today"), True),
                'next': escape(_("Next"), True),
                'prev': escape(_("Prev"), True),
                'site': escape(CFG_SITE_URL, True),
            }


    def tmpl_fulltext_information(self, filename, publicationid, download_url, md5, mimetype, format, size, ln=CFG_SITE_LANG):
        _ = gettext_set_language(ln)
        filename = filename.decode('utf8')
        filename = ''.join(["%s<br />" % escape(filename[i:i+30].encode('utf8')) for i in xrange(0, len(filename), 30)])
        return """
            %(file_label)s: <div class="file" id="file_%(id)s"><em>%(filename)s</em></div>
            <script type="text/javascript">//<![CDATA[
                $(document).ready(function(){
                    var tooltip = clone(gTipDefault);
                    tooltip.content = {
                        'text': '<table><tbody><tr><td align="right"><strong>%(filename_label)s:<strong></td><td align="left"><a href="%(download_url)s" target="_blank" type="%(mimetype)s">%(filename)s</a></td></tr><tr><td align="right"><strong>%(format_label)s:<strong></td><td align="left">%(format)s</td></tr><tr><td align="right"><strong>%(size_label)s:<strong></td><td align="left">%(size)s</td></tr><tr><td align="right"><strong>%(mimetype_label)s:<strong></td><td align="left">%(mimetype)s</td></tr><tr><td align="right"><strong>%(checksum_label)s:<strong></td><td align="left">%(md5)s</td></tr><tbody></table>'
                    };
                    $('#file_%(id)s').qtip(tooltip);
                });
            //]]></script>""" % {
                'file_label': escape(_('file')),
                'id': escape(publicationid, True),
                'filename': filename,
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
