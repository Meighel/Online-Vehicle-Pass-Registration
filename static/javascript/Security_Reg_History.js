document.addEventListener("DOMContentLoaded", () => {
    const registered = JSON.parse(localStorage.getItem("registered")) || [];
    const tbody = document.getElementById("transaction-body");
    const searchBar = document.getElementById("search-bar");
    const entriesInfo = document.querySelector(".entries-info");
    const paginationContainer = document.getElementById("pagination");
    const rowsPerPage = 5;
    let filteredRegistered = registered;

    // ========== FUNCTION: Render Registered Table ==========
    function renderRegistered(page = 1) {
        tbody.innerHTML = "";
        let start = (page - 1) * rowsPerPage;
        let end = start + rowsPerPage;
        let displayedRegistered = filteredRegistered.slice(start, end);

        displayedRegistered.forEach(({ id, username, status, date, remarks, processBy }) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${date || "N/A"}</td>
                <td>${username}</td>
                <td><span class="status-badge status-${status.toLowerCase()}">${status}</span></td>
                <td>${remarks || "N/A"}</td>
                <td>${processBy || "N/A"}</td>
            `;
            tbody.appendChild(row);
        });

        entriesInfo.textContent = `Showing ${filteredRegistered.length} entries`;
        updatePagination(page);
    }

    // ========== FUNCTION: Update Pagination ==========
    function updatePagination(currentPage) {
        paginationContainer.innerHTML = "";
        let totalPages = Math.ceil(filteredRegistered.length / rowsPerPage) || 1;

        for (let i = 1; i <= totalPages; i++) {
            let btn = document.createElement("button");
            btn.textContent = i;
            btn.classList.add("page-btn");
            if (i === currentPage) btn.classList.add("active");
            btn.addEventListener("click", () => renderRegistered(i));
            paginationContainer.appendChild(btn);
        }
    }

    // ========== FUNCTION: Search Registered ==========
    searchBar.addEventListener("input", () => {
        let searchText = searchBar.value.toLowerCase().trim();
        filteredRegistered = registered.filter(({ username, status, date }) =>
            username.toLowerCase().includes(searchText) ||
            status.toLowerCase().includes(searchText) ||
            (date && date.toLowerCase().includes(searchText))
        );

        renderRegistered(1);
    });

    // ========== INITIATE REGISTERED TABLE ==========
    renderRegistered();
});

document.getElementById("resetStorage").addEventListener("click", () => {
    if (confirm("Are you sure you want to reset all stored data?")) {
        localStorage.clear();
        alert("All data has been reset.");
        location.reload(); // Refresh the page to apply changes
    }
});
