# -*- coding: utf-8 -*-

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

def is_dry_run_request(req):
    """
    @return: True if the current request is a dry_run (or No-Op) request.
    @see: section 3.1 in http://www.swordapp.org/docs/sword-profile-1.3.html
    """
    return req.headers_in.get("X-No-Op", "false").lower() == 'true'

def is_verbose_request(req):
    """
    @return: True if the current request should be handled verbosely.
    @see: section 3.2 in http://www.swordapp.org/docs/sword-profile-1.3.html
    """
    return req.headers_in.get("X-Verbose", "false").lower() == 'true'


def get_sword_service_description(req):
