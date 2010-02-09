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
bhr_famous_software - plugin to guess OAI ID for famous software.
"""


import urlparse

from invenio.websearch_external_collections_getter import async_download, HTTPAsyncPageGetter


CFG_FAMOUS_SCRIPT_PATHS = (
    "/dspace-oai/request",
    "/perl/oai2",
    "/cgi/oai2",
    "/oai/request",
    "/cgi/oai2.cgi",
    "/oai/",
    "/dice/oai",
    "/cgi-bin/oai.exe",
    "/oai/oai2.php",
    "/dlibra/oai-pmh-repository.xml",
    "/oaiextended/request",
    "/OAI-PUB",
    "/phpoai/oai2.php",
    "/oai/oai.php",
    "/oai/scielo-oai.php",
    "/oai",
    "/oai2/oai2.php",
    "/fedora/oai",
    "/servlets/OAIDataProvider",
    "/request",
    "/oai2d.py/"
)

def get_full_registry():
    return {}

def guess_oai_pmh_handler(url):
    baseurl = "%s://%s" % (urlparse.urlsplit(url)[0:2])
    pagegetters = [HTTPAsyncPageGetter(baseurl + path + '?verb=Identify') for path in CFG_FAMOUS_SCRIPT_PATHS]
    async_download(pagegetters, timeout=3)
    ret = set()
    for pagegetter in pagegetters:
        if pagegetter.done:
            data = pagegetter.data
            if "<OAI-PMH" in data and "Identify" in data:
                ret.add(pagegetter.uri[:-len("?verb=Identify")])
    return ret

