# -*- coding: utf-8 -*-
## Invenio elmsubmit unit tests.

## This file is part of Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010 CERN.
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

"""Unit tests for the elmsubmit."""

__revision__ = "$Id$"

import unittest
import os
from string import expandtabs
import xml.dom.minidom

from invenio.config import CFG_TMPDIR
import invenio.elmsubmit_config as elmsubmit_config
from invenio import elmsubmit
from invenio.testutils import make_test_suite, run_test_suite

if os.path.exists(os.path.join(CFG_TMPDIR,
                  elmsubmit_config.CFG_ELMSUBMIT_FILES['test_case_1'])):
    test_case_1_file_exists = True
else:
    test_case_1_file_exists = False

if os.path.exists(os.path.join(CFG_TMPDIR,
                  elmsubmit_config.CFG_ELMSUBMIT_FILES['test_case_2'])):
    test_case_2_file_exists = True
else:
    test_case_2_file_exists = False

class MarcTest(unittest.TestCase):
    """ elmsubmit - test for sanity """

    if test_case_1_file_exists:
        def test_simple_marc(self):
            """elmsubmit - parsing simple email"""
            f=open(os.path.join(CFG_TMPDIR, elmsubmit_config.CFG_ELMSUBMIT_FILES['test_case_1']),'r')
            email = f.read()
            f.close()

            # let's try to parse an example email and compare it with the appropriate marc xml
            x = elmsubmit.process_email(email)
            y  = """<record>
            <datafield tag ="245" ind1="" ind2="">
            <subfield code="a">something</subfield>
            </datafield>
            <datafield tag ="100" ind1="" ind2="">
            <subfield code="a">Simko, T</subfield>
            <subfield code="u">CERN</subfield>
            </datafield>
            </record>"""

            # in order to properly compare the marc files we have to remove the FFT node, it includes a random generated file path

            dom_x = xml.dom.minidom.parseString(x)
            datafields = dom_x.getElementsByTagName("datafield")

            #remove all the FFT datafields
            for node in datafields:
                if (node.hasAttribute("tag") and  node.getAttribute("tag") == "FFT"):
                    node.parentNode.removeChild(node)
                    node.unlink()

            new_x = dom_x.toprettyxml("","\n")

            dom_y = xml.dom.minidom.parseString(y)
            new_y = dom_y.toprettyxml("","\n")

            # 'normalize' the two XML MARC files for the purpose of comparing
            new_x = expandtabs(new_x)
            new_y = expandtabs(new_y)

            new_x = new_x.replace(' ','')
            new_y = new_y.replace(' ','')

            new_x = new_x.replace('\n','')
            new_y = new_y.replace('\n','')

            # compare the two xml marcs
            self.assertEqual(new_x,new_y)

    if test_case_2_file_exists:
        def test_complex_marc(self):
            """elmsubmit - parsing complex email with multiple fields"""
            f=open(os.path.join(CFG_TMPDIR, elmsubmit_config.CFG_ELMSUBMIT_FILES['test_case_2']),'r')
            email = f.read()
            f.close()

            # let's try to reproduce the demo XML MARC file by parsing it and printing it back:
            x = elmsubmit.process_email(email)
            y = """<record>
            <datafield tag ="245" ind1="" ind2="">
            <subfield code="a">something</subfield>
            </datafield>
            <datafield tag ="700" ind1="" ind2="">
            <subfield code="a">Le Meur, J Y</subfield>
            <subfield code="u">MIT</subfield>
            </datafield>
            <datafield tag ="700" ind1="" ind2="">
            <subfield code="a">Jedrzejek, K J</subfield>
            <subfield code="u">CERN2</subfield>
            </datafield>
            <datafield tag ="700" ind1="" ind2="">
            <subfield code="a">Favre, G</subfield>
            <subfield code="u">CERN3</subfield>
            </datafield>
            <datafield tag ="111" ind1="" ind2="">
            <subfield code="a">test11</subfield>
            <subfield code="c">test31</subfield>
            </datafield>
            <datafield tag ="111" ind1="" ind2="">
            <subfield code="a">test12</subfield>
            <subfield code="c">test32</subfield>
            </datafield>
            <datafield tag ="111" ind1="" ind2="">
            <subfield code="a">test13</subfield>
            <subfield code="c">test33</subfield>
            </datafield>
            <datafield tag ="111" ind1="" ind2="">
            <subfield code="b">test21</subfield>
            <subfield code="d">test41</subfield>
            </datafield>
            <datafield tag ="111" ind1="" ind2="">
            <subfield code="b">test22</subfield>
            <subfield code="d">test42</subfield>
            </datafield>
            <datafield tag ="111" ind1="" ind2="">
            <subfield code="a">test14</subfield>
            </datafield>
            <datafield tag ="111" ind1="" ind2="">
            <subfield code="e">test51</subfield>
            </datafield>
            <datafield tag ="111" ind1="" ind2="">
            <subfield code="e">test52</subfield>
            </datafield>
            <datafield tag ="100" ind1="" ind2="">
            <subfield code="a">Simko, T</subfield>
            <subfield code="u">CERN</subfield>
            </datafield>
            </record>"""

            # in order to properly compare the marc files we have to remove the FFT node, it includes a random generated file path

            dom_x = xml.dom.minidom.parseString(x)
            datafields = dom_x.getElementsByTagName("datafield")

            #remove all the FFT datafields
            for node in datafields:
                if (node.hasAttribute("tag") and  node.getAttribute("tag") == "FFT"):
                    node.parentNode.removeChild(node)
                    node.unlink()


            new_x = dom_x.toprettyxml("","\n")

            dom_y = xml.dom.minidom.parseString(y)
            new_y = dom_y.toprettyxml("","\n")
            # 'normalize' the two XML MARC files for the purpose of comparing
            new_x = expandtabs(new_x)
            new_y = expandtabs(new_y)

            new_x = new_x.replace(' ','')
            new_y = new_y.replace(' ','')

            new_x = new_x.replace('\n','')
            new_y = new_y.replace('\n','')

            # compare the two xml marcs
            self.assertEqual(new_x,new_y)

class FileStorageTest(unittest.TestCase):
    """ testing proper storage of files """

    if test_case_2_file_exists:
        def test_read_text_files(self):
            """elmsubmit - reading text files"""

            f=open(os.path.join(CFG_TMPDIR, elmsubmit_config.CFG_ELMSUBMIT_FILES['test_case_2']),'r')
            email = f.read()
            f.close()

            # let's try to see if the files were properly stored:
            xml_marc = elmsubmit.process_email(email)

            dom = xml.dom.minidom.parseString(xml_marc)
            datafields = dom.getElementsByTagName("datafield")

            # get the file addresses
            file_list = []

            for node in datafields:
                if (node.hasAttribute("tag") and  node.getAttribute("tag") == "FFT"):
                    children = node.childNodes
                    for child in children:
                        if (child.hasChildNodes()):
                            file_list.append(child.firstChild.nodeValue)

            f=open(file_list[0], 'r')
            x = f.read()
            f.close()

            x.lstrip()
            x.rstrip()

            y = """second attachment\n"""

            self.assertEqual(x,y)

            f=open(file_list[1], 'r')
            x = f.read()
            f.close()

            x.lstrip()
            x.rstrip()

            y = """some attachment\n"""
            self.assertEqual(x,y)

TEST_SUITE = make_test_suite(MarcTest,
                             FileStorageTest,)

if __name__ == '__main__':
    run_test_suite(TEST_SUITE)
