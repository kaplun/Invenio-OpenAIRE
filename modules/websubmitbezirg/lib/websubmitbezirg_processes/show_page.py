from invenio.workflow_engine import HaltProcessing

def show_page(p):
    def show_page_(session,engine):
        engine.setVar('__current_page_name',p.name)
        raise HaltProcessing
    show_page_.__page__ = p
    return show_page_



