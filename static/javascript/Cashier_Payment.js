$(document).ready(function () {
    const rowsPerPage = 5;
    let allRows = $(".payments-table tbody tr");
    let filteredRows = allRows;

    // ========== FORMAT DATE ==========
    function formatDate(dateStr) {
        let parts = dateStr.split("/");
        return new Date(parts[2], parts[0] - 1, parts[1]);
    }

    // ========== FILTER FUNCTION ==========
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

    // ========== PAGINATION ==========
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

    // ========== SORTING ==========
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

    // ========== EVENT LISTENERS ==========
    $(document).on("click", ".page-btn", function () {
        $(".page-btn").removeClass("active");
        $(this).addClass("active");
        showPage($(this).data("page"));
    });

    $("#filter-btn, #search-bar, #start-date, #end-date").on("input change", function () {
        filterRows();
    });

    updatePagination();

    // ========== UPDATE STATUS ========== //
    $(document).ready(function () {
        let selectedRow; // Store the selected row
    
        // Open Modal on "Update" Click
        $(document).on("click", ".open-modal", function () {
            selectedRow = $(this).closest("tr"); // Get the row that was clicked
            $("#statusModal").modal("show"); // Show the modal
        });
    
        // Approve Button Click
        $("#approveBtn").on("click", function () {
            updateStatus("Approved", "status-approved");
        });
    
        // Reject Button Click
        $("#rejectBtn").on("click", function () {
            updateStatus("Rejected", "status-rejected");
        });
    
        // Function to Update Status
        function updateStatus(statusText, statusClass) {
            let statusBadge = selectedRow.find(".status-badge"); // Find the status badge in the row
    
            // Update Status Text
            statusBadge.text(statusText);
    
            // Update CSS Classes
            statusBadge.removeClass("status-pending status-approved status-rejected")
                        .addClass(statusClass);
    
            $("#statusModal").modal("hide"); // Close the modal after updating
        }
    });
        // Handle Update Status action
     $("#btn-updateStatus").click(function () {
        if (confirm("Are you sure you want to update this application?")) {
            let applications = JSON.parse(localStorage.getItem("applications")) || {};
            applications[userData.plateNumber] = status; // Use Plate Number as unique ID
            localStorage.setItem("applications", JSON.stringify(applications));
    
            sessionStorage.updateStatus("userDetails"); // Clear session storage
            alert("Application Deleted!");
            window.location.href = "Cashier_Transaction.js"; // Redirect back
        }
    });
});
