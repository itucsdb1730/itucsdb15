/* Elif Ozer */


function UpdateUser()
{
	$.getJSON('/updateuser',
	{
		usersettings_firstName: $('input[name="usersettings_firstName"]').val(),
		usersettings_lastName: $('input[name="usersettings_lastName"]').val(),
		usersettings_username: $('input[name="usersettings_username"]').val(),
		usersettings_email: $('input[name="usersettings_email"]').val(),
		usersettings_password: $('input[name="usersettings_password"]').val()
	},
	function(data)
	{
		if(data == "")
			alert("Successfully updated");
		else
		{
			alert(data);
			location.reload();
		}
	});

	return false;
}


function DeleteUser()
{
	if(!confirm("Are you sure to delete your account?"))
		return;

	$.getJSON('/deleteuser',
	{
	},
	function(data)
	{
		if(data == true)
		{
			alert("Permanently deleted your account");
			window.location = "/";
		}
		else
			alert("An error occured while deleting");
	});

	return false;
}