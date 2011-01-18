# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2008, 2009, 2010, 2011 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
BibClassify text extractor.

This module provides method to extract the fulltext from local or remote
documents. Currently 2 formats of documents are supported: PDF and text
documents.

2 methods provide the functionality of the module: text_lines_from_local_file
and text_lines_from_url.

This module also provides the utility 'is_pdf' that uses GNU file in order to
determine if a local file is a PDF file.
"""

import os
import re
import sys
import tempfile
import urllib2

from bibclassify_utils import write_message

_ONE_WORD = re.compile("[A-Za-z]{2,}")

def text_lines_from_local_file(document, remote=False):
    """Returns the fulltext of the local file."""
    try:
        if is_pdf(document):
            if not executable_exists("pdftotext"):
                write_message("ERROR: pdftotext is not available on the "
                    "system.", stream=sys.stderr, verbose=1)
            cmd = "pdftotext -q -enc UTF-8 %s -" % re.escape(document)
            filestream = os.popen(cmd)
        else:
            filestream = open(document, "r")
    except IOError, ex1:
        write_message("ERROR: Unable to read from file %s. (%s)" % (document,
            ex1.strerror), stream=sys.stderr, verbose=1)
        return None

    lines = [line.decode("utf-8") for line in filestream]
    filestream.close()

    if not _is_english_text('\n'.join(lines)):
        write_message("WARNING: It seems the file '%s' is unvalid and doesn't "
            "contain text. Please communicate this file to the Invenio "
            "team." % document, stream=sys.stderr, verbose=0)

    line_nb = len(lines)
    word_nb = 0
    for line in lines:
        word_nb += len(re.findall("\S+", line))

    # Discard lines that do not contain at least one word.
    lines = [line for line in lines if _ONE_WORD.search(line) is not None]

    if not remote:
        write_message("INFO: Local file has %d lines and %d words." % (line_nb,
            word_nb), stream=sys.stderr, verbose=3)

    return lines

def _is_english_text(text):
    """
    Checks if a text is correct english.
    Computes the number of words in the text and compares it to the
    expected number of words (based on an average size of words of 5.1
    letters).

    @param text_lines: the text to analyze
    @type text_lines:  string
    @return:           True if the text is English, False otherwise
    @rtype:            Boolean
    """
    # Consider one word and one space.
    avg_word_length = 5.1 + 1
    expected_word_number = float(len(text)) / avg_word_length

    words = [word
             for word in re.split('\W', text)
             if word.isalpha()]

    word_number = len(words)

    return word_number > .5 * expected_word_number

def text_lines_from_url(url, user_agent=""):
    """Returns the fulltext of the file found at the URL."""
    request = urllib2.Request(url)
    if user_agent:
        request.add_header("User-Agent", user_agent)
    try:
        distant_stream = urllib2.urlopen(request)
        # Write the URL content to a temporary file.
        tmpfd, local_file = tempfile.mkstemp(prefix="bibclassify.")
        os.close(tmpfd)
        local_stream = open(local_file, "w")
        local_stream.write(distant_stream.read())
        local_stream.close()
    except:
        write_message("ERROR: Unable to read from URL %s." % url,
            stream=sys.stderr, verbose=1)
        return None
    else:
        # Read lines from the temporary file.
        lines = text_lines_from_local_file(local_file, remote=True)
        os.remove(local_file)

        line_nb = len(lines)
        word_nb = 0
        for line in lines:
            word_nb += len(re.findall("\S+", line))

        write_message("INFO: Remote file has %d lines and %d words." %
            (line_nb, word_nb), stream=sys.stderr, verbose=3)

        return lines

def executable_exists(executable):
    """Tests if an executable is available on the system."""
    for directory in os.getenv("PATH").split(":"):
        if os.path.exists(os.path.join(directory, executable)):
            return True
    return False

def is_pdf(document):
    """Checks if a document is a PDF file. Returns True if is is."""
    if not executable_exists:
        write_message("WARNING: GNU file was not found on the system. "
            "Switching to a weak file extension test.", stream=sys.stderr,
            verbose=2)
        if document.lower().endswith(".pdf"):
            return True
        return False
    # Tested with file version >= 4.10. First test is secure and works
    # with file version 4.25. Second condition is tested for file
    # version 4.10.
    file_output = os.popen('file ' + re.escape(document)).read()
    try:
        filetype = file_output.split(":")[1]
    except IndexError:
        write_message("WARNING: Your version of the 'file' utility seems to "
            "be unsupported. Please report this to info@invenio-software.org.",
            stream=sys.stderr, verbose=2)
        sys.exit(1)

    pdf = filetype.find("PDF") > -1
    # This is how it should be done however this is incompatible with
    # file version 4.10.
    #os.popen('file -bi ' + document).read().find("application/pdf")
    return pdf

