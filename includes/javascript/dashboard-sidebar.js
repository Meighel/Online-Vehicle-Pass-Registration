function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const content = document.getElementById("content");
    const toggleBtn = document.getElementById("toggle-btn");

    if (sidebar.classList.contains("collapsed")) {
        sidebar.classList.remove("collapsed");
        content.classList.remove("expanded");
    } else {
        sidebar.classList.add("collapsed");
        content.classList.add("expanded");
    }
}


document.addEventListener("DOMContentLoaded", function () {
    const menuItems = document.querySelectorAll(".sidebar ul li");

    // Set default active item on page load (Dashboard)
    menuItems[0].classList.add("active");

    // Add event listener to each menu item
    menuItems.forEach((item) => {
        item.addEventListener("click", function () {
            // Remove 'active' class from all items
            menuItems.forEach((li) => li.classList.remove("active"));
            
            // Add 'active' class to clicked item
            this.classList.add("active");
        });
    });
});

function updateDate() {
    const dateElement = document.getElementById("real-time-date");
    const now = new Date();

    // Format Date (e.g., "Monday, Feb 24, 2025 - 12:34 PM")
    const options = { weekday: 'long', month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true };
    dateElement.textContent = now.toLocaleString('en-US', options);
}

// Update the date on page load and every minute
updateDate();
setInterval(updateDate, 60000);
