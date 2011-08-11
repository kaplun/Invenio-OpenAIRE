from invenio.workflow_engine import HaltProcessing

def explode_records():
    def _explode_records(obj, engine):
        form = engine.getVar("input_form")
        nopages2 = form['nopages1']
        url2 = form['url1']
        checkbox_a2 = form['checkbox_a1'] if 'checkbox_a1' in form else False
        checkbox_b2 = form['checkbox_b1'] if 'checkbox_b1' in form else False
        language2 = form['language1']
        output_form = {"nopages2": nopages2, "url2": url2, "checkbox_a2": checkbox_a2, "checkbox_b2": checkbox_b2, "language2": language2}
        engine.setVar("output_form", output_form)
    return _explode_records
