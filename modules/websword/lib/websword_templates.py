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

from invenio.atom import AtomFeed
from cStringIO import StringIO

class Template:
    def tmpl_package_support(self):
        return """<?xml version="1.0" encoding='utf-8'?>
<service xmlns="http://www.w3.org/2007/app"
         xmlns:atom="http://www.w3.org/2005/Atom"
         xmlns:sword="http://purl.org/net/sword/"
         xmlns:dcterms="http://purl.org/dc/terms/">

 <sword:version>1.3</sword:version>
 <workspace>

   <atom:title>%(title)s</atom:title>
   <collection
       href="http://www.myrepository.ac.uk/atom/geography-collection" >
     <atom:title>My Repository : Geography Collection</atom:title>
     <accept>application/zip</accept>
     <sword:collectionPolicy>Collection Policy</sword:collectionPolicy>
     <dcterms:abstract>Collection description</dcterms:abstract>
     <sword:acceptPackaging q="1.0">http://www.loc.gov/METS/</sword:acceptPackaging>
   </collection>

 </workspace>
</service>"""

    def tmpl_app_collection_in_service_document(self, atom_title, href, app_accepts=None, app_categories=None, sword_accept_packagings = None):
        if app_accepts is None:
            app_accepts = []
        if app_categories is None:
            app_categories = []
        if sword_accept_packagings is None:
            sword_accept_packagings = []
        return """<collection href="%(href)s">
  <atom:title>%(atom_title)s</atom_title>
  %(app_accepts)s
  %(app_categories)s

</collection>""" % {
        "href": href,
        "atom_title": atom_title,
        "app_accepts": '\n'.join([tmpl_app_accept(app_accept) for app_accept in app_accepts]),
        "app_categories": '\n'.join([tmpl_app_categories(app_category) for app_category in app_categories])}

    def tmpl_atom_entry_document(self, atom_id, title, atom_contributor=None, sword_user_agent=None, sword_treatment=None, sword_verbose_description=None, sword_no_op=None, sword_packaging=None):
        extra_attrs = {'xmlns:sword': 'http://purl.org/net/sword/'}
        if atom_contributor:
            extra_attrs["atom:contributor"] = atom_contributor
        if sword_user_agent:
            extra_attrs["sword:userAgent"] = sword_user_agent
        if sword_treatment:
            extra_attrs["sword:treatment"] = sword_treatment
        if sword_verbose_description:
            extra_attrs["sword:verboseDescription"] = sword_verbose_description
        if sword_no_op:
            extra_attrs["sword:noOp"] = sword_no_op
        if sword_packaging:
            extra_attrs["sword:packaging"] = sword_packaging

        atom_feed = AtomFeed(atom_id=atom_id, title=title, extra_attrs=extra_attrs)
        out = StringIO()
        atom_feed.write(out, 'UTF8')
        return out.getvalue()

    def tmpl_sword_error(error_url, summary):
        return """\
<<?xml version="1.0" encoding='utf-8'?>
<sword:error xmlns="http://www.w3.org/2007/app"
         xmlns:atom="http://www.w3.org/2005/Atom"
         xmlns:sword="http://purl.org/net/sword/"
         xmlns:dcterms="http://purl.org/dc/terms/">