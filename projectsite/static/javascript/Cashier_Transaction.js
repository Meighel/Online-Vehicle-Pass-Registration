document.addEventListener("DOMContentLoaded", () => {
    const transactions = JSON.parse(localStorage.getItem("transactions")) || [];
    const tbody = document.getElementById("transaction-body");
    const searchBar = document.getElementById("search-bar");
    const entriesInfo = document.querySelector(".entries-info");
    const paginationContainer = document.getElementById("pagination");
    const rowsPerPage = 5;
    let filteredTransactions = transactions;

    // ========== FUNCTION: Render Transactions Table ==========
    function renderTransactions(page = 1) {
        tbody.innerHTML = "";
        let start = (page - 1) * rowsPerPage;
        let end = start + rowsPerPage;
        let displayedTransactions = filteredTransactions.slice(start, end);

        displayedTransactions.forEach(({ id, username, email, status, paidDate, remarks }) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${paidDate || "N/A"}</td>
                <td>${username}</td>
                <td><span class="status-badge status-${status.toLowerCase()}">${status}</span></td>
                <td>${remarks || "N/A"}</td>
                <td>Cashier</td> <!-- Replace this dynamically if needed -->
            `;
            tbody.appendChild(row);
        });

        entriesInfo.textContent = `Showing ${filteredTransactions.length} entries`;
        updatePagination(page);
    }

    // ========== FUNCTION: Update Pagination ==========
    function updatePagination(currentPage) {
        paginationContainer.innerHTML = "";
        let totalPages = Math.ceil(filteredTransactions.length / rowsPerPage) || 1;

        for (let i = 1; i <= totalPages; i++) {
            let btn = document.createElement("button");
            btn.textContent = i;
            btn.classList.add("page-btn");
            if (i === currentPage) btn.classList.add("active");
            btn.addEventListener("click", () => renderTransactions(i));
            paginationContainer.appendChild(btn);
        }
    }

    // ========== FUNCTION: Search Transactions ==========
    searchBar.addEventListener("input", () => {
        let searchText = searchBar.value.toLowerCase().trim();
        filteredTransactions = transactions.filter(({ username, status, paidDate }) =>
            username.toLowerCase().includes(searchText) ||
            status.toLowerCase().includes(searchText) ||
            (paidDate && paidDate.toLowerCase().includes(searchText))
        );

        renderTransactions(1);
    });

    // ========== INITIATE TRANSACTIONS TABLE ==========
    renderTransactions();
});
document.getElementById("resetStorage").addEventListener("click", () => {
    if (confirm("Are you sure you want to reset all stored data?")) {
        localStorage.clear();
        alert("All data has been reset.");
        location.reload(); // Refresh the page to apply changes
    }
});