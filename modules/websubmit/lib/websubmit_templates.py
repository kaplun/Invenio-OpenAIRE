## $Id: websubmit_templates.py,v 1.14 2007/08/17 13:10:13 nich Exp $

## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007 CERN.
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

__revision__ = "$Id: websubmit_templates.py,v 1.14 2007/08/17 13:10:13 nich Exp $"

import urllib
import time
import cgi
import gettext
import string
import locale
import re
import operator
import os

from invenio.config import \
     accessurl, \
     images, \
     version, \
     weburl
from invenio.messages import gettext_set_language
##----NEW STUFF--------------------
from invenio.config import cdslang
##----END OF NEW STUFF-------------
class Template:

    # Parameters allowed in the web interface for fetching files
    files_default_urlargd = {
        'version': (str, "") # version "" means "latest"
        }


    def tmpl_submit_home_page(self, ln, catalogues):
        """
        The content of the home page of the submit engine

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'catalogues' *string* - The HTML code for the catalogues list
        """

        # load the right message language
        _ = gettext_set_language(ln)

        return """
          <script type="text/javascript" language="Javascript1.2">
          var allLoaded = 1;
          </script>
           <table class="searchbox" width="100%%" summary="">
              <tr>
                  <th class="portalboxheader">%(document_types)s:</th>
              </tr>
              <tr>
                  <td class="portalboxbody">
                    <br />
                    %(please_select)s:
                    <br /><br />
                    <table width="100%%">
                    <tr>
                        <td width="50%%" class="narrowsearchboxbody">
                          <form method="get" action="/submit">
                            <input type="hidden" name="doctype" />
                              %(catalogues)s
                          </form>
                        </td>
                    </tr>
                    </table>
                  </td>
              </tr>
            </table>""" % {
              'document_types' : _("Document types available for submission"),
              'please_select' : _("Please select the type of document you want to submit."),
              'catalogues' : catalogues,
            }

    def tmpl_submit_home_catalog_no_content(self, ln):
        """
        The content of the home page of submit in case no doctypes are available

        Parameters:

          - 'ln' *string* - The language to display the interface in
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = "<h3>" + _("No document types available.") + "</h3>\n"
        return out

    def tmpl_submit_home_catalogs(self, ln, catalogs):
        """
        Produces the catalogs' list HTML code

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'catalogs' *array* - The catalogs of documents, each one a hash with the properties:
                - 'id' - the internal id
                - 'name' - the name
                - 'sons' - sub-catalogs
                - 'docs' - the contained document types, in the form:
                      - 'id' - the internal id
                      - 'name' - the name
            There is at least one catalog
        """

        # load the right message language
        _ = gettext_set_language(ln)

        # import pprint
        # out = "<pre>" + pprint.pformat(catalogs)
        out = ""
        for catalog in catalogs:
            out += "\n<ul>"
            out += self.tmpl_submit_home_catalogs_sub(ln, catalog)
            out += "\n</ul>\n"

        return out

    def tmpl_submit_home_catalogs_sub(self, ln, catalog):
        """
        Recursive function that produces a catalog's HTML display

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'catalog' *array* - A catalog of documents, with the properties:
                - 'id' - the internal id
                - 'name' - the name
                - 'sons' - sub-catalogs
                - 'docs' - the contained document types, in the form:
                      - 'id' - the internal id
                      - 'name' - the name
        """

        # load the right message language
        _ = gettext_set_language(ln)

        if catalog['level'] == 1:
            out = "<li><font size=\"+1\"><strong>%s</strong></font>\n" % catalog['name']
        else:
            if catalog['level'] == 2:
                out = "<li>%s\n" % catalog['name']
            else:
                if catalog['level'] > 2:
                    out = "<li>%s\n" % catalog['name']

        if len(catalog['docs']) or len(catalog['sons']):
            out += "<ul>\n"

        if len(catalog['docs']) != 0:
            for row in catalog['docs']:
                out += self.tmpl_submit_home_catalogs_doctype(ln, row)

        if len(catalog['sons']) != 0:
            for row in catalog['sons']:
                out += self.tmpl_submit_home_catalogs_sub(ln, row)

        if len(catalog['docs']) or len(catalog['sons']):
            out += "</ul></li>"
        else:
            out += "</li>"
            
        return out

    def tmpl_submit_home_catalogs_doctype(self, ln, doc):
        """
        Recursive function that produces a catalog's HTML display

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'doc' *array* - A catalog of documents, with the properties:
                      - 'id' - the internal id
                      - 'name' - the name
        """

        # load the right message language
        _ = gettext_set_language(ln)

        return """<li><a href="" onclick="document.forms[0].doctype.value='%(id)s';document.forms[0].submit();return false;">%(name)s</a></li>""" % doc

    def tmpl_action_page(self, ln, uid, guest, pid, now, doctype,
                         description, docfulldesc, snameCateg,
                         lnameCateg, actionShortDesc, indir,
                         statustext):
        """
        Recursive function that produces a catalog's HTML display

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'guest' *boolean* - If the user is logged in or not

          - 'pid' *string* - The current process id

          - 'now' *string* - The current time (security control features)

          - 'doctype' *string* - The selected doctype

          - 'description' *string* - The description of the doctype

          - 'docfulldesc' *string* - The title text of the page

          - 'snameCateg' *array* - The short names of all the categories of documents

          - 'lnameCateg' *array* - The long names of all the categories of documents

          - 'actionShortDesc' *array* - The short names (codes) for the different actions

          - 'indir' *array* - The directories for each of the actions

          - 'statustext' *array* - The names of the different action buttons
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = ""

        out += """
              <script language="JavaScript" type="text/javascript">
              var checked = 0;
              function tester() {
              """
        if (guest):
            out += "alert(\"%(please_login_js)s\");return false;\n" % {
                     'please_login_js' : _("Please log in first.") + '\\n' + _("Use the top-right menu to log in.")
                   }

        out += """
                    if (checked == 0) {
                        alert ("%(select_cat)s");
                        return false;
                    } else {
                        return true;
                    }
                }

                function clicked() {
                    checked=1;
                }

                function selectdoctype(nb) {
                    document.forms[0].act.value = docname[nb];
                }
                </script>
                <form method="get" action="/submit">
                <input type="hidden" name="doctype" value="%(doctype)s" />
                <input type="hidden" name="indir" />
                <input type="hidden" name="access" value="%(now)i_%(pid)s" />

                <input type="hidden" name="act" />
                <input type="hidden" name="startPg" value="1" />
                <input type="hidden" name="mainmenu" value="/submit?doctype=%(doctype)s" />

                <table class="searchbox" width="100%%" summary="">
                  <tr>
                    <th class="portalboxheader">%(docfulldesc)s</th>
                  </tr>
                  <tr>
                      <td class="portalboxbody">%(description)s
                        <br />
                        <script language="JavaScript" type="text/javascript">
                        var nbimg = document.images.length + 1;
                        </script>
                        <br />
                        <table align="center" cellpadding="0" cellspacing="0" border="0">
                        <tr valign="top">
                """ % {
                      'select_cat' : _("Please select a category"),
                      'doctype' : doctype,
                      'now' : now,
                      'pid' : pid,
                      'docfulldesc' : docfulldesc,
                      'description' : description,
                    }

        if len(snameCateg) :
            out += """<td align="right">"""
            for i in range(0, len(snameCateg)):
                out += """<label for="combo%(shortname)s">%(longname)s</label><input type="radio" name="combo%(doctype)s" id="combo%(shortname)s" value="%(shortname)s" onclick="clicked();" />&nbsp;<br />""" % {
                         'longname' : lnameCateg[i],
                         'doctype' : doctype,
                         'shortname' : snameCateg[i],
                       }
            out += "</td>"
        else:
            out += "<script>checked=1;</script>"
        out += """<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
                  <td>
                    <table><tr><td>
               """
        #display list of actions
        for i in range(0,len(actionShortDesc)):
            out += """<input type="submit" class="adminbutton" value="%(status)s" onclick="if (tester()) { document.forms[0].indir.value='%(indir)s';document.forms[0].act.value='%(act)s';document.forms[0].submit();}; return false;" /><br />""" % {
                     'status' : statustext[i],
                     'indir' : indir[i],
                     'act' : actionShortDesc[i]
                   }
        out += """  </td></tr></table>
                    </td>
                </tr>
                </table>
                <br />"""
        if len(snameCateg) :
            out += """<strong class="headline">%(notice)s:</strong><br />
                    %(select_cat)s""" % {
                     'notice' : _("Notice"),
                     'select_cat' : _("Select a category and then click on an action button."),
                    }
        out += """
                <br /><br />
            
                </td>
                </tr>
                </table>
                </form>
                <form action="/submit"><hr />
                  <font color="black"><small>%(continue_explain)s</small></font>
                  <table border="0" bgcolor="#CCCCCC" width="100%%"><tr>
                    <td width="100%%">
                    <small>Access Number: <input size="15" name="AN" />
                      <input type="hidden" name="doctype" value="%(doctype)s" />
                      <input class="adminbutton" type="submit" value=" %(go)s " />
                    </small>
                    </td></tr>
                  </table>
                  <hr />
                 </form>
                 """ % {
                'continue_explain' : _("To continue with a previously interrupted submission, enter an access number into the box below:"),
                  'doctype' : doctype,
                  'go' : _("GO"),
                }

        return out

    def tmpl_warning_message(self, ln, msg):
        """
        Produces a warning message for the specified text

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'msg' *string* - The message to display
        """

        # load the right message language
        _ = gettext_set_language(ln)

        return """<center><font color="red">%s</font></center>""" % msg

    def tmpl_page_interface(self, ln, docname, actname, curpage, nbpages, file, nextPg, access, nbPg, doctype, act, indir, fields, javascript, images, mainmenu):
        """
        Produces a page with the specified fields (in the submit chain)

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'doctype' *string* - The document type

          - 'docname' *string* - The document type name

          - 'actname' *string* - The action name

          - 'act' *string* - The action

          - 'curpage' *int* - The current page of submitting engine

          - 'nbpages' *int* - The total number of pages

          - 'nextPg' *int* - The next page

          - 'access' *string* - The submission number

          - 'nbPg' *string* - ??

          - 'indir' *string* - the directory of submitting

          - 'fields' *array* - the fields to display in the page, with each record having the structure:

              - 'fullDesc' *string* - the description of the field

              - 'text' *string* - the HTML code of the field

              - 'javascript' *string* - if the field has some associated javascript code

              - 'type' *string* - the type of field (T, F, I, H, D, S, R)

              - 'name' *string* - the name of the field

              - 'rows' *string* - the number of rows for textareas

              - 'cols' *string* - the number of columns for textareas

              - 'val' *string* - the default value of the field

              - 'size' *string* - the size for text fields

              - 'maxlength' *string* - the maximum length for text fields

              - 'htmlcode' *string* - the complete HTML code for user-defined fields

              - 'typename' *string* - the long name of the type

          - 'javascript' *string* - the javascript code to insert in the page

          - 'images' *string* - the path to the images

          - 'mainmenu' *string* - the url of the main menu

        """

        # load the right message language
        _ = gettext_set_language(ln)

        # top menu
        out = """
                <form method="post" action="/submit" onsubmit="return tester();">
                <center><table cellspacing="0" cellpadding="0" border="0">
                  <tr>
                    <td class="submitHeader"><b>%(docname)s&nbsp;</b></td>
                    <td class="submitHeader"><small>&nbsp;%(actname)s&nbsp;</small></td>
                    <td valign="bottom">
                        <table cellspacing="0" cellpadding="0" border="0" width="100%%">
                        <tr><td class="submitEmptyPage">&nbsp;&nbsp;</td>
              """ % {
                'docname' : docname,
                'actname' : actname,
              }

        for i in range(1, nbpages+1):
            if i == int(curpage):
                out += """<td class="submitCurrentPage"><small>&nbsp;page: %s&nbsp;</small></td>""" % curpage
            else:
                out += """<td class="submitPage"><small>&nbsp;<a href='' onclick="if (tester2() == 1){document.forms[0].curpage.value=%s;document.forms[0].submit();return false;} else { return false; }">%s</a>&nbsp;</small></td>""" % (i,i)
        out += """        <td class="submitEmptyPage">&nbsp;&nbsp;
                        </td></tr></table>
                    </td>
                    <td class="submitHeader" align="right">&nbsp;<a href='' onclick="window.open('/submit/summary?doctype=%(doctype)s&amp;act=%(act)s&amp;access=%(access)s&amp;indir=%(indir)s','summary','scrollbars=yes,menubar=no,width=500,height=250');return false;"><font color="white"><small>%(summary)s(2)</small></font></a>&nbsp;</td>
                  </tr>
                  <tr><td colspan="5" class="submitHeader">
                    <table border="0" cellspacing="0" cellpadding="15" width="100%%" class="submitBody"><tr><td>
                     <br />
                     <input type="hidden" name="file" value="%(file)s" />
                     <input type="hidden" name="nextPg" value="%(nextPg)s" />
                     <input type="hidden" name="access" value="%(access)s" />
                     <input type="hidden" name="curpage" value="%(curpage)s" />
                     <input type="hidden" name="nbPg" value="%(nbPg)s" />
                     <input type="hidden" name="doctype" value="%(doctype)s" />
                     <input type="hidden" name="act" value="%(act)s" />
                     <input type="hidden" name="indir" value="%(indir)s" />
                     <input type="hidden" name="mode" value="U" />
                     <input type="hidden" name="step" value="0" />
                """ % {
                 'summary' : _("SUMMARY"),
                 'doctype' : doctype,
                 'act' : act,
                 'access' : access,
                 'indir' : indir,
                 'file' : file,
                 'nextPg' : nextPg,
                 'curpage' : curpage,
                 'nbPg' : nbPg,
               }

        for field in fields:
            if field['javascript']:
                out += """<script language="JavaScript1.1"  type="text/javascript">
                          %s
                          </script>
                       """ % field['javascript'];

            # now displays the html form field(s)
            out += "%s\n%s\n" % (field['fullDesc'], field['text'])

        out += javascript
        out += "<br />&nbsp;<br />&nbsp;</td></tr></table></td></tr>\n"

        # Display the navigation cell
        # Display "previous page" navigation arrows
        out += """<tr><td colspan="5"><table border="0" cellpadding="0" cellspacing="0" width="100%%"><tr>"""
        if int(curpage) != 1:
            out += """ <td class="submitHeader" align="left">&nbsp;
                         <a href='' onclick="if (tester2() == 1) {document.forms[0].curpage.value=%(prpage)s;document.forms[0].submit();return false;} else { return false; }">
                           <img src="%(images)s/left-trans.gif" alt="%(prevpage)s" border="0" />
                             <strong><font color="white">%(prevpage)s</font></strong>
                         </a>
                       </td>
            """ % {
              'prpage' : int(curpage) - 1,
              'images' : images,
              'prevpage' : _("Previous page"),
            }
        else:
            out += """ <td class="submitHeader">&nbsp;</td>"""
        # Display the submission number
        out += """ <td class="submitHeader" align="center"><small>%(submission)s: %(access)s</small></td>\n""" % {
                'submission' : _("Submission number") + '(1)',
                'access' : access,
              }
        # Display the "next page" navigation arrow
        if int(curpage) != int(nbpages):
            out += """ <td class="submitHeader" align="right">
                         <a href='' onclick="if (tester2()){document.forms[0].curpage.value=%(nxpage)s;document.forms[0].submit();return false;} else {return false;}; return false;">
                          <strong><font color="white">%(nextpage)s</font></strong>
                          <img src="%(images)s/right-trans.gif" alt="%(nextpage)s" border="0" />
                        </a>
                       </td>
            """ % {
              'nxpage' : int(curpage) + 1,
              'images' : images,
              'nextpage' : _("Next page"),
            }
        else:
            out += """ <td class="submitHeader">&nbsp;</td>"""
        out += """</tr></table></td></tr></table></center></form>

                  <br />
                  <br />
                 <a href="%(mainmenu)s" onclick="return confirm('%(surequit)s')">
                 <img src="%(images)s/mainmenu.gif" border="0" alt="%(back)s" align="right" /></a>
                 <br /><br />
                 <hr />
                  <small>%(take_note)s</small><br />
                  <small>%(explain_summary)s</small><br />
               """ % {
                 'surequit' : _("Are you sure you want to quit this submission?"),
                 'back' : _("Back to main menu"),
                 'mainmenu' : mainmenu,
                 'images' : images,
                 'take_note' : '(1) ' + _("This is your submission access number. It can be used to continue with an interrupted submission in case of problems."),
                 'explain_summary' : '(2) ' + _("Mandatory fields appear in red in the SUMMARY window."),
               }
        return out

    def tmpl_submit_field(self, ln, field):
        """
        Produces the HTML code for the specified field

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'field' *array* - the field to display in the page, with the following structure:

              - 'javascript' *string* - if the field has some associated javascript code

              - 'type' *string* - the type of field (T, F, I, H, D, S, R)

              - 'name' *string* - the name of the field

              - 'rows' *string* - the number of rows for textareas

              - 'cols' *string* - the number of columns for textareas

              - 'val' *string* - the default value of the field

              - 'size' *string* - the size for text fields

              - 'maxlength' *string* - the maximum length for text fields

              - 'htmlcode' *string* - the complete HTML code for user-defined fields

              - 'typename' *string* - the long name of the type

        """

        # load the right message language
        _ = gettext_set_language(ln)

        # If the field is a textarea
        if field['type'] == 'T':
            ## Field is a textarea:
            text="<textarea name=\"%s\" rows=\"%s\" cols=\"%s\">%s</textarea>" \
                  % (field['name'], field['rows'], field['cols'], cgi.escape(str(field['val']), 1))
        # If the field is a file upload
        elif field['type'] == 'F':
            ## the field is a file input:
            text = """<input type="file" name="%s" size="%s"%s />""" \
                   % (field['name'], field['size'], "%s" \
                      % ((field['maxlength'] in (0, None) and " ") or (""" maxlength="%s\"""" % field['maxlength'])) )
        # If the field is a text input
        elif field['type'] == 'I':
            ## Field is a text input:
            text = """<input type="text" name="%s" size="%s" value="%s"%s />""" \
                   % (field['name'], field['size'], field['val'], "%s" \
                      % ((field['maxlength'] in (0, None) and " ") or (""" maxlength="%s\"""" % field['maxlength'])) )
        # If the field is a hidden input
        elif field['type'] == 'H':
            text="<input type=\"hidden\" name=\"%s\" value=\"%s\" />" % (field['name'], field['val'])
        # If the field is user-defined
        elif field['type'] == 'D':
            text=field['htmlcode']
        # If the field is a select box
        elif field['type'] == 'S':
            text=field['htmlcode']
        # If the field type is not recognized
        else:
            text="%s: unknown field type" % field['typename']

        return text

    def tmpl_page_interface_js(self, ln, upload, field, fieldhtml, txt, check, level, curdir, values, select, radio, curpage, nbpages, images, returnto):
        """
        Produces the javascript for validation and value filling for a submit interface page

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'upload' *array* - booleans if the field is a <input type="file"> field

          - 'field' *array* - the fields' names

          - 'fieldhtml' *array* - the fields' HTML representation

          - 'txt' *array* - the fields' long name

          - 'check' *array* - if the fields should be checked (in javascript)

          - 'level' *array* - strings, if the fields should be filled (M) or not (O)

          - 'curdir' *array* - the current directory of the submission

          - 'values' *array* - the current values of the fields

          - 'select' *array* - booleans, if the controls are "select" controls

          - 'radio' *array* - booleans, if the controls are "radio" controls

          - 'curpage' *int* - the current page

          - 'nbpages' *int* - the total number of pages

          - 'images' *int* - the path to the images

          - 'returnto' *array* - a structure with 'field' and 'page', if a mandatory field on antoher page was not completed
        """

        # load the right message language
        _ = gettext_set_language(ln)

        nbFields = len(upload)
        # if there is a file upload field, we change the encoding type
        out = """<script language="JavaScript1.1" type="text/javascript">
              """
        for i in range(0,nbFields):
            if upload[i] == 1:
                out += "document.forms[0].encoding = \"multipart/form-data\";\n"
                break
        # we don't want the form to be submitted if the user enters 'Return'
        # tests if mandatory fields are well filled
        out += """function tester(){
                   return false;
                  }
                  function tester2() {
               """
        for i in range(0,nbFields):
            if re.search("%s\[\]" % field[i],fieldhtml[i]):
                fieldname = "%s[]" % field[i]
            else:
                fieldname = field[i]
            out += "  el = document.forms[0].elements['%s'];\n" % fieldname
            # If the field must be checked we call the checking function
            if check[i] != "":
                out += """if (%(check)s(el.value) == 0) {
                            el.focus();
                            return 0;
                          } """ % {
                            'check' : check[i]
                          }
            # If the field is mandatory, we check a value has been selected
            if level[i] == 'M':
                if select[i] != 0:
                    # If the field is a select box
                    out += """if ((el.selectedIndex == -1)||(el.selectedIndex == 0)){
                                    alert("%(field_mandatory)s");
                                    return 0;
                              } """ % {
                                'field_mandatory' : _("The field %s is mandatory.") % txt[i] + '\\n' + _("Please make a choice in the select box")
                              }
                elif radio[i] != 0:
                    # If the field is a radio buttonset
                    out += """var check=0;
                              for (var j = 0; j < el.length; j++) {
                                if (el.options[j].checked){
                                  check++;
                                }
                              }
                              if (check == 0) {
                                alert("%(press_button)s");
                                return 0;
                              }""" % {
                                'press_button':_("Please press a button.")
                              }
                else:
                    # If the field is a text input
                    out += """if (el.value == '') {
                               alert("%(field_mandatory)s");
                               return 0;
                              }""" % {
                                'field_mandatory' : _("The field %s is mandatory. Please fill it in.") % txt[i]
                              }
        out += """  return 1;
                  }
               <!-- Fill the fields in with the previous saved values-->
               """

        # # # # # # # # # # # # # # # # # # # # # # # # #
        # Fill the fields with the previously saved values
        # # # # # # # # # # # # # # # # # # # # # # # # #
        for i in range(0,nbFields):
            if re.search("%s\[\]"%field[i],fieldhtml[i]):
                fieldname = "%s[]" % field[i]
            else:
                fieldname = field[i]
            text = values[i]

            if text != '':
                if select[i] != 0:
                    # If the field is a SELECT element
                    vals = text.split("\n")
                    tmp=""
                    for val in vals:
                        if tmp != "":
                            tmp = tmp + " || "
                        tmp = tmp + "el.options[j].value == \"%s\" || el.options[j].text == \"%s\"" % (val,val)
                    if tmp != "":
                        out += """
                                 <!--SELECT field found-->
                                 el = document.forms[0].elements['%(fieldname)s'];
                                 for (var j = 0; j < el.length; j++){
                                   if (%(tmp)s){
                                     el.options[j].selected = true;
                                   }
                                 }""" % {
                                   'fieldname' : fieldname,
                                   'tmp' : tmp,
                                 }
                elif radio[i] != 0:
                    # If the field is a RADIO element
                    out += """<!--RADIO field found-->
                              el = document.forms[0].elements['%(fieldname)s'];
                              if (el.value == "%(text)s"){
                                el.checked=true;
                              }""" % {
                                'fieldname' : fieldname,
                                'text' : cgi.escape(str(text)),
                              }
                elif upload[i] == 0:
                    text = text.replace('"','\"')
                    text = text.replace("\n","\\n")
                    # If the field is not an upload element
                    out += """<!--input field found-->
                               el = document.forms[0].elements['%(fieldname)s'];
                               el.value="%(text)s";
                           """ % {
                             'fieldname' : fieldname,
                             'text' : cgi.escape(str(text)),
                           }
        out += """<!--End Fill in section-->
               """

        # JS function finish
        # This function tests each mandatory field in the whole submission and checks whether
        # the field has been correctly filled in or not
        # This function is called when the user presses the "End
        # Submission" button
        if int(curpage) == int(nbpages):
            out += """function finish() {
                   """
            if returnto:
                out += """alert ("%(msg)s");
                          document.forms[0].curpage.value="%(page)s";
                          document.forms[0].submit();
                         }
                       """ % {
                         'msg' : _("The field %(field)s is mandatory.") + '\n' + _("Going back to page") + returnto['page'],
                         'page' : returnto['page']
                       }
            else:
                out += """ if (tester2()) {
                             document.forms[0].action="/submit";
                             document.forms[0].step.value=1;
                             document.forms[0].submit();
                           } else {
                             return false;
                           }
                         }"""
        out += """</script>"""
        return out

    def tmpl_page_endaction(self, ln, weburl, file, nextPg, startPg, access, curpage, nbPg, nbpages, doctype, act, docname, actname, indir, mainmenu, finished, function_content, next_action, images):
        """
        Produces the pages after all the fields have been submitted.

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'weburl' *string* - The url of CDS Invenio

          - 'doctype' *string* - The document type

          - 'act' *string* - The action

          - 'docname' *string* - The document type name

          - 'actname' *string* - The action name

          - 'curpage' *int* - The current page of submitting engine

          - 'startPg' *int* - The start page

          - 'nextPg' *int* - The next page

          - 'access' *string* - The submission number

          - 'nbPg' *string* - total number of pages

          - 'nbpages' *string* - number of pages (?)

          - 'indir' *string* - the directory of submitting

          - 'file' *string* - ??

          - 'mainmenu' *string* - the url of the main menu

          - 'finished' *bool* - if the submission is finished

          - 'images' *string* - the path to the images

          - 'function_content' *string* - HTML code produced by some function executed

          - 'next_action' *string* - if there is another action to be completed, the HTML code for linking to it
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = """
          <form ENCTYPE="multipart/form-data" action="/submit" method="post">
          <input type="hidden" name="file" value="%(file)s" />
          <input type="hidden" name="nextPg" value="%(nextPg)s" />
          <input type="hidden" name="startPg" value="%(startPg)s" />
          <input type="hidden" name="access" value="%(access)s" />
          <input type="hidden" name="curpage" value="%(curpage)s" />
          <input type="hidden" name="nbPg" value="%(nbPg)s" />
          <input type="hidden" name="doctype" value="%(doctype)s" />
          <input type="hidden" name="act" value="%(act)s" />
          <input type="hidden" name="indir" value="%(indir)s" />
          <input type="hidden" name="fromdir" value="" />
          <input type="hidden" name="mainmenu" value="%(mainmenu)s" />

          <input type="hidden" name="mode" value="U" />
          <input type="hidden" name="step" value="1" />
          <input type="hidden" name="deleted" value="no" />
          <input type="hidden" name="file_path" value="" />
          <input type="hidden" name="userfile_name" value="" />

          <center><table cellspacing="0" cellpadding="0" border="0"><tr>
             <td class="submitHeader"><b>%(docname)s&nbsp;</b></td>
             <td class="submitHeader"><small>&nbsp;%(actname)s&nbsp;</small></td>
             <td valign="bottom">
                 <table cellspacing="0" cellpadding="0" border="0" width="100%%">
                 <tr><td class="submitEmptyPage">&nbsp;&nbsp;</td>
              """ % {
                'file' : file,
                'nextPg' : nextPg,
                'startPg' : startPg,
                'access' : access,
                'curpage' : curpage,
                'nbPg' : nbPg,
                'doctype' : doctype,
                'act' : act,
                'docname' : docname,
                'actname' : actname,
                'indir' : indir,
                'mainmenu' : mainmenu,
              }

        if finished == 1:
            out += """<td class="submitCurrentPage">%(finished)s</td>
                      <td class="submitEmptyPage">&nbsp;&nbsp;</td>
                     </tr></table>
                    </td>
                    <td class="submitEmptyPage" align="right">&nbsp;</td>
                   """ % {
                     'finished' : _("finished!"),
                   }
        else:
            for i in range(1, nbpages + 1):
                out += """<td class="submitPage"><small>&nbsp;
                            <a href='' onclick="document.forms[0].curpage.value=%s;document.forms[0].action='/submit';document.forms[0].step.value=0;document.forms[0].submit();return false;">%s</a>&nbsp;</small></td>""" % (i,i)
            out += """<td class="submitCurrentPage">%(end_action)s</td><td class="submitEmptyPage">&nbsp;&nbsp;</td></tr></table></td>
                      <td class="submitHeader" align="right">&nbsp;<a href='' onclick="window.open('/submit/summary?doctype=%(doctype)s&amp;act=%(act)s&amp;access=%(access)s&amp;indir=%(indir)s','summary','scrollbars=yes,menubar=no,width=500,height=250');return false;"><font color="white"><small>%(summary)s(2)</small></font></a>&nbsp;</td>""" % {
                        'end_action' : _("end of action"),
                        'summary' : _("SUMMARY"),
                        'doctype' : doctype,
                        'act' : act,
                        'access' : access,
                        'indir' : indir,
                      }
        out += """</tr>
                  <tr>
                    <td colspan="5" class="submitBody">
                      <small><br /><br />
                      %(function_content)s
                      %(next_action)s
                      <br /><br />
                    </td>
                </tr>
                <tr class="submitHeader">
                    <td class="submitHeader" colspan="5" align="center">""" % {
                       'function_content' : function_content,
                       'next_action' : next_action,
                     }
        if finished == 0:
            out += """<small>%(submission)s</small>&sup2;:
                      <small>%(access)s</small>""" % {
                        'submission' : _("Submission no"),
                        'access' : access,
                      }
        else:
            out += "&nbsp;\n"
        out += """
            </td>
        </tr>
        </table>
        </center>
        </form>
        <br />
        <br />"""
        # Add the "back to main menu" button
        if finished == 0:
            out += """ <a href="%(mainmenu)s" onclick="return confirm('%(surequit)s')">
                       <img src="%(images)s/mainmenu.gif" border="0" alt="%(back)s" align="right" /></a>
                       <br /><br />""" % {
                           'surequit' : _("Are you sure you want to quit this submission?"),
                           'back' : _("Back to main menu"),
                           'images' : images,
                           'mainmenu' : mainmenu
                           }
        else:
            out += """ <a href="%(mainmenu)s">
                       <img src="%(images)s/mainmenu.gif" border="0" alt="%(back)s" align="right" /></a>
                       <br /><br />""" % {
                     'back' : _("Back to main menu"),
                     'images' : images,
                     'mainmenu' : mainmenu,
                   }

        return out

    def tmpl_function_output(self, ln, display_on, action, doctype, step, functions):
        """
        Produces the output of the functions.

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'display_on' *bool* - If debug information should be displayed

          - 'doctype' *string* - The document type

          - 'action' *string* - The action

          - 'step' *int* - The current step in submission

          - 'functions' *aray* - HTML code produced by functions executed and informations about the functions

              - 'name' *string* - the name of the function

              - 'score' *string* - the score of the function

              - 'error' *bool* - if the function execution produced errors

              - 'text' *string* - the HTML code produced by the function
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = ""
        if display_on:
            out += """<br /><br />%(function_list)s<P>
                      <table border="1" cellpadding="15">
                        <tr><th>%(function)s</th><th>%(score)s</th><th>%(running)s</th></tr>
                   """ % {
                     'function_list' : _("Here is the %(x_action)s function list for %(x_doctype)s documents at level %(x_step)s") % {
                                         'x_action' : action,
                                         'x_doctype' : doctype,
                                         'x_step' : step,
                                       },
                     'function' : _("Function"),
                     'score' : _("Score"),
                     'running' : _("Running function"),
                   }
            for function in functions:
                out += """<tr><td>%(name)s</td><td>%(score)s</td><td>%(result)s</td></tr>""" % {
                          'name' : function['name'],
                          'score' : function['score'],
                          'result' : function['error'] and (_("Function %s does not exist.") % function['name'] + "<br />") or function['text']
                        }
            out += "</table>"
        else:
            for function in functions:
                if not function['error']:
                    out += function['text']

        return out

    def tmpl_next_action(self, ln, actions):
        """
        Produces the output of the functions.

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'actions' *array* - The actions to display, in the structure

              - 'page' *string* - the starting page

              - 'action' *string* - the action (in terms of submission)

              - 'doctype' *string* - the doctype

              - 'nextdir' *string* - the path to the submission data

              - 'access' *string* - the submission number

              - 'indir' *string* - ??

              - 'name' *string* - the name of the action
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = "<br /><br />%(haveto)s<ul>" % {
                'haveto' : _("You must now"),
              }
        i = 0
        for action in actions:
            if i > 0:
                out += " <b>" + _("or") + "</b> "
            i += 1
            out += """<li><a href="" onclick="document.forms[0].action='/submit';document.forms[0].curpage.value='%(page)s';document.forms[0].startPg.value='%(page)s';document.forms[0].act.value='%(action)s';document.forms[0].doctype.value='%(doctype)s';document.forms[0].indir.value='%(nextdir)s';document.forms[0].access.value='%(access)s';document.forms[0].fromdir.value='%(indir)s';document.forms[0].submit();return false;"> %(name)s </a></li>""" % action

        out += "</ul>"
        return out

    def tmpl_filelist(self, ln, filelist, recid, docid, version):
        """
        Displays the file list for a record.

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'recid' *string* - The record id

          - 'docid' *string* - The document id

          - 'version' *string* - The version of the document

          - 'filelist' *string* - The HTML string of the filelist (produced by the BibDoc classes)
        """

        # load the right message language
        _ = gettext_set_language(ln)

        title = _("record") + ' #' + '<a href="%s/record/%s">%s</a>' % (weburl, recid, recid)
        if docid != "":
            title += ' ' + _("document") + ' #' + str(docid)
        if version != "":
            title += ' ' + _("version") + ' #' + str(version)

        out = """<div style="width:90%%;margin:auto;min-height:100px;">
                <!--start file list-->
                  %s
                <!--end file list--></div>
              """ % (filelist)

        return out

    def tmpl_bibrecdoc_filelist(self, ln, types):
        """
        Displays the file list for a record.

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'types' *array* - The different types to display, each record in the format:

               - 'name' *string* - The name of the format

               - 'content' *array of string* - The HTML code produced by tmpl_bibdoc_filelist, for the right files
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = ""
        for mytype in types:
            out += "<small><b>%s</b> %s:</small>" % (mytype['name'], _("file(s)"))
            out += "<ul>"
            for content in mytype['content']:
                out += content
            out += "</ul>"
        return out

    def tmpl_bibdoc_filelist(self, ln, weburl, versions, imagepath, docname, id, recid):
        """
        Displays the file list for a record.

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'weburl' *string* - The url of CDS Invenio

          - 'versions' *array* - The different versions to display, each record in the format:

               - 'version' *string* - The version

               - 'content' *string* - The HTML code produced by tmpl_bibdocfile_filelist, for the right file

               - 'previous' *bool* - If the file has previous versions

          - 'imagepath' *string* - The path to the image of the file

          - 'docname' *string* - The name of the document

         - 'id' *int* - The id of the document

         - 'recid' *int* - The record id

        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = """<table border="0" cellspacing="1" class="searchbox">
                   <tr>
                     <td align="left" colspan="2" class="portalboxheader">
                       <img src='%(imagepath)s' border="0" />&nbsp;&nbsp;%(docname)s
                     </td>
                   </tr>""" % {
                     'imagepath' : imagepath,
                     'docname' : docname
                   }
        for version in versions:
            if version['previous']:
                versiontext =  """<br />(%(see)s <a href="%(weburl)s/record/%(recID)s/files/getfile.py?docid=%(id)s&amp;version=all">%(previous)s</a>)""" % {
                                 'see' : _("see"),
                                 'weburl' : weburl,
                                 'id' : id,
                                 'recID': recid,
                                 'previous': _("previous"),
                               }
            else:
                versiontext = ""
            out += """<tr>
                        <td class="portalboxheader">
                          <font size="-2">%(version)s %(ver)s%(text)s</font>
                        </td>
                        <td>
                          <table>
                        """ % {
                          'version' : _("version"),
                          'ver' : version['version'],
                          'text' : versiontext,
                        }
            for content in version['content']:
                out += content
            out += "</table></td></tr>"
        out += "</table>"
        return out

    def tmpl_bibdocfile_filelist(self, ln, weburl, id, name, selfformat, version, format, size):
        """
        Displays a file in the file list.

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'weburl' *string* - The url of CDS Invenio

          - 'id' *int* - The id of the document

          - 'name' *string* - The name of the file

          - 'selfformat' *string* - The format to pass in parameter

          - 'version' *string* - The version

          - 'format' *string* - The display format

          - 'size' *string* - The size of the file
        """

        # load the right message language
        _ = gettext_set_language(ln)

        return """<tr>
                    <td valign="top">
                      <small><a href="%(weburl)s/getfile.py?docid=%(docid)s&amp;name=%(quotedname)s&amp;format=%(selfformat)s&amp;version=%(version)s">
                        %(name)s%(format)s
                      </a></small>
                    </td>
                    <td valign="top">
                      <font size="-2" color="green">[%(size)s&nbsp;B]</font>
                    </td></tr>""" % {
                      'weburl' : weburl,
                      'docid' : id,
                      'quotedname' : urllib.quote(name),
                      'selfformat' : urllib.quote(selfformat),
                      'version' : version,
                      'name' : name,
                      'format' : format,
                      'size' : size
                    }

    def tmpl_submit_summary (self, ln, values, images):
        """
        Displays the summary for the submit procedure.

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'values' *array* - The values of submit. Each of the records contain the following fields:

                - 'name' *string* - The name of the field

                - 'mandatory' *bool* - If the field is mandatory or not

                - 'value' *string* - The inserted value

                - 'page' *int* - The submit page on which the field is entered

          - 'images' *string* - the path to the images
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = """<body style="background-image: url(%(images)s/header_background.gif);"><table border="0">""" % \
              { 'images' : images }
        
        for value in values:
            if value['mandatory']:
                color = "red"
            else:
                color = ""
            out += """<tr>
                        <td align="right">
                          <small>
                            <a href='' onclick="window.opener.document.forms[0].curpage.value='%(page)s';window.opener.document.forms[0].action='/submit';window.opener.document.forms[0].submit();return false;">
                              <font color="%(color)s">%(name)s</font>
                            </a>
                          </small>
                        </td>
                        <td>
                          <i><small><font color="black">%(value)s</font></small></i>
                        </td>
                      </tr>""" % {
                        'color' : color,
                        'name' : value['name'],
                        'value' : value['value'],
                        'page' : value['page']
                      }
        out += "</table>"
        return out

    def tmpl_yoursubmissions(self, ln, images, weburl, order, doctypes, submissions):
        """
        Displays the list of the user's submissions.

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'images' *string* - the path to the images

          - 'weburl' *string* - The url of CDS Invenio

          - 'order' *string* - The ordering parameter

          - 'doctypes' *array* - All the available doctypes, in structures:

              - 'id' *string* - The doctype id

              - 'name' *string* - The display name of the doctype

              - 'selected' *bool* - If the doctype should be selected

          - 'submissions' *array* - The available submissions, in structures:

              - 'docname' *string* - The document name

              - 'actname' *string* - The action name

              - 'status' *string* - The status of the document

              - 'cdate' *string* - Creation date

              - 'mdate' *string* - Modification date

              - 'id' *string* - The id of the submission

              - 'reference' *string* - The display name of the doctype

              - 'pending' *bool* - If the submission is pending

              - 'act' *string* - The action code

              - 'doctype' *string* - The doctype code
        """

        # load the right message language
        _ = gettext_set_language(ln)


        out = ""
        out += """
                  <br />
                  <form action="">
                  <input type="hidden" value="%(order)s" name="order" />
                  <input type="hidden" name="deletedId" />
                  <input type="hidden" name="deletedDoctype" />
                  <input type="hidden" name="deletedAction" />
                  <table class="searchbox" width="100%%" summary="" >
                    <tr>
                      <th class="portalboxheader"><small>%(for)s</small>&nbsp;
                        <select name="doctype" onchange="document.forms[0].submit();">
                          <option value="">%(alltype)s</option>
                  """ % {
                    'order' : order,
                    'for' : _("For"),
                    'alltype' : _("all types of document"),
                  }
        for doctype in doctypes:
            out += """<option value="%(id)s" %(sel)s>%(name)s</option>""" % {
                     'id' : doctype['id'],
                     'name' : doctype['name'],
                     'sel' : doctype['selected'] and "selected=\"selected\"" or ""
                   }
        out += """     </select>
                      </th>
                    </tr>
                    <tr>
                     <td class="portalboxbody">
                      <table>
                        <tr>
                          <td></td>
                        </tr>
               """

        num = 0
        docname = ""
        for submission in submissions:
            if submission['docname'] != docname:
                docname = submission['docname']
                out += """</table>
                          %(docname)s<br />
                          <table border="0" class="searchbox" align="left" width="100%%">
                            <tr>
                              <th class="headerselected">%(action)s&nbsp;&nbsp;
                                <a href='' onclick='document.forms[0].order.value="actiondown";document.forms[0].submit();return false;'><img src="%(images)s/smalldown.gif" alt="down" border="0" /></a>&nbsp;
                                <a href='' onclick='document.forms[0].order.value="actionup";document.forms[0].submit();return false;'><img src="%(images)s/smallup.gif" alt="up" border="0" /></a>
                              </th>
                              <th class="headerselected">%(status)s&nbsp;&nbsp;
                                <a href='' onclick='document.forms[0].order.value="statusdown";document.forms[0].submit();return false;'><img src="%(images)s/smalldown.gif" alt="down" border="0" /></a>&nbsp;
                                <a href='' onclick='document.forms[0].order.value="statusup";document.forms[0].submit();return false;'><img src="%(images)s/smallup.gif" alt="up" border="0" /></a>
                              </th>
                              <th class="headerselected">%(id)s</th>
                              <th class="headerselected">%(reference)s&nbsp;&nbsp;
                                <a href='' onclick='document.forms[0].order.value="refdown";document.forms[0].submit();return false;'><img src="%(images)s/smalldown.gif" alt="down" border="0" /></a>&nbsp;
                                <a href='' onclick='document.forms[0].order.value="refup";document.forms[0].submit();return false;'><img src="%(images)s/smallup.gif" alt="up" border="0" /></a>
                              </th>
                              <th class="headerselected">%(first)s&nbsp;&nbsp;
                                <a href='' onclick='document.forms[0].order.value="cddown";document.forms[0].submit();return false;'><img src="%(images)s/smalldown.gif" alt="down" border="0" /></a>&nbsp;
                                <a href='' onclick='document.forms[0].order.value="cdup";document.forms[0].submit();return false;'><img src="%(images)s/smallup.gif" alt="up" border="0" /></a>
                              </th>
                              <th class="headerselected">%(last)s&nbsp;&nbsp;
                                <a href='' onclick='document.forms[0].order.value="mddown";document.forms[0].submit();return false;'><img src="%(images)s/smalldown.gif" alt="down" border="0" /></a>&nbsp;
                                <a href='' onclick='document.forms[0].order.value="mdup";document.forms[0].submit();return false;'><img src="%(images)s/smallup.gif" alt="up" border="0" /></a>
                              </th>
                            </tr>
                       """ % {
                         'docname' : submission['docname'],
                         'action' : _("Action"),
                         'status' : _("Status"),
                         'id' : _("Id"),
                         'reference' : _("Reference"),
                         'images' : images,
                         'first' : _("First access"),
                         'last' : _("Last access"),
                       }
            if submission['pending']:
                idtext = """<a href="submit/sub?access=%(id)s@%(action)s%(doctype)s">%(id)s</a>
                            &nbsp;<a onclick='if (confirm("%(sure)s")){document.forms[0].deletedId.value="%(id)s";document.forms[0].deletedDoctype.value="%(doctype)s";document.forms[0].deletedAction.value="%(action)s";document.forms[0].submit();return true;}else{return false;}' href=''><img src="%(images)s/smallbin.gif" border="0" alt='%(delete)s' /></a>
                         """ % {
                           'images' : images,
                           'id' : submission['id'],
                           'action' : submission['act'],
                           'doctype' : submission['doctype'],
                           'sure' : _("Are you sure you want to delete this submission?"),
                           'delete' : _("Delete submission %(x_id)s in %(x_docname)s") % {
                                        'x_id' : str(submission['id']),
                                        'x_docname' : str(submission['docname'])
                                      }
                         }
            else:
                idtext = submission['id']

            if operator.mod(num,2) == 0:
                color = "#e0e0e0"
            else:
                color = "#eeeeee"

            if submission['reference']:
                reference = submission['reference']
            else:
                reference = """<font color="red">%s</font>""" % _("Reference not yet given")

            cdate = str(submission['cdate']).replace(" ","&nbsp;")
            mdate= str(submission['mdate']).replace(" ","&nbsp;")

            out += """
                     <tr bgcolor="%(color)s">
                       <td align="center" class="mycdscell">
                         <small>%(actname)s</small>
                       </td>
                       <td align="center" class="mycdscell">
                         <small>%(status)s</small>
                       </td>
                       <td class="mycdscell">
                         <small>%(idtext)s</small>
                       </td>
                       <td class="mycdscell">
                         <small>&nbsp;%(reference)s</small>
                       </td>
                       <td class="mycdscell">
                         <small>%(cdate)s</small>
                       </td>
                       <td class="mycdscell">
                         <small>%(mdate)s</small>
                       </td>
                     </tr>
                   """ % {
                     'color' : color,
                     'actname' : submission['actname'],
                     'status' : submission['status'],
                     'idtext' : idtext,
                     'reference' : reference,
                     'cdate' : cdate,
                     'mdate' : mdate,
                   }
            num += 1

        out += "</table></td></tr></table></form>"
        return out


    def tmpl_yourapprovals(self, ln, referees):
        """
        Displays the doctypes and categories for which the user is referee

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'referees' *array* - All the doctypes for which the user is referee:

              - 'doctype' *string* - The doctype

              - 'docname' *string* - The display name of the doctype

              - 'categories' *array* - The specific categories for which the user is referee:

                    - 'id' *string* - The category id

                    - 'name' *string* - The display name of the category
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = """ <table class="searchbox" width="100%%" summary="">
                    <tr>
                        <th class="portalboxheader">%(refdocs)s</th>
                    </tr>
                    <tr>
                    <td class="portalboxbody">""" % {
                      'refdocs' : _("Refereed Documents"),
                    }

        for doctype in referees:
            out += """<ul><li><b>%(docname)s</b><ul>""" % doctype

            if doctype ['categories'] is None:            
                out += '''<li><a href="publiline.py?doctype=%(doctype)s">%(generalref)s</a></li>''' % {
                    'docname' : doctype['docname'],
                    'doctype' : doctype['doctype'],
                    'generalref' : _("You are a general referee")}

            else:
                for category in doctype['categories']:
                    out += """<li><a href="publiline.py?doctype=%(doctype)s&amp;categ=%(categ)s">%(referee)s</a></li>""" % {
                        'referee' : _("You are a referee for category:") + ' ' + str(category['name']) + ' (' + str(category['id']) + ')',
			'doctype' : doctype['doctype'],
                        'categ' : category['id']}
                    
            out += "</ul><br /></li></ul>"

        out += "</td></tr></table>"
        return out

    def tmpl_publiline_selectdoctype(self, ln, docs):
        """
        Displays the doctypes that the user can select

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'docs' *array* - All the doctypes that the user can select:

              - 'doctype' *string* - The doctype

              - 'docname' *string* - The display name of the doctype
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = """
               <table class="searchbox" width="100%%" summary="">
                  <tr>
                      <th class="portalboxheader">%(list)s</th>
                  </tr>
                  <tr>
                      <td class="portalboxbody">
              %(select)s:
            </small>
            <blockquote>""" % {
              'list' : _("List of refereed types of documents"),
              'select' : _("Select one of the following types of documents to check the documents status."),
            }

        for doc in docs:
            out += "<li><a href='publiline.py?doctype=%(doctype)s'>%(docname)s</a></li><br />" % doc

        out += """</blockquote>
                </td>
            </tr>
        </table>"""
        return out

    def tmpl_publiline_selectcateg(self, ln, doctype, title, categories, images):
        """
        Displays the categories from a doctype that the user can select

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'doctype' *string* - The doctype

          - 'title' *string* - The doctype name

          - 'images' *string* - the path to the images

          - 'categories' *array* - All the categories that the user can select:

              - 'id' *string* - The id of the category

              - 'waiting' *int* - The number of documents waiting

              - 'approved' *int* - The number of approved documents

              - 'rejected' *int* - The number of rejected documents
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = """
               <table class="searchbox" width="100%%" summary="">
                  <tr>
                    <th class="portalboxheader">%(title)s: %(list_categ)s</th>
                  </tr>
                  <tr>
                      <td class="portalboxbody">
                      %(choose_categ)s
                      <blockquote>
                      <form action="publiline.py" method="get">
                          <input type="hidden" name="doctype" value="%(doctype)s" />
                          <input type="hidden" name="categ" value="" />
                          </form>
               <table>
                 <tr>
                 <td align="left">""" % {
                 'title' : title,
                 'doctype' : doctype,
                 'list_categ' : _("List of refereed categories"),
                 'choose_categ' : _("Please choose a category"),
               }

        for categ in categories:
            num = categ['waiting'] + categ['approved'] + categ['rejected']

            if categ['waiting'] != 0:
                classtext = "class=\"blocknote\""
            else:
                classtext = ""

            out += """<a href="" onclick="document.forms[0].categ.value='%(id)s';document.forms[0].submit();return false;"><small %(classtext)s>%(id)s</small></a><small> (%(num)s document(s)""" % {
                     'id' : categ['id'],
                     'classtext' : classtext,
                     'num' : num,
                   }
            if categ['waiting'] != 0:
                out += """| %(waiting)s <img alt="%(pending)s" src="%(images)s/waiting_or.gif" border="0" />""" % {
                          'waiting' : categ['waiting'],
                          'pending' : _("Pending"),
                          'images' : images,
                        }
            if categ['approved'] != 0:
                out += """| %(approved)s<img alt="%(approved_text)s" src="%(images)s/smchk_gr.gif" border="0" />""" % {
                          'approved' : categ['approved'],
                          'approved_text' : _("Approved"),
                          'images' : images,
                        }
            if categ['rejected'] != 0:
                out += """| %(rejected)s<img alt="%(rejected_text)s" src="%(images)s/cross_red.gif" border="0" />""" % {
                          'rejected' : categ['rejected'],
                          'rejected_text' : _("Rejected"),
                          'images' : images,
                        }
            out += ")</small><br />"

        out += """
                    </td>
                    <td>
                     <table class="searchbox" width="100%%" summary="">
                        <tr>
                            <th class="portalboxheader">%(key)s:</th>
                        </tr>
                        <tr>
                            <td>
                              <img alt="%(pending)s" src="%(images)s/waiting_or.gif" border="0" /> %(waiting)s<br />
                              <img alt="%(approved)s" src="%(images)s/smchk_gr.gif" border="0" /> %(already_approved)s<br />
                              <img alt="%(rejected)s" src="%(images)s/cross_red.gif" border="0" /> %(rejected_text)s<br /><br />
                              <small class="blocknote">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</small> %(somepending)s<br />
                            </td>
                        </tr>
                    </table>
                  </td>
                </tr>
                </table>
              </blockquote>
              </td>
             </tr>
            </table>""" % {
              'key' : _("Key"),
              'pending' : _("Pending"),
              'images' : images,
              'waiting' : _("Waiting for approval"),
              'approved' : _("Approved"),
              'already_approved' : _("Already approved"),
              'rejected' : _("Rejected"),
              'rejected_text' : _("Rejected"),
              'somepending' : _("Some documents are pending."),
            }
        return out

    def tmpl_publiline_selectdocument(self, ln, doctype, title, categ, images, docs):
        """
        Displays the documents that the user can select in the specified category

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'doctype' *string* - The doctype

          - 'title' *string* - The doctype name

          - 'images' *string* - the path to the images

          - 'categ' *string* - the category

          - 'docs' *array* - All the categories that the user can select:

              - 'RN' *string* - The id of the document

              - 'status' *string* - The status of the document
        """

        # load the right message language
        _ = gettext_set_language(ln)

        out = """
               <table class="searchbox" width="100%%" summary="">
                  <tr>
                    <th class="portalboxheader">%(title)s - %(categ)s: %(list)s</th>
                  </tr>
                  <tr>
                    <td class="portalboxbody">
                    %(choose_report)s
                    <blockquote>
                      <form action="publiline.py" method="get">
                        <input type="hidden" name="doctype" value="%(doctype)s" />
                        <input type="hidden" name="categ" value="%(categ)s" />
                        <input type="hidden" name="RN" value="" />
                        </form>
                  <table class="searchbox">
                    <tr>
                      <th class="portalboxheader">%(report_no)s</th>
                      <th class="portalboxheader">%(pending)s</th>
                      <th class="portalboxheader">%(approved)s</th>
                      <th class="portalboxheader">%(rejected)s</th>
                    </tr>
              """ % {
                'doctype' : doctype,
                'title' : title,
                'categ' : categ,
                'list' : _("List of refereed documents"),
                'choose_report' : _("Click on a report number for more information."),
                'report_no' : _("Report Number"),
                'pending' : _("Pending"),
                'approved' : _("Approved"),
                'rejected' : _("Rejected"),
              }

        for doc in docs:
            status = doc ['status']
            
            if status == "waiting":
                out += """<tr>
                            <td align="center">
                              <a href="" onclick="document.forms[0].RN.value='%(rn)s';document.forms[0].submit();return false;">%(rn)s</a>
                            </td>
                            <td align="center">
                              <img alt="check" src="%(images)s/waiting_or.gif" />
                            </td>
                            <td align="center">&nbsp;</td>
                            <td align="center">&nbsp;</td>
                          </tr>
                       """ % {
                         'rn' : doc['RN'],
                         'images' : images,
                       }
            elif status == "rejected":
                out += """<tr>
                            <td align="center">
                              <a href="" onclick="document.forms[0].RN.value='%(rn)s';document.forms[0].submit();return false;">%(rn)s</a>
                            </td>
                            <td align="center">&nbsp;</td>
                            <td align="center">&nbsp;</td>
                            <td align="center"><img alt="check" src="%(images)s/cross_red.gif" /></td>
                          </tr>
                       """ % {
                         'rn' : doc['RN'],
                         'images' : images,
                       }
            elif status == "approved":
                out += """<tr>
                            <td align="center">
                              <a href="" onclick="document.forms[0].RN.value='%(rn)s';document.forms[0].submit();return false;">%(rn)s</a>
                            </td>
                            <td align="center">&nbsp;</td>
                            <td align="center"><img alt="check" src="%(images)s/smchk_gr.gif" /></td>
                            <td align="center">&nbsp;</td>
                          </tr>
                       """ % {
                         'rn' : doc['RN'],
                         'images' : images,
                       }
        out += """  </table>
                    </blockquote>
                   </td>
                  </tr>
                 </table>"""
        return out

    def tmpl_publiline_displaydoc(self, ln, doctype, docname, categ, rn, status, dFirstReq, dLastReq, dAction, access, images, accessurl, confirm_send, auth_code, auth_message, authors, title, sysno, newrn):
        """
        Displays the categories from a doctype that the user can select

        Parameters:

          - 'ln' *string* - The language to display the interface in

          - 'doctype' *string* - The doctype

          - 'docname' *string* - The doctype name

          - 'categ' *string* - the category

          - 'rn' *string* - The document RN (id number)

          - 'status' *string* - The status of the document

          - 'dFirstReq' *string* - The date of the first approval request

          - 'dLastReq' *string* - The date of the last approval request

          - 'dAction' *string* - The date of the last action (approval or rejection)

          - 'images' *string* - the path to the images

          - 'accessurl' *string* - the URL of the publications

          - 'confirm_send' *bool* - must display a confirmation message about sending approval email

          - 'auth_code' *bool* - authorised to referee this document

          - 'auth_message' *string* - ???

          - 'authors' *string* - the authors of the submission

          - 'title' *string* - the title of the submission

          - 'sysno' *string* - the unique database id for the record

          - 'newrn' *string* - the record number assigned to the submission
        """

        # load the right message language
        _ = gettext_set_language(ln)

        if status == "waiting":
            image = """<img src="%s/waiting_or.gif" alt="" align="right" />""" % images
        elif status == "approved":
            image = """<img src="%s/smchk_gr.gif" alt="" align="right" />""" % images
        elif status == "rejected":
            image = """<img src="%s/iconcross.gif" alt="" align="right" />""" % images
        else:
            image = ""
        out = """
                <table class="searchbox" summary="">
                 <tr>
                  <th class="portalboxheader">%(image)s %(rn)s</th>
                 </tr>
                 <tr>
                   <td class="portalboxbody">""" % {
                   'image' : image,
                   'rn' : rn,
                 }
        if confirm_send:
            out += """<i><strong class="headline">%(requestsent)s</strong></i><br /><br />""" % {
                     'requestsent' : _("Your request has been sent to the referee."),
                   }

        out += """<form action="publiline.py">
                    <input type="hidden" name="RN" value="%(rn)s" />
                    <input type="hidden" name="categ" value="%(categ)s" />
                    <input type="hidden" name="doctype" value="%(doctype)s" />
                  <small>""" % {
                 'rn' : rn,
                 'categ' : categ,
                 'doctype' : doctype,
               }
        if title != "unknown":
            out += """<strong class="headline">%(title_text)s</strong>%(title)s<br /><br />""" % {
                     'title_text' : _("Title:"),
                     'title' : title,
                   }

        if authors != "":
            out += """<strong class="headline">%(author_text)s</strong>%(authors)s<br /><br />""" % {
                     'author_text' : _("Author:"),
                     'authors' : authors,
                   }
        if sysno != "":
            out += """<strong class="headline">%(more)s</strong>
                        <a href="%(weburl)s/record/%(sysno)s">%(click)s</a>
                        <br /><br />
                   """ % {
                     'more' : _("More information:"),
                     'click' : _("Click here"),
                     'weburl' : weburl,
                     'sysno' : sysno,
                   }

        if status == "waiting":
            out += _("This document is still %(x_fmt_open)swaiting for approval%(x_fmt_close)s.") % {'x_fmt_open': '<strong class="headline">', 
                                                                                                     'x_fmt_close': '</strong>'}
	    out += "<br /><br />"
	    out += _("It was first sent for approval on:") + ' <strong class="headline">' + str(dFirstReq) + '</strong><br />'
            if dLastReq == "0000-00-00 00:00:00":
                out += _("Last approval email was sent on:") + ' <strong class="headline">' + str(dFirstReq) + '</strong><br />'
            else:
                out += _("Last approval email was sent on:") + ' <strong class="headline">' + str(dLastReq) + '</strong><br />'
            out += "<br />" + _("You can send an approval request email again by clicking the following button:") + " <br />" +\
                   """<input class="adminbutton" type="submit" name="send" value="%(send)s" onclick="return confirm('%(warning)s')" />""" % {
                     'send' : _("Send Again"),
                     'warning' : _("WARNING! Upon confirmation, an email will be sent to the referee.")
                   }
            if auth_code == 0:
                out += "<br />" + _("As a referee for this document, you may click this button to approve or reject it.") + ":<br />" +\
                       """<input class="adminbutton" type="submit" name="approval" value="%(approve)s" onclick="window.location='approve.py?%(access)s';return false;" />""" % {
                         'approve' : _("Approve/Reject"),
                         'access' : access
                       }
        if status == "approved":
            out += _("This document has been %(x_fmt_open)sapproved%(x_fmt_close)s.") % {'x_fmt_open': '<strong class="headline">', 
                                                                                         'x_fmt_close': '</strong>'}
            out += '<br />' + _("Its approved reference is:") + ' <strong class="headline">' + str(newrn) + '</strong><br /><br />'
            out += _("It was first sent for approval on:") + ' <strong class="headline">' + str(dFirstReq) + '</strong><br />'
            if dLastReq == "0000-00-00 00:00:00":
                out += _("Last approval email was sent on:") + ' <strong class="headline">' + str(dFirstReq) + '</strong><br />'
            else:
                out += _("Last approval email was sent on:") + ' <strong class="headline">' + str(dLastReq) + '</strong><br />' +\
                       _("It was approved on:") + ' <strong class="headline">' + str(dAction) + '</strong><br />'
        if status == "rejected":
            out += _("This document has been %(x_fmt_open)srejected%(x_fmt_close)s.") % {'x_fmt_open': '<strong class="headline">',
                                                                                         'x_fmt_close': '</strong>'} 
            out += "<br /><br />"
            out += _("It was first sent for approval on:") + ' <strong class="headline">' + str(dFirstReq) +'</strong><br />'
            if dLastReq == "0000-00-00 00:00:00":
                out += _("Last approval email was sent on:") + ' <strong class="headline">' + str(dFirstReq) + '</strong><br />'
            else:
                out += _("Last approval email was sent on:") + ' <strong class="headline">' + str(dLastReq) +'</strong><br />'
            out += _("It was rejected on:") + ' <strong class="headline">' + str(dAction) + '</strong><br />'

        out += """    </small></form>
                      <br />
                    </td>
                   </tr>
                  </table>"""
        return out
    
#----------NEW STUFF-----------------
    def tmpl_wse_group_container(self, container_label, ln=cdslang):
        """
        Create html for a container with the label according to the language
        @param container_label: (dict) labels for the current container, the keys
        are the language 
        @param ln: language of the page.
        @return the HTML for this container, MUST be completed with a string value for element
        """
        _ = gettext_set_language(ln)
        
        out = """
        <!-- Open the "submission page" -->
        <div class="websubmit_form_page">
        """
        out +=  """
        <!-- WSE-Container -->
        <!-- WSE-Container-Leader -->
        <div class="wse_element_container6">
        <div class="wse_element_container_header6">%(title)s</div>
        <div class="wse_spacer">
        &nbsp;
        </div>
        <!-- /WSE-Container-Leder -->"""
        if container_label.has_key(ln):
            out %=  {"title": container_label[ln]}
        elif container_label.has_key(cdslang):
            out %=  {"title": container_label[cdslang]}
        elif container_label.values():
            out %=  {"title": container_label.values()[0]}
        else:
            out %=  {"title": ""}
        out += "%(elements)s"
        out += """
        <!-- WSE-Container-Footer -->
        <div class="wse_spacer">
        &nbsp;
        </div>
        </div>
        <!-- /WSE-Container-Footer -->
        <!-- /WSE-Container -->
        <div class="wse_spacer">
        &nbsp;
        </div>"""
        out += """</div>"""
        return out

    def tmpl_wse_html_instance(self, wse_element_html):
        """
        Put the html value of a wse_element in a div
        @param wse_element_html: (string) html value of the current wse element
        @param ln: language of the page.
        @return the HTML for this element
        """
        out = """     
        <!-- WSE-Element-Body -->
        <div class="wse_field_row">
        %(content)s
        </div>
        <!-- /WSE-Element-Body -->""" % { "content" : wse_element_html }
        return out

    def tmpl_warning_guest_user_must_login(self, ln=cdslang):
        """A message to be displayed when a guest user tries to perform some
           kind of submission-related action requiring login.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the warning message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""You seem to be a guest user. You have to
%(x_url_open)slogin%(x_url_close)s first.""") % \
             { 'x_url_open'  : '<a href="../youraccount/login?ln=' + ln + '">',
               'x_url_close' : '<a/>'}

    def tmpl_error_permission_denied_for_user_access_to_submission(self,
                                                                  user_nickname,
                                                                  submission_id,
                                                                  ln=cdslang):
        """A message to be displayed when a user attempts to manipulate a
           submission that is registered to another user in the submission log.
           @param user_nickname: (string) - the user's nickname.
           @param submission_id: (integer) - the submission ID.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""User %(x_user_nickname)s is not allowed to access 
submission %(x_submission_id)s.""") \
                % { 'x_user_nickname' : user_nickname,
                    'x_submission_id' : submission_id,
                  }

    def tmpl_error_unresolvable_doctype(self, ln=cdslang):
        """A message to be displayed when an attempt is made to create a
           submission form, but the document type is either missing or unknown.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""There was an error while trying to process your submission
(the document type could not be resolved).""")

    def tmpl_error_unresolvable_action(self, ln=cdslang):
        """A message to be displayed when an attempt is made to create a
           submission form, but the action is either missing or unknown.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""There was an error while trying to process your submission
(the action could not be resolved).""")

    def tmpl_error_submission_directory_not_found(self,
                                                  submission_id,
                                                  ln=cdslang):
        """A message to be displayed when, upon re-visiting a submission page,
           WebSubmit is unable to find the "submission directory" in the
           storage archive. (The submission directory should already exist
           when a visit to a submission page is not the first visit.)
           @param submission_id: (integer) - the submission ID.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (WebSubmit 
could not find the working directory for submission %(x_submission_id)s).""") \
                % { 'x_submission_id' : submission_id, }

    def tmpl_error_submission_directory_already_existed(self,
                                                        submission_id,
                                                        ln=cdslang):
        """A message to be displayed when WebSubmit tried to create the
           working directory for a new submission, but was unable to because
           it already existed.
           @param submission_id: (integer) - the submission ID.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (WebSubmit tried 
to create the working directory for submission %(x_submission_id)s, but it 
already existed).""") \
                % { 'x_submission_id' : submission_id, }

    def tmpl_error_couldnt_create_submission_directory(self,
                                                       submission_id,
                                                       error_message,
                                                       ln=cdslang):
        """A message to be displayed when WebSubmit tried to create the
           working directory for a new submission, but was unable to for an
           unknown reason (the error message received from the OS will be
           included into the message string that is returned).
           @param submission_id: (integer) - the submission ID.
           @param error_message: (string) - the error message received from the
            system.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (WebSubmit tried 
to create the working directory for submission %(x_submission_id)s, but it 
was not possible [%(x_error_message)s]).""") \
                    % { 'x_submission_id' : submission_id,
                        'x_error_message' : error_message,
                      }

    def tmpl_error_unresolvable_submission_config_template(self, ln=cdslang):
        """A message to be displayed when an attempt is made to process a
           submission, but the name of the submission configuration template
           is either missing or unknown.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""There was an error while trying to process your submission
(the submission configuration template's name could not be resolved).""")

    def tmpl_error_couldnt_access_submission_config_template(self,
                                                             templatename,
                                                             ln=cdslang):
        """A message to be displayed when an attempt is made to process a
           submission, but the submission configuration template is not
           readable.
           @param templatename: (string) - the name of the configuration
            template file.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (WebSubmit could 
not open submission configuration template file %(x_config_filename)s. Either 
it didn't exist as a normal file, or WebSubmit didn't have the required 
privileges to read it.""") \
                    % { 'x_config_filename' : templatename, }

    def tmpl_error_couldnt_read_submission_config_template(self,
                                                           templatename,
                                                           error_message,
                                                           ln=cdslang):
        """A message to be displayed when an attempt is made to process a
           submission, but there is a problem opening the submission
           configuration template.
           @param templatename: (string) - the name of the configuration
            template file.
           @param error_message: (string) - the error message received from the
            system.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (WebSubmit could 
not read submission configuration template file %(x_config_filename)s. 
[%(x_error_message)s]).""") \
                    % { 'x_config_filename' : templatename,
                        'x_error_message'   : error_message,
                      }

    def tmpl_error_xml_submission_template_unparsable(self,
                                                      templatename,
                                                      error_message,
                                                      ln=cdslang):
        """A message to be displayed when one of the XML configuration
           templates that describe a given submission couldnt be parsed
           due to some kind of XML error.
           @param templatename: (string) - the name of the configuration
            template file.
           @param error_message: (string) - the error message received from the
            system.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (WebSubmit could 
not parse the XML config file %(x_config_filename)s. [%(x_error_message)s])
.""") \
                    % { 'x_config_filename' : templatename,
                        'x_error_message'   : error_message,
                      }

    def tmpl_error_xml_submission_template_container_label_invalid(self,
                                                                   templatename,
                                                                   ln=cdslang):
        """A message to be displayed when during the parsing of one of the
           XML configuration templates that describe a given submission, a
           container label that is invalid was found.
           @param templatename: (string) - the name of the configuration
            template file.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (when parsing the 
XML config file %(x_config_filename)s, an invalid container-label was 
encountered. Container labels must have a language attribute and a message 
value).""") \
                    % { 'x_config_filename' : templatename, }


    def tmpl_error_xml_submission_template_element_name_missing(self,
                                                                templatename,
                                                                ln=cdslang):
        """A message to be displayed when during the parsing of one of the
           XML configuration templates that describe a given submission, an
           element node with no name is encountered.
           @param templatename: (string) - the name of the configuration
            template file.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (when parsing the 
XML config file %(x_config_filename)s, an element node without a name 
attribute was encountered. An element's name is mandatory).""") \
                    % { 'x_config_filename' : templatename, }

    def tmpl_error_xml_submission_template_element_type_missing(self,
                                                                templatename,
                                                                elementname,
                                                                ln=cdslang):
        """A message to be displayed when during the parsing of one of the
           XML configuration templates that describe a given submission, an
           element node with no type is encountered and there is no
           definition of this element in the WebSubmit common elements
           library config file.
           If an element is not declared in the library file, its type
           is mandatory.
           @param templatename: (string) - the name of the configuration
            template file.
           @param elementname: (string) - the name of the problem element.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (when parsing the 
XML config file %(x_config_filename)s, an element node [%(x_elementname)s] 
without a type attribute was encountered. If an element must be declared 
with a type either in the config file itself, or in the the common elements 
library. To repeat: element type is mandatory).""") \
                    % { 'x_config_filename' : templatename,
                        'x_elementname'     : elementname,
                      }

    def tmpl_error_xml_submission_template_node_value_missing(self,
                                                              templatename,
                                                              nodename,
                                                              ln=cdslang):
        """A message to be displayed when during the parsing of a submission
           config file, a node is encountered for which a value is
           mandatory, but is actually missing. For example, it could be
           said that if there is a "default-value" node, then there must
           actually be a value supplied for the default value.
           I.e. this could be classed as illegal:

                 <default-value />

           @param templatename: (string) - the name of the configuration
            template file.
           @param nodename: (string) - the name of the problem node.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (when parsing the 
XML config file %(x_config_filename)s, a node (%(x_nodename)s) without a 
value was encountered. A value for this node is mandatory.""") \
                    % { 'x_config_filename' : templatename,
                        'x_nodename' : nodename,
                      }

    def tmpl_error_xml_submission_template_invalid_element_label(self,
                                                                 templatename,
                                                                 elementname,
                                                                 ln=cdslang):
        """A message to be displayed when during the parsing of a submission
           config file, an element-label node with a missing "ln" attribute
           or with no value is encountered. An element label must have both a
           language and a node value.
           @param templatename: (string) - the name of the configuration
            template file.
           @param elementname: (string) - the name of the element to which
            the problem element-label node belongs.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
           
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (when parsing the 
XML config file %(x_config_filename)s, an invalid element-label node belonging 
to the element %(x_elementname)s was encountered. An element-label must have 
both a "ln" attribute and a value).""") \
                    % { 'x_config_filename' : templatename,
                        'x_elementname'     : elementname,
                      }

    def tmpl_error_xml_submission_template_invalid_element_option(self,
                                                                 templatename,
                                                                 elementname,
                                                                 ln=cdslang):
        """A message to be displayed when during the parsing of a submission
           config file, an invalid option for an element is encountered.
           @param templatename: (string) - the name of the configuration
            template file.
           @param elementname: (string) - the name of the element to which
            the problem option node belongs.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
           
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (when parsing the 
XML config file %(x_config_filename)s, an invalid "option" node belonging to 
the element %(x_elementname)s was encountered. An option must have a "value" 
attribute and if it contains option-labels, they must have "ln" 
attributes).""") \
                    % { 'x_config_filename' : templatename,
                        'x_elementname'     : elementname,
                      }

    def tmpl_error_unable_to_retrieve_WSET_class_reference(self,
                                                           wset_name,
                                                           ln=cdslang):
        """A message to be displayed when it isn't possible to obtain a
           reference to the class of a given WSET.
           @param wset_name: (string) - the WSET for which a class reference
            couldn't be retrieved/
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (it was not possible 
to retrieve a class reference for the %(x_WSET_name)s WSET.""") \
                    % { 'x_WSET_name'     : wset_name, }

    def tmpl_error_unable_to_instantiate_WSET_object(self,
                                                     wset_name,
                                                     error_message,
                                                     ln=cdslang):
        """A message to be displayed when it isn't possible to instantiate
           a WSET object from its class reference.
           @param wset_name: (string) - the WSET class name.
           @param error_message: (string) - the error message received from the
            system.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (it was not possible 
to instantiate an object of class %(x_WSET_name)s [%(x_error_message)s]).""") \
                    % { 'x_WSET_name'     : wset_name,
                        'x_error_message' : error_message,
                      }

    def tmpl_error_xml_submission_template_invalid_check_node(self,
                                                              templatename,
                                                              ln=cdslang):
        """A message to be displayed when during the parsing of one of the
           XML configuration templates that describe a given submission, an
           invalid "check" node is encountered.
           @param templatename: (string) - the name of the configuration
            template file.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (when parsing the 
XML config file %(x_config_filename)s, an invalid "check" node was 
encountered. A check node must have a "test" attribute and any of its error-
labels must have "ln" attributes and values).""") \
                    % { 'x_config_filename' : templatename, }

    def tmpl_error_xml_submission_template_invalid_check_string(self,
                                                                templatename,
                                                                ln=cdslang):
        """A message to be displayed when during the parsing of one of the
           XML configuration templates that describe a given submission, a
           "check" node with an invalid "test" value is encountered.
           @param templatename: (string) - the name of the configuration
            template file.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (when parsing the 
XML config file %(x_config_filename)s, a "check" node with an invalid 
"test" attribute was encountered).""") \
                    % { 'x_config_filename' : templatename, }


    def tmpl_error_unable_to_retrieve_WSC_function_reference(self,
                                                             wsc_name,
                                                             ln=cdslang):
        """A message to be displayed when it isn't possible to obtain a
           reference to a given WSC function from its name.
           @param wsc_name: (string) - the WSC for which a function reference
            couldn't be retrieved.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (it was not possible 
to retrieve a class reference for the %(x_WSET_name)s WSET).""") \
                    % { 'x_WSET_name'     : cgi.escape(wsc_name, 1), }

    def tmpl_error_unable_to_create_simple_WSE_XML_record(self,
                                                          error_message,
                                                          ln=cdslang):
        """A message to be displayed when it isn't possible to create the simple
           WSE XML record for a given submission.
           @param error_message: (string) - the error message received from the
            system.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (it was not possible 
to create the simple XML record [%(error)s]).""") \
                    % { 'error'       : cgi.escape(error_message, 1), }

    def tmpl_error_unable_to_create_MARCXML_record(self,
                                                   error_message,
                                                   ln=cdslang):
        """A message to be displayed when it isn't possible to create the
           MARCXML record for a given submission.
           @param error_message: (string) - the error message received from the
            system.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (it was not possible 
to create the MARCXML record [%(error)s]).""") \
                    % { 'error'       : cgi.escape(error_message, 1), }

    def tmpl_error_unable_to_read_MARCXML_record(self,
                                                   error_message,
                                                   ln=cdslang):
        """A message to be displayed when it isn't possible to read the
           MARCXML record that has been created in a given submission's
           working directory.
           @param error_message: (string) - the error message received from the
            system.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (it was not possible 
to read the MARCXML record [%(error)s]).""") \
                    % { 'error'       : cgi.escape(error_message, 1), }

    def tmpl_error_unable_to_create_record_preview_lockfile(self,
                                                            error_message,
                                                            ln=cdslang):
        """A message to be displayed when it isn't possible to create the
           lock-file that is used to signify that a preview of the submitted
           data has been shown to the user.
           @param error_message: (string) - the error message received from the
            system.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (it was not possible 
to create the "submitted data previewed" lockfile: [%(error)s]).""") \
                    % { 'error'       : cgi.escape(error_message, 1), }

    def tmpl_error_unable_to_delete_record_preview_lockfile(self,
                                                            error_message,
                                                            ln=cdslang):
        """A message to be displayed when it isn't possible to delete the
           lock-file that is used to signify that a preview of the submitted
           data has been shown to the user.
           @param error_message: (string) - the error message received from the
            system.
           @param ln: (string) - the language that the message is to be
            displayed in.
           @return: (string) - the error message.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)
        ## Return the message:
        return _("""An unexpected internal error occurred (it was not possible 
to remove the "submitted data previewed" lockfile: [%(error)s]).""") \
                    % { 'error'       : cgi.escape(error_message, 1), }

    def tmpl_new_record_preview_page(self,
                                     doctype,
                                     action,
                                     config,
                                     submissionid,
                                     categories,
                                     record_preview,
                                     ln=cdslang):
        """Create a page that allows the user to see a preview of the record
           that they are about to submit and asks for confirmation that it's
           OK to proceed with the submission.
           @param doctype: (string) - the document type of the submission.
           @param action: (string) - the action.
           @param config: (string) - the config name.
           @param submissionid: (string) - the identifier of the submission.
           @param categories: (list) - the categories into which the
            submission is being made.
           @param record_preview: (string) - a preview of the record.
           @param ln: (string) - the interface language. It defaults to
            cdslang if not supplied.
        """
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)

        ## Wash categories (it needs to be a list or tuple):
        if type(categories) is str:
            ## Since categories is a string, it needs to be put into a list:
            categories = [categories]
        elif type(categories) not in (list, tuple):
            ## Invalid format for categories - suppress it:
            categories = []

        ## A buffer in which to put the form's HTML:
        out = ""

        ## Open the form:
        out += """
<form action="/submit" method="post" enctype="multipart/form-data">
"""

        ## Add some constant (hidden) system fields into the form:
        out += """
  <input type="hidden" name="ln" value="%(language)s" />
  <input type="hidden" name="WebSubmit_document_type" value="%(doctype)s" />
  <input type="hidden" name="WebSubmit_action" value="%(action)s" />
  <input type="hidden" name="WebSubmit_Submission_Config" value="%(config)s" />
  <input type="hidden" name="WebSubmit_submissionid" value="%(submissionid)s" />
"""     % { 'language'     : cgi.escape(ln, 1),
            'doctype'      : cgi.escape(doctype, 1),
            'action'       : cgi.escape(action, 1),
            'config'       : cgi.escape(config, 1),
            'submissionid' : cgi.escape(str(submissionid), 1),
          }

        ## Add the "categories" into the form. We should have a list of them
        ## and just add each member into a hidden "WebSubmit_category" field:
        for category in categories:
            out += """
  <input type="hidden" name="WebSubmit_category" value="%(category)s" />""" \
            % { 'category' : cgi.escape(category, 1), }

        ## Add a message about the preview, followed by confirm submission and
        ## edit data buttons:
        out += """
<div style="color: green;">
%(x_preview_descr)s
</div>
<br />
<div style="text-align: center;">
<input type="submit" name="WebSubmitEditForm" value="%(x_edit_data)s" 
class="formbutton" />
&nbsp;&nbsp;
<input type="submit" name="WebSubmitFormSubmit" 
value="%(x_confirm_submission)s" class="formbutton" />
</div>
<br />
<br />
</form>""" % { 'x_preview_descr'      : _("""
The information that you're about to submit can be seen in the record preview 
below - please check it. Note that it's only a rough preview and there may be 
minor differences in the final presentation. Nevertheless, you should check 
that the data itself is correct.  If everything looks OK, you must confirm 
the submission. If there is a problem however, you can edit the data again. 
Do you want to confirm this submission?"""),
               'x_edit_data'          : \
                 _("""No! I need to change something!"""),
               'x_confirm_submission' : \
                 _("""Yes! Go ahead and submit the data!"""),
            }

        ## Now add the record preview into the output buffer:
        out += """\n%s\n""" % record_preview

        ## return the newly created form to the caller:
        return out


    def tmpl_submission_form_body(self,
                                  doctype,
                                  action,
                                  config,
                                  submissionid,
                                  categories,
                                  main_form_content,
                                  error_messages=None,
                                  ln=cdslang):
        ## Setup gettext for the interface language:
        _ = gettext_set_language(ln)

        ## Wash error_messages (it needs to be a list or tuple):
        if type(error_messages) is str:
            ## Since error messages is a string, it needs to be put into a list:
            error_messages = [error_messages]
        elif type(error_messages) not in (list, tuple):
            ## Invalid format for error messages - suppress it:
            error_messages = []

        ## Wash categories (it needs to be a list or tuple):
        if type(categories) is str:
            ## Since categories is a string, it needs to be put into a list:
            categories = [categories]
        elif type(categories) not in (list, tuple):
            ## Invalid format for categories - suppress it:
            categories = []

        ## A buffer in which to put the form's HTML:
        out = ""

        ## Add the error messages if there are any:
        for error_message in error_messages:
            out += "%s<br />\n" % error_message

        ## Open the form:
        out += """
<form action="/submit" method="post" enctype="multipart/form-data">
"""

        ## Add some constant (hidden) system fields into the form:
        out += """
  <input type="hidden" name="ln" value="%(language)s" />
  <input type="hidden" name="WebSubmit_document_type" value="%(doctype)s" />
  <input type="hidden" name="WebSubmit_action" value="%(action)s" />
  <input type="hidden" name="WebSubmit_Submission_Config" value="%(config)s" />
  <input type="hidden" name="WebSubmit_submissionid" value="%(submissionid)s" />
"""     % { 'language'     : cgi.escape(ln, 1),
            'doctype'      : cgi.escape(doctype, 1),
            'action'       : cgi.escape(action, 1),
            'config'       : cgi.escape(config, 1),
            'submissionid' : cgi.escape(str(submissionid), 1),
          }

        ## Add the "categories" into the form. We should have a list of them
        ## and just add each member into a hidden "WebSubmit_category" field:
        for category in categories:
            out += """
  <input type="hidden" name="WebSubmit_category" value="%(category)s" />""" \
            % { 'category' : cgi.escape(category, 1), }

        ## Now add the WSE & container content into the output buffer:
        out += """
%s
""" \
        % main_form_content

        ## Add a "finish submission" button and close the form:
        out += """
  <input type="submit" name="WebSubmitFormSubmit" value="%(x_finish_submission)s" />
</form>""" % { 'x_finish_submission' : cgi.escape(_("Finish Submission"), 1), }

        ## return the newly created form to the caller:
        return out




#------END OF NEW STUFF-------------------------
