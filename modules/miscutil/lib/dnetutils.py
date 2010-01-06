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
CDS Invenio utilities to interact with D-NET.
"""

import os
import sys
import threading

from xml.dom.minidom import parseString
if sys.hexversion < 0x2060000:
    try:
        import simplejson as json
        simplejson_available = True
    except ImportError:
        # Okay, no Ajax app will be possible, but continue anyway,
        # since this package is only recommended, not mandatory.
        simplejson_available = False
else:
    import json
    simplejson_available = True


from invenio.config import CFG_CACHEDIR

CFG_DNET_VOCABULARY_DIR = os.path.join(CFG_CACHEDIR, 'D-NET', 'vocabularies')

_vocabularies_cache_lock = threading.Lock()
_vocabularies_cache_lock.acquire()
try:
    _vocabularies_cache = {}
finally:
    _vocabularies_cache_lock.release()

_autocomplete_cache_lock = threading.Lock()
_autocomplete_cache_lock.acquire()
try:
    _autocomplete_cache = {}
finally:
    _autocomplete_cache_lock.release()

def load_vocabulary(text, inverted=False):
    """
    Given the XML of a D-NET vocabulary, return a mapping
    with encoding->english_name content.

    @param text: the XML.
    @type text: string
    @return: the mapping.
    @rtype: dict
    """
    ret = {}
    vocabulary = parseString(text)
    terms = vocabulary.getElementsByTagName("TERM")
    for term in terms:
        key = term.getAttribute("encoding").encode('utf8')
        value = term.getAttribute("english_name").encode('utf8')
        if inverted:
            ret[value] = key
        else:
            ret[key] = value
    return ret

def load_vocabulary_from_file(name, inverted=False):
    """
    Given a name, load a corresponding D-NET vocabulary from
    C{CFG_CACHEDIR/D-NET/vocabularies/{NAME}.xml}.

    @param name: the name of a vocabulary (without extension).
    @type name: string
    @return: the mapping.
    @rtype: dict

    @see: L{load_vocabulary}
    """
    vocabulary_path = os.path.join(CFG_DNET_VOCABULARY_DIR, '%s.xml' % name)
    _vocabularies_cache_lock.acquire()
    try:
        if (name, inverted) in _vocabularies_cache:
            if _vocabularies_cache[(name, inverted)][0] >= os.path.getmtime(vocabulary_path):
                return _vocabularies_cache[(name, inverted)][1]
        _vocabularies_cache[(name, inverted)] = (os.path.getmtime(vocabulary_path), load_vocabulary(open(vocabulary_path).read(), inverted=inverted))
        return _vocabularies_cache[(name, inverted)][1]
    finally:
        _vocabularies_cache_lock.release()

def vocabulary_changed_p(name, inverted=False):
    """
    Given a vocabulary, return True if it has changed on disk and must
    be rivalidated.
    """
    vocabulary_path = os.path.join(CFG_DNET_VOCABULARY_DIR, '%s.xml' % name)
    _vocabularies_cache_lock.acquire()
    try:
        if (name, inverted) in _vocabularies_cache:
            return _vocabularies_cache[(name, inverted)][0] < os.path.getmtime(vocabulary_path)
        else:
            return True
    finally:
        _vocabularies_cache_lock.release()

def list_vocabularies():
    """
    @return: a list of names of existing vocabularies.
    @rtype: list of strings
    """

    ret = []
    if os.path.exists(CFG_DNET_VOCABULARY_DIR):
        for filename in os.listdir(CFG_DNET_VOCABULARY_DIR):
            if filename.endswith('.xml'):
                ret.append(filename[:-len('.xml')])
    return ret

def get_ajax_suggestions(name, query, cmp_function=lambda x, y: cmp(x.lower(), y.lower())):
    """
    Return in the format:
        {
            query:'Li',
            suggestions:['Liberia','Libyan Arab Jamahiriya','Liechtenstein','Lithuania'],
            data:['LR','LY','LI','LT']
        }
    the suggestion for a given vocabulary.
    @param name: the name of D-NET vocabulary.
    @type name: string
    @param query: part of the string that should be suggested.
    @type query: string
    @return: a JSon string in the above format.
    @rtype: string

    @see: <http://www.devbridge.com/projects/autocomplete/jquery/>
    """
    def bisect(a, x):
        lo = 0
        hi = len(a)
        while lo < hi:
            mid = (lo+hi) // 2
            if cmp_function(x, a[mid]) < 0:
                hi = mid
            else:
                lo = mid + 1
        return lo

    if not simplejson_available:
        return "{}"

    _autocomplete_cache_lock.acquire()
    try:
        if vocabulary_changed_p(name, True) and (name, cmp_function) in _autocomplete_cache:
            del _autocomplete_cache[(name, cmp_function)]

        if name not in _autocomplete_cache:
            vocabulary = load_vocabulary_from_file(name, inverted=True)
            keys = vocabulary.keys()
            keys.sort(cmp=cmp_function)
            _autocomplete_cache[(name, cmp_function)] = (keys, vocabulary, {})
        if query not in _autocomplete_cache[(name, cmp_function)][2]:
            keys = _autocomplete_cache[(name, cmp_function)][0]
            vocabulary = _autocomplete_cache[(name, cmp_function)][1]
            from_key = bisect(keys, query)
            to_key = from_key + 1
            while to_key < len(keys) and keys[to_key].startswith(query):
                to_key += 1
            suggestions = keys[from_key:to_key]
            data = []
            for key in suggestions:
                data.append(vocabulary[key])
            _autocomplete_cache[(name, cmp_function)][2][query] = json.dumps({
                'query' : query,
                'suggestions' : suggestions,
                'data' : data
            })
        return _autocomplete_cache[(name, cmp_function)][2][query]
    finally:
        _autocomplete_cache_lock.release()
