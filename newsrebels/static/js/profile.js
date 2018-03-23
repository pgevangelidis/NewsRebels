function deleteRss(elem) {
  var linkForDelete = $(elem).attr("link");

  var filtered = data.filter(function(item) {
     return item.rss_url !== linkForDelete;
  });
  data = filtered;

$('#table').bootstrapTable("load", data);
return false;
}

function addSugRss(elem) {
  console.log(data_sug);
  var linkForDelete1 = $(elem).attr("link");

  // iterate over each element in the array
  for (var i = 0; i < data_sug.length; i++){
    // look for the entry with a matching `code` value
    if (data_sug[i].rss_url == linkForDelete1){
       data.push(data_sug[i]);
    }
  }

  var filtered1 = data_sug.filter(function(item) {
     return item.rss_url !== linkForDelete1;
  });
  data_sug = filtered1;
console.log(data_sug);
$('#table1').bootstrapTable("load", data_sug);
$('#table').bootstrapTable("load", data);

$('#table1').bootstrapTable("refresh", {
    query: {pageSize: 5}
});
$('#table').bootstrapTable("refresh", {
    query: {pageSize: 5}
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

$(function() {
  $('#table').bootstrapTable({
    data: data
  });
  $('#table1').bootstrapTable({
    data: data_sug
  });
});
