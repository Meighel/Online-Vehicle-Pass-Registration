$(document).ready(function () {
    const rowsPerPage = 5;
    let allRows = $(".payments-table tbody tr");
    let filteredRows = allRows; // This will hold the current set of rows after filtering

    function formatDate(dateStr) {
        let parts = dateStr.split("/");
        return new Date(parts[2], parts[0] - 1, parts[1]);
    }

    function filterRows() {
        let searchText = $("#search-bar").val().toLowerCase().trim();
        let startDate = $("#start-date").val() ? new Date($("#start-date").val()) : null;
        let endDate = $("#end-date").val() ? new Date($("#end-date").val()) : null;

        filteredRows = allRows.filter(function () {
            let row = $(this);
            let username = row.find("td:nth-child(2)").text().trim().toLowerCase(); // Username column
            let applicationId = row.find("td:nth-child(3)").text().trim().toLowerCase(); // Application ID column
            let dateText = row.find("td:nth-child(5)").text().trim(); // Date column
            let rowDate = formatDate(dateText);

            let show = true;

            // Search filter for username and application ID
            if (searchText && !username.includes(searchText) && !applicationId.includes(searchText)) {
                show = false;
            }

            // Filter by start and end date
            if (startDate && rowDate < startDate) show = false;
            if (endDate && rowDate > endDate) show = false;

            return show;
        });

        // Hide all rows and only show filtered ones
        allRows.hide();
        filteredRows.show();

        updatePagination(filteredRows.length);
        showPage(1);
    }

    // Pagination Update
    function updatePagination(totalRows) {
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
    }

    function showPage(page) {
        let startIndex = (page - 1) * rowsPerPage;
        let endIndex = startIndex + rowsPerPage;

        // for pagination purposes
        filteredRows.hide();
        filteredRows.slice(startIndex, endIndex).show();
    }

    $(document).on("click", ".page-btn", function () {
        $(".page-btn").removeClass("active");
        $(this).addClass("active");
        showPage($(this).data("page"));
    });

    $("#filter-btn, #search-bar, #application, #start-date, #end-date").on("input change", function () {
        filterRows();
    });

    $("#select-all").on("change", function () {
        $(".row-checkbox").prop("checked", $(this).prop("checked"));
    });

    $(document).on("click", ".btn-view", function () {
        let row = $(this).closest("tr");

        // Collect user data
        let userData = {
            firstName: row.data("first-name"),
            middleName: row.data("middle-name"),
            lastName: row.data("last-name"),
            email: row.data("email"),
            role: row.data("role"),
            plateNumber: row.data("plate-number"),
            model: row.data("model"),
            color: row.data("color"),
            vehicleType: row.data("vehicle-type"),
            owner: row.data("owner"),
            googleDriveLink: row.data("google-drive")
        };

        // Store data in sessionStorage
        sessionStorage.setItem("userDetails", JSON.stringify(userData));

        // Redirect to the details page
        window.location.href = "user_details.html";
    });

    $(document).on("click", ".btn-approve", function () {
        let row = $(this).closest("tr");
        let userId = row.find("td:nth-child(3)").text().trim(); // Assuming Application ID is in 3rd column

        // Update the row visually
        row.find(".status").text("Approved").css("color", "green");

        // Update status in localStorage (simulating database)
        updateUserStatus(userId, "Approved");
    });

    $(document).on("click", ".btn-reject", function () {
        let row = $(this).closest("tr");
        let userId = row.find("td:nth-child(3)").text().trim(); // Assuming Application ID is in 3rd column

        // Update the row visually
        row.find(".status").text("Rejected").css("color", "red");

        // Update status in localStorage (simulating database)
        updateUserStatus(userId, "Rejected");
    });

    function updateUserStatus(userId, status) {
        let applications = JSON.parse(localStorage.getItem("applications")) || {};

        // Update status for the user
        applications[userId] = status;

        // Save back to storage
        localStorage.setItem("applications", JSON.stringify(applications));
    }

    $(document).on("click", ".btn-delete", function () {
        let row = $(this).closest("tr");
        let userId = row.find("td:nth-child(3)").text().trim();

        // Remove from localStorage
        let applications = JSON.parse(localStorage.getItem("applications")) || {};
        delete applications[userId];
        localStorage.setItem("applications", JSON.stringify(applications));

        // Remove row from DOM and re-filter
        row.remove();
        filterRows();
    });

    // Handle Modal Close
    $(".close").click(function () {
        $("#user-modal").fadeOut();
    });

    // Initialize pagination
    updatePagination(allRows.length);
    showPage(1);
});
