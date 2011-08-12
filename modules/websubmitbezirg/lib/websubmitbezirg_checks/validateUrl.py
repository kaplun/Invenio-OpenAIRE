def validateUrl(url):
    import re
    #import simplejson # this will fail, because this module is not implemented in pyjamas and turns this check automatically to server check
    if re.match("^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$", url) != None:
            return True
    return False


