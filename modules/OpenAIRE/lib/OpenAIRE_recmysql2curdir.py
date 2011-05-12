## $Id: Move_Revised_Files_to_Storage.py,v 1.20 2009/03/26 13:48:42 jerome Exp $

## This file is part of Invenio.
## Copyright (C) 2010, 2011 CERN.
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
OpenAIRE_recmysql2curdir - this function transform a record into the field in curdir.
"""

import os

from invenio.bibrecord import create_record, record_get_field_value, record_get_field_values
from invenio.dateutils import guess_datetime
from time import strftime

##START::DEFP()---<record>
##001::REPL(EOL,)---<controlfield tag="001"><:SN::SN:></controlfield>
##037a::REPL(EOL,)::MINLW(82)---<datafield tag="037" ind1=" " ind2=" "><subfield code="a"><:ART_RN::ART_RN:></subfield></datafield>
##041a::REPL(EOL,)::MINLW(82)---<datafield tag="041" ind1=" " ind2=" "><subfield code="a"><:ART_LANG::ART_LANG::IF(Select:,eng,ORIG):></subfield></datafield>
##088a::REP(EOL,)::MINLW(82)---<datafield tag="088" ind1=" " ind2=" "><subfield code="a"><:ART_REP*::ART_REP:></subfield></datafield>
##100xxa::REP(EOL,)::RANGE(1,1)::MINLW(82)---<datafield tag="100" ind1=" " ind2=" "><subfield code="a"><:ART_SEPARATE_AU*::ART_SEPARATE_AU:></subfield><:ART_SEPARATE_AF::ART_SEPARATE_AF::IF(,,<subfield code="u">):><:ART_SEPARATE_AF*::ART_SEPARATE_AF::IF(;,-,ORIG):><:ART_SEPARATE_AF::ART_SEPARATE_AF::IF(,,</subfield>):></datafield>
##245a::REPL(EOL,)::MINLW(82)---<datafield tag="245" ind1=" " ind2=" "><subfield code="a"><:ART_TITLE::ART_TITLE:></subfield></datafield>
##260::REPL(EOL,)::MINLW(84)---<datafield tag="260" ind1=" " ind2=" "><subfield code="c"><:ART_DATE::year:>-<:ART_DATE::mm:>-<:ART_DATE::dd:></subfield></datafield>
##300::REPL(EOL,)::MINLW(82)---<datafield tag="300" ind1=" " ind2=" "><subfield code="a"><:ART_NUMP::ART_NUMP::IF(,mult. p,ORIG):></subfield></datafield>
##500a::REP(EOL,)::MINLW(82)---<datafield tag="500" ind1=" " ind2=" "><subfield code="a"><:ART_NOTE::ART_NOTE:></subfield></datafield>
##520a::REP(EOL,)::MINLW(82)---<datafield tag="520" ind1=" " ind2=" "><subfield code="a"><:ART_ABS::ART_ABS:></subfield></datafield>
##542l::REP(EOL,)::MINLW(82)---<datafield tag="542" ind1=" " ind2=" "><subfield code="l"><:ART_LICENSE::ART_LICENSE:></subfield></datafield>
##65017a::REP(EOL,)::MINLW(82)---<datafield tag="650" ind1="1" ind2="7"><subfield code="a"><:ART_SUBJ*::ART_SUBJ:></subfield></datafield>
##6531xa::REP(EOL,)::MINLW(82)---<datafield tag="653" ind1="1" ind2=" "><subfield code="a"><:ART_KW*::ART_KW:></subfield></datafield>
##700xxa::REP(EOL,)::RANGE(2,1999)::MINLW(82)---<datafield tag="700" ind1=" " ind2=" "><subfield code="a"><:ART_SEPARATE_AU*::ART_SEPARATE_AU:></subfield><:ART_SEPARATE_AF::ART_SEPARATE_AF::IF(,,<subfield code="u">):><:ART_SEPARATE_AF*::ART_SEPARATE_AF::IF(;,-,ORIG):><:ART_SEPARATE_AF::ART_SEPARATE_AF::IF(,,</subfield>):></datafield>
##856f::REPL(EOL,)---<datafield tag="856" ind1="0" ind2=" "><subfield code="f"><:SuE::SuE:></subfield></datafield>
##980::REPL(EOL,)---<datafield tag="980" ind1=" " ind2=" "><subfield code="a">OpenAIRE</subfield></datafield>
##END::DEFP()---</record>


def write_field(curdir, field, value):
    if value:
        if type(value) is list:
            value = '\n'.join(value)
        open(os.path.join(curdir, field), 'w').write(value)

def OpenAIRE_recmysql2curdir(parameters, curdir, form, user_info=None):
    record = create_record(open(os.path.join(curdir, 'recmysql')).read())[0]
    write_field(curdir, 'SN', record_get_field_value(record, '001'))
    write_field(curdir, 'ART_RN', record_get_field_value(record, '037', code='a'))
    write_field(curdir, 'ART_LANG', record_get_field_value(record, '041', code='a'))
    write_field(curdir, 'ART_REP', record_get_field_values(record, '088', code='a'))
    write_field(curdir, 'ART_SEPARATE_AU', record_get_field_values(record, '100', code='a') + record_get_field_values(record, '700', code='a'))
    write_field(curdir, 'ART_SEPARATE_AF', record_get_field_values(record, '100', code='u') + record_get_field_values(record, '700', code='u'))
    write_field(curdir, 'ART_TITLE', record_get_field_value(record, '245', code='a'))
    date = record_get_field_value(record, '260', code='c')
    if date:
        date = strftime("%Y-%m-%d", guess_datetime(date))
    write_field(curdir, 'ART_DATE', date)
    write_field(curdir, 'ART_NUMP', record_get_field_value(record, '300', code='a'))
    write_field(curdir, 'ART_NOTE', record_get_field_value(record, '500', code='a'))
    write_field(curdir, 'ART_ABS', record_get_field_value(record, '520', code='a'))
    write_field(curdir, 'ART_LICENSE', record_get_field_value(record, '542', code='l'))
    write_field(curdir, 'ART_SUBJ', record_get_field_values(record, '650', '1', '7', 'a'))
    write_field(curdir, 'ART_KW', record_get_field_values(record, '653', '1', ' ', 'a'))
    return ''


