Vue.component('txtinput',
    {
        // language=HTML
        template:
                `
            <div class='input-txt-div'>
                <div class="input-legend" style="padding-bottom:5px;">
                    <img class="rounded float-left" v-bind:src="flag" style="width:30px;height:15px;margin-top:4px;"/>
                    <span style="padding-left:10px;">{{ lng }}</span>
                </div>
                <textarea style="padding:10px;" class="input" spellcheck="false" v-bind:id="lngid"
                          v-bind:readonly="isdisabled">
				
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
                    <button type="button" class="btn btn-dark" v-if="(lng==='Tamaziɣt') && !isdisabled"
                            @click="this.correct()">
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
                        case 'ṣ':
                            return 'Ṣ';
                            break;
                        case 'ɛ':
                            return 'Ԑ';
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
        tifinaghAlphas: "ⴰⴱⵛⵞⴷⴹⴻⴼⴳⴶⵀⵃⵉⵊⴽⵍⵎⵏⵄⵇⵔⵕⵙⵚⵜⵟⵓⵖⵡⵅⵢⵣⵥ",
        berberAlphas: "abcčdḍefgǧhḥijklmnɛqrṛsṣtṭuɣwxyzẓ",
        fromLng: "Tamaziɣt",
        toLng: "English",
        fromFlag: 'img/flags/berber.png',
        toFlag: 'img/flags/uk.png',
    }
    ,
    methods:
        {
            swapLngs: function () {
                let tmp = this.fromLng, tmpf = this.fromFlag;
                this.fromLng = this.toLng;
                this.fromFlag = this.toFlag;
                this.toLng = tmp;
                this.toFlag = tmpf;
            }
            ,
            toLatin: function () {
                // converting from Tfng to Latin chars
                let berberInputID = (this.fromLng === 'Tamaziɣt') ? 'from-lng' : 'to-lng';
                let txt = $('#' + berberInputID).val();
                // conversion algorithm
                let converted = '';
                for (let i = 0; i < txt.length; i++) {
                    let c = txt[i];
                    let cPos = this.tifinaghAlphas.indexOf(c);
                    if (cPos >= 0)
                        c = this.berberAlphas[cPos];
                    converted += c;
                }
                $('#' + berberInputID).val(converted);
            }
            ,
            toTfng: function () {
                // converting from Latin chars to Tfng
                let berberInputID = (this.fromLng === 'Tamaziɣt') ? 'from-lng' : 'to-lng';
                let txt = $('#' + berberInputID).val();
                // conversion algorithm
                let converted = '';
                for (let i = 0; i < txt.length; i++) {
                    let c = txt[i];
                    let cPos = this.berberAlphas.indexOf(c.toLowerCase());
                    if (cPos >= 0)
                        c = this.tifinaghAlphas[cPos];
                    converted += c;
                }
                $('#' + berberInputID).val(converted);
            }
        }
});

function emptyAreas() {
    $(".input").val('');
}

function correct() {
    // correct common written Tamazight;
    if (alphasApp.fromLng != 'Tamaziɣt') return;
    let txt = $('#from-lng').val();
    // conversion algorithm
    let converted = '';
    let len = txt.length;
    for (let i = 0; i < len; i++) {
        let c = txt[i];
        let c0 = c;
        switch (c.toLowerCase()) {
            case 'd':
                if (i < len - 1)
                    if (txt[i + 1].toLowerCase() == 'j') {
                        c0 = 'ǧ';
                        i++;
                    }
                break;
            case 'k':
                if (i < len - 1)
                    if (txt[i + 1].toLowerCase() == 'h') {
                        c0 = 'x';
                        i++;
                    }
                break;
            case 'h':
                if (i < len - 1)
                    if (txt[i + 1].toLowerCase() == 'h') {
                        c0 = 'ḥ';
                        i++;
                    }
                break;
            case 'g':
                if (i < len - 1)
                    if (txt[i + 1].toLowerCase() == 'h') {
                        c0 = 'ɣ';
                        i++;
                    }
                break;
            case 'o':
                if (i < len - 1)
                    if (txt[i + 1].toLowerCase() == 'u') {
                        c0 = 'u';
                        i++;
                    }
                break;
            case 'c':
                if (i < len - 1)
                    if (txt[i + 1].toLowerCase() == 'h') {
                        c0 = 'c';
                        i++;
                    }
                break;
            case 't':
                if (i < len - 1) {
                    if (txt[i + 1].toLowerCase() == 's') {
                        c0 = 'tt';
                        i++;
                    }
                    else if (txt[i + 1].toLowerCase() == 'h') {
                        c0 = 't';
                        i++;
                    }
                    else if (txt[i + 1].toLowerCase() == 'c' && i < len - 2)
                        if (txt[i + 2].toLowerCase() == 'h') {
                            c0 = 'č';
                            i+=2;
                        }
                }
                break;
            case
            '3'
            :
                c0 = 'ɛ';
                break;
        }
        converted += c0;
    }
    console.log(converted);
    $('#from-lng').val(converted);
}

function copyTranslation() {
    $('#to-lng').select();
    document.execCommand('copy');
}