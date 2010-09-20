<div class="OpenAIRE" id="form_%(id)s">
    <div class="index">%(index)s
        <div class="metadata note">
            <div class="header note" id="header_%(id)s">
                <div>
                    %(title_value)s
                    <br />
                    %(fileinfo)s
                    <br />
                </div>
                <div>
                    <img title="%(access_rights_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                    <select id="access_rights_%(id)s" name="access_rights_%(id)s" class="access_rights">
                        %(access_rights_options)s
                    </select>
                </div>
                <div id="embargo_date_container_%(id)s">
                    <img title="%(embargo_date_tooltip)s" class="tooltip" src="%(site)s/img/help.png" hint="%(embargo_date_hint)s"/>
                    <input name="embargo_date_%(id)s" type="text" id="embargo_date_%(id)s" value="%(embargo_date_value)s" size="10" maxlength="10" class="datepicker" />
                    <div id="error_embargo_date_%(id)s" class="error">%(error_embargo_date_value)s</div>
                    <div id="warning_embargo_date_%(id)s" class="warning">%(warning_embargo_date_value)s</div>
                </div>
                <div>
                    <a href="%(site)s/deposit?projectid=%(projectid)s&amp;delete=%(id)s&amp;ln=%(ln)s" id="remove_%(id)s"><img src="%(site)s/img/smallbin.gif" /> %(remove_label)s</a>
                </div>
                <div class="clear"></div>
            </div>
            <div class="body" id="body_%(id)s">
                <div>
                    <img title="%(publication_date_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                    <label for="publication_date_%(id)s">%(publication_date_label)s</label>
                    <input name="publication_date_%(id)s" type="text" id="publication_date_%(id)s" value="%(publication_date_value)s" size="10" maxlength="10" class="datepicker" />
                    <div id="error_publication_date_%(id)s" class="error">%(error_publication_date_value)s</div>
                    <div id="warning_publication_date_%(id)s" class="warning">%(warning_publication_date_value)s</div>
                </div>
                <fieldset class="left">
                    <legend>%(english_language_label)s</legend>
                    <div>
                        <img title="%(title_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                        <label for="title_%(id)s">%(title_label)s
                            <div id="error_title_%(id)s" class="error">%(error_title_value)s</div>
                            <div id="warning_title_%(id)s" class="warning">%(warning_title_value)s</div>
                        </label>
                        <br />
                        <input type="text" name="title_%(id)s" id="title_%(id)s" value="%(title_value)s" size="30" class="title" />
                    </div>
                    <div>
                        <img title="%(abstract_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                        <label for="abstract_%(id)s">%(abstract_label)s
                            <div id="error_abstract_%(id)s" class="error">%(error_abstract_value)s</div>
                            <div id="warning_abstract_%(id)s" class="warning">%(warning_abstract_value)s</div>
                        </label>
                        <br />
                        <textarea name="abstract_%(id)s" id="abstract_%(id)s" cols="28" rows="5" class="abstract">%(abstract)s</textarea>
                    </div>
                </fieldset>
                <fieldset class="right">
                    <legend>%(original_language_label)s</legend>
                    <div>
                        <img title="%(language_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                        <label for="language_%(id)s">%(language_label)s
                            <div id="error_language_%(id)s" class="error">%(error_language_value)s</div>
                            <div id="warning_language_%(id)s" class="warning">%(warning_language_value)s</div>
                        </label>
                        <select name="language_%(id)s" id="language_%(id)s" class="language" style="width: 100px">
                            %(language_options)s
                        </select>
                    </div>
                    <div>
                        <img title="%(original_abstract_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                        <label for="original_abstract_%(id)s">%(original_abstract_label)s
                            <div id="error_original_abstract_%(id)s" class="error">%(error_original_abstract_value)s</div>
                            <div id="warning_original_abstract_%(id)s" class="warning" >%(warning_original_abstract_value)s</div>
                        </label>
                        <br />
                        <textarea name="original_abstract_%(id)s" id="original_abstract_%(id)s" cols="28" rows="5" class="original_abstract">%(original_abstract)s</textarea>
                    </div>
                </fieldset>
                <div class="clear"></div>
                <div>
                    <img title="%(journal_title_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                    <label for="journal_title_%(id)s">%(journal_title_label)s
                        <div id="error_journal_title_%(id)s" class="error">%(error_journal_title_value)s</div>
                        <div id="warning_journal_title_%(id)s" class="warning">%(warning_journal_title_value)s</div>
                    </label>
                    <br />
                    <input type="text" name="journal_title_%(id)s" id="journal_title_%(id)s" value="%(journal_title_value)s" size="30" class="journal_title" />
                </div>
                <div>
                    <img title="%(volume_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                    <label for="volume_%(id)s">%(volume_label)s</label>
                    <input name="volume_%(id)s" type="text" id="volume_%(id)s" value="%(volume_value)s" size="4" class="volume" />
                    <br />
                    <img title="%(issue_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                    <label for="issue_%(id)s">%(issue_label)s</label>
                    <input name="issue_%(id)s" type="text" id="issue_%(id)s" value="%(issue_value)s" size="4" class="issue" />
                    <br />
                    <img title="%(pages_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                    <label for="pages_%(id)s">%(pages_label)s</label>
                    <input name="pages_%(id)s" type="text" id="pages_%(id)s" value="%(pages_value)s" size="8" class="pages" />
                    <div id="error_volume_%(id)s" class="error">%(error_volume_value)s</div>
                    <div id="warning_volume_%(id)s" class="warning">%(warning_volume_value)s</div>
                    <div id="error_issue_%(id)s" class="error">%(error_issue_value)s</div>
                    <div id="warning_issue_%(id)s" class="warning">%(warning_issue_value)s</div>
                    <div id="error_pages_%(id)s" class="error">%(error_pages_value)s</div>
                    <div id="warning_pages_%(id)s" class="warning">%(warning_pages_value)s</div>
                </div>
                <div>
                    <img title="%(authors_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                    <label for="authors_%(id)s">%(authors_label)s
                        <div id="error_authors_%(id)s" class="error">%(error_authors_value)s</div>
                        <div id="warning_authors_%(id)s" class="warning">%(warning_authors_value)s</div>
                    </label>
                    <br />
                    <textarea name="authors_%(id)s" id="authors_%(id)s" cols="28" rows="5" class="authors">%(authors)s</textarea>
                </div>
            </div>
        </div>
    </div>
    <div class="clear"></div>
    <div><input type="submit" value="%(save_label)s" id="save_%(id)s"/><input type="submit" value="%(submit_label)s" id="submit_%(id)s"/></div>
</div>
<script type="text/javascript">
$(document).ready(function(){
    $('#access_rights_%(id)s').bind('change', {from_id: '#access_rights_%(id)s', to_id: '#embargo_date_container_%(id)s'}, update_embargo_date);
    $('#access_rights_%(id)s').trigger('change');
    $('#language_%(id)s').bind('change', {from_id: '#language_%(id)s', to_id: '.original_language_column_%(id)s'}, update_language);
    $('#language_%(id)s').trigger('change');
    $('#save_label_%(id)s').click(function(){
        backgroundsubmit('save');
        return 0;
    });
    $('#submit_label_%(id)s').click(function(){
        backgroundsubmit('submit');
        return 0;
    });
    $('#remove_%(id)s').click(function(){
        return confirm("%(remove_confirm)s");
    });
    $('#header_%(id)s').click(function(){
        $('#body_%(id)s').toggle();
    });
});
</script>
