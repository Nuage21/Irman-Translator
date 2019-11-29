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
        $('.latinbox').fadeOut(300, () => $('.tifibox').show());

    });
    $('#latinbtn').click(() => {
        $('.tifibox').fadeOut(300, () => $('.latinbox').show());
    });
    $('#modeSwitcher').click(() => {
        $('.side-app-btn').toggleClass('btn-dark');
        $('#MainApp').toggleClass('dark');
        $('#App').toggleClass('dark');
        $('#AdsApp').toggleClass('dark');
        $('#side-app').toggleClass('dark');
        $('button.berber-alpha').toggleClass('dark');
        $('textarea.input').toggleClass('dark');
        $('.side-app-btn').toggleClass('dark');
        $('.input-legend').toggleClass('dark');
        $('.areabtnholder > button').toggleClass('btn-dark');
    });
        $("#from-lng")
            .focus() // set initial focus
            .on('blur', function () { // on blur
                $(this).focus(); // return focus
            });
    });
