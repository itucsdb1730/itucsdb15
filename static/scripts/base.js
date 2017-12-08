/* Elif Ozer */

$(document).ready(function()
{
	$('html, body').animate({scrollTop:$('#top').position().top}, 'slow');

	$('#popUpLogin').on('dialogclose', function(e)
	{
		$('body').css('position', 'static');
		$('body').css('overflow-y', 'auto');
	});
});


$(document).click(function()
{
	$('.userIconDropdown').removeClass("open");
});


function UserIconClick(event)
{
	$('.userIconDropdown').toggleClass("open");

	if (event.stopPropagation)
	    event.stopPropagation();
}

function CustomAlert(message)
{
	$('#alertHolder').html('<div class="alert alert-success alert-dismissible" role="alert" style="width: 500px; margin: 10px 0 40px 0; background: #90a681;">' +
						   		'<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
									'<span aria-hidden="true">&times;</span>' +
								'</button>' +
								'<p style="color: #fff">' + message + '</p>' +
							'</div>');
}