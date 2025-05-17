function validateEmail() {
    const email = document.getElementById("email").value;
    const errorMessage = document.getElementById("error-message");

    const pattern = /^[a-zA-Z0-9._%+-]+@psu\.palawan\.edu\.ph$/;

    if (!pattern.test(email)) {
    errorMessage.textContent = "Invalid email. Must end with @psu.palawan.edu.ph";
    return false; // prevent form submission
    }

    errorMessage.textContent = ""; // clear error if valid
    return true;
}