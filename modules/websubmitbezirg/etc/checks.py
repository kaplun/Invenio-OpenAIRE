# -*- coding: utf-8 -*-

import re

def validateNoPages(noPages):
    return noPages.isdigit()

def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False

def validateUrl(url):
    if re.match("^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$", url) != None:
            return True
    return False
        
        
def validatePassword(password):
    return password.isalnum() and len(password)>=8



