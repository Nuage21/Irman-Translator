
Vue.component('txtinput',
	{
		template:
		`<div class = 'input-txt-div'>
				<div class = "input-legend" style = "padding-bottom:5px;"> 
				<img class = "rounded float-left" v-bind:src = "flag" style="width:30px;height:15px;margin-top:4px;"/>
				<span style="padding-left:10px;">{{ lng }}</span>
				</div>
				<textarea style="padding:10px;" class = "input" spellcheck="false" v-bind:id="lngid" v-bind:disabled="isdisabled"> </textarea>
			</div>`
		,
		props: ['lng', 'flag', 'lngid', 'isdisabled'],

	}
);

Vue.component('alpha',
	{
		template:
		`<div class="couple-alphas-holder">
			<div class="alpha-box, latinbox" >
				<button class="berber-alpha latinalpha" v-on:click = "appendAlpha(berberalpha)">
				{{ berberalpha }}
			</button>
			</div>
			<div class="alpha-box, tifibox">
				<button class = "berber-alpha tifialpha" v-on:click = "appendAlpha(tifinaghalpha)">
				{{ tifinaghalpha }}
				</button>
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
				let inner = $("#from-lng").val();
				$("#from-lng").val(inner + c);
			}
		}
	}
);

var alphasApp = new Vue ({
	el: "#MainApp",
	data: {
		tifinaghAlphas: "ⴰⴱⴳⴷⴹⴻⴼⴽⵀⵃⵄⵅⵇⵉⵊⵍⵎⵏⵓⵔⵕⵖⵙⵚⵛⵜⵟⵡⵢⵣⵥⵯⵞⴶ",
		berberAlphas: "abgdḌefkhḤɛxqijlmnurṚɣsṢctṬwyzẒwčǧ",
		fromLng: "Tamaziɣ",
		toLng: "English",
		fromFlag: 'img/berber-flag.png',
		toFlag: 'img/uk-flag.png',
	}
	,
	methods:
	{
		swapLngs()
		{
			let tmp = this.fromLng, tmpf = this.fromFlag;
			this.fromLng = this.toLng;
			this.fromFlag = this.toFlag;
			this.toLng = tmp;
			this.toFlag = tmpf;
		}
		,
		emptyAreas()
		{
			$(".input").val('');
		}
	}
});


