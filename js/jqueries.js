$(document).ready(function(){
	var quoteSlideFnc = () => {
		var quoteSlide = quoteIsDown?'-=23%':'+=23%';
		var quoteBorder = quoteIsDown?'-=1px':'+=1px';
		$(".quote").animate({marginTop: quoteSlide});
		$(".quote-core").animate({borderLeftWidth: quoteBorder});
		quoteIsDown = !quoteIsDown; 
	};
	quoteSlideFnc();
	var quoteIsDown = true;
	var textareasWidth = (($(window).width() - $(".quote").width())/2) - 100;
	$(".input").css({"width": textareasWidth  + "px"});
	
	$("#quote-slider").click(() => {
		quoteSlideFnc();
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
