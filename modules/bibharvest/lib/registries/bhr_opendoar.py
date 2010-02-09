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
bhr_opendoar - plugin to retrieve data from the OpenDOAR registry..
"""
__revision__ = "$Id$"

import threading
import time
import os
import urllib
import urlparse
from xml.dom.minidom import parseString

from invenio.config import CFG_CACHEDIR

## Number of seconds after which to refresh the OPENDOAR
## database
CFG_OPENDOARLIB_REFRESH_OPENDOAR_DICT = 24 * 60 * 60
CFG_OPENDOARLIB_RAWLIST_URL = "http://www.opendoar.org/api.php?all=y&show=min"

_opendoar_data_lock = threading.Lock()
_opendoar_data_lock.acquire()
try:
    _opendoar_data = []
    _opendoar_data_handlers = {}
    _opendoar_data_timestamp = 0.
finally:
    _opendoar_data_lock.release()

def _get_host(url):
    return urlparse.urlsplit(url)[1]

def get_full_registry():
    """
    @return: the OpenDOAR database. This is a list of dictionaries where
        each element of the list represent a repository.
        e.g.:
            eprintid: 1
            rev_number: 26
            eprint_status: archive
            dir: disk0/00/00/00/01
            datestamp: 2010-01-06 13:43:48
            lastmod: 2010-02-06 06:44:52
            status_changed: 2010-01-06 13:43:48
            type: subject
            metadata_visibility: show
            item_issues_count: 0
            home_page: http://archivesic.ccsd.cnrs.fr/
            title: @RCHIVESIC
            oai_pmh: http://archivesic.ccsd.cnrs.fr/oai/oai.php
            location_country: fr
            software: hal
            geoname: geoname_2_FR
            version: other
            date: 2002-05-17 19:24:41
            activity_low: 70
            activity_medium: 0
            activity_high: 0
            recordcount: 1118
            recordhistory: 0,0,0,0,0,0,0,0,0,0,0,0,77,290,489,619,748,901,1000,1115,1118
            registry_name: opendoar
            registry_name: celestial
            registry_id: 58
            registry_id: 669
    @rtype: list of dict
    """
    global _opendoar_data, _opendoar_data_timestamp, _opendoar_data_handlers

    def add_item(xml):
        global _opendoar_data, _opendoar_data_handlers
        item = {}
        for row in xml.childNodes:
            if row.nodeType == row.ELEMENT_NODE:
                if row.firstChild:
                    key = row.nodeName.encode('utf8')
                    value = row.firstChild.nodeValue.encode('utf8')
                    item[key] = value
        _opendoar_data.append(item)
        if "rOaiBaseUrl" in item:
            oai_pmh = item["rOaiBaseUrl"]
            host = _get_host(oai_pmh)
            if host not in _opendoar_data_handlers:
                _opendoar_data_handlers[host] = set()
            _opendoar_data_handlers[host].add(oai_pmh)
            if "rUrl" in item:
                host = _get_host(item["rUrl"])
                if host not in _opendoar_data_handlers:
                    _opendoar_data_handlers[host] = set()
                _opendoar_data_handlers[host].add(oai_pmh)

    def load_opendoar_file(path):
        _opendoar_data = []
        _opendoar_data_handlers = {}
        opendoar_file = open(path)
        item = {}
        for item in parseString(opendoar_file.read()).getElementsByTagName("repository"):
            add_item(item)
        ## Let's add the last item, if any

    _opendoar_data_lock.acquire()
    try:
        if _opendoar_data and (time.time() - _opendoar_data_timestamp) < CFG_OPENDOARLIB_REFRESH_OPENDOAR_DICT:
            return _opendoar_data
        opendoarpath = os.path.join(CFG_CACHEDIR, 'opendoar_dict.txt')
        if not os.path.exists(opendoarpath) or time.time() - os.path.getmtime(opendoarpath) >= CFG_OPENDOARLIB_REFRESH_OPENDOAR_DICT:
            urllib.urlretrieve(CFG_OPENDOARLIB_RAWLIST_URL, opendoarpath)
        _opendoar_data_timestamp = os.path.getmtime(opendoarpath)
        load_opendoar_file(opendoarpath)
        return _opendoar_data
    finally:
        _opendoar_data_lock.release()

def guess_oai_pmh_handler(url):
    """
    Guess the OAI-PMH handler for the given URL.

    @param url: a possible url for which there might be one or more
        OAI-PMH handlers available.
    @type url: string
    @return: the list of OAI-PMH handler URLs.
    @rtype: list of string
    """
    hostname = _get_host(url)
    get_full_registry()
    return _opendoar_data_handlers.get(hostname, set())
