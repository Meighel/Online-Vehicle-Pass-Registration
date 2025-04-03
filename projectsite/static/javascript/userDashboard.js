document.addEventListener("DOMContentLoaded", function () {
    loadSidebar().then(() => {
        setupSidebarToggle();
        setupSidebarHighlight();
    });

    updateDate(); // Initialize date update
    setInterval(updateDate, 60000); // Refresh date every minute

    loadApplicationData(); // Load and display application details
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

        // Restore active menu from localStorage
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
        weekday: "long",
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        hour12: true
    };
    dateElement.textContent = now.toLocaleString("en-US", options);
}

// ✅ Load Chart (if applicable)
document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById("registrationChart");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Pending Applicants", "Rejected", "Approved"],
            datasets: [{
                data: [550, 185, 120],
                backgroundColor: ["#007bff", "#dc3545", "#28a745"],
                hoverOffset: 10
            }]
        },
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

// ✅ Load Application Data (Simulated API Call)
function loadApplicationData() {
    const applicationData = {
        status: "In Progress",
        dateApplied: "02-12-2025",
        history: [
            { number: "123456", type: "Sedan", approvalDate: "02-15-2025", remarks: "Approved" },
            { number: "789012", type: "SUV", approvalDate: "02-10-2025", remarks: "Pending" }
        ]
    };

    // Update Application Status
    const statusElement = document.getElementById("application-status");
    const dateElement = document.getElementById("date-applied");

    if (statusElement && dateElement) {
        statusElement.innerHTML = `<p class="fs-4 fw-bold">${applicationData.status}</p>`;
        dateElement.textContent = `Date Applied: ${applicationData.dateApplied}`;
    }

    // Populate Application History Table
    const historyTable = document.getElementById("application-history");
    if (historyTable) {
        historyTable.innerHTML = applicationData.history.map(item => `
            <tr>
                <td>${item.number}</td>
                <td>${item.type}</td>
                <td>${item.approvalDate}</td>
                <td class="${item.remarks === 'Approved' ? 'text-success' : 'text-warning'}">${item.remarks}</td>
            </tr>
        `).join('');
    }
}
