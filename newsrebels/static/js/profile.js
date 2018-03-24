$(function() {
  $('#table').bootstrapTable({
    data: data
  });
  $('#table1').bootstrapTable({
    data: data_sug
  });
});

//code taken from: http://www.the-art-of-web.com/javascript/validate-password/
function checkUserUpdateSettingsForm() {
  var form = document.getElementById("update_user_settings");
  re = /^\w+$/;
  if (form.username.value != "" && !re.test(form.username.value)) {
    $('#formErrorMessage').text("Error: Username must contain only letters, digits and underscores!")
    $('#formErrorContainer').show();
    return false;
  }

  re = /^[a-zA-Z]+$/;
  if (form.first_name.value != "" && !re.test(form.first_name.value)) {
    $('#formErrorMessage').text("Error: First Name must contain only letters!")
    $('#formErrorContainer').show();
    return false;
  }

  re = /^[a-zA-Z]+$/;
  if (form.last_name.value != "" && !re.test(form.last_name.value)) {
    $('#formErrorMessage').text("Error: Last Name must contain only letters!")
    $('#formErrorContainer').show();
    return false;
  }
  if (form.password.value != "") {
    if (form.password.value == form.password2.value) {
      if (form.password.value.length < 6) {
        $('#formErrorMessage').text("Error: Password must contain at least six characters!")
        $('#formErrorContainer').show();
        return false;
      }
      if (form.password.value == form.username.value) {
        $('#formErrorMessage').text("Error: Password must be different from Username!")
        $('#formErrorContainer').show();
        return false;
      }
      re = /[0-9]/;
      if (!re.test(form.password.value)) {
        $('#formErrorMessage').text("Error: password must contain at least one number (0-9)!")
        $('#formErrorContainer').show();
        return false;
      }
      re = /[a-z]/;
      if (!re.test(form.password.value)) {
        $('#formErrorMessage').text("Error: password must contain at least one lowercase letter (a-z)!")
        $('#formErrorContainer').show();
        return false;
      }
      re = /[A-Z]/;
      if (!re.test(form.password.value)) {
        $('#formErrorMessage').text("Error: password must contain at least one uppercase letter (A-Z)!")
        $('#formErrorContainer').show();
        return false;
      }
    } else {
      $('#formErrorMessage').text("Error: Please check that you've entered and confirmed your password!")
      $('#formErrorContainer').show();
      return false;
    }
  }

  if (form.first_name.value == "" && form.last_name.value == "" && form.username.value == "" && form.email.value == "" && form.password.value == "") {
    $('#formErrorMessage').text("Please enter a value to an input to update it, before you submit this form!!!");
    $('#formErrorContainer').show();
    return false;
  }
  return true;
}


//https://stackoverflow.com/questions/5717093/check-if-a-javascript-string-is-a-url
function isURL(str) {
  return /^(?:\w+:)?\/\/([^\s\.]+\.\S{2}|localhost[\:?\d]*)\S*$/.test(str);
}

function jsonHasUrlValue(jsonObj, url) {
  for (var index = 0; index < jsonObj.length; ++index) {
    if (jsonObj[index].rss_url === url) {
      return true;
    }
  }
  return false;
}

// using jQuery
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function deleteRssForThisUser(url, callback) {
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  $.ajax({
    async: true,
    url: 'http://localhost:8000/rebels/delete_rss_from_user/',
    method: 'POST',
    type: "POST",
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    data: '{"url_to_delete": "' + url + '"}',
    success: function(response) {
      if (response.status != 'ok') {
        throw response.message;
      } else {
        callback(response);
      }
    }
  });

}

function addSugRssToThisUser(url, callback) {


  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  $.ajax({
    async: true,
    url: 'http://localhost:8000/rebels/add_sug_rss_to_user/',
    method: 'POST',
    type: "POST",
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    data: '{"sug_url_to_add": "' + url + '"}',
    success: function(response) {
      if (response.status != 'ok') {
        throw response.message;
      } else {
        callback(response);
      }
    }
  });

}

$(function() {
  var addRssForm = $('#add_a_new_rss_to_a_user');

  addRssForm.submit(function(e) {

    e.preventDefault();

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
    if (jsonHasUrlValue(data, addRssForm.find('input[name="add_url"]').val())) { // if this link already exists do not add it and show a message to the user
      $('#AddRssFormErrorMessage').text("Rss url has already been added.");
      $('#addRssFormErrorContainer').show();
      return false;
    }

    if (isURL(addRssForm.find('input[name="add_url"]').val())) { // the provided url was valid

      $.ajax({
        async: true,
        url: 'https://api.rss2json.com/v1/api.json',
        method: 'POST',
        type: "POST",
        dataType: "json",
        data: {
          rss_url: addRssForm.find('input[name="add_url"]').val(),
          count: 1
        },
        success: function(response) {
          if (response.status != 'ok') {
            $('#AddRssFormErrorMessage').text(response.message);
            $('#addRssFormErrorContainer').show();
            throw response.message;
          } else {
            console.log(response);
            console.log(response['feed']['title']);
            console.log(response['feed']['description']);

            $.ajax({

              contentType: "application/json; charset=utf-8",
              dataType: "json",
              method: addRssForm.attr('method'),
              type: addRssForm.attr('method'),
              url: addRssForm.attr('action'),
              data: '{"add_url": "' + addRssForm.find('input[name="add_url"]').val() + '" , "rss_title": "' + response['feed']['title'] + '" ,  "rss_desc": "' + response['feed']['description'] + '"}',
              success: function(response2) {
                if (response2.status != 'ok') {
                  throw response2.message;
                } else {
                  data.push({
                    "rss_url": addRssForm.find('input[name="add_url"]').val(),
                    "rss_name": response['feed']['title']
                  });
                  $('#table').bootstrapTable("load", data);

                  $('#addRssFormErrorContainer').hide();
                  addRssForm.find('input[name="add_url"]').val("");
                }
              },
              error: function(data) {
                console.log('An error occurred.');
                console.log(data);
              },
            });
          }
        }
      });


    } else { //the provided url wasnt valid
      $('#AddRssFormErrorMessage').text("Invalid Url!!! Check the protocol the domain and the TLD (e.g. .com).");
      $('#addRssFormErrorContainer').show();
    }

  });

  var updateUsrSetForm = $('#update_user_settings');

  updateUsrSetForm.submit(function(e) {
    $('#formSuccessMessage').text("");
    $('#formSuccessContainer').hide();

    e.preventDefault();
    if (checkUserUpdateSettingsForm()) { //if the elements of the form are right then proceed to update
      var csrftoken = getCookie('csrftoken');
      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        }
      });

      $.ajax({

        contentType: "application/json; charset=utf-8",
        dataType: "json",
        method: updateUsrSetForm.attr('method'),
        type: updateUsrSetForm.attr('method'),
        url: updateUsrSetForm.attr('action'),
        data: '{"first_name": "' + updateUsrSetForm.find('input[name="first_name"]').val() +
          '" , "last_name": "' + updateUsrSetForm.find('input[name="last_name"]').val() +
          '" ,  "username": "' + updateUsrSetForm.find('input[name="username"]').val() +
          '" ,  "email": "' + updateUsrSetForm.find('input[name="email"]').val() +
          '" ,  "password": "' + updateUsrSetForm.find('input[name="password"]').val() +
          '" ,  "password2": "' + updateUsrSetForm.find('input[name="password2"]').val() +
          '"}',
        success: function(response2) {
          if (response2.status != 'ok') {
            $('#formErrorMessage').text(response2.message);
            $('#formErrorContainer').show();
            throw response2.message;
          } else {
            updateUsrSetForm.find('input[name="first_name"]').val("");
            updateUsrSetForm.find('input[name="last_name"]').val("");
            updateUsrSetForm.find('input[name="username"]').val("");
            updateUsrSetForm.find('input[name="email"]').val("");
            updateUsrSetForm.find('input[name="password"]').val("");
            updateUsrSetForm.find('input[name="password2"]').val("");
            $('#formErrorMessage').text("");
            $('#formErrorContainer').hide();

            $('#formSuccessMessage').text("Update has been completed!!");
            $('#formSuccessContainer').show();
          }


        },
        error: function(data) {
          $('#formErrorMessage').text("An error occured!");
          $('#formErrorContainer').show();
        },
      });
    }
  });

});



function nothing(kati) {

}

function deleteRss(elem) {
  var linkForDelete = $(elem).attr("link");
  deleteRssForThisUser(linkForDelete, nothing)
  var filtered = data.filter(function(item) {
    return item.rss_url !== linkForDelete;
  });
  data = filtered;

  $('#table').bootstrapTable("load", data);

  return false;
}

function addSugRss(elem) {
  var linkForDelete1 = $(elem).attr("link");


  if (!jsonHasUrlValue(data, linkForDelete1)) { //if the suggested doesnt exist in the data add it from the suggested list
    addSugRssToThisUser(linkForDelete1, nothing);
    // iterate over each element in the array
    for (var i = 0; i < data_sug.length; i++) {
      // look for the entry with a matching `code` value
      if (data_sug[i].rss_url == linkForDelete1) {
        data.push(data_sug[i]);
      }
    }
    $('#table').bootstrapTable("load", data);
    $('#table').bootstrapTable("refresh", {
      query: {}
    });
  }

  var filtered1 = data_sug.filter(function(item) {
    return item.rss_url !== linkForDelete1;
  });
  data_sug = filtered1;
  $('#table1').bootstrapTable("load", data_sug);

  $('#table1').bootstrapTable("refresh", {
    query: {}
  });
  return false;
}



function urlFormatter(value) {
  var str = value.replace("https://", "").replace("http://", " ").replace("www.", "");
  if (str.length > 30) {
    str = str.substring(0, 30) + "...";
  }

  return '<table > <tr> <td width="300"> <a  target="_blank"  href="' + value + '">' + str + '</a> </td>' + ' <td> <a onclick="deleteRss(this);" link="' + value + '" class="btn btn-danger float-right"><em class="fa fa-trash"></em></a>  </td> </tr> </table>';
}


function urlFormatterSuggestedRss(value) {
  var str = value.replace("https://", "").replace("http://", " ").replace("www.", "");
  if (str.length > 30) {
    str = str.substring(0, 30) + "...";
  }

  return '<table > <tr> <td width="300"> <a target="_blank" href="' + value + '">' + str + '</a> </td>' + ' <td> <a onclick="addSugRss(this);" link="' + value + '" class="btn btn-success float-right"><span class="glyphicon glyphicon-plus"></span></a>  </td> </tr> </table>';
}

function nameFormatter(value) {
  return value;
}
