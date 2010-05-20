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
PDF to HOCR converter.

@see: http://en.wikipedia.org/wiki/HOCR
"""

from logging import debug
import shutil
import os

from invenio.websubmit_file_converter_utils import execute_command, execute_command_with_stderr
from invenio.config import CFG_PATH_OCROSCRIPT, CFG_ETCDIR, CFG_PATH_PAMFILE, CFG_PATH_PDFTOPPM
from invenio.bibdocfile import get_format_from_url, get_superformat_from_format

CFG_TWO2THREE_LANG_CODES = {
    'en': 'eng',
    'nl': 'nld',
    'es': 'spa',
    'de': 'deu',
    'it': 'ita',
    'fr': 'fra',
}

def converter(input_file, output_file, working_dir, ln='en'):
    """
    Return the text content in input_file.
    @param ln is a two letter language code to give the OCR tool a hint.
    """

    def _perform_rotate(working_dir, imagefile, angle):
        """Rotate imagefile of the corresponding angle. Creates a new file
        with rotated- as prefix."""
        debug('Performing rotate on %s by %s degrees' % (imagefile, angle))
        if not angle:
            #execute_command('%s %s %s', CFG_PATH_CONVERT, os.path.join(working_dir, imagefile), os.path.join(working_dir, 'rotated-%s' % imagefile))
            shutil.copy(os.path.join(working_dir, imagefile), os.path.join(working_dir, 'rotated-%s' % imagefile))
        else:
            execute_command(CFG_PATH_CONVERT, os.path.join(working_dir, imagefile), '-rotate', str(angle), os.path.join(working_dir, 'rotated-%s' % imagefile))
        return True

    def _perform_deskew(working_dir, imagefile):
        """Perform ocroscript deskew. Expect to work on rotated-imagefile.
        Creates deskewed-imagefile.
        Return True if deskewing was fine."""
        debug('Performing deskew on %s' % imagefile)
        try:
            dummy, stderr = execute_command_with_stderr(CFG_PATH_OCROSCRIPT, os.path.join(CFG_ETCDIR, 'websubmit', 'file_converter_templates', 'deskew.lua'), os.path.join(working_dir, 'rotated-%s' % imagefile), os.path.join(working_dir, 'deskewed-%s' % imagefile))
            if stderr.strip():
                debug('Errors found during deskewing')
                return False
            else:
                return True
        except InvenioWebSubmitFileConverterError, err:
            debug('Deskewing error: %s' % err)
            return False

    def _perform_recognize(working_dir, imagefile):
        """Perform ocroscript recognize. Expect to work on deskewed-imagefile.
        Creates recognized.out Return True if recognizing was fine."""
        debug('Performing recognize on %s' % imagefile)
        if extract_only_text:
            output_mode = 'text'
        else:
            output_mode = 'hocr'
        try:
            dummy, stderr = execute_command_with_stderr(CFG_PATH_OCROSCRIPT, 'recognize', '--tesslanguage=%s' % ln, '--output-mode=%s' % output_mode, os.path.join(working_dir, 'deskewed-%s' % imagefile), filename_out=os.path.join(working_dir, 'recognize.out'))
            if stderr.strip():
                ## There was some output on stderr
                debug('Errors found in recognize.err')
                return False
            return not guess_ocropus_produced_garbage(os.path.join(working_dir, 'recognize.out'), not extract_only_text)
        except InvenioWebSubmitFileConverterError, err:
            debug('Recognizer error: %s' % err)
            return False

    def _perform_dummy_recognize(working_dir, imagefile):
        """Return an empty text or an empty hocr referencing the image."""
        debug('Performing dummy recognize on %s' % imagefile)
        if extract_only_text:
            out = ''
        else:
            stdout = stderr = ''
            try:
                ## Since pdftoppm is returning a netpbm image, we use
                ## pamfile to retrieve the size of the image, in order to
                ## create an empty .hocr file containing just the
                ## desired file and a reference to its size.
                stdout, stderr = execute_command_with_stderr(CFG_PATH_PAMFILE, os.path.join(working_dir, imagefile))
                g = re.search(r'(?P<width>\d+) by (?P<height>\d+)', stdout)
                if g:
                    width = int(g.group('width'))
                    height = int(g.group('height'))

                    out = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml"><head><meta content="ocr_line ocr_page" name="ocr-capabilities"/><meta content="en" name="ocr-langs"/><meta content="Latn" name="ocr-scripts"/><meta content="" name="ocr-microformats"/><title>OCR Output</title></head>
    <body><div class="ocr_page" title="bbox 0 0 %s %s; image %s">
    </div></body></html>""" % (width, height, os.path.join(working_dir, imagefile))
                else:
                    raise InvenioWebSubmitFileConverterError()
            except Exception, err:
                raise InvenioWebSubmitFileConverterError('It\'s impossible to retrieve the size of %s needed to perform a dummy OCR. The stdout of pamfile was: %s, the stderr was: %s. (%s)' % (imagefile, stdout, stderr, err))
        open(os.path.join(working_dir, 'recognize.out'), 'w').write(out)

    if CFG_PATH_OCROSCRIPT:
        ln = CFG_TWO2THREE_LANG_CODES.get(ln, 'eng')

        extract_only_text = get_superformat_from_format(get_format_from_url(output_file)) == '.txt'
        execute_command(CFG_PATH_PDFTOPPM, '-r', '300', '-aa', 'yes', '-freetype' 'yes', input_file, os.path.join(working_dir, 'image'))

        images = os.listdir(working_dir)
        images.sort()
        for imagefile in images:
            if imagefile.startswith('image-'):
                for angle in (0, 90, 180, 270):
                    if _perform_rotate(working_dir, imagefile, angle) and _perform_deskew(working_dir, imagefile) and _perform_recognize(working_dir, imagefile):
                        ## Things went nicely! So we can remove the original
                        ## pbm picture which is soooooo huuuuugeee.
                        os.remove(os.path.join(working_dir, 'rotated-%s' % imagefile))
                        os.remove(os.path.join(working_dir, imagefile))
                        break
                else:
                    _perform_dummy_recognize(working_dir, imagefile)
                open(output_file, 'a').write(open(os.path.join(working_dir, 'recognize.out')).read())

    else:
        raise InvenioWebSubmitFileConverterError("It's impossible to generate HOCR output from PDF. OCROpus is not available.")

def check_prerequisites(input_format, output_format, working_dir, ln='en'):
    if not is_executable(CFG_PATH_OCROSCRIPT):
        raise InvenioWebSubmitFileConverterError("CFG_PATH_OCROSCRIPT is set to %s, which either does not exists or is not executable" % (repr(CFG_PATH_OCROSCRIPT)))
    if not is_executable(CFG_PATH_PAMFILE):
        raise InvenioWebSubmitFileConverterError("CFG_PATH_PAMFILE is set to %s, which either does not exists or is not executable" % (repr(CFG_PATH_PAMFILE)))
    if not is_executable(CFG_PATH_PDFTOPPM):
        raise InvenioWebSubmitFileConverterError("CFG_PATH_PDFTOPPM is set to %s, which either does not exists or is not executable" % (repr(CFG_PATH_PDFTOPPM)))
    if not is_executable(CFG_PATH_CONVERT):
        raise InvenioWebSubmitFileConverterError("CFG_PATH_CONVERT is set to %s, which either does not exists or is not executable" % (repr(CFG_PATH_CONVERT)))
