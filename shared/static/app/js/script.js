var numeroSlide = 1;
var formatearLoop = false;
/*Slide */

$("#indicator li").click(function () {

    var roleSlide = $(this).attr("role-slide")
    console.log('roleSlide', roleSlide);

    $("#slide ul li").css({ "display": "none" });

    $("#slide ul li:nth-child(" + roleSlide + ")").fadeIn();

    $("#indicator li").css({ "opacity": ".5" });

    $(this).css({ "opacity": "none" });

    formatearLoop = true;

    numeroSlide= roleSlide;
});

function avanzar() {
    if (numeroSlide >= 3) {
        numeroSlide = 1;
    }
    else {
        numeroSlide++;
    }

    $("#slide ul li").css({ "display": "none" });

    $("#slide ul li:nth-child(" + numeroSlide + ")").fadeIn();

    $("#indicator li").css({ "opacity": ".5" });

    $("#slide ul li:nth-child(" + numeroSlide + ")").css({ "opacity": "1" });
    console.log('numeroSlide', numeroSlide);

    
}

$("#right").click(function () {
    avanzar();
    formatearLoop = true;
});

$("#left").click(function () {
    if (numeroSlide <= 1) {
        numeroSlide = 3;
    }
    else {
        numeroSlide--;
    }

    $("#slide ul li").css({ "display": "none" });

    $("#slide ul li:nth-child(" + numeroSlide + ")").fadeIn();

    $("#indicator li").css({ "opacity": ".5" });

    $("#slide ul li:nth-child(" + numeroSlide + ")").css({ "opacity": "1" });
    console.log('numeroSlide', numeroSlide);

    formatearLoop = true;
});

setInterval(function () {
    if (formatearLoop) {
        formatearLoop = false;
    } else {
        avanzar();
    }

}, 5000);