/**
 * Created by Dmitry on 03.03.2015.
 */
$(document).ready(function () {
    var join_us = $("#join_us_input");
    $("#join_us_btn").click(function(){
        if (join_us.val() !== "http://" && join_us.val() !== "Введите url вашего сайта" && join_us.val() !== ""){
            window.location = "/registration?site="+ encodeURIComponent(join_us.val());
        }
    });
    join_us.on("focus", function () {
        if ($(this).val() === "Введите url вашего сайта") {
            $(this).val("http://");
        }
    });
    join_us.on("blur", function () {
        if ($(this).val() === "http://" || $(this).val() === "") {
            $(this).val("Введите url вашего сайта");
        }
    });
});