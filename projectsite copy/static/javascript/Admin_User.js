$(document).ready(function () {
    const rowsPerPage = 5;
    let allRows = $(".users-table tbody tr");
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
        let startDate = $("#start-date").val() ? new Date($("#start-date").val()) : null;
        let endDate = $("#end-date").val() ? new Date($("#end-date").val()) : null;

        filteredRows = allRows.filter(function () {
            let row = $(this);
            let username = row.find("td:nth-child(2)").text().trim().toLowerCase();
            let applicationId = row.find("td:nth-child(3)").text().trim().toLowerCase();
            let dateText = row.find("td:nth-child(5)").text().trim();
            let rowDate = formatDate(dateText);

            if (!rowDate) {
                console.warn("Skipping invalid date:", dateText);
                return false;
            }

            let matchesSearch = !searchText || username.includes(searchText) || applicationId.includes(searchText);
            let matchesDateRange = true;

            if (startDate && rowDate < startDate) matchesDateRange = false;
            if (endDate && rowDate > endDate) matchesDateRange = false;

            return matchesSearch && matchesDateRange;
        });

        $(".users-table tbody tr").hide();
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

    $("#filter-btn, #search-bar, #start-date, #end-date").on("input change", function () {
        filterRows();
    });

    $("#select-all").on("change", function () {
        $(".row-checkbox").prop("checked", $(this).prop("checked"));
    });

    $(document).on("click", ".btn-view", function () {
        let row = $(this).closest("tr");

        // Collect user data 
        // another page eto for admin to view the user details. pero hindi ko alam kong anong details yun. kung personal info
        // or registration details
        let userData = {
            username: row.find("td:nth-child(2)").text().trim(),
            applicationId: row.find("td:nth-child(3)").text().trim(),
            account: row.find("td:nth-child(4)").text().trim(),
            date: row.find("td:nth-child(5)").text().trim(),
            status: row.find("td:nth-child(6)").text().trim(),
        };

        // Store data in sessionStorage
        sessionStorage.setItem("userDetails", JSON.stringify(userData));

        // Redirect to details page
        window.location.href = "user_details.html";
    });

    $(document).on("click", ".btn-approve", function () {
        let row = $(this).closest("tr");
        let userId = row.find("td:nth-child(3)").text().trim();

        row.find(".status").text("Approved").css("color", "green");
        updateUserStatus(userId, "Approved");
    });

    $(document).on("click", ".btn-reject", function () {
        let row = $(this).closest("tr");
        let userId = row.find("td:nth-child(3)").text().trim();

        row.find(".status").text("Rejected").css("color", "red");
        updateUserStatus(userId, "Rejected");
    });

    function updateUserStatus(userId, status) {
        let applications = JSON.parse(localStorage.getItem("applications")) || {};
        applications[userId] = status;
        localStorage.setItem("applications", JSON.stringify(applications));
    }

    $(document).on("click", ".btn-delete", function () {
        let row = $(this).closest("tr");
        let userId = row.find("td:nth-child(3)").text().trim();

        let applications = JSON.parse(localStorage.getItem("applications")) || {};
        delete applications[userId];
        localStorage.setItem("applications", JSON.stringify(applications));

        row.remove();
        filterRows();
    });

    $(".close").click(function () {
        $("#user-modal").fadeOut();
    });

    updatePagination();
    showPage(1);
});
