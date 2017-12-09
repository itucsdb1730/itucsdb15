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
		CustomAlert(data);
		location.reload();
	});

	return false;
}
