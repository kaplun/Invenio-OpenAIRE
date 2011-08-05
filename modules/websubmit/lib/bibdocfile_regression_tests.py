# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2009, 2010, 2011 CERN.
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

"""BibDocFile Regression Test Suite."""

__revision__ = "$Id$"

import unittest
from invenio.testutils import make_test_suite, run_test_suite
from invenio.bibdocfile import BibRecDocs, check_bibdoc_authorization
from invenio.access_control_config import CFG_WEBACCESS_WARNING_MSGS
from invenio.config import \
        CFG_SITE_URL, \
        CFG_PREFIX, \
        CFG_WEBSUBMIT_FILEDIR, \
        CFG_SITE_RECORD
import invenio.template


class BibRecDocsTest(unittest.TestCase):
    """regression tests about BibRecDocs"""

    def test_BibRecDocs(self):
        """bibdocfile - BibRecDocs functions"""
        my_bibrecdoc = BibRecDocs(2)
        #add bibdoc
        my_bibrecdoc.add_new_file(CFG_PREFIX + '/lib/webtest/invenio/test.jpg', 'Main', 'img_test', False, 'test add new file', 'test', '.jpg')
        my_bibrecdoc.add_bibdoc(doctype='Main', docname='file', never_fail=False)
        self.assertEqual(len(my_bibrecdoc.list_bibdocs()), 3)
        my_added_bibdoc = my_bibrecdoc.get_bibdoc('file')
        #add bibdocfile in empty bibdoc
        my_added_bibdoc.add_file_new_version(CFG_PREFIX + '/lib/webtest/invenio/test.gif', \
        description= 'added in empty bibdoc', comment=None, format=None, flags=['PERFORM_HIDE_PREVIOUS'])
        #propose unique docname
        self.assertEqual(my_bibrecdoc.propose_unique_docname('file'), 'file_2')
        #has docname
        self.assertEqual(my_bibrecdoc.has_docname_p('file'), True)
        #merge 2 bibdocs
        my_bibrecdoc.merge_bibdocs('img_test', 'file')
        self.assertEqual(len(my_bibrecdoc.get_bibdoc("img_test").list_all_files()), 2)
        #check file exists
        self.assertEqual(my_bibrecdoc.check_file_exists(CFG_PREFIX + '/lib/webtest/invenio/test.jpg'), True)
        #get bibdoc names
        self.assertEqual(my_bibrecdoc.get_bibdoc_names('Main')[0], '0104007_02')
        self.assertEqual(my_bibrecdoc.get_bibdoc_names('Main')[1],'img_test')
        #get total size
        self.assertEqual(my_bibrecdoc.get_total_size(), 1647591)
        #get total size latest version
        self.assertEqual(my_bibrecdoc.get_total_size_latest_version(), 1647591)
        #display
        tmpl = invenio.template.load("bibdocfile")
        value = tmpl.tmpl_display_bibrecdocs(my_bibrecdoc, docname='img_test', version='', doctype='', ln='en', verbose=0, display_hidden=True)

        self.assert_("<small><b>Main</b>" in value)
        #get xml 8564
        value = my_bibrecdoc.get_xml_8564()
        self.assert_('/'+ CFG_SITE_RECORD +'/2/files/img_test.jpg</subfield>' in value)
        #check duplicate docnames
        self.assertEqual(my_bibrecdoc.check_duplicate_docnames(), True)

    def tearDown(self):
        my_bibrecdoc = BibRecDocs(2)
        #delete
        my_bibrecdoc.delete_bibdoc('img_test')
        my_bibrecdoc.delete_bibdoc('file')

class BibDocsTest(unittest.TestCase):
    """regression tests about BibDocs"""

    def test_BibDocs(self):
        """bibdocfile - BibDocs functions"""
        #add file
        my_bibrecdoc = BibRecDocs(2)
        my_bibrecdoc.add_new_file(CFG_PREFIX + '/lib/webtest/invenio/test.jpg', 'Main', 'img_test', False, 'test add new file', 'test', '.jpg')
        my_new_bibdoc = my_bibrecdoc.get_bibdoc("img_test")
        value = my_bibrecdoc.list_bibdocs()
        self.assertEqual(len(value), 2)
        #get total file (bibdoc)
        self.assertEqual(my_new_bibdoc.get_total_size(), 91750)
        #get recid
        self.assertEqual(my_new_bibdoc.get_recid(), 2)
        #change name
        my_new_bibdoc.change_name('new_name')
        #get docname
        self.assertEqual(my_new_bibdoc.get_docname(), 'new_name')
        #get type
        self.assertEqual(my_new_bibdoc.get_type(), 'Main')
        #get id
        self.assert_(my_new_bibdoc.get_id() > 80)
        #set status
        my_new_bibdoc.set_status('new status')
        #get status
        self.assertEqual(my_new_bibdoc.get_status(), 'new status')
        #get base directory
        self.assert_(my_new_bibdoc.get_base_dir().startswith(CFG_WEBSUBMIT_FILEDIR))
        #get file number
        self.assertEqual(my_new_bibdoc.get_file_number(), 1)
        #add file new version
        my_new_bibdoc.add_file_new_version(CFG_PREFIX + '/lib/webtest/invenio/test.jpg', description= 'the new version', comment=None, format=None, flags=["PERFORM_HIDE_PREVIOUS"])
        self.assertEqual(my_new_bibdoc.list_versions(), [1, 2])
        #revert
        my_new_bibdoc.revert(1)
        self.assertEqual(my_new_bibdoc.list_versions(), [1, 2, 3])
        self.assertEqual(my_new_bibdoc.get_description('.jpg', version=3), 'test add new file')
        #get total size latest version
        self.assertEqual(my_new_bibdoc.get_total_size_latest_version(), 91750)
        #get latest version
        self.assertEqual(my_new_bibdoc.get_latest_version(), 3)
        #list latest files
        self.assertEqual(len(my_new_bibdoc.list_latest_files()), 1)
        self.assertEqual(my_new_bibdoc.list_latest_files()[0].get_version(), 3)
        #list version files
        self.assertEqual(len(my_new_bibdoc.list_version_files(1, list_hidden=True)), 1)
        #display
        tmpl = invenio.template.load("bibdocfile")
        value = tmpl.tmpl_display_bibdoc(my_new_bibdoc, version='', ln='en', display_hidden=True)
        self.assert_('>test add new file<' in value)
        #format already exist
        self.assertEqual(my_new_bibdoc.format_already_exists_p('.jpg'), True)
        #get file
        self.assertEqual(my_new_bibdoc.get_file('.jpg', version='1').get_version(), 1)
        #set description
        my_new_bibdoc.set_description('new description', '.jpg', version=1)
        #get description
        self.assertEqual(my_new_bibdoc.get_description('.jpg', version=1), 'new description')
        #set comment
        my_new_bibdoc.set_description('new comment', '.jpg', version=1)
        #get comment
        self.assertEqual(my_new_bibdoc.get_description('.jpg', version=1), 'new comment')
        #get history
        assert len(my_new_bibdoc.get_history()) > 0
        #delete file
        my_new_bibdoc.delete_file('.jpg', 2)
        #list all files
        self.assertEqual(len(my_new_bibdoc.list_all_files()), 2)
        #delete file
        my_new_bibdoc.delete_file('.jpg', 3)
        #add new format
        my_new_bibdoc.add_file_new_format(CFG_PREFIX + '/lib/webtest/invenio/test.gif', version=None, description=None, comment=None, format=None)
        self.assertEqual(len(my_new_bibdoc.list_all_files()), 2)
        #delete file
        my_new_bibdoc.delete_file('.jpg', 1)
        #delete file
        my_new_bibdoc.delete_file('.gif', 1)
        #empty bibdoc
        self.assertEqual(my_new_bibdoc.empty_p(), True)
        #hidden?
        self.assertEqual(my_new_bibdoc.hidden_p('.jpg', version=1), False)
        #hide
        my_new_bibdoc.set_flag('HIDDEN', '.jpg', version=1)
        #hidden?
        self.assertEqual(my_new_bibdoc.hidden_p('.jpg', version=1), True)
        #add and get icon
        my_new_bibdoc.add_icon( CFG_PREFIX + '/lib/webtest/invenio/icon-test.gif')
        value =  my_bibrecdoc.list_bibdocs()[1]
        self.assertEqual(value.get_icon(), my_new_bibdoc.get_icon())
        #delete icon
        my_new_bibdoc.delete_icon()
        #get icon
        self.assertEqual(my_new_bibdoc.get_icon(), None)
        #delete
        my_new_bibdoc.delete()
        self.assertEqual(my_new_bibdoc.deleted_p(), True)
        #undelete
        my_new_bibdoc.undelete(previous_status='')
        #expunging
        my_new_bibdoc.expunge()
        my_bibrecdoc.build_bibdoc_list()
        self.failIf('new_name' in my_bibrecdoc.get_bibdoc_names())
        self.failUnless(my_bibrecdoc.get_bibdoc_names())

    def tearDown(self):
        my_bibrecdoc = BibRecDocs(2)
        #delete
        my_bibrecdoc.delete_bibdoc('img_test')
        my_bibrecdoc.delete_bibdoc('new_name')


class BibDocFilesTest(unittest.TestCase):
    """regression tests about BibDocFiles"""

    def test_BibDocFiles(self):
        """bibdocfile - BibDocFile functions """
        #add bibdoc
        my_bibrecdoc = BibRecDocs(2)
        my_bibrecdoc.add_new_file(CFG_PREFIX + '/lib/webtest/invenio/test.jpg', 'Main', 'img_test', False, 'test add new file', 'test', '.jpg')
        my_new_bibdoc = my_bibrecdoc.get_bibdoc("img_test")
        my_new_bibdocfile = my_new_bibdoc.list_all_files()[0]
        #get url
        self.assertEqual(my_new_bibdocfile.get_url(), CFG_SITE_URL + '/%s/2/files/img_test.jpg' % CFG_SITE_RECORD)
        #get type
        self.assertEqual(my_new_bibdocfile.get_type(), 'Main')
        #get path
        self.assert_(my_new_bibdocfile.get_path().startswith(CFG_WEBSUBMIT_FILEDIR))
        self.assert_(my_new_bibdocfile.get_path().endswith('/img_test.jpg;1'))
        #get bibdocid
        self.assertEqual(my_new_bibdocfile.get_bibdocid(), my_new_bibdoc.get_id())
        #get name
        self.assertEqual(my_new_bibdocfile.get_name() , 'img_test')
        #get full name
        self.assertEqual(my_new_bibdocfile.get_full_name() , 'img_test.jpg')
        #get full path
        self.assert_(my_new_bibdocfile.get_full_path().startswith(CFG_WEBSUBMIT_FILEDIR))
        self.assert_(my_new_bibdocfile.get_full_path().endswith('/img_test.jpg;1'))
        #get format
        self.assertEqual(my_new_bibdocfile.get_format(), '.jpg')
        #get version
        self.assertEqual(my_new_bibdocfile.get_version(), 1)
        #get description
        self.assertEqual(my_new_bibdocfile.get_description(), my_new_bibdoc.get_description('.jpg', version=1))
        #get comment
        self.assertEqual(my_new_bibdocfile.get_comment(), my_new_bibdoc.get_comment('.jpg', version=1))
        #get recid
        self.assertEqual(my_new_bibdocfile.get_recid(), 2)
        #get status
        self.assertEqual(my_new_bibdocfile.get_status(), '')
        #get size
        self.assertEqual(my_new_bibdocfile.get_size(), 91750)
        #get checksum
        self.assertEqual(my_new_bibdocfile.get_checksum(), '28ec893f9da735ad65de544f71d4ad76')
        #check
        self.assertEqual(my_new_bibdocfile.check(), True)
        #display
        tmpl = invenio.template.load("bibdocfile")
        value = tmpl.tmpl_display_bibdocfile(my_new_bibdocfile, ln='en')
        assert 'files/img_test.jpg?version=1">' in value
        #hidden?
        self.assertEqual(my_new_bibdocfile.hidden_p(), False)
        #delete
        my_new_bibdoc.delete()
        self.assertEqual(my_new_bibdoc.deleted_p(), True)

class CheckBibDocAuthorization(unittest.TestCase):
    """Regression tests for check_bibdoc_authorization function."""
    def test_check_bibdoc_authorization(self):
        """bibdocfile - check_bibdoc_authorization function"""
        from invenio.webuser import collect_user_info, get_uid_from_email
        jekyll = collect_user_info(get_uid_from_email('jekyll@cds.cern.ch'))
        self.assertEqual(check_bibdoc_authorization(jekyll, 'role:thesesviewer'), (0, CFG_WEBACCESS_WARNING_MSGS[0]))
        self.assertEqual(check_bibdoc_authorization(jekyll, 'role: thesesviewer'), (0, CFG_WEBACCESS_WARNING_MSGS[0]))
        self.assertEqual(check_bibdoc_authorization(jekyll, 'role:  thesesviewer'), (0, CFG_WEBACCESS_WARNING_MSGS[0]))
        self.assertEqual(check_bibdoc_authorization(jekyll, 'Role:  thesesviewer'), (0, CFG_WEBACCESS_WARNING_MSGS[0]))
        self.assertEqual(check_bibdoc_authorization(jekyll, 'email: jekyll@cds.cern.ch'), (0, CFG_WEBACCESS_WARNING_MSGS[0]))
        self.assertEqual(check_bibdoc_authorization(jekyll, 'email: jekyll@cds.cern.ch'), (0, CFG_WEBACCESS_WARNING_MSGS[0]))

        juliet = collect_user_info(get_uid_from_email('juliet.capulet@cds.cern.ch'))
        self.assertEqual(check_bibdoc_authorization(juliet, 'restricted_picture'), (0, CFG_WEBACCESS_WARNING_MSGS[0]))
        self.assertEqual(check_bibdoc_authorization(juliet, 'status: restricted_picture'), (0, CFG_WEBACCESS_WARNING_MSGS[0]))
        self.assertNotEqual(check_bibdoc_authorization(juliet, 'restricted_video')[0], 0)
        self.assertNotEqual(check_bibdoc_authorization(juliet, 'status: restricted_video')[0], 0)

lass MoreInfoTest(unittest.TestCase):
    """regression tests about BibDocFiles"""

    def test_DictionaryBehaviour(self):
        """moreinfo - tests assignments of data, both using the general interface and using
           namespaces"""
        more_info = MoreInfo()
        more_info.set_data("namespace1", "key1", "val1")
        more_info.set_data("namespace1", "key2", "val2")
        more_info.set_data("namespace2", "key1", "val3")
        self.assertEqual(more_info.get_data("namespace1", "key1"), "val1")
        self.assertEqual(more_info.get_data("namespace1", "key2"), "val2")
        self.assertEqual(more_info.get_data("namespace2", "key1"), "val3")


class BibDocRelationTest(unittest.TestCase):
    def test_rel(self):
        """bibdoc_relation"""
        doc1 = BibDoc(docid = 10)
        doc2 = BibDoc(docid = 12)
        # creating a relation without passing more_info object -> the database will be accessed
        rel1 = BibDocRelation(doc1, doc2, "some_rel", 1, 1)
        rel2 = BibDocRelation(doc1, doc2, "some_rel", 1, 2)

        rel1["key1"] = "value1"
        rel1["key2"] = "value2"
        rel2["key1"] = "value3"

        rel1.flush()
        rel2.flush()

        # now testing the retrieval of data
        new_rel1 = BibDocRelation(doc1, doc2, "some_rel", 1, 1)
        new_rel2 = BibDocRelation(doc1, doc2, "some_rel", 1, 2)

        self.assertEqual(new_rel1["key1"], "value1")
        self.assertEqual(new_rel1["key2"], "value2")
        self.assertEqual(new_rel2["key1"], "value3")

        new_rel1.flush()
        new_rel2.flush()

        # now testing the deletion of relations
        new_rel1.delete()
        new_rel2.delete()

        newer_rel1 = BibDocRelation(doc1, doc2, "some_rel", 1, 1)
        newer_rel2 = BibDocRelation(doc1, doc2, "some_rel", 3, 2)
        self.assertEqual("key1" in newer_rel1, False)
        self.assertEqual("key1" in newer_rel2, False)

    def test_retrieve_rel(self):
        """bibdoc_relation_retrieval"""
        doc1 = BibDoc(docid = 3)
        doc2 = BibDoc(docid = 7)
        rel = BibDocRelation(doc1, doc2, "is_extracted_from", 1, 1)
        rel["key"] = "value"
        rel.flush()

        rel2 = BibDocRelation(doc1, doc2, "is_extracted_from", 3, 2)
        rel2["key2"] = "value2"
        rel2.flush()

        rels = doc2.get_incoming_relations()
        # retreived all incoming relations regardless the version
        #  - should return 2 results
        self.assertEqual(len(rels), 2)

        rels = doc2.get_incoming_relations(version = 2) # only rels of version 2
        self.assertEqual(len(rels), 1)
        self.assertEqual(rels[0]["key2"], "value2")

        rels = doc2.get_incoming_relations(version = 1) # only relations of ver 1
        self.assertEqual(len(rels), 1)
        self.assertEqual(rels[0]["key"], "value")

        rels = doc2.get_outgoing_relations() # there should be no outgoing relations
        self.assertEqual(len(rels), 0)

        #now retrieving outgoing relations

        rels = doc1.get_outgoing_relations()
        # retreived all incoming relations regardless the version
        #  - should return 2 results
        self.assertEqual(len(rels), 2)

        rels = doc1.get_outgoing_relations(version = 1) # only rels of version 1
        self.assertEqual(len(rels), 1)
        self.assertEqual(rels[0]["key"], "value")

        rels = doc1.get_outgoing_relations(version = 3) # only relations of ver 3
        self.assertEqual(len(rels), 1)
        self.assertEqual(rels[0]["key2"], "value2")

        rels = doc1.get_incoming_relations() # there should be no outgoing relations
        self.assertEqual(len(rels), 0)


        rel.delete()
        rel2.delete()



TEST_SUITE = make_test_suite(BibRecDocsTest, \
                             BibDocsTest, \
                             BibDocFilesTest, \
                             MoreInfoTest, \
                             BibDocRelationTest, \
                             CheckBibDocAuthorization)

if __name__ == "__main__":
    run_test_suite(TEST_SUITE, warn_user=True)
