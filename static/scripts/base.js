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