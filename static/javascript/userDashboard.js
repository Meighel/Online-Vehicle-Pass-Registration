document.addEventListener("DOMContentLoaded", function () {
    loadSidebar().then(() => {
        setupSidebarToggle();
        setupSidebarHighlight();
    });
    updateDate(); // Initialize date update
    setInterval(updateDate, 60000); // Refresh date every minute
});

// ✅ Load Sidebar Dynamically
function loadSidebar() {
    return fetch("../../templates/includes/user-sidebar.html")
        .then(response => {
            if (!response.ok) throw new Error("Sidebar not found.");
            return response.text();
        })
        .then(html => document.getElementById("sidebar-container").innerHTML = html)
        .catch(error => console.error("Error loading sidebar:", error));
}

// ✅ Sidebar Toggle Function
function setupSidebarToggle() {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("toggle-btn");

    if (!sidebar || !toggleBtn) return;

    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
        localStorage.setItem("sidebarState", sidebar.classList.contains("collapsed") ? "collapsed" : "expanded");
    });

    // Load sidebar state from localStorage
    if (localStorage.getItem("sidebarState") === "collapsed") {
        sidebar.classList.add("collapsed");
    }
}

// ✅ Sidebar Active Item Highlight
function setupSidebarHighlight() {
    const items = document.querySelectorAll(".sidebar ul li");

    items.forEach(item => {
        item.addEventListener("click", () => {
            document.querySelector(".sidebar ul li.active")?.classList.remove("active");
            item.classList.add("active");
            localStorage.setItem("activeMenu", item.dataset.menu);
        });

        // Set active menu from localStorage
        if (item.dataset.menu === localStorage.getItem("activeMenu")) {
            item.classList.add("active");
        }
    });
}

// ✅ Update Date in Real-Time
function updateDate() {
    const dateElement = document.getElementById("real-time-date");
    if (!dateElement) return;

    const now = new Date();
    const options = {
        weekday: "long", month: "short", day: "numeric",
        year: "numeric", hour: "2-digit", minute: "2-digit", hour12: true
    };
    dateElement.textContent = now.toLocaleString("en-US", options);
}

// ✅ Load Chart Only if Canvas Exists
document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById("registrationChart");
    if (!canvas) return; // Exit if no chart element is found

    const ctx = canvas.getContext("2d");

    const data = {
        labels: ["Pending Applicants", "Rejected", "Approved"],
        datasets: [{
            data: [550, 185, 120], // Example values
            backgroundColor: ["#007bff", "#dc3545", "#28a745"], // Blue, Red, Green
            hoverOffset: 10
        }]
    };

    new Chart(ctx, {
        type: "doughnut",
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: { padding: 5 },
            plugins: {
                legend: { position: "bottom" },
                title: {
                    display: true,
                    text: "Registration Overview",
                    font: { size: 16, weight: "bold" },
                    color: "#fff",
                    padding: { top: 10, bottom: 10 }
                }
            }
        }
    });
});
