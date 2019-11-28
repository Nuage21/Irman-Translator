Vue.component('txtinput',
    {
        template:
            `<div class = 'input-txt-div'>
				<div class = "input-legend" style = "padding-bottom:5px;"> 
				<img class = "rounded float-left" v-bind:src = "flag" style="width:30px;height:15px;margin-top:4px;"/>
				<span style="padding-left:10px;">{{ lng }}</span>
				</div>
				<textarea style="padding:10px;" class = "input" spellcheck="false" v-bind:id="lngid" v-bind:readonly="isdisabled">
				
                </textarea>
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
                    <button type="button" class="btn btn-dark" @click="copytxt(lngid)">
                    <img src="img/icons/copy.png" class="down-app-icon">
                    Copy
                    </button>
                    <button type="button" class="btn btn-dark" v-if="!isdisabled" @click="pastetxt(lngid)">
                    <img src="img/icons/paste.png" class="down-app-icon">
                    Paste
                    </button>
                    <button type="button" class="btn btn-dark" v-if="!isdisabled" v-on:click="this.emptyAreas()">
                    <img src="img/icons/empty.png" class="down-app-icon">
                    Empty
                    </button>
                    <button type="button" class="btn btn-dark" v-if="lng==='Tamaziɣt' && !isdisabled">
                    <img src="img/icons/correct.png" class="down-app-icon">
                    Correct
                    </button>
                </div>
			</div>`
        ,
        props: ['lng', 'flag', 'lngid', 'isdisabled']
        ,
        methods:
            {
                copytxt(id) {
                    $('#' + id).select();
                    document.execCommand('copy');
                }
                ,
                async pastetxt(id) {
                    const txt = await navigator.clipboard.readText();
                    var cursorPos = $('#' + id).prop('selectionStart');
                    var v = $('#' + id).val();
                    var textBefore = v.substring(0, cursorPos);
                    var textAfter = v.substring(cursorPos, v.length);

                    $('#' + id).val(textBefore + txt + textAfter);
                }

            }
    }
);

Vue.component('alpha',
    {
        template:
            `<div class="couple-alphas-holder">
			<div class="alpha-box, latinbox" >
				<button class="berber-alpha latinalpha" @click.right.prevent ="appendAlpha(uppercase(berberalpha))" @click.left  = "appendAlpha(berberalpha)">
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
                ,
                uppercase(c) {
                    switch (c) {
                        case 'č':
                            return 'Č';
                            break;
                        case 'ḍ':
                            return 'Ḍ';
                            break;
                        case 'ǧ':
                            return 'Ǧ';
                            break;
                        case 'ḥ':
                            return 'Ḥ';
                            break;
                        case 'ɛ':
                            return 'Ḥ';
                            break;
                        case 'ṛ':
                            return 'Ṛ';
                            break;
                        case 'ṭ':
                            return 'Ṭ';
                            break;
                        case 'ɣ':
                            return 'Γ';
                            break;
                        case 'ẓ':
                            return 'Ẓ';
                            break;
                        default:
                            return c.toUpperCase();

                    }
                }
            }
    }
);

var alphasApp = new Vue({
    el: "#MainApp",
    data: {
        tifinaghAlphas: "ⴰⴱⵛⵞⴷⴹⴻⴼⴳⴶⵀⵃⵉⵊⴽⵍⵎⵏⵄⵇⵔⵕⵙⵚⵜⵓⵖⵡⵅⵢⵣⵥ",
        berberAlphas: "abcčdḍefgǧhḥijklmnɛqrṛsṢtṭuɣwxyzẓ",
        fromLng: "Tamaziɣt",
        toLng: "English",
        fromFlag: 'img/flags/berber.png',
        toFlag: 'img/flags/uk.png',
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
            ,
            toLatin()
            {
                // converting from Tfng to Latin chars
                let berberInputID = (this.fromLng==='Tamaziɣt')?'from-lng':'to-lng';
                let txt = $('#' +  berberInputID).val();
                // conversion algorithm
                let converted = '';
                for(let i = 0; i<txt.length; i++)
                {
                    let c = txt[i];
                    let cPos = this.tifinaghAlphas.indexOf(c)
                    let cLatin  = '0';
                    if(cPos >= 0)
                        cLatin = this.berberAlphas[cPos];
                    else cLatin = c;

                    converted += cLatin;
                }
               $('#' +  berberInputID).val(converted);
            }
            ,
            toTfng()
            {
                // converting from Latin chars to Tfng
                let berberInputID = (this.fromLng==='Tamaziɣt')?'from-lng':'to-lng';
                let txt = $('#' +  berberInputID).val();
                // conversion algorithm
                let converted = '';
                for(let i = 0; i<txt.length; i++)
                {
                    let c = txt[i];
                    let cPos = this.berberAlphas.indexOf(c.toLowerCase());
                    let cLatin  = '0';
                    if(cPos >= 0)
                        cLatin = this.tifinaghAlphas[cPos];
                    else cLatin = c;

                    converted += cLatin;
                }
               $('#' +  berberInputID).val(converted);
            }
        }
});

function emptyAreas() {
    $(".input").val('');
}

function copyTranslation() {
    $('#to-lng').select();
    document.execCommand('copy');
}
