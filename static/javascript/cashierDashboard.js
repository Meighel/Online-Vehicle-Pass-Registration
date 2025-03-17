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

// Initial call and update every second (for future-proofing)
updateDate();
setInterval(updateDate, 1000);

document.addEventListener("DOMContentLoaded", function () {
    setupSidebarToggle();
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
