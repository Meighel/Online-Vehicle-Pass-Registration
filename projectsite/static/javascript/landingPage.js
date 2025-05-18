document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById("email");
    const vehicleGif = document.getElementById("vehicleGif");
    const createAccountBtn = document.getElementById("create-account-btn");
    const emailErrorMsg = document.getElementById("email-error-message");

    function validateEmail(email) {
        const domain = "@psu.palawan.edu.ph";
        return email.toLowerCase().endsWith(domain);
    }

    emailInput.addEventListener("blur", function () {
        const email = emailInput.value.trim();
        if (email && !validateEmail(email)) {
            emailErrorMsg.textContent = "Please use a valid @psu.palawan.edu.ph email address";
            emailErrorMsg.style.display = "block";
            emailInput.classList.add("is-invalid");
        } else {
            emailErrorMsg.style.display = "none";
            emailInput.classList.remove("is-invalid");
        }
    });

    emailInput.addEventListener("input", function () {
        emailErrorMsg.style.display = "none";
        emailInput.classList.remove("is-invalid");
    });

    createAccountBtn.addEventListener("click", function () {
        const email = emailInput.value.trim();

        if (!email) {
            emailErrorMsg.textContent = "Please enter your email address";
            emailErrorMsg.style.display = "block";
            emailInput.classList.add("is-invalid");
            return;
        }

        if (!validateEmail(email)) {
            emailErrorMsg.textContent = 'Please provide a correct email "@psu.palawan.edu.ph"';
            emailErrorMsg.style.display = "block";
            emailInput.classList.add("is-invalid");
            return;
        }

        vehicleGif.style.transition = "transform 0.5s ease-in-out";
        vehicleGif.style.transform = "rotate(15deg) translateX(0)";

        setTimeout(() => {
            vehicleGif.style.transition = "transform 1.5s ease-in-out";
            vehicleGif.style.transform = "translateX(570px)";
        }, 500);

        setTimeout(() => {
            window.location.href = signupUrl + "?email_value=" + encodeURIComponent(email);
        }, 2000);
    });
});