Vue.component('txtinput',
	{
		template:
		`<div class = 'input-txt-div'>
				<div class = "input-legend" style = "padding-bottom:5px;"> 
				<img class = "rounded float-left" v-bind:src = "flag" style="width:30px;height:15px;margin-top:4px;"/>
				<span style="padding-left:10px;">{{ lng}}</span>
				</div>
				<textarea class = "input"> </textarea>
			</div>`
		,
		props: ['lng', 'flag'],
		data: function (){
			return { 
			flag: this.flag,
			lng: this.lng,
			}
		}

	}
);

var app = new Vue ({el: "#translater"});
