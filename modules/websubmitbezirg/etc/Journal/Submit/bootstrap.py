try:
    from engine import *
    from elements import *
except:
    pass


Interface(
    Title(),
    Author(),
    Abstract(),
    Published(),
    NoPages(Name="pages1"),
    Language(),
    Email(Name="email1", Required=True),
    Url(Name="url1"),
    Password(Name="p1", Required=True)
)


Workflow(

)
