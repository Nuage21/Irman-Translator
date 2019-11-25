$(document).ready(function () {

    if (navigator.appVersion.indexOf("Edge") != -1) {
        $('body').css({zoom: "85%"});
    }

    var quoteIsVisible = false;
    var quoteToogleFade = () => {
        if (quoteIsVisible)
            $(".quote").fadeOut(700);
        else $(".quote").fadeIn(700);
        quoteIsVisible = !quoteIsVisible;
    };
    quoteToogleFade();

    $("#quote-slider").click(() => {
        quoteToogleFade();
    });

    $('#tifibtn').click(() => {
        $('.latinbox').fadeOut(500, () => $('.tifibox').show());

    });
    $('#latinbtn').click(() => {
        $('.tifibox').fadeOut(500, () => $('.latinbox').show());
    });
    $("#from-lng")
        .focus() // set initial focus
        .on('blur', function () { // on blur
            $(this).focus(); // return focus
        });
});
