<tr class="header odd" id="header_row_%(id)s">
    <td width="5%%" id="status_%(id)s" rowspan="2" class="%(status)s"></td>
    <td width="40%%" valign="top">
        %(publication_information)s
        <br />
        %(fulltext_information)s
        <br />
    </td>
    <td width="35%%" valign="top">
        <img title="%(access_rights_tooltip)s" class="tooltip mandatory" src="%(site)s/img/help.png" />
        <select id="access_rights_%(id)s" name="access_rights_%(id)s" class="access_rights">
            %(access_rights_options)s
        </select>
        <div id="error_access_rights_%(id)s" class="error">%(error_embargo_date_value)s</div>
        <div id="warning_access_rights_%(id)s" class="warning">%(warning_embargo_date_value)s</div>
        <div id="embargo_date_container_%(id)s">
            <img title="%(embargo_date_tooltip)s" class="tooltip mandatory" src="%(site)s/img/help.png"/>
            <input name="embargo_date_%(id)s" type="text" id="embargo_date_%(id)s" value="%(embargo_date_value)s" size="%(embargo_date_size)s" maxlength="10" class="datepicker" />
            <div id="error_embargo_date_%(id)s" class="error">%(error_embargo_date_value)s</div>
            <div id="warning_embargo_date_%(id)s" class="warning">%(warning_embargo_date_value)s</div>
        </div>
    </td>
    <td width="20%%" valign="top">
        <a href="javascript:void(0)" id="edit_metadata_%(id)s"><img src="%(site)s/img/wb-notes.png" alt="%(edit_metadata_label)s"/> <strong>%(edit_metadata_label)s</strong></a><br />
        <a href="%(site)s/deposit?projectid=%(projectid)s&amp;delete=%(id)s&amp;ln=%(ln)s" id="remove_%(id)s"><img src="%(site)s/img/smallbin.gif" /> %(remove_label)s</a>
    </td>
</tr>
<tr class="body even" id="body_row_%(id)s">
    <td colspan="3" valign="top">
        <div id="body_%(id)s" class="body">
            <p><em>%(mandatory_label)s</em></p>
            <fieldset>
                <legend>%(projects_information_label)s</legend>
                <img title="%(projects_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                <label class="mandatory">%(projects_description)s</label>
                %(projects_information)s
            </fieldset>
            <div class="clear"></div>
            <fieldset>
                <div>
                    <img title="%(authors_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                    <label for="authors_%(id)s" class="mandatory">%(authors_label)s
                    </label>
                    <br />
                    <textarea name="authors_%(id)s" id="authors_%(id)s" cols="60" rows="5" class="authors">%(authors_value)s</textarea>
                    <div id="error_authors_%(id)s" class="error">%(error_authors_value)s</div>
                    <div id="warning_authors_%(id)s" class="warning">%(warning_authors_value)s</div>
                </div>
            </fieldset>
            <div class="clear"></div>
            <fieldset>
                <legend>%(english_language_label)s</legend>
                <div>
                    <img title="%(title_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                    <label for="title_%(id)s" class="mandatory">%(title_label)s
                    </label>
                    <br />
                    <input type="text" name="title_%(id)s" id="title_%(id)s" value="%(title_value)s" size="75" class="title" />
                    <div id="error_title_%(id)s" class="error">%(error_title_value)s</div>
                    <div id="warning_title_%(id)s" class="warning">%(warning_title_value)s</div>
                </div>
                <div>
                    <img title="%(abstract_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                    <label for="abstract_%(id)s" class="mandatory">%(abstract_label)s
                    </label>
                    <br />
                    <textarea name="abstract_%(id)s" id="abstract_%(id)s" cols="60" rows="5" class="abstract">%(abstract_value)s</textarea>
                    <div id="error_abstract_%(id)s" class="error">%(error_abstract_value)s</div>
                    <div id="warning_abstract_%(id)s" class="warning">%(warning_abstract_value)s</div>
                </div>
            </fieldset>
            <fieldset>
                <legend>%(original_language_label)s</legend>
                <div>
                    <img title="%(language_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                    <label for="language_%(id)s" class="mandatory">%(language_label)s
                    </label>
                    <select name="language_%(id)s" id="language_%(id)s" class="language" style="width: 100px">
                        %(language_options)s
                    </select>
                    <div id="error_language_%(id)s" class="error">%(error_language_value)s</div>
                    <div id="warning_language_%(id)s" class="warning">%(warning_language_value)s</div>
                </div>
                <div id="original_language_container_%(id)s">
                    <div>
                        <img title="%(original_title_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                        <label for="original_title_%(id)s">%(original_title_label)s
                        </label>
                        <br />
                        <input type="text" name="original_title_%(id)s" id="original_title_%(id)s" value="%(original_title_value)s" size="75" class="original_title mandatory" />
                        <div id="error_original_title_%(id)s" class="error">%(error_original_title_value)s</div>
                        <div id="warning_original_title_%(id)s" class="warning">%(warning_original_title_value)s</div>
                    </div>
                    <div>
                        <img title="%(original_abstract_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                        <label for="original_abstract_%(id)s">%(original_abstract_label)s
                        </label>
                        <br />
                        <textarea name="original_abstract_%(id)s" id="original_abstract_%(id)s" cols="60" rows="5" class="original_abstract">%(original_abstract_value)s</textarea>
                        <div id="error_original_abstract_%(id)s" class="error">%(error_original_abstract_value)s</div>
                        <div id="warning_original_abstract_%(id)s" class="warning" >%(warning_original_abstract_value)s</div>
                    </div>
                </div>
            </fieldset>
            <div class="clear"></div>
            <fieldset>
                <legend>%(publication_information_label)s</legend>
                <div>
                    <img title="%(publication_date_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                    <label for="publication_date_%(id)s" class="mandatory">%(publication_date_label)s</label>
                    <input name="publication_date_%(id)s" type="text" id="publication_date_%(id)s" value="%(publication_date_value)s" size="10" maxlength="10" class="datepicker" />
                    <div id="error_publication_date_%(id)s" class="error">%(error_publication_date_value)s</div>
                    <div id="warning_publication_date_%(id)s" class="warning">%(warning_publication_date_value)s</div>
                </div>
               <div>
                    <img title="%(journal_title_tooltip)s" class="tooltip" src="%(site)s/img/help.png" />
                    <label for="journal_title_%(id)s">%(journal_title_label)s
                    </label>
                    <br />
                    <input type="text" name="journal_title_%(id)s" id="journal_title_%(id)s" value="%(journal_title_value)s" size="75" class="journal_title" />
                    <div id="error_journal_title_%(id)s" class="error">%(error_journal_title_value)s</div>
                    <div id="warning_journal_title_%(id)s" class="warning">%(warning_journal_title_value)s</div>
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
            </fieldset>
            <div class="clear"></div>
            <input type="submit" value="%(save_label)s" name="save_%(id)s" id="save_%(id)s"/><input type="submit" value="%(submit_label)s" name="submit_%(id)s" id="submit_%(id)s"/>
        </div>
    </td>
</tr>
<script type="text/javascript">// <![CDATA[
    $(document).ready(function(){
        $('#access_rights_%(id)s').bind('change', {
            from_id: '#access_rights_%(id)s',
            to_id: '#embargo_date_container_%(id)s'
        }, update_embargo_date);
        $('#access_rights_%(id)s').trigger('change');
        $('#language_%(id)s').bind('change', {
            from_id: '#language_%(id)s',
            to_id: '#original_language_container_%(id)s'
        }, update_language);
        update_language({
            data: {
                from_id: '#language_%(id)s',
                to_id: '#original_language_container_%(id)s'
            }
        });
        $('#save_%(id)s').click(function(event){
            var element = this;
            ajaxGateway(element, 'save');
            event.preventDefault();
            return 0;
        });
        $('#submit_%(id)s').click(function(event){
            var element = this;
            ajaxGateway(element, 'submit');
            event.preventDefault();
            return 0;
        });
        $('#remove_%(id)s').click(function(){
            return confirm("%(remove_confirm)s");
        });
        $('#edit_metadata_%(id)s,#status_%(id)s').click(function(){
            $('#body_%(id)s').toggle('slow');
            return false;
        });
        $('#journal_title_%(id)s').autocomplete({
            source: "%(site)s/kb/export?kbname=journal_name&amp;format=jquery&amp;ln=%(ln)s&amp;limit=100"
        });
        $('#body_%(id)s').hide();
    });
// ]]></script>