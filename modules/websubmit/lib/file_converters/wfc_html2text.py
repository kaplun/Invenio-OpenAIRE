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
html2text WebSubmit File Converter Python based.
"""
import HTMLParser

CFG_CONVERTER_NEEDS_WORKING_DIR = False

def check_prerequisities():
    return True

def converter(input_file, output_file, working_dir, **dummy):
    """
    Return the text content of an HTML/XML file.
    """

    class HTMLStripper(HTMLParser.HTMLParser):

        def __init__(self, output_file):
            HTMLParser.HTMLParser.__init__(self)
            self.output_file = output_file

        def handle_entityref(self, name):
            if name in entitydefs:
                self.output_file.write(entitydefs[name].decode('latin1').encode('utf8'))

        def handle_data(self, data):
            if data.strip():
                self.output_file.write(_RE_CLEAN_SPACES.sub(' ', data))

        def handle_charref(self, data):
            try:
                self.output_file.write(unichr(int(data)).encode('utf8'))
            except:
                pass

        def close(self):
            self.output_file.close()
            HTMLParser.HTMLParser.close(self)

    html_stripper = HTMLStripper(open(output_file, 'w'))
    for line in open(input_file):
        html_stripper.feed(line)
    html_stripper.close()

def get_conversion_map():
    return {
        '.xml' : {'.txt' : ()},
        '.html' : {'.txt' : ()},
        '.htm' : {'.txt' : ()}}
