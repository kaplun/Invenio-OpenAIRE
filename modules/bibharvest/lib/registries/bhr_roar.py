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
bhr_roar - plugin to retrieve data from the ROAR registry.
"""
__revision__ = "$Id$"


import threading
import time
import os
import urllib
import urlparse

from invenio.config import CFG_CACHEDIR

## Number of seconds after which to refresh the ROAR
## database
CFG_ROARLIB_REFRESH_ROAR_DICT = 24 * 60 * 60
CFG_ROARLIB_RAWLIST_URL = "http://roar.eprints.org/rawlist.txt"

_roar_data_lock = threading.Lock()
_roar_data_lock.acquire()
try:
    _roar_data = []
    _roar_data_handlers = {}
    _roar_data_timestamp = 0.
finally:
    _roar_data_lock.release()

def _get_host(url):
    return urlparse.urlsplit(url)[1]

def get_full_registry():
    """
    @return: the ROAR database. This is a list of dictionaries where
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
    global _roar_data, _roar_data_timestamp, _roar_data_handlers

    def add_item(item):
        global _roar_data, _roar_data_handlers
        if item:
            _roar_data.append(item)
            if "oai_pmh" in item:
                oai_pmh = item["oai_pmh"]
                host = _get_host(oai_pmh)
                if host not in _roar_data_handlers:
                    _roar_data_handlers[host] = set()
                _roar_data_handlers[host].add(oai_pmh)
                if "home_page" in item:
                    host = _get_host(item["home_page"])
                    if host not in _roar_data_handlers:
                        _roar_data_handlers[host] = set()
                    _roar_data_handlers[host].add(oai_pmh)

    def load_roar_file(path):
        _roar_data = []
        _roar_data_handlers = {}
        roar_file = open(path)
        item = {}
        for row in roar_file:
            if not row.strip():
                add_item(item)
                item = {}
                continue
            try:
                key, value = row.split(':', 1)
            except Exception, err:
                print "%s: %s" % (err, row)
                raise err
            item[key.strip()] = value.strip()
        ## Let's add the last item, if any
        add_item(item)

    _roar_data_lock.acquire()
    try:
        if _roar_data and (time.time() - _roar_data_timestamp) < CFG_ROARLIB_REFRESH_ROAR_DICT:
            return _roar_data
        roarpath = os.path.join(CFG_CACHEDIR, 'roar_dict.txt')
        if not os.path.exists(roarpath) or time.time() - os.path.getmtime(roarpath) >= CFG_ROARLIB_REFRESH_ROAR_DICT:
            urllib.urlretrieve(CFG_ROARLIB_RAWLIST_URL, roarpath)
        _roar_data_timestamp = os.path.getmtime(roarpath)
        load_roar_file(roarpath)
        return _roar_data
    finally:
        _roar_data_lock.release()

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
    return _roar_data_handlers.get(hostname, set())
