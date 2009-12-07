# -*- coding: utf-8 -*-
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
WebSubmit NG Web Templates.
"""

class Template:
    def tmpl_default_html_submit_interface(elements):
        """
        Build the default submission interface by combining the different
        elements.
        @param elements: a list of tuples of the form:
            (name, label, html, handle_label)
        @type elements: [(string, string, string, bool), ...]
        @note: if handle_label is True, the element HTML is expected to already
            contain (if though necessary, the label).
        """
        out = '<table class="websubmitng_form"><tbody>\n'
        for name, label, html, handle_label elements:
            out += '  <tr>\n'
            if handle_label:
                out += '    <td class="websubmitng_element" colspan="2">\n'
                out += html
                out += '    </td>\n'
            else:
                out += '    <td class="websubmitng_label">\n'
                out += '      <label for="%s">%s</label>\n' % (escape(name, True), label)
                out += '    </td>\n'
                out += '    <td class="websubmitng_element">\n'
                out += html
                out += '    </td>\n'
            else:
            out += '  <tr>\n'
        out += '</tbody></table>\n'
        return out

