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

submitdir = $(libdir)/python/invenio/websubmit_functions
formatdir = $(libdir)/python/invenio/bibformat_elements
taskletdir = $(libdir)/python/invenio/bibsched_tasklets
pylibdir = $(libdir)/python/invenio
jsdir = $(localstatedir)/www/js

submit_DATA = OpenAIRE_recmysql2curdir.py OpenAIRE_Response_Elements.py
format_DATA = bfe_dnet_field.py
tasklet_DATA = bst_chomsky.py bst_load_OpenAIRE_kbs.py bst_OpenAIRE_pgreplayqueue.py
pylib_DATA = chomsky.py \
             openaire_deposit_webinterface.py \
             openaire_deposit_engine.py \
             openaire_deposit_templates.py \
             dnetutils.py \
             openaire_deposit_utils.py \
             openaire_deposit_config.py \
             webstyle_templates_OpenAIRE.py \
             websession_templates_OpenAIRE.py
js_DATA = openaire_deposit_engine.js

EXTRA_DIST = $(pylib_DATA) $(jsdir)

CLEANFILES = *~ *.tmp *.pyc
