// Initial call and update every second (for future-proofing)
updateDate();
setInterval(updateDate, 1000);

document.addEventListener("DOMContentLoaded", function () {
    setupSidebarToggle();
    setupMobileSidebar();
    setupSidebarHighlight();
    setupSearchFilter();
    setupChart();
});

// Search Functionality
function setupSearchFilter() {
    const searchInput = document.getElementById("searchInput");
    const userList = document.getElementById("userList");
    const noResults = document.getElementById("noResults");

    searchInput.addEventListener("keyup", function () {
        const searchTerm = searchInput.value.toLowerCase();
        let matchFound = false;

        document.querySelectorAll(".user-item").forEach(item => {
            const userInfo = item.querySelector(".user-info").textContent.toLowerCase();
            if (userList && searchTerm) {
                if (userInfo.includes(searchTerm)) {
                    item.style.display = "flex";
                    matchFound = true;
                } else {
                    item.style.display = "none";
                }
            }
        });

        noResults.style.display = matchFound ? "none" : "block";
    });
}

// Chart.js Setup
function setupChart() {
    const ctx = document.getElementById("trendChart").getContext("2d");
    
    new Chart(ctx, {
        type: "line",
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            datasets: [
                {
                    label: "Paid Clients",
                    data: [10, 15, 13, 20, 25, 22, 30, 28, 35, 40, 45, 50], // Sample Data
                    borderColor: "#ffcc00",
                    backgroundColor: "rgba(255, 204, 0, 0.2)",
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false,
                },
            },
            scales: {
                x: {
                    grid: {
                        display: false,
                    },
                },
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
}

// 📌 Sidebar toggle functionality (Desktop)
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

// 📌 Mobile sidebar functionality
function setupMobileSidebar() {
    const sidebar = document.getElementById("sidebar");
    const mobileToggle = document.getElementById("mobile-menu-toggle");
    const overlay = document.getElementById("sidebar-overlay");

    console.log("Sidebar:", sidebar);
    console.log("Mobile toggle:", mobileToggle);
    console.log("Overlay:", overlay);

    if (!sidebar) {
        console.error("Sidebar not found!");
        return;
    }
    if (!mobileToggle) {
        console.error("Mobile toggle button not found!");
        return;
    }
    if (!overlay) {
        console.error("Overlay not found!");
        return;
    }

    // Toggle mobile sidebar
    mobileToggle.addEventListener("click", (e) => {
        console.log("Mobile toggle clicked!");
        sidebar.classList.toggle("mobile-active");
        overlay.classList.toggle("active");
    });

    // Close sidebar when clicking overlay
    overlay.addEventListener("click", () => {
        sidebar.classList.remove("mobile-active");
        overlay.classList.remove("active");
    });

    // Close sidebar when clicking a menu item (mobile only)
    if (window.innerWidth <= 767) {
        const menuItems = document.querySelectorAll(".sidebar ul li a");
        menuItems.forEach(item => {
            item.addEventListener("click", () => {
                sidebar.classList.remove("mobile-active");
                overlay.classList.remove("active");
            });
        });
    }

    // Handle window resize
    window.addEventListener("resize", () => {
        if (window.innerWidth > 767) {
            sidebar.classList.remove("mobile-active");
            overlay.classList.remove("active");
        }
    });
}

// Highlight active sidebar menu & navigate
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

function updateDate() {
    const now = new Date();
    const dateElement = document.getElementById("current-date");
    if (dateElement) {
        dateElement.textContent = now.toLocaleString("en-US", {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
        });
    }
}