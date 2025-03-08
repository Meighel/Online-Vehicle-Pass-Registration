document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("toggle-btn");
    const content = document.querySelector(".content");

    toggleBtn.addEventListener("click", function () {
        sidebar.classList.toggle("collapsed");
        content.classList.toggle("expanded");
    });
});

//Recent Applications
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const userList = document.getElementById("userList");
    const users = userList.getElementsByTagName("li");
    const noResults = document.getElementById("noResults");

    searchInput.addEventListener("input", function () {
        const filter = searchInput.value.toLowerCase().trim();
        let found = false;

        for (let i = 0; i < users.length; i++) {
            let userInfo = users[i].querySelector(".user-info").textContent.toLowerCase();
            
            if (userInfo.includes(filter)) {
                users[i].style.display = "flex"; // Show matching users
                found = true;
            } else {
                users[i].style.display = "none"; // Hide non-matching users
            }
        }

        // Show "No results found" if no matches are found
        noResults.style.display = found ? "none" : "block";
    });
});

// GRAPH
document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById("trendChart").getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May"],
            datasets: [{
                label: "Paid Clients",
                data: [70, 85, 50, 20, 25], 
                borderColor: "#28a745",
                backgroundColor: "rgba(40, 167, 69, 0.2)",
                borderWidth: 2,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});