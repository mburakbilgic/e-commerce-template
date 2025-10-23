// category.js

$(document).ready(function () {
    console.log("Category page loaded successfully.");

    $(".product-card").on("mouseenter", function () {
        $(this).addClass("shadow-lg");
    });

    $(".product-card").on("mouseleave", function () {
        $(this).removeClass("shadow-lg");
    });

    // (Optional) filter, ordering, infinite scroll etc...
    // function filterProducts(criteria) { ... }
});