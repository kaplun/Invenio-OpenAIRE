# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2010, 2011 CERN.
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
The Refextract regression tests suite

The tests will not modifiy the database.
They are intended to make sure there is no regression in references parsing.
"""

import unittest
import re

from invenio.testutils import make_test_suite, run_test_suite
## Import the minimal necessary methods and variables needed to run Refextract
from invenio.refextract_engine import parse_references
from invenio.docextract_utils import setup_loggers
from invenio.refextract_text import wash_and_repair_reference_line

try:
    from nose.plugins.skip import SkipTest
except ImportError:
    class SkipTest(Exception):
        """Skip a test"""


def compare_references(test, references, expected_references, ignore_misc=True):
    out = references

    # Remove the ending statistical datafield from the final extracted references
    out = out[:out.find('<datafield tag="999" ind1="C" ind2="6">')].rstrip()
    out += "\n</record>"

    # We don't care about what's in the misc field
    out = re.sub('      <subfield code="m">[^<]*</subfield>\n', '', out)

    if out != expected_references:
        print 'OUT'
        print out

    test.assertEqual(out, expected_references)


def reference_test(test, ref_line, parsed_reference, ignore_misc=True):
    #print u'refs: %s' % ref_line
    ref_line = wash_and_repair_reference_line(ref_line)
    #print u'cleaned: %s' % ref_line
    out = parse_references([ref_line], inspire=test.inspire,
        kb_journals=test.kb_journals, kb_reports=test.kb_reports,
        kb_authors=test.kb_authors, kb_books=test.kb_books,
        kb_conferences=test.kb_conferences, kb_journals_re=test.kb_journals_re)
    compare_references(test, out, parsed_reference)


class RefextractInvenioTest(unittest.TestCase):

    def setUp(self):
        self.inspire = False
        setup_loggers(verbosity=1)
        self.maxDiff = 2000
        self.kb_journals = None
        self.kb_journals_re = None
        self.kb_reports = None
        self.kb_authors = None
        self.kb_books = None
        self.kb_conferences = None

    def test_month_with_year(self):
        ref_line = u"""[2] S. Weinberg, A Model of Leptons, Phys. Rev. Lett. 19 (Nov, 1967) 1264–1266."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">2</subfield>
      <subfield code="h">S. Weinberg, A Model of Leptons</subfield>
      <subfield code="s">Phys. Rev. Lett. 19 (1967) 1264</subfield>
   </datafield>
</record>""")

    def test_numeration_not_finding_year(self):
        ref_line = u"""[137] M. Papakyriacou, H. Mayer, C. Pypen, H. P. Jr., and S. Stanzl-Tschegg, “Inﬂuence of loading frequency on high cycle fatigue properties of b.c.c. and h.c.p. metals,” Materials Science and Engineering, vol. A308, pp. 143–152, 2001."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">137</subfield>
      <subfield code="h">M. Papakyriacou, H. Mayer, C. Pypen, H. P. Jr., and S. Stanzl-Tschegg</subfield>
      <subfield code="s">Mat.Sci.Eng. A308 (2001) 143</subfield>
   </datafield>
</record>""")

    def test_numeration_not_finding_year2(self):
        """Bug fix test for numeration not finding year in this citation"""
        ref_line = u"""[138] Y.-B. Park, R. Mnig, and C. A. Volkert, “Frequency effect on thermal fatigue damage in Cu interconnects,” Thin Solid Films, vol. 515, pp. 3253– 3258, 2007."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">138</subfield>
      <subfield code="h">Y.-B. Park, R. Mnig, and C. A. Volkert</subfield>
      <subfield code="s">Thin Solid Films 515 (2007) 3253</subfield>
   </datafield>
</record>""")


class RefextractTest(unittest.TestCase):
    """Testing output of refextract"""

    def setUp(self):
        self.inspire = True
        self.kb_books = [
            ('Griffiths, David', 'Introduction to elementary particles', '2008')
        ]
        self.kb_conferences = []
        self.kb_authors = [
            "Du ̈hrssen---Dührssen"
        ]
        self.kb_journals = [
            "PHYSICAL REVIEW SPECIAL TOPICS ACCELERATORS AND BEAMS---Phys.Rev.ST Accel.Beams",
            "PHYS REV D---Phys.Rev.D",
            "PHYS REV---Phys.Rev.",
            "PHYS REV LETT---Phys.Rev.Lett.",
            "J PHYS---J.Phys.",
            "JOURNAL OF PHYSICS---J.Phys.",
            "J PHYS G---J.Phys.G",
            "PHYSICAL REVIEW---Phys.Rev.",
            "ADV THEO MATH PHYS---Adv.Theor.Math.Phys.",
            "MATH PHYS---Math.Phys.",
            "J MATH PHYS---J.Math.Phys.",
            "JHEP---JHEP",
            "SITZUNGSBER PREUSS AKAD WISS PHYS MATH KL---Sitzungsber.Preuss.Akad.Wiss.Berlin (Math.Phys.)",
            "PHYS LETT---Phys.Lett.",
            "NUCL PHYS---Nucl.Phys.",
            "JINST---JINST",
            "THE EUROPEAN PHYSICAL JOURNAL C PARTICLES AND FIELDS---Eur.Phys.J.C",
            "COMMUN MATH PHYS---Commun.Math.Phys.",
            "COMM MATH PHYS---Commun.Math.Phys.",
            "REV MOD PHYS---Rev.Mod.Phys.",
            "ANN PHYS U S---Ann.Phys.",
            "AM J PHYS---Am.J.Phys.",
            "PROC R SOC LONDON SER---Proc.Roy.Soc.Lond.",
            "CLASS QUANT GRAVITY---Class.Quant.Grav.",
            "FOUND PHYS---Found.Phys.",
            "IEEE TRANS NUCL SCI---IEEE Trans.Nucl.Sci.",
            "SCIENCE---Science",
            "ACTA MATERIALIA---Acta Mater.",
            "REVIEWS OF MODERN PHYSICS---Rev.Mod.Phys.",
            "NUCL INSTRUM METHODS---Nucl.Instrum.Meth.",
            "Z PHYS---Z.Phys.",
        ]
        self.kb_journals_re = [
            "DAN---Dokl.Akad.Nauk Ser.Fiz.",
        ]
        self.kb_reports = [
            "#####CERN#####",
            "< yy 999>",
            "< yyyy 999>",
            "ATL CONF---ATL-CONF",
            "ATL PHYS INT---ATL-PHYS-INT",
            "ATLAS CONF---ATL-CONF",
            "#####LANL#####",
            "<s/syymm999>",
            "<syymm999>",
            "HEP PH---hep-ph",
            "HEP TH---hep-th",
            "#####LHC#####",
            "< yy 999>",
            "<syyyy 999>",
            "< 999>",
            "< 9999>",
            "CERN LHC PROJECT REPORT---CERN-LHC-Project-Report",
            "CLIC NOTE              ---CERN-CLIC-Note",
            "CERN LHCC              ---CERN-LHCC",
        ]
        setup_loggers(verbosity=1)
        self.maxDiff = 2000

    def test_year_title_volume_page(self):
        ref_line = u"[14] L. Randall and R. Sundrum, (1999) Phys. Rev. Lett. B83  S08004 More text"
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">14</subfield>
      <subfield code="h">L. Randall and R. Sundrum</subfield>
      <subfield code="s">Phys.Rev.Lett.,B83,S08004</subfield>
   </datafield>
</record>""")

    def test_url1(self):
        ref_line = u"""[1] <a href="http://cdsweb.cern.ch/">CERN Document Server</a> J. Maldacena, Adv. Theor. Math. Phys. 2 (1998) 231, hep-th/9711200; http://cdsweb.cern.ch/ then http://www.itp.ucsb.edu/online/susyc99/discussion/. ; L. Susskind, J. Math. Phys. 36 (1995) 6377, hep-th/9409089; hello world a<a href="http://uk.yahoo.com/">Yahoo!</a>. Fin."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">1</subfield>
      <subfield code="u">http://cdsweb.cern.ch/</subfield>
      <subfield code="z">CERN Document Server</subfield>
      <subfield code="h">J. Maldacena</subfield>
      <subfield code="s">Adv.Theor.Math.Phys.,2,231</subfield>
      <subfield code="r">hep-th/9711200</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">1</subfield>
      <subfield code="u">http://cdsweb.cern.ch/</subfield>
      <subfield code="u">http://www.itp.ucsb.edu/online/susyc99/discussion/</subfield>
      <subfield code="h">L. Susskind</subfield>
      <subfield code="s">J.Math.Phys.,36,6377</subfield>
      <subfield code="r">hep-th/9409089</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">1</subfield>
      <subfield code="u">http://uk.yahoo.com/</subfield>
      <subfield code="z">Yahoo!</subfield>
   </datafield>
</record>""")

    def test_url2(self):
        ref_line = u"""[2] J. Maldacena, Adv. Theor. Math. Phys. 2 (1998) 231; hep-th/9711200. http://cdsweb.cern.ch/"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">2</subfield>
      <subfield code="h">J. Maldacena</subfield>
      <subfield code="s">Adv.Theor.Math.Phys.,2,231</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">2</subfield>
      <subfield code="r">hep-th/9711200</subfield>
      <subfield code="u">http://cdsweb.cern.ch/</subfield>
   </datafield>
</record>""")

    def test_url3(self):
        ref_line = u"3. “pUML Initial Submission to OMG’ s RFP for UML 2.0 Infrastructure”. URL http://www.cs.york.ac.uk/puml/"
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">3</subfield>
      <subfield code="t">pUML Initial Submission to OMG\u2019 s RFP for UML 2.0 Infrastructure</subfield>
      <subfield code="u">http://www.cs.york.ac.uk/puml/</subfield>
   </datafield>
</record>""")

    def test_url4(self):
        ref_line = u"""[3] S. Gubser, I. Klebanov and A. Polyakov, Phys. Lett. B428 (1998) 105; hep-th/9802109. http://cdsweb.cern.ch/search.py?AGE=hello-world&ln=en"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">3</subfield>
      <subfield code="h">S. Gubser, I. Klebanov and A. Polyakov</subfield>
      <subfield code="s">Phys.Lett.,B428,105</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">3</subfield>
      <subfield code="r">hep-th/9802109</subfield>
      <subfield code="u">http://cdsweb.cern.ch/search.py?AGE=hello-world&amp;ln=en</subfield>
   </datafield>
</record>""")

    def test_hep(self):
        ref_line = u"""[5] O. Aharony, S. Gubser, J. Maldacena, H. Ooguri and Y. Oz, hep-th/9905111."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">5</subfield>
      <subfield code="h">O. Aharony, S. Gubser, J. Maldacena, H. Ooguri and Y. Oz</subfield>
      <subfield code="r">hep-th/9905111</subfield>
   </datafield>
</record>""")

    def test_hep2(self):
        ref_line = u"""[4] E. Witten, Adv. Theor. Math. Phys. 2 (1998) 253; hep-th/9802150."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">4</subfield>
      <subfield code="h">E. Witten</subfield>
      <subfield code="s">Adv.Theor.Math.Phys.,2,253</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">4</subfield>
      <subfield code="r">hep-th/9802150</subfield>
   </datafield>
</record>""")

    def test_hep3(self):
        ref_line = u"""[6] L. Susskind, J. Math. Phys. 36 (1995) 6377; hep-th/9409089."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">6</subfield>
      <subfield code="h">L. Susskind</subfield>
      <subfield code="s">J.Math.Phys.,36,6377</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">6</subfield>
      <subfield code="r">hep-th/9409089</subfield>
   </datafield>
</record>""")

    def test_hep4(self):
        ref_line = u"""[7] L. Susskind and E. Witten, hep-th/9805114."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">7</subfield>
      <subfield code="h">L. Susskind and E. Witten</subfield>
      <subfield code="r">hep-th/9805114</subfield>
   </datafield>
</record>""")

    def test_double_hep_no_semi_colon(self):
        ref_line = u"""[7] W. Fischler and L. Susskind, hep-th/9806039; N. Kaloper and A. Linde, Phys. Rev. D60 (1999) 105509, hep-th/9904120."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">7</subfield>
      <subfield code="h">W. Fischler and L. Susskind</subfield>
      <subfield code="r">hep-th/9806039</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">7</subfield>
      <subfield code="h">N. Kaloper and A. Linde</subfield>
      <subfield code="s">Phys.Rev.,D60,105509</subfield>
      <subfield code="r">hep-th/9904120</subfield>
   </datafield>
</record>""")

    def test_journal_colon_sep(self):
        ref_line = u"""[9] R. Bousso, JHEP 9906:028 (1999); hep-th/9906022."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">9</subfield>
      <subfield code="h">R. Bousso</subfield>
      <subfield code="s">JHEP,9906,028</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">9</subfield>
      <subfield code="r">hep-th/9906022</subfield>
   </datafield>
</record>""")

    def test_book1(self):
        """book with authors and title but no quotes"""
        ref_line = u"""[10] R. Penrose and W. Rindler, Spinors and Spacetime, volume 2, chapter 9 (Cambridge University Press, Cambridge, 1986)."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">10</subfield>
      <subfield code="h">R. Penrose and W. Rindler</subfield>
   </datafield>
</record>""")

    def test_hep_combined(self):
        ref_line = u"""[11] R. Britto-Pacumio, A. Strominger and A. Volovich, JHEP 9911:013 (1999); hep-th/9905210. blah hep-th/9905211 blah hep-ph/9711200"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">11</subfield>
      <subfield code="h">R. Britto-Pacumio, A. Strominger and A. Volovich</subfield>
      <subfield code="s">JHEP,9911,013</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">11</subfield>
      <subfield code="r">hep-th/9905210</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">11</subfield>
      <subfield code="r">hep-th/9905211</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">11</subfield>
      <subfield code="r">hep-ph/9711200</subfield>
   </datafield>
</record>""")

    def test_misc5(self):
        ref_line = u"""[12] V. Balasubramanian and P. Kraus, Commun. Math. Phys. 208 (1999) 413; hep-th/9902121."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">12</subfield>
      <subfield code="h">V. Balasubramanian and P. Kraus</subfield>
      <subfield code="s">Commun.Math.Phys.,208,413</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">12</subfield>
      <subfield code="r">hep-th/9902121</subfield>
   </datafield>
</record>""")

    def test_misc6(self):
        ref_line = u"""[13] V. Balasubramanian and P. Kraus, Phys. Rev. Lett. 83 (1999) 3605; hep-th/9903190."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">13</subfield>
      <subfield code="h">V. Balasubramanian and P. Kraus</subfield>
      <subfield code="s">Phys.Rev.Lett.,83,3605</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">13</subfield>
      <subfield code="r">hep-th/9903190</subfield>
   </datafield>
</record>""")

    def test_hep5(self):
        ref_line = u"""[14] P. Kraus, F. Larsen and R. Siebelink, hep-th/9906127."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">14</subfield>
      <subfield code="h">P. Kraus, F. Larsen and R. Siebelink</subfield>
      <subfield code="r">hep-th/9906127</subfield>
   </datafield>
</record>""")

    def test_report1(self):
        ref_line = u"""[15] L. Randall and R. Sundrum, Phys. Rev. Lett. 83 (1999) 4690; hep-th/9906064. this is a test RN of a different type: CERN-LHC-Project-Report-2006. more text."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">15</subfield>
      <subfield code="h">L. Randall and R. Sundrum</subfield>
      <subfield code="s">Phys.Rev.Lett.,83,4690</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">15</subfield>
      <subfield code="r">hep-th/9906064</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">15</subfield>
      <subfield code="r">CERN-LHC-Project-Report-2006</subfield>
   </datafield>
</record>""")

    def test_hep6(self):
        ref_line = u"""[16] S. Gubser, hep-th/9912001."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">16</subfield>
      <subfield code="h">S. Gubser</subfield>
      <subfield code="r">hep-th/9912001</subfield>
   </datafield>
</record>""")

    def test_triple_hep(self):
        ref_line = u"""[17] H. Verlinde, hep-th/9906182; H. Verlinde, hep-th/9912018; J. de Boer, E. Verlinde and H. Verlinde, hep-th/9912012."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">17</subfield>
      <subfield code="h">H. Verlinde</subfield>
      <subfield code="r">hep-th/9906182</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">17</subfield>
      <subfield code="h">H. Verlinde</subfield>
      <subfield code="r">hep-th/9912018</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">17</subfield>
      <subfield code="h">J. de Boer, E. Verlinde and H. Verlinde</subfield>
      <subfield code="r">hep-th/9912012</subfield>
   </datafield>
</record>""")

    def test_url_no_tag(self):
        ref_line = u"""[18] E. Witten, remarks at ITP Santa Barbara conference, "New dimensions in field theory and string theory": http://www.itp.ucsb.edu/online/susyc99/discussion/."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">18</subfield>
      <subfield code="h">E. Witten</subfield>
      <subfield code="t">New dimensions in field theory and string theory</subfield>
      <subfield code="u">http://www.itp.ucsb.edu/online/susyc99/discussion/</subfield>
   </datafield>
</record>""")

    def test_journal_simple(self):
        ref_line = u"""[19] D. Page and C. Pope, Commun. Math. Phys. 127 (1990) 529."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">19</subfield>
      <subfield code="h">D. Page and C. Pope</subfield>
      <subfield code="s">Commun.Math.Phys.,127,529</subfield>
   </datafield>
</record>""")

    def test_unknown_report(self):
        ref_line = u"""[20] M. Duff, B. Nilsson and C. Pope, Physics Reports 130 (1986), chapter 9."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">20</subfield>
      <subfield code="h">M. Duff, B. Nilsson and C. Pope</subfield>
   </datafield>
</record>""")

    def test_journal_volume_with_letter(self):
        ref_line = u"""[21] D. Page, Phys. Lett. B79 (1978) 235."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">21</subfield>
      <subfield code="h">D. Page</subfield>
      <subfield code="s">Phys.Lett.,B79,235</subfield>
   </datafield>
</record>""")

    def test_journal_with_hep1(self):
        ref_line = u"""[22] M. Cassidy and S. Hawking, Phys. Rev. D57 (1998) 2372, hep-th/9709066; S. Hawking, Phys. Rev. D52 (1995) 5681."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">22</subfield>
      <subfield code="h">M. Cassidy and S. Hawking</subfield>
      <subfield code="s">Phys.Rev.,D57,2372</subfield>
      <subfield code="r">hep-th/9709066</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">22</subfield>
      <subfield code="h">S. Hawking</subfield>
      <subfield code="s">Phys.Rev.,D52,5681</subfield>
   </datafield>
</record>""")

    def test_hep7(self):
        ref_line = u"""[23] K. Skenderis and S. Solodukhin, hep-th/9910023."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">23</subfield>
      <subfield code="h">K. Skenderis and S. Solodukhin</subfield>
      <subfield code="r">hep-th/9910023</subfield>
   </datafield>
</record>""")

    def test_journal_with_hep2(self):
        ref_line = u"""[24] M. Henningson and K. Skenderis, JHEP 9807:023 (1998), hep-th/9806087."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">24</subfield>
      <subfield code="h">M. Henningson and K. Skenderis</subfield>
      <subfield code="s">JHEP,9807,023</subfield>
      <subfield code="r">hep-th/9806087</subfield>
   </datafield>
</record>""")

    def test_unknown_book(self):
        ref_line = u"""[25] C. Fefferman and C. Graham, "Conformal Invariants", in Elie Cartan et les Mathematiques d'aujourd'hui (Asterisque, 1985) 95."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">25</subfield>
      <subfield code="h">C. Fefferman and C. Graham</subfield>
      <subfield code="t">Conformal Invariants</subfield>
   </datafield>
</record>""")

    def test_hep8(self):
        ref_line = u"""[27] E. Witten and S.-T. Yau, hep-th/9910245."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">27</subfield>
      <subfield code="h">E. Witten and S.-T. Yau</subfield>
      <subfield code="r">hep-th/9910245</subfield>
   </datafield>
</record>""")

    def test_hep9(self):
        ref_line = u"""[28] R. Emparan, JHEP 9906:036 (1999); hep-th/9906040."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">28</subfield>
      <subfield code="h">R. Emparan</subfield>
      <subfield code="s">JHEP,9906,036</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">28</subfield>
      <subfield code="r">hep-th/9906040</subfield>
   </datafield>
</record>""")

    def test_journal_with_hep3(self):
        ref_line = u"""[29] A. Chamblin, R. Emparan, C. Johnson and R. Myers, Phys. Rev. D59 (1999) 64010, hep-th/9808177; S. Hawking, C. Hunter and D. Page, Phys. Rev. D59 (1999) 44033, hep-th/9809035."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">29</subfield>
      <subfield code="h">A. Chamblin, R. Emparan, C. Johnson and R. Myers</subfield>
      <subfield code="s">Phys.Rev.,D59,64010</subfield>
      <subfield code="r">hep-th/9808177</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">29</subfield>
      <subfield code="h">S. Hawking, C. Hunter and D. Page</subfield>
      <subfield code="s">Phys.Rev.,D59,44033</subfield>
      <subfield code="r">hep-th/9809035</subfield>
   </datafield>
</record>""")

    def test_journal_with_hep4(self):
        ref_line = u"""[30] S. Sethi and L. Susskind, Phys. Lett. B400 (1997) 265, hep-th/9702101; T. Banks and N. Seiberg, Nucl. Phys. B497 (1997) 41, hep-th/9702187."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">30</subfield>
      <subfield code="h">S. Sethi and L. Susskind</subfield>
      <subfield code="s">Phys.Lett.,B400,265</subfield>
      <subfield code="r">hep-th/9702101</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">30</subfield>
      <subfield code="h">T. Banks and N. Seiberg</subfield>
      <subfield code="s">Nucl.Phys.,B497,41</subfield>
      <subfield code="r">hep-th/9702187</subfield>
   </datafield>
</record>""")

    def test_misc7(self):
        ref_line = u"""[31] R. Emparan, C. Johnson and R. Myers, Phys. Rev. D60 (1999) 104001; hep-th/9903238."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">31</subfield>
      <subfield code="h">R. Emparan, C. Johnson and R. Myers</subfield>
      <subfield code="s">Phys.Rev.,D60,104001</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">31</subfield>
      <subfield code="r">hep-th/9903238</subfield>
   </datafield>
</record>""")

    def test_misc8(self):
        ref_line = u"""[32] S. Hawking, C. Hunter and M. Taylor-Robinson, Phys. Rev. D59 (1999) 064005; hep-th/9811056."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">32</subfield>
      <subfield code="h">S. Hawking, C. Hunter and M. Taylor-Robinson</subfield>
      <subfield code="s">Phys.Rev.,D59,064005</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">32</subfield>
      <subfield code="r">hep-th/9811056</subfield>
   </datafield>
</record>""")

    def test_misc9(self):
        ref_line = u"""[33] J. Dowker, Class. Quant. Grav. 16 (1999) 1937; hep-th/9812202."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">33</subfield>
      <subfield code="h">J. Dowker</subfield>
      <subfield code="s">Class.Quant.Grav.,16,1937</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">33</subfield>
      <subfield code="r">hep-th/9812202</subfield>
   </datafield>
</record>""")

    def test_journal3(self):
        ref_line = u"""[34] J. Brown and J. York, Phys. Rev. D47 (1993) 1407."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">34</subfield>
      <subfield code="h">J. Brown and J. York</subfield>
      <subfield code="s">Phys.Rev.,D47,1407</subfield>
   </datafield>
</record>""")

    def test_misc10(self):
        ref_line = u"""[35] D. Freedman, S. Mathur, A. Matsuis and L. Rastelli, Nucl. Phys. B546 (1999) 96; hep-th/9804058. More text, followed by an IBID A 546 (1999) 96"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">35</subfield>
      <subfield code="h">D. Freedman, S. Mathur, A. Matsuis and L. Rastelli</subfield>
      <subfield code="s">Nucl.Phys.,B546,96</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">35</subfield>
      <subfield code="r">hep-th/9804058</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">35</subfield>
      <subfield code="s">Nucl.Phys.,A546,96</subfield>
      <subfield code="h">D. Freedman, S. Mathur, A. Matsuis and L. Rastelli</subfield>
   </datafield>
</record>""")

    def test_misc11(self):
        ref_line = u"""[36] D. Freedman, S. Mathur, A. Matsuis and L. Rastelli, Nucl. Phys. B546 (1999) 96; hep-th/9804058. More text, followed by an IBID A"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">36</subfield>
      <subfield code="h">D. Freedman, S. Mathur, A. Matsuis and L. Rastelli</subfield>
      <subfield code="s">Nucl.Phys.,B546,96</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">36</subfield>
      <subfield code="r">hep-th/9804058</subfield>
   </datafield>
</record>""")

    def test_misc12(self):
        ref_line = u"""[37] some misc  lkjslkdjlksjflksj [hep-th/9804058] lkjlkjlkjlkj [hep-th/0001567], hep-th/1212321, some more misc; Nucl. Phys. B546 (1999) 96"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">37</subfield>
      <subfield code="r">hep-th/9804058</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">37</subfield>
      <subfield code="r">hep-th/0001567</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">37</subfield>
      <subfield code="r">hep-th/1212321</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">37</subfield>
      <subfield code="s">Nucl.Phys.,B546,96</subfield>
   </datafield>
</record>""")

    def test_misc13(self):
        ref_line = u"""[38] R. Emparan, C. Johnson and R.. Myers, Phys. Rev. D60 (1999) 104001; this is :: .... misc! hep-th/9903238. and some ...,.,.,.,::: more hep-ph/9912000"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">38</subfield>
      <subfield code="h">R. Emparan, C. Johnson and R.. Myers</subfield>
      <subfield code="s">Phys.Rev.,D60,104001</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">38</subfield>
      <subfield code="r">hep-th/9903238</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">38</subfield>
      <subfield code="r">hep-ph/9912000</subfield>
   </datafield>
</record>""")

    def test_journal_with_hep5(self):
        ref_line = u"""[39] A. Ceresole, G. Dall Agata and R. D Auria, JHEP 11(1999) 009, [hep-th/9907216]."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">39</subfield>
      <subfield code="h">A. Ceresole, G. Dall Agata and R. D Auria</subfield>
      <subfield code="s">JHEP,9911,009</subfield>
      <subfield code="r">hep-th/9907216</subfield>
   </datafield>
</record>""")

    def test_journal_with_hep6(self):
        ref_line = u"""[40] D.P. Jatkar and S. Randjbar-Daemi, Phys. Lett. B460, 281 (1999) [hep-th/9904187]."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">40</subfield>
      <subfield code="h">D.P. Jatkar and S. Randjbar-Daemi</subfield>
      <subfield code="s">Phys.Lett.,B460,281</subfield>
      <subfield code="r">hep-th/9904187</subfield>
   </datafield>
</record>""")

    def test_journal_with_hep7(self):
        ref_line = u"""[41] G. DallAgata, Phys. Lett. B460, (1999) 79, [hep-th/9904198]."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">41</subfield>
      <subfield code="h">G. DallAgata</subfield>
      <subfield code="s">Phys.Lett.,B460,79</subfield>
      <subfield code="r">hep-th/9904198</subfield>
   </datafield>
</record>""")

    def test_journal_year_volume_page(self):
        ref_line = u"""[43] Becchi C., Blasi A., Bonneau G., Collina R., Delduc F., Commun. Math. Phys., 1988, 120, 121."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">43</subfield>
      <subfield code="h">Becchi C., Blasi A., Bonneau G., Collina R., Delduc F.</subfield>
      <subfield code="s">Commun.Math.Phys.,120,121</subfield>
   </datafield>
</record>""")

    def test_journal_volume_year_page1(self):
        ref_line = u"""[44]: N. Nekrasov, A. Schwarz, Instantons on noncommutative R4 and (2, 0) superconformal six-dimensional theory, Comm. Math. Phys., 198, (1998), 689-703."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">44</subfield>
      <subfield code="h">N. Nekrasov, A. Schwarz</subfield>
      <subfield code="s">Commun.Math.Phys.,198,689</subfield>
   </datafield>
</record>""")

    def test_journal_volume_year_page2(self):
        ref_line = u"""[42] S.M. Donaldson, Instantons and Geometric Invariant Theory, Comm. Math. Phys., 93, (1984), 453-460."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">42</subfield>
      <subfield code="h">S.M. Donaldson</subfield>
      <subfield code="s">Commun.Math.Phys.,93,453</subfield>
   </datafield>
</record>""")

    def test_many_references_in_one_line(self):
        ref_line = u"""[45] H. J. Bhabha, Rev. Mod. Phys. 17, 200(1945); ibid, 21, 451(1949); S. Weinberg, Phys. Rev. 133, B1318(1964); ibid, 134, 882(1964); D. L. Pursey, Ann. Phys(U. S)32, 157(1965); W. K. Tung, Phys, Rev. Lett. 16, 763(1966); Phys. Rev. 156, 1385(1967); W. J. Hurley, Phys. Rev. Lett. 29, 1475(1972)."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">45</subfield>
      <subfield code="h">H. J. Bhabha</subfield>
      <subfield code="s">Rev.Mod.Phys.,17,200</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">45</subfield>
      <subfield code="s">Rev.Mod.Phys.,21,451</subfield>
      <subfield code="h">H. J. Bhabha</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">45</subfield>
      <subfield code="h">S. Weinberg</subfield>
      <subfield code="s">Phys.Rev.,133,B1318</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">45</subfield>
      <subfield code="s">Phys.Rev.,134,882</subfield>
      <subfield code="h">S. Weinberg</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">45</subfield>
      <subfield code="h">D. L. Pursey</subfield>
      <subfield code="s">Ann.Phys.,32,157</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">45</subfield>
      <subfield code="h">W. K. Tung</subfield>
      <subfield code="s">Phys.Rev.Lett.,16,763</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">45</subfield>
      <subfield code="s">Phys.Rev.,156,1385</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">45</subfield>
      <subfield code="h">W. J. Hurley</subfield>
      <subfield code="s">Phys.Rev.Lett.,29,1475</subfield>
   </datafield>
</record>""")

    def test_ibid(self):
        ref_line = u"""[46] E. Schrodinger, Sitzungsber. Preuss. Akad. Wiss. Phys. Math. Kl. 24, 418(1930); ibid, 3, 1(1931)"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">46</subfield>
      <subfield code="h">E. Schrodinger</subfield>
      <subfield code="s">Sitzungsber.Preuss.Akad.Wiss.Berlin (Math.Phys.),24,418</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">46</subfield>
      <subfield code="s">Sitzungsber.Preuss.Akad.Wiss.Berlin (Math.Phys.),3,1</subfield>
      <subfield code="h">E. Schrodinger</subfield>
   </datafield>
</record>""")

    def test_misc4(self):
        ref_line = u"""[47] P. A. M. Dirac, Proc. R. Soc. London, Ser. A155, 447(1936); ibid, D24, 3333(1981)."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">47</subfield>
      <subfield code="h">P. A. M. Dirac</subfield>
      <subfield code="s">Proc.Roy.Soc.Lond.,A155,447</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">47</subfield>
      <subfield code="s">Proc.Roy.Soc.Lond.,D24,3333</subfield>
      <subfield code="h">P. A. M. Dirac</subfield>
   </datafield>
</record>""")

    def test_doi(self):
        ref_line = u"""[48] O.O. Vaneeva, R.O. Popovych and C. Sophocleous, Enhanced Group Analysis and Exact Solutions of Vari-able Coefficient Semilinear Diffusion Equations with a Power Source, Acta Appl. Math., doi:10.1007/s10440-008-9280-9, 46 p., arXiv:0708.3457."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">48</subfield>
      <subfield code="h">O.O. Vaneeva, R.O. Popovych and C. Sophocleous</subfield>
      <subfield code="a">10.1007/s10440-008-9280-9</subfield>
      <subfield code="r">arXiv:0708.3457</subfield>
   </datafield>
</record>""")

    def test_misc3(self):
        ref_line = u"""[49] M. I. Trofimov, N. De Filippis and E. A. Smolenskii. Application of the electronegativity indices of organic molecules to tasks of chemical informatics. Russ. Chem. Bull., 54:2235-2246, 2005. http://dx.doi.org/10.1007/s11172-006-0105-6."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">49</subfield>
      <subfield code="h">M. I. Trofimov, N. De Filippis and E. A. Smolenskii</subfield>
      <subfield code="a">10.1007/s11172-006-0105-6</subfield>
   </datafield>
</record>""")

    def test_misc2(self):
        ref_line = u"""[50] M. Gell-Mann, P. Ramon ans R. Slansky, in Supergravity, P. van Niewenhuizen and D. Freedman (North-Holland 1979); T. Yanagida, in Proceedings of the Workshop on the Unified Thoery and the Baryon Number in teh Universe, ed. O. Sawaga and A. Sugamoto (Tsukuba 1979); R.N. Mohapatra and G. Senjanovic, Phys. Rev. Lett. 44, 912, (1980)."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">50</subfield>
      <subfield code="h">M. Gell-Mann, P. Ramon ans R. Slansky</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">50</subfield>
      <subfield code="h">P. van Niewenhuizen and D. Freedman</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">50</subfield>
      <subfield code="h">T. Yanagida (O. Sawaga and A. Sugamoto (eds.))</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">50</subfield>
      <subfield code="h">R.N. Mohapatra and G. Senjanovic</subfield>
      <subfield code="s">Phys.Rev.Lett.,44,912</subfield>
   </datafield>
</record>""")

    def test_misc1(self):
        ref_line = u"""[51] L.S. Durkin and P. Langacker, Phys. Lett B166, 436 (1986); Amaldi et al., Phys. Rev. D36, 1385 (1987); Hayward and Yellow et al., eds. Phys. Lett B245, 669 (1990); Nucl. Phys. B342, 15 (1990);"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">51</subfield>
      <subfield code="h">L.S. Durkin and P. Langacker</subfield>
      <subfield code="s">Phys.Lett.,B166,436</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">51</subfield>
      <subfield code="h">Amaldi et al.</subfield>
      <subfield code="s">Phys.Rev.,D36,1385</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">51</subfield>
      <subfield code="h">(Hayward and Yellow et al. (eds.))</subfield>
      <subfield code="s">Phys.Lett.,B245,669</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">51</subfield>
      <subfield code="s">Nucl.Phys.,B342,15</subfield>
   </datafield>
</record>""")

    def test_combination_of_authors_names(self):
        """authors names in varied formats"""
        ref_line = u"""[53] Hush, D.R., R.Leighton, and B.G. Horne, 1993. "Progress in supervised Neural Netw. What's new since Lippmann?" IEEE Signal Process. Magazine 10, 8-39"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">53</subfield>
      <subfield code="h">Hush, D.R., R.Leighton, and B.G. Horne</subfield>
      <subfield code="t">Progress in supervised Neural Netw. What's new since Lippmann?</subfield>
   </datafield>
</record>""")

    def test_two_initials_no_space(self):
        ref_line = u"""[54] T.G. Rizzo, Phys. Rev. D40, 3035 (1989)"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">54</subfield>
      <subfield code="h">T.G. Rizzo</subfield>
      <subfield code="s">Phys.Rev.,D40,3035</subfield>
   </datafield>
</record>""")

    def test_surname_prefix_van(self):
        """An author with prefix + surname
        e.g. van Niewenhuizen"""
        ref_line = u"""[55] Hawking S., P. van Niewenhuizen, L.S. Durkin, D. Freeman, some title of some journal"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">55</subfield>
      <subfield code="h">Hawking S., P. van Niewenhuizen, L.S. Durkin, D. Freeman</subfield>
   </datafield>
</record>""")

    def test_authors_coma_but_no_journal(self):
        """2 authors separated by coma"""
        ref_line = u"""[56] Hawking S., D. Freeman, some title of some journal"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">56</subfield>
      <subfield code="h">Hawking S., D. Freeman</subfield>
   </datafield>
</record>""")

    def test_authors_and_but_no_journal(self):
        """2 authors separated by "and" """
        ref_line = u"""[57] Hawking S. and D. Freeman, another random title of some random journal"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">57</subfield>
      <subfield code="h">Hawking S. and D. Freeman</subfield>
   </datafield>
</record>""")

    def test_simple_et_al(self):
        """author ending with et al."""
        ref_line = u"""[1] Amaldi et al., Phys. Rev. D36, 1385 (1987)"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">1</subfield>
      <subfield code="h">Amaldi et al.</subfield>
      <subfield code="s">Phys.Rev.,D36,1385</subfield>
   </datafield>
</record>""")

    def test_ibidem(self):
        """IBIDEM test

        ibidem must copy the previous reference journal and not
        the first one
        """
        ref_line = u"""[58] Nucl. Phys. B342, 15 (1990); Phys. Lett. B261, 146 (1991); ibidem B263, 459 (1991);"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">58</subfield>
      <subfield code="s">Nucl.Phys.,B342,15</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">58</subfield>
      <subfield code="s">Phys.Lett.,B261,146</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">58</subfield>
      <subfield code="s">Phys.Lett.,B263,459</subfield>
   </datafield>
</record>""")

    def test_collaboration(self):
        """collabration"""
        ref_line = u"""[60] HERMES Collaboration, Airapetian A et al. 2005 Phys. Rev. D 71 012003 1-36"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">60</subfield>
      <subfield code="h">(HERMES Collaboration) Airapetian A et al.</subfield>
      <subfield code="s">Phys.Rev.D,71,012003</subfield>
   </datafield>
</record>""")

    def test_weird_number_after_volume(self):
        ref_line = u"""[61] de Florian D, Sassot R and Stratmann M 2007 Phys. Rev. D 75 114010 1-26"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">61</subfield>
      <subfield code="h">de Florian D, Sassot R and Stratmann M</subfield>
      <subfield code="s">Phys.Rev.D,75,114010</subfield>
   </datafield>
</record>""")

    def test_year_before_journal(self):
        ref_line = u"""[64] Bourrely C, Soffer J and Buccella F 2002 Eur. Phys. J. C 23 487-501"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">64</subfield>
      <subfield code="h">Bourrely C, Soffer J and Buccella F</subfield>
      <subfield code="s">Eur.Phys.J.C,23,487</subfield>
   </datafield>
</record>""")

    def test_non_recognized_reference(self):
        ref_line = u"""[63] Z. Guzik and R. Jacobsson, LHCb Readout Supervisor ’ODIN’ with a L1\nTrigger - Technical reference, Aug 2005, EDMS 704078-V1.0"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">63</subfield>
      <subfield code="h">Z. Guzik and R. Jacobsson</subfield>
   </datafield>
</record>""")

    def test_year_stuck_to_volume(self):
        ref_line = u"""[65] K. Huang, Am. J. Phys. 20, 479(1952)"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">65</subfield>
      <subfield code="h">K. Huang</subfield>
      <subfield code="s">Am.J.Phys.,20,479</subfield>
   </datafield>
</record>""")

    def test_two_initials_after_surname(self):
        """Author with 2 initials
        e.g. Pate S. F."""
        ref_line = u"""[62] Pate S. F., McKee D. W. and Papavassiliou V. 2008 Phys.Rev. C 78 448"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">62</subfield>
      <subfield code="h">Pate S. F., McKee D. W. and Papavassiliou V.</subfield>
      <subfield code="s">Phys.Rev.,C78,448</subfield>
   </datafield>
</record>""")

    def test_one_initial_after_surname(self):
        """Author with 1 initials
        e.g. Pate S."""
        ref_line = u"""[62] Pate S., McKee D., 2008 Phys.Rev. C 78 448"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">62</subfield>
      <subfield code="h">Pate S., McKee D.</subfield>
      <subfield code="s">Phys.Rev.,C78,448</subfield>
   </datafield>
</record>""")

    def test_two_initials_no_dot_after_surname(self):
        """Author with 2 initials
        e.g. Pate S F"""
        ref_line = u"""[62] Pate S F, McKee D W and Papavassiliou V 2008 Phys.Rev. C 78 448"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">62</subfield>
      <subfield code="h">Pate S F, McKee D W and Papavassiliou V</subfield>
      <subfield code="s">Phys.Rev.,C78,448</subfield>
   </datafield>
</record>""")

    def test_one_initial_no_dot_after_surname(self):
        """Author with 1 initials
        e.g. Pate S"""
        ref_line = u"""[62] Pate S, McKee D, 2008 Phys.Rev. C 78 448"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">62</subfield>
      <subfield code="h">Pate S, McKee D</subfield>
      <subfield code="s">Phys.Rev.,C78,448</subfield>
   </datafield>
</record>""")

    def test_two_initials_before_surname(self):
        ref_line = u"""[67] G. A. Perkins, Found. Phys. 6, 237(1976)"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">67</subfield>
      <subfield code="h">G. A. Perkins</subfield>
      <subfield code="s">Found.Phys.,6,237</subfield>
   </datafield>
</record>""")

    def test_one_initial_before_surname(self):
        ref_line = u"""[67] G. Perkins, Found. Phys. 6, 237(1976)"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">67</subfield>
      <subfield code="h">G. Perkins</subfield>
      <subfield code="s">Found.Phys.,6,237</subfield>
   </datafield>
</record>""")

    def test_two_initials_no_dot_before_surname(self):
        ref_line = u"""[67] G A Perkins, Found. Phys. 6, 237(1976)"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">67</subfield>
      <subfield code="h">G A Perkins</subfield>
      <subfield code="s">Found.Phys.,6,237</subfield>
   </datafield>
</record>""")

    def test_one_initial_no_dot_before_surname(self):
        ref_line = u"""[67] G Perkins, Found. Phys. 6, 237(1976)"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">67</subfield>
      <subfield code="h">G Perkins</subfield>
      <subfield code="s">Found.Phys.,6,237</subfield>
   </datafield>
</record>""")

    def test_ibid_twice(self):
        ref_line = u"""[68] A. O. Barut et al, Phys. Rev. D23, 2454(1981); ibid, D24, 3333(1981); ibid, D31, 1386(1985)"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">68</subfield>
      <subfield code="h">A. O. Barut et al.</subfield>
      <subfield code="s">Phys.Rev.,D23,2454</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">68</subfield>
      <subfield code="s">Phys.Rev.,D24,3333</subfield>
      <subfield code="h">A. O. Barut et al.</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">68</subfield>
      <subfield code="s">Phys.Rev.,D31,1386</subfield>
      <subfield code="h">A. O. Barut et al.</subfield>
   </datafield>
</record>""")

    def test_no_authors(self):
        ref_line = u"""[69] Phys. Rev. Lett. 52, 2009(1984)"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">69</subfield>
      <subfield code="s">Phys.Rev.Lett.,52,2009</subfield>
   </datafield>
</record>""")

    def test_extra_01(self):
        "Parsed erroniously as Phys.Rev.Lett.,101,01"
        ref_line = u"""[17] de Florian D, Sassot R, Stratmann M and Vogelsang W 2008 Phys. Rev. Lett. 101 072001 1-4; 2009 Phys.
Rev. D 80 034030 1-25"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">17</subfield>
      <subfield code="h">de Florian D, Sassot R, Stratmann M and Vogelsang W</subfield>
      <subfield code="s">Phys.Rev.Lett.,101,072001</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">17</subfield>
      <subfield code="s">Phys.Rev.D,80,034030</subfield>
   </datafield>
</record>""")

    def test_extra_no_after_vol(self):
        ref_line = u"""[130] A. Kuper, H. Letaw, L. Slifkin, E-Sonder, and C. T. Tomizuka, “Self- diffusion in copper,” Physical Review, vol. 96, no. 5, pp. 1224–1225, 1954."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">130</subfield>
      <subfield code="h">A. Kuper, H. Letaw, L. Slifkin, E-Sonder, and C. T. Tomizuka</subfield>
      <subfield code="t">Self- diffusion in copper</subfield>
      <subfield code="s">Phys.Rev.,96,1224</subfield>
   </datafield>
</record>""")

    def test_jinst(self):
        ref_line = u"""[1] ATLAS Collaboration, G. Aad et al., The ATLAS Experiment at the CERN Large Hadron Collider, JINST 3 (2008) S08003."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">1</subfield>
      <subfield code="h">(ATLAS Collaboration) G. Aad et al.</subfield>
      <subfield code="s">JINST,0803,S08003</subfield>
   </datafield>
</record>""")

    def test_collaboration2(self):
        ref_line = u"""[28] Particle Data Group Collaboration, K. Nakamura et al., Review of particle physics, J. Phys. G37 (2010) 075021."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">28</subfield>
      <subfield code="h">(Particle Data Group Collaboration) K. Nakamura et al.</subfield>
      <subfield code="s">J.Phys.,G37,075021</subfield>
   </datafield>
</record>""")

    def test_sub_volume(self):
        ref_line = u"""[8] S. Horvat, D. Khartchenko, O. Kortner, S. Kotov, H. Kroha, A. Manz, S. Mohrdieck-Mock, K. Nikolaev, R. Richter, W. Stiller, C. Valderanis, J. Dubbert, F. Rauscher, and A. Staude, Operation of the ATLAS muon drift-tube chambers at high background rates and in magnetic fields, IEEE Trans. Nucl. Sci. 53 (2006) no. 2, 562–566"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">8</subfield>
      <subfield code="h">S. Horvat, D. Khartchenko, O. Kortner, S. Kotov, H. Kroha, A. Manz, S. Mohrdieck-Mock, K. Nikolaev, R. Richter, W. Stiller, C. Valderanis, J. Dubbert, F. Rauscher, and A. Staude</subfield>
      <subfield code="s">IEEE Trans.Nucl.Sci.,53,562</subfield>
   </datafield>
</record>""")

    def test_journal_not_recognized(self):
        ref_line = u"""[33] A. Moraes, C. Buttar, and I. Dawson, Prediction for minimum bias and the underlying event at LHC energies, The European Physical Journal C - Particles and Fields 50 (2007) 435–466."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">33</subfield>
      <subfield code="h">A. Moraes, C. Buttar, and I. Dawson</subfield>
      <subfield code="s">Eur.Phys.J.C,50,435</subfield>
   </datafield>
</record>""")

    def test_multiple_eds(self):
        ref_line = u"""[7] L. Evans, (ed.) and P. Bryant, (ed.), LHC Machine, JINST 3 (2008) S08001."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">7</subfield>
      <subfield code="h">L. Evans, (ed.) and P. Bryant, (ed.)</subfield>
      <subfield code="s">JINST,0803,S08001</subfield>
   </datafield>
</record>""")

    def test_atlas_conf(self):
        """not recognizing preprint format"""
        ref_line = u"""[32] The ATLAS Collaboration, Charged particle multiplicities in pp interactions at √s = 0.9 and 7 TeV in a diffractive limited phase space measured with the ATLAS detector at the LHC and a new pythia6 tune, 2010. http://cdsweb.cern.ch/record/1266235/files/ ATLAS-COM-CONF-2010-031.pdf. ATLAS-CONF-2010-031."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">32</subfield>
      <subfield code="h">(The ATLAS Collaboration)</subfield>
      <subfield code="u">http://cdsweb.cern.ch/record/1266235/files/ATLAS-COM-CONF-2010-031.pdf</subfield>
      <subfield code="r">ATL-CONF-2010-031</subfield>
   </datafield>
</record>""")

    def test_journal_of_physics(self):
        """eventually not recognizing the journal, the collaboration or authors"""
        ref_line = u"""[19] ATLAS Inner Detector software group Collaboration, T. Cornelissen, M. Elsing, I. Gavilenko, W. Liebig, E. Moyse, and A. Salzburger, The new ATLAS Track Reconstruction (NEWT), Journal of Physics 119 (2008) 032014."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">19</subfield>
      <subfield code="h">(ATLAS Inner Detector software group Collaboration) T. Cornelissen, M. Elsing, I. Gavilenko, W. Liebig, E. Moyse, and A. Salzburger</subfield>
      <subfield code="s">J.Phys.,119,032014</subfield>
   </datafield>
</record>""")

    def test_jhep(self):
        """was splitting JHEP in JHE: P"""
        ref_line = u"""[22] G. P. Salam and G. Soyez, A practical seedless infrared-safe cone jet algorithm, JHEP 05 (2007) 086."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">22</subfield>
      <subfield code="h">G. P. Salam and G. Soyez</subfield>
      <subfield code="s">JHEP,0705,086</subfield>
   </datafield>
</record>""")

    def test_journal_not_recognized2(self):
        ref_line = u"""[3] Physics Performance Report Vol 1 – J. Phys. G. Vol 30 N° 11 (2004)"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">3</subfield>
      <subfield code="s">J.Phys.G,30,1</subfield>
   </datafield>
</record>""")

    def test_journal_not_recognized3(self):
        ref_line = u"""[128] D. P. Pritzkau and R. H. Siemann, “Experimental study of rf pulsed heat- ing on oxygen free electronic copper,” Physical Review Special Topics - Accelerators and Beams, vol. 5, pp. 1–22, 2002."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">128</subfield>
      <subfield code="h">D. P. Pritzkau and R. H. Siemann</subfield>
      <subfield code="t">Experimental study of rf pulsed heat- ing on oxygen free electronic copper</subfield>
      <subfield code="s">Phys.Rev.ST Accel.Beams,5,1</subfield>
   </datafield>
</record>""")

    def test_note_format1(self):
        ref_line = u"""[91] S. Calatroni, H. Neupert, and M. Taborelli, “Fatigue testing of materials by UV pulsed laser irradiation,” CLIC Note 615, CERN, 2004."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">91</subfield>
      <subfield code="h">S. Calatroni, H. Neupert, and M. Taborelli</subfield>
      <subfield code="t">Fatigue testing of materials by UV pulsed laser irradiation</subfield>
      <subfield code="r">CERN-CLIC-Note-615</subfield>
   </datafield>
</record>""")

    def test_note_format2(self):
        ref_line = u"""[5] H. Braun, R. Corsini, J. P. Delahaye, A. de Roeck, S. Dbert, A. Ferrari, G. Geschonke, A. Grudiev, C. Hauviller, B. Jeanneret, E. Jensen, T. Lefvre, Y. Papaphilippou, G. Riddone, L. Rinolfi, W. D. Schlatter, H. Schmickler, D. Schulte, I. Syratchev, M. Taborelli, F. Tecker, R. Toms, S. Weisz, and W. Wuensch, “CLIC 2008 parameters,” tech. rep., CERN CLIC-Note-764, Oct 2008."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">5</subfield>
      <subfield code="h">H. Braun, R. Corsini, J. P. Delahaye, A. de Roeck, S. Dbert, A. Ferrari, G. Geschonke, A. Grudiev, C. Hauviller, B. Jeanneret, E. Jensen, T. Lefvre, Y. Papaphilippou, G. Riddone, L. Rinolfi, W. D. Schlatter, H. Schmickler, D. Schulte, I. Syratchev, M. Taborelli, F. Tecker, R. Toms, S. Weisz, and W. Wuensch</subfield>
      <subfield code="t">CLIC 2008 parameters</subfield>
      <subfield code="r">CERN-CLIC-Note-764</subfield>
   </datafield>
</record>""")

    def test_remove_empty_misc_tag(self):
        ref_line = u"""[21] “http://www.linearcollider.org/.”"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">21</subfield>
      <subfield code="u">http://www.linearcollider.org/</subfield>
   </datafield>
</record>""", ignore_misc=False)

    def test_sub_volume_not_recognized(self):
        ref_line = u"""[37] L. Lu, Y. Shen, X. Chen, L. Qian, and K. Lu, “Ultrahigh strength and high electrical conductivity in copper,” Science, vol. 304, no. 5669, pp. 422–426, 2004."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">37</subfield>
      <subfield code="h">L. Lu, Y. Shen, X. Chen, L. Qian, and K. Lu</subfield>
      <subfield code="t">Ultrahigh strength and high electrical conductivity in copper</subfield>
      <subfield code="s">Science,304,422</subfield>
   </datafield>
</record>""")

    def test_extra_a_after_journal(self):
        ref_line = u"""[28] Particle Data Group Collaboration, K. Nakamura et al., Review of particle physics, J. Phys. G37 (2010) 075021."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">28</subfield>
      <subfield code="h">(Particle Data Group Collaboration) K. Nakamura et al.</subfield>
      <subfield code="s">J.Phys.,G37,075021</subfield>
   </datafield>
</record>""")

    def test_full_month_with_volume(self):
        ref_line = u"""[2] C. Rubbia, Experimental observation of the intermediate vector bosons W+, W−, and Z0, Reviews of Modern Physics 57 (July, 1985) 699–722."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">2</subfield>
      <subfield code="h">C. Rubbia</subfield>
      <subfield code="s">Rev.Mod.Phys.,57,699</subfield>
   </datafield>
</record>""")

    def test_wrong_replacement(self):
        """Wrong replacement

        A. J. Hey, Gauge by Astron.J. Hey
        """
        ref_line = u"""[5] I. J. Aitchison and A. J. Hey, Gauge Theories in Particle Physics, Vol II: QCD and the Electroweak Theory. CRC Pr I Llc, 2003."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">5</subfield>
      <subfield code="h">I. J. Aitchison and A. J. Hey</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">5</subfield>
      <subfield code="h">I Llc</subfield>
   </datafield>
</record>""")

    def test_author_replacement(self):
        ref_line = u"""[48] D. Adams, S. Asai, D. Cavalli, M. Du ̈hrssen, K. Edmonds, S. Elles, M. Fehling, U. Felzmann, L. Gladilin, L. Helary, M. Hohlfeld, S. Horvat, K. Jakobs, M. Kaneda, G. Kirsch, S. Kuehn, J. F. Marchand, C. Pizio, X. Portell, D. Rebuzzi, E. Schmidt, A. Shibata, I. Vivarelli, S. Winkelmann, and S. Yamamoto, The ATLFAST-II performance in release 14 -particle signatures and selected benchmark processes-, Tech. Rep. ATL-PHYS-INT-2009-110, CERN, Geneva, Dec, 2009."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">48</subfield>
      <subfield code="h">D. Adams, S. Asai, D. Cavalli, M. D\xfchrssen, K. Edmonds, S. Elles, M. Fehling, U. Felzmann, L. Gladilin, L. Helary, M. Hohlfeld, S. Horvat, K. Jakobs, M. Kaneda, G. Kirsch, S. Kuehn, J. F. Marchand, C. Pizio, X. Portell, D. Rebuzzi, E. Schmidt, A. Shibata, I. Vivarelli, S. Winkelmann, and S. Yamamoto</subfield>
      <subfield code="r">ATL-PHYS-INT-2009-110</subfield>
   </datafield>
</record>""")

    def test_author_not_recognized1(self):
        ref_line = u"""[7] Pod I., C. Jennings, et al, etc., Nucl. Phys. B342, 15 (1990)"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">7</subfield>
      <subfield code="h">Pod I., C. Jennings, et al.</subfield>
      <subfield code="s">Nucl.Phys.,B342,15</subfield>
   </datafield>
</record>""")

    def test_title_comma(self):
        ref_line = u"""[24] R. Downing et al., Nucl. Instrum. Methods, A570, 36 (2007)."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">24</subfield>
      <subfield code="h">R. Downing et al.</subfield>
      <subfield code="s">Nucl.Instrum.Meth.,A570,36</subfield>
   </datafield>
</record>""")

    def test_author1(self):
        ref_line = u"""[43] L.S. Durkin and P. Langacker, Phys. Lett B166, 436 (1986); Amaldi et al., Phys. Rev. D36, 1385 (1987); Hayward and Yellow et al., Phys. Lett B245, 669 (1990); Nucl. Phys. B342, 15 (1990);"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">43</subfield>
      <subfield code="h">L.S. Durkin and P. Langacker</subfield>
      <subfield code="s">Phys.Lett.,B166,436</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">43</subfield>
      <subfield code="h">Amaldi et al.</subfield>
      <subfield code="s">Phys.Rev.,D36,1385</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">43</subfield>
      <subfield code="h">Hayward and Yellow et al.</subfield>
      <subfield code="s">Phys.Lett.,B245,669</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">43</subfield>
      <subfield code="s">Nucl.Phys.,B342,15</subfield>
   </datafield>
</record>""")

    def test_author2(self):
        ref_line = u"""[15] Nucl. Phys., B372, 3 (1992); T.G. Rizzo, Phys. Rev. D40, 3035 (1989); Proceedings of the 1990 Summer Study on High Energy Physics. ed E. Berger, June 25-July 13, 1990, Snowmass Colorado (World Scientific, Singapore, 1992) p. 233; V. Barger, J.L. Hewett and T.G. Rizzo, Phys. Rev. D42, 152 (1990); J.L. Hewett, Phys. Lett. B238, 98 (1990)"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">15</subfield>
      <subfield code="s">Nucl.Phys.,B372,3</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">15</subfield>
      <subfield code="h">T.G. Rizzo</subfield>
      <subfield code="s">Phys.Rev.,D40,3035</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">15</subfield>
      <subfield code="h">(E. Berger (eds.))</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">15</subfield>
      <subfield code="h">V. Barger, J.L. Hewett and T.G. Rizzo</subfield>
      <subfield code="s">Phys.Rev.,D42,152</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">15</subfield>
      <subfield code="h">J.L. Hewett</subfield>
      <subfield code="s">Phys.Lett.,B238,98</subfield>
   </datafield>
</record>""")

    def test_extra_blank_reference(self):
        ref_line = u"""[26] U. Gursoy and E. Kiritsis, “Exploring improved holographic theories for QCD: Part I,” JHEP 0802 (2008) 032 [ArXiv:0707.1324][hep-th]; U. Gursoy, E. Kiritsis and F. Nitti, “Exploring improved holographic theories for QCD: Part II,” JHEP 0802 (2008) 019 [ArXiv:0707.1349][hep-th];"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">26</subfield>
      <subfield code="h">U. Gursoy and E. Kiritsis</subfield>
      <subfield code="t">Exploring improved holographic theories for QCD Part I</subfield>
      <subfield code="s">JHEP,0802,032</subfield>
      <subfield code="r">arXiv:0707.1324</subfield>
   </datafield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">26</subfield>
      <subfield code="h">U. Gursoy, E. Kiritsis and F. Nitti</subfield>
      <subfield code="t">Exploring improved holographic theories for QCD Part II</subfield>
      <subfield code="s">JHEP,0802,019</subfield>
      <subfield code="r">arXiv:0707.1349</subfield>
   </datafield>
</record>""")

    def test_invalid_author(self):
        """used to detected invalid author as at Finite T"""
        ref_line = u"""[23] A. Taliotis, “qq ̄ Potential at Finite T and Weak Coupling in N = 4,” Phys. Rev. C83, 045204 (2011). [ArXiv:1011.6618][hep-th]."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">23</subfield>
      <subfield code="h">A. Taliotis</subfield>
      <subfield code="t">qq \u0304 Potential at Finite T and Weak Coupling in N = 4</subfield>
      <subfield code="s">Phys.Rev.,C83,045204</subfield>
      <subfield code="r">arXiv:1011.6618</subfield>
   </datafield>
</record>""")

    def test_split_arxiv(self):
        """used to split arxiv reference from its reference"""
        ref_line = u"""[18] A. Taliotis, “DIS from the AdS/CFT correspondence,” Nucl. Phys. A830, 299C-302C (2009). [ArXiv:0907.4204][hep-th]."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">18</subfield>
      <subfield code="h">A. Taliotis</subfield>
      <subfield code="t">DIS from the AdS/CFT correspondence</subfield>
      <subfield code="s">Nucl.Phys.,A830,299C</subfield>
      <subfield code="r">arXiv:0907.4204</subfield>
   </datafield>
</record>""")

    def test_report_without_dash(self):
        ref_line = u"""[20] G. Duckeck et al., “ATLAS computing: Technical design report,” CERN-LHCC2005-022."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">20</subfield>
      <subfield code="h">G. Duckeck et al.</subfield>
      <subfield code="t">ATLAS computing Technical design report</subfield>
      <subfield code="r">CERN-LHCC-2005-022</subfield>
   </datafield>
</record>""")

    def test_report_with_slashes(self):
        ref_line = u"""[20] G. Duckeck et al., “ATLAS computing: Technical design report,” CERN/LHCC/2005-022."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">20</subfield>
      <subfield code="h">G. Duckeck et al.</subfield>
      <subfield code="t">ATLAS computing Technical design report</subfield>
      <subfield code="r">CERN-LHCC-2005-022</subfield>
   </datafield>
</record>""")

    def test_ed_before_et_al(self):
        ref_line = u"""[20] G. Duckeck, (ed. ) et al., “ATLAS computing: Technical design report,” CERN-LHCC-2005-022."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">20</subfield>
      <subfield code="h">G. Duckeck, (ed.) et al.</subfield>
      <subfield code="t">ATLAS computing Technical design report</subfield>
      <subfield code="r">CERN-LHCC-2005-022</subfield>
   </datafield>
</record>""")

    def test_journal_but_no_page(self):
        ref_line = u"""[20] G. Duckeck, “ATLAS computing: Technical design report,” JHEP,03,1988"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">20</subfield>
      <subfield code="h">G. Duckeck</subfield>
      <subfield code="t">ATLAS computing Technical design report</subfield>
      <subfield code="s">JHEP,8803,1</subfield>
   </datafield>
</record>""")

    def test_isbn1(self):
        ref_line = u"""[22] B. Crowell, Vibrations and Waves. www.lightandmatter.com, 2009. ISBN 0-9704670-3-6."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">22</subfield>
      <subfield code="h">B. Crowell</subfield>
      <subfield code="i">0-9704670-3-6</subfield>
   </datafield>
</record>""")

    def test_isbn2(self):
        ref_line = u"""[119] D. E. Gray, American Institute of Physics Handbook. Mcgraw-Hill, 3rd ed., 1972. ISBN 9780070014855."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">119</subfield>
      <subfield code="h">D. E. Gray</subfield>
      <subfield code="i">9780070014855</subfield>
   </datafield>
</record>""")

    def test_book(self):
        ref_line = u"""[1] D. Griffiths, “Introduction to elementary particles,” Weinheim, USA: Wiley-VCH (2008) 454 p."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">1</subfield>
      <subfield code="h">D. Griffiths</subfield>
      <subfield code="t">Introduction to elementary particles</subfield>
      <subfield code="xbook" />
   </datafield>
</record>""")

    def test_complex_arxiv(self):
        ref_line = u"""[4] J.Prat, arXiv:1012.3675v1 [physics.ins-det]"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">4</subfield>
      <subfield code="h">J.Prat</subfield>
      <subfield code="r">arXiv:1012.3675 [physics.ins-det]</subfield>
   </datafield>
</record>""")

    def test_new_arxiv(self):
        ref_line = u"""[178] D. R. Tovey, On measuring the masses of pair-produced semi-invisibly decaying particles at hadron colliders, JHEP 04 (2008) 034, [0802.2879]."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">178</subfield>
      <subfield code="h">D. R. Tovey</subfield>
      <subfield code="s">JHEP,0804,034</subfield>
      <subfield code="r">arXiv:0802.2879</subfield>
   </datafield>
</record>""")

    def test_unrecognized_author(self):
        ref_line = u"""[27] B. Feng, Y. -H. He, P. Fre', "On correspondences between toric singularities and (p,q) webs," Nucl. Phys. B701 (2004) 334-356. [hep-th/0403133]"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">27</subfield>
      <subfield code="h">B. Feng, Y. -H. He, P. Fre'</subfield>
      <subfield code="t">On correspondences between toric singularities and (p,q) webs</subfield>
      <subfield code="s">Nucl.Phys.,B701,334</subfield>
      <subfield code="r">hep-th/0403133</subfield>
   </datafield>
</record>""")

    def test_unrecognized_author2(self):
        ref_line = u"""[75] J. M. Figueroa-O’Farrill, J. M. Figueroa-O'Farrill, C. M. Hull and B. J. Spence, "Branes at conical singularities and holography," Adv. Theor. Math. Phys. 2, 1249 (1999) [arXiv:hep-th/9808014]"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">75</subfield>
      <subfield code="h">J. M. Figueroa-O’Farrill, J. M. Figueroa-O'Farrill, C. M. Hull and B. J. Spence</subfield>
      <subfield code="t">Branes at conical singularities and holography</subfield>
      <subfield code="s">Adv.Theor.Math.Phys.,2,1249</subfield>
      <subfield code="r">hep-th/9808014</subfield>
   </datafield>
</record>""")

    def test_pos(self):
        ref_line = u"""[23] M. A. Donnellan, et al., PoS LAT2007 (2007) 369."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">23</subfield>
      <subfield code="h">M. A. Donnellan, et al.</subfield>
      <subfield code="s">PoS,LAT2007,369</subfield>
   </datafield>
</record>""")

    def test_complex_author(self):
        ref_line = u"""[39] Michael E. Peskin, Michael E. Peskin and Michael E. Peskin “An Introduction To Quantum Field Theory,” Westview Press, 1995."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">39</subfield>
      <subfield code="h">Michael E. Peskin, Michael E. Peskin and Michael E. Peskin</subfield>
      <subfield code="t">An Introduction To Quantum Field Theory</subfield>
   </datafield>
</record>""")

    def test_complex_author2(self):
        ref_line = u"""[39] Dan V. Schroeder, Dan V. Schroeder and Dan V. Schroeder “An Introduction To Quantum Field Theory,” Westview Press, 1995."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">39</subfield>
      <subfield code="h">Dan V. Schroeder, Dan V. Schroeder and Dan V. Schroeder</subfield>
      <subfield code="t">An Introduction To Quantum Field Theory</subfield>
   </datafield>
</record>""")

    def test_dan_journal(self):
        ref_line = u"""[39] Michael E. Peskin and Dan V. Schroeder “An Introduction To Quantum Field Theory,” Westview Press, 1995."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">39</subfield>
      <subfield code="h">Michael E. Peskin and Dan V. Schroeder</subfield>
      <subfield code="t">An Introduction To Quantum Field Theory</subfield>
   </datafield>
</record>""")

    def test_dan_journal2(self):
        ref_line = u"""[39] Dan V. Schroeder DAN B701 (2004) 334-356"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">39</subfield>
      <subfield code="h">Dan V. Schroeder</subfield>
      <subfield code="s">Dokl.Akad.Nauk Ser.Fiz.,B701,334</subfield>
   </datafield>
</record>""")

    def test_query_in_url(self):
        ref_line = u"""[69] ATLAS Collaboration. Mutag. http://indico.cern.ch/getFile.py/access?contribId=9&resId=1&materialId=slides&confId=35502"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">69</subfield>
      <subfield code="h">(ATLAS Collaboration)</subfield>
      <subfield code="u">http://indico.cern.ch/getFile.py/access?contribId=9&amp;resId=1&amp;materialId=slides&amp;confId=35502</subfield>
   </datafield>
</record>""")

    def test_volume_colon_page(self):
        ref_line = u"""[77] J. M. Butterworth et al. Multiparton interactions in photoproduction at hera. Z.Phys.C72:637-646,1996."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">77</subfield>
      <subfield code="h">J. M. Butterworth et al.</subfield>
      <subfield code="s">Z.Phys.,C72,637</subfield>
   </datafield>
</record>""")

    def test_no_spaces_numeration(self):
        ref_line = u"""[1] I.M. Gregor et al, Optical links for the ATLAS SCT and Pixel detector, Z.Phys. 465(2001)131-134"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">1</subfield>
      <subfield code="h">I.M. Gregor et al.</subfield>
      <subfield code="s">Z.Phys.,465,131</subfield>
   </datafield>
</record>""")


    def test_dot_after_year(self):
        ref_line = u"""[1] Neutrino Mass and New Physics, Phys.Rev. 2006. 56:569-628"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">1</subfield>
      <subfield code="s">Phys.Rev.,56,569</subfield>
   </datafield>
</record>""")

    def test_journal_roman(self):
        ref_line = u"""[19] D. Page and C. Pope, Commun. Math. Phys. VI (1990) 529."""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">19</subfield>
      <subfield code="h">D. Page and C. Pope</subfield>
      <subfield code="s">Commun.Math.Phys.,6,529</subfield>
   </datafield>
</record>""")

    def test_journal_phys_rev_d(self):
        ref_line = u"""[6] Sivers D. W., Phys. Rev.D, 41 (1990) 83"""
        reference_test(self, ref_line, u"""<record>
   <controlfield tag="001">1</controlfield>
   <datafield tag="999" ind1="C" ind2="5">
      <subfield code="o">6</subfield>
      <subfield code="h">Sivers D. W.</subfield>
      <subfield code="s">Phys.Rev.D,41,83</subfield>
   </datafield>
</record>""")


if __name__ == '__main__':
    test_suite = make_test_suite(RefextractTest)
    run_test_suite(test_suite)
