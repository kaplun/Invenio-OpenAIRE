# -*- coding: utf-8 -*-

import re

def validateEmail(email):
	if len(email) > 7:
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
			return 1
	return 0

def validateURL(url):
    #if re.match("^(http://|https://)?(([a-z0-9]?([-a-z0-9]*[a-z0-9]+)?){1,63}\.)+[a-z]{2,6}", url) != None:
    if re.match("^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$", url) != None:
        return 1
    return 0
