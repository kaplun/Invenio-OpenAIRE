"""
Invenio software enables you to run your own electronic preprint server,
your own online library catalogue or a digital document system on the
web.

To learn more about Invenio software, please go to U{Invenio software
distribution site <http://invenio-software.org/>}.

To learn more about Invenio modules and programming, please go to
U{Hacking Invenio <http://invenio-demo.cern.ch/help/hacking/>} web pages.

To browse Invenio source code repository, inspect commits,
revisions and the like, please go to U{Invenio git web repository
<http://invenio-software.org/repo/invenio>}.

This place enables you to browse Invenio source code documentation
as well as the source code snippets themselves.
"""

"""
Here are very often used Invenio APIs that can be useful when writing quick
scripts at the Python prompt.
"""
from intbitset import intbitset
from bibdocfile import BibRecDocs, BibDoc, decompose_file
try:
    from dbquery import run_sql, OperationalError
    from search_engine import perform_request_search, search_pattern, get_record, get_fieldvalues
except (ImportError, OperationalError):
    pass
from bibrecord import create_record, record_xml_output, record_add_field
from bibformat import format_record
from bibformat_engine import BibFormatObject
from websubmit_file_converter import can_convert, convert_file
from webuser import collect_user_info, get_uid_from_email
from access_control_engine import acc_authorize_action
from mailutils import send_email
from errorlib import register_exception
from shellutils import run_process_with_timeout
from bibtask import task_low_level_submission

__all__ = ['intbitset', 'BibRecDocs', 'BibDoc', 'decompose_file', 'run_sql',
           'perform_request_search', 'search_pattern', 'get_record',
           'get_fieldvalues', 'create_record', 'record_xml_output',
           'record_add_field', 'format_record', 'BibFormatObject',
           'can_convert', 'convert_file', 'collect_user_info',
           'get_uid_from_email', 'acc_authorize_action', 'send_email',
           'register_exception', 'run_process_with_timeout',
           'task_low_level_submission']
