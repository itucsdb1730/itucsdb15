function AddNews()
{
	$.getJSON('/addnews',
	{
		addnews_title: document.getElementById("addnews_title").value,
		addnews_musician: document.getElementById("addnews_musician").value,
		addnews_imgUrl: document.getElementById("addnews_imgUrl").value,
		addnews_content: $("#addnews_content").val()
	},
	function(data)
	{
		if(data == "")
		{
			location.reload();
		}
		else
		{
			CustomNewsAddAlert(data);
		}
	});

	return false;
}


function SearchNews()
{
	window.location = "/news?searchBy=" + $('input[name="searchBy"]').val();

	return false;
}


function UpdateNewsModal(newsId, title, musicianName, imgUrl, content)
{
	$("#modalNewsId").text(newsId);
	document.getElementById("newsupdate_title").value = title;
	document.getElementById("newsupdate_musicianName").value = musicianName;
	document.getElementById("newsupdate_imgUrl").value = imgUrl;
	$("#newsupdate_content").text(content);
}


function UpdateNews()
{
	$.getJSON('/updatenews',
	{
	    newsId: $("#modalNewsId").text(),
	    title: document.getElementById("newsupdate_title").value,
	    musicianName: document.getElementById("newsupdate_musicianName").value,
	    imgUrl: document.getElementById("newsupdate_imgUrl").value,
	    content: $("#newsupdate_content").val()
	},
	function(data)
	{
		if(data == "")
		{
			location.reload();
		}
		else
		{
			CustomNewsUpdateAlert(data);
		}
	});

	return false;
}


function DeleteNewsModal(newsId)
{
	$("#modalNewsDeleteId").text(newsId);
}


function DeleteNews()
{
	$.getJSON('/deletenews',
	{
		newsId: $("#modalNewsDeleteId").text()
	},
	function(data)
	{
		if(data == true)
			location.reload();
		else
			CustomAlert("An error occured while deleting news");
	});

	return false;
}


function CustomNewsAddAlert(message)
{
	$('#newsAddAlertHolder').html('<div class="alert alert-success alert-dismissible" role="alert" style="width: 500px; margin: 10px 0 40px 0; background: #90a681;">' +
						   		'<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
									'<span aria-hidden="true">&times;</span>' +
								'</button>' +
								'<p style="color: #fff">' + message + '</p>' +
							'</div>');
}


function CustomNewsUpdateAlert(message)
{
	$('#updateNewsAlertHolder').html('<div class="alert alert-success alert-dismissible" role="alert" style="width: 500px; margin: 10px 0 40px 0; background: #90a681;">' +
						   		'<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
									'<span aria-hidden="true">&times;</span>' +
								'</button>' +
								'<p style="color: #fff">' + message + '</p>' +
							'</div>');
}