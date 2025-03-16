document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("toggle-btn");

    if (toggleBtn) {
        toggleBtn.addEventListener("click", function () {
            sidebar.classList.toggle("collapsed");
        });
    }
});
