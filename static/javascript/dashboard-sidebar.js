// FETCH SIDEBAR
document.addEventListener("DOMContentLoaded", function () {
    loadSidebar().then(() => {
        setupSidebarToggle();
        setupSidebarHighlight();
    });
});

function loadSidebar() {
    return fetch("../../templates/includes/admin_sidebar.html")
        .then(response => response.text())
        .then(html => {
            document.getElementById("sidebar-container").innerHTML = html;
        })
        .catch(error => console.error("Error loading sidebar:", error));
}

// Sidebar Toggle Function
function setupSidebarToggle() {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("toggle-btn");

    if (!sidebar || !toggleBtn) return;

    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
        localStorage.setItem("sidebarState", sidebar.classList.contains("collapsed") ? "collapsed" : "expanded");
    });

    if (localStorage.getItem("sidebarState") === "collapsed") {
        sidebar.classList.add("collapsed");
    }
}

// Sidebar Active Item Highlight
function setupSidebarHighlight() {
    const items = document.querySelectorAll(".sidebar ul li");

    items.forEach(item => {
        item.addEventListener("click", () => {
            document.querySelector(".sidebar ul li.active")?.classList.remove("active");
            item.classList.add("active");
            localStorage.setItem("activeMenu", item.dataset.menu);
        });

        if (item.dataset.menu === localStorage.getItem("activeMenu")) {
            item.classList.add("active");
        }
    });
}


//time 
function updateDate() {
    const options = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
    document.getElementById('date').textContent = new Date().toLocaleDateString('en-US', options);
}

function updateDate() {
    const dateElement = document.getElementById("real-time-date");
    const now = new Date();
    const options = { weekday: 'long', month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true };
    dateElement.textContent = now.toLocaleString('en-US', options);
}

updateDate();
setInterval(updateDate, 60000);
