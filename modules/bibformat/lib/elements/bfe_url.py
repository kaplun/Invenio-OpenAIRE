# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2006, 2007, 2008, 2009, 2010, 2011 CERN.
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
"""BibFormat element - Prints full-text URLs
"""
__revision__ = "$Id$"

import cgi

from invenio.bibdocfile import bibdocfile_url_p
from invenio.bibformat_elements.bfe_fulltext import serve_external_url_through_invenio

def format_element(bfo, style, separator='; '):
    """
    This is the default format for formatting full-text URLs.
    @param separator: the separator between urls.
    @param style: CSS class of the link
    """

    urls_u = bfo.fields("8564_u")
    if style != "":
        style = 'class="'+style+'"'

    if not bibdocfile_url_p(url):
        final_url = serve_external_url_through_invenio(url)
    else:
        final_url = url

    urls = []

    for url in urls_u:
        if not bibdocfile_url_p(url):
            final_url = serve_external_url_through_invenio(url)
        else:
            final_url = url
        urls.append('<a '+ style + \
            'href="' + cgi.escape(final_url, True) + '">' + cgi.escape(url) +'</a>')
    return separator.join(urls)

def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0
