$(document).ready(function(){
	var quoteIsDown = false;
	var berberAlphas = "ⴰⴱⴳⴷⴹⴻⴼⴽⵀⵃⵄⵅⵇⵉⵊⵍⵎⵏⵓⵔⵕⵖⵙⵚⵛⵜⵟⵡⵢⵣⵥⵯ".split('');
	var latinBerberAlphas = "abgdḌefkhḤɛxqijlmnurṚɣsṢctṬwyzẒw".split('');
	var alphasLng = berberAlphas.length;
	var textareasWidth = (($(window).width() - $(".quote").width())/2) - 100;
	$("textarea").css({"width": textareasWidth  + "px"});
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
});