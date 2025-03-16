document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById("email");
    const vehicleGif = document.getElementById("vehicleGif");
    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent instant submission

        // Step 1: Reset GIF to original position
        vehicleGif.style.transition = "transform 0.5s ease-in-out";
        vehicleGif.style.transform = "rotate(15deg) translateX(0)";

        // Step 2: Move GIF to the right after a short delay
        setTimeout(() => {
            vehicleGif.style.transition = "transform 1.5s ease-in-out";
            vehicleGif.style.transform = "translateX(570px)";
        }, 500);

        setTimeout(() => {
            window.location.href = "signup.html";
        }, 2000);
    });
});
