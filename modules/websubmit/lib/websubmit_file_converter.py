# -*- coding: utf-8 -*-
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
This module implement fulltext conversion between many different file formats.
"""

import os
import re
import sys
import shutil
import tempfile
import HTMLParser
import time

from logging import debug, error, DEBUG, getLogger
from htmlentitydefs import entitydefs
from optparse import OptionParser

try:
    from invenio.hocrlib import create_pdf, extract_hocr
    CFG_HAS_REPORTLAB = True
except ImportError:
    CFG_HAS_REPORTLAB = False

from invenio.shellutils import run_process_with_timeout
from invenio.config import CFG_TMPDIR, CFG_ETCDIR, CFG_PYLIBDIR, \
    CFG_PATH_ANY2DJVU, \
    CFG_PATH_PDFINFO, \
    CFG_PATH_GS, \
    CFG_PATH_PDFOPT, \
    CFG_PATH_PDFTOPS, \
    CFG_PATH_GZIP, \
    CFG_PATH_GUNZIP, \
    CFG_PATH_PDFTOTEXT, \
    CFG_PATH_PDFTOPPM, \
    CFG_PATH_OCROSCRIPT, \
    CFG_PATH_DJVUPS, \
    CFG_PATH_DJVUTXT, \
    CFG_PATH_OPENOFFICE_PYTHON, \
    CFG_PATH_PSTOTEXT, \
    CFG_PATH_TIFF2PDF, \
    CFG_OPENOFFICE_SERVER_HOST, \
    CFG_OPENOFFICE_SERVER_PORT, \
    CFG_OPENOFFICE_USER, \
    CFG_PATH_CONVERT, \
    CFG_PATH_PAMFILE

from invenio.websubmit_config import \
    CFG_WEBSUBMIT_BEST_FORMATS_TO_EXTRACT_TEXT_FROM, \
    CFG_WEBSUBMIT_DESIRED_CONVERSIONS
from invenio.errorlib import register_exception

#logger = getLogger()
#logger.setLevel(DEBUG)

CFG_TWO2THREE_LANG_CODES = {
    'en': 'eng',
    'nl': 'nld',
    'es': 'spa',
    'de': 'deu',
    'it': 'ita',
    'fr': 'fra',
}

CFG_OPENOFFICE_TMPDIR = os.path.join(CFG_TMPDIR, 'ooffice-tmp-files')

_RE_CLEAN_SPACES = re.compile(r'\s+')


class InvenioWebSubmitFileConverterError(Exception):
    pass


def get_conversion_map():
    """Return a dictionary of the form:
    '.pdf' : {'.ps.gz' : ('pdf2ps', {param1 : value1...})
    """
    ret = {
        '.csv': {},
        '.djvu': {},
        '.doc': {},
        '.docx': {},
        '.htm': {},
        '.html': {},
        '.odp': {},
        '.ods': {},
        '.odt': {},
        '.pdf': {},
        '.ppt': {},
        '.pptx': {},
        '.ps': {},
        '.ps.gz': {},
        '.rtf': {},
        '.tif': {},
        '.tiff': {},
        '.txt': {},
        '.xls': {},
        '.xlsx': {},
        '.xml': {},
        '.hocr': {},
    }
    if CFG_PATH_GZIP:
        ret['.ps']['.ps.gz'] = (gzip, {})
    if CFG_PATH_GUNZIP:
        ret['.ps.gz']['.ps'] = (gunzip, {})
    if CFG_PATH_ANY2DJVU:
        ret['.pdf']['.djvu'] = (any2djvu, {})
        ret['.ps']['.djvu'] = (any2djvu, {})
        ret['.ps.gz']['.djvu'] = (any2djvu, {})
    if CFG_PATH_DJVUPS:
        ret['.djvu']['.ps'] = (djvu2ps, {'compress': False})
        if CFG_PATH_GZIP:
            ret['.djvu']['.ps.gz'] = (djvu2ps, {'compress': True})
    if CFG_PATH_DJVUTXT:
        ret['.djvu']['.txt'] = (djvu2text, {})
    if CFG_PATH_PSTOTEXT:
        ret['.ps']['.txt'] = (pstotext, {})
        if CFG_PATH_GUNZIP:
            ret['.ps.gz']['.txt'] = (pstotext, {})
    if CFG_PATH_GS:
        ret['.ps']['.pdf'] = (ps2pdfa, {})
        if CFG_PATH_GUNZIP:
            ret['.ps.gz']['.pdf'] = (ps2pdfa, {})
    if CFG_PATH_PDFTOPS:
        ret['.pdf']['.ps'] = (pdf2ps, {'compress': False})
        if CFG_PATH_GZIP:
            ret['.pdf']['.ps.gz'] = (pdf2ps, {'compress': True})
    if CFG_PATH_PDFTOTEXT:
        ret['.pdf']['.txt'] = (pdf2text, {})
    if CFG_PATH_PDFTOPPM and CFG_PATH_OCROSCRIPT and CFG_PATH_PAMFILE:
        ret['.pdf']['.hocr'] = (pdf2hocr, {})
    if CFG_PATH_PDFTOPS and CFG_PATH_GS and CFG_PATH_PDFOPT and CFG_PATH_PDFINFO:
        ret['.pdf']['.pdf'] = (pdf2pdfa, {})
    ret['.txt']['.txt'] = (txt2text, {})
    ret['.csv']['.txt'] = (txt2text, {})
    ret['.html']['.txt'] = (html2text, {})
    ret['.htm']['.txt'] = (html2text, {})
    ret['.xml']['.txt'] = (html2text, {})
    if CFG_HAS_REPORTLAB:
        ret['.hocr']['.pdf'] = (hocr2pdf, {})
    if CFG_PATH_TIFF2PDF:
        ret['.tiff']['.pdf'] = (tiff2pdf, {})
        ret['.tif']['.pdf'] = (tiff2pdf, {})
    if CFG_PATH_OPENOFFICE_PYTHON and CFG_OPENOFFICE_SERVER_HOST:
        ret['.rtf']['.odt'] = (unoconv, {'output_format': 'odt'})
        ret['.rtf']['.doc'] = (unoconv, {'output_format': 'doc'})
        ret['.rtf']['.pdf'] = (unoconv, {'output_format': 'pdf'})
        ret['.rtf']['.txt'] = (unoconv, {'output_format': 'text'})
        ret['.doc']['.odt'] = (unoconv, {'output_format': 'odt'})
        ret['.doc']['.pdf'] = (unoconv, {'output_format': 'pdf'})
        ret['.doc']['.txt'] = (unoconv, {'output_format': 'text'})
        ret['.docx']['.odt'] = (unoconv, {'output_format': 'odt'})
        ret['.docx']['.doc'] = (unoconv, {'output_format': 'doc'})
        ret['.docx']['.pdf'] = (unoconv, {'output_format': 'pdf'})
        ret['.docx']['.txt'] = (unoconv, {'output_format': 'text'})
        ret['.odt']['.doc'] = (unoconv, {'output_format': 'doc'})
        ret['.odt']['.pdf'] = (unoconv, {'output_format': 'pdf'})
        ret['.odt']['.txt'] = (unoconv, {'output_format': 'text'})
        ret['.ppt']['.odp'] = (unoconv, {'output_format': 'odp'})
        ret['.ppt']['.pdf'] = (unoconv, {'output_format': 'pdf'})
        ret['.ppt']['.txt'] = (unoconv, {'output_format': 'text'})
        ret['.pptx']['.odp'] = (unoconv, {'output_format': 'odp'})
        ret['.pptx']['.ppt'] = (unoconv, {'output_format': 'ppt'})
        ret['.pptx']['.pdf'] = (unoconv, {'output_format': 'pdf'})
        ret['.pptx']['.txt'] = (unoconv, {'output_format': 'text'})
        ret['.odp']['.ppt'] = (unoconv, {'output_format': 'ppt'})
        ret['.odp']['.pdf'] = (unoconv, {'output_format': 'pdf'})
        ret['.odp']['.txt'] = (unoconv, {'output_format': 'text'})
        ret['.xls']['.ods'] = (unoconv, {'output_format': 'ods'})
        ret['.xls']['.pdf'] = (unoconv, {'output_format': 'pdf'})
        ret['.xls']['.txt'] = (unoconv, {'output_format': 'text'})
        ret['.xls']['.csv'] = (unoconv, {'output_format': 'csv'})
        ret['.xlsx']['.xls'] = (unoconv, {'output_format': 'xls'})
        ret['.xlsx']['.ods'] = (unoconv, {'output_format': 'ods'})
        ret['.xlsx']['.pdf'] = (unoconv, {'output_format': 'pdf'})
        ret['.xlsx']['.txt'] = (unoconv, {'output_format': 'text'})
        ret['.xlsx']['.csv'] = (unoconv, {'output_format': 'csv'})
        ret['.ods']['.xls'] = (unoconv, {'output_format': 'xls'})
        ret['.ods']['.pdf'] = (unoconv, {'output_format': 'pdf'})
        ret['.ods']['.txt'] = (unoconv, {'output_format': 'text'})
        ret['.ods']['.csv'] = (unoconv, {'output_format': 'csv'})
    return ret


def get_best_format_to_extract_text_from(filelist, best_formats=CFG_WEBSUBMIT_BEST_FORMATS_TO_EXTRACT_TEXT_FROM):
    """
    Return among the filelist the best file whose format is best suited for
    extracting text.
    """
    from invenio.bibdocfile import decompose_file, normalize_format
    best_formats = [normalize_format(aformat) for aformat in best_formats if can_convert(aformat, '.txt')]
    for aformat in best_formats:
        for filename in filelist:
            if decompose_file(filename, skip_version=True)[2].endswith(aformat):
                return filename
    raise InvenioWebSubmitFileConverterError("It's not possible to extract valuable text from any of the proposed files.")


def get_missing_formats(filelist, desired_conversion=None):
    """Given a list of files it will return a dictionary of the form:
    file1 : missing formats to generate from it...
    """
    from invenio.bibdocfile import normalize_format, decompose_file

    def normalize_desired_conversion():
        ret = {}
        for key, value in desired_conversion.iteritems():
            ret[normalize_format(key)] = [normalize_format(aformat) for aformat in value]
        return ret

    if desired_conversion is None:
        desired_conversion = CFG_WEBSUBMIT_DESIRED_CONVERSIONS

    available_formats = [decompose_file(filename, skip_version=True)[2] for filename in filelist]
    missing_formats = []
    desired_conversion = normalize_desired_conversion()
    ret = {}
    for filename in filelist:
        aformat = decompose_file(filename, skip_version=True)[2]
        if aformat in desired_conversion:
            for desired_format in desired_conversion[aformat]:
                if desired_format not in available_formats and desired_format not in missing_formats:
                    missing_formats.append(desired_format)
                    if filename not in ret:
                        ret[filename] = []
                    ret[filename].append(desired_format)
    return ret


def can_convert(input_format, output_format, max_intermediate_conversions=2):
    """Return the chain of conversion to transform input_format into output_format, if any."""
    from invenio.bibdocfile import normalize_format
    if max_intermediate_conversions <= 0:
        return []
    input_format = normalize_format(input_format)
    output_format = normalize_format(output_format)
    if input_format in __CONVERSION_MAP:
        if output_format in __CONVERSION_MAP[input_format]:
            return [__CONVERSION_MAP[input_format][output_format]]
        best_res = []
        best_intermediate = ''
        for intermediate_format in __CONVERSION_MAP[input_format]:
            res = can_convert(intermediate_format, output_format, max_intermediate_conversions-1)
            if res and (len(res) < best_res or not best_res):
                best_res = res
                best_intermediate = intermediate_format
        if best_res:
            return [__CONVERSION_MAP[input_format][best_intermediate]] + best_res
    return []

def guess_ocropus_produced_garbage(input_file, hocr_p):
    """Return True if the output produced by OCROpus in hocr format contains
    only garbage instead of text. This is implemented via an heuristic:
    if the most common length for sentences encoded in UTF-8 is 1 then
    this is Garbage (tm).
    """

    def _get_words_from_text():
        ret = []
        for row in open(input_file):
            for word in row.strip().split(' '):
                ret.append(word.strip())
        return ret

    def _get_words_from_hocr():
        ret = []
        hocr = extract_hocr(open(input_file).read())
        for dummy, dummy, lines in hocr:
            for dummy, line in lines:
                for word in line.split():
                    ret.append(word.strip())
        return ret

    if hocr_p:
        words = _get_words_from_hocr()
    else:
        words = _get_words_from_text()
    #stats = {}
    #most_common_len = 0
    #most_common_how_many = 0
    #for word in words:
        #if word:
            #word_length = len(word.decode('utf-8'))
            #stats[word_length] = stats.get(word_length, 0) + 1
            #if stats[word_length] > most_common_how_many:
                #most_common_len = word_length
                #most_common_how_many = stats[word_length]
    goods = 0
    bads = 0
    for word in words:
        for char in word.decode('utf-8'):
            if (u'a' <= char <= u'z') or (u'A' <= char <= u'Z'):
                goods += 1
            else:
                bads += 1
    if bads > goods:
        debug('OCROpus produced garbage')
        return True
    else:
        return False


def guess_is_OCR_needed(input_file, ln='en'):
    """
    Tries to see if enough text is retrievable from input_file.
    Return True if OCR is needed, False if it's already
    possible to retrieve information from the document.
    """
    ## FIXME: a way to understand if pdftotext has returned garbage
    ## shuould be found. E.g. 1.0*len(text)/len(zlib.compress(text)) < 2.1
    ## could be a good hint for garbage being found.
    return True


def convert_file(input_file, output_file=None, input_format=None, **params):
    """
    Convert files from one format to another.
    @param input_file [string] the path to an existing file
    @param output_file [string] the path to the desired ouput. (if None a
        temporary file is generated)
    @param input_format [string] the desired format (if None it is taken from
        output_file)
    @param params other paramaters to pass to the particular converter
    @return [string] the final output_file
    """
    from invenio.bibdocfile import decompose_file, normalize_format
    if input_format is None:
        if output_file is None:
            raise ValueError("At least output_file or format should be specified.")
        else:
            output_ext = decompose_file(output_file, skip_version=True)[2]
    else:
        output_ext = normalize_format(input_format)
    input_ext = decompose_file(input_file, skip_version=True)[2]
    conversion_chain = can_convert(input_ext, output_ext)
    if conversion_chain:
        current_input = input_file
        current_output = None
        for i in xrange(len(conversion_chain)):
            if i == (len(conversion_chain) - 1):
                current_output = output_file
            converter = conversion_chain[i][0]
            final_params = dict(conversion_chain[i][1])
            final_params.update(params)
            try:
                return converter(current_input, current_output, **final_params)
            except InvenioWebSubmitFileConverterError, err:
                raise InvenioWebSubmitFileConverterError("Error when converting from %s to %s: %s" % (input_file, output_ext, err))
            except Exception, err:
                register_exception()
                raise InvenioWebSubmitFileConverterError("Unexpected error when converting from %s to %s (%s): %s" % (input_file, output_ext, type(err), err))
            current_input = current_output
    else:
        raise InvenioWebSubmitFileConverterError("It's impossible to convert from %s to %s" % (input_ext, output_ext))




def pstotext(input_file, output_file=None, **dummy):
    """
    Convert a .ps[.gz] into text.
    """
    input_file, output_file, working_dir = prepare_io(input_file, output_file, '.txt')
    if input_file.endswith('.gz'):
        new_input_file = os.path.join(working_dir, 'input.ps')
        execute_command(CFG_PATH_GUNZIP, '-c', input_file, filename_out=new_input_file)
        input_file = new_input_file
    execute_command(CFG_PATH_PSTOTEXT, '-output', output_file, input_file)
    clean_working_dir(working_dir)
    return output_file




__CONVERSION_MAP = get_conversion_map()


def main_cli():
    """
    main function when the library behaves as a normal CLI tool.
    """
    from invenio.bibdocfile import normalize_format
    parser = OptionParser()
    parser.add_option("-c", "--convert", dest="input_name",
                  help="convert the specified FILE", metavar="FILE")
    parser.add_option("-d", "--debug", dest="debug", action="store_true", help="Enable debug information")
    parser.add_option("--special-pdf2hocr2pdf", dest="ocrize", help="convert the given scanned PDF into a PDF with OCRed text", metavar="FILE")
    parser.add_option("-f", "--format", dest="output_format", help="the desired output format", metavar="FORMAT")
    parser.add_option("-o", "--output", dest="output_name", help="the desired output FILE (if not specified a new file will be generated with the desired output format)")
    parser.add_option("--without-pdfa", action="store_false", dest="pdf_a", default=True, help="don't force creation of PDF/A  PDFs")
    parser.add_option("--without-pdfopt", action="store_false", dest="pdfopt", default=True, help="don't force optimization of PDFs files")
    parser.add_option("--without-ocr", action="store_false", dest="ocr", default=True, help="don't force OCR")
    parser.add_option("--can-convert", dest="can_convert", help="display all the possible format that is possible to generate from the given format", metavar="FORMAT")
    parser.add_option("--is-ocr-needed", dest="check_ocr_is_needed", help="check if OCR is needed for the FILE specified", metavar="FILE")
    parser.add_option("-t", "--title", dest="title", help="specify the title (used when creating PDFs)", metavar="TITLE")
    parser.add_option("-l", "--language", dest="ln", help="specify the language (used when performing OCR, e.g. en, it, fr...)", metavar="LN", default='en')
    (options, dummy) = parser.parse_args()
    if options.debug:
        getLogger().setLevel(DEBUG)
    if options.can_convert:
        if options.can_convert:
            input_format = normalize_format(options.can_convert)
            if input_format == '.pdf':
                if can_pdfopt():
                    print "PDF linearization supported"
                else:
                    print "No PDF linearization support"
                if can_pdfa():
                    print "PDF/A generation supported"
                else:
                    print "No PDF/A generation support"
            if can_perform_ocr():
                print "OCR supported"
            else:
                print "OCR not supported"
            print 'Can convert from "%s" to:' % input_format[1:],
            for output_format in __CONVERSION_MAP:
                if can_convert(input_format, output_format):
                    print '"%s"' % output_format[1:],
            print
    elif options.check_ocr_is_needed:
        print "Checking if OCR is needed on %s..." % options.check_ocr_is_needed,
        sys.stdout.flush()
        if guess_is_OCR_needed(options.check_ocr_is_needed):
            print "needed."
        else:
            print "not needed."
    elif options.ocrize:
        try:
            output = pdf2hocr2pdf(options.ocrize, output_file=options.output_name, title=options.title, ln=options.ln)
            print "Output stored in %s" % output
        except InvenioWebSubmitFileConverterError, err:
            print "ERROR: %s" % err
            sys.exit(1)
    else:
        try:
            if not options.output_name and not options.output_format:
                parser.error("Either --format, --output should be specified")
            if not options.input_name:
                parser.error("An input should be specified!")
            output = convert_file(options.input_name, output_file=options.output_name, output_format=options.output_format, pdfopt=options.pdfopt, pdfa=options.pdf_a, title=options.title, ln=options.ln)
            print "Output stored in %s" % output
        except InvenioWebSubmitFileConverterError, err:
            print "ERROR: %s" % err
            sys.exit(1)


if __name__ == "__main__":
    main_cli()
