function getUrlParam(name) {
  //https://www.sitepoint.com/community/t/how-to-check-if-url-parameter-is-empty-or-not/117524/2
  var results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(window.location.href);
  return (results && results[1]) || undefined;
}

$(function() {
  var error_msg_div_cont = document.getElementById("loginErrorMessageDisplay");
  if (error_msg_div_cont != null) {
    var error_msg = error_msg_div_cont.textContent
    if (error_msg.indexOf('Invalid') >= 0 || error_msg.indexOf('disabled') >= 0) {
      $("#login-dp").show();
    } else {
      $("#login-dp").hide();
    }
  }
});

function moveToElement(kati) {
  console.log($(kati).offset().top);
  $('html, body').animate({
    scrollTop: $(kati).offset().top - $('#navBarID').height() + 'px'
  }, 'fast');
  return false;
}

//the following function hides and shows the login form when the login button is pressed
$(document).mouseup(function(e) {
  var container = $("#loginBtn");
  // if the target of the click isn't the container nor a descendant of the container
  if (!container.is(e.target) && container.has(e.target).length === 0) {
    $("#login-dp").hide();
  } else {
    var container1 = $("#login-dp");
    // if the target of the click isn't the container nor a descendant of the container
    if (!container1.is(e.target) && container1.has(e.target).length === 0) {
      if ($("#login-dp").is(':visible')) {
        $("#login-dp").hide()
      } else {
        $("#login-dp").show();
      }
    }
  }
});
