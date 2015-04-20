/**
 * Created by Dmitry on 03.03.2015.
 * @return {boolean}
 */
function ValidUrl(str) {
        var pattern = new RegExp('^(https?:\\/\\/)?' + // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
        '(\\#[-a-z\\d_]*)?$', 'i'); // fragment locator
        return pattern.test(str);
}
$(document).ready(function () {
    var join_us = $("#join_us_input");
    join_us.keyup(function() {
        if (join_us.val() !== "http://" && join_us.val() !== "Введите адрес вашего сайта" && join_us.val() !== "" && ValidUrl(join_us.val())) {
            $("#join_us_btn").css('display', 'block');
        }else{
            $("#join_us_btn").css('display', 'none');
        }
    });
    $("#join_us_btn").click(function(){
        if (join_us.val() !== "http://" && join_us.val() !== "Введите адрес вашего сайта" && join_us.val() !== "" && ValidUrl(join_us.val())){
            window.location = "/registration?site="+ encodeURIComponent(join_us.val());
        }
    });
    join_us.on("focus", function () {
        if ($(this).val() === "Введите адрес вашего сайта" || !ValidUrl(join_us.val())) {
            $(this).val("http://");
        }
    });
    join_us.on("blur", function () {
        if ($(this).val() === "http://" || $(this).val() === "" || !ValidUrl(join_us.val())) {
            $(this).val("Введите адрес вашего сайта");
        }
    });
    $('a[href*=#]:not([href=#])').click(function () {
            if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                if (target.length) {
                    $('html,body').animate({
                        scrollTop: target.offset().top
                    }, 1000);
                    return false;
                }
            }
    });
    //$(".player").mb_YTPlayer();
    $(".preload").removeAttr("hidden");
});
//// Mute Vimeo
//var iframe = document.getElementsByTagName('iframe')[0];
//iframe.contentWindow.postMessage('{"method":"setVolume", "value":0}', '*');

