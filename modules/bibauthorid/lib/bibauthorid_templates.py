# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2011 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Bibauthorid HTML templates"""

# pylint: disable=W0105

#from cgi import escape
#from urllib import quote
#
from invenio.config import CFG_SITE_LANG
from invenio.config import CFG_SITE_URL
from invenio.config import CFG_SITE_SUPPORT_EMAIL
from invenio.bibformat import format_record
from invenio.session import get_session
from invenio.search_engine import get_fieldvalues
from invenio.webuser import collect_user_info
from invenio.webuser import getUid
from invenio.bibauthorid_webapi import get_bibref_name_string, get_person_redirect_link
from invenio.messages import gettext_set_language, wash_language
#from invenio.textutils import encode_for_xml

class Template:
    """Templating functions used by aid"""

    def __init__(self, language=CFG_SITE_LANG):
        """Set defaults for all aid template output"""

        self.language = language
        self._ = gettext_set_language(wash_language(language))


    def tmpl_person_detail_layout(self, content):
        '''
        writes HTML content into the person css container

        @param content: HTML content
        @type content: string

        @return: HTML code
        @rtype: string
        '''
        html = []
        h = html.append
        h('<div id="aid_person">')
        h(content)
        h('</div>')

        return "\n".join(html)


    def tmpl_notification_box(self, message, teaser="Notice:", show_close_btn=True):
        '''
        Creates a notification box based on the jQuery UI style

        @param message: message to display in the box
        @type message: string
        @param teaser: Teaser text in bold next to icon
        @type teaser: string
        @param show_close_btn: display close button [x]
        @type show_close_btn: boolean

        @return: HTML code
        @rtype: string
        '''
        html = []
        h = html.append
        h('<div id="aid_notification" class="ui-widget">')
        h('  <div style="margin-top: 20px; padding: 0pt 0.7em;" class="ui-state-highlight ui-corner-all">')
        h('    <p><span style="float: left; margin-right: 0.3em;" class="ui-icon ui-icon-info"></span>')
        h('    <strong>%s</strong> %s' % (teaser, message))

        if show_close_btn:
            h('    <span style="float:right; margin-right: 0.3em;"><a href="#" class="aid_close-notify">X</a></span></p>')

        h(' </div>')
        h('</div>')

        return "\n".join(html)


    def tmpl_error_box(self, message, teaser="Alert:", show_close_btn=True):
        '''
        Creates an error box based on the jQuery UI style

        @param message: message to display in the box
        @type message: string
        @param teaser: Teaser text in bold next to icon
        @type teaser: string
        @param show_close_btn: display close button [x]
        @type show_close_btn: boolean

        @return: HTML code
        @rtype: string
        '''
        html = []
        h = html.append
        h('<div id="aid_notification" class="ui-widget">')
        h('  <div style="margin-top: 20px; padding: 0pt 0.7em;" class="ui-state-error ui-corner-all">')
        h('    <p><span style="float: left; margin-right: 0.3em;" class="ui-icon ui-icon-alert"></span>')
        h('    <strong>%s</strong> %s' % (teaser, message))

        if show_close_btn:
            h('    <span style="float:right; margin-right: 0.3em;"><a href="#" class="aid_close-notify">X</a></span></p>')

        h(' </div>')
        h('</div>')

        return "\n".join(html)


    def tmpl_ticket_box(self, teaser, message, ticket, show_close_btn=True):
        '''
        Creates a semi-permanent box informing about ticket
        status notifications

        @param message: message to display in the box
        @type message: string
        @param teaser: Teaser text in bold next to icon
        @type teaser: string
        @param ticket: The ticket object from the session
        @param ticket: list of dict
        @param show_close_btn: display close button [x]
        @type show_close_btn: boolean

        @return: HTML code
        @rtype: string
        '''
        html = []
        h = html.append
        h('<div id="aid_notification" class="ui-widget">')
        h('  <div style="margin-top: 20px; padding: 0pt 0.7em;" class="ui-state-highlight ui-corner-all">')
        h('    <p><span style="float: left; margin-right: 0.3em;" class="ui-icon ui-icon-info"></span>')
        h('    <strong>%s</strong> %s ' % (teaser, message))
        h('<a id="checkout" href="action?checkout=True">'+ self._('Click here to review the transactions.')+ '</a>')
        h('<br>')

        if show_close_btn:
            h('    <span style="float:right; margin-right: 0.3em;"><a href="#" class="aid_close-notify">X</a></span></p>')

        h(' </div>')
        h('</div>')

        return "\n".join(html)

    def tmpl_search_ticket_box(self, teaser, message, search_ticket, show_close_btn=False):
        '''
        Creates a box informing about a claim in progress for
        the search.

        @param message: message to display in the box
        @type message: string
        @param teaser: Teaser text in bold next to icon
        @type teaser: string
        @param search_ticket: The search ticket object from the session
        @param search_ticket: list of dict
        @param show_close_btn: display close button [x]
        @type show_close_btn: boolean

        @return: HTML code
        @rtype: string
        '''
        html = []
        h = html.append
        h('<div id="aid_notification" class="ui-widget">')
        h('  <div style="margin-top: 20px; padding: 0pt 0.7em;" class="ui-state-highlight ui-corner-all">')
        h('    <p><span style="float: left; margin-right: 0.3em;" class="ui-icon ui-icon-info"></span>')
        h('    <strong>%s</strong> %s ' % (teaser, message))
        h("<ul>")
        for paper in search_ticket['bibrefs']:
            if ',' in paper:
                pbibrec = paper.split(',')[1]
            else:
                pbibrec = paper
            h("<li>%s</li>"
                   % (format_record(pbibrec, "ha", on_the_fly=True)))
        h("</ul>")
        h('<a id="checkout" href="action?cancel_search_ticket=True">'+self._('Quit searching.')+ '</a>')
#        h('DBGticket - ' + str(search_ticket))

        if show_close_btn:
            h('    <span style="float:right; margin-right: 0.3em;"><a href="#" class="aid_close-notify">X</a></span></p>')

        h(' </div>')
        h('</div>')
        h('<p>&nbsp;</p>')

        return "\n".join(html)


    def tmpl_meta_includes(self, kill_browser_cache=False):
        '''
        Generates HTML code for the header section of the document
        META tags to kill browser caching
        Javascript includes
        CSS definitions

        @param kill_browser_cache: Do we want to kill the browser cache?
        @type kill_browser_cache: boolean
        '''

        js_path = "%s/js" % CFG_SITE_URL
        imgcss_path = "%s/img" % CFG_SITE_URL

        result = []
        # Add browser cache killer, hence some notifications are not displayed
        # out of the session.
        if kill_browser_cache:
            result = [
                '<META HTTP-EQUIV="Pragma" CONTENT="no-cache">',
                '<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">',
                '<META HTTP-EQUIV="Pragma-directive" CONTENT="no-cache">',
                '<META HTTP-EQUIV="Cache-Directive" CONTENT="no-cache">',
                '<META HTTP-EQUIV="Expires" CONTENT="0">']

        scripts = ["jquery-1.4.4.js",
                   "ui.core.js",
                   "jquery.ui.widget.min.js",
                   "jquery.ui.tabs.min.js",
                   "jquery.form.js",
                   "jquery.dataTables.min.js",
                   "jquery.ui.mouse.min.js",
                   "jquery.ui.draggable.min.js",
                   "jquery.ui.position.min.js",
                   "jquery.ui.resizable.min.js",
                   "jquery.ui.button.min.js",
                   "jquery.ui.dialog.min.js",
                   "bibauthorid.js"]

        result.append('<link rel="stylesheet" type="text/css" href='
                      '"%s/jquery-ui/themes/smoothness/jquery-ui.css" />'
                      % (imgcss_path))
        result.append('<link rel="stylesheet" type="text/css" href='
                      '"%s/datatables_jquery-ui.css" />'
                      % (imgcss_path))
        result.append('<link rel="stylesheet" type="text/css" href='
                      '"%s/bibauthorid.css" />'
                      % (imgcss_path))

        for script in scripts:
            result.append('<script type="text/javascript" src="%s/%s">'
                      '</script>' % (js_path, script))

        return "\n".join(result)


    def tmpl_author_confirmed(self, bibref, pid, verbiage_dict = {'alt_confirm':'Confirmed.',
                                                                       'confirm_text':'This record assignment has been confirmed.',
                                                                       'alt_forget':'Forget decision!',
                                                                       'forget_text':'Forget assignment decision',
                                                                       'alt_repeal':'Repeal!',
                                                                       'repeal_text':'Repeal record assignment',
                                                                       'to_other_text':'Assign to another person',
                                                                       'alt_to_other':'To other person!'
                                                                       }):
        '''
        Generate play per-paper links for the table for the
        status "confirmed"

        @param bibref: construct of unique ID for this author on this paper
        @type bibref: string
        @param pid: the Person ID
        @type pid: int
        @param verbiage_dict: language for the link descriptions
        @type verbiage_dict: dict
        '''
        return ('<!--2!--><span id="aid_status_details"> '
                '<img src="%(url)s/img/aid_check.png" alt="%(alt_confirm)s" />'
                '%(confirm_text)s <br>'
                '<a id="aid_reset_gr" class="aid_grey" href="%(url)s/person/action?reset=True&selection=%(ref)s&pid=%(pid)s">'
                '<img src="%(url)s/img/aid_reset_gray.png" alt="%(alt_forget)s" style="margin-left:22px;" />'
                '%(forget_text)s</a><br>'
                '<a id="aid_repeal" class="aid_grey" href="%(url)s/person/action?repeal=True&selection=%(ref)s&pid=%(pid)s">'
                '<img src="%(url)s/img/aid_reject_gray.png" alt="%(alt_repeal)s" style="margin-left:22px;"/>'
                '%(repeal_text)s</a><br>'
                '<a id="aid_to_other" class="aid_grey" href="%(url)s/person/action?to_other_person=True&selection=%(ref)s">'
                '<img src="%(url)s/img/aid_to_other_gray.png" alt="%(alt_to_other)s" style="margin-left:22px;"/>'
                '%(to_other_text)s</a> </span>'
                % ({'url': CFG_SITE_URL, 'ref': bibref, 'pid': pid,
                    'alt_confirm':verbiage_dict['alt_confirm'],
                    'confirm_text':verbiage_dict['confirm_text'],
                    'alt_forget':verbiage_dict['alt_forget'],
                    'forget_text':verbiage_dict['forget_text'],
                    'alt_repeal':verbiage_dict['alt_repeal'],
                    'repeal_text':verbiage_dict['repeal_text'],
                    'to_other_text':verbiage_dict['to_other_text'],
                    'alt_to_other':verbiage_dict['alt_to_other']}))


    def tmpl_author_repealed(self, bibref, pid, verbiage_dict = {'alt_confirm':'Confirm!',
                                                                       'confirm_text':'Confirm record assignment.',
                                                                       'alt_forget':'Forget decision!',
                                                                       'forget_text':'Forget assignment decision',
                                                                       'alt_repeal':'Rejected!',
                                                                       'repeal_text':'Repeal this record assignment.',
                                                                       'to_other_text':'Assign to another person',
                                                                       'alt_to_other':'To other person!'
                                                                       }):
        '''
        Generate play per-paper links for the table for the
        status "repealed"

        @param bibref: construct of unique ID for this author on this paper
        @type bibref: string
        @param pid: the Person ID
        @type pid: int
        @param verbiage_dict: language for the link descriptions
        @type verbiage_dict: dict
        '''
        return ('<!---2!--><span id="aid_status_details"> '
                '<img src="%(url)s/img/aid_reject.png" alt="%(alt_repeal)s" />'
                '%(repeal_text)s <br>'
                '<a id="aid_reset" class="aid_grey" href="%(url)s/person/action?reset=True&selection=%(ref)s&pid=%(pid)s">'
                '<img src="%(url)s/img/aid_reset_gray.png" alt="%(alt_forget)s" style="margin-left: 22px;" />'
                '%(forget_text)s</a><br>'
                '<a id="aid_confirm" class="aid_grey" href="%(url)s/person/action?confirm=True&selection=%(ref)s&pid=%(pid)s">'
                '<img src="%(url)s/img/aid_check_gray.png" alt="%(alt_confirm)s" style="margin-left: 22px;" />'
                '%(confirm_text)s</a><br>'
                '<a id="aid_to_other" class="aid_grey" href="%(url)s/person/action?to_other_person=True&selection=%(ref)s">'
                '<img src="%(url)s/img/aid_to_other_gray.png" alt="%(alt_to_other)s" style="margin-left:22px;"/>'
                '%(to_other_text)s</a> </span>'
                % ({'url': CFG_SITE_URL, 'ref': bibref, 'pid': pid,
                    'alt_confirm':verbiage_dict['alt_confirm'],
                    'confirm_text':verbiage_dict['confirm_text'],
                    'alt_forget':verbiage_dict['alt_forget'],
                    'forget_text':verbiage_dict['forget_text'],
                    'alt_repeal':verbiage_dict['alt_repeal'],
                    'repeal_text':verbiage_dict['repeal_text'],
                    'to_other_text':verbiage_dict['to_other_text'],
                    'alt_to_other':verbiage_dict['alt_to_other']}))


    def tmpl_author_undecided(self, bibref, pid, verbiage_dict = {'alt_confirm':'Confirm!',
                                                                       'confirm_text':'Confirm record assignment.',
                                                                       'alt_repeal':'Rejected!',
                                                                       'repeal_text':'This record has been repealed.',
                                                                       'to_other_text':'Assign to another person',
                                                                       'alt_to_other':'To other person!'
                                                                       }):
        '''
        Generate play per-paper links for the table for the
        status "no decision taken yet"

        @param bibref: construct of unique ID for this author on this paper
        @type bibref: string
        @param pid: the Person ID
        @type pid: int
        @param verbiage_dict: language for the link descriptions
        @type verbiage_dict: dict
        '''
        #batchprocess?mconfirm=True&bibrefs=['100:17,16']&pid=1
        return ('<!--0!--><span id="aid_status_details"> '
                '<a id="aid_confirm" href="%(url)s/person/action?confirm=True&selection=%(ref)s&pid=%(pid)s">'
                '<img src="%(url)s/img/aid_check.png" alt="%(alt_confirm)s" />'
                '%(confirm_text)s</a><br />'
                '<a id="aid_repeal" href="%(url)s/person/action?repeal=True&selection=%(ref)s&pid=%(pid)s">'
                '<img src="%(url)s/img/aid_reject.png" alt="%(alt_repeal)s" />'
                '%(repeal_text)s</a> <br />'
                '<a id="aid_to_other" href="%(url)s/person/action?to_other_person=True&selection=%(ref)s">'
                '<img src="%(url)s/img/aid_to_other.png" alt="%(alt_to_other)s" />'
                '%(to_other_text)s</a> </span>'
                % ({'url': CFG_SITE_URL, 'ref': bibref, 'pid': pid,
                    'alt_confirm':verbiage_dict['alt_confirm'],
                    'confirm_text':verbiage_dict['confirm_text'],
                    'alt_repeal':verbiage_dict['alt_repeal'],
                    'repeal_text':verbiage_dict['repeal_text'],
                    'to_other_text':verbiage_dict['to_other_text'],
                    'alt_to_other':verbiage_dict['alt_to_other']}))


    def tmpl_open_claim(self, bibrefs, pid, last_viewed_pid,
                        search_enabled=True):
        '''
        Generate entry page for "claim or attribute this paper"

        @param bibref: construct of unique ID for this author on this paper
        @type bibref: string
        @param pid: the Person ID
        @type pid: int
        @param last_viewed_pid: last ID that had been subject to an action
        @type last_viewed_pid: int
        '''
        t_html = []
        h = t_html.append
        h(self._('You are about to attribute the following paper'))
        if len(bibrefs) > 1:
            h('s: <br>')
        else:
            h(': <br>')
        h("<ul>")
        bibs = ''
        for paper in bibrefs:
            if bibs:
                bibs = bibs + '&'
            bibs = bibs + 'selection=' + str(paper)
            if ',' in paper:
                pbibrec = paper.split(',')[1]
            else:
                pbibrec = paper
            h("<li>%s</li>"
                       % (format_record(pbibrec, "ha", on_the_fly=True)))
            h("</ul>")

        pp_html = []
        h = pp_html.append
        h(self.tmpl_notification_box("\n".join(t_html),
                                     self._("Info"), False))
        h('<p> Your options: </p>')

        if pid > -1:
            h(('<a id="clam_for_myself" href="%s/person/action?confirm=True&%s&pid=%s"> Claim for yourself </a> <br>')
              % (CFG_SITE_URL, bibs, str(pid)))

        if last_viewed_pid:
            h(('<a id="clam_for_last_viewed" href="%s/person/action?confirm=True&%s&pid=%s"> Attribute to %s </a> <br>')
              % (CFG_SITE_URL, bibs, str(last_viewed_pid[0]), last_viewed_pid[1]))

        if search_enabled:
            h(('<a id="claim_search" href="%s/person/action?to_other_person=True&%s">'+self._(' Search for a person to attribute the paper to')+' </a> <br>')
                  % (CFG_SITE_URL, bibs))

        return "\n".join(pp_html)


    def __tmpl_admin_records_table(self, form_id, person_id, bibrecids, verbiage_dict = {'no_doc_string':'Sorry, there are currently no documents to be found in this category.',
                                                                                              'b_confirm':'Confirm',
                                                                                              'b_repeal':'Repeal',
                                                                                              'b_to_others':'Assign to other person',
                                                                                              'b_forget':'Forget decision'},
                                                                            buttons_verbiage_dict = {'mass_buttons':{'no_doc_string':'Sorry, there are currently no documents to be found in this category.',
                                                                                                      'b_confirm':'Confirm',
                                                                                                      'b_repeal':'Repeal',
                                                                                                      'b_to_others':'Assign to other person',
                                                                                                      'b_forget':'Forget decision'},
                                                                                     'record_undecided':{'alt_confirm':'Confirm!',
                                                                                                         'confirm_text':'Confirm record assignment.',
                                                                                                         'alt_repeal':'Rejected!',
                                                                                                         'repeal_text':'This record has been repealed.'},
                                                                                     'record_confirmed':{'alt_confirm':'Confirmed.',
                                                                                                           'confirm_text':'This record assignment has been confirmed.',
                                                                                                           'alt_forget':'Forget decision!',
                                                                                                           'forget_text':'Forget assignment decision',
                                                                                                           'alt_repeal':'Repeal!',
                                                                                                           'repeal_text':'Repeal record assignment'},
                                                                                     'record_repealed':{'alt_confirm':'Confirm!',
                                                                                                        'confirm_text':'Confirm record assignment.',
                                                                                                        'alt_forget':'Forget decision!',
                                                                                                        'forget_text':'Forget assignment decision',
                                                                                                        'alt_repeal':'Rejected!',
                                                                                                        'repeal_text':'Repeal this record assignment.'}}):
        '''
        Generate the big tables for the person overview page

        @param form_id: name of the form
        @type form_id: string
        @param person_id: Person ID
        @type person_id: int
        @param bibrecids: List of records to display
        @type bibrecids: list
        @param verbiage_dict: language for the elements
        @type verbiage_dict: dict
        @param buttons_verbiage_dict: language for the buttons
        @type buttons_verbiage_dict: dict
        '''
        no_papers_html = ['<div style="text-align:left;margin-top:1em;"><strong>']
        no_papers_html.append('%s' % verbiage_dict['no_doc_string'])
        no_papers_html.append('</strong></div>')

        if not bibrecids or not person_id:
            return "\n".join(no_papers_html)

        pp_html = []
        h = pp_html.append
        h('<form id="%s" action="/person/action" method="post">'
                   % (form_id))
        h('<table  class="paperstable" cellpadding="3" width="100%">')
        h("<thead>")
        h("  <tr>")
        h('    <th>&nbsp;</th>')
        h('    <th>Paper Short Info</th>')
        h("    <th>Author Name</th>")
        h("    <th>Affiliation</th>")
#        h("    <th>Date</th>")
        h("    <th>Actions</th>")
        h("  </tr>")
        h("</thead>")
        h("<tbody>")

        for paper in bibrecids:
            h('  <tr style="padding-top: 6px; padding-bottom: 6px;">')

            h('    <td><input type="checkbox" name="selection" '
                           'value="%s" /> </td>' % (paper['bibref']))
            rec_info = format_record(paper['recid'], "ha", on_the_fly=True)

            h("    <td>%s</td>" % (rec_info))
            h("    <td>%s</td>" % (paper['authorname'].encode("utf-8")))
            aff = ""

            if paper['authoraffiliation']:
                aff = paper['authoraffiliation'].encode("utf-8")
            else:
                aff = "unknown"

            h("    <td>%s</td>" % (aff))
#            h("    <td>%s</td>" % (paper['paperdate']))
            paper_status = self._("No status information found.")

            if paper['flag'] == 2:
                paper_status = self.tmpl_author_confirmed(paper['bibref'], person_id, verbiage_dict=buttons_verbiage_dict['record_confirmed'])
            elif paper['flag'] == -2:
                paper_status = self.tmpl_author_repealed(paper['bibref'], person_id,verbiage_dict=buttons_verbiage_dict['record_repealed'] )
            else:
                paper_status = self.tmpl_author_undecided(paper['bibref'], person_id, verbiage_dict=buttons_verbiage_dict['record_undecided'])

            h('    <td><div id="bibref%s"><!--%s!-->%s &nbsp;</div></td>'
                           % (paper['bibref'], paper['flag'], paper_status))
            h("  </tr>")

        h("  </tbody>")
        h("</table>")

        h('<div class="aid_reclist_selector">'+self._(' On all pages: '))
        h('<a rel="group_1" href="#select_all">'+self._('Select All')+'</a> | ')
        h('<a rel="group_1" href="#select_none">'+self._('Select None')+'</a> | ')
        h('<a rel="group_1" href="#invert_selection">'+self._('Invert Selection')+'</a>')
        h('</div>')

        h('<div class="aid_reclist_buttons">')
        h(('<img src="%s/img/aid_90low_right.png" alt="∟" />'+self._(' With selected do: '))
          % (CFG_SITE_URL))
        h('<input type="hidden" name="pid" value="%s" />' % (person_id))
        h('<input type="submit" name="confirm" value="%s" class="aid_btn_blue" />' % verbiage_dict['b_confirm'])
        h('<input type="submit" name="repeal" value="%s" class="aid_btn_blue" />' % verbiage_dict['b_repeal'])
        h('<input type="submit" name="to_other_person" value="%s" class="aid_btn_blue" />' % verbiage_dict['b_to_others'])
        h('<input type="submit" name="reset" value="%s" class="aid_btn_blue" />' % verbiage_dict['b_forget'])
        h("  </div>")
        h('</form>')

        return "\n".join(pp_html)


    def __tmpl_reviews_table(self, person_id, bibrecids, admin=False):
        '''
        Generate the table for potential reviews.

        @param form_id: name of the form
        @type form_id: string
        @param person_id: Person ID
        @type person_id: int
        @param bibrecids: List of records to display
        @type bibrecids: list
        @param admin: Show admin functions
        @type admin: boolean
        '''
        no_papers_html = ['<div style="text-align:left;margin-top:1em;"><strong>']
        no_papers_html.append(self._('Sorry, there are currently no records to be found in this category.'))
        no_papers_html.append('</strong></div>')

        if not bibrecids or not person_id:
            return "\n".join(no_papers_html)

        pp_html = []
        h = pp_html.append
        h('<form id="review" action="/person/batchprocess" method="post">')
        h('<table  class="reviewstable" cellpadding="3" width="100%">')
        h("  <thead>")
        h("    <tr>")
        h('      <th>&nbsp;</th>')
        h('      <th>Paper Short Info</th>')
        h("      <th>Actions</th>")
        h("    </tr>")
        h("  </thead>")
        h("  <tbody>")

        for paper in bibrecids:
            h('  <tr>')
            h('    <td><input type="checkbox" name="selected_bibrecs" '
                       'value="%s" /> </td>' % (paper))
            rec_info = format_record(paper[0], "ha", on_the_fly=True)

            if not admin:
                rec_info = rec_info.replace("person/search?q=", "author/")

            h("    <td>%s</td>" % (rec_info))
            h('    <td><a href="/person/batchprocess?selected_bibrecs=%s&mfind_bibref=claim">'+self._('Review Transaction')+'</a></td>'
                           % (paper))
            h("  </tr>")

        h("  </tbody>")
        h("</table>")

        h('<div style="text-align:left;">'+self._(' On all pages: '))
        h('<a rel="group_1" href="#select_all">'+self._('Select All')+'</a> | ')
        h('<a rel="group_1" href="#select_none">'+self._('Select None')+'</a> | ')
        h('<a rel="group_1" href="#invert_selection">'+self._('Invert Selection')+'</a>')
        h('</div>')

        h('<div style="vertical-align:middle;">')
        h('∟ With selected do: ')
        h('<input type="hidden" name="pid" value="%s" />' % (person_id))
        h('<input type="hidden" name="mfind_bibref" value="claim" />')
        h('<input type="submit" name="submit" value="Review selected transactions" />')
        h("  </div>")
        h('</form>')

        return "\n".join(pp_html)


    def tmpl_admin_person_info_box(self, ln, person_id= -1, names=[]):
        '''
        Generate the box showing names

        @param ln: the language to use
        @type ln: string
        @param person_id: Person ID
        @type person_id: int
        @param names: List of names to display
        @type names: list
        '''
        html = []
        h = html.append
        #class="ui-tabs ui-widget ui-widget-content ui-corner-all">
        h('<div id="aid_person_names"')
        h('<p><strong>'+self._('Names of the person as collected from the records attached')+'</strong></p>')
        h("<p>")
        h('<!--<span class="aid_lowlight_text">Person ID: <span id="pid%s">%s</span></span><br />!-->'
                      % (person_id, person_id))

        for name in names:
            h(("%s "+self._('as appeared on')+" %s"+self._(' records')+"<br />")
                             % (name[0], name[1]))

        h("</p>")
        h("</div>")

        return "\n".join(html)


    def tmpl_admin_tabs(self, ln=CFG_SITE_LANG, person_id= -1,
                        rejected_papers=[],
                        rest_of_papers=[],
                        review_needed=[],
                        rt_tickets=[],
                        open_rt_tickets=[],
                        show_tabs=['records', 'repealed', 'review', 'comments', 'tickets', 'data'],
                        ticket_links=['delete', 'commit', 'del_entry', 'commit_entry'],
                        verbiage_dict={'confirmed':'Records','repealed':'Not this person\'s records',
                                         'review':'Records in need of review',
                                         'tickets':'Open Tickets','data':'Data',
                                         'confirmed_ns':'Papers of this Person',
                                         'repealed_ns':'Papers _not_ of this Person',
                                         'review_ns':'Papers in need of review',
                                         'tickets_ns':'Tickets for this Person',
                                         'data_ns':'Additional Data for this Person'},
                        buttons_verbiage_dict = {'mass_buttons':{'no_doc_string':'Sorry, there are currently no documents to be found in this category.',
                                                                  'b_confirm':'Confirm',
                                                                  'b_repeal':'Repeal',
                                                                  'b_to_others':'Assign to other person',
                                                                  'b_forget':'Forget decision'},
                                                 'record_undecided':{'alt_confirm':'Confirm!',
                                                                     'confirm_text':'Confirm record assignment.',
                                                                     'alt_repeal':'Rejected!',
                                                                     'repeal_text':'This record has been repealed.'},
                                                 'record_confirmed':{'alt_confirm':'Confirmed.',
                                                                       'confirm_text':'This record assignment has been confirmed.',
                                                                       'alt_forget':'Forget decision!',
                                                                       'forget_text':'Forget assignment decision',
                                                                       'alt_repeal':'Repeal!',
                                                                       'repeal_text':'Repeal record assignment'},
                                                 'record_repealed':{'alt_confirm':'Confirm!',
                                                                    'confirm_text':'Confirm record assignment.',
                                                                    'alt_forget':'Forget decision!',
                                                                    'forget_text':'Forget assignment decision',
                                                                    'alt_repeal':'Rejected!',
                                                                    'repeal_text':'Repeal this record assignment.'}}):
        '''
        Generate the tabs for the person overview page

        @param ln: the language to use
        @type ln: string
        @param person_id: Person ID
        @type person_id: int
        @param rejected_papers: list of repealed papers
        @type rejected_papers: list
        @param rest_of_papers: list of attributed of undecided papers
        @type rest_of_papers: list
        @param review_needed: list of papers that need a review (choose name)
        @type review_needed:list
        @param rt_tickets: list of tickes for this Person
        @type rt_tickets: list
        @param open_rt_tickets: list of open request tickets
        @type open_rt_tickets: list
        @param show_tabs: list of tabs to display
        @type show_tabs: list of strings
        @param ticket_links: list of links to display
        @type ticket_links: list of strings
        @param verbiage_dict: language for the elements
        @type verbiage_dict: dict
        @param buttons_verbiage_dict: language for the buttons
        @type buttons_verbiage_dict: dict
        '''
        html = []
        h = html.append

        h('<div id="aid_tabbing">')
        h('  <ul>')
        if 'records' in show_tabs:
            r = verbiage_dict['confirmed']
            h('    <li><a href="#tabRecords"><span>%(r)s (%(l)s)</span></a></li>' % ({'r':r,'l':len(rest_of_papers)}))
        if 'repealed' in show_tabs:
            r = verbiage_dict['repealed']
            h('    <li><a href="#tabNotRecords"><span>%(r)s (%(l)s)</span></a></li>' % ({'r':r,'l':len(rejected_papers)}))
        if 'review' in show_tabs:
            r = verbiage_dict['review']
            h('    <li><a href="#tabReviewNeeded"><span>%(r)s (%(l)s)</span></a></li>' % ({'r':r,'l':len(review_needed)}))
        if 'tickets' in show_tabs:
            r = verbiage_dict['tickets']
            h('    <li><a href="#tabTickets"><span>%(r)s (%(l)s)</span></a></li>' % ({'r':r, 'l':len(open_rt_tickets)}))
        if 'data' in show_tabs:
            r = verbiage_dict['data']
            h('    <li><a href="#tabData"><span>%s</span></a></li>' % r)
        h('  </ul>')

        if 'records' in show_tabs:
            h('  <div id="tabRecords">')
            r = verbiage_dict['confirmed_ns']
            h('<noscript><h5>%s</h5></noscript>' % r)
            h(self.__tmpl_admin_records_table("massfunctions",
                                             person_id, rest_of_papers, verbiage_dict = buttons_verbiage_dict['mass_buttons'], buttons_verbiage_dict = buttons_verbiage_dict))
            h("  </div>")

        if 'repealed' in show_tabs:
            h('  <div id="tabNotRecords">')
            r = verbiage_dict['repealed_ns']
            h('<noscript><h5>%s</h5></noscript>' % r)
            h(self._('These records have been marked as not being from this person.'))
            h('<br />'+self._('They will be regarded in the next run of the author ')
              +self._('disambiguation algorithm and might disappear from this listing.'))
            h(self.__tmpl_admin_records_table("rmassfunctions",
                                             person_id, rejected_papers, verbiage_dict = buttons_verbiage_dict['mass_buttons'], buttons_verbiage_dict = buttons_verbiage_dict))
            h("  </div>")

        if 'review' in show_tabs:
            h('  <div id="tabReviewNeeded">')
            r = verbiage_dict['review_ns']
            h('<noscript><h5>%s</h5></noscript>' % r)
            h(self.__tmpl_reviews_table(person_id, review_needed, True))
            h('  </div>')
        if 'tickets' in show_tabs:
            h('  <div id="tabTickets">')
            r = verbiage_dict['tickets']
            h('<noscript><h5>%s</h5></noscript>' % r)
            r = verbiage_dict['tickets_ns']
            h('<p>%s:</p>' % r)
    #        if rt_tickets:
    #            open_rt_tickets = [a for a in open_rt_tickets if a[1] == rt_tickets]

            for t in open_rt_tickets:
                name = self._('Not provided')
                surname = self._('Not provided')
                uidip = self._('Not available')
                comments = self._('No comments')
                email = self._('Not provided')
                date = self._('Not Available')
                actions = []

                for info in t[0]:
                    if info[0] == 'firstname':
                        name = info[1]
                    elif info[0] == 'lastname':
                        surname = info[1]
                    elif info[0] == 'uid-ip':
                        uidip = info[1]
                    elif info[0] == 'comments':
                        comments = info[1]
                    elif info[0] == 'email':
                        email = info[1]
                    elif info[0] == 'date':
                        date = info[1]
                    elif info[0] in ['confirm', 'repeal']:
                        actions.append(info)

                if 'delete' in ticket_links:
                    h(('<strong>Ticket number: %(tnum)s </strong> <a id="cancel" href=%(url)s/person/action?cancel_rt_ticket=True&selection=%(tnum)s&pid=%(pid)s>'+self._(' Delete this ticket')+' </a>')
                  % ({'tnum':t[1], 'url':CFG_SITE_URL, 'pid':str(person_id)}))
                if 'commit' in ticket_links:
                    h((' or <a id="commit" href=%(url)s/person/action?commit_rt_ticket=True&selection=%(tnum)s&pid=%(pid)s>'+self._(' Commit this entire ticket')+' </a> <br>')
                  % ({'tnum':t[1], 'url':CFG_SITE_URL, 'pid':str(person_id)}))
                h('<dd>')
                h('Open from: %s, %s <br>' % (surname, name))
                h('Date: %s <br>' % date)
                h('identified by: %s <br>' % uidip)
                h('email: %s <br>' % email)
                h('comments: %s <br>' % comments)
                h('Suggested actions: <br>')
                h('<dd>')
                for a in actions:
                    bibref, bibrec = a[1].split(',')
                    pname = get_bibref_name_string(bibref)
                    title = get_fieldvalues(int(bibrec), "245__a")[0]
                    if 'commit_entry' in ticket_links:
                        h('<a id="action" href="%(url)s/person/action?%(action)s=True&pid=%(pid)s&selection=%(bib)s&rt_id=%(rt)s">%(action)s - %(name)s on %(title)s </a>'
                      % ({'action':a[0], 'url':CFG_SITE_URL, 'pid':str(person_id), 'bib':a[1], 'name':pname, 'title':title, 'rt':t[1]}))
                    else:
                        h('%(action)s - %(name)s on %(title)s'
                      % ({'action':a[0], 'url':CFG_SITE_URL, 'pid':str(person_id), 'bib':a[1], 'name':pname, 'title':title, 'rt':t[1]}))
                    if 'del_entry' in ticket_links:
                        h(' - <a id="action" href="%(url)s/person/action?cancel_rt_ticket=True&pid=%(pid)s&selection=%(bib)s&rt_id=%(rt)s&rt_action=%(action)s"> Delete this entry </a> <br>'
                      % ({'action':a[0], 'url':CFG_SITE_URL, 'pid':str(person_id), 'bib':a[1], 'name':pname, 'title':title, 'rt':t[1]}))
                h('</dd>')
                h('</dd><br>')
#            h(str(open_rt_tickets))
            h("  </div>")

        if 'data' in show_tabs:
            h('  <div id="tabData">')
            r = verbiage_dict['data_ns']
            h('<noscript><h5>%s</h5></noscript>' % r)
            h('  <b>' +self._('This tab is currently under construction')+'</p>')
            h("  </div>")

        h("</div>")

        return "\n".join(html)


    def tmpl_bibref_check(self, bibrefs_auto_assigned, bibrefs_to_confirm):
        '''
        Generate overview to let user chose the name on the paper that
        resembles the person in question.

        @param bibrefs_auto_assigned: list of auto-assigned papers
        @type bibrefs_auto_assigned: list
        @param bibrefs_to_confirm: list of unclear papers and names
        @type bibrefs_to_confirm: list
        '''
        html = []
        h = html.append
        h('<form id="review" action="/person/action" method="post">')
        h('<p><strong>'+self._('We could not reliably determine the name of the author on the records below to automatically perform an assignment.')
          +'</strong></p>')
        h('<p>'+self._('Please select an author for the records in question.')+'<br/>')
        h(self._('Boxes not selected will be ignored in the process.'))
        h('</p>')

        for person in bibrefs_to_confirm:
            if not "bibrecs" in bibrefs_to_confirm[person]:
                continue

            h((self._("Select name for")+" %s") % bibrefs_to_confirm[person]["person_name"])
            pid = person

            for recid in bibrefs_to_confirm[person]["bibrecs"]:
                h('<div id="aid_moreinfo">')

                try:
                    fv = get_fieldvalues(int(recid), "245__a")[0]
                except (ValueError, IndexError, TypeError):
                    fv = self._('Error retrieving record title')

                h(self._("Paper title: ") + fv)
                h('<select name="bibrecgroup%s">' % (recid))
                h('<option value="" selected>-- Ignore --</option>')

                for bibref in bibrefs_to_confirm[person]["bibrecs"][recid]:
                    h('<option value="%s||%s">%s</option>'
                      % (pid, bibref[0], bibref[1]))

                h('</select>')
                h("</div>")

        if bibrefs_auto_assigned:
            h(self._('The following names have been automatically chosen:'))
            for person in bibrefs_auto_assigned:
                if not "bibrecs" in bibrefs_auto_assigned[person]:
                    continue

                h((self._("For")+" %s:") % bibrefs_auto_assigned[person]["person_name"])
                pid = person

                for recid in bibrefs_auto_assigned[person]["bibrecs"]:
                    try:
                        fv = get_fieldvalues(int(recid), "245__a")[0]
                    except (ValueError, IndexError, TypeError):
                        fv = self._('Error retrieving record title')

                    h('<div id="aid_moreinfo">')
                    h(('%s' + self._('with name: '))
                      % (fv))
                    #, bibrefs_auto_assigned[person]["bibrecs"][recid][0][1]))
                    # asbibref = "%s||%s" % (person, bibrefs_auto_assigned[person]["bibrecs"][recid][0][0])
                    pbibref = bibrefs_auto_assigned[person]["bibrecs"][recid][0][0]
                    h('<select name="bibrecgroup%s">' % (recid))
                    h('<option value="" selected>-- '+self._('Ignore')+' --</option>')

                    for bibref in bibrefs_auto_assigned[person]["bibrecs"][recid]:
                        selector = ""

                        if bibref[0] == pbibref:
                            selector = ' selected="selected"'

                        h('<option value="%s||%s"%s>%s</option>'
                          % (pid, bibref[0], selector, bibref[1]))

                    h('</select>')
#                    h('<input type="hidden" name="bibrecgroup%s" value="%s" />'
#                      % (recid, asbibref))
                    h('</div>')

        h('<div style="text-align:center;">')
        h('  <input type="submit" class="aid_btn_green" name="bibref_check_submit" value="Accept" />')
        h('  <input type="submit" class="aid_btn_blue" name="cancel_stage" value="Cancel" />')
        h("</div>")
        h('</form>')

        return "\n".join(html)


    def tmpl_invenio_search_box(self):
        '''
        Generate little search box for missing papers. Links to main invenio
        search on start papge.
        '''
        html = []
        h = html.append
        h('<div style="margin-top: 15px;"> <strong>Search for missing papers:</strong> <form method="GET" action="%s/search">' % CFG_SITE_URL)
        h('<input name="p" id="p" type="text" style="border:1px solid #333; width:500px;" /> ')
        h('<input type="submit" name="action_search" value="search" '
          'class="aid_btn_blue" />')
        h('</form> </div>')

        return "\n".join(html)


    def tmpl_person_menu(self):
        '''
        Generate the menu bar
        '''
        html = []
        h = html.append
        h('<div id="aid_menu">')
        h('  <ul>')
        h('    <li><a href="#">'+self._('Navigation:')+'</a></li>')
        h(('    <li><a href="%s/person/search">'+self._('Person Search')+'</a></li>') % CFG_SITE_URL)
        h('    <!--<li><a href="#">'+self._('Person Interface FAQ')+'</a></li>!-->')
        h('  </ul>')
        h('</div>')

        return "\n".join(html)

    def tmpl_person_menu_admin(self):
        '''
        Generate the menu bar
        '''
        html = []
        h = html.append
        h('<div id="aid_menu">')
        h('  <ul>')
        h('    <li>'+self._('Navigation:')+'</li>')
        h(('    <li><a href="%s/person/search">'+self._('Person Search')+'</a></li>') % CFG_SITE_URL)
        h(('    <li><a href="%s/person/tickets_admin">'+self._('Open tickets')+'</a></li>') % CFG_SITE_URL)
        h('    <!--<li><a href="#">'+self._('Person Interface FAQ')+'</a></li>!-->')
        h('  </ul>')
        h('</div>')

        return "\n".join(html)

    def tmpl_ticket_final_review(self, req, mark_yours=[], mark_not_yours=[],
                                 mark_theirs=[], mark_not_theirs=[]):
        '''
        Generate final review page. Displaying transactions if they
        need confirmation.

        @param req: Apache request object
        @type req: Apache request object
        @param mark_yours: papers marked as 'yours'
        @type mark_yours: list
        @param mark_not_yours: papers marked as 'not yours'
        @type mark_not_yours: list
        @param mark_theirs: papers marked as being someone else's
        @type mark_theirs: list
        @param mark_not_theirs: papers marked as NOT being someone else's
        @type mark_not_theirs: list
        '''
        def html_icon_legend():
            html = []
            h = html.append
            h('<div id="legend">')
            h("<p>")
            h(self._("Symbols legend: "))
            h("</p>")
            h('<span style="margin-left:25px; vertical-align:middle;">')
            h('<img src="%s/img/aid_granted.png" '
              'alt="%s" width="30" height="30" />'
              % (CFG_SITE_URL, self._("Everything is shiny, captain!")))
            h(self._('The result of this request will be visible immediately'))
            h('</span><br />')
            h('<span style="margin-left:25px; vertical-align:middle;">')
            h('<img src="%s/img/aid_warning_granted.png" '
              'alt="%s" width="30" height="30" />'
              % (CFG_SITE_URL, self._("Confirmation needed to continue")))
            h(self._('The result of this request will be visible immediately but we need your confirmation to do so'))
            h('</span><br />')
            h('<span style="margin-left:25px; vertical-align:middle;">')
            h('<img src="%s/img/aid_denied.png" '
              'alt="%s" width="30" height="30" />'
              % (CFG_SITE_URL, self._("This will create a change request for the operators")))
            h(self._("The result of this request will be visible upon confirmation through an operator"))
            h("</span>")
            h("</div>")

            return "\n".join(html)


        def mk_ticket_row(ticket):
            recid = -1
            rectitle = ""
            recauthor = "No Name Found."
            personname = "No Name Found."

            try:
                recid = ticket['bibref'].split(",")[1]
            except (ValueError, KeyError, IndexError):
                return ""

            try:
                rectitle = get_fieldvalues(int(recid), "245__a")[0]
            except (ValueError, IndexError, TypeError):
                rectitle = self._('Error retrieving record title')

            if "authorname_rec" in ticket:
                recauthor = ticket['authorname_rec']

            if "person_name" in ticket:
                personname = ticket['person_name']

            html = []
            h = html.append

#            h("Debug: " + str(ticket) + "<br />")
            h('<td width="25">&nbsp;</td>')
            h('<td>')
            h(rectitle)
            h('</td>')
            h('<td>')
            h((personname + " ("+self._("Selected name on paper")+": %s)") % recauthor)
            h('</td>')
            h('<td>')

            if ticket['status'] == "granted":
                h('<img src="%s/img/aid_granted.png" '
                  'alt="%s" width="30" height="30" />'
                  % (CFG_SITE_URL, self._("Everything is shiny, captain!")))
            elif ticket['status'] == "warning_granted":
                h('<img src="%s/img/aid_warning_granted.png" '
                  'alt="%s" width="30" height="30" />'
                  % (CFG_SITE_URL, self._("Verification needed to continue")))
            else:
                h('<img src="%s/img/aid_denied.png" '
                  'alt="%s" width="30" height="30" />'
                  % (CFG_SITE_URL, self._("This will create a request for the operators")))

            h('</td>')
            h('<td>')
            h('<a href="%s/person/action?checkout_remove_transaction=%s ">'
              'Cancel'
              '</a>' % (CFG_SITE_URL, ticket['bibref']))
            h('</td>')

            return "\n".join(html)


        session = get_session(req)
        pinfo = session["personinfo"]
        ulevel = pinfo["ulevel"]

        html = []
        h = html.append

        h(html_icon_legend())

        if "checkout_faulty_fields" in pinfo and pinfo["checkout_faulty_fields"]:
            h(self.tmpl_error_box(self._("Please Check your entries"), self._("Sorry.")))

        if ("checkout_faulty_fields" in pinfo
            and pinfo["checkout_faulty_fields"]
            and "tickets" in pinfo["checkout_faulty_fields"]):
            h(self.tmpl_error_box(self._("Please provide at least one transaction."), self._("Error:")))

        h('<div id="aid_person_names" '
          'class="ui-tabs ui-widget ui-widget-content ui-corner-all"'
          'style="padding:10px;">')

        h('<table width="100%" border="0" cellspacing="0" cellpadding="4">')

        if not ulevel == "guest":
            h('<tr>')
            h("<td colspan='5'><h4>"+self._('Mark as your documents')+"</h4></td>")
            h('</tr>')

            if mark_yours:
                for idx, ticket in enumerate(mark_yours):
                    h('<tr id="aid_result%s">' % ((idx +1) % 2))
                    h(mk_ticket_row(ticket))
                    h('</tr>')
            else:
                h('<tr>')
                h('<td width="25">&nbsp;</td>')
                h('<td colspan="4">Nothing staged as yours</td>')
                h("</tr>")

            h('<tr>')
            h("<td colspan='5'><h4>"+self._("Mark as _not_ your documents")+"</h4></td>")
            h('</tr>')

            if mark_not_yours:
                for idx, ticket in enumerate(mark_not_yours):
                    h('<tr id="aid_result%s">' % ((idx +1) % 2))
                    h(mk_ticket_row(ticket))
                    h('</tr>')
            else:
                h('<tr>')
                h('<td width="25">&nbsp;</td>')
                h('<td colspan="4">'+self._('Nothing staged as not yours')+'</td>')
                h("</tr>")

        h('<tr>')
        h("<td colspan='5'><h4>"+self._('Mark as their documents')+"</h4></td>")
        h('</tr>')

        if mark_theirs:
            for idx, ticket in enumerate(mark_theirs):
                h('<tr id="aid_result%s">' % ((idx +1) % 2))
                h(mk_ticket_row(ticket))
                h('</tr>')
        else:
            h('<tr>')
            h('<td width="25">&nbsp;</td>')
            h('<td colspan="4">'+self._('Nothing staged in this category')+'</td>')
            h("</tr>")

        h('<tr>')
        h("<td colspan='5'><h4>"+self._('Mark as _not_ their documents')+"</h4></td>")
        h('</tr>')

        if mark_not_theirs:
            for idx, ticket in enumerate(mark_not_theirs):
                h('<tr id="aid_result%s">' % ((idx +1) % 2))
                h(mk_ticket_row(ticket))
                h('</tr>')
        else:
            h('<tr>')
            h('<td width="25">&nbsp;</td>')
            h('<td colspan="4">'+self._('Nothing staged in this category')+'</td>')
            h("</tr>")

        h('</table>')

        h("<h4>"+self._('Please provide your information')+"</h4>")
        h('<form id="final_review" action="%s/person/action" method="post">'
          % (CFG_SITE_URL))

        if ("checkout_faulty_fields" in pinfo
            and pinfo["checkout_faulty_fields"]
            and "user_first_name" in pinfo["checkout_faulty_fields"]):
            h("<p class='aid_error_line'>"+self._('Please provide your first name')+"</p>")

        h("<p>")
        if "user_first_name_sys" in pinfo and pinfo["user_first_name_sys"]:
            h((self._("Your first name:")+" %s") % pinfo["user_first_name"])
        else:
            h(self._('Your first name:')+' <input type="text" name="user_first_name" value="%s" />'
              % pinfo["user_first_name"])

        if ("checkout_faulty_fields" in pinfo
            and pinfo["checkout_faulty_fields"]
            and "user_last_name" in pinfo["checkout_faulty_fields"]):
            h("<p class='aid_error_line'>"+self._('Please provide your last name')+"</p>")

        h("</p><p>")

        if "user_last_name_sys" in pinfo and pinfo["user_last_name_sys"]:
            h((self._("Your last name:")+" %s") % pinfo["user_last_name"])
        else:
            h(self._('Your last name:')+' <input type="text" name="user_last_name" value="%s" />'
              % pinfo["user_last_name"])

        h("</p>")

        if ("checkout_faulty_fields" in pinfo
            and pinfo["checkout_faulty_fields"]
            and "user_email" in pinfo["checkout_faulty_fields"]):
            h("<p class='aid_error_line'>"+self._('Please provide your eMail address')+"</p>")

        if ("checkout_faulty_fields" in pinfo
            and pinfo["checkout_faulty_fields"]
            and "user_email_taken" in pinfo["checkout_faulty_fields"]):
            h("<p class='aid_error_line'>"+
              self._('This eMail address is reserved by a user. Please log in or provide an alternative eMail address')
              +"</p>")

        h("<p>")
        if "user_email_sys" in pinfo and pinfo["user_email_sys"]:
            h((self._("Your eMail:")+" %s") % pinfo["user_email"])
        else:
            h((self._('Your eMail:')+' <input type="text" name="user_email" value="%s" />')
              % pinfo["user_email"])
        h("</p><p>")

        h(self._("You may leave a comment (optional)")+":<br>")
        h('<textarea name="user_comments">')

        if "user_ticket_comments" in pinfo:
            h(pinfo["user_ticket_comments"])

        h("</textarea>")

        h("</p>")
        h("<p>&nbsp;</p>")

        h('<div style="text-align: center;">')
        h(('  <input type="submit" name="checkout_continue_claiming" class="aid_btn_green" value="%s" />')
          % self._("Continue claiming*"))
        h(('  <input type="submit" name="checkout_submit" class="aid_btn_green" value="%s" />')
          % self._("Confirm these changes**"))
        h('<span style="margin-left:150px;">')
        h(('  <input type="submit" name="cancel" class="aid_btn_red" value="%s" />')
          % self._("!Delete the entire request!"))
        h('</span>')
        h('</div>')
        h("</form>")
        h("</div>")
        h("<p>")
        h(self._("  * You can come back to this page later. Nothing will be lost. <br />"))
        h(self._("  ** Performs all requested changes. Changes subject to permission restrictions "
                 "will be submitted to an operator for manual review."))
        h("</p>")

        h(html_icon_legend())

        return "\n".join(html)


    def tmpl_author_search(self, query, results,
                           search_ticket=None, author_papges_mode=False):
        '''
        Generates the search for Person entities.

        @param query: the query a user issued to the search
        @type query: string
        @param results: list of results
        @type results: list
        @param search_ticket: search ticket object to inform about pending
            claiming procedure
        @type search_ticket: dict
        '''
        linktarget = "person"

        if author_papges_mode:
            linktarget = "author"

        if not query:
            query = ""

        html = []
        h = html.append

        if not author_papges_mode:
            h('<div id="header">Search for a person</div>')
            h('<form id="searchform" action="/person/search" method="GET">')
            h('<input type="text" name="q" style="border:1px solid #333; width:500px;" '
                        'maxlength="250" value="%s" class="focus" />' % query)
            h('<input type="submit" value="Search" />')
            h('</form>')

        if not results and not query:
            h('</div>')
            return "\n".join(html)

        h("<p>&nbsp;</p>")

        if query and not results:
            h(('<strong>'+self._('Sorry, no results could be found for the query')+' "%s"</strong>') % query)
            h('</div>')
            return "\n".join(html)

        h(('<p><strong>'+self._('Results for the query ')+'"%s"</strong></p>') % query)
        base_color = 100
        row_color = 0

        for index, result in enumerate(results):
            if len(results) > base_color:
                row_color += 1
            else:
                row_color = base_color - (base_color - index *
                                          (base_color / len(results)))

            pid = result[0]
            names = result[1]
            papers = result[2]

            h('<div id="aid_result%s">' % (index % 2))
            h('<div>')
            h('<span style="color:rgb(%d,%d,%d);">%s. </span>'
                         % (row_color, row_color, row_color, index + 1))

            for nindex, name in enumerate(names):
                color = row_color + nindex * 35
                color = min(color, base_color)
                h('<span style="color:rgb(%d,%d,%d);">%s; </span>'
                            % (color, color, color, name[0]))
            h('</div>')
            h(('<em><a href="#" id="moreinfolink" class="mpid%s">'
                        '<img src="../img/aid_plus_16.png" '
                        'alt = "toggle additional information." '
                        'width="11" height="11"/> '
                        +self._('Show additional information')+
                        '</a></em>' )
                        % (pid))

            if search_ticket:
                link = "%s/person/action?confirm=True&pid=%s" % (CFG_SITE_URL, pid)

                for r in search_ticket['bibrefs']:
                    link = link + '&selection=%s' % str(r)

                h(('<span style="margin-left: 40px;">'
                            '<em><a href="%s" id="confirmlink">'
                            '<strong>'+self._('YES!')+'</strong>'
                            +self._(' Assign papers to ')+
                            '%s (PersonID: %d )</a></em></span>')
                            % (link, get_person_redirect_link(pid), pid))
            else:
                h(('<span style="margin-left: 40px;">'
                            '<em><a href="%s/%s/%s" id="aid_moreinfolink">'
                            +self._('Show author page ')+'(person ID: %s - %d)</a></em></span>')
                            % (CFG_SITE_URL, linktarget,
                               get_person_redirect_link(pid),
                               get_person_redirect_link(pid), pid))
            h('<div class="more-mpid%s" id="aid_moreinfo">' % (pid))

            if papers:
                h((self._('Showing the')+' %d '+self._('most recent documents:')) % len(papers))
                h("<ul>")

                for paper in papers:
                    h("<li>%s</li>"
                           % (format_record(paper[0], "ha", on_the_fly=True)))

                h("</ul>")
            else:
                h("<p>"+self._('Sorry, there are no documents known for this person')+"</p>")

            h(('<p><a href="%s/perons/%d" target="_blank">'
                        +self._('Show more information about this person in a new window or tab')+
                        '</a></p>') % (CFG_SITE_URL, pid))
            h('</div>')
            h('</div>')

        return "\n".join(html)


    def tmpl_welcome(self):
        '''
        SSO landing/welcome page.
        '''
        html = []
        h = html.append
        h('Bibauthorid assigned you a unique ID in this system <br>')
        h('Click on the following link to confirm the data we got from ArXiv and start using '
          ' the papers claiming facility <br>')
        h('<a href=action?checkout=True> Start to Claim my papers! </a>')
        return "\n".join(html)

    def tmpl_tickets_admin(self, tickets=[]):
        '''
        Open tickets short overview for operators.
        '''
        html = []
        h = html.append
        if len(tickets)>0:
            h('List of open tickets: <br><br>')
            for t in tickets:
                h('<a href=%(cname)s#tabTickets> %(longname)s - (%(cname)s - PersonID: %(pid)s): %(num)s open tickets. </a><br>'
                  % ({'cname':str(t[1]),'longname':str(t[0]),'pid':str(t[2]),'num':str(t[3])}))
        else:
            h('There are currently no open tickets.')
        return "\n".join(html)


