function update_embargo_date(event){
    if ($(event.data.from_id).val() == 'embargoedAccess') {
        $(event.data.to_id).removeAttr("disabled").show('slow');
    } else {
        $(event.data.to_id).attr("disabled", "disabled").hide('slow');
    }
}

function update_language(event){
    if ($(event.data.from_id).val() != 'eng') {
        $(event.data.to_id).removeAttr("disabled").show('slow');
    } else {
        $(event.data.to_id).attr("disabled", "disabled").hide('slow');
    }
}

function elaborate_check_metadata(results, textStatus, XMLHttpRequest){
    var errors = results.errors;
    var warnings = results.warnings;
    var publicationid = results.publicationid;
    $('#form_' + publicationid + ' .error').hide('slow');
    $('#form_' + publicationid + ' .warning').hide('slow');
    $('.warning').hide();
    for (var error in errors) {
        $('#error_' + error).html(errors[error][0]).show('slow');
    }
    for (var warning in warnings) {
        $('#warning_' + warning).html(warnings[warning][0]).show('slow');
    }
}

function get_publication_metadata(publicationid){
    var ret = {};
    $('#form_' + publicationid + ' input').each(function(){
        ret[this.id] = this.value;
    });
    $('#form_' + publicationid + ' select').each(function(){
        ret[this.id] = this.value;
    });
    $('#form_' + publicationid + ' textarea').each(function(){
        ret[this.id] = this.value;
    });
    return ret;
}

function object_to_str(o){
    var ret = 'start';
    for (var key in o) {
        ret += key + ' = ' + o[key] + '\n';
    }
    ret += 'end';
    return ret;
}

function submit_form(){
    var publicationid = this.id.split('_').pop();
    var data = get_publication_metadata(publicationid);
    data['publicationid'] = publicationid;
    data['check_required_fields'] = 1;
    $.ajax({
        error: onAjaxError,
        url: OpenAIREURL + '/deposit/checkmetadata',
        data: data,
        success: elaborate_check_metadata
    });
}

function verify_field(){
    var publicationid = this.id.split('_').pop();
    var data = get_publication_metadata(publicationid);
    data['publicationid'] = publicationid;
    data['check_required_fields'] = 0;
    $.ajax({
        error: onAjaxError,
        url: OpenAIREURL + '/deposit/checkmetadata',
        data: data,
        success: elaborate_check_metadata
    });
}

$(document).ready(function(){
    $('div.OpenAIRE input').blur(verify_field);
    $('div.OpenAIRE textarea').blur(verify_field);
    $('div.OpenAIRE select').blur(verify_field);
})

function onAjaxError(XHR, textStatus, errorThrown){
  /*
   * Handle Ajax request errors.
   */
  alert('Request completed with status ' + textStatus +
    '\nResult: ' + XHR.responseText +
    '\nError: ' + errorThrown);
}
