$(document).ready(function(){
	var quoteIsDown = false;
	var berberAlphas = "ⴰⴱⴳⴷⴹⴻⴼⴽⵀⵃⵄⵅⵇⵉⵊⵍⵎⵏⵓⵔⵕⵖⵙⵚⵛⵜⵟⵡⵢⵣⵥⵯ".split('');
	var latinBerberAlphas = "abgdḌefkhḤɛxqijlmnurṚɣsṢctṬwyzẒw".split('');
	var alphasLng = berberAlphas.length;
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
		var quoteSlide = quoteIsDown?'-=17%':'+=17%';
		var quoteBorder = quoteIsDown?'-=1px':'+=1px';
		$(".quote").animate({marginTop: quoteSlide});
		$(".quote-core").animate({borderLeftWidth: quoteBorder});
		quoteIsDown = !quoteIsDown; 
	});
});