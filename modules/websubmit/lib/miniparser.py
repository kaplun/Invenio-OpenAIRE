## $Id: miniparser.py,v 1.4 2007/06/20 15:18:53 nich Exp $

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

"""Take a string that represents the arguments to be passed in a function
   call, and parse it, producing a tuple of values that can be passed
   directly to the function.
   Written for use with WSC (WebSubmit Checks) because the parameters to be
   passed to WSCs are written in string form in an XML config file.
   Example of use:
   >>> import miniparser
   >>> s = '(wse_author, "hello world(!)", 45, wse_title)'
   >>> p = miniparser.Parser(s, {"wse_author" : "<wse_author object>", \
                                 "wse_title" : "<wse_title object>"})
   >>> p.parse()
   ('<wse_author object>', 'hello world(!)', 45, '<wse_title object>')

   Note that the "wse objects" are just strings in this simple example.
"""

__revision__ = "$Id: miniparser.py,v 1.4 2007/06/20 15:18:53 nich Exp $"

# Tokens:
EOF = -1
BAD = 0
IDENT = BAD + 1
NUMBER = IDENT + 1
STRING = NUMBER + 1
LPAREN = STRING + 1
RPAREN = LPAREN + 1
COMMA = RPAREN + 1

class Scanner:

    def __init__(self, line):
        self.__EOF_CH = '\n'
        self.__line = line + self.__EOF_CH
        self.__char_pos = 0
        self.__ch = self.__line[self.__char_pos]
        self.__buffer = ''
        self._chars =  ''
        self._token = EOF
        
    def next_token(self):
        while self.__ch in (' ', '\t'):
            self.__next_ch()
        self._token = self._read_token()
        
    def __next_ch(self):
        if self.__ch == self.__EOF_CH:
            return
        self.__char_pos += 1
        self.__ch = self.__line[self.__char_pos] 
    
    def _read_token(self):
        self.__buffer = ''
        if self.__ch == '0':
            self._chars = '0'
            return NUMBER
        elif self.__ch in '123456789':
            while self.__ch in '123456789':
                self.__buffer += self.__ch
                self.__next_ch()
            self._chars = self.__buffer
            return NUMBER
        elif self.__ch == '"':
            escaping = False
            self.__next_ch()
            while self.__ch != '"':
                if self.__ch == '\\':
                    self.__next_ch()  
                self.__buffer += self.__ch
                self.__next_ch()
            self._chars = self.__buffer
            self.__next_ch()
            return STRING
        elif self.__ch.isalpha():
            while (self.__ch.isalnum() or self.__ch == '_'):
                self.__buffer += self.__ch
                self.__next_ch()
            self._chars = self.__buffer
            return IDENT
        elif self.__ch == '(':
            self.__next_ch()
            return LPAREN
        elif self.__ch == ')':
            self.__next_ch()
            return RPAREN
        elif self.__ch == ',':
            self.__next_ch()
            return COMMA
        elif self.__ch == self.__EOF_CH:
            return EOF
        else:
            self.__next_ch()
            return BAD
            

class Parser(Scanner):
    def __init__(self, line, elements):
        Scanner.__init__(self, line)
        self._elements = elements
        self.next_token()
        
    def __accept(self, expected_token):
        if self._token == expected_token:
            self.next_token()
        else:
            raise SyntaxError
    
    def parse(self):
        """returns a tuple of values to be used directly in func call"""
        out = self._params()
        self.__accept(EOF)
        return out
    
    def _params(self):
        """ Params = '(' param {',' param} ')' """
        out = []
        self.__accept(LPAREN)
        if self._token in (IDENT, STRING, NUMBER, LPAREN):
            out.append(self._param())
            while self._token == COMMA:
                # a comma should always be followed by a param!
                self.next_token()
                out.append(self._param())
        self.__accept(RPAREN)
        return tuple(out)
    
    def _param(self):
        """Param = IDENT | STRING | NUMBER | Tuple"""
        if self._token == IDENT:
            out = self._ident()
        
        elif self._token == STRING:
            out = self._chars
            self.next_token()
        
        elif self._token == NUMBER:
            out = int(self._chars)
            self.next_token()
        
        elif self._token == LPAREN:
            out = self._params() 
        else:
            raise SyntaxError    
        return out    
        
    def _ident(self):
        ### TODO: find the value or the pointer to the object of the given identifier... (eval?)
        ident_name = self._chars
        self.next_token()
        return self._elements[ident_name]
            
         
    
                
