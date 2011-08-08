from invenio.workflow_engine import HaltProcessing

def explode_records():
    def _explode_records(obj, engine):
        form = engine.getVar("input_form")
        nopages2 = form['nopages1']
        url2 = form['url1']
        output_form = {"nopages2": nopages2, "url2": url2}
        engine.setVar("output_form", output_form)
    return _explode_records
