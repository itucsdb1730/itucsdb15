/* Elif Ozer */


function AddMusician()
{
	$.getJSON('/addmusician',
	{
		musicianadd_musicianName: $('input[name="musicianadd_musicianName"]').val(),
		musicianadd_musicianGenre: $('input[name="musicianadd_musicianGenre"]').val(),
		musicianadd_musicianEstYear: $('input[name="musicianadd_musicianEstYear"]').val(),
		musicianadd_musicianImgUrl: $('input[name="musicianadd_musicianImgUrl"]').val(),
		musicianadd_musicianDesc: $('input[name="musicianadd_musicianDesc"]').val()
	},
	function(data)
	{
		if(data == "")
			alert("Successfully added new musician");
		else
		{
			alert(data);
			location.reload();
		}
	});

	return false;
}