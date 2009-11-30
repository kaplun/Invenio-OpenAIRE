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
CDS Invenio WebAccess exporter.

This code has been contributed by Gregory Favre from InfoScience.
"""

from xml.dom.minidom import parseString, getDOMImplementation
import xml.dom
from invenio.access_control_firerole import compile_role_definition, serialize
from invenio.access_control_admin import acc_add_role, \
                                         acc_get_role_id, \
                                         acc_get_all_roles, \
                                         acc_update_role, \
                                         acc_delete_role, \
                                         acc_add_user_role, \
                                         acc_delete_user_role, \
                                         acc_get_user_id, \
                                         acc_get_action_id, \
                                         acc_add_action, \
                                         acc_get_all_actions, \
                                         acc_get_action_details, \
                                         acc_update_action, \
                                         acc_delete_action, \
                                         acc_add_authorization, \
                                         acc_delete_role_action
from invenio.access_control_config import CFG_ACC_EMPTY_ROLE_DEFINITION_SER, \
                                          CFG_ACC_EMPTY_ROLE_DEFINITION_SRC
from invenio.dbquery import run_sql
from invenio.webuser import get_email


def acc_save_xml_config(stream):
    """Saves the webacces configuration as xml. Stream should
    have a write() method (e.g. open('path/to/file', 'w'))"""
    impl = getDOMImplementation()
    newdoc = impl.createDocument(None, "access_configuration", None)
    root_element = newdoc.documentElement
    roles = newdoc.createElement('roles')
    _acc_save_roles(roles, newdoc)
    root_element.appendChild(roles)
    actions = newdoc.createElement('actions')
    _acc_save_actions(actions, newdoc)
    root_element.appendChild(actions)
    authorizations = newdoc.createElement('authorizations')
    _acc_save_authorizations(authorizations, newdoc)
    root_element.appendChild(authorizations)
    xml_config = newdoc.toprettyxml(encoding="utf-8" )
    stream.write(xml_config)

def _acc_save_roles(rolesNode, document):
    roles = acc_get_all_roles()
    for (role_id, role_name, role_description,
        firerole_def_ser, firerole_def_src) in roles:
        role = document.createElement('role')
        role.setAttribute('name', role_name)
        if role_description:
            description = document.createElement('description')
            description_text = document.createTextNode(role_description)
            description.appendChild(description_text)
            role.appendChild(description)
        if firerole_def_src:
            definition = document.createElement('definition')
            definition_text = document.createTextNode(firerole_def_src)
            definition.appendChild(definition_text)
            role.appendChild(definition)
        query = "SELECT id_user FROM user_accROLE WHERE id_accROLE=%i"
        uids = run_sql(query % role_id)
        if len(uids):
            users = document.createElement('users')
            for uid in uids:
                email = get_email(uid[0])
                user = document.createElement('user')
                user.setAttribute('uid', str(uid[0]))
                user.setAttribute('email', email)
                users.appendChild(user)
            role.appendChild(users)
        role = rolesNode.appendChild(role)

def _acc_save_actions(actionsNode, document):
     actions = acc_get_all_actions()
     for (action_id, action_name, action_description) in actions:
        (action_id, action_name, action_description,
        allowed_keywords, optional) = acc_get_action_details(action_id)
        action = document.createElement('action')
        action.setAttribute('name', action_name)
        action.setAttribute('optional_arguments', optional)
        if action_description:
            description = document.createElement('description')
            description_text = document.createTextNode(action_description)
            description.appendChild(description_text)
            action.appendChild(description)
        if allowed_keywords:
            allowedKeywordsNode = document.createElement('allowedkeywords')
            for keyword in allowed_keywords.split(','):
                keywordNode = document.createElement('keyword')
                keyword_text = document.createTextNode(keyword)
                keywordNode.appendChild(keyword_text)
                allowedKeywordsNode.appendChild(keywordNode)
            action.appendChild(allowedKeywordsNode)
        action = actionsNode.appendChild(action)

def _acc_save_authorizations(authorizationsNode, document):
    query = """SELECT role.name, action.name,
                      raa.id_accARGUMENT, raa.argumentlistid
               FROM accROLE_accACTION_accARGUMENT raa
               LEFT JOIN accROLE role ON raa.id_accROLE=role.id
               LEFT JOIN accACTION action ON raa.id_accACTION = action.id"""
    authorizations = run_sql(query)
    authorizations_dict = {}
    for (role, action, id_argument, argumentlistid) in authorizations:
        if authorizations_dict.has_key((role, action, argumentlistid)):
            authorizations_dict[(role, action, argumentlistid)].append(id_argument)
        else:
            authorizations_dict[(role, action, argumentlistid)] = [id_argument]
    for (role, action, argumentlistid) in authorizations_dict.keys():
        authorize = document.createElement('authorize')
        authorize.setAttribute('role', role)
        authorize.setAttribute('action', action)
        if authorizations_dict[(role, action, argumentlistid)][0] == -1:
            # no reference to a list => this auth had optional arguments
            # which weren't given
            authorize.setAttribute('optional', 'yes')
        elif authorizations_dict[(role, action, argumentlistid)][0] == 0:
            # there is no optional parameter for this action.
            authorize.setAttribute('optional', 'no')
        else:
            # we got a reference to some arguments. These arguments weren't optional.
            authorize.setAttribute('optional', 'no')
            for argument_id in authorizations_dict[(role, action, argumentlistid)]:
                query = "SELECT keyword, value FROM accARGUMENT where id=%i"
                res = run_sql(query % argument_id)
                if len(res):
                    argument = document.createElement('argument')
                    argument.setAttribute('name', res[0][0])
                    argument.setAttribute('value', res[0][1])
                    authorize.appendChild(argument)
        authorizationsNode.appendChild(authorize)



def acc_load_xml_config(stream, dump_old_config=True, verbose=False):
    """Takes an xml config file and stores it in the database. Stream should
    have a read() method (e.g. open('path/to/file'))"""
    xml_stream = stream.read()
    root = parseString(xml_stream).documentElement
    for root_child in root.childNodes:
        if root_child.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
            if root_child.nodeName == 'roles':
                (new, updated, deleted) = _acc_load_roles(root_child, dump_old_config)
                if verbose:
                    print "Added %i new roles, updated %i existing roles, dropped %i roles." % \
                           (new, updated, deleted)
            elif root_child.nodeName == 'actions':
                (new, updated, deleted) = _acc_load_actions(root_child, dump_old_config)
                if verbose:
                    print "Added %i new actions, updated %i existing actions, dropped %i actions." % \
                           (new, updated, deleted)
            elif root_child.nodeName == 'authorizations':
                (new) = _acc_load_authorizations(root_child, dump_old_config)
                if verbose:
                    print "Added %i authorizations." % (new)

def _acc_load_roles(rolesNode, dump_old_roles=True):
    """Given the roles node of a config file, compute all roles and store
    them in the database"""
    roles_list = []
    for role in rolesNode.getElementsByTagName("role"):
        role_dict = {}
        role_dict['name'] = role.getAttribute('name').encode("utf-8")
        role_dict['description'] = ''
        for element in role.childNodes:
            if element.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                if element.nodeName == 'description':
                    role_dict['description'] = \
                                    element.firstChild.data.encode("utf-8").strip()
                if element.nodeName == 'definition':
                    role_dict['definition'] = \
                                    element.firstChild.data.encode("utf-8").strip()
                if element.nodeName == 'users':
                    users = []
                    for subelement in element.childNodes:
                        if subelement.nodeType == \
                                            xml.dom.minidom.Node.ELEMENT_NODE:
                            user = {}
                            if subelement.hasAttribute('email'):
                                user['email'] = \
                                subelement.getAttribute('email').encode("utf-8")
                            if subelement.hasAttribute('uid'):
                                user['uid'] = \
                                subelement.getAttribute('uid').encode("utf-8")
                            users.append(user)
                    role_dict['users'] = users
        roles_list.append(role_dict)
    # Now that everything is parsed, put it in the database
    # first: get all roles, in order to be able to dump old ones.
    query = "SELECT name, id from accROLE"
    old_roles_to_dump = dict(run_sql(query))
    query2 = "SELECT id_user, id_accROLE from user_accROLE"
    old_user_roles_to_dump = dict.fromkeys(run_sql(query2), True)
    new, updated, deleted = 0, 0, 0
    for role_dict in roles_list:
        if old_roles_to_dump.has_key(role_dict['name']):
            del(old_roles_to_dump[role_dict['name']])
        if role_dict.has_key('definition'):
            firerole_def_src = role_dict['definition']
        else:
            firerole_def_src = CFG_ACC_EMPTY_ROLE_DEFINITION_SRC
        firerole_def_ser = serialize(compile_role_definition(firerole_def_src))
        role_id = acc_get_role_id(role_dict['name'])
        if role_id == 0:
            new += 1
            acc_add_role(name_role=role_dict['name'],
                         description=role_dict['description'],
                         firerole_def_ser=firerole_def_ser,
                         firerole_def_src=firerole_def_src)
        else:
            updated += 1
            acc_update_role(id_role=role_id, name_role=role_dict['name'],
                            description=role_dict['description'],
                            firerole_def_ser=firerole_def_ser,
                            firerole_def_src=firerole_def_src)
        if role_dict.has_key('users'):
            role_id = acc_get_role_id(role_dict['name'])
            for user in role_dict['users']:
                uid = 0
                if user.has_key('uid'):
                    uid = int(user['uid'])
                elif user.has_key('email'):
                    uid = acc_get_user_id(user['email'])
                acc_add_user_role(id_user=uid, id_role=role_id)
                if old_user_roles_to_dump.has_key((uid, role_id)):
                    del(old_user_roles_to_dump[(uid, role_id)])
    if dump_old_roles:
         for role_id in old_roles_to_dump.values():
            deleted += 1
            acc_delete_role(id_role=role_id)
         for (uid, role_id) in old_user_roles_to_dump:
            acc_delete_user_role(id_user=uid, id_role=role_id)
    return (new, updated, deleted)

def _acc_load_actions(actionsNode, dump_old_actions=True):
    """Given the actions node of a config file, compute all actions and store
    them in the database"""
    actions_list = []
    for action in actionsNode.getElementsByTagName("action"):
        action_dict = {}
        action_dict['name'] = action.getAttribute('name').encode("utf-8")
        action_dict['optional_arguments'] = \
                action.getAttribute('optional_arguments').encode("utf-8")
        for element in action.childNodes:
            if element.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                if element.nodeName == 'description':
                    action_dict['description'] = \
                                element.firstChild.data.encode("utf-8").strip()
                allowed_keywords = []
                if element.nodeName == 'allowedkeywords':
                    for subelement in element.childNodes:
                        if subelement.nodeType == \
                                            xml.dom.minidom.Node.ELEMENT_NODE:
                            keyword = \
                                subelement.firstChild.data.encode("utf-8").strip()
                            allowed_keywords.append(keyword)
                action_dict['allowed_keywords'] = allowed_keywords
        actions_list.append(action_dict)
    # save the parsed xml...
    # first, find the old actions already present in the database
    query = "SELECT name, id from accACTION"
    old_actions_to_dump = dict(run_sql(query))
    new, updated, deleted = 0, 0, 0
    for action_dict in actions_list:
        action_name = action_dict['name']
        if old_actions_to_dump.has_key(action_name):
            del(old_actions_to_dump[action_name])
        if action_dict.has_key('description'):
            description = action_dict['description']
        else:
            description = ''
        if action_dict.has_key('optional'):
            optional = action_dict['optional']
        else:
            optional = 'no'
        action_id = acc_get_action_id(action_name)
        if action_id == 0:
            new += 1
            acc_add_action(action_name, description,
                           optional, *action_dict['allowed_keywords'])
        else:
            updated += 1
            allowedkeywords = ','.join(action_dict['allowed_keywords'])
            acc_update_action(id_action=action_id, verbose=0,
                              description=action_dict['description'],
                              optional=action_dict['optional_arguments'],
                              allowedkeywords=allowedkeywords)
    if dump_old_actions:
        for action_id in old_actions_to_dump.values():
            deleted += 1
            acc_delete_action(id_action=action_id)
    return (new, updated, deleted)

def _acc_load_authorizations(authorizationsNode, dump_old_authorizations=True):
    """Given the authorizations node of a config file, compute all
    authorizations (role-action association) and store them in the database"""
    auths_list = []
    if dump_old_authorizations:
        query = "TRUNCATE accROLE_accACTION_accARGUMENT"
        run_sql(query)

    for auth in authorizationsNode.getElementsByTagName("authorize"):
        auth_dict = {}
        auth_dict['role'] = auth.getAttribute('role').encode("utf-8")
        auth_dict['action'] = auth.getAttribute('action').encode("utf-8")
        auth_dict['optional'] = auth.getAttribute('optional').encode("utf-8")
        arguments = {}
        for element in auth.childNodes:
            if element.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                if element.nodeName == 'argument':
                    arguments[element.getAttribute('name').encode("utf-8")] =\
                              element.getAttribute('value').encode("utf-8")
        auth_dict['arguments'] = arguments
        auths_list.append(auth_dict)
    new = 0
    for auth_dict in auths_list:
        optional = auth_dict['optional'] == 'yes' and 1 or 0
        id_role = acc_get_role_id(name_role=auth_dict['role'])
        id_action = acc_get_action_id(name_action=auth_dict['action'])
        new += 1
        acc_add_authorization(auth_dict['role'], auth_dict['action'],
                              optional, **auth_dict['arguments'])
    return new

def test():
    acc_load_xml_config(open('access_configuration.xml'), verbose=True)
    acc_save_xml_config(open('access_configuration_test_output.xml', 'w'))

if __name__=="__main__":
    test()