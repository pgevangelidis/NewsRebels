function read_more_btn(elem, url) {
  $(elem).blur();

    $.ajax({
      async: true,
      url: '/rebels/read_more_btn/',
      method: 'POST',
      type: "POST",
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      data: '{"url": "'+url +'"}',
      success: function(response) {
        if (response.status != 'ok') {
          throw response.message;
        }
        if (url.indexOf(window.location.host.split('/')[0]) >= 0) {
          window.location = url;
        } else {
          window.open(url, '_blank');
        }
      }
    });





}
