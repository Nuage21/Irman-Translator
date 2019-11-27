Vue.component('txtinput',
    {
        template:
            `<div class = 'input-txt-div'>
				<div class = "input-legend" style = "padding-bottom:5px;"> 
				<img class = "rounded float-left" v-bind:src = "flag" style="width:30px;height:15px;margin-top:4px;"/>
				<span style="padding-left:10px;">{{ lng }}</span>
				</div>
				<textarea style="padding:10px;" class = "input" spellcheck="false" v-bind:id="lngid" v-bind:disabled="isdisabled"> </textarea>
			    <div class="rate" v-if="isdisabled">
			        <div class="ratephrase">
			        <span> Rate this translation </span>
			        </div>
                        <input type="radio" id="star5" name="rate" value="5"/>
                        <label for="star5" title="text">5 stars</label>
                        <input type="radio" id="star4" name="rate" value="4"/>
                        <label for="star4" title="text">4 stars</label>
                        <input type="radio" id="star3" name="rate" value="3"/>
                        <label for="star3" title="text">3 stars</label>
                        <input type="radio" id="star2" name="rate" value="2"/>
                        <label for="star2" title="text">2 stars</label>
                        <input type="radio" id="star1" name="rate" value="1"/>
                        <label for="star1" title="text">1 star</label>
                    </div>
			    <div class="btn-group-sm areabtnholder" role="group" style="float:right" aria-label="Basic example">
                    <!-- star rater -->
                    <button type="button" class="btn btn-dark">
                    <img src="img/icons/copy.png" class="down-app-icon">
                    Copy
                    </button>
                    <button type="button" class="btn btn-dark" v-if="!isdisabled">
                    <img src="img/icons/paste.png" class="down-app-icon">
                    Paste
                    </button>
                    <button type="button" class="btn btn-dark" v-if="!isdisabled" v-on:click="this.emptyAreas()">
                    <img src="img/icons/empty.png" class="down-app-icon">
                    Empty
                    </button>
                    <button type="button" class="btn btn-dark" v-if="lng==='Tamaziɣt'">
                    <img src="img/icons/correct.png" class="down-app-icon">
                    Correct
                    </button>
                </div>
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
                appendAlpha(c) {
                    let inner = $("#from-lng").val();
                    $("#from-lng").val(inner + c);
                }
            }
    }
);

var alphasApp = new Vue({
    el: "#MainApp",
    data: {
        tifinaghAlphas: "ⴰⴱⴳⴷⴹⴻⴼⴽⵀⵃⵄⵅⵇⵉⵊⵍⵎⵏⵓⵔⵕⵖⵙⵚⵛⵜⵟⵡⵢⵣⵥⵯⵞⴶ",
        berberAlphas: "abgdḌefkhḤɛxqijlmnurṚɣsṢctṬwyzẒwčǧ",
        fromLng: "Tamaziɣt",
        toLng: "English",
        fromFlag: 'img/berber-flag.png',
        toFlag: 'img/uk-flag.png',
    }
    ,
    methods:
        {
            swapLngs() {
                let tmp = this.fromLng, tmpf = this.fromFlag;
                this.fromLng = this.toLng;
                this.fromFlag = this.toFlag;
                this.toLng = tmp;
                this.toFlag = tmpf;
            }
        }
});

function emptyAreas(){
    $(".input").val('');
}
