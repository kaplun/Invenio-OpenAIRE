## -*- mode: python; coding: utf-8; -*-
##
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

"""
Invenio garbage collector.
"""

__revision__ = "$Id$"

import sys
import datetime
import time
import os
try:
    from invenio.dbquery import run_sql
    from invenio.config import CFG_LOGDIR, CFG_TMPDIR, CFG_CACHEDIR, \
         CFG_WEBSEARCH_RSS_TTL, \
         CFG_WEBSESSION_NOT_CONFIRMED_EMAIL_ADDRESS_EXPIRE_IN_DAYS
    from invenio.bibtask import task_init, task_set_option, task_get_option, \
         write_message, write_messages
    from invenio.access_control_mailcookie import mail_cookie_gc
    from invenio.bibdocfile import BibDoc
    from invenio.bibsched import gc_tasks
except ImportError, e:
    print "Error: %s" % (e, )
    sys.exit(1)

# configure variables
CFG_MYSQL_ARGUMENTLIST_SIZE = 100
# After how many days to remove obsolete log/err files
CFG_MAX_ATIME_RM_LOG = 28
# After how many days to zip obsolete log/err files
CFG_MAX_ATIME_ZIP_LOG = 7
# After how many days to remove obsolete bibreformat fmt xml files
CFG_MAX_ATIME_RM_FMT = 28
# After how many days to zip obsolete bibreformat fmt xml files
CFG_MAX_ATIME_ZIP_FMT = 7
# After how many days to remove obsolete bibharvest fmt xml files
CFG_MAX_ATIME_RM_OAI = 28
# After how many days to zip obsolete bibharvest fmt xml files
CFG_MAX_ATIME_ZIP_OAI = 7
# After how many days to remove deleted bibdocs
CFG_DELETED_BIBDOC_MAXLIFE = 365*10
# AFter how many day to remove old cached webjournal files
CFG_WEBJOURNAL_TTL = 7


def gc_exec_command(command):
    """ Exec the command logging in appropriate way its output."""
    write_message('  %s' % command, verbose=9)
    (dummy, output, errors) = os.popen3(command)
    write_messages(errors.read())
    write_messages(output.read())

def clean_logs():
    """ Clean the logs from obsolete files. """
    write_message("""CLEANING OF LOG FILES STARTED""")
    write_message("- deleting/gzipping bibsched empty/old err/log "
            "BibSched files")
    vstr = task_get_option('verbose') > 1 and '-v' or ''
    gc_exec_command('find %s -name "bibsched_task_*"'
        ' -size 0c -exec rm %s -f {} \;' \
            % (CFG_LOGDIR, vstr))
    gc_exec_command('find %s -name "bibsched_task_*"'
        ' -atime +%s -exec rm %s -f {} \;' \
            % (CFG_LOGDIR, CFG_MAX_ATIME_RM_LOG, vstr))
    gc_exec_command('find %s -name "bibsched_task_*"'
        ' -atime +%s -exec gzip %s -9 {} \;' \
            % (CFG_LOGDIR, CFG_MAX_ATIME_ZIP_LOG, vstr))

    write_message("- deleting/gzipping temporary empty/old "
            "BibReformat xml files")
    gc_exec_command('find %s -name "rec_fmt_*"'
        ' -size 0c -exec rm %s -f {} \;' \
            % (CFG_TMPDIR, vstr))
    gc_exec_command('find %s -name "rec_fmt_*"'
        ' -atime +%s -exec rm %s -f {} \;' \
            % (CFG_TMPDIR, CFG_MAX_ATIME_RM_FMT, vstr))
    gc_exec_command('find %s -name "rec_fmt_*"'
        ' -atime +%s -exec gzip %s -9 {} \;' \
            % (CFG_TMPDIR, CFG_MAX_ATIME_ZIP_FMT, vstr))

    write_message("- deleting/gzipping temporary old "
            "BibHarvest xml files")
    gc_exec_command('find %s -name "bibharvestadmin.*"'
        ' -exec rm %s -f {} \;' \
            % (CFG_TMPDIR, vstr))
    gc_exec_command('find %s -name "bibconvertrun.*"'
        ' -exec rm %s -f {} \;' \
            % (CFG_TMPDIR, vstr))
    gc_exec_command('find %s -name "oaiharvest*"'
        ' -atime +%s -exec gzip %s -9 {} \;' \
            % (CFG_TMPDIR, CFG_MAX_ATIME_ZIP_OAI, vstr))
    gc_exec_command('find %s -name "oaiharvest*"'
        ' -atime +%s -exec rm %s -f {} \;' \
            % (CFG_TMPDIR, CFG_MAX_ATIME_RM_OAI, vstr))
    gc_exec_command('find %s -name "oai_archive*"'
        ' -atime +%s -exec rm %s -f {} \;' \
            % (CFG_TMPDIR, CFG_MAX_ATIME_RM_OAI, vstr))
    write_message("""CLEANING OF LOG FILES FINISHED""")

def clean_cache():
    """Clean the cache for expired and old files."""
    write_message("""CLEANING OF OLD CACHED RSS REQUEST STARTED""")
    rss_cache_dir = "%s/rss/" % CFG_CACHEDIR
    try:
        filenames = os.listdir(rss_cache_dir)
    except OSError:
        filenames = []
    count = 0
    for filename in filenames:
        filename = os.path.join(rss_cache_dir, filename)
        last_update_time = datetime.datetime.fromtimestamp(os.stat(os.path.abspath(filename)).st_mtime)
        if not (datetime.datetime.now() < last_update_time + datetime.timedelta(minutes=CFG_WEBSEARCH_RSS_TTL)):
            try:
                os.remove(filename)
                count += 1
            except OSError, e:
                write_message("Error: %s" % e)
    write_message("""%s rss cache file pruned out of %s.""" % (count, len(filenames)))
    write_message("""CLEANING OF OLD CACHED RSS REQUEST FINISHED""")

    write_message("""CLEANING OF OLD CACHED WEBJOURNAL FILES STARTED""")
    webjournal_cache_dir = "%s/webjournal/" % CFG_CACHEDIR
    try:
        filenames = os.listdir(webjournal_cache_dir)
    except OSError:
        filenames = []
    count = 0
    for filename in filenames:
        filename = os.path.join(webjournal_cache_dir, filename)
        last_update_time = datetime.datetime.fromtimestamp(os.stat(os.path.abspath(filename)).st_mtime)
        if not (datetime.datetime.now() < last_update_time + datetime.timedelta(days=CFG_WEBJOURNAL_TTL)):
            try:
                os.remove(filename)
                count += 1
            except OSError, e:
                write_message("Error: %s" % e)
    write_message("""%s webjournal cache file pruned out of %s.""" % (count, len(filenames)))
    write_message("""CLEANING OF OLD CACHED WEBJOURNAL FILES FINISHED""")


def clean_bibxxx():
    """
    Clean unreferenced bibliographic values from bibXXx tables.
    This is useful to prettify browse results, as it removes
    old, no longer used values.

    WARNING: this function must be run only when no bibupload is
    running and/or sleeping.
    """
    write_message("""CLEANING OF UNREFERENCED bibXXx VALUES STARTED""")
    for xx in range(0, 100):
        bibxxx = 'bib%02dx' % xx
        bibrec_bibxxx = 'bibrec_bib%02dx' % xx
        if task_get_option('verbose') >= 9:
            num_unref_values = run_sql("""SELECT COUNT(*) FROM %(bibxxx)s
                     LEFT JOIN %(bibrec_bibxxx)s
                            ON %(bibxxx)s.id=%(bibrec_bibxxx)s.id_bibxxx
                     WHERE %(bibrec_bibxxx)s.id_bibrec IS NULL""" % \
                        {'bibxxx': bibxxx,
                         'bibrec_bibxxx': bibrec_bibxxx,})[0][0]
        run_sql("""DELETE %(bibxxx)s FROM %(bibxxx)s
                     LEFT JOIN %(bibrec_bibxxx)s
                            ON %(bibxxx)s.id=%(bibrec_bibxxx)s.id_bibxxx
                     WHERE %(bibrec_bibxxx)s.id_bibrec IS NULL""" % \
                        {'bibxxx': bibxxx,
                         'bibrec_bibxxx': bibrec_bibxxx,})
        if task_get_option('verbose') >= 9:
            write_message(""" - %d unreferenced %s values cleaned""" % \
                          (num_unref_values, bibxxx))
    write_message("""CLEANING OF UNREFERENCED bibXXx VALUES FINISHED""")

def clean_documents():
    """Delete all the bibdocs that have been set as deleted and have not been
    modified since CFG_DELETED_BIBDOC_MAXLIFE days. Returns the number of
    bibdocs involved."""
    write_message("""CLEANING OF OBSOLETED DELETED DOCUMENTS STARTED""")
    write_message("select id from bibdoc where status='DELETED' and NOW()>ADDTIME(modification_date, '%s 0:0:0')" % CFG_DELETED_BIBDOC_MAXLIFE, verbose=9)
    records = run_sql("select id from bibdoc where status='DELETED' and NOW()>ADDTIME(modification_date, '%s 0:0:0')" % CFG_DELETED_BIBDOC_MAXLIFE)
    for record in records:
        bibdoc = BibDoc(record[0])
        bibdoc.expunge()
        write_message("DELETE FROM bibdoc WHERE id=%i" % int(record[0]), verbose=9)
        run_sql("DELETE FROM bibdoc WHERE id=%s", (record[0], ))
    write_message("""%s obsoleted deleted documents cleaned""" % len(records))
    write_message("""CLEANING OF OBSOLETED DELETED DOCUMENTS FINISHED""")
    return len(records)

def guest_user_garbage_collector():
    """Session Garbage Collector

    program flow/tasks:
    1: delete expired sessions
    1b:delete guest users without session
    2: delete queries not attached to any user
    3: delete baskets not attached to any user
    4: delete alerts not attached to any user
    5: delete expired mailcookies
    5b: delete expired not confirmed email address
    6: delete expired roles memberships

    verbose - level of program output.
              0 - nothing
              1 - default
              9 - max, debug"""

    # dictionary used to keep track of number of deleted entries
    delcount = {'session': 0,
                'user': 0,
                'user_query': 0,
                'query': 0,
                'bskBASKET': 0,
                'user_bskBASKET': 0,
                'bskREC': 0,
                'bskRECORDCOMMENT': 0,
                'bskEXTREC': 0,
                'bskEXTFMT': 0,
                'user_query_basket': 0,
                'mail_cookie': 0,
                'email_addresses': 0,
                'role_membership' : 0}

    write_message("CLEANING OF GUEST SESSIONS STARTED")

    # 1 - DELETE EXPIRED SESSIONS
    write_message("- deleting expired sessions")
    timelimit = time.time()
    write_message("  DELETE FROM session WHERE"
        " session_expiry < %d \n" % (timelimit, ), verbose=9)
    delcount['session'] += run_sql("DELETE FROM session WHERE"
        " session_expiry < %s """ % (timelimit, ))


    # 1b - DELETE GUEST USERS WITHOUT SESSION
    write_message("- deleting guest users without session")

    # get uids
    write_message("""  SELECT u.id\n  FROM user AS u LEFT JOIN session AS s\n  ON u.id = s.uid\n  WHERE s.uid IS NULL AND u.email = ''""", verbose=9)

    result = run_sql("""SELECT u.id
    FROM user AS u LEFT JOIN session AS s
    ON u.id = s.uid
    WHERE s.uid IS NULL AND u.email = ''""")
    write_message(result, verbose=9)

    if result:
        # work on slices of result list in case of big result
        for i in range(0, len(result), CFG_MYSQL_ARGUMENTLIST_SIZE):
            # create string of uids
            uidstr = ''
            for (id_user, ) in result[i:i+CFG_MYSQL_ARGUMENTLIST_SIZE]:
                if uidstr: uidstr += ','
                uidstr += "%s" % (id_user, )

            # delete users
            write_message("  DELETE FROM user WHERE"
                " id IN (TRAVERSE LAST RESULT) AND email = '' \n", verbose=9)
            delcount['user'] += run_sql("DELETE FROM user WHERE"
                " id IN (%s) AND email = ''" % (uidstr, ))


    # 2 - DELETE QUERIES NOT ATTACHED TO ANY USER

    # first step, delete from user_query
    write_message("- deleting user_queries referencing"
        " non-existent users")

    # find user_queries referencing non-existent users
    write_message("  SELECT DISTINCT uq.id_user\n"
        "  FROM user_query AS uq LEFT JOIN user AS u\n"
        "  ON uq.id_user = u.id\n  WHERE u.id IS NULL", verbose=9)
    result = run_sql("""SELECT DISTINCT uq.id_user
        FROM user_query AS uq LEFT JOIN user AS u
        ON uq.id_user = u.id
        WHERE u.id IS NULL""")
    write_message(result, verbose=9)


    # delete in user_query one by one
    write_message("  DELETE FROM user_query WHERE"
        " id_user = 'TRAVERSE LAST RESULT' \n", verbose=9)
    for (id_user, ) in result:
        delcount['user_query'] += run_sql("""DELETE FROM user_query
            WHERE id_user = %s""" % (id_user, ))

    # delete the actual queries
    write_message("- deleting queries not attached to any user")

    # select queries that must be deleted
    write_message("""  SELECT DISTINCT q.id\n  FROM query AS q LEFT JOIN user_query AS uq\n  ON uq.id_query = q.id\n  WHERE uq.id_query IS NULL AND\n  q.type <> 'p' """, verbose=9)
    result = run_sql("""SELECT DISTINCT q.id
                        FROM query AS q LEFT JOIN user_query AS uq
                        ON uq.id_query = q.id
                        WHERE uq.id_query IS NULL AND
                              q.type <> 'p'""")
    write_message(result, verbose=9)

    # delete queries one by one
    write_message("""  DELETE FROM query WHERE id = 'TRAVERSE LAST RESULT \n""", verbose=9)
    for (id_user, ) in result:
        delcount['query'] += run_sql("""DELETE FROM query WHERE id = %s""", (id_user, ))


    # 3 - DELETE BASKETS NOT OWNED BY ANY USER
    write_message("- deleting baskets not owned by any user")

    # select basket ids
    write_message(""" SELECT ub.id_bskBASKET\n  FROM user_bskBASKET AS ub LEFT JOIN user AS u\n  ON u.id = ub.id_user\n  WHERE u.id IS NULL""", verbose=9)
    try:
        result = run_sql("""SELECT ub.id_bskBASKET
                              FROM user_bskBASKET AS ub LEFT JOIN user AS u
                                ON u.id = ub.id_user
                             WHERE u.id IS NULL""")
    except:
        result = []
    write_message(result, verbose=9)

    # delete from user_basket and basket one by one
    write_message("""  DELETE FROM user_bskBASKET WHERE id_bskBASKET = 'TRAVERSE LAST RESULT' """, verbose=9)
    write_message("""  DELETE FROM bskBASKET WHERE id = 'TRAVERSE LAST RESULT' """, verbose=9)
    write_message("""  DELETE FROM bskREC WHERE id_bskBASKET = 'TRAVERSE LAST RESULT'""", verbose=9)
    write_message("""  DELETE FROM bskRECORDCOMMENT WHERE id_bskBASKET = 'TRAVERSE LAST RESULT' \n""", verbose=9)
    for (id_basket, ) in result:
        delcount['user_bskBASKET'] += run_sql("""DELETE FROM user_bskBASKET WHERE id_bskBASKET = %s""", (id_basket, ))
        delcount['bskBASKET'] += run_sql("""DELETE FROM bskBASKET WHERE id = %s""", (id_basket, ))
        delcount['bskREC'] += run_sql("""DELETE FROM bskREC WHERE id_bskBASKET = %s""", (id_basket, ))
        delcount['bskRECORDCOMMENT'] += run_sql("""DELETE FROM bskRECORDCOMMENT WHERE id_bskBASKET = %s""", (id_basket, ))
    write_message(""" SELECT DISTINCT ext.id, rec.id_bibrec_or_bskEXTREC FROM bskEXTREC AS ext \nLEFT JOIN bskREC AS rec ON ext.id=-rec.id_bibrec_or_bskEXTREC WHERE id_bibrec_or_bskEXTREC is NULL""", verbose=9)
    try:
        result = run_sql("""SELECT DISTINCT ext.id FROM bskEXTREC AS ext
                            LEFT JOIN bskREC AS rec ON ext.id=-rec.id_bibrec_or_bskEXTREC
                            WHERE id_bibrec_or_bskEXTREC is NULL""")
    except:
        result = []
    write_message(result, verbose=9)
    write_message("""  DELETE FROM bskEXTREC WHERE id = 'TRAVERSE LAST RESULT' """, verbose=9)
    write_message("""  DELETE FROM bskEXTFMT WHERE id_bskEXTREC = 'TRAVERSE LAST RESULT' \n""", verbose=9)
    for (id_basket, ) in result:
        delcount['bskEXTREC'] += run_sql("""DELETE FROM bskEXTREC WHERE id=%s""", (id_basket,))
        delcount['bskEXTFMT'] += run_sql("""DELETE FROM bskEXTFMT WHERE id_bskEXTREC=%s""", (id_basket,))

    # 4 - DELETE ALERTS NOT OWNED BY ANY USER
    write_message('- deleting alerts not owned by any user')

    # select user ids in uqb that reference non-existent users
    write_message("""SELECT DISTINCT uqb.id_user FROM user_query_basket AS uqb LEFT JOIN user AS u ON uqb.id_user = u.id WHERE u.id IS NULL""", verbose=9)
    result = run_sql("""SELECT DISTINCT uqb.id_user FROM user_query_basket AS uqb LEFT JOIN user AS u ON uqb.id_user = u.id WHERE u.id IS NULL""")
    write_message(result, verbose=9)

    # delete all these entries
    for (id_user, ) in result:
        write_message("""DELETE FROM user_query_basket WHERE id_user = 'TRAVERSE LAST RESULT """, verbose=9)
        delcount['user_query_basket'] += run_sql("""DELETE FROM user_query_basket WHERE id_user = %s """, (id_user, ))

    # 5 - delete expired mailcookies
    write_message("""mail_cookie_gc()""", verbose=9)
    delcount['mail_cookie'] = mail_cookie_gc()

    ## 5b - delete expired not confirmed email address
    write_message("""DELETE FROM user WHERE note='2' AND NOW()>ADDTIME(last_login, '%s 0:0:0')""" % CFG_WEBSESSION_NOT_CONFIRMED_EMAIL_ADDRESS_EXPIRE_IN_DAYS, verbose=9)
    delcount['email_addresses'] = run_sql("""DELETE FROM user WHERE note='2' AND NOW()>ADDTIME(last_login, '%s 0:0:0')""" % CFG_WEBSESSION_NOT_CONFIRMED_EMAIL_ADDRESS_EXPIRE_IN_DAYS)

    # 6 - delete expired roles memberships
    write_message("""DELETE FROM user_accROLE WHERE expiration<NOW()""", verbose=9)
    delcount['role_membership'] = run_sql("""DELETE FROM user_accROLE WHERE expiration<NOW()""")

    # print STATISTICS
    write_message("""- statistics about deleted data: """)
    write_message("""  %7s sessions.""" % (delcount['session'], ))
    write_message("""  %7s users.""" % (delcount['user'], ))
    write_message("""  %7s user_queries.""" % (delcount['user_query'], ))
    write_message("""  %7s queries.""" % (delcount['query'], ))
    write_message("""  %7s baskets.""" % (delcount['bskBASKET'], ))
    write_message("""  %7s user_baskets.""" % (delcount['user_bskBASKET'], ))
    write_message("""  %7s basket_records.""" % (delcount['bskREC'], ))
    write_message("""  %7s basket_external_records.""" % (delcount['bskEXTREC'], ))
    write_message("""  %7s basket_external_formats.""" % (delcount['bskEXTFMT'], ))
    write_message("""  %7s basket_comments.""" % (delcount['bskRECORDCOMMENT'], ))
    write_message("""  %7s user_query_baskets.""" % (delcount['user_query_basket'], ))
    write_message("""  %7s mail_cookies.""" % (delcount['mail_cookie'], ))
    write_message("""  %7s non confirmed email addresses.""" % delcount['email_addresses'])
    write_message("""  %7s role_memberships.""" % (delcount['role_membership'], ))
    write_message("""CLEANING OF GUEST SESSIONS FINISHED""")

def main():
    """Main that construct all the bibtask."""
    task_init(authorization_action='runinveniogc',
            authorization_msg="InvenioGC Task Submission",
            help_specific_usage="  -l, --logs\t\tClean old logs and temporary files.\n" \
                "  -g, --guests\t\tClean expired guest user related information. [default action]\n" \
                "  -b, --bibxxx\t\tClean unreferenced bibliographic values in bibXXx tables.\n" \
                "  -c, --cache\t\tClean cache by removing old files.\n" \
                "  -d, --documents\tClean deleted documents and revisions older than %s days.\n" \
                "  -T, --tasks\t\tClean the BibSched queue removing/archiving old DONE tasks.\n" \
                "  -a, --all\t\tClean all of the above.\n" % CFG_DELETED_BIBDOC_MAXLIFE,
            version=__revision__,
            specific_params=("lgbdacT", ["logs", "guests", "bibxxx", "documents", "all", "cache", "tasks"]),
            task_submit_elaborate_specific_parameter_fnc=task_submit_elaborate_specific_parameter,
            task_submit_check_options_fnc=task_submit_check_options,
            task_run_fnc=task_run_core)

def task_submit_check_options():
    if not task_get_option('logs') and \
       not task_get_option('guests') and \
       not task_get_option('bibxxx') and \
       not task_get_option('documents') and \
       not task_get_option('cache') and \
       not task_get_option('tasks'):
        task_set_option('sessions', True)
    return True

def task_submit_elaborate_specific_parameter(key, value, opts, args):
    """ Given the string key it checks it's meaning, eventually using the
    value. Usually it fills some key in the options dict.
    It must return True if it has elaborated the key, False, if it doesn't
    know that key.
    eg:
    if key in ['-n', '--number']:
        self.options['number'] = value
        return True
    return False
    """
    if key in ('-l', '--logs'):
        task_set_option('logs', True)
        return True
    elif key in ('-g', '--guests'):
        task_set_option('guests', True)
        return True
    elif key in ('-b', '--bibxxx'):
        task_set_option('bibxxx', True)
        return True
    elif key in ('-d', '--documents'):
        task_set_option('documents', True)
        return True
    elif key in ('-c', '--cache'):
        task_set_option('cache', True)
        return True
    elif key in ('-t', '--tasks'):
        task_set_option('tasks', True)
        return True
    elif key in ('-a', '--all'):
        task_set_option('logs', True)
        task_set_option('guests', True)
        task_set_option('bibxxx', True)
        task_set_option('documents', True)
        task_set_option('cache', True)
        task_set_option('tasks', True)
        return True
    return False

def task_run_core():
    """ Reimplement to add the body of the task."""
    if task_get_option('guests'):
        guest_user_garbage_collector()
    if task_get_option('logs'):
        clean_logs()
    if task_get_option('bibxxx'):
        clean_bibxxx()
    if task_get_option('documents'):
        clean_documents()
    if task_get_option('cache'):
        clean_cache()
    if task_get_option('tasks'):
        gc_tasks()
    return True

if __name__ == '__main__':
    main()
