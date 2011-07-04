def fill_test():
    def _fill_test(obj, engine):
        # take the input_form sent by the user
        input_form = engine.getVar("input_form")

        # process it
        nopages = input_form['nopages1']
        url = input_form['url1']
        email = input_form['email1']
        p = input_form['p1']

        if 'ca1' in input_form:
            ca = input_form['ca1'] 
        else: 
            ca = False
        if 'cb1' in input_form:
            cb = input_form['ca1'] 
        else: 
            cb = False

        published = input_form['published1']
        language = input_form['language1']

        # create the output_form
        output_form = {'nopages1': nopages,
                       'url1': url,
                       'email1': email,
                       'p1': p,
                       'ca1': ca,
                       'cb1': cb,
                       'published1': published,
                       'language1': language
                       }
        engine.setVar("output_form", output_form)
    return _fill_test
