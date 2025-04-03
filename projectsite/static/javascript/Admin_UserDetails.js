$(document).ready(function () {
    // Retrieve user data from sessionStorage
    let userData = JSON.parse(sessionStorage.getItem("userDetails"));

    if (userData) {
        $("#first-name").text(userData.firstName);
        $("#middle-name").text(userData.middleName);
        $("#last-name").text(userData.lastName);
        $("#email").text(userData.email);
        $("#role").text(userData.role);
        $("#plate-number").text(userData.plateNumber);
        $("#model").text(userData.model);
        $("#color").text(userData.color);
        $("#vehicle-type").text(userData.vehicleType);
        $("#owner").text(userData.owner);
        $("#google-drive").html(
            `<a href="${userData.googleDriveLink}" target="_blank" class="btn btn-info">View Documents</a>`
        );
    }

    // Function to update user status in localStorage (simulating a database)
    function updateUserStatus(status) {
        let applications = JSON.parse(localStorage.getItem("applications")) || {};
        applications[userData.plateNumber] = status; // Use Plate Number as unique ID
        localStorage.setItem("applications", JSON.stringify(applications));
    }

    // Handle Approve action
    $("#btn-approve").click(function () {
        updateUserStatus("Approved");
        alert("Application Approved!");
    });

    // Handle Reject action
    $("#btn-reject").click(function () {
        updateUserStatus("Rejected");
        alert("Application Rejected!");
    });

    // Handle Delete action
    $("#btn-delete").click(function () {
        if (confirm("Are you sure you want to delete this application?")) {
            let applications = JSON.parse(localStorage.getItem("applications")) || {};
            delete applications[userData.plateNumber]; // Remove from storage
            localStorage.setItem("applications", JSON.stringify(applications));

            sessionStorage.removeItem("userDetails"); // Clear session storage
            alert("Application Deleted!");
            window.location.href = "Admin_User.html"; // Redirect back
        }
    });
});
