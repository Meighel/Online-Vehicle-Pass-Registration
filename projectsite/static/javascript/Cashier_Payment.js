$(document).ready(function () {
    const rowsPerPage = 5;
    let allRows = $(".payments-table tbody tr");
    let filteredRows = allRows;

    // ========== Load Updated Data from localStorage ==========
    function loadUpdatedPayments() {
        $(".payments-table tbody tr").each(function () {
            const row = $(this);
            const appId = row.find("td:first").text().trim();
            const storedData = localStorage.getItem(`payment_${appId}`);

            if (storedData) {
                const { status, paidDate } = JSON.parse(storedData);
                row.find("td:eq(3)").html(`<span class="status-badge status-${status.toLowerCase()}">${status}</span>`);
                row.find("td:eq(4)").text(paidDate || "N/A");
            }
        });
    }

    // ========== Format Date Helper Function ==========
    function formatDate(dateStr) {
        let parts = dateStr.split("/");
        return new Date(parts[2], parts[0] - 1, parts[1]);
    }

    // ========== Filter Table Rows ==========
    function filterRows() {
        let searchText = $("#search-bar").val().toLowerCase().trim();
        let startDate = $("#start-date").val() ? new Date($("#start-date").val()) : null;
        let endDate = $("#end-date").val() ? new Date($("#end-date").val()) : null;

        filteredRows = allRows.filter(function () {
            let row = $(this);
            let username = row.find("td:nth-child(2)").text().toLowerCase().trim();
            let appID = row.find("td:nth-child(1)").text().trim();
            let dateText = row.find("td:nth-child(5)").text().trim();
            let rowDate = dateText !== "N/A" ? formatDate(dateText) : null;

            let show = true;
            if (searchText && !username.includes(searchText) && !appID.includes(searchText)) show = false;
            if (startDate && rowDate && rowDate < startDate) show = false;
            if (endDate && rowDate && rowDate > endDate) show = false;

            return show;
        });

        $(".payments-table tbody tr").hide();
        filteredRows.show();
        updatePagination();
        showPage(1);
    }

    // ========== Pagination ==========
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

    // ========== Sorting ==========
    $(".payments-table th").on("click", function () {
        let columnIndex = $(this).index();
        let rows = $(".payments-table tbody tr").toArray();

        rows.sort((a, b) => {
            let aText = $(a).find(`td:eq(${columnIndex})`).text().trim();
            let bText = $(b).find(`td:eq(${columnIndex})`).text().trim();

            return aText.localeCompare(bText, undefined, { numeric: true });
        });

        $(".payments-table tbody").empty().append(rows);
    });

    // ========== Redirect to Update Page ==========
    $(document).on("click", ".update-button", function () {
        const applicationId = $(this).data("id");
        const username = encodeURIComponent($(this).data("username"));
        const email = encodeURIComponent($(this).data("email"));
        const status = encodeURIComponent($(this).data("status"));
        const date = encodeURIComponent($(this).data("date"));

        window.location.href = `Update_Payment.html?id=${applicationId}&username=${username}&email=${email}&status=${status}&date=${date}`;
    });

    $(document).on("click", ".page-btn", function () {
        $(".page-btn").removeClass("active");
        $(this).addClass("active");
        showPage($(this).data("page"));
    });

    $("#filter-btn, #search-bar, #start-date, #end-date").on("input change", function () {
        filterRows();
    });

    // Load updates & remove completed 
    loadUpdatedPayments();
    updatePagination();
});