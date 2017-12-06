/* Elif Ozer */

$( document ).ready(function()
{
	var choice = window.location.hash.substr(1);

	if(choice == "login")
	{
		$(".login-area").addClass("hideSide");
		$(".register-box").addClass("hideSide");

		flipLoginCard();
	}

	else
	{
		$(".register-area").addClass("hideSide");
		$(".login-box").addClass("hideSide");

		flipRegisterCard();
	}
});


$(window).on('hashchange', function(e)
{
	var choice = window.location.hash.substr(1);

	if(choice == "login")
		flipLoginCard();
	else
		flipRegisterCard();
});


function flipRegisterCard()
{
	var e="rotateY-90", o="rotateY90";

	if(!$(".login-box").hasClass("hideSide"))
		$(".login-box").addClass("hideSide");

	$(".register-area").addClass("hideSide");
	$(".register-box").addClass("transition-05s").addClass(e);

	setTimeout(function()
	{
		$(".register-box").addClass("hideSide");
		$(".register-area").addClass(o).removeClass("hideSide").addClass("transition-05s");

		setTimeout(function()
		{
			$(".register-area").removeClass(o);
			$(".register-box").removeClass(e)

			$(".login-area").addClass("transition-05s").addClass(e);

			setTimeout(function()
			{
				$(".login-area").addClass("hideSide");
				$(".login-box").addClass(o).removeClass("hideSide").addClass("transition-05s");

				setTimeout(function()
				{
					$(".login-box").removeClass(o);
					$(".login-area").removeClass(e)
				}, 50)
			}, 500)
		}, 100)
	}, 500)

	window.location.hash = "register";
}


function flipLoginCard()
{
	var e="rotateY-90", o="rotateY90";

	if(!$(".register-box").hasClass("hideSide"))
		$(".register-box").addClass("hideSide");

	$(".login-area").addClass("hideSide");
	$(".login-box").addClass("transition-05s").addClass(o);

	setTimeout(function()
	{
		$(".login-box").addClass("hideSide");
		$(".login-area").addClass(e).removeClass("hideSide").addClass("transition-05s");

		setTimeout(function()
		{
			$(".login-area").removeClass(e);
			$(".login-box").removeClass(o)

			$(".register-area").addClass("transition-05s").addClass(o);

			setTimeout(function()
			{
				$(".register-area").addClass("hideSide");
				$(".register-box").addClass(e).removeClass("hideSide").addClass("transition-05s");

				setTimeout(function()
				{
					$(".register-box").removeClass(e);
					$(".register-area").removeClass(o)
				}, 50)
			}, 500)
		}, 100)
	}, 500)

	window.location.hash = "login";
}


function LoginOperation()
{

}


function RegisterOperation()
{

}