Vue.component('txtinput',
	{
		template:
		`<div class = 'input-txt-div'>
				<div class = "input-legend" style = "padding-bottom:5px;"> 
				<img class = "rounded float-left" v-bind:src = "flag" style="width:30px;height:15px;margin-top:4px;"/>
				<span style="padding-left:10px;">{{ lng }}</span>
				</div>
	<textarea class = "input" spellcheck="false" v-bind:id="lngid"> </textarea>
			</div>`
		,
		props: ['lng', 'flag', 'lngid'],

	}
);

Vue.component('alpha',
	{
		template:
		`<div class="couple-alphas-holder">
			<div class="alpha-box, latinbox" >
				<button class="berber-alpha latinalpha" v-on:click = "appendAlpha(berberalpha)">{{ berberalpha }}</button>
			</div>
			<div class="alpha-box, tifibox">
				<button class = "berber-alpha tifialpha" v-on:click = "appendAlpha(tifinaghalpha)">{{ tifinaghalpha }}</button>
			</div>
		</div>
		`
		,
		props: ['berberalpha', 'tifinaghalpha']
		,
		methods:
		{
			appendAlpha(c)
			{
				let inner = $("#from-lng").html();
				$("#from-lng").html(inner + c);
			}
		}
	}
);

var app = new Vue ({el: "#translater"});
var alphasApp = new Vue ({
	el: "#alphas-holder",
	data: {
		tifinaghAlphas: "ⴰⴱⴳⴷⴹⴻⴼⴽⵀⵃⵄⵅⵇⵉⵊⵍⵎⵏⵓⵔⵕⵖⵙⵚⵛⵜⵟⵡⵢⵣⵥⵯⵞⴶ",
		berberAlphas: "abgdḌefkhḤɛxqijlmnurṚɣsṢctṬwyzẒwčǧ",
	}
});
