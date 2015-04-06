$(document).ready(function () {
    if ($(window).width() >= 1024000) {

        $('.banner').show().revolution(
            {
                dottedOverlay: "none",
                delay: 35000,
                startwidth: 1100,
                startheight: 600,

                touchenabled: "on",
                onHoverStop: "on",

                swipe_velocity: 0.7,
                swipe_min_touches: 1,
                swipe_max_touches: 1,
                drag_block_vertical: false,

                //parallax:"mouse",
                //parallaxBgFreeze:"on",
                //parallaxLevels:[7,4,3,2,5,4,3,2,1,0],

                shadow: 1,
                fullWidth: "on",

                spinner: "spinner4",

                startWithSlide: 0,
                fullScreenAlignForce: "on",
                autoHeight: "on",
                fullScreenOffsetContainer: " "
            });
    }

});	//ready