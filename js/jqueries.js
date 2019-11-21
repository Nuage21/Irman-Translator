$(document).ready(function(){
	var quoteIsDown = false;
	var berberAlphas = "ⴰⴱⴳⴷⴹⴻⴼⴽⵀⵃⵄⵅⵇⵉⵊⵍⵎⵏⵓⵔⵕⵖⵙⵚⵛⵜⵟⵡⵢⵣⵥⵯⵞⴶ".split('');
	var latinBerberAlphas = "abgdḌefkhḤɛxqijlmnurṚɣsṢctṬwyzẒwčǧ".split('');
	var alphasLng = berberAlphas.length;
	var textareasWidth = (($(window).width() - $(".quote").width())/2) - 100;
	$(".input").css({"width": textareasWidth  + "px"});
	for(var i =0; i<alphasLng;i++)
	{
		var coupleHolder = "<div class = \"couple-alphas-holder\"><div class=\"alpha-box\"><button class = \"berber-alpha\">";
		coupleHolder += latinBerberAlphas[i];
		coupleHolder += "</button></div><div class=\"alpha-box\"><button class = \"berber-alpha\">";
		coupleHolder += berberAlphas[i];
		coupleHolder += "</button></div></div>";
		$("#alphas-holder").append(coupleHolder);
	}
	$("#quote-slider").click(() => {
		var quoteSlide = quoteIsDown?'-=23%':'+=23%';
		var quoteBorder = quoteIsDown?'-=1px':'+=1px';
		$(".quote").animate({marginTop: quoteSlide});
		$(".quote-core").animate({borderLeftWidth: quoteBorder});
		quoteIsDown = !quoteIsDown; 
	});

	$("#nav-container").css({"width": $(window).width()/1.32 + "px"});
	$("#social-topbar").css({"margin-left": $(window).width()/10 + "px"});
});