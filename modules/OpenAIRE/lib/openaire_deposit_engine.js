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
    var hiddens = results.hiddens;
    var appends = results.appends;
    var showns = results.showns;
    for (var error in errors) {
        if (errors[error]) {
            $('#error_' + error).html(errors[error]).fadeIn('slow');
        } else {
            $('#error_' + error).fadeOut('slow')
        }
    }
    for (var warning in warnings) {
        if (warnings[warning]) {
            $('#warning_' + warning).html(warnings[warning]).fadeIn('slow');
        } else {
            $('#warning_' + warning).fadeOut('slow')
        }
    }
    for (var query in addclasses) {
        $(query).addClass(addclasses[query]);
    }
    for (var query in delclasses) {
        $(query).removeClass(delclasses[query]);
    }
    for (var query in hiddens) {
        $(hiddens[query]).hide('slow');
    }
    for (var query in appends) {
        $(query).append(appends[query]);
    }
    for (var query in showns) {
        $(showns[query]).show('slow');
    }
    return 0;
}

function getPublicationMetadata(publicationid){
    var ret = {};
    $('#body_row_' + publicationid + ' input').each(function(){
        ret[this.id] = this.value;
    });
    $('#body_row_' + publicationid + ' select').each(function(){
        ret[this.id] = this.value;
    });
    $('#body_row_' + publicationid + ' textarea').each(function(){
        ret[this.id] = this.value;
    });
    $('#header_row_' + publicationid + ' input').each(function(){
        ret[this.id] = this.value;
    });
    $('#header_row_' + publicationid + ' select').each(function(){
        ret[this.id] = this.value;
    });
    $('#header_row_' + publicationid + ' textarea').each(function(){
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
    $.post(gSite + '/deposit/ajaxgateway', data, elaborateAjaxGateway, "json");
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
    $('div.OpenAIRE input').focusout(function(){
        return ajaxGateway(this, 'verify_field');
    });
    $('div.OpenAIRE textarea').focusout(function(){
        return ajaxGateway(this, 'verify_field');
    });
    $('div.OpenAIRE select').focusout(function(){
        return ajaxGateway(this, 'verify_field');
    });
    $('*[title]').qtip(gTipDefault);
    $('div.error').filter(function(){
        return this.textContent == '';
    }).hide()
    $('div.warning').filter(function(){
        return this.textContent == '';
    }).hide()
    $.datepicker.setDefaults($.datepicker.regional[gLn]);
})


