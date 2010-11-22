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

"""
CDS Invenio utilities to interact with D-NET.
"""

import os
import sys
import threading
import thread
import psycopg2
import pyRXP

from invenio.bibknowledge import add_kb_mapping, kb_exists, update_kb_mapping, add_kb, kb_mapping_exists, add_kb_mapping, remove_kb_mapping, get_kbr_keys, get_kb_mappings

if sys.hexversion < 0x2060000:
    try:
        import simplejson as json
    except ImportError:
        # Okay, no Ajax app will be possible, but continue anyway,
        # since this package is only recommended, not mandatory.
        pass
else:
    import json



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


from invenio.config import CFG_CACHEDIR, CFG_DNET_PG_DSN

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

_DB_CONN = {}

try:
    _db_cache
except NameError:
    _db_cache = {}

def _db_login(relogin = 0):
    """Login to the database."""

    ## Note: we are using "use_unicode=False", because we want to
    ## receive strings from MySQL as Python UTF-8 binary string
    ## objects, not as Python Unicode string objects, as of yet.

    ## Note: "charset='utf8'" is needed for recent MySQLdb versions
    ## (such as 1.2.1_p2 and above).  For older MySQLdb versions such
    ## as 1.2.0, an explicit "init_command='SET NAMES utf8'" parameter
    ## would constitute an equivalent.  But we are not bothering with
    ## older MySQLdb versions here, since we are recommending to
    ## upgrade to more recent versions anyway.

    thread_ident = thread.get_ident()
    if relogin:
        _DB_CONN[thread_ident] =psycopg2.connect(CFG_DNET_PG_DSN)
        return _DB_CONN[thread_ident]
    else:
        if _DB_CONN.has_key(thread_ident):
            return _DB_CONN[thread_ident]
        else:
            _DB_CONN[thread_ident] =psycopg2.connect(CFG_DNET_PG_DSN)
            return _DB_CONN[thread_ident]

def dnet_save_query_into_pgreplayqueue(query, param):
    """
    If for some reason the D-NET Db is not working, we save a query and its
    param inside the pgreplayqueue, and we expect a daemon to replay such
    query in the future.
    """
    from invenio.dbquery import run_sql
    from marshal import dumps
    from zlib import compress
    run_sql("INSERT INTO pgreplayqueue(query, first_try, last_try) VALUES(%s, NOW(), NOW())", (compress(dumps((query, param)))))

def dnet_run_sql(sql, param=None, n=0, with_desc=0, support_replay=True):
    """Run SQL on the server with PARAM and return result.

    @param param: tuple of string params to insert in the query (see
        notes below)

    @param n: number of tuples in result (0 for unbounded)

    @param with_desc: if True, will return a DB API 7-tuple describing
        columns in query.

    @param support_replay: if support_replay is True then, in case of errors,
        the query is queued and replayed later in the future. Of course
        this flag should be set to false when the query is actually being
        replayed from the very queue, as otherwise we would enter an endless
        loop (at least in case of errors ;-).

    @return: If SELECT, SHOW, DESCRIBE statements, return tuples of
        data, followed by description if parameter with_desc is
        provided.  If INSERT, return last row id.  Otherwise return
        SQL result as provided by database.

    @note: When the site is closed for maintenance (as governed by the
        config variable CFG_ACCESS_CONTROL_LEVEL_SITE), do not attempt
        to run any SQL queries but return empty list immediately.
        Useful to be able to have the website up while MySQL database
        is down for maintenance, hot copies, table repairs, etc.

    @note: In case of problems, exceptions are returned according to
        the Python DB API 2.0.  The client code can import them from
        this file and catch them.
    """

    ### log_sql_query(sql, param) ### UNCOMMENT ONLY IF you REALLY want to log all queries

    if param:
        param = tuple(param)

    try:
        db = _db_login()
        cur = db.cursor()
        rc = cur.execute(sql, param)
        db.commit()
    except (psycopg2.OperationalError, psycopg2.InternalError): # unexpected disconnect, bad malloc error, etc
        # FIXME: now reconnect is always forced, we may perhaps want to ping() first?
        try:
            db = _db_login(relogin=1)
            cur = db.cursor()
            rc = cur.execute(sql, param)
            db.commit()
        except (psycopg2.OperationalError, psycopg2.InternalError): # again an unexpected disconnect, bad malloc error, etc
            if support_replay and sql.split()[0].upper() in ("INSERT", "UPDATE", "DELETE"):
                dnet_save_query_into_pgreplayqueue(sql, param)
            raise

    if sql.split()[0].upper() in ("SELECT", "SHOW", "DESC", "DESCRIBE"):
        if n:
            recset = cur.fetchmany(n)
        else:
            recset = cur.fetchall()
        if with_desc:
            return recset, cur.description
        else:
            return recset
    else:
        if sql.split()[0].upper() == "INSERT":
            rc =  cur.lastrowid
        return rc


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

def get_oaioaf(path):
    return pyRXP.Parser().parse(open(path).read())

def oaioaf2oafs(oaioaf):
    for elem in oaioaf[2]:
        if elem[0] == 'ListRecords':
            return elem[2]

def oafs2oafrecords(oafs):
    for record in oafs:
        if isinstance(record, tuple) and record[0] == 'record':
            yield record[2]

def oafrecords2oafmetadatas(oafrecords):
    for oafrecord in oafrecords:
        for elem in oafrecord:
            if isinstance(elem, tuple) and elem[0] == 'metadata':
                yield elem[2]

def oafrecords2oafheaders(oafrecords):
    for oafrecord in oafrecords:
        for elem in oafrecord:
            if isinstance(elem, tuple) and elem[0] == 'header':
                yield elem[2]

def oafheaders2setSpec(oafheaders):
    for oafheader in oafheaders:
        for elem in oafheader:
            if isinstance(elem, tuple) and elem[0] == 'setSpec':
                yield elem[2][0]


def oafmetadatas2realoafs(oafmetadatas):
    for oafmetadata in oafmetadatas:
        for elem in oafmetadata:
            if isinstance(elem, tuple) and elem[0] == 'oaf:OAF':
                yield elem[2]

def realoafs2dicts(realoafs):
    for realoaf in realoafs:
        out = {}
        for elem in realoaf:
            out[elem[0][len("oaf:"):]] = elem[2] and elem[2][0] or ''
        yield out

def path2dicts(path):
    xml = oaioaf2oafs(get_oaioaf(path))
    setSpec = ""
    for setSpec in oafheaders2setSpec(oafrecords2oafheaders(oafs2oafrecords(xml))):
        break
    return setSpec, list(realoafs2dicts(oafmetadatas2realoafs(oafrecords2oafmetadatas(oafs2oafrecords(xml)))))

def merge_into_kbs(path):
    table, data = path2dicts(path)
    for row in data:
        if table == 'organizations':
            kb = 'institutes'
            key = row.get('legal_name', "")
            value = row.get('legal_name', "")
        elif table == 'languages':
            kb = 'languages'
            key = row.get('languageid', "")
            value = row.get('name', "")
        elif table == 'projects_projectsubjects':
            kb = 'project_subjects'
            key = row.get('project', "")
            value = row.get('project_subject', "")
        elif table == 'projects':
            kb = 'projects'
            key = row.get('grant_agreement_number', "")
            value = (row.get("acronym", "") or row.get("title", "")) + ' - ' + (row.get("title", "") or row.get("acronym", "")) + ' (' + row.get("grant_agreement_number", "") + ')'

        if kb_mapping_exists(kb, key):
            update_kb_mapping(kb, key, key, value)
        else:
            add_kb_mapping(kb, key, value)

        if table == 'projects':
            kb = 'json_projects'
            key = row.get("projectid", "")
            value = json.dumps(row)
            if kb_mapping_exists(kb, key):
                update_kb_mapping(kb, key, key, value)
            else:
                add_kb_mapping(kb, key, value)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        merge_into_kbs(sys.argv[1])
