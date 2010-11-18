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
"""
WebStyle templates. Customize the look of pages of CDS Invenio
"""
__revision__ = \
    "$Id$"

import time
import cgi
import traceback
import urllib
import sys
import string

from invenio.config import \
     CFG_SITE_LANG, \
     CFG_SITE_NAME, \
     CFG_SITE_NAME_INTL, \
     CFG_SITE_SUPPORT_EMAIL, \
     CFG_SITE_SECURE_URL, \
     CFG_SITE_URL, \
     CFG_VERSION, \
     CFG_WEBSTYLE_INSPECT_TEMPLATES, \
     CFG_WEBSTYLE_TEMPLATE_SKIN
from invenio.messages import gettext_set_language, language_list_long
from invenio.urlutils import make_canonical_urlargd, create_html_link
from invenio.dateutils import convert_datecvs_to_datestruct, \
                              convert_datestruct_to_dategui
from invenio.bibformat import format_record
from invenio.webuser import collect_user_info, isUserSubmitter, \
     isUserReferee
from invenio import template
from invenio.webstyle_templates import Template as InvenioTemplate
websearch_templates = template.load('websearch')

class Template(InvenioTemplate):

    def tmpl_navtrailbox_body(self, ln, title, previous_links,
                              separator, prolog, epilog):
        """Create navigation trail box body

           Parameters:

          - 'ln' *string* - The language to display

          - 'title' *string* - page title;

          - 'previous_links' *string* - the trail content from site title until current page (both ends exclusive)

          - 'prolog' *string* - HTML code to prefix the navtrail item with

          - 'epilog' *string* - HTML code to suffix the navtrail item with

          - 'separator' *string* - HTML code that separates two navtrail items

           Output:

          - text containing the navtrail

           Note: returns empty string for Home page. (guessed by title).
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = ""

        if title == CFG_SITE_NAME_INTL.get(ln, CFG_SITE_NAME):
            # return empty string for the Home page
            return out
        else:
            out += create_html_link(CFG_SITE_URL, {'ln': ln},
                                    _("Home"), {'class': 'navtrail'})
        if previous_links:
            if out:
                out += separator
            out += previous_links
        if title:
            if out:
                out += separator
            if title == CFG_SITE_NAME_INTL.get(ln, CFG_SITE_NAME): # hide site name, print Home instead
                out += cgi.escape(_("Home"))
            else:
                out += cgi.escape(title)

        return cgi.escape(prolog) + out + cgi.escape(epilog)

    def tmpl_pageheader(self, req, ln=CFG_SITE_LANG, headertitle="",
                        description="", keywords="", userinfobox="",
                        useractivities_menu="", adminactivities_menu="",
                        navtrailbox="", pageheaderadd="", uid=0,
                        secure_page_p=0, navmenuid="admin", metaheaderadd="",
                        rssurl=CFG_SITE_URL+"/rss", body_css_classes=None):

        """Creates a page header

           Parameters:

          - 'ln' *string* - The language to display

          - 'headertitle' *string* - the second part of the page HTML title

          - 'description' *string* - description goes to the metadata in the header of the HTML page

          - 'keywords' *string* - keywords goes to the metadata in the header of the HTML page

          - 'userinfobox' *string* - the HTML code for the user information box

          - 'useractivities_menu' *string* - the HTML code for the user activities menu

          - 'adminactivities_menu' *string* - the HTML code for the admin activities menu

          - 'navtrailbox' *string* - the HTML code for the navigation trail box

          - 'pageheaderadd' *string* - additional page header HTML code

          - 'uid' *int* - user ID

          - 'secure_page_p' *int* (0 or 1) - are we to use HTTPS friendly page elements or not?

          - 'navmenuid' *string* - the id of the navigation item to highlight for this page

          - 'metaheaderadd' *string* - list of further tags to add to the <HEAD></HEAD> part of the page

          - 'rssurl' *string* - the url of the RSS feed for this page

          - 'body_css_classes' *list* - list of classes to add to the body tag

           Output:

          - HTML code of the page headers
        """

        # load the right message language
        _ = gettext_set_language(ln)

        if body_css_classes is None:
            body_css_classes = []
        body_css_classes.append(navmenuid)

        if CFG_WEBSTYLE_INSPECT_TEMPLATES:
            inspect_templates_message = '''
<table width="100%%" cellspacing="0" cellpadding="2" border="0">
<tr bgcolor="#aa0000">
<td width="100%%">
<font color="#ffffff">
<strong>
<small>
CFG_WEBSTYLE_INSPECT_TEMPLATES debugging mode is enabled.  Please
hover your mouse pointer over any region on the page to see which
template function generated it.
</small>
</strong>
</font>
</td>
</tr>
</table>
'''
        else:
            inspect_templates_message = ""

        out = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-gb" lang="en-gb" dir="ltr" >
<head>
  <base href="http://www.openaire.eu/how-to-deposit/orphan-repository.html" />
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <meta name="robots" content="index, follow" />
  <meta name="keywords" content="Open Access, repository, repositories, deposit publication, Open Access Europe, Open Research Data, Repository Usage statistics" />
  <meta name="title" content="Under Construction" />
  <meta name="author" content="Administrator" />
  <meta name="description" content="OpenAIRE - Open Access Infrastructure Research for Europe" />

  <title>OpenAIRE - Orphan Record Repository</title>
  <link href="http://www.openaire.eu/templates/yoo_level/favicon.ico" rel="shortcut icon" type="image/x-icon" />
  <link rel="stylesheet" href="%(cssurl)s/img/invenio%(cssskin)s.css" type="text/css" />
  <link rel="search" type="application/opensearchdescription+xml" href="%(siteurl)s/opensearchdescription" title="%(sitename)s" />
  <link rel="unapi-server" type="application/xml" title="unAPI" href="%(unAPIurl)s" />
  <link rel="stylesheet" href="http://www.openaire.eu/plugins/content/attachments.css" type="text/css" />
  <link rel="stylesheet" href="http://www.openaire.eu/templates/yoo_level/css/template.css" type="text/css" />
  <link rel="stylesheet" href="http://www.openaire.eu/templates/yoo_level/css/openaire2/openaire2-layout.css" type="text/css" />
  <link rel="stylesheet" href="http://www.openaire.eu/templates/yoo_level/css/custom.css" type="text/css" />
  <link rel="stylesheet" href="http://www.openaire.eu/modules/mod_yoo_login/mod_yoo_login.css.php" type="text/css" />

  <style type="text/css">
    <!--
.social_bookmarker_top { float:left;text-align:center;margin:10px 10px 10px 0; }
div.wrapper { width: 900px; }
    -->
  </style>
  <script type="text/javascript" src="http://www.openaire.eu/templates/yoo_level/lib/js/mootools/mootools-release-1.12.js"></script>
  <script type="text/javascript" src="http://www.openaire.eu/media/system/js/caption.js"></script>
  <script type="text/javascript">
var YtSettings = { tplurl: 'http://www.openaire.eu/templates/yoo_level', color: 'openaire2', itemColor: '', layout: 'left' };
  </script>
  <script type="text/javascript" src="http://www.openaire.eu/templates/yoo_level/lib/js/addons/base.js"></script>
<script type="text/javascript" src="http://www.openaire.eu/templates/yoo_level/lib/js/addons/accordionmenu.js"></script>

<script type="text/javascript" src="http://www.openaire.eu/templates/yoo_level/lib/js/addons/fancymenu.js"></script>
<script type="text/javascript" src="http://www.openaire.eu/templates/yoo_level/lib/js/addons/dropdownmenu.js"></script>
<script type="text/javascript" src="http://www.openaire.eu/templates/yoo_level/lib/js/yoo_tools.js"></script>

<link rel="apple-touch-icon" href="http://www.openaire.eu/templates/yoo_level/apple_touch_icon.png" />
 %(metaheaderadd)s
</head>

<body id="page" class="yoopage left   ">
%(inspect_templates_message)s


    <div id="page-body">
        <div class="page-body-t">
            <div class="wrapper floatholder">


                <div id="header">

                    <div id="toolbar">
                        <div class="toolbar-1">
                            <div class="toolbar-2">

                                            <div class="mod-blank">
                <div class="module">


                                        <form action="index.php" method="post">
    <div class="module-search">

        <input name="searchword" maxlength="20" alt="Search" type="text" size="22" value="search..."  onblur="if(this.value=='') this.value='search...';" onfocus="if(this.value=='search...') this.value='';" />

                <button value="" name="Submit" type="submit"></button>

    </div>

    <input type="hidden" name="task"   value="search" />
    <input type="hidden" name="option" value="com_search" />
</form>
                </div>
            </div>
                        <div class="mod-blank">
                <div class="module">



                                        <div id="jflanguageselection"><label for="jflanguageselection" class="jflanguageselection">Select</label><img src="http://www.openaire.eu/components/com_joomfish/images/flags/en.gif" alt="English" title="English" border="0" class="langImg"/>
<select name="lang"  class="jflanguageselection" onfocus="jfselectlang=this.selectedIndex;" onchange="if(this.options[this.selectedIndex].disabled){this.selectedIndex=jfselectlang;} else {document.location.replace(this.value);}">
    <option value="http://www.openaire.eu/el/deposit/registration-author-account.html"  style='padding-left:22px;background-image: url("http://www.openaire.eu/components/com_joomfish/images/flags/el.gif");background-repeat: no-repeat;background-position:center left;'  >Ελληνικά</option>
    <option value="http://www.openaire.eu/en/how-to-deposit/orphan-repository.html"  style='padding-left:22px;background-image: url("http://www.openaire.eu/components/com_joomfish/images/flags/en.gif");background-repeat: no-repeat;background-position:center left;'  selected="selected" >English</option>
</select>
</div>
<noscript><a href="http://www.openaire.eu/el/deposit/registration-author-account.html"><span lang="el" xml:lang="el">Ελληνικά</span></a>&nbsp;<a href="http://www.openaire.eu/en/how-to-deposit/orphan-repository.html"><span lang="en" xml:lang="en">English</span></a>&nbsp;</noscript><!--Joom!fish V2.0.4 (Lightning)-->
<!-- &copy; 2003-2009 Think Network, released under the GPL. -->
<!-- More information: at http://www.joomfish.net -->

                </div>

            </div>



                                                                <div id="topmenu">
                                    <ul class="menu"><li class="level1 item1 first"><a href="http://www.openaire.eu/" class="level1 item1 first"><span>Home</span></a></li><li class="level1 item2"><a href="http://www.openaire.eu/en/contact-us.html" class="level1 item2"><span>Contact us</span></a></li><li class="level1 item3 last"><a href="http://www.openaire.eu/en/terms-of-use.html" class="level1 item3 last"><span>Terms of use</span></a></li></ul>
                                </div>

                            </div>
                        </div>
                    </div>


                    <div id="headerbar">
                        <div class="floatbox ie_fix_floats">
                                        <div class="mod-rounded-header ">
                <div class="module">


                    <div class="box-1">
                        <div class="box-2">
                            <div class="box-3 deepest">
                                                                <h3 class="header"><span class="header-2"><span class="header-3">Consortium<span class="color"> members</span></span></span></h3>


<form action="http://www.openaire.eu/en/how-to-deposit/orphan-repository.html" method="post" name="login">

<span class="niftyquick" style="display: block;">
    <span class="yoo-login">

                <span class="login">


            <span class="username">

                <input type="text" name="username" size="18" alt="Username" value="Username" onblur="if(this.value=='') this.value='Username';" onfocus="if(this.value=='Username') this.value='';" />

            </span>

            <span class="password">

                <input type="password" name="passwd" size="10" alt="Password" value="Password" onblur="if(this.value=='') this.value='Password';" onfocus="if(this.value=='Password') this.value='';" />


            </span>

                        <input type="hidden" name="remember" value="yes" />

            <span class="login-button">
                <button value="Login" name="Submit" type="submit" title="Login">Login</button>
            </span>

                        <span class="lostpassword">
                <a href="http://www.openaire.eu/en/component/user/reset.html" title="Forgot your password?"></a>
            </span>


                        <span class="lostusername">
                <a href="http://www.openaire.eu/en/component/user/remind.html" title="Forgot your username?"></a>
            </span>



            <input type="hidden" name="option" value="com_user" />
            <input type="hidden" name="task" value="login" />
            <input type="hidden" name="return" value="L2VuL2Fib3V0LW9wZW5haXJlL3ByaXZhdGUtc3BhY2UuaHRtbA==" />
            <input type="hidden" name="023a93a5e8c5328c6dc0e586e714805d" value="1" />
        </span>


    </span>

</span>
</form>                         </div>
                        </div>
                    </div>

                </div>
            </div>
                        <div class="mod-rounded-header ">
                <div class="module">


                    <div class="box-1">

                        <div class="box-2">
                            <div class="box-3 deepest">
                                                                <h3 class="header"><span class="header-2"><span class="header-3">Follow<span class="color"> us on Twitter</span></span></span></h3>
                                                                <div style="text-align: center;"><a target="_blank" href="http://www.twitter.com/OpenAIRE_eu"> <img src="http://twitter-badges.s3.amazonaws.com/follow_bird-c.png" alt="Follow OpenAIRE on Twitter" /> </a></div>                           </div>
                        </div>
                    </div>


                </div>
            </div>

                        </div>
                    </div>

                    <div id="menubar">
                        <div class="menubar-1">
                            <div class="menubar-2"></div>
                        </div>
                    </div>



                    <div id="logo">
                        <p><a href="http://www.openaire.eu/index.php"><img alt="articles" src="http://www.openaire.eu/images/openaire/logos/logo_openaire.png" /></a></p>
                    </div>


                                        <div id="menu">
                        <ul class="menu"><li class="level1 item1 first"><a href="http://www.openaire.eu/en/open-access/open-access-overview.html" class="level1 item1 first"><span>Open Access &amp; EC Pilot</span></a></li><li class="level1 item2 active"><a href="http://www.openaire.eu/en/how-to-deposit/claim-depositions.html" class="level1 item2 active"><span>How to deposit</span></a></li><li class="level1 item3"><a href="http://www.openaire.eu/en/support/faq.html" class="level1 item3"><span>Support</span></a></li><li class="level1 item4"><a href="http://www.openaire.eu/en/nlo/country-information.html" class="level1 item4"><span>National OA Desks</span></a></li><li class="level1 item6 last"><a href="http://www.openaire.eu/en/about-openaire/fact-sheet.html" class="level1 item6 last"><span>About OpenAIRE</span></a></li></ul>

                    </div>


                </div>
                <!-- header end -->

                <div class="shadow-l">
                    <div class="shadow-r">

                                                <div id="top">
                            <div class="top-t">
                                <div class="floatbox ie_fix_floats">

                                                                        <div class="topblock width100 float-left">

                                                    <div class="mod-rounded ">
                <div class="module">


                    <div class="box-t1">
                        <div class="box-t2">
                            <div class="box-t3"></div>
                        </div>
                    </div>

                    <div class="box-1">
                        <div class="box-2">

                            <div class="box-3 deepest">
                                                                <ul class="menu"><li class="level1 item1 first"><a href="http://www.openaire.eu/en/how-to-deposit/claim-depositions.html" class="level1 item1 first"><span>General instructions</span></a></li><li class="level1 item2"><a href="http://www.openaire.eu/en/how-to-deposit/repository-map.html" class="level1 item2"><span>Repositories in Europe</span></a></li><li class="level1 item3 last active current"><a href="http://www.openaire.eu/en/how-to-deposit/orphan-repository.html" class="level1 item3 last active current"><span>Orphan repository</span></a></li></ul>                          </div>
                        </div>
                    </div>

                    <div class="box-b1">
                        <div class="box-b2">

                            <div class="box-b3"></div>
                        </div>
                    </div>

                </div>
            </div>

                                    </div>


                                </div>
                            </div>
                        </div>


                        <!-- top end -->

                        <div id="middle">
                            <div class="middle-b">
                                <div class="background">
""" % {
          'siteurl' : CFG_SITE_URL,
          'sitesecureurl' : CFG_SITE_SECURE_URL,
          'cssurl' : secure_page_p and CFG_SITE_SECURE_URL or CFG_SITE_URL,
          'cssskin' : CFG_WEBSTYLE_TEMPLATE_SKIN != 'default' and '_' + CFG_WEBSTYLE_TEMPLATE_SKIN or '',
          'rssurl': rssurl,
          'ln' : ln,
          'ln_iso_639_a' : ln.split('_', 1)[0],
          'langlink': '?ln=' + ln,

          'sitename' : CFG_SITE_NAME_INTL.get(ln, CFG_SITE_NAME),
          'headertitle' : cgi.escape(headertitle),

          'sitesupportemail' : CFG_SITE_SUPPORT_EMAIL,

          'description' : cgi.escape(description),
          'keywords' : cgi.escape(keywords),
          'metaheaderadd' : metaheaderadd,

          'userinfobox' : userinfobox,
          'navtrailbox' : navtrailbox,
          'useractivities': useractivities_menu,
          'adminactivities': adminactivities_menu and ('<td class="headermoduleboxbodyblank">&nbsp;</td><td class="headermoduleboxbody%(personalize_selected)s">%(adminactivities)s</td>' % \
          {'personalize_selected': navmenuid.startswith('admin') and "selected" or "",
          'adminactivities': adminactivities_menu}) or '<td class="headermoduleboxbodyblank">&nbsp;</td>',

          'pageheaderadd' : pageheaderadd,
          'body_css_classes' : body_css_classes and ' class="%s"' % ' '.join(body_css_classes) or '',

          'search_selected': navmenuid == 'search' and "selected" or "",
          'submit_selected': navmenuid == 'submit' and "selected" or "",
          'personalize_selected': navmenuid.startswith('your') and "selected" or "",
          'help_selected': navmenuid == 'help' and "selected" or "",

          'msg_search' : _("Search"),
          'msg_submit' : _("Submit"),
          'msg_personalize' : _("Personalize"),
          'msg_help' : _("Help"),
          'languagebox' : self.tmpl_language_selection_box(req, ln),
          'unAPIurl' : cgi.escape('%s/unapi' % CFG_SITE_URL),
          'inspect_templates_message' : inspect_templates_message
        }
        return out

        out = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="%(ln_iso_639_a)s" xml:lang="%(ln_iso_639_a)s">
<head>
 <title>%(headertitle)s - %(sitename)s</title>
 <link rev="made" href="mailto:%(sitesupportemail)s" />
 <link rel="stylesheet" href="%(cssurl)s/img/invenio%(cssskin)s.css" type="text/css" />
 <link rel="alternate" type="application/rss+xml" title="%(sitename)s RSS" href="%(rssurl)s" />
 <link rel="search" type="application/opensearchdescription+xml" href="%(siteurl)s/opensearchdescription" title="%(sitename)s" />
 <link rel="unapi-server" type="application/xml" title="unAPI" href="%(unAPIurl)s" />
 <link rel="icon" href="%(siteurl)s/img/favicon.png" type="image/png" />
 <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
 <meta http-equiv="Content-Language" content="%(ln)s" />
 <meta name="description" content="%(description)s" />
 <meta name="keywords" content="%(keywords)s" />
 %(metaheaderadd)s
</head>
<body%(body_css_classes)s lang="%(ln_iso_639_a)s">
<div class="pageheader">
%(inspect_templates_message)s
<!-- replaced page header -->
<div class="headerlogo">
<table class="headerbox" cellspacing="0">
 <tr>
  <td align="right" valign="top" colspan="12">
  <div class="userinfoboxbody">
    %(userinfobox)s
  </div>
  <div class="headerboxbodylogo">
   <a href="%(siteurl)s?ln=%(ln)s">%(sitename)s</a>
  </div>
  </td>
 </tr>
 <tr class="menu">
       <td class="headermoduleboxbodyblank">
             &nbsp;
       </td>
       <td class="headermoduleboxbodyblank">
             &nbsp;
       </td>
       <td class="headermoduleboxbody%(search_selected)s">
             <a class="header%(search_selected)s" href="%(siteurl)s/?ln=%(ln)s">%(msg_search)s</a>
       </td>
       <td class="headermoduleboxbodyblank">
             &nbsp;
       </td>
       <td class="headermoduleboxbody%(submit_selected)s">
             <a class="header%(submit_selected)s" href="%(siteurl)s/submit?ln=%(ln)s">%(msg_submit)s</a>
       </td>
       <td class="headermoduleboxbodyblank">
             &nbsp;
       </td>
       <td class="headermoduleboxbody%(personalize_selected)s">
             %(useractivities)s
       </td>
       <td class="headermoduleboxbodyblank">
             &nbsp;
       </td>
       <td class="headermoduleboxbody%(help_selected)s">
             <a class="header%(help_selected)s" href="%(siteurl)s/help/%(langlink)s">%(msg_help)s</a>
       </td>
       %(adminactivities)s
       <td class="headermoduleboxbodyblanklast">
             &nbsp;
       </td>
 </tr>
</table>
</div>
<table class="navtrailbox">
 <tr>
  <td class="navtrailboxbody">
   %(navtrailbox)s
  </td>
 </tr>
</table>
<!-- end replaced page header -->
%(pageheaderadd)s
</div>
        """ % {
          'siteurl' : CFG_SITE_URL,
          'sitesecureurl' : CFG_SITE_SECURE_URL,
          'cssurl' : secure_page_p and CFG_SITE_SECURE_URL or CFG_SITE_URL,
          'cssskin' : CFG_WEBSTYLE_TEMPLATE_SKIN != 'default' and '_' + CFG_WEBSTYLE_TEMPLATE_SKIN or '',
          'rssurl': rssurl,
          'ln' : ln,
          'ln_iso_639_a' : ln.split('_', 1)[0],
          'langlink': '?ln=' + ln,

          'sitename' : CFG_SITE_NAME_INTL.get(ln, CFG_SITE_NAME),
          'headertitle' : cgi.escape(headertitle),

          'sitesupportemail' : CFG_SITE_SUPPORT_EMAIL,

          'description' : cgi.escape(description),
          'keywords' : cgi.escape(keywords),
          'metaheaderadd' : metaheaderadd,

          'userinfobox' : userinfobox,
          'navtrailbox' : navtrailbox,
          'useractivities': useractivities_menu,
          'adminactivities': adminactivities_menu and ('<td class="headermoduleboxbodyblank">&nbsp;</td><td class="headermoduleboxbody%(personalize_selected)s">%(adminactivities)s</td>' % \
          {'personalize_selected': navmenuid.startswith('admin') and "selected" or "",
          'adminactivities': adminactivities_menu}) or '<td class="headermoduleboxbodyblank">&nbsp;</td>',

          'pageheaderadd' : pageheaderadd,
          'body_css_classes' : body_css_classes and ' class="%s"' % ' '.join(body_css_classes) or '',

          'search_selected': navmenuid == 'search' and "selected" or "",
          'submit_selected': navmenuid == 'submit' and "selected" or "",
          'personalize_selected': navmenuid.startswith('your') and "selected" or "",
          'help_selected': navmenuid == 'help' and "selected" or "",

          'msg_search' : _("Search"),
          'msg_submit' : _("Submit"),
          'msg_personalize' : _("Personalize"),
          'msg_help' : _("Help"),
          'languagebox' : self.tmpl_language_selection_box(req, ln),
          'unAPIurl' : cgi.escape('%s/unapi' % CFG_SITE_URL),
          'inspect_templates_message' : inspect_templates_message
        }
        return out

    def tmpl_pagefooter(self, req=None, ln=CFG_SITE_LANG, lastupdated=None,
                        pagefooteradd=""):
        """Creates a page footer

           Parameters:

          - 'ln' *string* - The language to display

          - 'lastupdated' *string* - when the page was last updated

          - 'pagefooteradd' *string* - additional page footer HTML code

           Output:

          - HTML code of the page headers
        """

        # load the right message language
        _ = gettext_set_language(ln)

        if lastupdated and lastupdated != '$Date$':
            if lastupdated.startswith("$Date: ") or \
            lastupdated.startswith("$Id: "):
                lastupdated = convert_datestruct_to_dategui(\
                                 convert_datecvs_to_datestruct(lastupdated),
                                 ln=ln)
            msg_lastupdated = _("Last updated") + ": " + lastupdated
        else:
            msg_lastupdated = ""

        out = """
</div>
                            </div>
                        </div>
                        <!-- middle end -->


                    </div>
                </div>

                <div id="footer">
                    <div class="footer-1">

                        <div class="footer-2">
                            <a class="anchor" href="#page"></a>
                            <p>Copyright © 2010, OpenAIRE Consortium.</p>

                        </div>
                    </div>
                </div>
                <!-- footer end -->

            </div>

        </div>
    </div>

</body>
""" % {
          'siteurl' : CFG_SITE_URL,
          'sitesecureurl' : CFG_SITE_SECURE_URL,
          'ln' : ln,
          'langlink': '?ln=' + ln,

          'sitename' : CFG_SITE_NAME_INTL.get(ln, CFG_SITE_NAME),
          'sitesupportemail' : CFG_SITE_SUPPORT_EMAIL,

          'msg_search' : _("Search"),
          'msg_submit' : _("Submit"),
          'msg_personalize' : _("Personalize"),
          'msg_help' : _("Help"),

          'msg_poweredby' : _("Powered by"),
          'msg_maintainedby' : _("Maintained by"),

          'msg_lastupdated' : msg_lastupdated,
          'languagebox' : self.tmpl_language_selection_box(req, ln),
          'version' : CFG_VERSION,

          'pagefooteradd' : pagefooteradd,
}
        return out
        out = """
<div class="pagefooter">
%(pagefooteradd)s
<!-- replaced page footer -->
 <div class="pagefooterstripeleft">
  <img style="margin-top: 0px; margin-left: 0px; float: left;" alt="fp7-capacities" src="/img/fp7-capacities_tr.png" height="45" width="58">
  <img style="margin-left: 10px; margin-top: 10px; float: left;" alt="e_infrastructures" src="/einfrastructure_sm.png" height="32" width="87">
  %(sitename)s&nbsp;::&nbsp;<a class="footer" href="%(siteurl)s/?ln=%(ln)s">%(msg_search)s</a>&nbsp;::&nbsp;<a class="footer" href="%(siteurl)s/submit?ln=%(ln)s">%(msg_submit)s</a>&nbsp;::&nbsp;<a class="footer" href="%(sitesecureurl)s/youraccount/display?ln=%(ln)s">%(msg_personalize)s</a>&nbsp;::&nbsp;<a class="footer" href="%(siteurl)s/help/%(langlink)s">%(msg_help)s</a>
  <br />
  %(msg_poweredby)s <a class="footer" href="http://cdsware.cern.ch/">Invenio</a> v%(version)s
  <br />
  %(msg_maintainedby)s <a class="footer" href="mailto:%(sitesupportemail)s">%(sitesupportemail)s</a>
  <br />
  %(msg_lastupdated)s
 </div>
 <div class="pagefooterstriperight">
  %(languagebox)s
 </div>
<!-- replaced page footer -->
</div>
</body>
</html>
        """ % {
          'siteurl' : CFG_SITE_URL,
          'sitesecureurl' : CFG_SITE_SECURE_URL,
          'ln' : ln,
          'langlink': '?ln=' + ln,

          'sitename' : CFG_SITE_NAME_INTL.get(ln, CFG_SITE_NAME),
          'sitesupportemail' : CFG_SITE_SUPPORT_EMAIL,

          'msg_search' : _("Search"),
          'msg_submit' : _("Submit"),
          'msg_personalize' : _("Personalize"),
          'msg_help' : _("Help"),

          'msg_poweredby' : _("Powered by"),
          'msg_maintainedby' : _("Maintained by"),

          'msg_lastupdated' : msg_lastupdated,
          'languagebox' : self.tmpl_language_selection_box(req, ln),
          'version' : CFG_VERSION,

          'pagefooteradd' : pagefooteradd,

        }
        return out

