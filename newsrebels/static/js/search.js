function searchAquery(elem) {
  $(this).blur();
  $('#articleSearchButton').hide();
  $('#articleSearchButtonHidden').show();

  $("#articleSearchTextInput").attr('readonly', true);
  $('#loading_image_container').show();



  $('#searchQueryPlaceHolder').text($("#articleSearchTextInput").val());

  $.ajax({
    async: true,
    url: '/rebels/search_for_relevant_articles/',
    method: 'POST',
    type: "POST",
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    data: '{"query" : "' + $("#articleSearchTextInput").val() + '"}',
    success: function(response) {
      if (response.status != 'ok') {
          $('#loading_image_container').html("An error has occured!! Plz refresh the page!!");
        throw response.message;
      } else {

        //  console.log(response.json_articles);
        // grab our template code from the DOM
        var source = $("#category-template").html();

        // compile the template so we can use it
        var template = Handlebars.compile(source);

        // generate HTML from the data
        var html = template(JSON.parse(response.json_articles));

        // add the HTML to the content div
        $('#search_content').html(html);

        $("#articleSearchTextInput").attr('readonly', false);

        $('#loading_image_container').hide();
        $('#articleSearchButton').show();
        $('#articleSearchButtonHidden').hide();
      }
    }
  });

  return false;
}
