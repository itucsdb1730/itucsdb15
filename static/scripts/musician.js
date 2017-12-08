/* Elif Ozer */


function AddMusician()
{
	var img = document.getElementById("musicianadd_musicianDesc");

	$.getJSON('/addmusician',
	{
		musicianadd_musicianName: $('input[name="musicianadd_musicianName"]').val(),
		musicianadd_musicianGenre: $('input[name="musicianadd_musicianGenre"]').val(),
		musicianadd_musicianEstYear: $('input[name="musicianadd_musicianEstYear"]').val(),
		musicianadd_musicianImgUrl: $('input[name="musicianadd_musicianImgUrl"]').val(),
		musicianadd_musicianDesc: img.value
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
