$(document).ready(function () {
    const rowsPerPage = 5;
    let allRows = $(".application-table tbody tr");
    let filteredRows = allRows;

    function formatDate(dateStr) {
        const parts = dateStr.split("/");
        return parts.length === 3 ? new Date(parts[2], parts[0] - 1, parts[1]) : null;
    }

    function filterRows() {
        let searchText = $("#search-bar").val().toLowerCase().trim();
        let startDate = $("#start-date").val() ? new Date($("#start-date").val()) : null;
        let endDate = $("#end-date").val() ? new Date($("#end-date").val()) : null;

        filteredRows = allRows.filter(function () {
            let row = $(this);
            let username = row.find("td:nth-child(2)").text().toLowerCase();
            let applicationId = row.find("td:nth-child(3)").text().toLowerCase();
            let rowDate = formatDate(row.find("td:nth-child(5)").text());

            return (!searchText || username.includes(searchText) || applicationId.includes(searchText)) &&
                   (!startDate || rowDate >= startDate) &&
                   (!endDate || rowDate <= endDate);
        });

        $(".application-table tbody tr").hide();
        filteredRows.show();
        updatePagination();
        showPage(1);
    }

    function updatePagination() {
        let totalPages = Math.ceil(filteredRows.length / rowsPerPage) || 1;
        $(".pagination").empty().append([...Array(totalPages).keys()].map(i => 
            `<button class="page-btn" data-page="${i+1}">${i+1}</button>`
        ));
        $(".entries-info").text(`Showing ${filteredRows.length} entries`);
        $(".page-btn").first().addClass("active");
        showPage(1);
    }

    function showPage(page) {
        filteredRows.hide().slice((page - 1) * rowsPerPage, page * rowsPerPage).show();
    }

    $("#search-bar, #start-date, #end-date").on("input change", filterRows);

    $("#select-all").on("change", function () {
        $(".row-checkbox").prop("checked", $(this).prop("checked"));
    });

    $(".btn-view").on("click", function () {
        let userId = $(this).data("user-id");
        $("#formFrame").attr("src", `../Forms/forms_1.html?user=${userId}`);
        $("#viewModal").modal("show");
    });

    $(".btn-approve").on("click", function () {
        $(this).closest("tr").find(".status").text("Approved").css("color", "green");
    });

    $(".btn-reject").on("click", function () {
        $(this).closest("tr").find(".status").text("Rejected").css("color", "red");
    });

    $(".btn-delete").on("click", function () {
        if (confirm("Are you sure you want to delete this application?")) {
            $(this).closest("tr").remove();
        }
    });

    updatePagination();
    showPage(1);
});