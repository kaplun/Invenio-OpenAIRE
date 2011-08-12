from time import strptime

def validateDate(text, date_format):
    try:
         strptime(text, date_format)
    except:
        return False
    else:
        return True
