# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2011 CERN.
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
'''
Bibauthorid_webapi
Point of access to the documents clustering facility.
Provides utilities to safely interact with stored data.
'''

import invenio.bibauthorid_personid_tables_utils as tu
import invenio.bibauthorid_tables_utils as tu0
import invenio.bibauthorid_config as bconfig
import invenio.bibauthorid_utils as bu
import invenio.bibauthorid_authorname_utils as bau
import invenio.search_engine as search_engine

from cgi import escape
from time import gmtime, strftime, ctime
from invenio.bibauthorid_utils import get_field_values_on_condition
from invenio.dbquery import OperationalError
from invenio.access_control_admin import acc_find_user_role_actions
from invenio.webuser import collect_user_info, get_session, getUid
from invenio.webuser import isUserSuperAdmin
from invenio.access_control_engine import acc_authorize_action
from invenio.access_control_admin import acc_get_role_id, acc_get_user_roles
from invenio.external_authentication_robot import ExternalAuthRobot
from invenio.external_authentication_robot import load_robot_keys
from invenio.config import CFG_BIBAUTHORID_AUTHOR_TICKET_ADMIN_EMAIL
from invenio.config import CFG_SITE_URL
from invenio.mailutils import send_email


def get_person_redirect_link(pid):
    '''
    Returns the canonical name of a pid if found, the pid itself otherwise
    @param pid: int
    '''
    cname = tu.get_canonical_id_from_personid(pid)
    if len(cname) > 0:
        return str(cname[0][0])
    else:
        return str(pid)


def get_person_id_from_canonical_id(canonical_id):
    '''
    Finds the person id from a canonical name (e.g. Ellis_J_R_1)

    @param canonical_id: the canonical ID
    @type canonical_id: string

    @return: result from the request or -1 on failure
    @rtype: int
    '''
    if not canonical_id or not isinstance(canonical_id, str):
        return - 1

    pid = -1

    try:
        pid = tu.get_person_id_from_canonical_id(canonical_id)[0][0]
    except IndexError:
        pass

    return pid


def get_bibrefs_from_bibrecs(bibreclist):
    '''
    Retrieve all bibrefs for all the recids in the list

    @param bibreclist: list of record IDs
    @type bibreclist: list of int

    @return: a list of record->bibrefs
    @return: list of lists
    '''
    lists = []
    for bibrec in bibreclist:
        lists.append([bibrec, tu.get_possible_bibrecref([''], bibrec,
                                                        always_match=True)])
    return lists


def get_possible_bibrefs_from_pid_bibrec(pid, bibreclist, always_match=False):
    '''
    Returns for each bibrec a list of bibrefs for which the surname matches.
    @param pid: person id to gather the names strings from
    @param bibreclist: list of bibrecs on which to search
    '''
    pid = wash_integer_id(pid)

    pid_names = tu.get_person_names_set([pid])
    lists = []
    for bibrec in bibreclist:
        lists.append([bibrec, tu.get_possible_bibrecref([n[0] for n in pid_names], bibrec,
                                                        always_match)])
    return lists


def get_pid_from_uid(uid):
    '''
    Return the PID associated with the uid

    @param uid: the internal ID of a user
    @type uid: int

    @return: the Person ID attached to the user or -1 if none found
    '''
    if not isinstance(uid, tuple):
        uid = ((uid,),)

    return tu.get_personid_from_uid(uid)


def get_user_level(uid):
    '''
    Finds and returns the aid-universe-internal numeric user level

    @param uid: the user's id
    @type uid: int

    @return: A numerical representation of the maximum access level of a user
    @rtype: int
    '''
    actions = [row[1] for row in acc_find_user_role_actions({'uid': uid})]
    return max([tu.resolve_paper_access_right(acc) for acc in actions])


def get_person_id_from_paper(bibref=None):
    '''
    Returns the id of the person who wrote the paper

    @param bibref: the bibref,bibrec pair that identifies the person
    @type bibref: str

    @return: the person id
    @rtype: int
    '''
    if not is_valid_bibref(bibref):
        return - 1

    person_id = -1
    db_data = tu.get_papers_status([(bibref,)])

    try:
        person_id = db_data[0][1]
    except (IndexError):
        pass

    return person_id


def get_papers_by_person_id(person_id= -1, rec_status= -2, ext_out=False):
    '''
    Returns all the papers written by the person

    @param person_id: identifier of the person to retrieve papers from
    @type person_id: int
    @param rec_status: minimal flag status a record must have to be displayed
    @type rec_status: int
    @param ext_out: Extended output (w/ author aff and date)
    @type ext_out: boolean

    @return: list of record ids
    @rtype: list of int
    '''
    if not isinstance(person_id, int):
        try:
            person_id = int(person_id)
        except (ValueError, TypeError):
            return []

    if person_id < 0:
        return []

    if not isinstance(rec_status, int):
        return []

    records = []
    db_data = tu.get_person_papers((person_id,),
                                   rec_status,
                                   show_author_name=True,
                                   show_title=False,
                                   show_rt_status=True)
    if not ext_out:
        records = [[row["data"].split(",")[1], row["data"], row["flag"],
                    row["authorname"]] for row in db_data]
    else:
        for row in db_data:
            recid = row["data"].split(",")[1]
            bibref = row["data"]
            flag = row["flag"]
            authorname = row["authorname"]
            rt_status = row['rt_status']
            gfoc = get_field_values_on_condition
            authoraff = ", ".join(gfoc(recid, ["100", "700"], "u", "a",
                                       authorname, source="API"))
            try:
                date = list(gfoc(recid, "269", "c"))[0]
            except (IndexError):
                date = ""

            records.append([recid, bibref, flag, authorname,
                            authoraff, date, rt_status])


    return records


def get_papers_cluster(bibref):
    '''
    Returns the cluster of documents connected with this one

    @param bibref: the table:bibref,bibrec pair to look for
    @type bibref: str

    @return: a list of record IDs
    @rtype: list of int
    '''
    papers = []
    person_id = get_person_id_from_paper(bibref)

    if person_id > -1:
        papers = get_papers_by_person_id(person_id)

    return papers

def get_person_request_ticket(pid= -1, tid=None):
    '''
    Returns the list of request tickets associated to a person.
    @param pid: person id
    @param tid: ticket id, to select if want to retrieve only a particular one
    @return: tickets [[],[]]
    '''
    if pid < 0:
        return []
    else:
        return tu.get_request_ticket(pid, ticket_id=tid)

def get_persons_with_open_tickets_list():
    '''
    Finds all the persons with open tickets and returns pids and count of tickets
    @return: [[pid,ticket_count]]
    '''
    return tu.get_persons_with_open_tickets_list()

def get_person_names_from_id(person_id= -1):
    '''
    Finds and returns the names associated with this person along with the
    frequency of occurrence (i.e. the number of papers)

    @param person_id: an id to find the names for
    @type person_id: int

    @return: name and number of occurrences of the name
    @rtype: tuple of tuple
    '''
#    #retrieve all rows for the person
    if (not person_id > -1) or (not isinstance(person_id, int)):
        return []

    return tu.get_person_names_count((person_id,))


def get_person_db_names_from_id(person_id= -1):
    '''
    Finds and returns the names associated with this person as stored in the
    meta data of the underlying data set along with the
    frequency of occurrence (i.e. the number of papers)

    @param person_id: an id to find the names for
    @type person_id: int

    @return: name and number of occurrences of the name
    @rtype: tuple of tuple
    '''
#    #retrieve all rows for the person
    if (not person_id > -1) or (not isinstance(person_id, int)):
        return []

    return tu.get_person_db_names_count((person_id,))


def get_longest_name_from_pid(person_id= -1):
    '''
    Finds the longest name of a person to be representative for this person.

    @param person_id: the person ID to look at
    @type person_id: int

    @return: returns the longest normalized name of a person
    @rtype: string
    '''
    if (not person_id > -1) or (not isinstance(person_id, int)):
        return "This doesn't look like a person ID!"

    longest_name = ""

    for name in tu.get_person_names_count((person_id,)):
        if name and len(name[0]) > len(longest_name):
            longest_name = name[0]

    if longest_name:
        return longest_name
    else:
        return "This person does not seem to have a name!"


def get_most_frequent_name_from_pid(person_id= -1):
    '''
    Finds the most frequent name of a person to be
    representative for this person.

    @param person_id: the person ID to look at
    @type person_id: int

    @return: returns the most frequent normalized name of a person
    @rtype: string
    '''
    if (not person_id > -1) or (not isinstance(person_id, int)):
        return "'%s' doesn't look like a person ID!" % person_id

    mf_name = ""

    try:
        nn = tu.get_person_names_count((person_id,))
        mf_name = sorted(nn, key=lambda k:k[1], reverse=True)[0][0]
    except IndexError:
        pass

    if mf_name:
        return mf_name
    else:
        return "This person does not seem to have a name!"


def get_paper_status(bibref):
    '''
    Finds an returns the status of a bibrec to person assignment

    @param bibref: the bibref-bibrec pair that unambiguously identifies a paper
    @type bibref: string
    '''
    db_data = tu.get_papers_status([[bibref]])
    #data,PersonID,flag
    status = None

    try:
        status = db_data[0][2]
    except IndexError:
        status = -10

    status = wash_integer_id(status)

    return status


def wash_integer_id(param_id):
    '''
    Creates an int out of either int or string

    @param param_id: the number to be washed
    @type param_id: int or string

    @return: The int representation of the param or -1
    @rtype: int
    '''
    pid = -1

    try:
        pid = int(param_id)
    except (ValueError, TypeError):
        return (-1)

    return pid


def is_valid_bibref(bibref):
    '''
    Determines if the provided string is a valid bibref-bibrec pair

    @param bibref: the bibref-bibrec pair that unambiguously identifies a paper
    @type bibref: string

    @return: True if it is a bibref-bibrec pair and False if it's not
    @rtype: boolean
    '''
    if (not isinstance(bibref, str)) or (not bibref):
        return False

    if not bibref.count(":"):
        return False

    if not bibref.count(","):
        return False

    try:
        table = bibref.split(":")[0]
        ref = bibref.split(":")[1].split(",")[0]
        bibrec = bibref.split(":")[1].split(",")[1]
    except IndexError:
        return False

    try:
        table = int(table)
        ref = int(ref)
        bibrec = int(bibrec)
    except (ValueError, TypeError):
        return False

    return True


def is_valid_canonical_id(cid):
    '''
    Checks if presented canonical ID is valid in structure
    Must be of structure: ([Initial|Name]\.)*Lastname\.Number
    Example of valid cid: J.Ellis.1

    @param cid: The canonical ID to check
    @type cid: string

    @return: Is it valid?
    @rtype: boolean
    '''
    if not cid.count("."):
        return False

    xcheck = -1
    sp = cid.split(".")

    if not (len(sp) > 1 and sp[-1]):
        return False

    try:
        xcheck = int(sp[-1])
    except (ValueError, TypeError, IndexError):
        return False

    if xcheck and xcheck > -1:
        return True
    else:
        return False


def confirm_person_bibref_assignments(person_id, bibrefs, uid):
    '''
    Confirms a bibref-bibrec assignment to a person. That internally
    raises the flag of the entry to 2, which means 'user confirmed' and
    sets the user level to the highest level of the user provided as param

    @param person_id: the id of the person to confirm the assignment to
    @type person_id: int
    @param bibrefs: the bibref-bibrec pairs that unambiguously identify records
    @type bibrefs: list of strings
    @param uid: the id of the user that arranges the confirmation
    @type uid: int

    @return: True if the process ran smoothly, False if there was an error
    @rtype: boolean
    '''
    pid = wash_integer_id(person_id)
    refs = []

    if pid < 0:
        return False

    if not isinstance(bibrefs, list) or not len(bibrefs):
        return False
    else:
        for bibref in bibrefs:
            if is_valid_bibref(bibref):
                refs.append((bibref,))
            else:
                return False

    try:
        tu.confirm_papers_to_person((pid,), refs, get_user_level(uid))
    except OperationalError:
        return False

    return True


def repeal_person_bibref_assignments(person_id, bibrefs, uid):
    '''
    Repeals a bibref-bibrec assignment from a person. That internally
    sets the flag of the entry to -2, which means 'user repealed' and
    sets the user level to the highest level of the user provided as param

    @param person_id: the id of the person to repeal the assignment from
    @type person_id: int
    @param bibrefs: the bibref-bibrec pairs that unambiguously identify records
    @type bibrefs: list of strings
    @param uid: the id of the user that arranges the repulsion
    @type uid: int

    @return: True if the process ran smoothly, False if there was an error
    @rtype: boolean
    '''
    pid = wash_integer_id(person_id)
    refs = []

    if pid < 0:
        return False

    if not isinstance(bibrefs, list) or not len(bibrefs):
        return False
    else:
        for bibref in bibrefs:
            if is_valid_bibref(bibref):
                refs.append((bibref,))
            else:
                return False

    try:
        tu.reject_papers_from_person((pid,), refs, get_user_level(uid))
    except OperationalError:
        return False

    return True


def reset_person_bibref_decisions(person_id, bibrefs):
    '''
    Resets a bibref-bibrec assignment of a person. That internally
    sets the flag of the entry to 0, which means 'no user interaction' and
    sets the user level to 0 to give the record free for claiming/curation

    @param person_id: the id of the person to reset the assignment from
    @type person_id: int
    @param bibrefs: the bibref-bibrec pairs that unambiguously identify records
    @type bibrefs: list of strings

    @return: True if the process ran smoothly, False if there was an error
    @rtype: boolean
    '''
    pid = wash_integer_id(person_id)
    refs = []

    if pid < 0:
        return False

    if not isinstance(bibrefs, list) or not len(bibrefs):
        return False
    else:
        for bibref in bibrefs:
            if is_valid_bibref(bibref):
                refs.append((bibref,))
            else:
                return False

    try:
        tu.reset_papers_flag((person_id,), refs)
    except OperationalError:
        return False

    return True


def add_person_comment(person_id, message):
    '''
    Adds a comment to a person after enriching it with meta-data (date+time)

    @param person_id: person id to assign the comment to
    @type person_id: int
    @param message: defines the comment to set
    @type message: string

    @return the message incl. the metadata if everything was fine, False on err
    @rtype: string or boolean
    '''
    msg = ""
    pid = -1
    try:
        msg = str(message)
        pid = int(person_id)
    except (ValueError, TypeError):
        return False

    strtimestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    msg = escape(msg, quote=True)
    dbmsg = "%s;;;%s" % (strtimestamp, msg)
    tu.set_person_data(pid, "comment", dbmsg)

    return dbmsg


def get_person_comments(person_id):
    '''
    Get all comments from a person

    @param person_id: person id to get the comments from
    @type person_id: int

    @return the message incl. the metadata if everything was fine, False on err
    @rtype: string or boolean
    '''
    pid = -1
    comments = []

    try:
        pid = int(person_id)
    except (ValueError, TypeError):
        return False

    for row in tu.get_person_data(pid, "comment"):
        comments.append(row[1])

    return comments


def search_person_ids_by_name(namequery):
    '''
    Prepares the search to search in the database

    @param namequery: the search query the user enquired
    @type namequery: string

    @return: information about the result w/ probability and occurrence
    @rtype: tuple of tuple
    '''
    query = ""
    escaped_query = ""

    try:
        query = str(namequery)
    except (ValueError, TypeError):
        return []

    if query:
        escaped_query = escape(query, quote=True)
    else:
        return []

    return tu.find_personIDs_by_name_string(escaped_query)


def log(userinfo, personid, action, tag, value, comment='', transactionid=0):
    '''
    Log an action performed by a user

    Examples (in the DB):
    1 2010-09-30 19:30  admin||10.0.0.1  1  assign  paper  1133:4442 'from 23'
    1 2010-09-30 19:30  admin||10.0.0.1  1  assign  paper  8147:4442
    2 2010-09-30 19:35  admin||10.0.0.1  1  reject  paper  72:4442

    @param userinfo: information about the user [UID|IP]
    @type userinfo: string
    @param personid: ID of the person this action is targeting
    @type personid: int
    @param action: intended action
    @type action: string
    @param tag: A tag to describe the data entered
    @type tag: string
    @param value: The value of the action described by the tag
    @type value: string
    @param comment: Optional comment to describe the transaction
    @type comment: string
    @param transactionid: May group bulk operations together
    @type transactionid: int

    @return: Returns the current transactionid
    @rtype: int
    '''
    userinfo = escape(str(userinfo))
    action = escape(str(action))
    tag = escape(str(tag))
    value = escape(str(value))
    comment = escape(str(comment))

    if not isinstance(personid, int):
        try:
            personid = int(personid)
        except (ValueError, TypeError):
            return - 1

    if not isinstance(transactionid, int):
        try:
            transactionid = int(transactionid)
        except (ValueError, TypeError):
            return - 1

    return tu.insert_user_log(userinfo, personid, action, tag,
                       value, comment, transactionid)


def user_can_modify_data(uid, pid):
    '''
    Determines if a user may modify the data of a person

    @param uid: the id of a user (invenio user id)
    @type uid: int
    @param pid: the id of a person
    @type pid: int

    @return: True if the user may modify data, False if not
    @rtype: boolean

    @raise ValueError: if the supplied parameters are invalid
    '''
    if not isinstance(uid, int):
        try:
            uid = int(uid)
        except (ValueError, TypeError):
            raise ValueError("User ID has to be a number!")

    if not isinstance(pid, int):
        try:
            pid = int(pid)
        except (ValueError, TypeError):
            raise ValueError("Person ID has to be a number!")

    return tu.user_can_modify_data(uid, pid)


def user_can_modify_paper(uid, paper):
    '''
    Determines if a user may modify the record assignments of a person

    @param uid: the id of a user (invenio user id)
    @type uid: int
    @param pid: the id of a person
    @type pid: int

    @return: True if the user may modify data, False if not
    @rtype: boolean

    @raise ValueError: if the supplied parameters are invalid
    '''
    if not isinstance(uid, int):
        try:
            uid = int(uid)
        except (ValueError, TypeError):
            raise ValueError("User ID has to be a number!")

    if not paper:
        raise ValueError("A bibref is expected!")

    return tu.user_can_modify_paper(uid, paper)


def person_bibref_is_touched(pid, bibref):
    '''
    Determines if an assignment has been touched by a user (i.e. check for
    the flag of an assignment being 2 or -2)

    @param pid: the id of the person to check against
    @type pid: int
    @param bibref: the bibref-bibrec pair that unambiguously identifies a paper
    @type bibref: string

    @raise ValueError: if the supplied parameters are invalid
    '''
    if not isinstance(pid, int):
        try:
            pid = int(pid)
        except (ValueError, TypeError):
            raise ValueError("Person ID has to be a number!")

    if not bibref:
        raise ValueError("A bibref is expected!")

    return tu.person_bibref_is_touched(pid, bibref)


def assign_uid_to_person(uid, pid, create_new_pid=False):
    '''
    Assign uid to person
    @param uid: uid
    @param pid: pid
    @param create_new_pid: forces creation of new person
    '''
    pid = wash_integer_id(pid)
    uid = wash_integer_id(uid)

    tu.assign_uid_to_person(uid, pid, create_new_pid)


def get_review_needing_records(pid):
    '''
    Returns list of records associated to pid which are in need of review
    (only bibrec ma no bibref selected)
    @param pid: pid
    '''
    pid = wash_integer_id(pid)
    db_data = tu.get_person_papers_to_be_manually_reviewed(pid)

    return [int(row[1]) for row in db_data if row[1]]


def add_review_needing_record(pid, bibrec_id):
    '''
    Add record in need of review to a person
    @param pid: pid
    @param bibrec_id: bibrec
    '''
    pid = wash_integer_id(pid)
    bibrec_id = wash_integer_id(bibrec_id)
    tu.add_person_paper_needs_manual_review(pid, bibrec_id)


def del_review_needing_record(pid, bibrec_id):
    '''
    Removes a record in need of review from a person
    @param pid: personid
    @param bibrec_id: bibrec
    '''
    pid = wash_integer_id(pid)
    bibrec_id = wash_integer_id(bibrec_id)
    tu.del_person_papers_needs_manual_review(pid, bibrec_id)


def get_processed_external_recids(pid):
    '''
    Get list of records that have been processed from external identifiers

    @param pid: Person ID to look up the info for
    @type pid: int

    @return: list of record IDs
    @rtype: list of strings
    '''

    list_str = tu.get_processed_external_recids(pid)

    return list_str.split(";")


def set_processed_external_recids(pid, recid_list):
    '''
    Set list of records that have been processed from external identifiers

    @param pid: Person ID to set the info for
    @type pid: int
    @param recid_list: list of recids
    @type recid_list: list of int
    '''
    if isinstance(recid_list, list):
        recid_list_str = ";".join(recid_list)

    tu.set_processed_external_recids(pid, recid_list_str)


def arxiv_login(req):
    '''
    Log in through arxive. If user already associated to a personid, returns the personid.
    If user has no pid, try to guess which personid to associate based on surname and papers
    from arxiv. If no compatible person is found, creates a new person.
    At the end of the process opens a ticket for the user claiming the papers from arxiv.
    !!! the user will find the open ticket, which will require him to go through the
    final review before getting committed.

    @param req: Apache request object
    @type req: Apache request object

    @return: Returns the pid resulting in the process
    @rtype: int
    '''
    def session_bareinit(req):
        session = get_session(req)
        try:
            pinfo = session["personinfo"]
            if 'ticket' not in pinfo:
                pinfo["ticket"] = []
        except KeyError:
            pinfo = dict()
            session['personinfo'] = pinfo
            pinfo["ticket"] = []
        session.save()

    session_bareinit(req)
    session = get_session(req)
    ticket = session['personinfo']['ticket']

    uid = getUid(req)
    curren_pid = tu.get_personid_from_uid([[uid]])
    if curren_pid[1]:
        return curren_pid[0][0]

    uinfo = collect_user_info(req)

    arxiv_p_ids = []
    name = ''
    surname = ''
    try:
        for i in  uinfo['external_arxivids'].split(';'):
            arxiv_p_ids.append(i)
        name = uinfo['external_firstname']
        surname = uinfo['external_familyname']
    #'external_arxivids': 'hep-th/0112017;hep-th/0112020',
    #'external_familyname': 'Weiler',
    #'external_firstname': 'Henning',
    except KeyError:
        pass

    found_bibrecs = []
    for arx in arxiv_p_ids:
        t = search_engine.perform_request_search(p='037:' + str(arx), of='id')
        for i in t:
            found_bibrecs.append(i)
    #found_bibrecs = [78]

    bibrec_names = []
    for b in found_bibrecs:
        bibrec_names.append([b, bu.get_field_values_on_condition(b, source='API', get_table=['100', '700'], get_tag='a')])

    for n in list(bibrec_names):
        for i in list(n[1]):
            if bau.soft_compare_names(surname, i.encode('utf-8')) < 0.4:
                n[1].remove(i)
    #bibrec_names = [[78, set([u'M\xfcck, W'])]]

    #what is left are only suitable names for each record.
    bibrefrecs = []

    for bibrec in bibrec_names:
        for name in bibrec[1]:
            bibrefs = tu0.get_bibrefs_from_name_string(name.encode('utf-8'))
            if len(bibrefs) < 1:
                continue
            for bibref in bibrefs[0][0].split(','):
                bibrefrecs.append(str(bibref) + ',' + str(bibrec[0]))
    #bibrefrec = ['100:116,78', '700:505,78']


    brr = [[i] for i in bibrefrecs]
    possible_persons = tu.get_possible_personids_from_paperlist(brr)
    #[[0L, ['700:316,10']]]
    possible_persons = sorted(possible_persons, key=lambda k: len(k[1]))

    person_papers = []
    if len(possible_persons) > 1:
        if len(possible_persons[0][1]) > len(possible_persons[1][1]):
            pid = tu.assign_person_to_uid(uid, possible_persons[0][0])
            person_papers = possible_persons[0][1]
        else:
            pid = tu.assign_person_to_uid(uid, -1)
    elif len(possible_persons) == 1:
        pid = tu.assign_person_to_uid(uid, possible_persons[0][0])
        person_papers = possible_persons[0][1]
    else:
        pid = tu.assign_person_to_uid(uid, -1)

    tempticket = []
    #now we have to open the tickets...
    for bibref in person_papers:
        tempticket.append({'pid':pid, 'bibref':bibref, 'action':'confirm'})

    done_bibrecs = [b.split(',')[1] for b in person_papers]
    for b in found_bibrecs:
        if str(b) not in done_bibrecs:
            tempticket.append({'pid':pid, 'bibref':str(b), 'action':'confirm'})

    #check if ticket targets (bibref for pid) are already in ticket
    for t in list(tempticket):
        for e in list(ticket):
            if e['pid'] == t['pid'] and e['bibref'] == t['bibref']:
                ticket.remove(e)
        ticket.append(t)
    session.save()
    return pid


def external_user_can_perform_action(uid):
    '''
    Check for SSO user and if external claims will affect the
    decision wether or not the user may use the Invenio claiming platform

    @param uid: the user ID to check permissions for
    @type uid: int

    @return: is user allowed to perform actions?
    @rtype: boolean
    '''
    #If no EXTERNAL_CLAIMED_RECORDS_KEY we bypass this check
    if not bconfig.EXTERNAL_CLAIMED_RECORDS_KEY:
        return True

    uinfo = collect_user_info(uid)
    keys = []
    for k in bconfig.EXTERNAL_CLAIMED_RECORDS_KEY:
        if k in uinfo:
            keys.append(k)

    full_key = False
    for k in keys:
        if uinfo[k]:
            full_key = True
            break

    return full_key

def is_external_user(uid):
    '''
    Check for SSO user and if external claims will affect the
    decision wether or not the user may use the Invenio claiming platform

    @param uid: the user ID to check permissions for
    @type uid: int

    @return: is user allowed to perform actions?
    @rtype: boolean
    '''
    #If no EXTERNAL_CLAIMED_RECORDS_KEY we bypass this check
    if not bconfig.EXTERNAL_CLAIMED_RECORDS_KEY:
        return False

    uinfo = collect_user_info(uid)
    keys = []
    for k in bconfig.EXTERNAL_CLAIMED_RECORDS_KEY:
        if k in uinfo:
            keys.append(k)

    full_key = False
    for k in keys:
        if uinfo[k]:
            full_key = True
            break

    return full_key

def check_transaction_permissions(uid, bibref, pid, action):
    '''
    Check if the user can perform the given action on the given pid,bibrefrec pair.
    return in: granted, denied, warning_granted, warning_denied

    @param uid: The internal ID of a user
    @type uid: int
    @param bibref: the bibref pair to check permissions for
    @type bibref: string
    @param pid: the Person ID to check on
    @type pid: int
    @param action: the action that is to be performed
    @type action: string

    @return: granted, denied, warning_granted xor warning_denied
    @rtype: string
    '''
    c_own = True
    c_override = False
    is_superadmin = False
    if isUserSuperAdmin({'uid': uid}):
        is_superadmin = True

    access_right = _resolve_maximum_acces_rights(uid)
    bibref_status = tu.get_bibref_modification_status(bibref)

    if bibref_status[0]:
        c_override = True

    uid_pid = tu.get_personid_from_uid([[uid]])
    if not uid_pid[1] or pid != uid_pid[0][0]:
        c_own = False

    #if we cannot override an already touched bibref, no need to go on checking
    if c_override:
        if is_superadmin:
            return 'warning_granted'
        if access_right[1] < bibref_status[1]:
            return "warning_denied"
    else:
        if is_superadmin:
            return 'granted'

    #let's check if invenio is allowing us the action we want to perform
    if c_own:
        action = bconfig.CLAIMPAPER_CLAIM_OWN_PAPERS
    else:
        action = bconfig.CLAIMPAPER_CLAIM_OTHERS_PAPERS
    auth = acc_authorize_action(uid, action)
    if auth[0] != 0:
        return "denied"

    #now we know if claiming for ourselfs, we can ask for external ideas
    if c_own:
        action = 'claim_own_paper'
    else:
        action = 'claim_other_paper'

    ext_permission = external_user_can_perform_action(uid)

    #if we are here invenio is allowing the thing and we are not overwriting a
    #user with higher privileges, if externals are ok we go on!
    if ext_permission:
        if not c_override:
            return "granted"
        else:
            return "warning_granted"

    return "denied"


def delete_request_ticket(pid, ticket):
    '''
    Delete a request ticket associated to a person
    @param pid: pid (int)
    @param ticket: ticket id (int)
    '''
    tu.delete_request_ticket(pid, ticket)


def delete_transaction_from_request_ticket(pid, tid, action, bibref):
    '''
    Deletes a transaction from a ticket. If ticket empty, deletes it.
    @param pid: pid
    @param tid: ticket id
    @param action: action
    @param bibref: bibref
    '''
    rt = get_person_request_ticket(pid, tid)
    if len(rt) > 0:
#        rt_num = rt[0][1]
        rt = rt[0][0]
    else:
        return
    for t in list(rt):
        if str(t[0]) == str(action) and str(t[1]) == str(bibref):
            rt.remove(t)

    action_present = False
    for t in rt:
        if str(t[0]) in ['confirm', 'repeal']:
            action_present = True

    if not action_present:
        delete_request_ticket(pid, tid)
        return

    tu.update_request_ticket(pid, rt, tid)


def create_request_ticket(userinfo, ticket):
    '''
    Creates a request ticket
    @param usernfo: dictionary of info about user
    @param ticket: dictionary ticket
    '''
    # write ticket to DB
    # send eMail to RT
    udata = []
    mailcontent = []
    m = mailcontent.append
    m("A user sent a change request through the web interface.")
    m("User Information:")

    for k, v in userinfo.iteritems():
        if v:
            m("    %s: %s" % (k, v))

    m("\nLinks to all issued Person-based requests:\n")

    for i in userinfo:
        udata.append([i, userinfo[i]])

    tic = {}
    for t in ticket:
        if not t['action'] in ['confirm', 'assign', 'repeal', 'reset']:
            return False
        elif t['pid'] < 0:
            return False
        elif not is_valid_bibref(t['bibref']):
            return False
        if t['action'] == 'reset':
            #we ignore reset tickets
            continue
        else:
            if t['pid'] not in tic:
                tic[t['pid']] = []
        if t['action'] == 'assign':
            t['action'] = 'confirm'

        tic[t['pid']].append([t['action'], t['bibref']])

    for pid in tic:
        data = []
        for i in udata:
            data.append(i)
        data.append(['date', ctime()])
        for i in tic[pid]:
            data.append(i)
        tu.update_request_ticket(pid, data)
        pidlink = get_person_redirect_link(pid)

        m("%s/person/%s?open_claim=True#tabTickets" % (CFG_SITE_URL, pidlink))

    m("\nPlease remember that you have to be logged in "
      "in order to see the ticket of a person.\n")

    if ticket and tic and mailcontent:
        sender = CFG_BIBAUTHORID_AUTHOR_TICKET_ADMIN_EMAIL

        if bconfig.TICKET_SENDING_FROM_USER_EMAIL and userinfo['email']:
            sender = userinfo['email']

        send_email(sender,
                   CFG_BIBAUTHORID_AUTHOR_TICKET_ADMIN_EMAIL,
                   subject="[Author] Change Request",
                   content="\n".join(mailcontent))

    return True


def user_can_view_CMP(uid):
    action = bconfig.CLAIMPAPER_VIEW_PID_UNIVERSE
    auth = acc_authorize_action(uid, action)
    if auth[0] == 0:
        return True
    else:
        return False


def _resolve_maximum_acces_rights(uid):
    '''
    returns [max_role, lcul] to use in execute_action and check_transaction_permissions.
    Defaults to ['guest',0] if user has no roles assigned.
    Always returns the maximum privilege.
    '''

    roles = {bconfig.CLAIMPAPER_ADMIN_ROLE: acc_get_role_id(bconfig.CLAIMPAPER_ADMIN_ROLE),
            bconfig.CLAIMPAPER_USER_ROLE: acc_get_role_id(bconfig.CLAIMPAPER_USER_ROLE)}
    uroles = acc_get_user_roles(uid)

    max_role = ['guest', 0]

    for r in roles:
        if roles[r] in uroles:
            rright = bconfig.CMPROLESLCUL[r]
            if rright >= max_role[1]:
                max_role = [r, rright]

    return max_role


def create_new_person(uid, uid_is_owner=False):
    '''
    Create a new person.

    @param uid: User ID to attach to the person
    @type uid: int
    @param uid_is_owner: Is the uid provided owner of the new person?
    @type uid_is_owner: bool

    @return: the resulting person ID of the new person
    @rtype: int
    '''
    pid = tu.create_new_person(uid, uid_is_owner=uid_is_owner)

    return pid


def execute_action(action, pid, bibref, uid, userinfo='', comment=''):
    '''
    Executes the action, setting the last user right according to uid

    @param action: the action to perform
    @type action: string
    @param pid: the Person ID to perform the action on
    @type pid: int
    @param bibref: the bibref pair to perform the action for
    @type bibref: string
    @param uid: the internal user ID of the currently logged in user
    @type uid: int

    @return: success of the process
    @rtype: boolean
    '''
    pid = wash_integer_id(pid)

    if not action in ['confirm', 'assign', 'repeal', 'reset']:
        return False
    elif pid < 0:
        return False
    elif pid == -3:
        pid = tu.create_new_person(uid, uid_is_owner=False)
    elif not is_valid_bibref(bibref):
        return False

    user_level = _resolve_maximum_acces_rights(uid)[1]

    if action in ['confirm', 'assign']:
        tu.insert_user_log(userinfo, pid, 'assign', 'CMPUI_ticketcommit', bibref, comment)
        tu.confirm_papers_to_person([pid], [[bibref]], user_level)
    elif action in ['repeal']:
        tu.insert_user_log(userinfo, pid, 'repeal', 'CMPUI_ticketcommit', bibref, comment)
        tu.reject_papers_from_person([pid], [[bibref]], user_level)
    elif action in ['reset']:
        tu.insert_user_log(userinfo, pid, 'reset', 'CMPUI_ticketcommit', bibref, comment)
        tu.reset_papers_flag([pid], [[bibref]])
    else:
        return False
    return True


def get_bibref_name_string(bibref):
    '''
    Returns the name string associated to a name string
    @param bibref: bibrefrec '100:123,123'
    @return: string
    '''
    name = ""
    ref = ""

    if not (bibref and isinstance(bibref, str) and bibref.count(":")):
        return name

    if bibref.count(","):
        try:
            ref = bibref.split(",")[0]
        except (ValueError, TypeError, IndexError):
            return name
    else:
        ref = bibref

    dbname = tu0.get_bibref_name_string(((ref,),))

    if dbname:
        name = dbname

    return name


def sign_assertion(robotname, assertion):
    '''
    Sign an assertion for the export of IDs

    @param robotname: name of the robot. E.g. 'arxivz'
    @type robotname: string
    @param assertion: JSONized object to sign
    @type assertion: string

    @return: The signature
    @rtype: string
    '''
    robotname = ""
    secr = ""

    if not robotname:
        return ""

    robot = ExternalAuthRobot()
    keys = load_robot_keys()

    try:
        secr = keys["Robot"][robotname]
    except:
        secr = ""

    return robot.sign(secr, assertion)


def get_personid_status_cacher():
    '''
    Returns a DataCacher object describing the status of the pid table content

    @return: DataCacher Object
    @rtype: DataCacher
    '''
    return tu.get_personid_status_cacher()
