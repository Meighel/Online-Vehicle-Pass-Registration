document.addEventListener("DOMContentLoaded", function () {
    const emailInput = document.getElementById("email");
    const vehicleGif = document.getElementById("vehicleGif");
    const createAccountBtn = document.getElementById("create-account-btn");
    
    createAccountBtn.addEventListener("click", function() {
        const email = document.getElementById("email").value;
        if (email) {
            // Step 1: Reset GIF to original position
            vehicleGif.style.transition = "transform 0.5s ease-in-out";
            vehicleGif.style.transform = "rotate(15deg) translateX(0)";
            
            // Step 2: Move GIF to the right after a short delay
            setTimeout(() => {
                vehicleGif.style.transition = "transform 1.5s ease-in-out";
                vehicleGif.style.transform = "translateX(570px)";
            }, 500);
            
            // Step 3: Redirect after animation completes
            setTimeout(() => {
                window.location.href = "{% url 'signup' %}?email_value=" + encodeURIComponent(email);
            }, 2000);
        } else {
            alert('Please enter your email address');
        }
    });
});