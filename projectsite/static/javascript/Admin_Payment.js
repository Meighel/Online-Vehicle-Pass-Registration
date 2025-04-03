$(document).ready(function () {
    const rowsPerPage = 5;
    let allRows = $(".payments-table tbody tr");
    let filteredRows = allRows; // Store filtered rows for pagination

    function formatDate(dateStr) {
        let parts = dateStr.split("/");
        return new Date(parts[2], parts[0] - 1, parts[1]);
    }

     /**
     * ========== FILTERING FUNCTION ==========
     * This function filters the table based on:
     * - Username (search input)
     * - Date range (Start Date & End Date)
     * - Processed By (dropdown filter)
     */
    function filterRows() {
        let searchText = $("#search-bar").val().toLowerCase().trim();
        let startDate = $("#start-date").val() ? new Date($("#start-date").val()) : null;
        let endDate = $("#end-date").val() ? new Date($("#end-date").val()) : null;
        let processedBy = $("#processed-by").val().toLowerCase().trim();

        filteredRows = allRows.filter(function () {
            let row = $(this);
            let dateText = row.find("td:nth-child(1)").text().trim();
            let username = row.find("td:nth-child(2)").text().toLowerCase().trim();
            let processedByText = row.find("td:nth-child(6)").text().toLowerCase().trim();
            let rowDate = formatDate(dateText);

            let show = true;
            if (startDate && rowDate < startDate) show = false;
            if (endDate && rowDate > endDate) show = false;
            if (searchText && !username.includes(searchText)) show = false;
            if (processedBy && processedBy !== "all" && processedByText !== processedBy) show = false;

            return show;
        });

        $(".payments-table tbody tr").hide();
        filteredRows.show();
        updatePagination();
        showPage(1);
    }

     /**
     * ========== PAGINATION FUNCTIONS ==========
     * - Updates the pagination controls
     * - Handles page switching
     */
    function updatePagination() {
        let totalRows = filteredRows.length;
        let totalPages = Math.ceil(totalRows / rowsPerPage) || 1;
        let pagination = $(".pagination").empty();

        for (let i = 1; i <= totalPages; i++) {
            let btn = $("<button>")
                .text(i)
                .addClass("page-btn")
                .attr("data-page", i);
            pagination.append(btn);
        }

        $(".entries-info").text(`Showing ${totalRows} entries`);
        $(".page-btn").first().addClass("active");
        showPage(1);
    }

    function showPage(page) {
        let start = (page - 1) * rowsPerPage;
        let end = start + rowsPerPage;
        filteredRows.hide().slice(start, end).show();
    }

    /**
     * ========== EVENT LISTENERS ==========
     * - Handles page button clicks
     * - Triggers filtering when input values change
     */
    $(document).on("click", ".page-btn", function () {
        $(".page-btn").removeClass("active");
        $(this).addClass("active");
        showPage($(this).data("page"));
    });

    $("#filter-btn, #search-bar, #processed-by, #start-date, #end-date").on("input change", function () {
        filterRows();
    });

    updatePagination();
});
