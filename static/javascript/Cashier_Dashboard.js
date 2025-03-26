// FETCH SIDEBAR
document.addEventListener("DOMContentLoaded", function () {
    loadSidebar().then(() => {
        setupSidebarToggle();
        setupSidebarHighlight();
    });
});

function loadSidebar() {
    return fetch("../../templates/includes/cashier_sidebar.html")
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

function setupSidebarHighlight() {
    const sidebarItems = document.querySelectorAll(".sidebar ul li");

    // Check if transactions exist in localStorage
    const transactions = JSON.parse(localStorage.getItem("transactions")) || [];

    let activeMenu = localStorage.getItem("activeMenu") || "payments"; // Default to payments

    // If there are transactions, switch active menu to "transactions"
    if (transactions.length > 0) {
        activeMenu = "transactions";
        localStorage.setItem("activeMenu", "transactions"); // Store in localStorage
    }

    sidebarItems.forEach(item => {
        item.classList.remove("active");

        if (item.dataset.menu === activeMenu) {
            item.classList.add("active");
        }

        item.addEventListener("click", () => {
            document.querySelector(".sidebar ul li.active")?.classList.remove("active");
            item.classList.add("active");
            localStorage.setItem("activeMenu", item.dataset.menu);
        });
    });
}

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
