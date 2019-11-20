	$(document).ready(function(){
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
	});