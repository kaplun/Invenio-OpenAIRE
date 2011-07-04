def explode_records():
    def _explode_records(obj, engine):
        input_form = engine.getVar("input_form")
        # do some stuff with the input_form
        output_form = {}
        engine.setVar("output_form", output_form)
    return _explode_records
