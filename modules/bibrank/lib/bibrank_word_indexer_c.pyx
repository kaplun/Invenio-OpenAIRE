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
Cythonized BibRank word ranking algorithms.
"""

from marshal import loads, dumps
from zlib import compress, decompress
from time import time
from invenio.bibtask import task_get_option, task_update_progress, \
    task_sleep_now_if_required, write_message

from invenio.errorlib import register_exception
from invenio.dbquery import run_sql

cdef extern from "math.h":
    float sqrtf(float x)
    float floorf(float x)
    float logf(float x)

def test():
    cdef float x = 1
    x = x / 0.0
    print x
    return x

def update_rnkWORD(str table, list terms):
    """Updates rnkWORDF and rnkWORDR with Gi and Nj values. For each term in rnkWORDF, a Gi value for the term is added. And for each term in each document, the Nj value for that document is added. In rnkWORDR, the Gi value for each term in each document is added. For description on how things are computed, look in the hacking docs.
    table - name of forward index to update
    terms - modified terms"""

    cdef float stime = time()
    cdef dict Gi = {}
    cdef dict Nj = {}
    cdef int N = run_sql("select count(id_bibrec) from %sR" % table[:-1])[0][0]
    cdef int i, j, max_id
    cdef tuple terms_docs, docs_terms
    cdef str hitlist, t, termlist
    cdef dict term_docs
    cdef tuple tf
    cdef list records
    cdef float log2N = logf(2) * logf(N)

    if not terms and task_get_option("quick") == "yes":
        write_message("No terms to process, ending...")
        return ""
    elif task_get_option("quick") == "yes": #not used -R option, fast calculation (not accurate)
        write_message("Beginning post-processing of %s terms" % len(terms))
        task_update_progress("Post-processing %s terms" % len(terms))
        #Locating all documents related to the modified/new/deleted terms, if fast update,
        #only take into account new/modified occurences
        write_message("Phase 1: Finding records containing modified terms")
        i = 0

        while i < len(terms):
            terms_docs = get_from_forward_index(terms, i, (i+5000), table)
            for (t, hitlist) in terms_docs:
                term_docs = deserialize_via_marshal(hitlist)
                if term_docs.has_key("Gi"):
                    del term_docs["Gi"]
                for (j, tf) in term_docs.iteritems():
                    if (task_get_option("quick") == "yes" and tf[1] == 0) or task_get_option("quick") == "no":
                        Nj[j] = 0
            write_message("Phase 1: ......processed %s/%s terms" % ((i+5000>len(terms) and len(terms) or (i+5000)), len(terms)))
            task_update_progress("Post-processing phase 1: %s/%s terms" % ((i+5000>len(terms) and len(terms) or (i+5000)), len(terms)))
            i += 5000
            task_sleep_now_if_required()
        write_message("Phase 1: Finished finding records containing modified terms")
        task_sleep_now_if_required()
        #Find all terms in the records found in last phase
        write_message("Phase 2: Finding all terms in affected records")
        records = Nj.keys()
        i = 0
        while i < len(records):
            docs_terms = get_from_reverse_index(records, i, (i + 5000), table)
            for (j, termlist) in docs_terms:
                doc_terms = deserialize_via_marshal(termlist)
                for (t, tf) in doc_terms.iteritems():
                    Gi[t] = 0
            write_message("Phase 2: ......processed %s/%s records " % ((i+5000>len(records) and len(records) or (i+5000)), len(records)))
            task_update_progress("Post-processing phase 2: %s/%s records" % ((i+5000>len(records) and len(records) or (i+5000)), len(records)))

            i += 5000
            task_sleep_now_if_required()
        write_message("Phase 2: Finished finding all terms in affected records")

    else: #recalculate
        max_id = run_sql("SELECT MAX(id) FROM %s" % table)[0][0]
        write_message("Beginning recalculation of %s terms" % max_id)

        terms = []
        i = 0
        while i < max_id:
            terms_docs = get_from_forward_index_with_id(i, (i+5000), table)
            for (t, hitlist) in terms_docs:
                Gi[t] = 0
                term_docs = deserialize_via_marshal(hitlist)
                if term_docs.has_key("Gi"):
                    del term_docs["Gi"]
                for (j, tf) in term_docs.iteritems():
                    Nj[j] = 0
            write_message("Phase 1: ......processed %s/%s terms" % ((i+5000)>max_id and max_id or (i+5000), max_id))
            task_update_progress("Post-processing phase 1: %s/%s terms" % ((i+5000)>max_id and max_id or (i+5000), max_id))
            i += 5000
            task_sleep_now_if_required()

        write_message("Phase 1: Finished finding which records contains which terms")
        write_message("Phase 2: Jumping over..already done in phase 1 because of -R option")
    task_sleep_now_if_required()
    terms = Gi.keys()
    Gi = {}
    i = 0
    if task_get_option("quick") == "no":
        #Calculating Fi and Gi value for each term
        write_message("Phase 3: Calculating importance of all affected terms")
        while i < len(terms):
            terms_docs = get_from_forward_index(terms, i, (i+5000), table)
            for (t, hitlist) in terms_docs:
                term_docs = deserialize_via_marshal(hitlist)
                if term_docs.has_key("Gi"):
                    del term_docs["Gi"]
                Fi = 0
                Gi[t] = 1
                for (j, tf) in term_docs.iteritems():
                    Fi += tf[0]
                for (j, tf) in term_docs.iteritems():
                    if tf[0] != Fi and Fi != 0:
                        Gi[t] += ((<float>tf[0] / Fi) * logf(<float>tf[0] / Fi)) / log2N
            write_message("Phase 3: ......processed %s/%s terms" % ((i+5000>len(terms) and len(terms) or (i+5000)), len(terms)))
            task_update_progress("Post-processing phase 3: %s/%s terms" % ((i+5000>len(terms) and len(terms) or (i+5000)), len(terms)))
            i += 5000
            task_sleep_now_if_required()
        write_message("Phase 3: Finished calculating importance of all affected terms")
    else:
        #Using existing Gi value instead of calculating a new one. Missing some accurancy.
        write_message("Phase 3: Getting approximate importance of all affected terms")
        while i < len(terms):
            terms_docs = get_from_forward_index(terms, i, (i+5000), table)
            for (t, hitlist) in terms_docs:
                term_docs = deserialize_via_marshal(hitlist)
                if term_docs.has_key("Gi"):
                    Gi[t] = term_docs["Gi"][1]
                elif len(term_docs) == 1:
                    Gi[t] = 1
                else:
                    Fi = 0
                    Gi[t] = 1
                    for (j, tf) in term_docs.iteritems():
                        Fi += tf[0]
                    for (j, tf) in term_docs.iteritems():
                        if tf[0] != Fi and Fi != 0:
                            Gi[t] += (<float>tf[0] / Fi) * logf(<float>tf[0] / Fi) / log2N
            write_message("Phase 3: ......processed %s/%s terms" % ((i+5000>len(terms) and len(terms) or (i+5000)), len(terms)))
            task_update_progress("Post-processing phase 3: %s/%s terms" % ((i+5000>len(terms) and len(terms) or (i+5000)), len(terms)))
            i += 5000
            task_sleep_now_if_required()
        write_message("Phase 3: Finished getting approximate importance of all affected terms")
    task_sleep_now_if_required()
    write_message("Phase 4: Calculating normalization value for all affected records and updating %sR" % table[:-1])
    records = Nj.keys()
    i = 0
    while i < len(records):
        #Calculating the normalization value for each document, and adding the Gi value to each term in each document.
        docs_terms = get_from_reverse_index(records, i, (i + 5000), table)
        for (j, termlist) in docs_terms:
            doc_terms = deserialize_via_marshal(termlist)
            try:
                for (t, tf) in doc_terms.iteritems():
                    if Gi.has_key(t):
                        Nj[j] = Nj.get(j, 0) + (Gi[t] * (logf(1 + tf[0]))) ** 2
                        Git = <int>(floorf(Gi[t]*100))
                        if Git >= 0:
                            Git += 1
                        doc_terms[t] = (tf[0], Git)
                    else:
                        Nj[j] = Nj.get(j, 0) + (tf[1] * (logf(1 + tf[0]))) ** 2
                Nj[j] = 1.0 / sqrtf(Nj[j])
                Nj[j] = <int>(Nj[j] * 100)
                if Nj[j] >= 0:
                    Nj[j] += 1
                run_sql("UPDATE %sR SET termlist=%%s WHERE id_bibrec=%%s" % table[:-1],
                        (serialize_via_marshal(doc_terms), j))
            except (ZeroDivisionError, OverflowError), e:
                ## This is to try to isolate division by zero errors.
                register_exception(prefix="Error when analysing the record %s (%s): %s\n" % (j, repr(docs_terms), e), alert_admin=True)
        write_message("Phase 4: ......processed %s/%s records" % ((i+5000>len(records) and len(records) or (i+5000)), len(records)))
        task_update_progress("Post-processing phase 4: %s/%s records" % ((i+5000>len(records) and len(records) or (i+5000)), len(records)))
        i += 5000
        task_sleep_now_if_required()
    write_message("Phase 4: Finished calculating normalization value for all affected records and updating %sR" % table[:-1])
    task_sleep_now_if_required()
    write_message("Phase 5: Updating %s with new normalization values" % table)
    i = 0
    terms = Gi.keys()
    while i < len(terms):
        #Adding the Gi value to each term, and adding the normalization value to each term in each document.
        terms_docs = get_from_forward_index(terms, i, (i+5000), table)
        for (t, hitlist) in terms_docs:
            try:
                term_docs = deserialize_via_marshal(hitlist)
                if term_docs.has_key("Gi"):
                    del term_docs["Gi"]
                for (j, tf) in term_docs.iteritems():
                    if Nj.has_key(j):
                        term_docs[j] = (tf[0], Nj[j])
                Git = <int>(floorf(Gi[t]*100))
                if Git >= 0:
                    Git += 1
                term_docs["Gi"] = (0, Git)
                run_sql("UPDATE %s SET hitlist=%%s WHERE term=%%s" % table,
                        (serialize_via_marshal(term_docs), t))
            except (ZeroDivisionError, OverflowError), e:
                register_exception(prefix="Error when analysing the term %s (%s): %s\n" % (t, repr(terms_docs), e), alert_admin=True)
        write_message("Phase 5: ......processed %s/%s terms" % ((i+5000>len(terms) and len(terms) or (i+5000)), len(terms)))
        task_update_progress("Post-processing phase 5: %s/%s terms" % ((i+5000>len(terms) and len(terms) or (i+5000)), len(terms)))
        i += 5000
        task_sleep_now_if_required()
    write_message("Phase 5:  Finished updating %s with new normalization values" % table)
    write_message("Time used for post-processing: %.1fmin" % ((time() - stime) / 60))
    write_message("Finished post-processing")
    task_update_progress("Post-processing done")

cpdef get_from_forward_index(list terms, int start, int stop, str table):
    cdef int j
    cdef tuple terms_docs = ()
    stop = min(len(terms), stop)
    for j from start <= j < stop:
        terms_docs += run_sql("SELECT term, hitlist FROM %s WHERE term=%%s" % table, (terms[j],))
    return terms_docs

cpdef get_from_forward_index_with_id(int start, int stop, str table):
    cdef tuple terms_docs = run_sql("SELECT term, hitlist FROM %s WHERE id BETWEEN %%s AND %%s" % table, (start, stop))
    return terms_docs

cpdef get_from_reverse_index(list records, int start, int stop, str table):
    cdef str current_recs = "%s" % records[start:stop]
    cdef tuple docs_terms
    current_recs = current_recs[1:-1]
    docs_terms = run_sql("SELECT id_bibrec, termlist FROM %sR WHERE id_bibrec IN (%s)" % (table[:-1], current_recs))
    return docs_terms

cdef serialize_via_marshal(obj):
    """Serialize Python object via marshal into a compressed string."""
    return compress(dumps(obj))

cdef deserialize_via_marshal(str string):
    """Decompress and deserialize string into a Python object via marshal."""
    return loads(decompress(string))
