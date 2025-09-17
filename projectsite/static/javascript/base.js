document.addEventListener("DOMContentLoaded", async () => {
    setupSidebarHighlight();
    displayCurrentDate();

});
function setupSidebarHighlight() {
    const sidebarItems = document.querySelectorAll(".sidebar ul li");
    const activeMenu = localStorage.getItem("activeMenu") || "dashboard";

    sidebarItems.forEach(item => {
        const menuName = item.dataset.menu;
        item.classList.toggle("active", menuName === activeMenu);

        item.addEventListener("click", () => {
            document.querySelector(".sidebar ul li.active")?.classList.remove("active");
            item.classList.add("active");
            localStorage.setItem("activeMenu", menuName);

            // Navigate to the corresponding page
            const link = item.querySelector("a");
            if (link) window.location.href = link.href;
        });
    });
}

// Display current date
function displayCurrentDate() {
    const dateElement = document.getElementById("date");
    if (dateElement) {
        dateElement.textContent = new Date().toLocaleDateString("en-US", {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric"
        });
    }
}