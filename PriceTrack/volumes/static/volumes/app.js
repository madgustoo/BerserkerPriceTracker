$(".accordion-toggle").on("click", function() {
    if ($(this).hasClass("active")){
        $(this).css("color", "black");
        $(this).removeClass("active");
    } else {
        $(this).css("color", "lightcoral");
        $(this).addClass("active");
    }
});