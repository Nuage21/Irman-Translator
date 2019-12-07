$(document).ready(function () {

    if (navigator.appVersion.indexOf("Edge") != -1) {
        $('body').css({zoom: "85%"});
    }
    adjustElements();
    $(window).on('resize', adjustElements);

    $('#tifibtn').click(() => {
        $('.latinbox').fadeOut(300, () => $('.tifibox').show());

    });
    $('#latinbtn').click(() => {
        $('.tifibox').fadeOut(300, () => $('.latinbox').show());
    });

    var toggleMode = (isNowEntered) => {
        $('.side-app-btn').toggleClass('btn-dark');
        $('#MainApp').toggleClass('dark');
        $('#App').toggleClass('dark');
        $('#AdsApp').toggleClass('dark');
        $('#side-app').toggleClass('dark');
        $('button.berber-alpha').toggleClass('dark');
        $('textarea.input').toggleClass('dark');
        $('.side-app-btn').toggleClass('dark');
        $('.input-legend').toggleClass('dark');
        $('.down-input').toggleClass('dark');
        $('#Translater').toggleClass('dark');
        $('.areabtnholder > button').toggleClass('btn-dark');
        // toggle local storage mode only if not first time page chargement
        if (!isNowEntered) {
            nowMode = localStorage.getItem('irman_tapp')
            localStorage.setItem('irman_tapp', (nowMode == 'dark') ? 'light' : 'dark')
        }
    }

    let chargedMode = localStorage.getItem('irman_tapp');
    
    if (chargedMode == 'dark') {
        $('#dark-check').prop('checked', true);
        toggleMode(true);
    }

    $('#modeSwitcher').click(() => {
        toggleMode();
    });

    // Translation ajax here

    $('#from-lng').on('keyup', (key) => {
        var msg = $('#from-lng').val();
        console.log(msg);

        if (alphasApp.$data.fromLng == eng) {
            $.ajax({
                url: '/translator/ajax/translate/',
                data: {
                    'msg': msg
                },
                dataType: 'json',
                success: (data) => {
                    $('#to-lng').val(data.tmsg);
                }
            });
        }
    });

});

var isAdsAppDown = false;

function adjustElements() {

    let winWidth = $(window).width();
    if (winWidth <= 1100) {
        $('#AdsAppContainer').css({'width': '98.8%'});
        $('#AdsAppContainer').css({'height': '300px'});
        isAdsAppDown = true;
        $('#AppContainer').css({'width': '95%'});
    }
    else {
        $('#AdsAppContainer').css({'width': '20.5%'});
        $('#AppContainer').css({'width': '75%'});
        isAdsAppDown = false;
    }
    if (winWidth <= 890) {
        $('.down-btn-txt').hide();
    }
    else $('.down-btn-txt').show();

    let hideLngSelTxt = () => {
        $('.lng-sel-txt').hide();
        $('.switch-phrase').hide();
        $('.lng-sel-holder').css({'margin-right': '2px'});
    }
    let showLngSelTxt = () => {
        $('.lng-sel-txt').show();
        $('.switch-phrase').show();
        $('.switch-phrase').css({'font-size': '16px'});
        $('.lng-sel-holder').css({'margin-right': '15px'});
    }

    // ALERT: this is a shity function that does the BAD job HAHA !

    if (winWidth < 500) {
        $('.clear').show(); //  textareas superposed
        $('.unmarginit').css({'margin-left': '-30px'});
        hideLngSelTxt();
        $('.input-txt-div').css({'width': '100%'});
        if (winWidth < 325) {
            $('#side-app').css({'width': '18%'});
            $('#AppContainer').css({'width': '82%'});
            $('.lng-sel-flag').css({'width': '18px', 'height': '12px'});
        }
        else {
            $('.lng-sel-flag').css({'width': '19px', 'height': '15px'});
            if (winWidth < 350) {
                $('#side-app').css({'width': '15.5%'});
                $('#AppContainer').css({'width': '84.5%'});
            }
            else if (winWidth < 390) {
                $('#side-app').css({'width': '14%'});
                $('#AppContainer').css({'width': '86%'});
            }
            else {
                $('#side-app').css({'width': '12.5%'});
                $('#AppContainer').css({'width': '86.5%'});
                $('.clear').show();
            }
        }
    }
    else {
        $('.unmarginit').css({'margin-left': '0px'});
        $('.clear').hide();
        $('.input-txt-div').css({'width': '50%'});
        if (winWidth < 600) {
            hideLngSelTxt();
            $('#side-app').css({'width': '12%'});
            $('#AppContainer').css({'width': '87%'});
        }
        else {
            showLngSelTxt();
            if (winWidth <= 800) {
                $('.lng-sel-flag').css({'width': '20px', 'height': '15px'});
                if (winWidth < 690) {
                    $('.lng-sel-txt').css({'font-size': '8px'});
                    $('#side-app').css({'width': '10%'});
                    $('#AppContainer').css({'width': '89%'});
                } else {
                    $('.lng-sel-txt').css({'font-size': '10px'});
                    $('.ratephrase').css({'font-size': '25px'});
                    $('#side-app').css({'width': '8%'});
                    $('#AppContainer').css({'width': '91%'});
                }
            }
            else {
                $('.lng-sel-txt').css({'font-size': '14px'});
                $('.lng-sel-flag').css({'width': '25px', 'height': '15px'});
                if (winWidth <= 1100) {
                    $('.lng-sel-txt').css({'font-size': '12px'});
                    $('#side-app').css({'width': '6%'});
                    $('#AppContainer').css({'width': '93%'});
                }
                else if (winWidth > 1000) {
                    $('#side-app').css({'width': '4%'});
                } else {
                    console.log('Window Width: ' + winWidth + 'class used: col-lg');
                }
            }
        }
    }

    let topBarh = $('.topbar').height();
    $('#content-top-wrapper').css({'height': topBarh + 5 + 'px'});

    if (!isAdsAppDown)
        $('#AdsAppContainer').css({'height': topBarh + 'px'});

    let appH = $('#App').height();
    if (!isAdsAppDown) $('#AdsAppContainer').css({'height': appH + 17 + 'px'});
    $('#side-app').css({'height': appH + 17 + 'px'});
}