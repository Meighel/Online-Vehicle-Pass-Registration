$(document).ready(function () {
    const rowsPerPage = 5;
    let allRows = $(".passes-table tbody tr");
    let filteredRows = allRows;

    function formatDate(dateStr) {
        const parts = dateStr.split("/");
        if (parts.length !== 3) return null;
        return new Date(parts[2], parts[0] - 1, parts[1]); // MM/DD/YYYY format
    }

    /**
     * ========== FILTERING FUNCTION ==========
     * Filters based on:
     * - Username
     * - Application ID
     * - Date Range (Start & End Date)
     */
    function filterRows() {
        let searchText = $("#search-bar").val().toLowerCase().trim();
        let appIDText = $("#application-id").val()?.toLowerCase().trim() || "";
        let startDate = $("#start-date").val() ? new Date($("#start-date").val()) : null;
        let endDate = $("#end-date").val() ? new Date($("#end-date").val()) : null;

        filteredRows = allRows.filter(function () {
            let row = $(this);
            let username = row.find("td:nth-child(2)").text().toLowerCase().trim();
            let appID = row.find("td:nth-child(3)").text().toLowerCase().trim();
            let dateText = row.find("td:nth-child(8)").text().trim();
            let rowDate = formatDate(dateText);

            if (!rowDate) {
                console.warn("Skipping invalid date:", dateText);
                return false;
            }

            let matchesUsername = !searchText || username.includes(searchText);
            let matchesAppID = !appIDText || appID.includes(appIDText);
            let matchesDateRange = true;

            if (startDate && rowDate < startDate) matchesDateRange = false;
            if (endDate && rowDate > endDate) matchesDateRange = false;

            return matchesUsername && matchesAppID && matchesDateRange;
        });

        $(".passes-table tbody tr").hide();
        filteredRows.show();
        updatePagination();
        showPage(1);
    }

    /**
     * ========== PAGINATION FUNCTIONS ==========
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
     */
    $(document).on("click", ".page-btn", function () {
        $(".page-btn").removeClass("active");
        $(this).addClass("active");
        showPage($(this).data("page"));
    });

    $("#filter-btn, #search-bar, #application-id, #start-date, #end-date").on("input change", function () {
        filterRows();
    });

    updatePagination();
});
