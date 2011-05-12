#!/usr/bin/env python

import random, os, sys
import tempfile
import marshal
from datetime import timedelta, datetime, date

from invenio.bibtask import task_low_level_submission
from invenio.bibknowledge import get_kbr_keys
from invenio.textutils import encode_for_xml
from invenio.config import CFG_TMPDIR
from invenio.chomsky import chomsky

CFG_CHOMSKY_DIR = os.path.join(CFG_TMPDIR, 'chomsky')

rns = {}

def bst_chomsky(howmany=1, collection="TEST"):
    global rns
    marcxml_template = open(os.path.join(CFG_CHOMSKY_DIR, "template_marcxml.xml")).read()
    names = open(os.path.join(CFG_CHOMSKY_DIR, "names.txt")).read().split("\n")[:-1]
    pids = open(os.path.join(CFG_CHOMSKY_DIR, "projects.txt")).read().split("\n")[:-1]
    journals = get_kbr_keys('journal_name')
    language = get_kbr_keys('languages')

    rns = marshal.load(open(os.path.join(CFG_CHOMSKY_DIR, "rns.dat")))

    def random_date(from_date=date(2008, 1, 1), to_date=date(2011, 1, 1)):
        delta = to_date - from_date
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return (from_date + timedelta(seconds=random_second))

    def random_rn():
        year = random.randrange(2008, 2011)
        if year not in rns:
            rns[year] = 0
        rns[year] += 1
        marshal.dump(rns, open(os.path.join(CFG_CHOMSKY_DIR, "rns.dat"), 'w'))
        return 'OpenAIRE-TEST-%s-%03d' % (year, rns[year])

    output = ""
    for i in xrange(howmany):
        print >> sys.stderr, "Creating record %i" % i
        dcfields = dict(AUTHOR = encode_for_xml("%s, %s" % (random.choice(names), random.choice(names))),
                    TITLE = encode_for_xml(chomsky(1)),
                    DESCRIPTION = encode_for_xml(chomsky(4)),
                    SUBJECT = encode_for_xml(chomsky(1)),
                    DATE = random_date(),
                    JOURNAL = encode_for_xml(random.choice(journals)[0]),
                    LANGUAGE = encode_for_xml(random.choice(language)[0]),
                    RN = encode_for_xml(random_rn()),
                    YEAR = random.randrange(2008, 2011),
                    AUTHOR2 = '',
                    EMBARGO = '',
                    FULLTEXT = encode_for_xml(os.path.join(CFG_CHOMSKY_DIR, 'test.pdf')),
                    PID = random.choice(pids),
                    COLLECTION = collection
                    )
        rights = random.choice(['closedAccess', 'embargoedAccess', 'restrictedAccess', 'openAccess'])
        dcfields['LICENSE'] = rights
        if rights == 'embargoedAccess':
            embargo_date = random_date().strftime('%Y-%m-%d')
            dcfields["EMBARGO"] = """    <datafield tag="942" ind1=" " ind2=" ">
            <subfield code="a">%s</subfield>
        </datafield>""" % embargo_date
        dcfields['RIGHTS'] = rights

        if random.random() > .5:
            dcfields["AUTHOR2"] = """    <datafield tag="700" ind1=" " ind2=" ">
            <subfield code="a">%s</subfield>
        </datafield>""" % encode_for_xml("%s, %s" % (random.choice(names), random.choice(names)))

        output += marcxml_template % dcfields

    fd, name = tempfile.mkstemp(dir=CFG_CHOMSKY_DIR, suffix='.xml')
    os.write(fd, output)
    os.close(fd)
    task_low_level_submission('bibupload', 'Chomsky', '-i', name, '-P5', '-uChomsky')

if __name__ == "__main__":
    bst_chomsky()