# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2008, 2010, 2011 CERN.
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

"""Unit tests for messages library."""

__revision__ = "$Id$"

import unittest
import messages

from invenio.config import CFG_SITE_LANG, CFG_SITE_LANGS
from invenio.testutils import make_test_suite, run_test_suite

class MessagesLanguageTest(unittest.TestCase):
    """
    Testing language-related functions
    """

    def test_lang_list_long_ordering(self):
        """messages - preserving language order"""
        lang_list_long = messages.language_list_long()

        # Preliminary test: same number of languages in both lists
        self.assertEqual(len(lang_list_long),
                         len(CFG_SITE_LANGS))


        for lang, cfg_lang in zip(lang_list_long,
                                  CFG_SITE_LANGS):
            self.assertEqual(lang[0],
                             cfg_lang)

    def test_wash_invalid_language(self):
        """messages - washing invalid language code"""
        self.assertEqual(messages.wash_language('python'),
                         CFG_SITE_LANG)

    def test_wash_dashed_language(self):
        """messages - washing dashed language code (fr-ca)"""
        if 'fr' not in CFG_SITE_LANGS:
            self.assertEqual(messages.wash_language('fr-ca'),
                             CFG_SITE_LANG)
        else:
            self.assertEqual(messages.wash_language('fr-ca'),
                             'fr')

    def test_wash_languages(self):
        """messages - washing multiple languages"""
        if 'de' not in CFG_SITE_LANGS:
            self.assertEqual(messages.wash_languages(['00',
                                                  '11',
                                                  '22',
                                                  'de']),
                         CFG_SITE_LANG)
        else:
            self.assertEqual(messages.wash_languages(['00',
                                                  '11',
                                                  '22',
                                                  'de']),
                         'de')
        self.assertEqual(messages.wash_languages(['00',
                                                  '11',
                                                  '22']),
                         CFG_SITE_LANG)

TEST_SUITE = make_test_suite(MessagesLanguageTest,)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE)
