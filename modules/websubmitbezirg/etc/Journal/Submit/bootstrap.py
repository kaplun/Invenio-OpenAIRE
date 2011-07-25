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
    NoPages(),
    Language(),
    Email(Name="email1"),
    Url(Name="url1")
)


Workflow(

)
