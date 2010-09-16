#!/usr/bin/env python

from invenio.bibtask import write_message, task_update_progress
from invenio.dbquery import run_sql
from invenio.bibknowledge import add_kb_mapping, kb_exists, update_kb_mapping, add_kb, kb_mapping_exists, add_kb_mapping, remove_kb_mapping, get_kbr_keys
from invenio.dnetutils import dnet_run_sql
from invenio.errorlib import register_exception

import datetime
import urllib
import json

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)


def _init_journals():
    import gzip
    run_sql(gzip.open("journals.sql.gz").read())

CFG_JOURNAL_KBS = {
    'journal_issn': 'SELECT name, issn FROM journals_journal',
    'journal_essn': 'SELECT name, essn FROM journals_journal',
    'journal_publisher': 'SELECT journals_journal.name, journals_publisher.name FROM journals_journal JOIN journals_publisher ON journals_journal.publisher_id=journals_publisher.id',
    'journal_name': 'SELECT journals_journal.name, journals_variantname.name FROM journals_journal JOIN journals_variantname ON journals_journal.id=journals_variantname.journal_id'
}

CFG_DNET_KBS = {
    #'project_acronym': 'SELECT grant_agreement_number, acronym FROM projects',
    #'project_title': 'SELECT grant_agreement_number, title FROM projects',
    #'json_projects': """SELECT grant_agreement_number,*
        #FROM projects
            #LEFT OUTER JOIN projects_projectsubjects ON project=projectid
            #LEFT OUTER JOIN projectsubjects ON project_subject=projectsubjectid
            #LEFT OUTER JOIN projects_contracttypes ON projects_contracttypes.project=projectid
            #LEFT OUTER JOIN contracttypes ON contracttype=contracttypeid
            #LEFT OUTER JOIN participants_projects ON participants_projects.project=projectid
            #LEFT OUTER JOIN participants ON beneficiaryid=participant
    #""",
    'json_projects': """SELECT projectid,grant_agreement_number,ec_project_website,acronym,call_identifier,end_date,start_date,title,fundedby FROM projects""",
    'projects': "SELECT grant_agreement_number, acronym || ' - ' || title || ' (' || grant_agreement_number || ')' FROM projects",
    'project_subjects': "SELECT project, project_subject FROM projects_projectsubjects",
    'languages': "SELECT languageid, name FROM languages"
}


def load_kbs(cfg, run_sql):
    for kb, query in cfg.iteritems():
        if not kb_exists(kb):
            add_kb(kb)
        write_message("Updating %s KB..." % kb)
        try:
            if kb.startswith('json_'):
                encoder = ComplexEncoder()
                mapping, description = run_sql(query, with_desc=True)
                column_counter = {}
                new_description = []
                for column in description[1:]:
                    column = column[0]
                    counter = column_counter[column] = column_counter.get(column, 0) + 1
                    if counter > 1:
                        new_description.append('%s%d' % (column, counter))
                    else:
                        new_description.append(column)
                description = new_description
            else:
                mapping = run_sql(query)
            original_keys = set([key[0] for key in get_kbr_keys(kb)])
            for i, row in enumerate(mapping):
                key, value = row[0], row[1:]
                print key, value
                if kb.startswith('json_'):
                    value = encoder.encode(dict(zip(description, value)))
                else:
                    value = value[0]
                print value
                if value:
                    if key in original_keys:
                        original_keys.remove(key)
                    task_update_progress("%s - %s%%" % (kb, i * 100 / len(mapping)))
                    if kb_mapping_exists(kb, key):
                        update_kb_mapping(kb, key, key, value)
                    else:
                        add_kb_mapping(kb, key, value)
            task_update_progress("Cleaning %s" % kb)
            for key in original_keys:
                remove_kb_mapping(kb, key)
        except:
            raise
            register_exception(alert_admin=True, prefix="Error when updating KB %s" % kb)
            continue


def bst_load_OpenAIRE_kbs(journals=False):
    load_kbs(CFG_DNET_KBS, dnet_run_sql)
    if journals:
        load_kbs(CFG_JOURNAL_KBS, run_sql)

if __name__ == '__main__':
    bst_load_OpenAIRE_kbs(journals=True)