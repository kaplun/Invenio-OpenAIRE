## This file is part of Invenio.
## Copyright (C) 2007, 2008, 2009, 2010, 2011 CERN.
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

import invenio.template
from invenio.config import CFG_SITE_LANG, CFG_SITE_URL
from invenio.bibdocfile import list_types_from_array, list_versions_from_array
from invenio.textutils import nice_size

websubmit_templates = invenio.template.load('websubmit')
websearch_templates = invenio.template.load('websearch')

class Template:
    def tmpl_display_bibdocfile(self, bibdocfile, ln = CFG_SITE_LANG):
        """Returns a formatted representation of this docfile."""
        return websubmit_templates.tmpl_bibdocfile_filelist(
                 ln = ln,
                 recid = bibdocfile.recid,
                 version = bibdocfile.version,
                 md = bibdocfile.md,
                 name = bibdocfile.name,
                 superformat = bibdocfile.get_superformat(),
                 subformat = bibdocfile.subformat,
                 nice_size = nice_size(bibdocfile.get_size()),
                 description = bibdocfile.description or ''
               )

    def tmpl_display_bibdoc(self, bibdoc, version="", ln=CFG_SITE_LANG,
                            display_hidden=True):
        """
        Returns an HTML representation of the this document.

        @param version: if not set, only the last version will be displayed. If
            'all', all versions will be displayed.
        @type version: string (integer or 'all')
        @param ln: the language code.
        @type ln: string
        @param display_hidden: whether to include hidden files as well.
        @type display_hidden: bool
        @return: the formatted representation.
        @rtype: HTML string
        """
        t = ""
        if version == "all":
            docfiles = bibdoc.list_all_files(list_hidden=display_hidden)
        elif version != "":
            version = int(version)
            docfiles = bibdoc.list_version_files(version, list_hidden=display_hidden)
        else:
            docfiles = bibdoc.list_latest_files(list_hidden=display_hidden)
        icon = bibdoc.get_icon(display_hidden=display_hidden)
        if icon:
            imageurl = icon.get_url()
        else:
            imageurl = "%s/img/smallfiles.gif" % CFG_SITE_URL

        versions = []
        for version in list_versions_from_array(docfiles):
            currversion = {
                            'version' : version,
                            'previous' : 0,
                            'content' : []
                          }
            if version == bibdoc.get_latest_version() and version != 1:
                currversion['previous'] = 1
            for docfile in docfiles:
                if docfile.get_version() == version:
                    currversion['content'].append(self.tmpl_display_bibdocfile(docfile, ln = ln))
            versions.append(currversion)

        if versions:
            return websubmit_templates.tmpl_bibdoc_filelist(
                ln = ln,
                versions = versions,
                imageurl = imageurl,
                docname = bibdoc.get_docname(),
                recid = bibdoc.get_recid()
                )
        else:
            return ""


    def tmpl_display_bibrecdocs(self, bibrecdocs, docname="", version="", doctype="", ln=CFG_SITE_LANG, verbose=0, display_hidden=True):
        """
        Returns an HTML representation of the the attached documents.

        @param docname: if set, include only the requested document.
        @type docname: string
        @param version: if not set, only the last version will be displayed. If
            'all', all versions will be displayed.
        @type version: string (integer or 'all')
        @param doctype: is set, include only documents of the requested type.
        @type doctype: string
        @param ln: the language code.
        @type ln: string
        @param verbose: if greater than 0, includes debug information.
        @type verbose: integer
        @param display_hidden: whether to include hidden files as well.
        @type display_hidden: bool
        @return: the formatted representation.
        @rtype: HTML string
        """
        t = ""
        if docname:
            try:
                bibdocs = [bibrecdocs.get_bibdoc(docname)]
            except InvenioWebSubmitFileError:
                bibdocs = bibrecdocs.list_bibdocs(doctype)
        else:
            bibdocs = bibrecdocs.list_bibdocs(doctype)
        if bibdocs:
            types = list_types_from_array(bibdocs)
            fulltypes = []
            for mytype in types:
                if mytype in ('Plot', 'PlotMisc'):
                    # FIXME: quick hack to ignore plot-like doctypes
                    # on Files tab
                    continue
                fulltype = {
                            'name' : mytype,
                            'content' : [],
                           }
                for bibdoc in bibdocs:
                    if mytype == bibdoc.get_type():
                        fulltype['content'].append(
                            self.tmpl_display_bibdoc(bibdoc, version,
                                ln=ln, display_hidden=display_hidden))
                fulltypes.append(fulltype)

            if verbose >= 9:
                verbose_files = str(bibrecdocs)
            else:
                verbose_files = ''

            t = websubmit_templates.tmpl_bibrecdoc_filelist(
                  ln=ln,
                  types = fulltypes,
                  verbose_files=verbose_files
                )
        return t

