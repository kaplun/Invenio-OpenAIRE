def validateUrl(url):
    import re
    if re.match("^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$", url) != None:
            return True
    return False


