/* Global Tooltips configuration :-) */
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
        $(event.data.to_id).show('slow');
    } else {
        $(event.data.to_id).hide('slow');
    }
}

function update_language(event){
    if ($(event.data.from_id).val() != 'eng') {
        $(event.data.to_id).removeAttr("disabled").show('slow');
    } else {
        $(event.data.to_id).attr("disabled", "disabled").hide('slow');
    }
}

function elaborateAjaxGateway(results, textStatus, XMLHttpRequest){
    var errors = results.errors;
    var warnings = results.warnings;
    var addclasses = results.addclasses;
    var delclasses = results.delclasses;
    var substitutions = results.substitutions;
    for (var error in errors) {
        if (errors[error]) {
            $('#error_' + error).html(errors[error]).show('slow');
        } else {
            $('#error_' + error).hide('slow')
        }
    }
    for (var warning in warnings) {
        if (warnings[warning]) {
            $('#warning_' + warning).html(warnings[warning]).show('slow');
        } else {
            $('#warning_' + warning).hide('slow')
        }
    }
    for (var query in addclasses) {
        $(query).addClass(addclasses[query]);
    }
    for (var query in delclasses) {
        $(query).removeClass(delclasses[query]);
    }
    for (var query in substitutions) {
        $(query).hide('slow').html(substitutions[query]).show('slow')
    }
    return 0;
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

function ajaxGateway(element, action) {
    var publicationid = element.id.split('_').pop();
    var data = getPublicationMetadata(publicationid);
    data['publicationid'] = publicationid;
    data['projectid'] = gProjectid;
    data['action'] = action;
    data['current_field'] = element.id;
    $.ajax({
        error: onAjaxError,
        url: gSite + '/deposit/ajaxgateway',
        data: data,
        success: elaborateAjaxGateway
    });
}

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

/* Initialization */
$(document).ready(function(){
    $('div.OpenAIRE input').blur(function(){
        return ajaxGateway(this, 'verify_field');
    });
    $('div.OpenAIRE textarea').blur(function(){
        return ajaxGateway(this, 'verify_field');
    });
    $('div.OpenAIRE select').blur(function(){
        return ajaxGateway(this, 'verify_field');
    });
    $('*[title]').qtip(gTipDefault);
    $('div.error').filter(function(){
        return this.textContent == '';
    }).hide()
    $('div.warning').filter(function(){
        return this.textContent == '';
    }).hide()
    $('input[hint],textarea[hint]').inputHint({hintAttr: "hint"});
    $('tr.body').hide();
})


