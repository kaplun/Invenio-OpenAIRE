# -*- coding: utf-8 -*-
##
## $Id: wsc_mandatory.py,v 1.1 2007/07/06 14:12:46 diane Exp $
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


"""This is the function "wsc_mandatory". It is used to check that the
   WSET object's "value" is not an empty value.
"""

__revision__ = "$Id: wsc_mandatory.py,v 1.1 2007/07/06 14:12:46 diane Exp $"




def wsc_mandatory(wset_object)
    """Check that WSET object's method "has_value" returns true
       
       @param wset_object: (WSET object) - this is the WebSubmit "element type"
        object whose has_value method is to be checked.
       @return: (integer) - 0 (zero) if no error is found and the test is
        passed; 1 (one) if an error is found and the test fails.
    """
    
    #call the has_value method of the given 
    has_value = wset_object.has_value()
    if has_value:
        data_error = 0
    else:
        data_error = 1
        
    ## return the error-flag:
    return data_error

