Vue.component('txtinput',
	{
		template:
		`<div class = 'input-txt-div'>
				<div class = "input-legend" style = "padding-bottom:5px;"> 
				<img class = "rounded float-left" v-bind:src = "flag" style="width:30px;height:15px;margin-top:4px;"/>
				<span style="padding-left:10px;">{{ lng }}</span>
				</div>
				<textarea class = "input" spellcheck="false"> </textarea>
			</div>`
		,
		props: ['lng', 'flag'],

	}
);

Vue.component('alpha',
	{
		template:
		`<div class="couple-alphas-holder">
			<div class="alpha-box">
				<button class="berber-alpha">{{ berberalpha }}</button>
			</div>
			<div class="alpha-box">
				<button class = "berber-alpha">{{ tifinaghalpha }}</button>
			</div>
		</div>
		`
		,
		props: ['berberalpha', 'tifinaghalpha']
		,
	}
);

var app = new Vue ({el: "#translater"});
var alphasApp = new Vue ({
	el: "#alphas-holder",
	data: {
		tifinaghAlphas: "ⴰⴱⴳⴷⴹⴻⴼⴽⵀⵃⵄⵅⵇⵉⵊⵍⵎⵏⵓⵔⵕⵖⵙⵚⵛⵜⵟⵡⵢⵣⵥⵯⵞⴶ",
		berberAlphas: "abgdḌefkhḤɛxqijlmnurṚɣsṢctṬwyzẒwčǧ",
		i: 0,
	}
});
