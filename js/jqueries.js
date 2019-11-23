$(document).ready(function(){
	var quoteIsVisible = false;
	var quoteToogleFade = () => {
		if(quoteIsVisible)
			$(".quote").fadeOut(700);
		else $(".quote").fadeIn(700);
		quoteIsVisible = !quoteIsVisible; 
	};
	quoteToogleFade();
	
	var textareasWidth = (($(window).width() - $(".quote").width())/2) - 100;
	$(".input").css({"width": textareasWidth  + "px"});
	
	$("#quote-slider").click(() => {
		quoteToogleFade();
	});
	$("#nav-container").css({"width": $(window).width()/1.32 + "px"});
	$("#social-topbar").css({"margin-left": $(window).width()/10 + "px"});
	
	$('#tifibtn').click( () => {
		$('.latinbox').fadeOut(500, ()=>$('.tifibox').show());

	});
	$('#latinbtn').click( () => {
		$('.tifibox').fadeOut(500, ()=> $('.latinbox').show());
	});
	$("#from-lng")
		.focus() // set initial focus
		.on('blur', function () { // on blur
		$(this).focus(); // return focus	
		});
});
