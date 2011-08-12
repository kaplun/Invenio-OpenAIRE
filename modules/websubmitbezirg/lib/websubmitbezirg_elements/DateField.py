import sys
if sys.version_info[3] == 'pyjamas':
    from pyjamas.ui.Calendar import DateField as DF
else:
    class NullClass(object):
        def __init__(self, *args, **kwargs):
            pass
    DF = NullClass

DF.icon_img = "/websubmitbezirg-static/icon_calendar.gif"
DateField = DF
