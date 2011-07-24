# -*- coding: utf-8 -*-

import re

def validateEmail(email):
	if len(email) > 7:
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
			return 1
	return 0

def validateUrl(url):
    if re.match("^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$", url) != None:
        return 1
    return 0
