$(document).ready(function () {
    let rowsPerPage = 5;
    let currentPage = 1;
    let allRows = $(".passes-table tbody tr"); // Store all rows initially
    let filteredRows = allRows; // Stores filtered rows for pagination

    /**
     * Function to show only the selected page rows
     */
    function showPage(page) {
        let totalRows = filteredRows.length;
        let totalPages = Math.ceil(totalRows / rowsPerPage) || 1;

        if (page < 1) page = 1;
        if (page > totalPages) page = totalPages;

        let start = (page - 1) * rowsPerPage;
        let end = start + rowsPerPage;

        filteredRows.hide().slice(start, end).show();
        currentPage = page;
        updatePagination(totalPages);
    }

    /**
     * Function to update the pagination UI
     */
    function updatePagination(totalPages) {
        let pagination = $(".pagination");
        pagination.empty();

        if (totalPages > 1) {
            pagination.append(`<button class="prev-btn" ${currentPage === 1 ? "disabled" : ""}>&laquo; Prev</button>`);

            for (let i = 1; i <= totalPages; i++) {
                let btn = $(`<button>`).text(i).addClass("page-btn").attr("data-page", i);
                if (i === currentPage) btn.addClass("active");
                pagination.append(btn);
            }

            pagination.append(`<button class="next-btn" ${currentPage === totalPages ? "disabled" : ""}>Next &raquo;</button>`);
        }
    }

    /**
     * Function to filter the table based on search input
     */
    function filterTable() {
        let searchText = $("#search-bar").val().toLowerCase().trim();

        // Filter rows based on username or application ID
        filteredRows = allRows.filter(function () {
            let row = $(this);
            let username = row.find("td:nth-child(2)").text().toLowerCase();
            let appID = row.find("td:nth-child(3)").text().toLowerCase();

            return username.includes(searchText) || appID.includes(searchText);
        });

        $(".passes-table tbody tr").hide(); // Hide all rows first
        filteredRows.show(); // Show only filtered rows
        updatePagination(Math.ceil(filteredRows.length / rowsPerPage)); // Update pagination
        showPage(1); // Reset to page 1 after filtering
    }

    /**
     * Event Listeners for pagination and filtering
     */
    $(document).on("click", ".page-btn", function () {
        let page = parseInt($(this).data("page"));
        showPage(page);
    });

    $(document).on("click", ".prev-btn", function () {
        if (currentPage > 1) {
            showPage(currentPage - 1);
        }
    });

    $(document).on("click", ".next-btn", function () {
        let totalPages = $(".page-btn").length;
        if (currentPage < totalPages) {
            showPage(currentPage + 1);
        }
    });

    $("#filter-btn, #search-bar").on("input", function () {
        filterTable();
    });

    // Initialize first page load
    showPage(1);
});
