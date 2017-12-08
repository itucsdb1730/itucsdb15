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
			CustomAlert("Successfully updated user settings");
		else
			CustomAlert(data);
	});

	return false;
}


function DeleteUser()
{
	$.getJSON('/deleteuser',
	{
	},
	function(data)
	{
		if(data == true)
			window.location = "/";
		else
			CustomAlert("An error occured while deleting the account");
	});

	return false;
}