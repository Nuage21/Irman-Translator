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
                <textarea style="padding:10px;float:left;" class="input" spellcheck="false" v-bind:id="lngid"
                          v-bind:readonly="isdisabled">
                </textarea>
                <div style="display: inline-block;float:left;width:75% !important;" v-if="isdisabled">
                    <div class="ratep-holder rate-el">
                        <span class="ratep"> {{this.$parent.$data.rateTranslationTxt}} </span>
                    </div>
                    <div class="rate rate-el">
                        <input type="radio" id="star5" name="rate" value="5"/>
                        <label for="star5" title="5 stars">5 stars</label>
                        <input type="radio" id="star4" name="rate" value="4"/>
                        <label for="star4" title="4 stars">4 stars</label>
                        <input type="radio" id="star3" name="rate" value="3"/>
                        <label for="star3" title="3 stars">3 stars</label>
                        <input type="radio" id="star2" name="rate" value="2"/>
                        <label for="star2" title="2 stars">2 stars</label>
                        <input type="radio" id="star1" name="rate" value="1"/>
                        <label for="star1" title="5 stars">1 star</label>
                    </div>
                </div>
                <div class="areabtnholder" role="group" style="padding: 0 !important;" aria-label="down-app-btns">
                    <button type="button" class="btn btn-sm shadow-none btn-light" @click="copytxt(lngid)">
                        <img src="/static/Translator/img/icons/copy.png" class="down-app-icon">
                        <span class="down-btn-txt">{{this.$parent.$data.copyBtnTxt}}</span>
                    </button>
                    <button type="button" class="btn btn-sm shadow-none btn-light" v-if="!isdisabled"
                            @click="pastetxt(lngid)">
                        <img src="/static/Translator/img/icons/paste.png" class="down-app-icon">
                        <span class="down-btn-txt">{{this.$parent.$data.pasteBtnTxt}}</span>
                    </button>
                    <button type="button" class="btn btn-sm shadow-none btn-light" v-if="!isdisabled"
                            v-on:click="this.emptyAreas()">
                        <img src="/static/Translator/img/icons/empty.png" class="down-app-icon">
                        <span class="down-btn-txt">{{this.$parent.$data.emptyBtnTxt}}</span>
                    </button>
                    <button type="button" class="btn btn-sm shadow-none btn-light"
                            v-show="(lng==='Tamaziɣt') && !isdisabled"
                            @click="this.correct()">
                        <img src="/static/Translator/img/icons/correct.png" class="down-app-icon">
                        <span class="down-btn-txt">{{this.$parent.$data.correctBtnTxt}}</span>
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
				<button class="berber-alpha latinalpha"  v-bind:disabled="this.isFromLngNotBerber()" @click.right.prevent ="appendAlpha(uppercase(berberalpha))" @click.left  = "appendAlpha(berberalpha)">
				{{ berberalpha }}
			</button>
			</div>
			<div class="alpha-box, tifibox">
				<button class = "berber-alpha tifialpha" v-bind:disabled="this.isFromLngNotBerber()" v-on:click = "appendAlpha(tifinaghalpha)">
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
                isFromLngNotBerber() {
                    return (this.$parent.$data.fromLng == 'Tamaziɣt') ? null : 1;
                }
                ,
                appendAlpha(c) {
                    var cursorPos = $("#from-lng").prop('selectionStart');
                    var v = $("#from-lng").val();
                    var textBefore = v.substring(0, cursorPos);
                    var textAfter = v.substring(cursorPos, v.length);

                    $("#from-lng").val(textBefore + c + textAfter);
                    setCursorPos(document.getElementById('from-lng'),cursorPos+1, cursorPos+1);
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
                            return 'Σ';
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
        fromLng: brbr,
        toLng: eng,
        fromFlag: '/static/Translator/img/flags/berber.png',
        toFlag: '/static/Translator/img/flags/uk.png',
        correctBtnTxt: correct_btn_txt,
        copyBtnTxt: copy_btn_txt,
        pasteBtnTxt: paste_btn_txt,
        emptyBtnTxt: empty_btn_txt,
        rateTranslationTxt: rate_translation_txt,
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
            toLatin() {
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
            toTfng() {
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
                            i += 2;
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

function setCursorPos(input, start, end) {
    if (arguments.length < 3) end = start;
    if ("selectionStart" in input) {
        setTimeout(function() {
            input.selectionStart = start;
            input.selectionEnd = end;
        }, 1);
    }
    else if (input.createTextRange) {
        var rng = input.createTextRange();
        rng.moveStart("character", start);
        rng.collapse();
        rng.moveEnd("character", end - start);
        rng.select();
    }
}