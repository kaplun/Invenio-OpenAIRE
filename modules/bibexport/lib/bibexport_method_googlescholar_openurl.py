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

"""
BibExport plugin implementing 'googlescholar_openurl' exporting method.

The main function is run_export_method(jobname) defined at the end.
This is what BibExport daemon calls for all the export jobs that use
this exporting method.

The Google Scholar via OpenURL exporting method implements the requirements
for homegrown OpenURL resolver at:
<http://scholar.google.com/intl/en/scholar/libraries.html#start4>.
"""

from invenio.config import CFG_WEBDIR, CFG_CERN_SITE, CFG_ETCDIR, \
    CFG_SITE_NAME, CFG_SITE_NAME_INTL, CFG_SITE_ADMIN_EMAIL, \
    CFG_SITE_URL
from invenio.bibtask import write_message
from invenio.search_engine import perform_request_search, get_record
from invenio.bibexport_method_googlescholar import GoogleScholarExporter, \
    GoogleScholarExportException
from invenio.errorlib import register_exception
from invenio.textutils import encode_for_xml
from invenio.intbitset import intbitset
from invenio.bibrecord import record_get_field_value
from invenio.dbquery import run_sql
from ConfigParser import ConfigParser
import os

def run_export_method(jobname):
    """Main function, reading params and running the task."""
    # FIXME: read jobname's cfg file to detect collection and fulltext status arguments
    write_message("bibexport_sitemap: job %s started." % jobname)

    try:
        output_directory = CFG_WEBDIR + os.sep + "export" + os.sep + "googlescholar_openurl"
        exporter = GoogleScholarExporterOpenURL(output_directory, jobname)
        exporter.export()
    except GoogleScholarExportException, ex:
        register_exception(alert_admin=True)
        write_message("%s Exception: %s" %(ex.get_error_message(), ex.get_inner_exception()))

    write_message("bibexport_sitemap: job %s finished." % jobname)

class GoogleScholarExporterOpenURL(GoogleScholarExporter):
    """Export data for google scholar via OpenURL"""

    def __init__(self, output_directory, jobname):
        """
        Constructor of GoogleScholarExporterOpenURL
        @param output_directory: directory where files will be placed.
        @type output_directory: string
        @param jobname: the name of the job to read the configuration
        @type jobname: string
        """
        GoogleScholarExporter.__init__(self, output_directory)
        job_config = ConfigParser()
        job_config.read(CFG_ETCDIR + os.sep + 'bibexport' + os.sep + jobname + '.cfg')
        ## FIXME: what if a collection has a ',' in its name
        self.electronic_holding_collections = job_config.get('export_job', 'electronic_holding_collections').split(',')
        self.print_holding_collections = job_config.get('export_job', 'print_holding_collections').split(',')
        self.electronic_link_label = job_config.get('export_job', 'electronic_link_label')
        self.other_link_label = job_config.get('export_job', 'other_link_label')
        self.patron_ip_range = job_config.get('export_job', 'patron_ip_range').split(',')
        self.openurl_options = job_config.get('export_job', 'openurl_options').split(',')
        self.keywords = job_config.get('export_job', 'keywords')
        self.all_fulltext_records = intbitset(run_sql('SELECT id_bibrec FROM bibrec_bibdoc JOIN bibdoc ON id_bibdoc=id WHERE status<>"DELETED"'))

    def export(self):
        """Export all records and records modified last month"""
        ALL_MONTH_FILE_NAME_PATTERN = "all"
        SPLIT_BY_RECORDS = 1000

        # Export all records
        all_electronic_records = self._get_all_electronic_records()
        all_print_records = self._get_all_print_records()
        all_records = all_electronic_records | all_print_records
        self._delete_files(self._output_directory, ALL_MONTH_FILE_NAME_PATTERN)
        self._split_records_into_files(list(all_records), SPLIT_BY_RECORDS, ALL_MONTH_FILE_NAME_PATTERN, self._output_directory)

    def _get_all_electronic_records(self):
        """
        Return all records which as at least a fulltext link,
        matching the criteria no matter of their modification date."""
        all_records = intbitset(perform_request_search(c=self.electronic_holding_collections))
        return self.all_fulltext_records & all_records

    def _get_all_print_records(self):
        """
        Return all records which has at least a print holding.
        """
        if CFG_CERN_SITE:
            pattern = "964__a:0*"
        else:
            pattern = ''
        return intbitset(perform_request_search(c=self.print_holding_collections, p=pattern))

    def _create_index_file(self, number_of_files, file_name_pattern, output_directory):
        """
        Creates institutional_links.xml file containing links to all files
        containing records.
        """

        try:
            index_file = open(output_directory + os.sep + file_name_pattern + "-institutional_links.xml", "w")
            print >> index_file, """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE institutional_links PUBLIC "-//GOOGLE//Institutional Links 1.0//EN" "http://scholar.google.com/scholar/institutional_links.dtd">
<institutional_links>
  <institution>%s</institution>""" % encode_for_xml(CFG_SITE_NAME)

            for lang, name in CFG_SITE_NAME_INTL.iteritems():
                print >> index_file, """\
  <institution lang="%s">%s</institution>""" % (encode_for_xml(lang), encode_for_xml(name))
            if self.keywords:
                print >> index_file, """\
  <keywords>%s</keywords>""" % encode_for_xml(self.keywords)

            print >> index_file, """\
  <contact>%s</contact>""" % encode_for_xml(CFG_SITE_ADMIN_EMAIL)

            print >> index_file, """\
  <electronic_link_label>%s</electronic_link_label>
  <other_link_label>%s</other_link_label>""" % (encode_for_xml(self.electronic_link_label), encode_for_xml(self.other_link_label))

            print >> index_file, """\
  <openurl_base>%s</openurl_base>""" % encode_for_xml(CFG_SITE_URL + '/openurl')

            for option in self.openurl_options:
                print >> index_file, """\
  <openurl_option>%s</openurl_option>""" % encode_for_xml(option)

            for ip_range in self.patron_ip_range:
                print >> index_file, """\
  <patron_ip_range>%s</patron_ip_range>""" % encode_for_xml(ip_range)

            print >> index_file, """\
  <electronic_holdings>"""

            for file_number in xrange(1, number_of_files + 1):
                file_name = self._get_part_file_name(file_name_pattern, file_number)
                print >> index_file, """\
    <url>%s</url>""" % encode_for_xml(file_name)

            print >> index_file, """\
  </electronic_holdings>
</institutional_links>"""
        except (IOError, OSError), exception:
            register_exception(alert_admin=True)
            self._report_error("Failed to create index file.", exception)

        if index_file is not None:
            index_file.close()

    def _save_records_into_file(self, records, file_name, output_directory):
        """Save all the records into file in proper format (currently
        National Library of Medicine XML).

        file_name - the name of the file where records will be saved

        output_directory - directory where the file will be placed"""

        output_file = self._open_output_file(file_name, output_directory)
        print >> output_file, """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE institutional_holdings PUBLIC "-//GOOGLE//Institutional Holdings 1.0//EN" "http://scholar.google.com/scholar/institutional_holdings.dtd">
<institutional_holdings>"""

        for recid in records:
            record = get_record(recid)
            title = record_get_field_value(record, '245', ' ', ' ', 'a')
            isbn = record_get_field_value(record, '020', ' ', ' ', 'a')
            if title:
                if recid in self.all_fulltext_records:
                    print >> output_file, """\
  <item type="electronic">"""
                else:
                    print >> output_file, """\
  <item type="print">"""
                print >> output_file, """\
    <title>%s</title>""" % encode_for_xml(title)
                if isbn:
                    print >> output_file, """\
    <isbn>%s</isbn>""" % encode_for_xml(isbn)
                print >> output_file, """\
  </item>"""

        print >> output_file, """\
</institutional_holdings>"""

        self._close_output_file(output_file)
