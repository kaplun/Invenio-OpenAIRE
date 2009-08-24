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
PDF2OCR WebSubmit File Converter based on Google OCROpus 0.3.1.
"""

import os
from invenio.config import CFG_PATH_CONVERT, CFG_PATH_OCROSCRIPT, \
    CFG_PATH_PAMFILE, CFG_PATH_PDFTOPPM, CFG_ETCDIR
from invenio.websubmit_file_converter_utils import execute_command, \
    execute_command_with_stderr, InvenioWebSubmitFileConverterError, \
    create_temporary_file

CFG_CONVERTER_NEEDS_WORKING_DIR = True


def converter(input_file, output_file, working_dir, ln='en', output_format='.pdf', font="Courier", author=None, keywords=None, subject=None, title=None, draft=False, **dummy):
    """
    Return the text content in input_file.
    @param ln is a two letter language code to give the OCR tool a hint.
    @param return_working_dir if set to True, will return output_file path and the working_dir path, instead of deleting the working_dir. This is useful in case you need the intermediate images to build again a PDF.
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
        if output_format == '.txt':
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
        if output_format == '.txt':
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

    def _perform_hocr2pdf(input_file):
        try:
            create_pdf(extract_hocr(open(input_file).read()), output_file, font=font, author=author, keywords=keywords, subject=subject, title=title, image_path=working_dir, draft=draft)
        except Exception, err:
            raise InvenioWebSubmitFileConverterError('It\'s impossible to convert the intermediate %s file to PDF: %s' % (input_file))

    if CFG_PATH_OCROSCRIPT:
        ln = CFG_TWO2THREE_LANG_CODES.get(ln, 'eng')
        execute_command(CFG_PATH_PDFTOPPM, '-r', '300', '-aa', 'yes', '-freetype' 'yes', input_file, os.path.join(working_dir, 'image'))

        images = os.listdir(working_dir)
        images.sort()
        if output_format == '.pdf':
            tmp_output_file = create_temporary_file('.hocr')
        else:
            tmp_output_file = output_file
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
                open(tmp_output_file, 'a').write(open(os.path.join(working_dir, 'recognize.out')).read())

        if output_format == '.pdf;ocr':
            _perform_hocr2pdf(tmp_output_file)
            os.remove(tmp_output_file)

    else:
        raise InvenioWebSubmitFileConverterError("It's impossible to generate HOCR output from PDF. OCROpus is not available.")


def check_prerequisities():
    """Return True if OpenOffice tmpdir do exists and OpenOffice can
    successfully create file there."""
    return bool(CFG_PATH_CONVERT and CFG_PATH_CONVERT and CFG_PATH_PAMFILE and CFG_PATH_PDFTOPPM)

def get_conversion_map():
    return {'pdf' : {'.txt;ocr' : {'output_format' : '.txt'}, '.pdf;ocr' : {'output_format' : '.pdf'}}}
