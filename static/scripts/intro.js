/* Elif Ozer */

$(document).ready(function()
{
	setTimeout(function(){$('.flyInText_ul').removeClass('firststate')}, 500);
});


function Scroll()
{
	var yPos = window.pageYOffset;

	if(yPos > 250)
		document.getElementById('underConstruction').classList.remove('firststate');
	else
		document.getElementById('underConstruction').classList.add('firststate');
}

window.addEventListener("scroll", Scroll);