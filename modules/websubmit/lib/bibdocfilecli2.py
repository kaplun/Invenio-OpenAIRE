# -*- coding: utf-8 -*-
##
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007 CERN.
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
BibDocAdmin CLI administration tool
"""

__revision__ = "$Id: bibdocfilecli.py,v 1.2 2008/04/22 17:26:47 kaplun Exp $"

import sys
import os
import re
import datetime
import time
from optparse import OptionParser, OptionGroup, OptionValueError
from logging import warning, error, debug, info

from invenio.config import CFG_TMPDIR, CFG_SITE_URL, CFG_WEBSUBMIT_FILEDIR
from invenio.bibdocfile import BibRecDocs, BibDoc, InvenioWebSubmitFileError, \
    nice_size, check_valid_url, clean_url, get_docname_from_url, \
    get_format_from_url, KEEP_OLD_VALUE
from invenio.intbitset import intbitset
from invenio.search_engine import perform_request_search
from invenio.textutils import wrap_text_in_a_box, wait_for_user
from invenio.dbquery import run_sql
from invenio.bibtask import task_low_level_submission, get_datetime
from invenio.bibrecord import encode_for_xml

CFG_IDS_CHUNK_SIZE=100

def _xml_mksubfield(key, subfield, fft):
    return fft.get(key) and '\t\t<subfield code="%s">%s</subfield>\n' % (subfield, encode_for_xml(fft[key])) or ''

def _xml_fft_creator(fft):
    """Transform an fft dictionary (made by keys url, docname, format,
    new_docname, icon, comment, description, restriction, doctype, into an xml
    string."""
    out = '\t<datafield tag ="FFT" ind1=" " ind2=" ">\n'
    out += _xml_mksubfield('url', 'a', fft)
    out += _xml_mksubfield('docname', 'n', fft)
    out += _xml_mksubfield('format', 'f', fft)
    out += _xml_mksubfield('new_docname', 'm', fft)
    out += _xml_mksubfield('doctype', 't', fft)
    out += _xml_mksubfield('description', 'd', fft)
    out += _xml_mksubfield('comment', 'z', fft)
    out += _xml_mksubfield('restriction', 'r', fft)
    out += _xml_mksubfield('icon', 'x', fft)
    out += _xml_mksubfield('options', 'o', fft)
    out += '\t</datafield>\n'
    return out

def ffts_to_xml(ffts):
    """Transform a dictionary: recid -> ffts where ffts is a list of fft dictionary
    into xml.
    """
    out = ''
    for recid, ffts in ffts.iteritems():
        if ffts:
            out += '<record>\n'
            out += '\t<controlfield tag="001">%i</controlfield>\n' % recid
            for fft in ffts:
                out += _xml_fft_creator(fft)
            out += '</record>\n'
    return out

<<<<<<< HEAD:modules/websubmit/lib/bibdocfilecli.py
_actions = [('get-info', 'print all the informations about the record/bibdoc/file structure'),
            #'get-stats',
            ('get-disk-usage', 'print statistics about usage disk usage'),
            ('get-docnames', 'print the document docnames'),
            #'get-docids',
            #'get-recids',
            #'get-doctypes',
            #'get-revisions',
            #'get-last-revisions',
            #'get-formats',
            #'get-comments',
            #'get-descriptions',
            #'get-restrictions',
            #'get-icons',
            ('get-history', 'print the document history'),
            ('delete', 'delete the specified docname'),
            ('undelete', 'undelete the specified docname'),
            #'purge',
            #'expunge',
            ('check-md5', 'check md5 checksum validity of files'),
            ('check-format', 'check if any format-related inconsistences exists'),
            ('check-duplicate-docnames', 'check for duplicate docnames associated with the same record'),
            ('update-md5', 'update md5 checksum of files'),
            ('fix-all', 'fix inconsistences in filesystem vs database vs MARC'),
            ('fix-marc', 'synchronize MARC after filesystem/database'),
            ('fix-format', 'fix format related inconsistences'),
            ('fix-duplicate-docnames', 'fix duplicate docnames associated with the same record')]

_actions_with_parameter = {
    #'set-doctype' : 'doctype',
    #'set-docname' : 'docname',
    #'set-comment' : 'comment',
    #'set-description' : 'description',
    #'set-restriction' : 'restriction',
    'append' : ('append_path', 'specify the URL/path of the file that will appended to the bibdoc'),
    'revise' : ('revise_path', 'specify the URL/path of the file that will revise the bibdoc'),
    'revise_hide_previous' : ('revise_hide_path', 'specify the URL/path of the file that will revise the bibdoc, previous revisions will be hidden'),
    'merge-into' : ('into_docname', 'merge the docname speficied --docname into_docname'),
}

class OptionParserSpecial(OptionParser):
    def format_help(self, *args, **kwargs):
        result = OptionParser.format_help(self, *args, **kwargs)
        if hasattr(self, 'trailing_text'):
            return "%s\n%s\n" % (result, self.trailing_text)
        else:
            return result

def prepare_option_parser():
    """Parse the command line options."""
    parser = OptionParserSpecial(usage="usage: %prog <query> <action> [options]",
    #epilog="""With <query> you select the range of record/docnames/single files to work on. Note that some actions e.g. delete, append, revise etc. works at the docname level, while others like --set-comment, --set-description, at single file level and other can be applied in an iterative way to many records in a single run. Note that specifing docid(2) takes precedence over recid(2) which in turns takes precedence over pattern/collection search.""",
        version=__revision__)
    parser.trailing_text = """
Examples:
    $ bibdocfile --append foo.tar.gz --recid=1
    $ bibdocfile --revise http://foo.com?search=123 --docname='sam'
            --format=pdf --recid=3 --new-docname='pippo'
    """
    parser.trailing_text += wrap_text_in_a_box("""
The bibdocfile command line tool is in a state of high developement. Please
do not rely on the command line parameters to remain compatible for the next
release. You should in particular be aware that if you need to build scripts
on top of the bibdocfile command line interfaces, you will probably need to
revise them with the next release of CDS Invenio.""", 'WARNING')
    query_options = OptionGroup(parser, 'Query parameters')
    query_options.add_option('-a', '--all', action='store_true', dest='all', help='Select all the records')
    query_options.add_option('--show-deleted', action='store_true', dest='show_deleted', help='Show deleted docname, too')
    query_options.add_option('-p', '--pattern', dest='pattern', help='select by specifying the search pattern')
    query_options.add_option('-c', '--collection', dest='collection', help='select by collection')
    query_options.add_option('-r', '--recid', type='int', dest='recid', help='select the recid (or the first recid in a range)')
    query_options.add_option('--recid2', type='int', dest='recid2', help='select the end of the range')
    query_options.add_option('-d', '--docid', type='int', dest='docid', help='select by docid (or the first docid in a range)')
    query_options.add_option('--docid2', type='int', dest='docid2', help='select the end of the range')
    query_options.add_option('--docname', dest='docname', help='specify the docname to work on')
    query_options.add_option('--new-docname', dest='newdocname', help='specify the desired new docname for revising')
    query_options.add_option('--doctype', dest='doctype', help='specify the new doctype')
    query_options.add_option('--format', dest='format', help='specify the format')
    query_options.add_option('--icon', dest='icon', help='specify the URL/path for an icon')
    query_options.add_option('--description', dest='description', help='specify a description')
    query_options.add_option('--comment', dest='comment', help='specify a comment')
    query_options.add_option('--restriction', dest='restriction', help='specify a restriction tag')

    parser.add_option_group(query_options)
    action_options = OptionGroup(parser, 'Actions')
    for (action, help) in _actions:
        action_options.add_option('--%s' % action, action='store_const', const=action, dest='action', help=help)
    parser.add_option_group(action_options)
    action_with_parameters = OptionGroup(parser, 'Actions with parameter')
    for action, (dest, help) in _actions_with_parameter.iteritems():
        action_with_parameters.add_option('--%s' % action, dest=dest, help=help)
    parser.add_option_group(action_with_parameters)
    parser.add_option('-v', '--verbose', type='int', dest='verbose', default=1)
    parser.add_option('--yes-i-know', action='store_true', dest='yes-i-know')
    return parser

def get_recids_from_query(pattern, collection, recid, recid2, docid, docid2):
    """Return the proper set of recids corresponding to the given
    parameters."""
    if docid:
        ret = intbitset()
        if not docid2:
            docid2 = docid
        for adocid in xrange(docid, docid2 + 1):
            try:
                bibdoc = BibDoc(adocid)
                if bibdoc and bibdoc.get_recid():
                    ret.add(bibdoc.get_recid())
            except (InvenioWebSubmitFileError, TypeError):
                pass
        return ret
    elif recid:
        if not recid2:
            recid2 = recid
        recid_range = intbitset(xrange(recid, recid2 + 1))
        recid_set = intbitset(run_sql('select id from bibrec'))
        recid_set &= recid_range
        return recid_set
    elif pattern or collection:
        return intbitset(perform_request_search(cc=collection, p=pattern))
    else:
        return intbitset(run_sql('select id from bibrec'))

def get_docids_from_query(recid_set, docid, docid2, show_deleted=False):
    """Given a set of recid and an optional range of docids
    return a corresponding docids set. The range of docids
    takes precedence over the recid_set."""
    if docid:
        ret = intbitset()
        if not docid2:
            docid2 = docid
        for adocid in xrange(docid, docid2 + 1):
            try:
                bibdoc = BibDoc(adocid)
                if bibdoc:
                    ret.add(adocid)
            except (InvenioWebSubmitFileError, TypeError):
                pass
        return ret
    else:
        ret = intbitset()
        for recid in recid_set:
            bibrec = BibRecDocs(recid, deleted_too=show_deleted)
            for bibdoc in bibrec.list_bibdocs():
                ret.add(bibdoc.get_id())
                icon = bibdoc.get_icon()
                if icon:
                    ret.add(icon.get_id())
        return ret

def print_info(recid, docid, info):
=======
def print_doc_info(recid, docid, info):
>>>>>>> New experimental BibDocFile Command Line Interface implementation.:modules/websubmit/lib/bibdocfilecli.py
    """Nicely print info about a recid, docid pair."""
    print '%i:%i:%s' % (recid, docid, info)

def print_file_info(recid, docid, revision, format, info):
    """Nicely print info about a recid, docid, revision, format."""
    print '%i:%i:%i:%s:%s' % (recid, docid, revision, format, info)

def bibupload_ffts(ffts, append=False):
    """Given an ffts dictionary it creates the xml and submit it."""
    xml = ffts_to_xml(ffts)
    print xml
    tmp_file = os.path.join(CFG_TMPDIR, "bibdocfile_%s" % time.strftime("%Y-%m-%d_%H:%M:%S"))
    open(tmp_file, 'w').write(xml)
    if append:
        wait_for_user("This will be appended via BibUpload")
        task = task_low_level_submission('bibupload', 'bibdocfile', '-a', tmp_file)
        print "BibUpload append submitted with id %s" % task
    else:
        wait_for_user("This will be corrected via BibUpload")
        task = task_low_level_submission('bibupload', 'bibdocfile', '-c', tmp_file)
        print "BibUpload correct submitted with id %s" % task
    return True

def ranges2ids(parse_string):
    """Parse a string and return the intbitset of the corresponding ids."""
    ids = intbitset()
    ranges = parse_string.split(",")
    for arange in ranges:
        tmp_ids = arange.split("-")
        if len(tmp_ids)==1:
            ids.add(int(tmp_ids[0]))
        else:
            if int(tmp_ids[0]) > int(tmp_ids[1]): # sanity check
                tmp = tmp_ids[0]
                tmp_ids[0] = tmp_ids[1]
                tmp_ids[1] = tmp
            ids += xrange(int(tmp_ids[0]), int(tmp_ids[1]) + 1)
    return ids

def chunkife_ids(ids):
    """Create a generator useful for iterate over, that break a set of ids
    into sets of at most CFG_IDS_CHUNK_SIZE."""
    ids_iter = iter(ids)
    try:
        chunk = []
        while True:
            if len(chunk) < CFG_IDS_CHUNK_SIZE:
                chunk.append(ids_iter.next())
            else:
                yield intbitset(chunk)
                chunk = []
    except StopIteration:
        if chunk:
            yield intbitset(chunk)
        raise StopIteration


def cli2recid(options):
    """Given the command line options return a recid."""
    recids = list(cli_recids_iterator(options))
    if len(recids) == 1:
        return recids[0]
    else:
        raise OptionValueError('Your query should match one and only one record. Instead it matches %s records: %s' % (len(recids), recids))

def cli2docid(options):
    """Given the command line options return a docname."""
    docids = list(cli_docids_iterator(options))
    if len(docids) == 1:
        return docids[0]
    else:
        raise OptionValueError('Your query should match one and only one document. Instead it matches %s documents: %s' % (len(docids), docids))

def cli2docname(options, recid=None, docid=None):
    """Given the command line options and optional precalculated recid and docid
    returns the corresponding docname."""
    if recid is None:
        recid = cli2recid(options)
    if docid is None:
        docid = cli2docid(options)
    docname = options.get('docname')
    if docname is None:
        try:
            bibdoc = BibDoc(docid=docid)
            docname = bibdoc.get_docname()
        except InvenioWebSubmitFileError, e:
            raise OptionValueError("It's impossible to retrieve the docname for docid %s: %s" % (docid, e))
    return docname

def cli2url(options):
    """Given the command line options returns the corresponding format."""
    try:
        url = options.get('append_path') or options.get('revise_path')
        if url is None:
            return url
        url = clean_url(url)
        check_valid_url(url)
    except StandardError, e:
        raise OptionValueError("ERROR: Not a valid url/file (%s) has been specified: %s" % (url, e))

def cli2format(options, url=None):
    """Given the command line options returns the corresponding format."""
    format = options.get('format')
    if format is None:
        if url is None:
            try:
                url = options.get('append_path') or options.get('revise_path')
                url = clean_url(url)
                check_valid_url(url)
            except StandardError, e:
                raise OptionValueError("ERROR: Not a valid url/file (%s) has been specified: %s" % (url, e))
        format = get_format_from_url(url)
        if not format:
            raise OptionValueError("ERROR: Not enough information to decide a format!")
        else:
            return format
    else:
        return normalize_format(format)

def cli2restriction(options):
    """Given the command line options returns the corresponding restriction."""
    restriction = options.get('restriction')
    if restriction is None:
        restriction = KEEP_OLD_VALUE
    return restriction

def cli2comment(options):
    """Given the command line options returns the corresponding comment."""
    comment = options.get('comment')
    if comment is None:
        comment = KEEP_OLD_VALUE
    return comment

def cli2description(options):
    """Given the command line options returns the corresponding description."""
    description = options.get('description')
    if description is None:
        description = KEEP_OLD_VALUE
    return description

def cli2icon(options):
    """Given the command line options returns the corresponding icon."""
    icon = options.get('icon')
    if icon is None:
        icon = KEEP_OLD_VALUE
    else:
        try:
            icon = clean_url(icon)
            check_valid_url(icon)
        except StandardError, e:
            raise OptionValueError("ERROR: Not a valid icon (%s) has been specified: %s" % (icon, e))
    return icon

def cli2new_docname(options, recid=None, docid=None, docname=None):
    """Given the command line options returns the corresponding new_docname."""
    new_docname = options.get('new_docname')
    if new_docname is not None:
        if docname is None:
            if recid is None:
                recid = cli2recid(options)
            docname = cli2docname(options, recid, docid)
            if new_docname == docname:
                new_docname = None
            else:
                bibrecdocs = BibRecDocs(recid)
                if new_docname in bibrecdocs.get_bibdoc_names():
                    raise OptionValueError("ERROR: docname '%s' already exists for record %s" % (new_docname, recid))
    return new_docname

def cli2doctype(options):
    """Given the command line options returns the corresponding doctype."""
    doctype = options.get(doctype)
    if doctype is None:
        doctype = 'Main'
    return doctype

_shift_re = re.compile("([-\+]{0,1})([\d]+)([dhms])")
def _parse_datetime(var):
    """Returns a date string according to the format string.
       It can handle normal date strings and shifts with respect
       to now."""
    if not var:
        return None
    date = time.time()
    factors = {"d":24*3600, "h":3600, "m":60, "s":1}
    m = _shift_re.match(var)
    if m:
        sign = m.groups()[0] == "-" and -1 or 1
        factor = factors[m.groups()[2]]
        value = float(m.groups()[1])
        return datetime.datetime.fromtimestamp(date + sign * factor * value)
    else:
        return datetime.datetime.strptime(var, "%Y-%m-%d %H:%M:%S")

def _parse_date_range(var):
    """Returns the two dates contained as a low,high tuple"""
    limits = var.split(",")
    if len(limits)==1:
        low = _parse_datetime(limits[0])
        return low, None
    if len(limits)==2:
        low = _parse_datetime(limits[0])
        high = _parse_datetime(limits[1])
        return low, high
    return None, None

def _quick_match_all_recids(options):
    """Return an quickly an approximate but (by excess) list of good recids."""
    collection = getattr(options, 'collection', None)
    pattern = getattr(options, 'pattern', None)
    recids = getattr(options, 'recids', None)
    deleted_recs = getattr(options, 'deleted_recs', None)
    deleted_docs = getattr(options, 'deleted_docs', None)
    md_rec = getattr(options, 'md_rec', (None, None))
    cd_rec = getattr(options, 'cd_rec', (None, None))
    print options
    tmp_date_query = []
    tmp_date_params = []
    if recids is None:
        recids = intbitset(run_sql('SELECT id FROM bibrec'))
        if not recids:
            warning('No record in the database')
    if md_rec[0] is not None:
        tmp_date_query.append('modification_date>=%s')
        tmp_date_params.append(md_rec[0])
    if md_rec[1] is not None:
        tmp_date_query.append('modification_date<=%s')
        tmp_date_params.append(md_rec[1])
    if cd_rec[0] is not None:
        tmp_date_query.append('creation_date>=%s')
        tmp_date_params.append(cd_rec[0])
    if cd_rec[1] is not None:
        tmp_date_query.append('creation_date<=%s')
        tmp_date_params.append(cd_rec[1])
    if tmp_date_query:
        tmp_date_query = ' AND '.join(tmp_date_query)
        tmp_date_params = tuple(tmp_date_params)
        print("run_sql('SELECT id FROM bibrec WHERE %s', %s)" % (tmp_date_query, repr(tmp_date_params)))
        recids &= intbitset(run_sql('SELECT id FROM bibrec WHERE %s' % tmp_date_query, tmp_date_params))
        if not recids:
            warning('Time constraints for records are too strict')
    if collection or pattern:
        recids &= intbitset(perform_request_search(cc=collection, p=pattern))
    return recids

def _quick_match_all_docids(options):
    """Return an quickly an approximate but (by excess) list of good docids."""
    deleted_docs = getattr(options, 'deleted_docs', None)
    empty_docs = getattr(options, 'empty_docs', None)
    action_undelete = getattr(options, 'action', None) == 'undelete'
    docids = getattr(options, 'docids', None)
    md_doc = getattr(options, 'md_doc', (None, None))
    cd_doc = getattr(options, 'cd_doc', (None, None))
    if docids is None:
        docids = intbitset(run_sql('SELECT id FROM bibdoc'))
    tmp_query = []
    tmp_params = []
    if deleted_docs is None and action_undelete:
        deleted_docs = 'only'
    if deleted_docs == 'no':
        tmp_query.append('status<>"DELETED"')
    elif deleted_docs == 'only':
        tmp_query.append('status="DELETED"')
    if md_doc[0] is not None:
        tmp_query.append('modification_date>=%s')
        tmp_params.append(md_doc[0])
    if md_doc[1] is not None:
        tmp_query.append('modification_date<=%s')
        tmp_params.append(md_doc[1])
    if cd_doc[0] is not None:
        tmp_query.append('creation_date>=%s')
        tmp_params.append(cd_doc[0])
    if cd_doc[1] is not None:
        tmp_query.append('creation_date<=%s')
        tmp_params.append(cd_doc[1])
    if tmp_query:
        tmp_query = tuple(' AND '.join(tmp_query))
        tmp_params = tuple(tmp_params)
        docids &= intbitset(run_sql('SELECT id FROM bibdoc WHERE %s' % tmp_query, tmp_params))
    return docids

def _slow_match_single_recid(options, recid, recids=None, docids=None):
    """Apply all the given queries in order to assert wethever a recid
    match or not."""
    deleted_docs = getattr(options, 'deleted_docs', None)
    deleted_recs = getattr(options, 'deleted_recs', None)
    empty_recs = getattr(options, 'empty_recs', None)
    docname = getattr(options, 'docname', None)
    if docids is None:
        docids = _quick_match_all_docids(options)
    bibrecdocs = BibRecDocs(recid, deleted_too=(deleted_docs != 'no'))
    if bibrecdocs.deleted_p() and (deleted_recs == 'no'):
        return False
    elif not bibrecdocs.deleted_p() and (deleted_recs != 'only'):
        if docids is not None:
            ok = False
            for bibdoc in bibrecdocs.list_bibdocs():
                if bibdoc.id in docids and _slow_match_single_docid(options, bibdoc.id, recids, docids):
                    ok = True
                    break
            if not ok:
                return False
        if docname is not None:
            if not bibrecdocs.has_docname_p(docname):
                return False
        if bibrecdocs.empty_p() and (empty_recs != 'no'):
            return True
        elif not bibrecdocs.empty_p() and (empty_recs != 'only'):
            return True
    return False

def _slow_match_single_docid(options, docid, recids=None, docids=None):
    """Apply all the given queries in order to assert wethever a recid
    match or not."""
    empty_docs = getattr(options, 'empty_docs', None)
    if recids is None:
        recids = _quick_match_all_recids(options)
    bibdoc = BibDoc(docid)
    if bibdoc.get_recid() not in recids:
        return False
    elif empty_docs == 'no' and bibdoc.empty_p():
        return False
    elif empty_docs == 'only' and not bibdoc.empty_p():
        return False
    else:
        return True

def cli_recids_iterator(options):
    """Slow iterator over all the matched recids."""
    recids = _quick_match_all_recids(options)
    docids = _quick_match_all_docids(options)
    for recid in recids:
        if _slow_match_single_recid(options, recid, recids, docids):
            yield recid
    raise StopIteration

def cli_docids_iterator(options):
    """Slow iterator over all the matched docids."""
    recids = _quick_match_all_recids(options)
    docids = _quick_match_all_docids(options)
    for docid in docids:
        if _slow_match_single_docid(options, docid, recids, docids):
            yield docid
    raise StopIteration

def cli_get_checksum(docids):
    """Print all the checksums for the given sequence of docids"""
    for docid in docids:
        bibdoc = BibDoc(docid)
        for afile in bibdoc.list_all_files():
            print_file_info(afile.get_recid(), afile.get_bibdocid(), afile.get_version(), afile.get_format(), afile.get_checksum())

def cli_get_info(recids):
    """Print all the checksums for the given sequence of recids."""
    for recid in recids:
        print str(BibRecDocs(recid))[:-1] ## Removing the final newline

def cli_append(url, docid=None, recid=None, docname=None, new_docname=None, format=None, icon=None, doctype=None, description=None, comment=None, restriction=None):
    try:
        url = clean_url(url)
        check_valid_url(url)
    except StandardError, e:
        raise OptionValueError("ERROR: Not a valid url/file (%s) has been specified: %s" % (url, e))
        return False

    if docid is not None:
        bibdoc = BibDoc(docid)
        if recid is not None and recid != bibdoc.get_recid():
            raise OptionValueError("ERROR: Provided recid %i is not linked with provided docid %i" % (recid, docid))
        if docname is not None and docname != bibdoc.get_docname():
            raise OptionValueError("ERROR: Provided docid %i is not named as the provided docname %s" % (docid, docname))
        recid = bibdoc.get_recid()
        docname = bibdoc.get_docname()
    elif recid is None:
        raise OptionValueError("ERROR: Not enough information to identify the record and desired document")
    if docname is None:
        docname = get_docname_from_url(url)
    if not docname:
        raise OptionValueError("ERROR: Not enough information to decide a docname!")
    else:
        try:
            bibdoc = BibDoc(recid=recid, docname=docname)
        except InvenioWebSubmitFileError, e:
            raise OptionValueError("ERROR: Unexpected error in retrieving docname '%s' for recid '%s': %s" % (docname, recid, e))
    if format is None:
        format = get_format_from_url(url)
    if not format:
        raise OptionValueError("ERROR: Not enough information to decide a format!")
    elif bibdoc.format_already_exists_p(format):
        raise OptionValueError("ERROR: the format '%s' already exists for docname '%s' and record '%s'" % (format, docname, recid))
    if icon is not None and icon != KEEP_OLD_VALUE:
        try:
            icon = clean_url(icon)
            check_valid_url(url)
        except StandardError, e:
            raise OptionValueError("ERROR: Not a valid url has been specified for the icon: %s" % e)
    else:
        icon = KEEP_OLD_VALUE
    if doctype is None:
        doctype = 'Main'
    if comment is None:
        comment = KEEP_OLD_VALUE
    if description is None:
        description = KEEP_OLD_VALUE
    if restriction is None:
        restriction = KEEP_OLD_VALUE

    fft = {
        'url' : url,
        'docname' : docname,
        'new_docname' : new_docname,
        'format' :format,
        'icon' : icon,
        'comment' : comment,
        'description' : description,
        'restriction' : restriction,
        'doctype' : doctype
    }
    ffts = {recid : [fft]}
    return bibupload_ffts(ffts, append=True)

<<<<<<< HEAD:modules/websubmit/lib/bibdocfilecli.py
def cli_revise(recid=None, docid=None, docname=None, new_docname=None, doctype=None, url=None, format=None, icon=None, description=None, comment=None, restriction=None, hide_previous=False):
    """Create a bibupload FFT task submission for appending a format."""
=======
def cli_revise(url, docid=None, recid=None, docname=None, new_docname=None, format=None, icon=None, doctype=None, description=None, comment=None, restriction=None):
    try:
        url = clean_url(url)
        check_valid_url(url)
    except StandardError, e:
        raise OptionValueError("ERROR: Not a valid url/file (%s) has been specified: %s" % (url, e))
        return False

>>>>>>> New experimental BibDocFile Command Line Interface implementation.:modules/websubmit/lib/bibdocfilecli.py
    if docid is not None:
        bibdoc = BibDoc(docid)
        if recid is not None and recid != bibdoc.get_recid():
            raise OptionValueError("ERROR: Provided recid %i is not linked with provided docid %i" % (recid, docid))
        if docname is not None and docname != bibdoc.get_docname():
            raise OptionValueError("ERROR: Provided docid %i is not named as the provided docname %s" % (docid, docname))
        recid = bibdoc.get_recid()
        docname = bibdoc.get_docname()
    elif recid is None:
        raise OptionValueError("ERROR: Not enough information to identify the record and desired document")
    if docname is None:
        docname = get_docname_from_url(url)
    if not docname:
        raise OptionValueError("ERROR: Not enough information to decide a docname!")
    else:
        try:
            bibdoc = BibDoc(recid=recid, docname=docname)
        except InvenioWebSubmitFileError, e:
            raise OptionValueError("ERROR: Unexpected error in retrieving docname '%s' for recid '%s': %s" % (docname, recid, e))
    if format is None:
        format = get_format_from_url(url)
    if not format:
        raise OptionValueError("ERROR: Not enough information to decide a format!")
    if icon is not None and icon != KEEP_OLD_VALUE:
        try:
            icon = clean_url(icon)
            check_valid_url(url)
        except StandardError, e:
            raise OptionValueError("ERROR: Not a valid url has been specified for the icon: %s" % e)
    else:
        icon = KEEP_OLD_VALUE
    if doctype is None:
        doctype = 'Main'
    if comment is None:
        comment = KEEP_OLD_VALUE
    if description is None:
        description = KEEP_OLD_VALUE
    if restriction is None:
        restriction = KEEP_OLD_VALUE

    fft = {
        'url' : url,
        'docname' : docname,
        'new_docname' : new_docname,
        'format' :format,
        'icon' : icon,
        'comment' : comment,
        'description' : description,
        'restriction' : restriction,
        'doctype' : doctype
    }
    if hide_previous:
        fft['options'] = 'HIDE_PREVIOUS'
    ffts = {recid : [fft]}
    return bibupload_ffts(ffts, append=False)

class OptionParserSpecial(OptionParser):
    def format_help(self, *args, **kwargs):
        result = OptionParser.format_help(self, *args, **kwargs)
        if hasattr(self, 'trailing_text'):
            return "%s\n%s\n" % (result, self.trailing_text)
        else:
            return result

<<<<<<< HEAD:modules/websubmit/lib/bibdocfilecli.py
def cli_check_format(recid_set):
    """Check if any format-related inconsistences exists."""
    count = 0
    duplicate = False
    for recid in recid_set:
        bibrecdocs = BibRecDocs(recid)
        if not bibrecdocs.check_duplicate_docnames():
            print >> sys.stderr, "recid %s has duplicate docnames!"
            broken = True
            duplicate = True
        else:
            broken = False
        for docname in bibrecdocs.get_bibdoc_names():
            if not bibrecdocs.check_format(docname):
                print >> sys.stderr, "recid %s with docname %s need format fixing" % (recid, docname)
                broken = True
        if broken:
            count += 1
    if count:
        result = "%d out of %d records need their formats to be fixed." % (count, len(recid_set))
    else:
        result = "All records appear to be correct with respect to formats."
    if duplicate:
        result += " Note however that at least one record appear to have duplicate docnames. You should better fix this situation by using --fix-duplicate-docnames."
    print wrap_text_in_a_box(result, style="conclusion")
    return not(duplicate or count)

def cli_check_duplicate_docnames(recid_set):
    """Check if some record is connected with bibdoc having the same docnames."""
    count = 0
    for recid in recid_set:
        bibrecdocs = BibRecDocs(recid)
        if bibrecdocs.check_duplicate_docnames():
            count += 1
            print sys.stderr, "recid %s has duplicate docnames!"
    if count:
        result = "%d out of %d records have duplicate docnames." % (count, len(recid_set))
        return False
    else:
        result = "All records appear to be correct with respect to duplicate docnames."
        return True

def cli_fix_format(recid_set):
    """Fix format-related inconsistences."""
    fixed = intbitset()
    for recid in recid_set:
        bibrecdocs = BibRecDocs(recid)
        for docname in bibrecdocs.get_bibdoc_names():
            if not bibrecdocs.check_format(docname):
                if bibrecdocs.fix_format(docname, skip_check=True):
                    print >> sys.stderr, "%i has been fixed for docname %s" % (recid, docname)
                else:
                    print >> sys.stderr, "%i has been fixed for docname %s. However note that a new bibdoc might have been created." % (recid, docname)
                fixed.add(recid)
    if fixed:
        print "Now we need to synchronize MARC to reflect current changes."
        cli_fix_marc(fixed)
    print wrap_text_in_a_box("%i out of %i record needed to be fixed." % (len(recid_set), len(fixed)), style="conclusion")
    return not fixed

def cli_fix_duplicate_docnames(recid_set):
    """Fix duplicate docnames."""
    fixed = intbitset()
    for recid in recid_set:
        bibrecdocs = BibRecDocs(recid)
        if not bibrecdocs.check_duplicate_docnames():
            bibrecdocs.fix_duplicate_docnames(skip_check=True)
            print >> sys.stderr, "%i has been fixed for duplicate docnames." % recid
            fixed.add(recid)
    if fixed:
        print "Now we need to synchronize MARC to reflect current changes."
        cli_fix_marc(fixed)
    print wrap_text_in_a_box("%i out of %i record needed to be fixed." % (len(recid_set), len(fixed)), style="conclusion")
    return not fixed

def cli_delete(recid, docname):
    """Delete the given docname of the given recid."""
    if docname in BibRecDocs(recid).get_bibdoc_names():
        ffts = {}
        ffts[recid] = [{'docname' : docname, 'doctype' : 'DELETE'}]
        return bibupload_ffts(ffts, append=False)
    else:
        print >> sys.stderr, '%s is not a valid docname for recid %s' % (docname, recid)

def cli_undelete(recid, docname, status):
    """Delete the given docname of the given recid."""
    bibrecdocs = BibRecDocs(recid, deleted_too=True)
    bibdoc = bibrecdocs.get_bibdoc(docname)
    bibdoc.undelete(status)
    cli_fix_marc(intbitset((recid,)))
    print wrap_text_in_a_box("docname %s of recid %i successfuly undeleted with status '%s'" % (docname, recid, status), style="conclusion")

def cli_merge_into(recid, docname, into_docname):
    """Merge docname into_docname for the given recid."""
    bibrecdocs = BibRecDocs(recid)
    docnames = bibrecdocs.get_bibdoc_names()
    if docname in docnames and into_docname in docnames:
        try:
            bibrecdocs.merge_bibdocs(into_docname, docname)
        except InvenioWebSubmitFileError, e:
            print >> sys.stderr, e
        else:
            cli_fix_marc(intbitset((recid)))
    else:
        print >> sys.stderr, 'Either %s or %s is not a valid docname for recid %s' % (docname, into_docname, recid)

def cli_get_info(recid_set, show_deleted=False):
    """Print all the info of a recid_set."""
    for recid in recid_set:
        print BibRecDocs(recid, deleted_too=show_deleted)
=======
def prepare_option_parser():
    """Return BibDocFile CLI parser."""

    def _ids_ranges_callback(option, opt, value, parser):
        """Callback for optparse to parse a set of ids ranges in the form
        nnn1-nnn2,mmm1-mmm2... returning the corresponding intbitset.
        """
        try:
            value = ranges2ids(value)
            setattr(parser.values, option.dest, value)
        except Exception, e:
            raise OptionValueError("It's impossible to parse the range '%s' for option %s: %s" % (value, opt, e))

    def _date_range_callback(option, opt, value, parser):
        """Callback for optparse to parse a range of dates in the form
        [date1],[date2]. Both date1 and date2 could be optional.
        the date can be expressed absolutely ("%Y-%m-%d %H:%M:%S")
        or relatively (([-\+]{0,1})([\d]+)([dhms])) to the current time."""
        try:
            value = _parse_date_range(value)
            setattr(parser.values, option.dest, value)
        except Exception, e:
            raise OptionValueError("It's impossible to parse the range '%s' for option %s: %s" % (value, opt, e))
>>>>>>> New experimental BibDocFile Command Line Interface implementation.:modules/websubmit/lib/bibdocfilecli.py


    usage = "usage: %prog [options] query action"
    parser = OptionParserSpecial(usage, version=__revision__)
    parser.trailing_text = """
Examples:
    $ bibdocfile --append foo.tar.gz --recid=1
    $ bibdocfile --revise http://foo.com?search=123 --with-docname='sam'
            --set-format=pdf --recid=3 --set-docname='pippo'
    """

    parser.add_option("-v", "--verbose", type="int", dest="verbose", default=1)
    parser.add_option("-q", "--quiet", action="store_const", dest="verbose", const=0, help="Same as --verbose 0")
    parser.add_option("--yes-i-know", action="store_false", dest="interactive", default=True, help="Non interactive")
    parser.add_option("--dry-run", action="store_true", dest="dry_run", default=False, help="Don't perform any modification")
    query = OptionGroup(parser, 'Query options')
    query.add_option("-c", "--with-collection", dest="collection", help="To query by collection")
    query.add_option("-p", "--with-pattern", dest="pattern", help="To query by pattern")
    query.add_option("-r", "--with-recids", action="callback", callback=_ids_ranges_callback, dest="recids", type="string", help="To query by recid(s) (ranges). Default is all recids")
    query.add_option("-d", "--with-docids", action="callback", callback=_ids_ranges_callback, dest="docids", type="string", help="To query by docid(s) (ranges)")
    query.add_option("--with-deleted-recs", choices=['yes', 'no', 'only'], type="choice", dest="deleted_recs", help="'Yes' to consider also deleted records in operations, 'no' to exclude them, 'only' to consider only them", metavar="yes/no/only")
    query.add_option("--with-deleted-docs", choices=['yes', 'no', 'only'], type="choice", dest="deleted_docs", help="'Yes' to consider also deleted documents in operations, 'no' to exclude them, 'only' to consider only them (e.g. for undeletion)", metavar="yes/no/only")
    query.add_option("--with-empty-recs", choices=['yes', 'no', 'only'], type="choice", dest="empty_recs",help="'Yes' to consider also records without document in operations, 'no' to exclude them, 'only' to consider only them (e.g. for statistics)", metavar="yes/no/only")
    query.add_option("--with-empty-docs", choices=['yes', 'no', 'only'], type="choice", dest="empty_docs", help="'Yes' to consider also documents without file connected in operations, 'no' to exclude them, 'only' to consider only them (e.g. for sanity checking)", metavar="yes/no/only")
    query.add_option("--with-record-modification-date", action="callback", callback=_date_range_callback, dest="md_rec", nargs=1, type="string", default=(None, None), help="To query for records modified between date1 and date2. Dates can be expressed relatively to now", metavar="date1,date2")
    query.add_option("--with-record-creation-date", action="callback", callback=_date_range_callback, dest="cd_rec", nargs=1, type="string", default=(None, None), help="To query for records created between date1 and date2. Dates can be expressed relatively to now", metavar="date1,date2")
    query.add_option("--with-document-modification-date", action="callback", callback=_date_range_callback, dest="md_doc", nargs=1, type="string", default=(None, None), help="To query for documents modified between date1 and date2. Dates can be expressed relatively to now", metavar="date1,date2")
    query.add_option("--with-document-creation-date", action="callback", callback=_date_range_callback, dest="cd_doc", nargs=1, type="string", default=(None, None), help="To query for documents created between date1 and date2. Dates can be expressed relatively to now", metavar="date1,date2")
    query.add_option("--with-url", dest="url", help='to retrieve recid/docid from a document url, e.g. %s/record/1/files/foobar.pdf' % CFG_SITE_URL)
    query.add_option("--with-path", dest="path", help='to retrieve recid/docid from a filesystem path, e.g. %s/g0/1/foobar.pdf;1' % CFG_WEBSUBMIT_FILEDIR)
    query.add_option("--with-docname", dest="docname", help='to specify a docname when appending/revising a document')
    query.add_option("--with-format", dest="format", help='to specify a format when appending/revising a document, e.g. ".pdf"')
    query.add_option("--with-revision", dest="revision", help='to sepcifiy a revision when querying for some info')
    query.add_option("--with-description", dest="description", help='to query by description')
    query.add_option("--with-comment", dest="comment", help='to query by comment')
    query.add_option("--with-doctype", dest="doctype", help='to query by doctype')
    parser.add_option_group(query)

    action = OptionGroup(parser, 'Core actions')
    action.add_option("-A", "--append", dest="append_path", help='Append a document. The query should correspond to exactly one record. Please specify through --set- options additional details.')
    action.add_option("-R", "--revise", dest="revise_path", help='Revise a document. The query should correspond to exactly one record. Please specify through --set- options additional details.')
    action.add_option("-T", "--revert", type="int", dest="revert_revision")
    action.add_option("-H", "--hard-delete", action="store_const", dest="action", const="hard_delete")
    action.add_option("-D", "--delete", action="store_const", dest="action", const="delete")
    action.add_option("-U", "--undelete", action="store_const", dest="action", const="undelete")
    action.add_option("-P", "--purge", action="store_const", dest="action", const="purge")
    action.add_option("-E", "--expunge", action="store_const", dest="action", const="expunge")
    action.add_option("-I", "--info", action="store_const", dest="action", const="info")
    parser.add_option_group(action)

    setter = OptionGroup(parser, 'Setting actions')
    setter.add_option("--set-icon", dest="set_icon_url")
    setter.add_option("--set-comment", dest="set_comment")
    setter.add_option("--set-description", dest="set_description")
    setter.add_option("--set-docname", dest="set_docname")
    setter.add_option("--set-format", dest="set_format")
    setter.add_option("--set-doctype", dest="set_doctype")
    setter.add_option("--set-restriction", dest="set_restriction")
    setter.add_option("--unset-icon", action="store_const", const='', dest="set_icon_url")
    setter.add_option("--unset-comment", action="store_const", const='', dest="set_comment")
    setter.add_option("--unset-description", action="store_const", const='', dest="set_description")
    setter.add_option("--unset-restriction", action="store_const", const='', dest="set_restriction")
    parser.add_option_group(setter)

    getter = OptionGroup(parser, 'Actions to obtain information')
    getter.add_option("--get-icon", action="store_const", dest="action", const="get_icon")
    getter.add_option("--get-description", action="store_const", dest="action", const="get_description")
    getter.add_option("--get-comment", action="store_const", dest="action", const="get_comment")
    getter.add_option("--get-restriction", action="store_const", dest="action", const="get_restriction")
    getter.add_option("--get-doctype", action="store_const", dest="action", const="get_doctype")
    getter.add_option("--get-format", action="store_const", dest="action", const="get_format")
    getter.add_option("--get-revision", action="store_const", dest="action", const="get_revision")
    getter.add_option("--get-disk-usage", action="store_const", dest="action", const="get_disk_usage")
    getter.add_option("--get-history", action="store_const", dest="action", const="get_history")
    getter.add_option("--get-stats", action="store_const", dest="action", const="get_stats")
    getter.add_option("--get-docname", action="store_const", dest="action", const="get_docname")
    getter.add_option("--get-docid", action="store_const", dest="action", const="get_docid")
    getter.add_option("--get-recid", action="store_const", dest="action", const="get_recid")
    getter.add_option("--get-checksum", action="store_const", dest="action", const="get_checksum")
    parser.add_option_group(getter)

    maintenance = OptionGroup(parser, 'Maintenance actions')
    maintenance.add_option("--check-md5s", action="store_const", dest="action", const="check_md5s")
    maintenance.add_option("--check-8564s", action="store_const", dest="action", const="check_8564s")
    maintenance.add_option("--check-filesystem", action="store_const", dest="action", const="check_filesystem")
    maintenance.add_option("--check-tables", action="store_const", dest="action", const="check_tables")
    maintenance.add_option("--check-all", action="store_const", dest="action", const="check_all")
    maintenance.add_option("--update-md5s-from-filesystem", action="store_const", dest="action", const="update_md5s_from_filesystem")
    maintenance.add_option("--update-8564s-from-tables", action="store_const", dest="action", const="update_8564s_from_tables")
    maintenance.add_option("--update-tables-from-filesystem", action="store_const", dest="action", const="update_tables_from_filesystem")
    maintenance.add_option("--update-tables-from-8564s", action="store_const", dest="action", const="update_tables_from_8564s")
    parser.add_option_group(maintenance)

<<<<<<< HEAD:modules/websubmit/lib/bibdocfilecli.py
def cli_assert_recid(options):
    """Check for recid to be correctly set."""
    try:
        assert(int(options.recid) > 0)
        return True
    except:
        print >> sys.stderr, 'recid not correctly set: "%s"' % options.recid
        return False

def cli_assert_docname(options):
    """Check for recid to be correctly set."""
    try:
        assert(options.docname)
        return True
    except:
        print >> sys.stderr, 'docname not correctly set: "%s"' % options.docname
        return False

def get_all_recids():
    """Return all the existing recids."""
    return intbitset(run_sql('select id from bibrec'))
=======
    return parser
>>>>>>> New experimental BibDocFile Command Line Interface implementation.:modules/websubmit/lib/bibdocfilecli.py

def main():
    parser = prepare_option_parser()
    (options, args) = parser.parse_args()
<<<<<<< HEAD:modules/websubmit/lib/bibdocfilecli.py
    if options.all:
        recid_set = get_all_recids()
    else:
        recid_set = get_recids_from_query(options.pattern, options.collection, options.recid, options.recid2, options.docid, options.docid2)
    docid_set = get_docids_from_query(recid_set, options.docid, options.docid2, options.show_deleted == True)
    try:
        if options.action == 'get-history':
            cli_get_history(docid_set)
        elif options.action == 'get-info':
            cli_get_info(recid_set, options.show_deleted == True)
        elif options.action == 'get-docnames':
            cli_get_docnames(docid_set)
        elif options.action == 'get-disk-usage':
            cli_get_disk_usage(docid_set)
        elif options.action == 'check-md5':
            cli_check_md5(docid_set)
        elif options.action == 'update-md5':
            cli_update_md5(docid_set)
        elif options.action == 'fix-all':
            cli_fix_all(recid_set)
        elif options.action == 'fix-marc':
            cli_fix_marc(recid_set)
        elif options.action == 'delete':
            cli_delete(options.recid, options.docname)
        elif options.action == 'fix-duplicate-docnames':
            cli_fix_duplicate_docnames(recid_set)
        elif options.action == 'fix-format':
            cli_fix_format(recid_set)
        elif options.action == 'check-duplicate-docnames':
            cli_check_duplicate_docnames(recid_set)
        elif options.action == 'check-format':
            cli_check_format(recid_set)
        elif options.action == 'undelete':
            if cli_assert_recid(options) and cli_assert_docname(options):
                cli_undelete(options.recid, options.docname, options.restriction or "")
        elif options.append_path:
            if cli_assert_recid(options):
                res = cli_append(options.recid, options.docid, options.docname, options.doctype, options.append_path, options.format, options.icon, options.description, options.comment, options.restriction)
                if not res:
                    sys.exit(1)
        elif options.revise_path:
            if cli_assert_recid(options):
                res = cli_revise(options.recid, options.docid, options.docname,
                options.newdocname, options.doctype, options.revise_path, options.format,
                options.icon, options.description, options.comment, options.restriction)
                if not res:
                    sys.exit(1)
        elif options.revise_hide_path:
            if cli_assert_recid(options):
                res = cli_revise(options.recid, options.docid, options.docname,
                options.newdocname, options.doctype, options.revise_path, options.format,
                options.icon, options.description, options.comment, options.restriction, True)
                if not res:
                    sys.exit(1)
        elif options.into_docname:
            if options.recid and options.docname:
                cli_merge_into(options.recid, options.docname, options.into_docname)
            else:
                print >> sys.stderr, "You have to specify both the recid and a docname for using --merge-into"
        else:
            print >> sys.stderr, "Action %s is not valid" % options.action
            sys.exit(1)
    except InvenioWebSubmitFileError, e:
        print >> sys.stderr, e
        sys.exit(1)
=======
    action = getattr(options, 'action')
    append_path = getattr(options, 'append_path')
    print cli2recid(options)
    #print cli2docid(options)
    #print cli2docname(options)
    #print cli2format(options)
    #print cli2description(options)
    #print cli2comment(options)
    #print cli2restriction(options)
    #print cli2icon(options)
    #print cli2new_docname(options)
    #print cli2doctype(options)
    #print cli2url(options)
    #if action == 'get_checksum':
        #cli_get_checksum(options)
    #elif action == 'info':
        #cli_get_info(options)
    #elif append_path:
        #cli_append()
>>>>>>> New experimental BibDocFile Command Line Interface implementation.:modules/websubmit/lib/bibdocfilecli.py

if __name__=='__main__':
    main()
