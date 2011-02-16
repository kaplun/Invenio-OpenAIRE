"""
This module consists of classes corresponding to the web 
interface(WebSubmitInterface), generic html element(WebSubmitInterfaceElement) 
and some specific html elements derived from it.

Any other html elements can be added by creating a class deived 
from 'WebSubmitInterfaceElement'
"""

from cgi import escape
from websubmit_managedocfiles import create_file_upload_interface
from htmlutils import H, create_html_select

class WebSubmitInterface(list):
    def __init__(self, user_info, session, title=None, description=None):
        self.user_info = user_info #?
        self.session = session
        self.title = title
        self.description = description

    def get_full_page(self, req):
        return page(req=req, title=self.title, description=self.description)

    def get_html(self):
        out = '<form name="input" action="submitted" method="post"> \
               <table class="websubmitng_form"><tbody>\n'
        for element in self:
            out += '  <tr>\n'
            out += '    <td class="websubmitng_label">\n'
            out += '    <label for="%s">%s  </label>\n' % \
                    (escape(element.element_id, True), element.label)
            out += '    </td>\n'
            out += '    <td class="websubmitng_element">\n'
            out += element.get_html()
            out += '    </td>\n'
            out += '  <tr>\n'
        out += '</tbody></table></form>\n'
        return out

    def get_js(self):
        out = ""
        classes = [] #class
        for element in self:
            element_class = type(element)
            if element_class not in classes:
                out += element.get_js()
                classes.append(element_class)
        return out

    def get_css(self):
        out = ""
        classes = []
        for element in self:
            element_class = type(element)
            if element_class not in classes:
                out += element.get_css()
                classes.append(element_class)
        return out

    def check_values(self):
        errors = []
        for element in self:
            try:
                element.check_value()
            except InvenioWebSubmitValueError, err:
                errors.append(err)
        if errors:
            raise InvenioWebSubmitValuesError(errors)
        return True

    def get_recstruct(self):
        recstruct = {}
        for element in self:
            recstruct.update(element.get_recstruct())
        return recstruct

    def get_simple_xml(self):
        out = '<?xml version="1.0"?>\n'


class WebSubmitInterfaceElement(object):
    """
    Class corresponding to the generic html element.

    Contains attributes and methods which are generic to any 
    html element. Those that are more specific to a particular 
    html element are added in the corresponding element's class 
    derived from this.
    """
    def __init__(self, element_id, marc_field, session, 
                 name=None, value='', label='', size=None, tooltip=None):
        self.__id = element_id
        self.__name = name
        self.__value = value
        self.__label = label
        self.__size = size
        self.__tootltip = tooltip
        self.__marc_field = marc_field
        #self.__user_info = session['user_info']
        self.__session = session

    def get_html(self):
        return ""

    def get_static_js():
        return ""
    get_static_js = staticmethod(get_static_js)

    def get_js(self):
        return ""

    def get_static_css():
        return ""
    get_static_css = staticmethod(get_static_css)

    def get_css():
        return ""

    def get_recstruct(self):
        return {}

    def check_value(self):
        return true

    def get_value_as_xml_snippet(self):
        return python2xml(self.__value, indent=8)

    def get_value(self):
        return self.__value
   
    def set_value(self, value):
        self.__value = value

    def get_name(self):
        return self.__name
  
    def get_label(self):
        return self.__label

    def get_size(self):
        return self.__size

    def get_tooltip(self):
        return self.__tooltip

    def get_marc_field(self):
        return self.__marc_field  

    def get_id(self):
        return self.__id

    def get_session(self):
        return self.__session 

    session =  property(get_session)
    value = property(get_value)
    name = property(get_name)
    label = property(get_label)
    size = property(get_size)
    tooltip = property(get_tooltip)
    marc_field = property(get_marc_field)
    element_id = property(get_id)


## Form Formatting classes

class Table(WebSubmitInterfaceElement):
    def __init__(self, elements, header=None):
        WebSubmitInterfaceElement.__init__(self, '', '', '')
        self.__elements = elements  
        self.__header = header

    def get_html(self):
        html = ''
        if self.__elements:
            html = '<table>'
            if self.__header:
                html += '<tr>'
                for col in self.__header:
                    html += '<th>' + col + '</th>'
                html += '</tr>'
            for row in self.__elements:
                html += '<tr>'
                for col in row:
                    html += '<td>' + col.get_html() + '</td>'
                html += '</tr>'
            html += '</table>'
        return html

    def get_name(self):
        element_names = []
        for row in self.__elements:
            for col in row:
                element_names.append(col.get_name())
        return element_names

    def get_value(self):
        element_values = []
        for row in self.__elements:
            for col in row:
                element_values.append(col.get_value())
        return element_values

class Fieldset(WebSubmitInterfaceElement):
    def __init__(self, legend, elements):
        WebSubmitInterfaceElement.__init__(self, '', '', '')
        self.__legend = legend
        self.__elements = elements

    def get_html(self):
        html = ''
        if self.__elements:
            html += '<fieldset><legend>' + self.__legend + '</legend>'
            for element in self.__elements:
                html += element.get_html() + '<br/>'
            html += '</fieldset>'
        return html
            
    def get_name(self):
        element_names = []
        for element in self.__elements:
            element_names.append(element.get_name())
        return element_names

    def get_value(self):
        element_values = []
        for element in self.__elements:
            element_values.append(element.get_value())
        return element_values

## Form Elements' classes
class TextInput(WebSubmitInterfaceElement):
    def __init__(self, element_id, marc_field, value=None, label='',
                 size=None, maxlength=None, tooltip=None, name=None, session=None):
        WebSubmitInterfaceElement.__init__(self, element_id, marc_field, session, name, 
                                           value, label, size, tooltip)
        self.__maxlength = maxlength
        
    def get_html(self):
        if self.session.has_key(self.name):
            self.set_value(self.session[self.name])
        html = H.input(type_="text", name=self.name, value=self.value, 
                       id_=self.element_id, size=self.size, maxlength=self.__maxlength)()
        return html

    def get_maxlength(self):
        return self.__maxlength     
 
    maxlength = property(get_maxlength)


class ButtonInput(WebSubmitInterfaceElement):
    def __init__(self, element_id, button_type, value, 
                 onclick_action=None, size=None, name=None, session=None):
        WebSubmitInterfaceElement.__init__(self, element_id, None, 
                                           session, name, value, size=size)
        self.__button_type = button_type
        self.__action = onclick_action

    def get_html(self):
        if self.button_type == "button":
            html = H.input(type_=self.__button_type, onclick=self.__action, name=self.name, 
                           value=self.value, id_=self.element_id, size=self.size)()
        else:
            html = H.input(type_=self.__button_type, name=self.name, 
                           value=self.value, id_=self.element_id, size=self.size)()
        return html

    def get_button_type(self):
        return self.__button_type

    def get_action(self):
        return self.__action

    button_type = property(get_button_type)
    action = property(get_action)


class CheckBoxInput(WebSubmitInterfaceElement):
    def __init__(self, element_id, marc_field, value=None,
                 label='', size=None, checked=False, tooltip=None, name=None, session=None):
        WebSubmitInterfaceElement.__init__(self, element_id, marc_field, session, name,
                                           value, label, size, tooltip)
        self.__checked = checked

    def get_html(self):
        if self.session.has_key(self.name):
            self.set_value(self.session[self.name])
        if __checked == True:
            html = H.input(type_="checkbox", name=self.name, value=self.value, 
                           id_=self.element_id, size=self.size, checked="checked")()
        else:
            html = H.input(type_="checkbox", name=self.name, value=self.value, 
                           id_=self.element_id, size=self.size)()
        return html

    def get_checked(self):
        return self.__checked

    checked = property(get_checked)


class RadioButtonInput(WebSubmitInterfaceElement):
    def __init__(self, element_id, marc_field, value=None,
                 label='', size=None, checked=False, tooltip=None, name=None, session=None):
        WebSubmitInterfaceElement.__init__(self, element_id, marc_field, session, name,
                                           value, label, size, tooltip)
        self.__checked = False

    def get_html(self):
        if self.session.has_key(self.name):
            self.set_value(self.session[self.name])
        if __checked == True:
            html = H.input(type_="radio", name=self.name, value=self.value, 
                           id_=self.element_id, size=self.size, checked="checked")()
        else:
            html = H.input(type_="radio", name=self.name, value=self.value, 
                           id_=self.element_id, size=self.size)()
        return html

    def get_checked(self):
        return self.__checked

    checked = property(get_checked)

class FileInput(WebSubmitInterfaceElement):
    def __init__(self, element_id, marc_field, value=None,
                 label='', size=None, accept=None, tooltip=None, name=None, session=None):
        WebSubmitInterfaceElement.__init__(self, element_id, marc_field, session, name,
                                           value, label, size, tooltip)
        self.__files_accepted = accept

    def get_html(self):
        if self.session.has_key(self.name):
            self.set_value(self.session[self.name])
        html = H.input(type_="file", name=self.name, value=self.value, 
                       id_=self.element_id, size=self.size, accept=self.__files_accepted)()
        return html

    def get_files_accepted(self):
        return self.__files_accepted

    files_accepted = property(get_files_accepted)

class HiddenInput(WebSubmitInterfaceElement):
    def __init__(self, element_id, marc_field, value=None, name=None, session=None):
        WebSubmitInterfaceElement.__init__(self, element_id, marc_field, session, name, value)

    def get_html(self):
        if self.session.has_key(self.name):
            self.set_value(self.session[self.name])
        html = H.input(type_="hidden", name=self.name, value=self.value, id_=self.element_id)()
        return html

class TextArea(WebSubmitInterfaceElement):
    def __init__(self, element_id, marc_field, rows, cols, label='', 
                 tooltip=None, name=None, session=None):
        WebSubmitInterfaceElement.__init__(self, element_id, marc_field, 
                                           session, name, label=label, tooltip=tooltip)
        self.__rows = rows
        self.__cols = cols

    def get_html(self):
        #raise Exception(str(self.session))
        if self.session.has_key(self.name):
            self.set_value(self.session[self.name])
        html = H.textarea(name=self.name, id_=self.element_id, 
                          rows=self.__rows, cols=self.__cols)(self.value)
        return html

    def get_rows(self):
        return self.__rows

    def get_cols(self):
        return self.__cols

    rows = property(get_rows)
    cols = property(get_cols)

class Select(WebSubmitInterfaceElement):
    def __init__(self, element_id, marc_field, options_name_value_pairs, label='',
                 multiple=False, selected=None, size=None, tooltip=None, name=None, session=None):
        WebSubmitInterfaceElement.__init__(self, element_id, marc_field, session, name,
                                           label=label, size=size, tooltip=tooltip)
        self.__options_name_value_pairs = options_name_value_pairs
        self.__selected = selected
        self.__multiple = multiple
 
    def get_html(self):
        if self.session.has_key(self.name):
            self.set_value(self.session[self.name])
        if self.__multiple == True:
            html = create_html_select(self.options_name_value_pairs, self.name, self.selected, 
                                      multiple=True, id_=self.element_id, size=self.size)
        else:
            html = create_html_select(self.options_name_value_pairs, self.name, self.selected, 
                                      id_=self.element_id, size=self.size)
        return html

    def get_options_name_value_pairs(self):
        return self.__options_name_value_pairs

    def get_selected(self):
        return self.__selected

    def get_multiple(self):
        return self.__multiple

    options_name_value_pairs = property(get_options_name_value_pairs)
    selected = property(get_selected)
    multiple = property(get_multiple)
