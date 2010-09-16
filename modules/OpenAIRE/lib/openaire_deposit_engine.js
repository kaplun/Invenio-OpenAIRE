var gTipDefault = {
    position: {
        corner: {
            target: 'bottomMiddle',
            tooltip: 'topMiddle'
        },
    },
    adjust: {
        screen: true,
    },
    hide: {
        fixed: true,
    },
    border: {
        width: 7,
        radius: 5,
    },
    style: {
        width: {
            max: 500,
        },
        name: 'light',
        tip: 'topMiddle',
    }
}

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

function elaborateCheckMetadata(results, textStatus, XMLHttpRequest){
    var errors = results.errors;
    var warnings = results.warnings;
    var submittedpublicationid = results.submittedpublicationid;
    var newcontent = results.newcontent;
    var publicationid = results.publicationid;
    if (submittedpublicationid != undefined && newcontent != undefined) {
        $('#form_' + submittedpublicationid + ' div.body').hide('slow').html(newcontent).show('slow');
    } else {
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
}

function getPublicationMetadata(publicationid){
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

function backgroundsubmit(element, action) {
    var publicationid = element.id.split('_').pop();
    var data = getPublicationMetadata(publicationid);
    data['publicationid'] = publicationid;
    data['projectid'] = gProjectid;
    data['action'] = action;
    $.ajax({
        error: onAjaxError,
        url: gSite + '/deposit/backgroundsubmit',
        data: data,
        success: elaborateCheckMetadata
    });
}

$(document).ready(function(){
    $('div.OpenAIRE input').blur(function(){
        return backgroundsubmit(this, 'verify_field');
    });
    $('div.OpenAIRE textarea').blur(function(){
        return backgroundsubmit(this, 'verify_field');
    });
    $('div.OpenAIRE select').blur(function(){
        return backgroundsubmit(this, 'verify_field');
    });
    $('*[title]').qtip(gTipDefault);
})

function onAjaxError(XHR, textStatus, errorThrown){
  /*
   * Handle Ajax request errors.
   */
  alert('Request completed with status ' + textStatus +
    '\nResult: ' + XHR.responseText +
    '\nError: ' + errorThrown);
}


/* See: http://oranlooney.com/functional-javascript/ */
function Clone() { }
function clone(obj) {
    Clone.prototype = obj;
    return new Clone();
}