try:
    from engine import *
    from elements import *
    from basic_checks import *
except:
    pass

from Journal.Submit import interface

x = PluginContainer(os.path.join(CFG_PYLIBDIR, 'invenio', 'websubmit_checks', '*.py')
globals().update(x)

x['Title']()


submitInterface = Interface("Submit",
                             Title(),
                             Author(),
                             Abstract(),
                             Published(),
                             NoPages(Name="pages1", Check=launch_missiles),
                             Language(),
                             Email(Name="email1", Required=True),
                             Url(Name="url1"),
                             Password(Name="p1", Required=True)
                             )

submitWorkflow = Workflow("Submit",
                           load_interface(submitInterface),
                           
modifyWorkflow = Workflow("Modify"
                          modify_interface(), # <-- this ask for the reportnumber
                          get_record(),
                          check_authorization(),
                          explode_record(),
                          prefilled_submit_interface(),
                          load_interface(i)
                           )
