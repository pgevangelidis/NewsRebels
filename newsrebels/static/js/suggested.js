
function loadMoreArticles(elem) {
  $("#load_more_sug_art").hide();
  $("#loading_sug_art").show();

  var loaded_articles = {
    articles: []
  };

  var divsContainingUrls = document.getElementsByClassName("hiddenFieldWithTheArticlesURL");
  for (var i = 0; i < divsContainingUrls.length; i++) {
    //console.log("kati" + i + " ---> " + divsContainingUrls[i].textContent);
    loaded_articles.articles.push({
      "url":  divsContainingUrls[i].textContent
    });
  }


//  console.log(JSON.stringify(loaded_articles));


  $.ajax({
    async: true,
    url: '/rebels/suggested_load_more_articles/',
    method: 'POST',
    type: "POST",
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    data: JSON.stringify(loaded_articles),
    success: function(response) {
      if (response.status != 'ok') {
        $("#load_more_sug_art").hide();
        $("#loading_sug_art").hide();
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
        $('#article_content').append(html);

        $("#load_more_sug_art").show();
        $("#load_more_sug_art").blur()
        $("#loading_sug_art").hide();
      }
    }
  });

  return false;
}
