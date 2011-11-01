# -*- coding: utf-8 -*-
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

"""
mod_wsgi Invenio application loader.
"""

from flask import Flask

try:
    from invenio import remote_debugger
    remote_debugger.start_file_changes_monitor()
except:
    pass

from invenio.webinterface_handler_wsgi import application as legacy_invenio
from invenio.webinterface_handler_wsgi import SimulatedModPythonRequest

class LegacyInvenioFixer(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        req = SimulatedModPythonRequest(environ, start_response)


application = Flask(__name__)
    application.wsgi_app()