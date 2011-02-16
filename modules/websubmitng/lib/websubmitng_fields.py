"""
This module consists of specific frquently used fields in the submission 
like Title, Authors etc

Others can be added in this file by deriving them from the appropriate 
html element present in the module websubmitng_elements.
"""
from websubmitng_elements import *

class Title(TextArea):
    def __init__(self, element_id, marc_field, rows, cols, label='', 
                 tooltip=None, name=None, session=None):
        TextArea.__init__(self, element_id, marc_field, rows, cols,
                          label, tooltip, name, session)

    def get_recstruct(self):
    # Must be added.
        return {}

    def check_value(self):
    # Will be added.
        return true

class Authors(TextArea):
    def __init__(self, element_id, marc_field, rows, cols, label='', 
                 tooltip=None, name=None, session=None):
        TextArea.__init__(self, element_id, marc_field, rows, cols,
                          label, tooltip, name, session)

    def get_recstruct(self):
        return {}

    def check_value(self):
        return true

class NumberOfPages(TextInput):
    def __init__(self, element_id, marc_field, value=None, label='',
                 size=None, maxlength=4, tooltip=None, name=None, session=None):
        TextInput.__init__(self, element_id, marc_field, value,
                           label, size, maxlength, tooltip, name, session)

    def get_recstruct(self):
        return {}

    def check_value(self):
        return true
    
class Date(TextInput):

    def __init__(self, element_id, marc_field, value=None, label='',
                 size=None, maxlength=10, tooltip=None, name=None, session=None):
        TextInput.__init__(self, element_id, marc_field, value,
                           label, size, maxlength, tooltip, name, session)
    
    def get_recstruct(self):    
        return {}

    def check_value(self):
        return true
    
class Abstract(TextArea):
    def __init__(self, element_id, marc_field, rows, cols, label='', 
                 tooltip=None, name=None, session=None):
        TextArea.__init__(self, element_id, marc_field, rows, cols,
                          label, tooltip, name, session)

    def get_recstruct(self):
        return {}

    def check_value(self):
        return true

class KeyWords(TextArea):
    def __init__(self, element_id, marc_field, rows, cols, label='', 
                 tooltip=None, name=None, session=None):
        TextArea.__init__(self, element_id, marc_field, rows, cols,
                          label, tooltip, name, session)

    def get_recstruct(self):
        return {}

    def check_value(self):
        return true    

class ReportNumbers(TextArea):
    def __init__(self, element_id, marc_field, rows, cols, label='', 
                 tooltip=None, name=None, session=None):
        TextArea.__init__(self, element_id, marc_field, rows, cols,
                          label, tooltip, name, session)

    def get_recstruct(self):
        return {}

    def check_value(self):
        return true

class Language(Select):
    def __init__(self, element_id, marc_field, options_name_value_pairs, label='',
                 multiple=False, selected=None, size=None, tooltip=None, 
                 name=None, session=None):
        Select.__init__(self, element_id, marc_field, options_name_value_pairs,
                        label, multiple, selected, size, tooltip, name, session)

    def get_recstruct(self):
        return {}

    def check_value(self):
        return true
