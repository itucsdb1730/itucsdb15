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
			CustomNewsAlert(data);
		}
	});

	return false;
}


function CustomNewsAlert(message)
{
	$('#newsAlertHolder').html('<div class="alert alert-success alert-dismissible" role="alert" style="width: 500px; margin: 10px 0 40px 0; background: #90a681;">' +
						   		'<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
									'<span aria-hidden="true">&times;</span>' +
								'</button>' +
								'<p style="color: #fff">' + message + '</p>' +
							'</div>');
}