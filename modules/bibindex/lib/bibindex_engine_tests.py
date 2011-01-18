# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2004, 2005, 2006, 2007, 2008, 2010, 2011 CERN.
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

"""Unit tests for the indexing engine."""

__revision__ = \
    "$Id$"

import unittest

from invenio import bibindex_engine
from invenio.testutils import make_test_suite, run_test_suite


class TestListSetOperations(unittest.TestCase):
    """Tests for list set operations."""

    def test_list_union(self):
        """bibindex engine - list union"""
        self.assertEqual([1, 2, 3, 4],
                         bibindex_engine.list_union([1, 2, 3],
                                                    [1, 3, 4]))


class TestWashIndexTerm(unittest.TestCase):
    """Tests for washing index terms, useful for both searching and indexing."""

    def test_wash_index_term_short(self):
        """bibindex engine - wash index term, short word"""
        self.assertEqual("ellis",
                         bibindex_engine.wash_index_term("ellis"))

    def test_wash_index_term_long(self):
        """bibindex engine - wash index term, long word"""
        self.assertEqual(50*"e",
                         bibindex_engine.wash_index_term(1234*"e"))

    def test_wash_index_term_case(self):
        """bibindex engine - wash index term, lower the case"""
        self.assertEqual("ellis",
                         bibindex_engine.wash_index_term("Ellis"))

    def test_wash_index_term_unicode(self):
        """bibindex engine - wash index term, unicode"""
        self.assertEqual("ελληνικό αλφάβητο",
          bibindex_engine.wash_index_term("Ελληνικό αλφάβητο"))


class TestGetWordsFromPhrase(unittest.TestCase):
    """Tests for getting words from phrase."""

    def test_easy_phrase(self):
        """bibindex engine - getting words from `word1 word2' phrase"""
        test_phrase = 'word1 word2'
        l_words_expected = ['word1', 'word2']
        l_words_obtained = bibindex_engine.get_words_from_phrase(test_phrase)
        l_words_obtained.sort()
        self.assertEqual(l_words_obtained, l_words_expected)

    def test_dashed_phrase(self):
        """bibindex engine - getting words from `word1-word2' phrase"""
        test_phrase = 'word1-word2'
        l_words_expected = ['word1', 'word1-word2', 'word2']
        l_words_obtained = bibindex_engine.get_words_from_phrase(test_phrase)
        l_words_obtained.sort()
        self.assertEqual(l_words_obtained, l_words_expected)

    def test_arXiv_good(self):
        """bibindex engine - getting words from `arXiv:1007.5048' phrase"""
        test_phrase = 'arXiv:1007.5048'
        l_words_expected = ['1007', '1007.5048', '5048', 'arxiv', 'arxiv:1007.5048']
        l_words_obtained = bibindex_engine.get_words_from_phrase(test_phrase)
        l_words_obtained.sort()
        self.assertEqual(l_words_obtained, l_words_expected)

    def test_arXiv_bad(self):
        """bibindex engine - getting words from `arXiv:1xy7.5z48' phrase"""
        test_phrase = 'arXiv:1xy7.5z48'
        l_words_expected = ['1xy7', '5z48', 'arxiv', 'arxiv:1xy7.5z48']
        l_words_obtained = bibindex_engine.get_words_from_phrase(test_phrase)
        l_words_obtained.sort()
        self.assertEqual(l_words_obtained, l_words_expected)

class TestGetWordsFromDateTag(unittest.TestCase):
    """Tests for getting words for date-like tag."""

    def test_dateindex_yyyy(self):
        """bibindex engine - index date-like tag, yyyy"""
        self.assertEqual(["2010"],
                         bibindex_engine.get_words_from_date_tag("2010"))

    def test_dateindex_yyyy_mm(self):
        """bibindex engine - index date-like tag, yyyy-mm"""
        self.assertEqual(["2010-03", "2010"],
                         bibindex_engine.get_words_from_date_tag("2010-03"))

    def test_dateindex_yyyy_mm_dd(self):
        """bibindex engine - index date-like tag, yyyy-mm-dd"""
        self.assertEqual(["2010-03-08", "2010", "2010-03", ],
                         bibindex_engine.get_words_from_date_tag("2010-03-08"))

    def test_dateindex_freetext(self):
        """bibindex engine - index date-like tag, yyyy-mm-dd"""
        self.assertEqual(["dd", "mon", "yyyy"],
          bibindex_engine.get_words_from_date_tag("dd mon yyyy"))


class TestGetAuthorFamilyNameWords(unittest.TestCase):
    """Tests for getting family name words from author names."""

    def test_authornames_john_doe(self):
        """bibindex engine - get author family name words for John Doe"""
        self.assertEqual(['doe',],
          bibindex_engine.get_author_family_name_words_from_phrase('John Doe'))

    def test_authornames_doe_john(self):
        """bibindex engine - get author family name words for Doe, John"""
        self.assertEqual(['doe',],
          bibindex_engine.get_author_family_name_words_from_phrase('Doe, John'))


TEST_SUITE = make_test_suite(TestListSetOperations,
                             TestWashIndexTerm,
                             TestGetWordsFromPhrase,
                             TestGetWordsFromDateTag,
                             TestGetAuthorFamilyNameWords)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE)
