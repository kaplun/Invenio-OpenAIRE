## This file is part of Invenio.
## Copyright (C) 2007, 2008, 2010, 2011 CERN.
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


import os
import re

from invenio.config import CFG_SITE_NAME, \
     CFG_SITE_URL, \
     CFG_SITE_SUPPORT_EMAIL
from invenio.access_control_admin import acc_get_role_users,acc_get_role_id
from invenio.websubmit_config import CFG_WEBSUBMIT_COPY_MAILS_TO_ADMIN
from invenio.mailutils import send_email

def Send_Request_For_Publication(parameters, curdir, form, user_info=None):
    global rn,sysno
    # variables declaration
    doctype = re.search(".*/([^/]*)/([^/]*)/[^/]*$",curdir).group(2)
    FROMADDR = '%s Submission Engine <%s>' % (CFG_SITE_NAME,CFG_SITE_SUPPORT_EMAIL)
    otheraddresses = parameters['addressesDAM']
    categformat = parameters['categformatDAM']
    # retrieve category
    categformat = categformat.replace("<CATEG>","([^-]*)")
    categs = re.match(categformat,rn)
    if categs is not None:
        category = categs.group(1)
    else:
        category = "unknown"
    # create TI
    if os.path.exists("%s/date" % curdir):
        fp = open("%s/date" % curdir, "r")
        date = fp.read()
        fp.close()
    else:
        date = ""
    if os.path.exists("%s/%s" % (curdir,parameters['titleFile'])):
        fp = open("%s/%s" % (curdir,parameters['titleFile']),"r")
        title = fp.read()
        fp.close()
        title = title.replace("\n","")
    else:
        title = ""
    title += " - %s" % date
    # create AU
    if os.path.exists("%s/%s" % (curdir,parameters['authorfile'])):
        fp = open("%s/%s" % (curdir,parameters['authorfile']), "r")
        author = fp.read()
        fp.close()
    else:
        author = ""
    # we get the referee password
    #sth = run_sql("SELECT access FROM sbmAPPROVAL WHERE rn=%s", (rn,))
    #if len(sth) >0:
        #access = sth[0][0]
    # Build referee's email address
    refereeaddress = ""
    # Try to retrieve the publication committee chair's email from the role database
    for user in acc_get_role_users(acc_get_role_id("pubcomchair_%s_%s" % (doctype,category))):
        refereeaddress += user[1] + ","
    # And if there are general referees
    for user in acc_get_role_users(acc_get_role_id("pubcomchair_%s_*" % doctype)):
        refereeaddress += user[1] + ","
    refereeaddress = re.sub(",$","",refereeaddress)
    # Creation of the mail for the referee
    addresses = ""
    if refereeaddress != "":
        addresses = refereeaddress + ","
    if otheraddresses != "":
        addresses += otheraddresses
    else:
        addresses = re.sub(",$","",addresses)
    title_referee = "Request for publication of %s" % rn
    mail_referee = "The document %s has been asked for publication to the %s Server..\nYour have to select an editorial board for it.\n\n" % (rn,CFG_SITE_NAME)
    mail_referee +="Title: %s\n\nAuthor(s): %s\n\n" % (title,author)
    mail_referee +="To access the document(s), select the file(s) from the location:<%s/record/%s/files/>\n\n" % (CFG_SITE_URL,sysno)
    mail_referee +="To select an editorial board, you should go to this URL:\n<%s/publiline.py?doctype=%s&categ=%s&RN=%s>\n" % (CFG_SITE_URL,doctype,category,rn)
    mail_referee +="---------------------------------------------\nBest regards.\nThe submission team.\n"
    #Send mail to referee
    send_email(FROMADDR, addresses, title_referee, mail_referee, copy_to_admin=CFG_WEBSUBMIT_COPY_MAILS_TO_ADMIN)
    return ""
