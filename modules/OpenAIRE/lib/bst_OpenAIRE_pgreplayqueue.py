## This file is part of Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010 CERN.
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

from marshal import loads
from zlib import decompress


from invenio.dbquery import run_sql
from invenio.dnetutils import dnet_run_sql
from invenio.errorlib import register_exception
from invenio.bibtask import write_message, task_update_progress, task_sleep_now_if_required
from invenio.intbitset import intbitset

def bfe_OpenAIRE_pgreplayqueue():
    replayqueue = intbitset(run_sql("SELECT id FROM pgreplayqueue"))
    for queryid in replayqueue:
        query, param = loads(decompress(run_sql("SELECT query FROM pgreplayqueue WHERE id=%s", (queryid, ))[0][0]))
        try:
            dnet_run_sql(query, param, support_replay=False)
        except:
            ## Mmh... things are still not working. Better give up now!
            try:
                run_sql("UPDATE pgreplayqueue SET last_try=NOW() WHERE id=%s", (queryid, ))
            except:
                register_exception(alert_admin=True)
                ## We are not really interested in this particular error.
                pass
            raise
        else:
            run_sql("DELETE FROM pgreplayqueue WHERE id=%s", (queryid, ))
