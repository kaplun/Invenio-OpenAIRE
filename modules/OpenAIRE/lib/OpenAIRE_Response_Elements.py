## This file is part of Invenio.
## Copyright (C) 2010, 2011 CERN.
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

"""All the OpenAIRE response elements"""

import os
from invenio.messages import gettext_set_language
from invenio.config import CFG_SITE_SUPPORT_EMAIL, CFG_SITE_URL
from invenio.htmlutils import create_html_tag
from invenio.oai_harvest_getter import magic_harvest_a_record, guess_oai_pmh_handler, guess_oai_pmh_id
from invenio.bibformat import format_record
from invenio.websubmit_functions.Shared_Functions import get_all_values_in_curdir
from invenio.webuser import collect_user_info

CFG_ACCESS_MODES = ('open access', 'restricted', 'embargo')

def ask_publication_remote_url_form(req, curdir, ln):
    """
    Implement the following workflow:

    1) show the user the REMOTE_URL input.
    2) user enter the REMOTE_URL and submit.
    3a) either OAI_PMH_BASE or OAI_PMH_ID cannot be guessed.
    4a) user is invited to fill the OAI_PMH_BASE/OAI_PMH_ID and submit
    5) a record can be retrieved and a detailed format is displayed to the user
    6) user tick a RECORD_IS_FINE checkbox
    """
    _ = gettext_set_language(ln)
    curdir_dict = get_all_values_in_curdir(curdir)
    remote_url = curdir_dict.get("REMOTE_URL", "")
    oai_phm_base = curdir_dict.get("OAI_PMH_BASE", "")
    curdir = curdir_dict["curdir"]

    out = create_html_tag("tr",
        create_html_tag("td",
            create_html_tag("label", _("Please, insert the URL pointing to the detailed record of your publication"), attrs={"for": "REMOTE_URL"})
        ) + create_html_tag("td",
            create_html_tag("input", type="text", name="REMOTE_URL", id="REMOTE_URL", value=remote_url)
        )
    )

    if oai_phm_base:
        oai_phm_bases = [oai_phm_base]
    else:
        oai_phm_bases = []

    if not oai_phm_bases and remote_url:
        try:
            oai_phm_bases = guess_oai_pmh_handler(remote_url)
        except:
            oai_phm_bases = []

    if not oai_phm_bases and remote_url:
        out += create_html_tag("tr",
            create_html_tag("td",
                create_html_tag("label", _("Please, explicitly specify the OAI-PMH base URL for the repository. If you do not know this value, either contact your repository manager or %(email)s:") % {
                "email" : create_html_tag("a", CFG_SITE_SUPPORT_EMAIL, escape_body=True, href="mailto:%s" % CFG_SITE_SUPPORT_EMAIL)
                }, attrs={"for": "OAI_PMH_BASE"})
            ) + create_html_tag("td",
                create_html_tag("input", type="text", name="OAI_PMH_BASE", id="OAI_PMH_BASE", value=oai_phm_base)
            )
        )

    oai_phm_id = curdir_dict.get("OAI_PMH_ID", "")
    if not oai_phm_id and remote_url:
        try:
            oai_phm_id = guess_oai_pmh_id(remote_url)
        except:
            oai_phm_id = ""
    if not oai_phm_id and remote_url:
        out += create_html_tag("tr",
            create_html_tag("td",
                create_html_tag("label", _("Please, explicitly specify the OAI-PMH identifier for your document within the repository. If you do not know this value, either contact your repository manager or %(email)s:") % {
                "email" : create_html_tag("a", CFG_SITE_SUPPORT_EMAIL, escape_body=True, href="mailto:%s" % CFG_SITE_SUPPORT_EMAIL)
                }, attrs={"for": "OAI_PMH_ID"})
            ) + create_html_tag("td",
                create_html_tag("input", type="text", name="OAI_PMH_ID", id="OAI_PMH_ID", value=oai_phm_id)
            )
        )

    out = create_html_tag("table", out)

    if oai_phm_bases and oai_phm_id:
        record = magic_harvest_a_record(remote_url, oai_phm_bases, oai_phm_id)
        open(os.path.join(curdir, "recmysql"), "w").write(record)
        formatted_record = format_record(0, "hd", ln=ln, user_info=collect_user_info(req), xml_record=record)
        out += create_html_tag("div", formatted_record, attrs={"style": "border-style: outset; background-color: #F0F0F0;"})

        out += create_html_tag("br")
        out += create_html_tag("input", type="button", name="endS", width="400", height="50", value=_("Continue Submission"), onclick="if (tester2()){document.forms[0].curpage.value=2;user_must_confirm_before_leaving_page = false;document.forms[0].submit();return false;} else {return false;}; return false;", attrs={"class": "adminbutton", })
        out += create_html_tag("input", type="button", name="endS", width="400", height="50", value=_("Try with another URL"), onclick="document.forms[0].submit();", attrs={"class": "adminbutton", })

    else:
        out += create_html_tag("input", type="submit", name="endS", width="400", height="50", value=_("Submit"), onclick="document.forms[0].submit();", attrs={"class": "adminbutton"})

    return out

def autocomplete_input_field(curdir, field_name, kbname):
    curdir_dict = get_all_values_in_curdir(curdir)
    field_value = curdir_dict.get(field_name, '')
    out = """<script type="text/javascript">
    jQuery(document).ready(function() {
        jQuery("#field_name").autocomplete({
            source: "%(site)s/kb/export?kbname=%(kb)s&format=jquery"
        });
    });
    </script>
    <div class="ui-widget"><input id="%(field_name)s" name="%(field_name)s" value="%(value)s"/></div>""" % {
        'site': CFG_SITE_URL,
        'kb': kbname,
        'field_name': field_name,
        'value': field_value,
        }
    return out

def license_field(req, curdir, ln, access_mode_field='OPENACCESSMODE', embargo_end_date_field='OPEN_EMBARGO_END_DATE'):
    curdir_dict = get_all_values_in_curdir(curdir)
    access_mode = curdir_dict.get(access_mode_field, 'Select:')
    if access_mode not in CFG_ACCESS_MODES:
        access_mode = 'Select:'
    embargo_end_date = curdir_dict.get(embargo_end_date_field)
    out = r"""<script type="text/javascript">
function check_access_mode() {
    access_mode = document.forms[0].%(access_mode_field)s.value;
    embargo_end_date = document.forms[0].%(embargo_end_date_field)s.value;
    /* Check in case the embargo is set that the date is at least well formed. */
    return (access_mode != 'Select:') && (access_mode != 'embargo' || embargo_end_date.match("/\d\d\d\d\/\d\d?\//\d\d?/"));
}

function apply_access_mode_change() {
    access_mode = document.forms[0].%(access_mode_field)s.value;
    if (access_mode == 'embargo') {
        document.getElementById('%(embargo_end_date_field)s_div').style.display='';
    } else {
        document.getElementById('%(embargo_end_date_field)s_div').style.display='none';
    }
    return 1;
}
</script>
""" % {
    'access_mode_field': access_mode_field,
    'embargo_end_date_field': embargo_end_date_field,
}

    out += """<select name="%(access_mode_field)s" onchange="apply_access_mode_change();"><option disabled="disabled">Select:</option>""" % {'access_mode_field': access_mode_field}
    for value in CFG_ACCESS_MODES:
        selected = value == access_mode and ' selected="selected"' or ''
        out += """<option%(selected)s>%(access_mode)s</option>""" % {'access_mode': value, 'selected': selected}
    out += """</select>"""
    out += """<div id="%(embargo_end_date_field)s_div">Embargo end date: <input type="text" id="%(embargo_end_date_field)s" name="%(embargo_end_date_field)s"></div>
<script type="text/javascript">
  Calendar.setup(
    {
      inputField  : "%(embargo_end_date_field)s",         // ID of the input field
      ifFormat    : "%%Y/%%m/%%d",    // the date format
    }
  );
</script>""" % {
    'embargo_end_date_field': embargo_end_date_field
}

    out += """<script type="text/javascript">apply_access_mode_change();</script>"""
    return out
