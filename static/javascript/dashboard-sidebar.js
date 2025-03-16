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

    const activeMenu = localStorage.getItem("activeMenu");

    if (activeMenu) {
        const activeItem = document.querySelector(`.sidebar ul li[data-id='${activeMenu}']`);
        if (activeItem) {
            activeItem.classList.add("active");
        }
    }

    menuItems.forEach((item) => {
        item.addEventListener("click", function () {
            menuItems.forEach((li) => li.classList.remove("active"));
            this.classList.add("active");
            localStorage.setItem("activeMenu", this.getAttribute("data-id"));
        });
    });
});


function updateDate() {
    const dateElement = document.getElementById("real-time-date");
    const now = new Date();
    const options = { weekday: 'long', month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true };
    dateElement.textContent = now.toLocaleString('en-US', options);
}

updateDate();
setInterval(updateDate, 60000);
