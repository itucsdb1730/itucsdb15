/* Elif Ozer */


function AddMusician()
{
	var desc = document.getElementById("musicianadd_musicianDesc");

	$.getJSON('/addmusician',
	{
		musicianadd_musicianName: $('input[name="musicianadd_musicianName"]').val(),
		musicianadd_musicianGenre: $('input[name="musicianadd_musicianGenre"]').val(),
		musicianadd_musicianEstYear: $('input[name="musicianadd_musicianEstYear"]').val(),
		musicianadd_musicianImgUrl: $('input[name="musicianadd_musicianImgUrl"]').val(),
		musicianadd_musicianDesc: desc.value
	},
	function(data)
	{
		if(data == "")
			location.reload();
		else
		{
			CustomAlert(data);
		}
	});

	return false;
}


function SearchMusician()
{
	window.location = "/musicians?searchBy=" + $('input[name="searchBy"]').val();

	return false;
}


function UpdateMusicianModal(musicianId, name, genre, establishYear, imgUrl, description)
{
	$("#modalMusicianId").text(musicianId);
	document.getElementById("musicianupdate_musicianName").value = name;
	document.getElementById("musicianupdate_musicianGenre").value = genre;
	document.getElementById("musicianupdate_musicianEstYear").value = establishYear;
	document.getElementById("musicianupdate_musicianImgUrl").value = imgUrl;
	$("#musicianupdate_musicianDesc").text(description);
}


function UpdateMusician()
{
	$.getJSON('/updatemusician',
	{
	    musicianId: $("#modalMusicianId").text(),
	    name: document.getElementById("musicianupdate_musicianName").value,
	    genre: document.getElementById("musicianupdate_musicianGenre").value,
	    establishYear: document.getElementById("musicianupdate_musicianEstYear").value,
	    imgUrl: document.getElementById("musicianupdate_musicianImgUrl").value,
	    description: $("#musicianupdate_musicianDesc").val()
	},
	function(data)
	{
		if(data == "")
		{
			location.reload();
		}
		else
		{
			CustomUpdateAlert(data);
		}
	});

	return false;
}


function CustomUpdateAlert(message)
{
	$('#updateAlertHolder').html('<div class="alert alert-success alert-dismissible" role="alert" style="width: 500px; margin: 10px 0 40px 0; background: #90a681;">' +
						   		'<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
									'<span aria-hidden="true">&times;</span>' +
								'</button>' +
								'<p style="color: #fff">' + message + '</p>' +
							'</div>');
}


function DeleteMusicianModal(musicianId)
{
	$("#modalMusicianDeleteId").text(musicianId);
}


function DeleteMusician()
{
	$.getJSON('/deletemusician',
	{
		musicianId: $("#modalMusicianDeleteId").text()
	},
	function(data)
	{
		if(data == true)
			location.reload();
		else
			CustomAlert("An error occured while deleting the musician");
	});

	return false;
}