$(window).on("load", function() {

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
    method:"POST",
    type: "POST",
    url: '/rebels/get_first_link_to_crawl/',
    data: '{"getLink": true }',
    success: function(response2) {
      if (response2.status != 'ok') {
        throw response2.message;
      } else {
          getRssFeedFromUrl(response2.link, connectTheTwoCallbackFunctionsForRetrievingRSS1);
      }
    },
    error: function(data) {
      console.log('An error occurred.');
      console.log(data);
    },
  });
});


function getRssFeedFromUrl(url, callback) {
  $.ajax({
    async: true,
    url: 'https://api.rss2json.com/v1/api.json',
    method: 'POST',
    type: "POST",
    dataType: "json",
    data: {
      rss_url: url,
      count: 10
    },
    success: function(responseFromRssFetch) {
      if (responseFromRssFetch.status != 'ok') {
        throw responseFromRssFetch.message;
      }
      console.log(responseFromRssFetch);
      callback( {   response: responseFromRssFetch , rss_url : url});
    }
  });
}

function connectTheTwoCallbackFunctionsForRetrievingRSS1(rssJson) {
  pushDataToServerAndGetNewLink(rssJson, connectTheTwoCallbackFunctionsForRetrievingRSS2);
}

function connectTheTwoCallbackFunctionsForRetrievingRSS2(url) {
  getRssFeedFromUrl(url.link, connectTheTwoCallbackFunctionsForRetrievingRSS1);
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

function pushDataToServerAndGetNewLink(responseFromRssFetch, callback) {
  console.log('====== ' + responseFromRssFetch.response.feed.title + ' ======');
  for (var i in responseFromRssFetch.response.items) {
    var item = responseFromRssFetch.response.items[i];
    console.log(item.title);
    //	console.log(item.description);
  }
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
    url: '/rebels/crawl_rss_feed/',
    method: 'POST',
    type: "POST",
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    data:   JSON.stringify( responseFromRssFetch ) ,
    success: function(response) {
      if (response.status != 'ok') {
        throw response.message;
      }
      callback(response);
    }
  });



}
