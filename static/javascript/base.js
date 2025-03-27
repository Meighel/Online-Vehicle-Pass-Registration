// FETCH SIDEBAR
document.addEventListener("DOMContentLoaded", function () {
    loadSidebar().then(() => {
        setupSidebarToggle();
        setupSidebarHighlight();
    });
});

document.addEventListener("DOMContentLoaded", async function () {
    await loadSidebar();
    setupSidebarToggle();
    setupSidebarHighlight();
});

async function loadSidebar() {
    // TEMPORARY HARDCODED ROLE FOR TESTING (Change this to test different sidebars)
    const userRole = "cashier"; // Change this to "cashier", "security", or "user"

    // Map roles to sidebar file paths
    const sidebarFiles = {
        admin: "../templates/includes/admin_sidebar.html",
        cashier: "../../templates/includes/cashier_sidebar.html",
        security: "../templates/includes/security_sidebar.html",
        user: "../templates/includes/user-sidebar.html"
    };

    // Get the sidebar container
    const sidebarContainer = document.getElementById("sidebar-container");

    if (!sidebarFiles[userRole]) {
        console.error("Invalid role or sidebar not found:", userRole);
        sidebarContainer.innerHTML = "<p>Error: Sidebar not available.</p>";
        return;
    }

    try {
        const response = await fetch(sidebarFiles[userRole]);
        if (!response.ok) throw new Error("Failed to fetch sidebar");

        sidebarContainer.innerHTML = await response.text();
    } catch (error) {
        console.error("Error loading sidebar:", error);
        sidebarContainer.innerHTML = "<p>Error loading sidebar.</p>";
    }
}

// Dummy functions for sidebar interactions
function setupSidebarToggle() {
    console.log("Sidebar toggle setup (add your code here)");
}

function setupSidebarHighlight() {
    console.log("Sidebar highlight setup (add your code here)");
}


// Function to get user role (Replace this with actual logic)
function getUserRole() {
    return "cashier"; // Replace with actual role (e.g., from sessionStorage, API, backend response)
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

function setupSidebarHighlight() {
    const sidebarItems = document.querySelectorAll(".sidebar ul li");
    let activeMenu = localStorage.getItem("activeMenu") || "dashboard"; // Default to "Dashboard"

    sidebarItems.forEach(item => {
        const menuName = item.dataset.menu;

        // Remove any existing active classes
        item.classList.remove("active");

        // Apply the active class if this item matches stored menu
        if (menuName === activeMenu) {
            item.classList.add("active");
        }

        // Add event listener for user clicks
        item.addEventListener("click", () => {
            // Remove active class from previously selected menu
            document.querySelector(".sidebar ul li.active")?.classList.remove("active");

            // Set new active menu
            item.classList.add("active");
            localStorage.setItem("activeMenu", menuName);
        });
    });
}

document.addEventListener("DOMContentLoaded", function () {
    loadSidebar().then(() => {
        setupSidebarToggle();
        setupSidebarHighlight();
    });
});

//time 
document.addEventListener("DOMContentLoaded", () => {
    const dateElement = document.getElementById("date");
    if (dateElement) {
        dateElement.textContent = new Date().toLocaleDateString('en-US', {
            weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
        });
    }
});


// Chart.js Setup
document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("trendChart");
    if (!canvas) {
        console.error("Canvas element #trendChart not found!");
        return;
    }

    const ctx = canvas.getContext("2d");

    const chartData = {
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
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
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
    };

    new Chart(ctx, {
        type: "line",
        data: chartData,
        options: chartOptions,
    });

    console.log("Chart initialized successfully.");
});
