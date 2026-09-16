
console.log("Luxe Bites JavaScript loaded");



document.addEventListener("DOMContentLoaded", function () {

    console.log("Luxe Bites JavaScript loaded!");

    const buttons = document.querySelectorAll(".buy-button");

    buttons.forEach(function (button) {

        button.addEventListener("click", function () {

            alert("Biscuit added to cart!");

        });

    });

});


/*
const button = document.getElementById("welcomeBtn");

const message = document.getElementById("message");

button.addEventListener("click", function () {

    message.textContent = "Welcome to Luxe Bites! 🍪";

});
*/