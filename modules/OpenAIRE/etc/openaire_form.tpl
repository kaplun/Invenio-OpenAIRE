<tr>
    <td align="right" valign="top" class="%(form_status)s">%(index)s</td>
    <td width="43%%" valign="top">
        <div id="tooltip_%(id)s" style="display: inline;">%(title)s</div>
        <br />
        <em id="tooltip_file_%(id)s">file: %(filename)s</em>
        <br />
        <div style="%(status_warning)s">
            <img src="images/box_alert.png" alt="%(status_warning_label)s" width="25" height="25" align="absmiddle" title="%(status_warning_label)s">
            <a href="javascript:void(0)" id="edit_%(id)s">Edit Metadata</a>
        </div>
        <div style="%(status_error)s">
            <img src="images/box_alert.png" alt="%(status_error_label)s" width="25" height="25" align="absmiddle" title="%(status_error_label)s">
            <a href="javascript:void(0)" id="edit_%(id)s">Edit Metadata</a>
        </div>
        <div style="%(status_ok)s">
            <img src="images/list_check.png" alt="%(status_ok_label)s" width="25" height="25" align="absmiddle" title="%(status_ok_label)s">
            <a href="javascript:void(0)" id="edit_%(id)s">Edit Metadata</a>
        </div>
        <div id="form_%(id)s">
            <p>
                <label for="language_%(id)s">%(language_label)s
                    <div id="error_language_%(id)s" class="error">%(error_language_value)s</div>
                    <div id="warning_language_%(id)s" class="warning">%(warning_language_value)s</div>
                </label>
                <select name="language_%(id)s" id="language_%(id)s" class="language">
                    %(language_options)s
                </select>
            </p>
            <p>
                <label for="title_%(id)s">%(title_label)s
                    <div id="error_title_%(id)s" class="error">%(error_title_value)s</div>
                    <div id="warning_title_%(id)s" class="warning">%(warning_title_value)s</div>
                </label>
                <br />
                <input type="text" name="title_%(id)s" id="title_%(id)s" value="%(title_value)s" size="30" class="title" />
            </p>
            <p>
                <label for="original_title_%(id)s">%(original_title_label)s
                    <div id="error_original_title_%(id)s" class="error">%(error_original_title_value)s</div>
                    <div id="warning_original_title_%(id)s" class="warning">%(warning_original_title_value)s</div>
                </label>
                <br />
                <input type="text" name="original_title_%(id)s" id="original_title_%(id)s" value="%(original_title_value)s" size="30" class="original_title" />
            </p>
            <p>
                <label for="authors_%(id)s">%(authors_label)s
                    <div id="error_authors_%(id)s" class="error">%(error_authors_value)s</div>
                    <div id="warning_authors_%(id)s" class="warning">%(warning_authors_value)s</div>
                </label>
                <br />
                <textarea name="authors_%(id)s" id="authors_%(id)s" cols="28" rows="5" class="authors">
                    %(authors)s
                </textarea>
            </p>
            <p>
                <label for="abstract_%(id)s">%(abstract_label)s
                    <div id="error_abstract_%(id)s" class="error">%(error_abstract_value)s</div>
                    <div id="warning_abstract_%(id)s" class="warning">%(warning_abstract_value)s</div>
                </label>
                <br />
                <textarea name="abstract_%(id)s" id="abstract_%(id)s" cols="28" rows="5" class="abstract">
                    %(abstract)s
                </textarea>
            </p>
            <p>
                <label for="original_abstract_%(id)s">%(original_abstract_label)s
                    <div id="error_original_abstract_%(id)s" class="error">%(error_original_abstract_value)s</div>
                    <div id="warning_original_abstract_%(id)s" class="warning" >%(warning_original_abstract_value)s</div>
                </label>
                <br />
                <textarea name="original_abstract_%(id)s" id="original_abstract_%(id)s" cols="28" rows="5" class="original_abstract">
                    %(original_abstract)s
                </textarea>
            </p>
            <p>
                <label for="journal_title_%(id)s">%(journal_title_label)s
                    <div id="error_journal_title_%(id)s" class="error">%(error_journal_title_value)s</div>
                    <div id="warning_journal_title_%(id)s" class="warning">%(warning_journal_title_value)s</div>
                </label>
                <br />
                <input type="text" name="journal_title_%(id)s" id="journal_title_%(id)s" value="%(journal_title_value)s" size="30" class="journal_title" />
            </p>
            <p>
                <label for="volume_%(id)s">%(volume_label)s</label>
                <input name="volume_%(id)s" type="text" id="volume_%(id)s" value="%(volume_value)s" size="4" class="volume" />
                <label for="issue_%(id)s">%(issue_label)s</label>
                <input name="issue_%(id)s" type="text" id="issue_%(id)s" value="%(issue_value)s" size="4" class="issue" />
                <label for="pages_%(id)s">%(pages_label)s</label>
                <input name="pages_%(id)s" type="text" id="pages_%(id)s" value="%(pages_value)s" size="8" class="pages" />
                <div id="error_volume_%(id)s" class="error">%(error_volume_value)s</div>
                <div id="warning_volume_%(id)s" class="warning">%(warning_volume_value)s</div>
                <div id="error_issue_%(id)s" class="error">%(error_issue_value)s</div>
                <div id="warning_issue_%(id)s" class="warning">%(warning_issue_value)s</div>
                <div id="error_pages_%(id)s" class="error">%(error_pages_value)s</div>
                <div id="warning_pages_%(id)s" class="warning">%(warning_pages_value)s</div>
            </p>
        </div>
    </td>
    </td>
    <td align="center" valign="top" width="27%%">
        <select id="access_rights_%(id)s" name="access_rights_%(id)s" class="access_rights">
            %(access_rights_options)s
        </select>
    </td>
    <td align="center" valign="top" nowrap="nowrap" width="17%%">
        <input name="embargo_date_%(id)s" type="text" id="embargo_date_%(id)s" value="%(embargo_date_value)s" size="10" maxlength="10" class="embargo_date" />
        <div id="error_embargo_date_%(id)s" class="error">%(error_embargo_date_value)s</div>
        <div id="warning_embargo_date_%(id)s" class="warning">%(warning_embargo_date_value)s</div>
    </td>
    <td width="10%" align="center" valign="top"><a href="#">%(remove_label)s</a></td>
</tr>
