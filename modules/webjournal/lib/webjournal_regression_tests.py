# -*- coding: utf-8 -*-
##
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008 CERN.
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

"""WebJournal Regression Test Suite."""

__revision__ = "$Id$"

import datetime
import unittest
import urllib
from invenio import webjournal_utils as wju
from invenio.config import CFG_SITE_URL, \
                           CFG_SITE_LANG, \
                           CFG_SITE_SUPPORT_EMAIL, \
			   CFG_PREFIX
from invenio.testutils import make_test_suite, run_test_suite

class ArticlesRelated(unittest.TestCase):
    """Functions about articles"""

    def test_is_new_article(self):
        """webjournal - checks if an article is new or not """
        article = wju.is_new_article('AtlantisTimes', '03/2009', 99)
        self.assertEqual(article, False)

        article = wju.is_new_article('AtlantisTimes', '03/2009', 103)
        self.assertEqual(article, True)


class CategoriesRelated(unittest.TestCase):
    """Functions about journal categories"""

    def test_get_journal_categories(self):
        """webjournal - returns all categories for a given issue"""
        journal1 = wju.get_journal_categories('AtlantisTimes', '03/2009')
        self.assertEqual(journal1[0], 'News')
        self.assertEqual(journal1[1], 'Science')

        journal2 = wju.get_journal_categories('AtlantisTimes', )
        self.assertEqual(journal2[0], 'News')
        self.assertEqual(journal2[1], 'Science')
        self.assertEqual(journal2[2], 'Arts')

    def test_get_category_query(self):
        """webjournal - returns the category definition  """
        self.assertEqual(wju.get_category_query('AtlantisTimes', 'News'),
                                                '980__a:ATLANTISTIMESNEWS or 980__a:ATLANTISTIMESNEWSDRAFT')
        self.assertEqual(wju.get_category_query('AtlantisTimes', 'Science'),
                                                '980__a:ATLANTISTIMESSCIENCE or 980__a:ATLANTISTIMESSCIENCEDRAFT')


class JournalConfigVars(unittest.TestCase):
    """Functions to get journal variables """

    def test_get_xml_from_config(self):
        """webjournal - returns values from the journal configuration file """
        value = wju.get_xml_from_config(["submission/doctype"], 'AtlantisTimes')
        self.assertEqual(value.values()[0], ['DEMOJRN'])
        self.assertEqual(value.keys(), ['submission/doctype'])
        value = wju.get_xml_from_config(["submission/identifier_element"], 'AtlantisTimes')
        self.assertEqual(value.values()[0], ['DEMOJRN_RN'])
        self.assertEqual(value.keys(), ['submission/identifier_element'])

    def test_get_journal_issue_field(self):
        """webjournal - returns the MARC field  """
        value = wju.get_journal_issue_field('AtlantisTimes')
        self.assertEqual(value, '773__n')

    def test_get_journal_css_url(self):
        """webjournal - returns URL to this journal's CSS """
        self.assertEqual(wju.get_journal_css_url('AtlantisTimes', type='screen'), CFG_SITE_URL + '/img/AtlantisTimes.css')

    def test_get_journal_submission_params(self):
        """webjournal - returns params for the submission of articles """
        submissions = wju.get_journal_submission_params('AtlantisTimes')
        self.assertEqual(submissions[0], 'DEMOJRN')
        self.assertEqual(submissions[1], 'DEMOJRN_RN')
        self.assertEqual(submissions[2], '037__a')

    def test_get_journal_draft_keyword_to_remove(self):
        """webjournal - returns the keyword to removed in order to move the article from Draft to Ready """
        self.assertEqual(wju.get_journal_draft_keyword_to_remove('AtlantisTimes'), 'DRAFT')

    def test_get_journal_alert_sender_email(self):
        """webjournal - returns the email address used to send of the alert email. """
        self.assertEqual(wju.get_journal_alert_sender_email('AtlantisTimes'), CFG_SITE_SUPPORT_EMAIL)

    def test_get_journal_alert_recipient_email(self):
        """webjournal - returns the default email address of the recipients of the email"""
        self.assertEqual(wju.get_journal_alert_recipient_email('AtlantisTimes'),'recipients@atlantis.atl')

    def test_get_journal_template(self):
        """webjournal - returns the journal templates name for the given template type"""
        value = wju.get_journal_template('index', 'AtlantisTimes', ln=CFG_SITE_LANG)
        self.assertEqual(value, 'webjournal/AtlantisTimes_Index.bft')

    def test_get_journal_name_intl(self):
        """webjournal - returns the nice name of the journal """
        name = wju.get_journal_name_intl('AtlantisTimes', ln=CFG_SITE_LANG)
        self.assertEqual(name, 'Atlantis Times')

    def test_get_journal_languages(self):
        """webjournal - returns the list of languages defined for this journal"""
        lang = wju.get_journal_languages('AtlantisTimes')
        self.assertEqual(lang[0], 'en')
        self.assertEqual(lang[1], 'fr')

    def test_get_journal_issue_grouping(self):
        """webjournal - returns the number of issue that are typically released
        at the same time"""
        issue = wju.get_journal_issue_grouping('AtlantisTimes')
        self.assertEqual(issue, 2)

    def test_get_journal_nb_issues_per_year(self):
        """webjournal - returns the default number of issues per year for this
        journal"""
        nb = wju.get_journal_nb_issues_per_year('AtlantisTimes')
        self.assertEqual(nb, 52)

    def test_get_journal_preferred_language(self):
        """webjournal - returns the most adequate language to display the
        journal, given a language """
        value = wju.get_journal_preferred_language('AtlantisTimes', 'fr')
        self.assertEqual(value, 'fr')
        value = wju.get_journal_preferred_language('AtlantisTimes', 'it')
        self.assertEqual(value, 'en')
        value = wju.get_journal_preferred_language('AtlantisTimes', 'hello')
        self.assertEqual(value, 'en')

    def test_get_unreleased_issue_hiding_mode(self):
        """webjournal - returns how unreleased issue should be treated"""
        value = wju.get_unreleased_issue_hiding_mode('AtlantisTimes')
        self.assertEqual(value, 'all')

    def test_get_first_issue_from_config(self):
        """webjournal - returns the first issue as defined from config"""
        issue = wju.get_first_issue_from_config('AtlantisTimes')
        self.assertEqual(issue, '02/2009')


class TimeIssueFunctions(unittest.TestCase):
    """Functions about time, using issues"""

    def test_get_current_issue(self):
        """webjournal - returns the current issue of a journal """
        issue = wju.get_current_issue('en', 'AtlantisTimes')
        self.assertEqual(issue,  '03/2009')

    def test_get_all_released_issues(self):
        """webjournal - returns the list of released issue"""
        issues = wju.get_all_released_issues('AtlantisTimes')
        self.assertEqual(issues[0], '03/2009')
        self.assertEqual(issues[1], '02/2009')

    def test_get_next_journal_issues(self):
        """webjournal - this function suggests the 'n' next issue numbers """
        issues = wju.get_next_journal_issues('03/2009', 'AtlantisTimes', n=2)
        self.assertEqual(issues[0], '04/2009')
        self.assertEqual(issues[1], '05/2009')

    def test_get_grouped_issues(self):
        """webjournal - returns all the issues grouped with a given one"""
        issues = wju.get_grouped_issues('AtlantisTimes', '03/2009')
        self.assertEqual(issues[0], '02/2009')
        self.assertEqual(issues[1], '03/2009')

    def test_get_issue_number_display(self):
        """webjournal - returns the display string for a given issue number"""
        issue_nb = wju.get_issue_number_display('03/2009', 'AtlantisTimes', ln=CFG_SITE_LANG)
        self.assertEqual(issue_nb, '02-03/2009')

    def test_make_issue_number(self):
        """webjournal - creates a normalized issue number representation"""
        issue = wju.make_issue_number('AtlantisTimes', 03, 2009, for_url_p=False)
        self.assertEqual(issue, '03/2009')
        issue = wju.make_issue_number('AtlantisTimes', 06, 2009, for_url_p=False)
        self.assertEqual(issue, '06/2009')
        issue = wju.make_issue_number('AtlantisTimes', 03, 2008, for_url_p=False)
        self.assertEqual(issue, '03/2008')

    def test_get_release_datetime(self):
        """webjournal - gets the date at which an issue was released from the DB"""
        value = wju.get_release_datetime('03/2009', 'AtlantisTimes', ln=CFG_SITE_LANG)
        self.assertEqual(value, datetime.datetime(2009, 1, 16, 0, 0))

    def test_get_announcement_datetime(self):
        """webjournal - get the date at which an issue was announced through
        the alert system"""
        value = wju.get_announcement_datetime('03/2009', 'AtlantisTimes', ln=CFG_SITE_LANG)
        self.assertEqual(value, None)

    def test_datetime_to_issue(self):
        """webjournal - returns the issue corresponding to the given datetime object"""
        date_value = datetime.datetime(2009, 7, 16, 13, 39, 46, 426373)
        value = wju.datetime_to_issue(date_value, 'AtlantisTimes')
        self.assertEqual(value, None)

    def test_issue_to_datetime(self):
        """webjournal - returns the *theoretical* date of release for given issue"""
        issue = wju.issue_to_datetime('03/2009', 'AtlantisTimes', granularity=None)
        self.assertEqual(issue, datetime.datetime(2009, 1, 19, 0, 0))

    def test_get_number_of_articles_for_issue(self):
        """webjournal - returns a dictionary with all categories and number of
        articles in each category"""
        value = wju.get_number_of_articles_for_issue('03/2009', 'AtlantisTimes', ln=CFG_SITE_LANG)
        self.assertEqual(value.values()[0], 3)
        self.assertEqual(value.values()[1], 1)
        self.assertEqual(value.keys()[0], 'News')
        self.assertEqual(value.keys()[1], 'Science')


class JournalRelated(unittest.TestCase):
    """Functions about journal"""

    def test_get_journal_info_path(self):
        """webjournal - returns the path to the info file of the given journal"""
        info = wju.get_journal_info_path('AtlantisTimes')
        path = CFG_PREFIX + '/var/cache/webjournal/AtlantisTimes/info.dat'
        self.assertEqual(info, path)

    def test_get_journal_article_cache_path(self):
        """webjournal - returns the path to cache file of the articles of a given issue"""
        info = wju.get_journal_article_cache_path('AtlantisTimes', '03/2009')
        path = CFG_PREFIX + '/var/cache/webjournal/AtlantisTimes/03_2009_articles_cache.dat'
        self.assertEqual(info, path)

    def test_get_journal_id(self):
        """webjournal - get the id for this journal from the DB"""
        jrnid = wju.get_journal_id('AtlantisTimes', ln=CFG_SITE_LANG)
        self.assertEqual(jrnid, 1)

    def test_guess_journal_name(self):
        """webjournal - tries to take a guess what a user was looking for on
        the server if not providing a name for the journal"""
        name = wju.guess_journal_name('en', journal_name=None)
        self.assertEqual(name, 'AtlantisTimes' )

    def test_get_journals_ids_and_names(self):
        """webjournal - returns the list of existing journals IDs and names"""
        ids_names = wju.get_journals_ids_and_names()
        self.assertEqual(ids_names[0].values(), [1, 'AtlantisTimes'])
        self.assertEqual(ids_names[0].keys(), ['journal_id', 'journal_name'])

    def test_parse_url_string(self):
        """webjournal - parses any url string given in webjournal"""
        d = wju.parse_url_string("/journal/AtlantisTimes/2009/03/News/?ln=en")
        self.assertEqual(d['category'], 'News')
        self.assertEqual(d['issue_year'], 2009)
        self.assertEqual(d['ln'], 'en')
        self.assertEqual(d['issue_number'], 3)
        self.assertEqual(d['journal_name'], 'AtlantisTimes')
        self.assertEqual(d['issue'], '03/2009')

        d = wju.parse_url_string("/journal/AtlantisTimes/2009/03/Science?ln=en")
        self.assertEqual(d['category'], 'Science')
        self.assertEqual(d['issue_year'], 2009)
        self.assertEqual(d['ln'], 'en')
        self.assertEqual(d['issue_number'], 3)
        self.assertEqual(d['journal_name'], 'AtlantisTimes')
        self.assertEqual(d['issue'], '03/2009')

        d = wju.parse_url_string("/journal/AtlantisTimes/2009/03/News/97?ln=en")
        self.assertEqual(d['category'], 'News')
        self.assertEqual(d['issue_year'], 2009)
        self.assertEqual(d['ln'], 'en')
        self.assertEqual(d['issue_number'], 3)
        self.assertEqual(d['recid'], 97)
        self.assertEqual(d['journal_name'], 'AtlantisTimes')
        self.assertEqual(d['issue'], '03/2009')

        try:
            wju.parse_url_string("/journal/fictivejournal/2009/03/News/97?ln=en")
            dont_find_journal = 'not'
        except:
            dont_find_journal = 'ok'
        self.assertEqual(dont_find_journal, 'ok')


class HtmlCachingFunction(unittest.TestCase):
    """HTML caching functions"""

    def setUp(self):
        "Access some URL for cache to be generated"
        urllib.urlopen(CFG_SITE_URL + '/journal/AtlantisTimes/2009/03/News')
        urllib.urlopen(CFG_SITE_URL + '/journal/AtlantisTimes/2009/03/News/103')

    def test_get_index_page_from_cache(self):
        """webjournal - function to get an index page from the cache"""
        value = wju.get_index_page_from_cache('AtlantisTimes', 'News', '03/2009', 'en')
        assert("Atlantis (Timaeus)" in value)

    def test_get_article_page_from_cache(self):
        """webjournal - gets an article view of a journal from cache"""
        value = wju.get_article_page_from_cache('AtlantisTimes', 'News', 103, '03/2009', 'en')
        assert("April 14th, 1832.—Leaving Socêgo, we rode to another estate on the Rio Macâe" in value)

    def test_clear_cache_for_issue(self):
        """webjournal - clears the cache of a whole issue"""
        value = wju.clear_cache_for_issue('AtlantisTimes', '03/2009')
        self.assertEqual(value, True)

TEST_SUITE = make_test_suite(ArticlesRelated,
                             CategoriesRelated,
                             JournalConfigVars,
                             TimeIssueFunctions,
                             JournalRelated,
                             HtmlCachingFunction)
if __name__ == "__main__":
    run_test_suite(TEST_SUITE, warn_user=True)














