# -*- coding: utf-8 -*-
##
## $Id: wsc_string_length.py,v 1.3 2007/06/21 07:40:40 nich Exp $
##
## This file is part of CDS Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007 CERN.
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


"""This is the function "wsc_string_length". It is used to check that the
   STRING-LENGTH of a WSET object's "value" data-member falls within
   mimnum and maximum length parameters.
"""

__revision__ = "$Id: wsc_string_length.py,v 1.3 2007/06/21 07:40:40 nich Exp $"




def wsc_string_length(wset_object, maxlen=None, minlen=None):
    """Check the STRING length of a WSET object's "value" against a minimum
       and maximum length.
       If the length of the WSET object's value falls within the minlen and
       maxlen parameters, the test will be passed and an integer value of
       0 (zero) will be returned. If the value does not fall within the parameters,
       an integer value of 1 (one, or at least non-zero) will be returned,
       indicating that the test failed.
       IMPORTANT - this function can only be used on those WSETs with a single
       STRING-TYPE value. Anything else will cause a TypeError to be raised.
       
       @param wset_object: (WSET object) - this is the WebSubmit "element type"
        object whose value's string length is to be checked.
       @param maxlen: (integer -or- NoneType) - the maximum permissable length
        for the WSET's data value. This defaults to None, indicating that there
        is no maximum length restriction.
       @param minlen: (integer) - the minimum permissable length for the WSET's
        data value. This defaults to None, indicating that there is no
        minimum length restriction on the value.
       @return: (integer) - 0 (zero) if no error is found and the test is
        passed; 1 (one) if an error is found and the test fails.
    """
    ## Flag indicating whether an error was found:
    data_error = 0
    
    ## Sanity checking for minlen:
    try:
        minlen = int(minlen)
    except (ValueError, TypeError):
        ## Invalid min-len. Set to 0
        minlen = 0
    else:
        ## Check to see that minlen is at least 0. Se it to 0 if not.
        if minlen < 0:
            minlen = 0

    ## Sanity check for maxlen:
    if maxlen is not None:
        try:
            maxlen = int(maxlen)
        except (ValueError, TypeError):
            ## Invalid value for maxlen - set it to None
            maxlen = None
        else:
            ## Check to ensure that maxlen is >= minlen. Set it to None if not:
            if maxlen < minlen:
                maxlen = None

    ## Extract the "value" member from the "wset_object":
    data_subject = wset_object.value

    ## Sanity checking for data-value's type:
    if type(data_subject) not in (str, unicode) and \
           not isinstance(data_subject, str):
        ## unknown type - raise a type-error
        msg = """wsc_check_string_length: Expected wset_object's""" \
              """ "value" member to be a string-type; Got %s""" \
              % str(type(data_subject))
        raise TypeError(msg)

    if len(data_subject) < minlen:
        ## Length of the test subject is less than the allowed minimum length.
        data_error = 1
    elif maxlen is not None and len(data_subject) > maxlen:
        ## Length of the test subject is more than the allowed maximum length.
        data_error = 1

    ## return the error-flag:
    return data_error

